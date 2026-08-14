from __future__ import annotations

from dataclasses import dataclass, replace
import json
import random
import struct
import zlib
from typing import Protocol

from .core import CostMeter


@dataclass(frozen=True)
class InterfaceState:
    entity_id: int
    action: int
    score: float
    target_id: int
    constraint: int
    flags: int
    priority: int = 0


class Representation(Protocol):
    name: str
    def encode(self, state: InterfaceState, version: int, cost: CostMeter) -> bytes: ...
    def decode(self, payload: bytes, consumer_version: int, cost: CostMeter) -> InterfaceState: ...
    def audit_view(self, payload: bytes, consumer_version: int, cost: CostMeter) -> str: ...
    def corrupt_critical_byte(self, payload: bytes, rng: random.Random) -> bytes: ...


class TextJSONRepresentation:
    name = "human_readable_json"

    def encode(self, state: InterfaceState, version: int, cost: CostMeter) -> bytes:
        data = {"entity_id": state.entity_id, "action": state.action, "score": state.score, "target_id": state.target_id, "constraint": state.constraint, "flags": state.flags}
        if version >= 2:
            data["priority"] = state.priority
        payload = json.dumps(data, separators=(",", ":"), sort_keys=True).encode("utf-8")
        cost.operations += len(data) + 1
        cost.reads += len(data)
        return payload

    def decode(self, payload: bytes, consumer_version: int, cost: CostMeter) -> InterfaceState:
        data = json.loads(payload.decode("utf-8"))
        required = ("entity_id", "action", "score", "target_id", "constraint", "flags")
        if any(key not in data for key in required):
            raise ValueError("missing required field")
        cost.operations += len(data) + 1
        cost.reads += len(data)
        return InterfaceState(int(data["entity_id"]), int(data["action"]), float(data["score"]), int(data["target_id"]), int(data["constraint"]), int(data["flags"]), int(data.get("priority", 0)) if consumer_version >= 2 else 0)

    def audit_view(self, payload: bytes, consumer_version: int, cost: CostMeter) -> str:
        return payload.decode("utf-8", errors="replace")

    def corrupt_critical_byte(self, payload: bytes, rng: random.Random) -> bytes:
        data = bytearray(payload)
        idx = rng.randrange(len(data))
        data[idx] ^= 0x01
        return bytes(data)


class ContinuousVectorRepresentation:
    name = "opaque_float32_vector"

    def encode(self, state: InterfaceState, version: int, cost: CostMeter) -> bytes:
        values = [float(state.entity_id), float(state.action), float(state.score)]
        if version >= 2:
            values.append(float(state.priority))
        values.extend([float(state.target_id), float(state.constraint), float(state.flags)])
        cost.operations += len(values)
        cost.reads += len(values)
        return struct.pack(f"!{len(values)}f", *values)

    def decode(self, payload: bytes, consumer_version: int, cost: CostMeter) -> InterfaceState:
        expected = 7 if consumer_version >= 2 else 6
        if len(payload) != expected * 4:
            raise ValueError("vector schema length mismatch")
        values = struct.unpack(f"!{expected}f", payload)
        cost.operations += expected
        cost.reads += expected
        if consumer_version >= 2:
            entity, action, score, priority, target, constraint, flags = values
        else:
            entity, action, score, target, constraint, flags = values
            priority = 0.0
        return InterfaceState(int(round(entity)), int(round(action)), float(score), int(round(target)), int(round(constraint)), int(round(flags)), int(round(priority)))

    def audit_view(self, payload: bytes, consumer_version: int, cost: CostMeter) -> str:
        state = self.decode(payload, consumer_version, cost)
        cost.operations += 2
        return _audit_json(state, consumer_version)

    def corrupt_critical_byte(self, payload: bytes, rng: random.Random) -> bytes:
        data = bytearray(payload)
        idx = rng.randrange(len(data))
        data[idx] ^= 0x01
        return bytes(data)


_TAGS = {1: ("entity_id", "!I"), 2: ("action", "!B"), 3: ("score", "!f"), 4: ("target_id", "!I"), 5: ("constraint", "!i"), 6: ("flags", "!H"), 7: ("priority", "!B")}
_NAME_TO_TAG = {name: (tag, fmt) for tag, (name, fmt) in _TAGS.items()}


def _tlv_core(state: InterfaceState, version: int, cost: CostMeter) -> bytes:
    names = ["entity_id", "action", "score", "target_id", "constraint", "flags"]
    if version >= 2:
        names.append("priority")
    body = bytearray()
    for name in names:
        tag, fmt = _NAME_TO_TAG[name]
        value_bytes = struct.pack(fmt, getattr(state, name))
        body.extend((tag, len(value_bytes)))
        body.extend(value_bytes)
    checksum = zlib.crc32(body) & 0xFFFFFFFF
    cost.operations += len(names) * 2 + 1
    cost.reads += len(names)
    return bytes(body) + struct.pack("!I", checksum)


