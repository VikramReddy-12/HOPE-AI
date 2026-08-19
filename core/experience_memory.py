"""
HOPE Experience Memory

7J - Outcome & Experience Memory

Purpose:
    Store structured experience records produced by HOPE's
    intelligence pipeline.

Design principles:
    - 7J records experience; it does not execute actions.
    - Experiences are trace-linked to the originating decision.
    - Outcomes may be unavailable initially.
    - Learning remains advisory.
    - Existing decisions cannot be silently overridden.
    - Experience records are structured and deterministic.
    - Self-modification is never authorized.
    - Automatic system-changing action is never authorized.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4


# ============================================================
# VERSION / STATUS
# ============================================================

EXPERIENCE_MEMORY_VERSION = "7J"
EXPERIENCE_MEMORY_STATUS = "READY"

SAFETY_LEVEL = "ADVISORY_ONLY"

EXECUTION_ALLOWED = False
AUTOMATIC_ACTION_ALLOWED = False
SELF_MODIFICATION_ALLOWED = False
DECISION_OVERRIDE_ALLOWED = False


# ============================================================
# TRACE
# ============================================================

TRACE_PREFIX = "7J"


def _utc_timestamp() -> str:
    """Return a UTC ISO-8601 timestamp."""

    return (
        datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _generate_experience_id() -> str:
    """Generate a deterministic-format experience identifier."""

    return (
        f"{TRACE_PREFIX}-EXP-"
        f"{uuid4().hex[:16].upper()}"
    )


# ============================================================
# SAFETY
# ============================================================

def _build_safety() -> Dict[str, Any]:
    """
    Return the immutable 7J safety contract.
    """

    return {
        "safety_level": SAFETY_LEVEL,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
    }


# ============================================================
# EXPERIENCE MODEL
# ============================================================

@dataclass
class ExperienceRecord:
    """
    Structured 7J experience record.
    """

    experience_id: str
    trace_id: str

    decision: str
    confidence: str
    priority: str

    evidence: List[Dict[str, Any]] = field(
        default_factory=list
    )

    contributing_engines: List[str] = field(
        default_factory=list
    )

    response: str = ""

    outcome: Any = None
    outcome_available: bool = False

    outcome_status: str = "PENDING"

    learning_signal: str = "COLLECT_OUTCOME"

    created_at: str = field(
        default_factory=_utc_timestamp
    )

    updated_at: str = field(
        default_factory=_utc_timestamp
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    safety: Dict[str, Any] = field(
        default_factory=_build_safety
    )


# ============================================================
# NORMALIZATION
# ============================================================

def _safe_string(
    value: Any,
    default: str = "",
) -> str:
    """
    Convert arbitrary input into a safe string.
    """

    if value is None:
        return default

    return str(value).strip()


def _safe_list(
    value: Any,
) -> List[Any]:
    """
    Convert arbitrary input into a list.
    """

    if value is None:
        return []

    if isinstance(value, list):
        return list(value)

    if isinstance(value, tuple):
        return list(value)

    return [value]


def _safe_dict(
    value: Any,
) -> Dict[str, Any]:
    """
    Convert arbitrary input into a dictionary.
    """

    if isinstance(value, dict):
        return dict(value)

    return {}


def _normalize_evidence(
    evidence: Any,
) -> List[Dict[str, Any]]:
    """
    Normalize evidence into structured dictionaries.
    """

    normalized: List[Dict[str, Any]] = []

    for item in _safe_list(evidence):
        if isinstance(item, dict):
            normalized.append(dict(item))
        else:
            normalized.append(
                {
                    "value": str(item),
                }
            )

    return normalized


def _normalize_engines(
    contributing_engines: Any,
) -> List[str]:
    """
    Normalize contributing engine identifiers.
    """

    engines: List[str] = []

    for engine in _safe_list(
        contributing_engines
    ):
        value = _safe_string(engine)

        if value and value not in engines:
            engines.append(value)

    return engines


# ============================================================
# OUTCOME CLASSIFICATION
# ============================================================

def _classify_outcome(
    outcome: Any,
    outcome_available: bool,
) -> str:
    """
    Classify the availability of an outcome.

    7J does not infer success or failure from missing data.
    """

    if not outcome_available:
        return "PENDING"

    if outcome is None:
        return "UNKNOWN"

    if isinstance(outcome, dict):
        status = _safe_string(
            outcome.get("status")
        ).upper()

        if status in {
            "SUCCESS",
            "FAILED",
            "PARTIAL",
            "UNKNOWN",
        }:
            return status

        return "RECORDED"

    if isinstance(outcome, bool):
        return (
            "SUCCESS"
            if outcome
            else "FAILED"
        )

    return "RECORDED"


def _determine_learning_signal(
    outcome_status: str,
    outcome_available: bool,
) -> str:
    """
    Determine the safe learning signal.

    No model or decision is modified here.
    """

    if not outcome_available:
        return "COLLECT_OUTCOME"

    if outcome_status == "SUCCESS":
        return "REINFORCE_OBSERVATION"

    if outcome_status == "FAILED":
        return "REVIEW_OUTCOME"

    if outcome_status == "PARTIAL":
        return "REVIEW_OUTCOME"

    return "RECORD_OUTCOME"


# ============================================================
# EXPERIENCE CREATION
# ============================================================

def create_experience(
    trace_id: str,
    decision: Any,
    confidence: Any,
    priority: Any,
    evidence: Any,
    contributing_engines: Any,
    response: Any = "",
    outcome: Any = None,
    outcome_available: bool = False,
    metadata: Optional[
        Dict[str, Any]
    ] = None,
) -> ExperienceRecord:
    """
    Create a new 7J experience record.
    """

    if not trace_id:
        raise ValueError(
            "trace_id cannot be empty."
        )

    normalized_decision = _safe_string(
        decision,
        "UNKNOWN",
    )

    normalized_confidence = _safe_string(
        confidence,
        "UNKNOWN",
    )

    normalized_priority = _safe_string(
        priority,
        "UNKNOWN",
    )

    normalized_evidence = _normalize_evidence(
        evidence
    )

    normalized_engines = _normalize_engines(
        contributing_engines
    )

    normalized_outcome_available = bool(
        outcome_available
    )

    outcome_status = _classify_outcome(
        outcome,
        normalized_outcome_available,
    )

    learning_signal = _determine_learning_signal(
        outcome_status,
        normalized_outcome_available,
    )

    now = _utc_timestamp()

    return ExperienceRecord(
        experience_id=_generate_experience_id(),
        trace_id=trace_id,
        decision=normalized_decision,
        confidence=normalized_confidence,
        priority=normalized_priority,
        evidence=normalized_evidence,
        contributing_engines=normalized_engines,
        response=_safe_string(response),
        outcome=outcome,
        outcome_available=(
            normalized_outcome_available
        ),
        outcome_status=outcome_status,
        learning_signal=learning_signal,
        created_at=now,
        updated_at=now,
        metadata=_safe_dict(metadata),
        safety=_build_safety(),
    )


# ============================================================
# DICTIONARY API
# ============================================================

def create_experience_dict(
    trace_id: str,
    decision: Any,
    confidence: Any,
    priority: Any,
    evidence: Any,
    contributing_engines: Any,
    response: Any = "",
    outcome: Any = None,
    outcome_available: bool = False,
    metadata: Optional[
        Dict[str, Any]
    ] = None,
) -> Dict[str, Any]:
    """
    Create a dictionary representation of an experience.
    """

    record = create_experience(
        trace_id=trace_id,
        decision=decision,
        confidence=confidence,
        priority=priority,
        evidence=evidence,
        contributing_engines=contributing_engines,
        response=response,
        outcome=outcome,
        outcome_available=outcome_available,
        metadata=metadata,
    )

    return asdict(record)


# ============================================================
# OUTCOME UPDATE
# ============================================================

def update_experience_outcome(
    experience: Dict[str, Any],
    outcome: Any,
    outcome_available: bool = True,
) -> Dict[str, Any]:
    """
    Attach an eventual outcome to an existing experience.

    This does not modify the original decision.
    """

    if not isinstance(
        experience,
        dict,
    ):
        raise TypeError(
            "experience must be a dictionary."
        )

    updated = dict(experience)

    available = bool(
        outcome_available
    )

    status = _classify_outcome(
        outcome,
        available,
    )

    signal = _determine_learning_signal(
        status,
        available,
    )

    updated["outcome"] = outcome
    updated["outcome_available"] = available
    updated["outcome_status"] = status
    updated["learning_signal"] = signal
    updated["updated_at"] = _utc_timestamp()

    # Preserve the original decision.
    updated["decision"] = experience.get(
        "decision",
        "UNKNOWN",
    )

    # Re-assert safety.
    updated["safety"] = _build_safety()

    return updated


# ============================================================
# EXPERIENCE VALIDATION
# ============================================================

def validate_experience(
    experience: Any,
) -> Dict[str, Any]:
    """
    Validate a 7J experience record.
    """

    errors: List[str] = []

    if not isinstance(
        experience,
        dict,
    ):
        return {
            "valid": False,
            "errors": [
                "experience must be a dictionary."
            ],
        }

    required_fields = (
        "experience_id",
        "trace_id",
        "decision",
        "confidence",
        "priority",
        "evidence",
        "contributing_engines",
        "outcome_available",
        "outcome_status",
        "learning_signal",
        "safety",
    )

    for field_name in required_fields:
        if field_name not in experience:
            errors.append(
                f"Missing field: {field_name}"
            )

    if not experience.get("trace_id"):
        errors.append(
            "trace_id cannot be empty."
        )

    safety = experience.get(
        "safety",
        {},
    )

    if safety.get(
        "execution_allowed"
    ) is not False:
        errors.append(
            "execution_allowed must remain False."
        )

    if safety.get(
        "automatic_action_allowed"
    ) is not False:
        errors.append(
            "automatic_action_allowed must remain False."
        )

    if safety.get(
        "self_modification_allowed"
    ) is not False:
        errors.append(
            "self_modification_allowed must remain False."
        )

    if safety.get(
        "decision_override_allowed"
    ) is not False:
        errors.append(
            "decision_override_allowed must remain False."
        )

    if not isinstance(
        experience.get(
            "evidence",
            [],
        ),
        list,
    ):
        errors.append(
            "evidence must be a list."
        )

    if not isinstance(
        experience.get(
            "contributing_engines",
            [],
        ),
        list,
    ):
        errors.append(
            "contributing_engines must be a list."
        )

    return {
        "valid": not errors,
        "errors": errors,
    }


# ============================================================
# CONTEXT INTEGRATION
# ============================================================

def integrate_experience_memory(
    context: Any,
    trace_id: str,
    decision: Any,
    confidence: Any,
    priority: Any,
    evidence: Any,
    contributing_engines: Any,
    response: Any = "",
    outcome: Any = None,
    outcome_available: bool = False,
    metadata: Optional[
        Dict[str, Any]
    ] = None,
) -> Dict[str, Any]:
    """
    Store a 7J experience in the shared orchestration context.

    The context must expose:

        update_memory(data)
        snapshot()

    No persistent memory is modified by this function.
    """

    if context is None:
        raise TypeError(
            "context cannot be None."
        )

    if not trace_id:
        raise ValueError(
            "trace_id cannot be empty."
        )

    experience = create_experience_dict(
        trace_id=trace_id,
        decision=decision,
        confidence=confidence,
        priority=priority,
        evidence=evidence,
        contributing_engines=contributing_engines,
        response=response,
        outcome=outcome,
        outcome_available=outcome_available,
        metadata=metadata,
    )

    validation = validate_experience(
        experience
    )

    if not validation["valid"]:
        return {
            "integration_layer": "7J",
            "integration_status": "FAILED",
            "trace_id": trace_id,
            "experience": experience,
            "experience_id": experience.get(
                "experience_id"
            ),
            "outcome_status": experience.get(
                "outcome_status"
            ),
            "learning_signal": experience.get(
                "learning_signal"
            ),
            "context_valid": False,
            "execution_allowed": False,
            "automatic_action_allowed": False,
            "self_modification_allowed": False,
            "decision_override_allowed": False,
            "errors": validation["errors"],
        }

    context.update_memory(
        {
            "experience_memory": experience,
        }
    )

    context_valid = True
    context_errors: List[str] = []

    try:
        from core.orchestration_context import (
            validate_context,
        )

        context_validation = validate_context(
            context
        )

        context_valid = bool(
            context_validation.get(
                "valid",
                False,
            )
        )

        context_errors = list(
            context_validation.get(
                "errors",
                [],
            )
        )

    except Exception as exc:
        context_valid = False
        context_errors.append(
            f"Context validation failed: {exc}"
        )

    return {
        "integration_layer": "7J",
        "integration_status": (
            "READY"
            if context_valid
            else "FAILED"
        ),
        "trace_id": trace_id,
        "experience_id": experience[
            "experience_id"
        ],
        "experience": experience,
        "decision": experience[
            "decision"
        ],
        "confidence": experience[
            "confidence"
        ],
        "priority": experience[
            "priority"
        ],
        "evidence": experience[
            "evidence"
        ],
        "contributing_engines": experience[
            "contributing_engines"
        ],
        "outcome": experience[
            "outcome"
        ],
        "outcome_available": experience[
            "outcome_available"
        ],
        "outcome_status": experience[
            "outcome_status"
        ],
        "learning_signal": experience[
            "learning_signal"
        ],
        "context_valid": context_valid,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
        "errors": context_errors,
    }


# ============================================================
# STATUS
# ============================================================

def get_experience_memory_status() -> Dict[str, Any]:
    """
    Return 7J capability status.
    """

    safety = _build_safety()

    return {
        "version": EXPERIENCE_MEMORY_VERSION,
        "status": EXPERIENCE_MEMORY_STATUS,
        "safety_level": safety[
            "safety_level"
        ],
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
        "safety_valid": (
            safety[
                "execution_allowed"
            ] is False
            and safety[
                "automatic_action_allowed"
            ] is False
            and safety[
                "self_modification_allowed"
            ] is False
            and safety[
                "decision_override_allowed"
            ] is False
        ),
    }


# ============================================================
# 7J REGRESSION
# ============================================================

def get_experience_memory_regression() -> Dict[str, Any]:
    """
    Run the standalone 7J experience-memory regression.
    """

    trace_id = "7J-REGRESSION"

    experience = create_experience_dict(
        trace_id=trace_id,
        decision="MONITOR",
        confidence="LOW",
        priority="MEDIUM",
        evidence=[
            {
                "source": "reasoning",
                "value": "Reasoning evidence",
            },
            {
                "source": "predictive",
                "value": "Predictive evidence",
            },
        ],
        contributing_engines=[
            "reasoning",
            "predictive",
        ],
        response=(
            "Continued monitoring is recommended."
        ),
        outcome=None,
        outcome_available=False,
    )

    validation = validate_experience(
        experience
    )

    updated = update_experience_outcome(
        experience,
        {
            "status": "SUCCESS",
            "note": "Observed outcome recorded.",
        },
        outcome_available=True,
    )

    checks = {
        "status_ready": (
            EXPERIENCE_MEMORY_STATUS == "READY"
        ),
        "layer_7j": (
            EXPERIENCE_MEMORY_VERSION == "7J"
        ),
        "trace_preserved": (
            experience["trace_id"]
            == trace_id
        ),
        "experience_id_generated": bool(
            experience.get(
                "experience_id"
            )
        ),
        "decision_preserved": (
            experience["decision"]
            == "MONITOR"
        ),
        "confidence_preserved": (
            experience["confidence"]
            == "LOW"
        ),
        "priority_preserved": (
            experience["priority"]
            == "MEDIUM"
        ),
        "evidence_preserved": (
            len(
                experience["evidence"]
            ) == 2
        ),
        "engines_preserved": (
            experience[
                "contributing_engines"
            ]
            == [
                "reasoning",
                "predictive",
            ]
        ),
        "pending_without_outcome": (
            experience[
                "outcome_status"
            ]
            == "PENDING"
        ),
        "collect_signal_without_outcome": (
            experience[
                "learning_signal"
            ]
            == "COLLECT_OUTCOME"
        ),
        "validation_passed": (
            validation["valid"]
        ),
        "outcome_recorded": (
            updated[
                "outcome_available"
            ]
            is True
        ),
        "outcome_status_updated": (
            updated[
                "outcome_status"
            ]
            == "SUCCESS"
        ),
        "learning_signal_updated": (
            updated[
                "learning_signal"
            ]
            == "REINFORCE_OBSERVATION"
        ),
        "decision_not_overridden": (
            updated[
                "decision"
            ]
            == experience[
                "decision"
            ]
        ),
        "safety_advisory": (
            experience[
                "safety"
            ]["safety_level"]
            == "ADVISORY_ONLY"
        ),
        "execution_blocked": (
            experience[
                "safety"
            ]["execution_allowed"]
            is False
        ),
        "automatic_action_blocked": (
            experience[
                "safety"
            ]["automatic_action_allowed"]
            is False
        ),
        "self_modification_blocked": (
            experience[
                "safety"
            ]["self_modification_allowed"]
            is False
        ),
        "decision_override_blocked": (
            experience[
                "safety"
            ]["decision_override_allowed"]
            is False
        ),
    }

    return {
        "integration_layer": "7J",
        "integration_status": (
            "READY"
            if all(checks.values())
            else "FAILED"
        ),
        "trace_id": trace_id,
        "experience_id": experience[
            "experience_id"
        ],
        "decision": experience[
            "decision"
        ],
        "confidence": experience[
            "confidence"
        ],
        "priority": experience[
            "priority"
        ],
        "evidence": experience[
            "evidence"
        ],
        "engines": experience[
            "contributing_engines"
        ],
        "outcome_status": experience[
            "outcome_status"
        ],
        "learning_signal": experience[
            "learning_signal"
        ],
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
        "checks": checks,
        "regression_passed": all(
            checks.values()
        ),
    }