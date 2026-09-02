"""
HOPE Adaptive Experience Intelligence

8G - Adaptive Experience Intelligence

Purpose:
    Convert validated experience and learning information into a
    structured advisory experience assessment for future HOPE
    orchestration.

Design principles:
    - 8G consumes existing 7J experience and 8F learning outputs.
    - Experience is preserved, not rewritten.
    - Learning signals are preserved, not fabricated.
    - Adaptation remains advisory only.
    - No automatic execution is permitted.
    - No self-modification is permitted.
    - No decision override is permitted.
    - Traceability is preserved.
    - Existing decision confidence and priority are preserved.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


# ============================================================
# VERSION / STATUS
# ============================================================

ADAPTIVE_EXPERIENCE_VERSION = "8G"
ADAPTIVE_EXPERIENCE_STATUS = "READY"

SAFETY_LEVEL = "ADVISORY_ONLY"

EXECUTION_ALLOWED = False
AUTOMATIC_ACTION_ALLOWED = False
SELF_MODIFICATION_ALLOWED = False
DECISION_OVERRIDE_ALLOWED = False

TRACE_PREFIX = "8G"


# ============================================================
# SAFETY
# ============================================================

def _build_safety() -> Dict[str, Any]:
    """
    Return the immutable 8G safety contract.
    """

    return {
        "safety_level": SAFETY_LEVEL,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
    }


def validate_adaptive_experience_safety() -> bool:
    """
    Validate the 8G safety contract.
    """

    return (
        SAFETY_LEVEL == "ADVISORY_ONLY"
        and EXECUTION_ALLOWED is False
        and AUTOMATIC_ACTION_ALLOWED is False
        and SELF_MODIFICATION_ALLOWED is False
        and DECISION_OVERRIDE_ALLOWED is False
    )


# ============================================================
# NORMALIZATION
# ============================================================

def _safe_string(
    value: Any,
    default: str = "",
) -> str:
    """
    Convert a value into a safe string.
    """

    if value is None:
        return default

    value = str(value).strip()

    return value if value else default


def _safe_dict(
    value: Any,
) -> Dict[str, Any]:
    """
    Return a defensive dictionary copy.
    """

    if isinstance(value, dict):
        return dict(value)

    return {}


def _safe_list(
    value: Any,
) -> List[Any]:
    """
    Return a defensive list copy.
    """

    if isinstance(value, list):
        return list(value)

    if isinstance(value, tuple):
        return list(value)

    return []


# ============================================================
# RESULT MODEL
# ============================================================

@dataclass
class AdaptiveExperienceResult:
    """
    Structured 8G adaptive experience result.
    """

    trace_id: str

    status: str

    experience_id: str

    decision: str
    confidence: str
    priority: str

    adaptation_state: str

    experience_status: str
    learning_signal: str

    adaptation_recommendation: str

    evidence: List[Dict[str, Any]] = field(
        default_factory=list
    )

    contributing_engines: List[str] = field(
        default_factory=list
    )

    safety: Dict[str, Any] = field(
        default_factory=_build_safety
    )

    errors: List[str] = field(
        default_factory=list
    )


# ============================================================
# TRACE
# ============================================================

def _preserve_trace(
    value: Any,
) -> str:
    """
    Preserve the originating trace ID.
    """

    return _safe_string(
        value,
        "8G-TRACE-UNAVAILABLE",
    )


# ============================================================
# EXPERIENCE EXTRACTION
# ============================================================

def _extract_experience(
    experience: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Preserve existing experience information.
    """

    experience = _safe_dict(experience)

    experience_id = _safe_string(
        experience.get("experience_id"),
        "EXPERIENCE_UNAVAILABLE",
    )

    experience_status = _safe_string(
        experience.get("outcome_status"),
        "PENDING",
    )

    return {
        "experience_id": experience_id,
        "experience_status": experience_status,
        "outcome": experience.get("outcome"),
        "outcome_available": bool(
            experience.get(
                "outcome_available",
                False,
            )
        ),
    }