def _parse_tlv_core(payload: bytes, consumer_version: int, cost: CostMeter) -> InterfaceState:
    if len(payload) < 4:
        raise ValueError("payload too short")
    body, checksum_bytes = payload[:-4], payload[-4:]
    expected_crc = struct.unpack("!I", checksum_bytes)[0]
    if (zlib.crc32(body) & 0xFFFFFFFF) != expected_crc:
        raise ValueError("checksum mismatch")
    values: dict[str, int | float] = {}
    idx = 0
    while idx < len(body):
        if idx + 2 > len(body):
            raise ValueError("truncated TLV header")
        tag, length = body[idx], body[idx + 1]
        idx += 2
        if idx + length > len(body):
            raise ValueError("truncated TLV value")
        raw = body[idx : idx + length]
        idx += length
        if tag not in _TAGS:
            continue
        name, fmt = _TAGS[tag]
        if struct.calcsize(fmt) != length:
            raise ValueError("invalid TLV size")
        values[name] = struct.unpack(fmt, raw)[0]
        cost.operations += 2
        cost.reads += 1
    required = ("entity_id", "action", "score", "target_id", "constraint", "flags")
    if any(name not in values for name in required):
        raise ValueError("missing required field")
    return InterfaceState(int(values["entity_id"]), int(values["action"]), float(values["score"]), int(values["target_id"]), int(values["constraint"]), int(values["flags"]), int(values.get("priority", 0)) if consumer_version >= 2 else 0)


class StructuredTLVRepresentation:
    name = "structured_tagged_binary"

    def encode(self, state: InterfaceState, version: int, cost: CostMeter) -> bytes:
        return _tlv_core(state, version, cost)

    def decode(self, payload: bytes, consumer_version: int, cost: CostMeter) -> InterfaceState:
        return _parse_tlv_core(payload, consumer_version, cost)

    def audit_view(self, payload: bytes, consumer_version: int, cost: CostMeter) -> str:
        state = self.decode(payload, consumer_version, cost)
        cost.operations += 1
        return _audit_json(state, consumer_version)

    def corrupt_critical_byte(self, payload: bytes, rng: random.Random) -> bytes:
        data = bytearray(payload)
        idx = rng.randrange(max(1, len(data) - 4))
        data[idx] ^= 0x01
        return bytes(data)


_HYBRID_SEPARATOR = b"\n--AUDIT--\n"


class HybridRepresentation:
    name = "hybrid_structured_plus_audit"

    def encode(self, state: InterfaceState, version: int, cost: CostMeter) -> bytes:
        core = _tlv_core(state, version, cost)
        audit = _audit_json(state, version).encode("utf-8")
        cost.operations += 1
        cost.reads += 1
        return core + _HYBRID_SEPARATOR + audit

    def decode(self, payload: bytes, consumer_version: int, cost: CostMeter) -> InterfaceState:
        core, sep, audit = payload.partition(_HYBRID_SEPARATOR)
        if not sep:
            raise ValueError("missing hybrid separator")
        try:
            return _parse_tlv_core(core, consumer_version, cost)
        except ValueError:
            data = json.loads(audit.decode("utf-8"))
            cost.operations += 4
            cost.reads += len(data)
            return InterfaceState(int(data["entity_id"]), int(data["action"]), float(data["score"]), int(data["target_id"]), int(data["constraint"]), int(data["flags"]), int(data.get("priority", 0)) if consumer_version >= 2 else 0)

    def audit_view(self, payload: bytes, consumer_version: int, cost: CostMeter) -> str:
        _core, sep, audit = payload.partition(_HYBRID_SEPARATOR)
        if not sep:
            raise ValueError("missing hybrid separator")
        return audit.decode("utf-8")

    def corrupt_critical_byte(self, payload: bytes, rng: random.Random) -> bytes:
        core, sep, audit = payload.partition(_HYBRID_SEPARATOR)
        data = bytearray(core)
        idx = rng.randrange(max(1, len(data) - 4))
        data[idx] ^= 0x01
        return bytes(data) + sep + audit


def _audit_json(state: InterfaceState, version: int) -> str:
    data = {"entity_id": state.entity_id, "action": state.action, "score": round(state.score, 6), "target_id": state.target_id, "constraint": state.constraint, "flags": state.flags}
    if version >= 2:
        data["priority"] = state.priority
    return json.dumps(data, separators=(",", ":"), sort_keys=True)


def _state_matches(expected: InterfaceState, actual: InterfaceState, consumer_version: int) -> bool:
    return expected.entity_id == actual.entity_id and expected.action == actual.action and abs(expected.score - actual.score) <= 1e-5 and expected.target_id == actual.target_id and expected.constraint == actual.constraint and expected.flags == actual.flags and (consumer_version < 2 or expected.priority == actual.priority)


