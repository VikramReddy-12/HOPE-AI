"""
HOPE AI — 8A Adaptive Intelligence

Purpose:
    Provide a safe, deterministic foundation for adaptive
    intelligence in HOPE v1.6.

8A responsibilities:
    - Represent adaptive assessments.
    - Consume learning/experience signals.
    - Produce advisory adaptation recommendations.
    - Preserve decision provenance.
    - Preserve traceability.
    - Preserve existing safety boundaries.

8A does NOT:
    - Execute actions.
    - Modify system state.
    - Modify its own source code.
    - Override existing decisions.
    - Automatically retrain or rewrite engines.
    - Authorize automatic actions.

Design principle:
    v1.5 intelligence remains the stable foundation.
    v1.6 8A adds controlled advisory adaptation above it.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List


# ============================================================
# VERSION / STATUS
# ============================================================

ADAPTIVE_INTELLIGENCE_VERSION = "8A"
ADAPTIVE_INTELLIGENCE_STATUS = "READY"

SAFETY_LEVEL = "ADVISORY_ONLY"

EXECUTION_ALLOWED = False
AUTOMATIC_ACTION_ALLOWED = False
SELF_MODIFICATION_ALLOWED = False
DECISION_OVERRIDE_ALLOWED = False


# ============================================================
# ADAPTATION STATES
# ============================================================

ADAPTATION_AVAILABLE = "ADAPTATION_AVAILABLE"
ADAPTATION_INSUFFICIENT = "INSUFFICIENT_DATA"
ADAPTATION_BLOCKED = "ADAPTATION_BLOCKED"


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

    if value is None:
        return []

    return [value]


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
# SAFETY
# ============================================================

def _build_safety() -> Dict[str, Any]:
    """
    Return the immutable 8A safety contract.
    """

    return {
        "safety_level": SAFETY_LEVEL,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
    }


# ============================================================
# ADAPTIVE ASSESSMENT
# ============================================================

@dataclass
class AdaptiveAssessment:
    """
    Structured advisory assessment produced by 8A.
    """

    trace_id: str

    status: str

    source_experience_id: str

    decision: str
    confidence: str
    priority: str

    learning_signal: str

    adaptation_state: str

    recommendation: str

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
# ADAPTATION LOGIC
# ============================================================

def _determine_adaptation_state(
    learning_signal: str,
    evidence: List[Any],
) -> str:
    """
    Determine whether enough information exists to produce
    an advisory adaptation recommendation.

    No decision is changed by this function.
    """

    signal = _safe_string(
        learning_signal
    ).upper()

    if signal in {
        "",
        "INSUFFICIENT_DATA",
        "COLLECT_OUTCOME",
    }:
        return ADAPTATION_INSUFFICIENT

    if not evidence:
        return ADAPTATION_INSUFFICIENT

    return ADAPTATION_AVAILABLE


def _build_recommendation(
    adaptation_state: str,
    learning_signal: str,
) -> str:
    """
    Build a deterministic advisory recommendation.
    """

    if adaptation_state == ADAPTATION_AVAILABLE:
        return (
            "Review available learning feedback and "
            "consider future orchestration improvements. "
            "No automatic adaptation is authorized."
        )

    if adaptation_state == ADAPTATION_INSUFFICIENT:
        return (
            "Collect additional outcome information before "
            "considering adaptive improvements."
        )

    return (
        "Adaptive recommendation is blocked by the "
        "current safety contract."
    )


# ============================================================
# MAIN ANALYSIS
# ============================================================

def analyze_adaptation(
    trace_id: str,
    decision: Any,
    confidence: Any,
    priority: Any,
    learning_signal: Any,
    evidence: Any,
    contributing_engines: Any,
    source_experience_id: Any = "",
) -> AdaptiveAssessment:
    """
    Analyze available learning information and produce a
    deterministic advisory adaptation assessment.
    """

    errors: List[str] = []

    normalized_trace = _safe_string(
        trace_id
    )

    if not normalized_trace:
        errors.append(
            "trace_id cannot be empty."
        )

    normalized_evidence = _safe_list(
        evidence
    )

    normalized_engines = [
        _safe_string(engine)
        for engine in _safe_list(
            contributing_engines
        )
        if _safe_string(engine)
    ]

    normalized_signal = _safe_string(
        learning_signal,
        "INSUFFICIENT_DATA",
    )

    adaptation_state = (
        _determine_adaptation_state(
            normalized_signal,
            normalized_evidence,
        )
    )

    recommendation = _build_recommendation(
        adaptation_state,
        normalized_signal,
    )

    status = (
        ADAPTIVE_INTELLIGENCE_STATUS
        if not errors
        else "FAILED"
    )

    return AdaptiveAssessment(
        trace_id=normalized_trace,
        status=status,
        source_experience_id=_safe_string(
            source_experience_id
        ),
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
        learning_signal=normalized_signal,
        adaptation_state=adaptation_state,
        recommendation=recommendation,
        evidence=[
            item
            for item in normalized_evidence
            if isinstance(item, dict)
        ],
        contributing_engines=normalized_engines,
        safety=_build_safety(),
        errors=errors,
    )


# ============================================================
# DICTIONARY API
# ============================================================

def analyze_adaptation_dict(
    trace_id: str,
    decision: Any,
    confidence: Any,
    priority: Any,
    learning_signal: Any,
    evidence: Any,
    contributing_engines: Any,
    source_experience_id: Any = "",
) -> Dict[str, Any]:
    """
    Return the 8A adaptive assessment as a dictionary.
    """

    assessment = analyze_adaptation(
        trace_id=trace_id,
        decision=decision,
        confidence=confidence,
        priority=priority,
        learning_signal=learning_signal,
        evidence=evidence,
        contributing_engines=contributing_engines,
        source_experience_id=source_experience_id,
    )

    return asdict(
        assessment
    )


# ============================================================
# SAFETY VALIDATION
# ============================================================

def validate_adaptive_safety() -> bool:
    """
    Validate the immutable 8A safety boundary.
    """

    safety = _build_safety()

    return (
        safety["safety_level"]
        == "ADVISORY_ONLY"
        and safety["execution_allowed"]
        is False
        and safety["automatic_action_allowed"]
        is False
        and safety["self_modification_allowed"]
        is False
        and safety["decision_override_allowed"]
        is False
    )


# ============================================================
# REGRESSION
# ============================================================

def get_adaptive_intelligence_regression() -> Dict[str, Any]:
    """
    Run the deterministic 8A foundation regression.
    """

    trace_id = "8A-REGRESSION"

    evidence = [
        {
            "source": "7I",
            "value": "learning feedback",
        }
    ]

    result = analyze_adaptation(
        trace_id=trace_id,
        decision="MONITOR",
        confidence="LOW",
        priority="MEDIUM",
        learning_signal="LEARNING_SIGNAL_AVAILABLE",
        evidence=evidence,
        contributing_engines=[
            "reasoning",
            "predictive",
        ],
        source_experience_id="7J-EXP-REGRESSION",
    )

    checks = {
        "status_ready": (
            result.status
            == ADAPTIVE_INTELLIGENCE_STATUS
        ),
        "layer_8a": (
            ADAPTIVE_INTELLIGENCE_VERSION
            == "8A"
        ),
        "trace_preserved": (
            result.trace_id
            == trace_id
        ),
        "experience_preserved": (
            result.source_experience_id
            == "7J-EXP-REGRESSION"
        ),
        "decision_preserved": (
            result.decision
            == "MONITOR"
        ),
        "confidence_preserved": (
            result.confidence
            == "LOW"
        ),
        "priority_preserved": (
            result.priority
            == "MEDIUM"
        ),
        "learning_signal_preserved": (
            result.learning_signal
            == "LEARNING_SIGNAL_AVAILABLE"
        ),
        "evidence_preserved": (
            len(result.evidence)
            == 1
        ),
        "engines_preserved": (
            result.contributing_engines
            == [
                "reasoning",
                "predictive",
            ]
        ),
        "adaptation_available": (
            result.adaptation_state
            == ADAPTATION_AVAILABLE
        ),
        "recommendation_generated": (
            bool(result.recommendation)
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
            validate_adaptive_safety()
        ),
    }

    regression_passed = all(
        checks.values()
    )

    return {
        "integration_layer": "8A",
        "integration_status": (
            "READY"
            if regression_passed
            else "FAILED"
        ),
        "regression_passed": regression_passed,
        "trace_id": result.trace_id,
        "adaptation_state": (
            result.adaptation_state
        ),
        "recommendation": (
            result.recommendation
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

def get_adaptive_intelligence_status() -> Dict[str, Any]:
    """
    Return the current 8A module status.
    """

    return {
        "layer": ADAPTIVE_INTELLIGENCE_VERSION,
        "status": ADAPTIVE_INTELLIGENCE_STATUS,
        "safety_level": SAFETY_LEVEL,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
        "safety_valid": validate_adaptive_safety(),
    }