# ============================================================
# LEARNING EXTRACTION
# ============================================================

def _extract_learning(
    learning: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Preserve existing learning-feedback information.
    """

    learning = _safe_dict(learning)

    return {
        "learning_signal": _safe_string(
            learning.get("learning_signal"),
            "INSUFFICIENT_DATA",
        ),
        "learning_recommendation": _safe_string(
            learning.get(
                "learning_recommendation"
            ),
            "No learning recommendation available.",
        ),
        "feedback_status": _safe_string(
            learning.get("feedback_status"),
            "MISSING_FEEDBACK",
        ),
        "feedback_quality": _safe_string(
            learning.get("feedback_quality"),
            "INSUFFICIENT",
        ),
    }


# ============================================================
# ADAPTATION STATE
# ============================================================

def _derive_adaptation_state(
    experience: Dict[str, Any],
    learning: Dict[str, Any],
) -> str:
    """
    Derive a conservative adaptation state.

    This does not modify decisions or system state.
    """

    outcome_available = bool(
        experience.get(
            "outcome_available",
            False,
        )
    )

    feedback_status = _safe_string(
        learning.get(
            "feedback_status"
        )
    )

    learning_signal = _safe_string(
        learning.get(
            "learning_signal"
        )
    )

    if (
        outcome_available
        and feedback_status == "AVAILABLE"
        and learning_signal
        and learning_signal != "INSUFFICIENT_DATA"
    ):
        return "ADAPTATION_SIGNAL_AVAILABLE"

    if outcome_available:
        return "OUTCOME_AVAILABLE"

    return "AWAITING_OUTCOME"


# ============================================================
# RECOMMENDATION
# ============================================================

def _build_recommendation(
    adaptation_state: str,
    learning: Dict[str, Any],
) -> str:
    """
    Produce an advisory adaptation recommendation.
    """

    learning_recommendation = _safe_string(
        learning.get(
            "learning_recommendation"
        )
    )

    if adaptation_state == "ADAPTATION_SIGNAL_AVAILABLE":
        if learning_recommendation:
            return (
                "Use the available learning signal as "
                "advisory input for future orchestration. "
                + learning_recommendation
            )

        return (
            "A learning signal is available and may be "
            "considered during future orchestration."
        )

    if adaptation_state == "OUTCOME_AVAILABLE":
        return (
            "An outcome is available, but no sufficient "
            "learning signal is currently available."
        )

    return (
        "Await the experience outcome before generating "
        "a stronger adaptation recommendation."
    )


# ============================================================
# ADAPTIVE EXPERIENCE INTEGRATION
# ============================================================

def integrate_adaptive_experience(
    *,
    trace_id: Any,
    experience: Dict[str, Any],
    learning: Dict[str, Any],
    decision: Any = "",
    confidence: Any = "",
    priority: Any = "",
    evidence: Any = None,
    contributing_engines: Any = None,
) -> AdaptiveExperienceResult:
    """
    Integrate experience and learning information into 8G.

    Existing decision information is preserved exactly as
    advisory data. No decision replacement is performed.
    """

    experience_data = _extract_experience(
        _safe_dict(experience)
    )

    learning_data = _extract_learning(
        _safe_dict(learning)
    )

    adaptation_state = _derive_adaptation_state(
        experience_data,
        learning_data,
    )

    recommendation = _build_recommendation(
        adaptation_state,
        learning_data,
    )

    return AdaptiveExperienceResult(
        trace_id=_preserve_trace(trace_id),
        status=ADAPTIVE_EXPERIENCE_STATUS,
        experience_id=experience_data[
            "experience_id"
        ],
        decision=_safe_string(
            decision,
            "UNKNOWN",
        ),
        confidence=_safe_string(
            confidence,
            "UNKNOWN",
        ),
        priority=_safe_string(
            priority,
            "UNKNOWN",
        ),
        adaptation_state=adaptation_state,
        experience_status=experience_data[
            "experience_status"
        ],
        learning_signal=learning_data[
            "learning_signal"
        ],
        adaptation_recommendation=recommendation,
        evidence=[
            item
            for item in _safe_list(evidence)
            if isinstance(item, dict)
        ],
        contributing_engines=[
            _safe_string(item)
            for item in _safe_list(
                contributing_engines
            )
            if _safe_string(item)
        ],
        safety=_build_safety(),
    )


# ============================================================
# REGRESSION
# ============================================================

def get_adaptive_experience_regression() -> Dict[str, Any]:
    """
    Run the complete 8G regression contract.
    """

    result = integrate_adaptive_experience(
        trace_id="7J-TEST-8G",
        experience={
            "experience_id": "7J-EXP-TEST",
            "outcome_status": "PENDING",
            "outcome_available": False,
        },
        learning={
            "feedback_status": "MISSING_FEEDBACK",
            "feedback_quality": "INSUFFICIENT",
            "learning_signal": "COLLECT_OUTCOME",
            "learning_recommendation": (
                "Await outcome."
            ),
        },
        decision="ADVISORY",
        confidence="MEDIUM",
        priority="NORMAL",
        evidence=[
            {
                "source": "experience",
                "value": "preserved",
            }
        ],
        contributing_engines=[
            "Experience Memory",
            "Learning Feedback",
        ],
    )

    checks = {
        "status_ready": (
            result.status
            == ADAPTIVE_EXPERIENCE_STATUS
        ),
        "layer_8g": (
            ADAPTIVE_EXPERIENCE_VERSION
            == "8G"
        ),
        "trace_preserved": (
            result.trace_id
            == "7J-TEST-8G"
        ),
        "experience_preserved": (
            result.experience_id
            == "7J-EXP-TEST"
        ),
        "decision_preserved": (
            result.decision
            == "ADVISORY"
        ),
        "confidence_preserved": (
            result.confidence
            == "MEDIUM"
        ),
        "priority_preserved": (
            result.priority
            == "NORMAL"
        ),
        "experience_status_preserved": (
            result.experience_status
            == "PENDING"
        ),
        "learning_signal_preserved": (
            result.learning_signal
            == "COLLECT_OUTCOME"
        ),
        "evidence_preserved": (
            bool(result.evidence)
        ),
        "engines_preserved": (
            "Experience Memory"
            in result.contributing_engines
            and
            "Learning Feedback"
            in result.contributing_engines
        ),
        "adaptation_available": (
            bool(result.adaptation_state)
        ),
        "recommendation_generated": (
            bool(
                result.adaptation_recommendation
            )
        ),
        "safety_advisory": (
            result.safety["safety_level"]
            == "ADVISORY_ONLY"
        ),
        "execution_blocked": (
            result.safety["execution_allowed"]
            is False
        ),
        "automatic_action_blocked": (
            result.safety[
                "automatic_action_allowed"
            ]
            is False
        ),
        "self_modification_blocked": (
            result.safety[
                "self_modification_allowed"
            ]
            is False
        ),
        "decision_override_blocked": (
            result.safety[
                "decision_override_allowed"
            ]
            is False
        ),
        "global_safety_valid": (
            validate_adaptive_experience_safety()
        ),
    }

    regression_passed = all(
        checks.values()
    )

    return {
        "integration_layer": "8G",
        "integration_status": (
            "READY"
            if regression_passed
            else "FAILED"
        ),
        "regression_passed": regression_passed,
        "trace_id": result.trace_id,
        "experience_id": result.experience_id,
        "adaptation_state": (
            result.adaptation_state
        ),
        "recommendation": (
            result.adaptation_recommendation
        ),
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
        "checks": checks,
    }


# ============================================================
# STATUS
# ============================================================

def get_adaptive_experience_status() -> Dict[str, Any]:
    """
    Return the current 8G module status.
    """

    return {
        "layer": ADAPTIVE_EXPERIENCE_VERSION,
        "status": ADAPTIVE_EXPERIENCE_STATUS,
        "safety_level": SAFETY_LEVEL,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
        "safety_valid": (
            validate_adaptive_experience_safety()
        ),
    }