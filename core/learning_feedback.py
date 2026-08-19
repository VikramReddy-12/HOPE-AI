"""
HOPE Learning Feedback Intelligence

7I - Learning & Feedback Intelligence

Purpose:
    Analyze completed HOPE intelligence results and produce a
    structured learning-feedback signal for future orchestration.

Design principles:
    - 7I analyzes outcomes; it does not execute actions.
    - Existing memory remains the persistent memory system.
    - Existing conversation history remains unchanged.
    - Shared orchestration context carries per-run feedback.
    - No automatic self-modification is permitted.
    - No automatic decision replacement is permitted.
    - No operating-system or external-system action is permitted.
    - Trace IDs are preserved.
    - Feedback quality is explicitly classified.
    - Insufficient feedback must remain insufficient.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ============================================================
# VERSION / STATUS
# ============================================================

LEARNING_FEEDBACK_VERSION = "7I"
LEARNING_FEEDBACK_STATUS = "READY"

SAFETY_LEVEL = "ADVISORY_ONLY"
EXECUTION_ALLOWED = False
AUTOMATIC_ACTION_ALLOWED = False


# ============================================================
# FEEDBACK STATES
# ============================================================

FEEDBACK_AVAILABLE = "AVAILABLE"
FEEDBACK_INSUFFICIENT = "INSUFFICIENT_FEEDBACK"
FEEDBACK_MISSING = "MISSING_FEEDBACK"

LEARNING_SIGNAL_AVAILABLE = "LEARNING_SIGNAL_AVAILABLE"
LEARNING_SIGNAL_INSUFFICIENT = "INSUFFICIENT_DATA"
LEARNING_SIGNAL_COLLECT_OUTCOME = "COLLECT_OUTCOME"

QUALITY_HIGH = "HIGH"
QUALITY_MEDIUM = "MEDIUM"
QUALITY_LOW = "LOW"
QUALITY_INSUFFICIENT = "INSUFFICIENT"


# ============================================================
# FEEDBACK RESULT
# ============================================================

@dataclass
class LearningFeedback:
    """
    Structured 7I learning-feedback result.
    """

    trace_id: str
    status: str

    decision: str
    confidence: str
    priority: str

    evidence: List[Dict[str, Any]]
    contributing_engines: List[str]

    feedback_status: str
    feedback_quality: str

    learning_signal: str
    learning_recommendation: str

    outcome_available: bool
    outcome: Optional[Any] = None

    source_layer: str = LEARNING_FEEDBACK_VERSION

    safety: Dict[str, Any] = field(
        default_factory=lambda: {
            "safety_level": SAFETY_LEVEL,
            "execution_allowed": False,
            "automatic_action_allowed": False,
            "self_modification_allowed": False,
            "decision_override_allowed": False,
        }
    )

    errors: List[str] = field(
        default_factory=list
    )


# ============================================================
# NORMALIZATION
# ============================================================

def _safe_string(
    value: Any,
    default: str = "UNKNOWN",
) -> str:
    """
    Convert a value to a safe non-empty string.
    """

    if value is None:
        return default

    value = str(value).strip()

    return value if value else default


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


def _safe_dict(
    value: Any,
) -> Dict[str, Any]:
    """
    Return a defensive dictionary copy.
    """

    if isinstance(value, dict):
        return dict(value)

    return {}


# ============================================================
# EVIDENCE QUALITY
# ============================================================

def _classify_evidence_quality(
    evidence: List[Any],
) -> str:
    """
    Classify the available evidence.

    This does not judge whether the decision itself is correct.
    It only evaluates whether usable evidence is present.
    """

    if not evidence:
        return QUALITY_INSUFFICIENT

    valid_items = 0

    for item in evidence:
        if isinstance(item, dict):
            if item:
                valid_items += 1
        elif item is not None:
            valid_items += 1

    if valid_items >= 5:
        return QUALITY_HIGH

    if valid_items >= 2:
        return QUALITY_MEDIUM

    if valid_items >= 1:
        return QUALITY_LOW

    return QUALITY_INSUFFICIENT


# ============================================================
# FEEDBACK QUALITY
# ============================================================

def _classify_feedback_quality(
    evidence: List[Any],
    confidence: str,
    outcome_available: bool,
) -> str:
    """
    Determine how useful the current run is for learning.
    """

    evidence_quality = _classify_evidence_quality(
        evidence
    )

    if not outcome_available:
        if evidence_quality == QUALITY_INSUFFICIENT:
            return QUALITY_INSUFFICIENT

        return QUALITY_LOW

    if (
        outcome_available
        and evidence_quality == QUALITY_HIGH
        and confidence == "HIGH"
    ):
        return QUALITY_HIGH

    if (
        outcome_available
        and evidence_quality in {
            QUALITY_HIGH,
            QUALITY_MEDIUM,
        }
    ):
        return QUALITY_MEDIUM

    if outcome_available:
        return QUALITY_LOW

    return QUALITY_INSUFFICIENT


# ============================================================
# LEARNING SIGNAL
# ============================================================

def _determine_learning_signal(
    outcome_available: bool,
    feedback_quality: str,
) -> str:
    """
    Determine whether the run can produce a useful learning signal.
    """

    if not outcome_available:
        return LEARNING_SIGNAL_COLLECT_OUTCOME

    if feedback_quality in {
        QUALITY_HIGH,
        QUALITY_MEDIUM,
    }:
        return LEARNING_SIGNAL_AVAILABLE

    return LEARNING_SIGNAL_INSUFFICIENT


# ============================================================
# LEARNING RECOMMENDATION
# ============================================================

def _determine_learning_recommendation(
    outcome_available: bool,
    feedback_quality: str,
    confidence: str,
) -> str:
    """
    Produce an advisory learning recommendation.
    """

    if not outcome_available:
        return (
            "Collect the eventual outcome before using this "
            "run as a learning signal."
        )

    if feedback_quality == QUALITY_HIGH:
        return (
            "Outcome feedback is sufficiently strong for "
            "future learning analysis."
        )

    if feedback_quality == QUALITY_MEDIUM:
        return (
            "Use the outcome as a learning signal, but retain "
            "confidence and evidence limitations."
        )

    if confidence == "LOW":
        return (
            "Retain this result as weak learning evidence and "
            "avoid changing future behavior from this run alone."
        )

    return (
        "Additional evidence is recommended before treating "
        "this result as a reliable learning signal."
    )


# ============================================================
# SAFETY
# ============================================================

def _build_safety() -> Dict[str, Any]:
    """
    Return the immutable 7I safety boundary.
    """

    return {
        "safety_level": SAFETY_LEVEL,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
    }


# ============================================================
# CORE ANALYSIS
# ============================================================

def analyze_learning_feedback(
    trace_id: str,
    decision: Any,
    confidence: Any,
    priority: Any,
    evidence: Any,
    contributing_engines: Any,
    outcome: Any = None,
    outcome_available: bool = False,
) -> LearningFeedback:
    """
    Analyze the completed intelligence result.

    This function does not modify HOPE's models, memory,
    decisions, or external systems.
    """

    errors: List[str] = []

    normalized_trace = _safe_string(
        trace_id,
        default="UNKNOWN_TRACE",
    )

    normalized_decision = _safe_string(
        decision
    )

    normalized_confidence = _safe_string(
        confidence
    )

    normalized_priority = _safe_string(
        priority
    )

    normalized_evidence = _safe_list(
        evidence
    )

    normalized_engines = [
        _safe_string(engine)
        for engine in _safe_list(
            contributing_engines
        )
        if engine is not None
    ]

    if not normalized_engines:
        errors.append(
            "No contributing engines were supplied."
        )

    if not normalized_evidence:
        errors.append(
            "No evidence was supplied."
        )

    if outcome_available:
        feedback_status = FEEDBACK_AVAILABLE
    else:
        feedback_status = FEEDBACK_INSUFFICIENT

    feedback_quality = _classify_feedback_quality(
        evidence=normalized_evidence,
        confidence=normalized_confidence,
        outcome_available=outcome_available,
    )

    learning_signal = _determine_learning_signal(
        outcome_available=outcome_available,
        feedback_quality=feedback_quality,
    )

    learning_recommendation = (
        _determine_learning_recommendation(
            outcome_available=outcome_available,
            feedback_quality=feedback_quality,
            confidence=normalized_confidence,
        )
    )

    return LearningFeedback(
        trace_id=normalized_trace,
        status=LEARNING_FEEDBACK_STATUS,
        decision=normalized_decision,
        confidence=normalized_confidence,
        priority=normalized_priority,
        evidence=normalized_evidence,
        contributing_engines=normalized_engines,
        feedback_status=feedback_status,
        feedback_quality=feedback_quality,
        learning_signal=learning_signal,
        learning_recommendation=learning_recommendation,
        outcome_available=bool(
            outcome_available
        ),
        outcome=outcome,
        safety=_build_safety(),
        errors=errors,
    )


# ============================================================
# DICTIONARY ADAPTER
# ============================================================

def analyze_learning_feedback_dict(
    trace_id: str,
    decision: Any,
    confidence: Any,
    priority: Any,
    evidence: Any,
    contributing_engines: Any,
    outcome: Any = None,
    outcome_available: bool = False,
) -> Dict[str, Any]:
    """
    Return 7I feedback as a serializable dictionary.
    """

    result = analyze_learning_feedback(
        trace_id=trace_id,
        decision=decision,
        confidence=confidence,
        priority=priority,
        evidence=evidence,
        contributing_engines=contributing_engines,
        outcome=outcome,
        outcome_available=outcome_available,
    )

    return {
        "integration_layer": LEARNING_FEEDBACK_VERSION,
        "status": result.status,
        "trace_id": result.trace_id,
        "decision": result.decision,
        "confidence": result.confidence,
        "priority": result.priority,
        "evidence": result.evidence,
        "evidence_count": len(
            result.evidence
        ),
        "contributing_engines": (
            result.contributing_engines
        ),
        "feedback_status": result.feedback_status,
        "feedback_quality": result.feedback_quality,
        "learning_signal": result.learning_signal,
        "learning_recommendation": (
            result.learning_recommendation
        ),
        "outcome_available": (
            result.outcome_available
        ),
        "outcome": result.outcome,
        "source_layer": result.source_layer,
        "safety": result.safety,
        "errors": result.errors,
    }


# ============================================================
# ORCHESTRATION CONTEXT INTEGRATION
# ============================================================

def integrate_learning_feedback(
    context: Any,
    trace_id: str,
    decision: Any,
    confidence: Any,
    priority: Any,
    evidence: Any,
    contributing_engines: Any,
    outcome: Any = None,
    outcome_available: bool = False,
) -> Dict[str, Any]:
    """
    Store 7I feedback in the shared orchestration context.

    The context is expected to expose:
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

    feedback = analyze_learning_feedback_dict(
        trace_id=trace_id,
        decision=decision,
        confidence=confidence,
        priority=priority,
        evidence=evidence,
        contributing_engines=contributing_engines,
        outcome=outcome,
        outcome_available=outcome_available,
    )

    # Preserve the orchestration trace.
    feedback["trace_id"] = trace_id

    # Safety is immutable at this layer.
    feedback["safety"] = _build_safety()

    context.update_memory(
        {
            "learning_feedback": feedback,
        }
    )

    context_valid = True
    validation_errors: List[str] = []

    try:
        from core.orchestration_context import (
            validate_context,
        )

        validation = validate_context(
            context
        )

        context_valid = bool(
            validation.get(
                "valid",
                False,
            )
        )

        validation_errors = list(
            validation.get(
                "errors",
                [],
            )
        )

    except Exception as exc:
        context_valid = False
        validation_errors.append(
            f"Context validation failed: {exc}"
        )

    return {
        "integration_layer": LEARNING_FEEDBACK_VERSION,
        "integration_status": (
            "READY"
            if context_valid
            else "FAILED"
        ),
        "trace_id": trace_id,
        "feedback": feedback,
        "feedback_status": feedback[
            "feedback_status"
        ],
        "feedback_quality": feedback[
            "feedback_quality"
        ],
        "learning_signal": feedback[
            "learning_signal"
        ],
        "learning_recommendation": feedback[
            "learning_recommendation"
        ],
        "outcome_available": feedback[
            "outcome_available"
        ],
        "context_valid": context_valid,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "errors": validation_errors,
    }


