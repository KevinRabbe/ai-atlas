from __future__ import annotations

from dataclasses import dataclass
import json
import math
import random
import struct
import zlib
from typing import Protocol

from .core import CostMeter

MAX_STACK = 4


@dataclass(frozen=True)
class SearchState:
    node_id: int
    stack: tuple[int, ...]
    forbidden: tuple[int, int]
    scores: tuple[float, float, float, float]
    mode: int
    budget: int = 0


def search_decision(state: SearchState) -> int:
    if state.node_id in state.forbidden:
        return 0  # backtrack
    margin = 1.2 * state.scores[0] - 0.8 * state.scores[1] + 0.5 * state.scores[2] + state.scores[3]
    if margin > 0.15:
        return 1  # expand
    if state.stack and margin < -0.2:
        return 0
    return 2  # verify


@dataclass(frozen=True)
class SearchRepresentationConfig:
    seed: int = 0
    calibration_count: int = 1200
    test_count: int = 1000
    bandwidth_cap: int = 44
    shifted_fraction: float = 0.25
    corruption_trials: int = 200


def generate_search_states(seed: int, count: int, shifted_fraction: float = 0.0) -> tuple[SearchState, ...]:
    rng = random.Random(seed)
    out: list[SearchState] = []
    for _ in range(count):
        node = rng.randint(30_000_000, 1_500_000_000)
        stack_len = rng.randrange(MAX_STACK + 1)
        stack = tuple(rng.randrange(8) for _ in range(stack_len))
        q = rng.random()
        if q < 0.25:
            forbidden = (node, rng.randint(30_000_000, 1_500_000_000))
        elif q < 0.55:
            forbidden = (node + rng.choice((-8, -4, -2, -1, 1, 2, 4, 8)), rng.randint(30_000_000, 1_500_000_000))
        else:
            forbidden = (rng.randint(30_000_000, 1_500_000_000), rng.randint(30_000_000, 1_500_000_000))
        shifted = rng.random() < shifted_fraction
        mean, sigma = (0.8, 1.45) if shifted else (0.0, 1.0)
        scores = tuple(rng.gauss(mean, sigma) for _ in range(4))
        out.append(SearchState(node, stack, forbidden, scores, rng.randrange(3), rng.randrange(1000)))
    return tuple(out)


class Representation(Protocol):
    name: str
    def encode(self, state: SearchState, version: int, cost: CostMeter) -> bytes: ...
    def decode(self, payload: bytes, consumer_version: int, cost: CostMeter) -> SearchState: ...
    def corrupt(self, payload: bytes, rng: random.Random) -> bytes: ...


class SearchJSON:
    name = "search_json"

    def encode(self, state: SearchState, version: int, cost: CostMeter) -> bytes:
        data = {"node": state.node_id, "stack": list(state.stack), "forbidden": list(state.forbidden), "scores": list(state.scores), "mode": state.mode}
        if version >= 2:
            data["budget"] = state.budget
        cost.operations += len(data)
        return json.dumps(data, separators=(",", ":"), sort_keys=True).encode("utf-8")

    def decode(self, payload: bytes, consumer_version: int, cost: CostMeter) -> SearchState:
        data = json.loads(payload)
        cost.operations += len(data)
        return SearchState(int(data["node"]), tuple(map(int, data["stack"])), tuple(map(int, data["forbidden"])), tuple(map(float, data["scores"])), int(data["mode"]), int(data.get("budget", 0)) if consumer_version >= 2 else 0)

    def corrupt(self, payload: bytes, rng: random.Random) -> bytes:
        data = bytearray(payload)
        data[rng.randrange(len(data))] ^= 1
        return bytes(data)


