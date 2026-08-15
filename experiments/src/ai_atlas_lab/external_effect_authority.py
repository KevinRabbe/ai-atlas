from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import random


@dataclass(frozen=True)
class I16Config:
    seed: int = 0
    trials: int = 20_000
    revoke_probability: float = 0.35
    effect_value: float = 1.0
    duplicate_penalty: float = 4.0
    unauthorized_penalty: float = 6.0
    history_error_penalty: float = 1.5
    missed_penalty: float = 1.0
    external_query_cost: float = 0.04


def run_i16(config: I16Config, policy: str) -> dict[str, float]:
    """Separate evidence that an effect happened from authority to try again."""

    valid = {
        "authority_only",
        "evidence_only",
        "revocation_erases_history",
        "separated",
    }
    if policy not in valid:
        raise ValueError(f"unknown I16 policy: {policy}")

    rng = random.Random(config.seed)
    stages = ("absent_unknown", "applied_unknown", "complete")
    weights = (0.28, 0.50, 0.22)
    metrics: dict[str, float] = defaultdict(float)

    for _ in range(config.trials):
        stage = rng.choices(stages, weights)[0]
        applied_before_recovery = stage in {"applied_unknown", "complete"}
        current_authority = rng.random() >= config.revoke_probability
        queried = False

        if stage == "complete":
            believed_applied = True
            retry = False

        elif policy == "authority_only":
            # This policy incorrectly asks permission to stand in for execution
            # history. If allowed it retries without knowing whether the first
            # attempt happened; if revoked it collapses the unknown to absent.
            retry = current_authority
            believed_applied = retry

        else:
            queried = True
            external_receipt_says_applied = applied_before_recovery

            if policy == "evidence_only":
                # Correct execution evidence but incorrectly lets an old intent
                # retry whenever the effect is absent, even after revocation.
                retry = not external_receipt_says_applied
                believed_applied = True

            elif policy == "revocation_erases_history":
                # Re-checks current permission, but incorrectly uses revocation
                # to rewrite the historical fact that the effect already ran.
                if not current_authority:
                    retry = False
                    believed_applied = False
                elif external_receipt_says_applied:
                    retry = False
                    believed_applied = True
                else:
                    retry = True
                    believed_applied = True

            else:  # separated
                if external_receipt_says_applied:
                    # Recording/completing an already-observed effect does not
                    # require permission to execute it again.
                    retry = False
                    believed_applied = True
                else:
                    # A fresh effect is a new consequential transition and is
                    # therefore gated by CURRENT capability authority.
                    retry = current_authority
                    believed_applied = retry

        final_effect_count = int(applied_before_recovery) + int(retry)
        duplicate = final_effect_count > 1
        unauthorized_retry = retry and not current_authority
        missed_while_authorized = final_effect_count < 1 and current_authority
        history_error = believed_applied != (final_effect_count >= 1)

        utility = (
            config.effect_value
            - float(duplicate) * config.duplicate_penalty
            - float(unauthorized_retry) * config.unauthorized_penalty
            - float(missed_while_authorized) * config.missed_penalty
            - float(history_error) * config.history_error_penalty
            - float(queried) * config.external_query_cost
        )

        metrics["utility"] += utility
        metrics["duplicate_effect"] += float(duplicate)
        metrics["unauthorized_retry"] += float(unauthorized_retry)
        metrics["missed_while_authorized"] += float(missed_while_authorized)
        metrics["history_error"] += float(history_error)
        metrics["external_queries"] += float(queried)

    return {key: value / config.trials for key, value in metrics.items()}