# ============================================================
# 7I REGRESSION
# ============================================================

def get_learning_feedback_regression() -> Dict[str, Any]:
    """
    Run the deterministic 7I learning-feedback regression.

    The regression verifies:

        - 7I is ready
        - trace is preserved
        - decision is preserved
        - confidence is preserved
        - priority is preserved
        - evidence is preserved
        - contributing engines are preserved
        - insufficient outcome is correctly detected
        - learning signal remains advisory
        - execution remains blocked
        - automatic action remains blocked
        - self-modification remains blocked
        - decision override remains blocked
    """

    trace_id = "7I-REGRESSION"

    evidence = [
        {
            "source": "reasoning",
            "type": "reasoning_summary",
            "value": "Reasoning contribution available.",
        },
        {
            "source": "predictive",
            "type": "risk",
            "value": "MEDIUM",
        },
        {
            "source": "predictive",
            "type": "confidence",
            "value": "LOW",
        },
        {
            "source": "predictive",
            "type": "priority",
            "value": "MEDIUM",
        },
        {
            "source": "system",
            "type": "decision",
            "value": "MONITOR",
        },
        {
            "source": "orchestration",
            "type": "trace",
            "value": trace_id,
        },
    ]

    result = analyze_learning_feedback_dict(
        trace_id=trace_id,
        decision="MONITOR",
        confidence="LOW",
        priority="MEDIUM",
        evidence=evidence,
        contributing_engines=[
            "reasoning",
            "predictive",
        ],
        outcome=None,
        outcome_available=False,
    )

    safety = result.get(
        "safety",
        {},
    )

    execution_allowed = safety.get(
        "execution_allowed",
        False,
    )

    automatic_action_allowed = safety.get(
        "automatic_action_allowed",
        False,
    )

    self_modification_allowed = safety.get(
        "self_modification_allowed",
        False,
    )

    decision_override_allowed = safety.get(
        "decision_override_allowed",
        False,
    )

    checks = {
        "status_ready": (
            result["status"]
            == LEARNING_FEEDBACK_STATUS
        ),
        "layer_7i": (
            result["integration_layer"]
            == "7I"
        ),
        "trace_preserved": (
            result["trace_id"]
            == trace_id
        ),
        "decision_preserved": (
            result["decision"]
            == "MONITOR"
        ),
        "confidence_preserved": (
            result["confidence"]
            == "LOW"
        ),
        "priority_preserved": (
            result["priority"]
            == "MEDIUM"
        ),
        "evidence_generated": (
            result["evidence_count"]
            == 6
        ),
        "reasoning_preserved": (
            "reasoning"
            in result[
                "contributing_engines"
            ]
        ),
        "predictive_preserved": (
            "predictive"
            in result[
                "contributing_engines"
            ]
        ),
        "feedback_detected": (
            result["feedback_status"]
            == FEEDBACK_INSUFFICIENT
        ),
        "learning_signal_safe": (
            result["learning_signal"]
            == LEARNING_SIGNAL_COLLECT_OUTCOME
        ),
        "safety_advisory": (
            safety.get("safety_level")
            == SAFETY_LEVEL
        ),
        "execution_blocked": (
            execution_allowed is False
        ),
        "automatic_action_blocked": (
            automatic_action_allowed is False
        ),
        "self_modification_blocked": (
            self_modification_allowed is False
        ),
        "decision_override_blocked": (
            decision_override_allowed is False
        ),
    }

    return {
        "integration_layer": "7I",
        "integration_status": (
            "READY"
            if all(checks.values())
            else "FAILED"
        ),
        "trace_id": result["trace_id"],
        "decision": result["decision"],
        "confidence": result["confidence"],
        "priority": result["priority"],
        "evidence": result["evidence_count"],
        "engines": result[
            "contributing_engines"
        ],
        "feedback_status": result[
            "feedback_status"
        ],
        "feedback_quality": result[
            "feedback_quality"
        ],
        "learning_signal": result[
            "learning_signal"
        ],
        "learning_recommendation": result[
            "learning_recommendation"
        ],
        "execution_allowed": execution_allowed,
        "automatic_action_allowed": (
            automatic_action_allowed
        ),
        "checks": checks,
        "regression_passed": all(
            checks.values()
        ),
    }


# ============================================================
# STATUS
# ============================================================

def get_learning_feedback_status() -> Dict[str, Any]:
    """
    Return the 7I subsystem status.
    """

    safety = _build_safety()

    return {
        "version": LEARNING_FEEDBACK_VERSION,
        "status": LEARNING_FEEDBACK_STATUS,
        "safety_level": safety[
            "safety_level"
        ],
        "execution_allowed": safety[
            "execution_allowed"
        ],
        "automatic_action_allowed": safety[
            "automatic_action_allowed"
        ],
        "self_modification_allowed": safety[
            "self_modification_allowed"
        ],
        "decision_override_allowed": safety[
            "decision_override_allowed"
        ],
        "safety_valid": (
            safety[
                "execution_allowed"
            ]
            is False
            and safety[
                "automatic_action_allowed"
            ]
            is False
            and safety[
                "self_modification_allowed"
            ]
            is False
            and safety[
                "decision_override_allowed"
            ]
            is False
        ),
    }