class SearchFloat32Vector:
    name = "search_float32_vector"

    def encode(self, state: SearchState, version: int, cost: CostMeter) -> bytes:
        values = [float(state.node_id), float(len(state.stack))]
        values.extend(float(x) for x in state.stack)
        values.extend([-1.0] * (MAX_STACK - len(state.stack)))
        values.extend((float(state.forbidden[0]), float(state.forbidden[1])))
        values.extend(state.scores)
        values.append(float(state.mode))
        if version >= 2:
            values.append(float(state.budget))
        cost.operations += len(values)
        return struct.pack(f"!{len(values)}f", *values)

    def decode(self, payload: bytes, consumer_version: int, cost: CostMeter) -> SearchState:
        count = 14 if consumer_version >= 2 else 13
        if len(payload) != count * 4:
            raise ValueError("vector schema length mismatch")
        values = struct.unpack(f"!{count}f", payload)
        cost.operations += count
        stack_len = max(0, min(MAX_STACK, int(round(values[1]))))
        stack = tuple(int(round(x)) for x in values[2 : 2 + stack_len])
        offset = 2 + MAX_STACK
        budget = int(round(values[-1])) if consumer_version >= 2 else 0
        return SearchState(int(round(values[0])), stack, (int(round(values[offset])), int(round(values[offset + 1]))), tuple(float(x) for x in values[offset + 2 : offset + 6]), int(round(values[offset + 6])), budget)

    def corrupt(self, payload: bytes, rng: random.Random) -> bytes:
        data = bytearray(payload)
        data[rng.randrange(len(data))] ^= 1
        return bytes(data)


class SearchStructuredBinary:
    name = "search_structured_binary"

    def encode(self, state: SearchState, version: int, cost: CostMeter) -> bytes:
        body = bytearray([version])
        body.extend(struct.pack("!I", state.node_id))
        body.append(len(state.stack))
        body.extend(bytes(state.stack))
        body.extend(struct.pack("!II", *state.forbidden))
        body.extend(struct.pack("!4f", *state.scores))
        body.append(state.mode)
        if version >= 2:
            body.extend(struct.pack("!H", state.budget))
        cost.operations += 12 + len(state.stack)
        return bytes(body) + struct.pack("!I", zlib.crc32(body) & 0xFFFFFFFF)

    def decode(self, payload: bytes, consumer_version: int, cost: CostMeter) -> SearchState:
        body, crc_bytes = payload[:-4], payload[-4:]
        if len(body) < 30 or (zlib.crc32(body) & 0xFFFFFFFF) != struct.unpack("!I", crc_bytes)[0]:
            raise ValueError("invalid structured payload")
        idx = 0
        producer_version = body[idx]; idx += 1
        node = struct.unpack("!I", body[idx:idx+4])[0]; idx += 4
        stack_len = body[idx]; idx += 1
        stack = tuple(body[idx:idx+stack_len]); idx += stack_len
        forbidden = struct.unpack("!II", body[idx:idx+8]); idx += 8
        scores = struct.unpack("!4f", body[idx:idx+16]); idx += 16
        mode = body[idx]; idx += 1
        budget = 0
        if producer_version >= 2 and idx + 2 <= len(body):
            raw_budget = struct.unpack("!H", body[idx:idx+2])[0]
            if consumer_version >= 2:
                budget = raw_budget
        cost.operations += 12 + stack_len
        return SearchState(node, stack, forbidden, scores, mode, budget)

    def corrupt(self, payload: bytes, rng: random.Random) -> bytes:
        data = bytearray(payload)
        data[rng.randrange(max(1, len(data) - 4))] ^= 1
        return bytes(data)