@dataclass(frozen=True)
class RepresentationExperimentConfig:
    seed: int = 0
    state_count: int = 800
    bandwidth_cap_bytes: int = 48
    corruption_trials: int = 250
    relay_hops: int = 6


def generate_interface_states(config: RepresentationExperimentConfig) -> tuple[InterfaceState, ...]:
    rng = random.Random(config.seed)
    return tuple(InterfaceState(rng.randint(20_000_000, 1_500_000_000), rng.randrange(8), rng.uniform(-3.0, 3.0), rng.randint(20_000_000, 1_500_000_000), rng.randint(-2_000_000_000, 2_000_000_000), rng.randrange(65536), rng.randrange(8)) for _ in range(config.state_count))


def _evaluate_representation(representation: Representation, states: tuple[InterfaceState, ...], config: RepresentationExperimentConfig) -> tuple[dict[str, float | int], CostMeter]:
    cost = CostMeter()
    encoded_sizes: list[int] = []
    roundtrip_ok = exact_discrete_ok = action_ok = priority_ok = bandwidth_success = audit_ok = cross_version_ok = relay_ok = decoded_count = 0
    score_abs_error = 0.0

    for state in states:
        payload = representation.encode(state, version=2, cost=cost)
        encoded_sizes.append(len(payload))
        try:
            decoded = representation.decode(payload, consumer_version=2, cost=cost)
            roundtrip_ok += int(_state_matches(state, decoded, 2))
            exact_discrete_ok += int(state.entity_id == decoded.entity_id and state.target_id == decoded.target_id and state.constraint == decoded.constraint and state.flags == decoded.flags)
            action_ok += int(state.action == decoded.action)
            priority_ok += int(state.priority == decoded.priority)
            score_abs_error += abs(state.score - decoded.score)
            decoded_count += 1
        except (ValueError, json.JSONDecodeError, struct.error, UnicodeDecodeError):
            pass
        if len(payload) <= config.bandwidth_cap_bytes:
            bandwidth_success += 1
        try:
            view = representation.audit_view(payload, 2, cost)
            audit_ok += int(str(state.entity_id) in view and str(state.target_id) in view)
        except (ValueError, json.JSONDecodeError, struct.error, UnicodeDecodeError):
            pass
        try:
            old_view = representation.decode(payload, consumer_version=1, cost=cost)
            cross_version_ok += int(_state_matches(replace(state, priority=0), old_view, 1))
        except (ValueError, json.JSONDecodeError, struct.error, UnicodeDecodeError):
            pass
        try:
            relay_state = state
            for _ in range(config.relay_hops):
                relay_payload = representation.encode(relay_state, version=2, cost=cost)
                relay_state = representation.decode(relay_payload, consumer_version=2, cost=cost)
            relay_ok += int(_state_matches(state, relay_state, 2))
        except (ValueError, json.JSONDecodeError, struct.error, UnicodeDecodeError):
            pass

    corruption_detected = corruption_recovered = 0
    rng = random.Random(config.seed + 443)
    trials = min(config.corruption_trials, len(states))
    for idx in range(trials):
        state = states[idx]
        payload = representation.encode(state, version=2, cost=cost)
        corrupted = representation.corrupt_critical_byte(payload, rng)
        try:
            decoded = representation.decode(corrupted, consumer_version=2, cost=cost)
            if _state_matches(state, decoded, 2):
                corruption_recovered += 1
        except (ValueError, json.JSONDecodeError, struct.error, UnicodeDecodeError):
            corruption_detected += 1

    n = len(states)
    metrics: dict[str, float | int] = {
        "roundtrip_state_accuracy": roundtrip_ok / n,
        "exact_discrete_field_accuracy": exact_discrete_ok / n,
        "action_accuracy": action_ok / n,
        "priority_accuracy": priority_ok / n,
        "mean_score_abs_error": score_abs_error / max(1, decoded_count),
        "avg_payload_bytes": sum(encoded_sizes) / n,
        "max_payload_bytes": max(encoded_sizes),
        "bandwidth_cap_success_rate": bandwidth_success / n,
        "audit_faithfulness_rate": audit_ok / n,
        "new_producer_old_consumer_compatibility": cross_version_ok / n,
        "multi_hop_exact_rate": relay_ok / n,
        "corruption_detection_rate": corruption_detected / trials,
        "corruption_recovery_rate": corruption_recovered / trials,
        "logical_operations_per_state": cost.operations / n,
    }
    return metrics, cost


def run_representation_experiment(config: RepresentationExperimentConfig) -> list[tuple[str, dict[str, float | int], CostMeter]]:
    states = generate_interface_states(config)
    representations: list[Representation] = [TextJSONRepresentation(), ContinuousVectorRepresentation(), StructuredTLVRepresentation(), HybridRepresentation()]
    return [(representation.name, *_evaluate_representation(representation, states, config)) for representation in representations]