class LearnedQuantizedExactSide:
    name = "learned_quantized_exact_side"

    def __init__(self, calibration: tuple[SearchState, ...]) -> None:
        self.means: list[float] = []
        self.stds: list[float] = []
        for index in range(4):
            values = [state.scores[index] for state in calibration]
            mean = sum(values) / len(values)
            variance = sum((value - mean) ** 2 for value in values) / len(values)
            self.means.append(mean)
            self.stds.append(math.sqrt(variance) or 1.0)

    def _quantize(self, value: float, index: int) -> int:
        z = (value - self.means[index]) / self.stds[index]
        z = max(-3.0, min(3.0, z))
        return int(round(z / 3.0 * 127))

    def _dequantize(self, value: int, index: int) -> float:
        return self.means[index] + (value / 127.0 * 3.0) * self.stds[index]

    def encode(self, state: SearchState, version: int, cost: CostMeter) -> bytes:
        body = bytearray([version])
        body.extend(struct.pack("!I", state.node_id))
        body.append(len(state.stack))
        body.extend(bytes(state.stack))
        body.extend(struct.pack("!II", *state.forbidden))
        body.extend(struct.pack("!4b", *(self._quantize(value, index) for index, value in enumerate(state.scores))))
        body.append(state.mode)
        if version >= 2:
            body.extend(struct.pack("!H", state.budget))
        cost.operations += 24 + len(state.stack)
        return bytes(body) + struct.pack("!I", zlib.crc32(body) & 0xFFFFFFFF)

    def decode(self, payload: bytes, consumer_version: int, cost: CostMeter) -> SearchState:
        body, crc_bytes = payload[:-4], payload[-4:]
        if len(body) < 18 or (zlib.crc32(body) & 0xFFFFFFFF) != struct.unpack("!I", crc_bytes)[0]:
            raise ValueError("invalid learned-side payload")
        idx = 0
        producer_version = body[idx]; idx += 1
        node = struct.unpack("!I", body[idx:idx+4])[0]; idx += 4
        stack_len = body[idx]; idx += 1
        stack = tuple(body[idx:idx+stack_len]); idx += stack_len
        forbidden = struct.unpack("!II", body[idx:idx+8]); idx += 8
        quantized = struct.unpack("!4b", body[idx:idx+4]); idx += 4
        scores = tuple(self._dequantize(value, index) for index, value in enumerate(quantized))
        mode = body[idx]; idx += 1
        budget = 0
        if producer_version >= 2 and idx + 2 <= len(body):
            raw_budget = struct.unpack("!H", body[idx:idx+2])[0]
            if consumer_version >= 2:
                budget = raw_budget
        cost.operations += 16 + stack_len
        return SearchState(node, stack, forbidden, scores, mode, budget)

    def corrupt(self, payload: bytes, rng: random.Random) -> bytes:
        data = bytearray(payload)
        data[rng.randrange(max(1, len(data) - 4))] ^= 1
        return bytes(data)


def evaluate_search_representation(rep: Representation, states: tuple[SearchState, ...], config: SearchRepresentationConfig) -> tuple[dict[str, float | int], CostMeter]:
    cost = CostMeter()
    exact = decisions = compatibility = corruption_detected = 0
    score_error = 0.0
    sizes: list[int] = []
    for state in states:
        payload = rep.encode(state, 2, cost)
        sizes.append(len(payload))
        try:
            decoded = rep.decode(payload, 2, cost)
        except Exception:
            continue
        exact += int(state.node_id == decoded.node_id and state.stack == decoded.stack and state.forbidden == decoded.forbidden and state.mode == decoded.mode and state.budget == decoded.budget)
        decisions += int(search_decision(state) == search_decision(decoded))
        score_error += sum(abs(a - b) for a, b in zip(state.scores, decoded.scores)) / 4
        try:
            old = rep.decode(payload, 1, cost)
            compatibility += int(state.node_id == old.node_id and state.stack == old.stack and state.forbidden == old.forbidden and state.mode == old.mode)
        except Exception:
            pass

    rng = random.Random(config.seed + 99)
    trials = min(config.corruption_trials, len(states))
    for index in range(trials):
        corrupted = rep.corrupt(rep.encode(states[index], 2, cost), rng)
        try:
            rep.decode(corrupted, 2, cost)
        except Exception:
            corruption_detected += 1

    count = len(states)
    return {
        "decision_accuracy": decisions / count,
        "exact_structural_accuracy": exact / count,
        "mean_score_abs_error": score_error / count,
        "avg_payload_bytes": sum(sizes) / count,
        "bandwidth_success_rate": sum(size <= config.bandwidth_cap for size in sizes) / count,
        "version_compatibility": compatibility / count,
        "corruption_detection_rate": corruption_detected / trials,
    }, cost


def run_search_representation_experiment(config: SearchRepresentationConfig) -> list[tuple[str, dict[str, float | int], CostMeter]]:
    calibration = generate_search_states(config.seed + 10, config.calibration_count, 0.0)
    tests = generate_search_states(config.seed + 20, config.test_count, config.shifted_fraction)
    representations: list[Representation] = [SearchJSON(), SearchFloat32Vector(), SearchStructuredBinary(), LearnedQuantizedExactSide(calibration)]
    return [(rep.name, *evaluate_search_representation(rep, tests, config)) for rep in representations]
