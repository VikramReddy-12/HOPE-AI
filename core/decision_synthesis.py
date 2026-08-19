"""
HOPE AI — 7F Decision Synthesis

7F consumes existing intelligence produced by HOPE's reasoning
and predictive layers and produces one structured unified result.

Responsibilities:
    - Aggregate reasoning output
    - Aggregate predictive system assessment
    - Aggregate predictive decision summary
    - Preserve evidence and confidence provenance
    - Produce a unified advisory decision
    - Preserve traceability
    - Preserve safety boundaries

7F does NOT:
    - Execute system actions
    - Modify system state
    - Override predictive decisions
    - Invent predictive confidence
    - Authorize automatic actions
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


SYNTHESIS_VERSION = "7F"
SYNTHESIS_STATUS = "READY"

SAFETY_LEVEL = "ADVISORY_ONLY"
EXECUTION_ALLOWED = False
AUTOMATIC_ACTION_ALLOWED = False


@dataclass
class DecisionSynthesisResult:
    """
    Unified intelligence result produced by 7F.
    """

    trace_id: str
    status: str
    decision: str
    confidence: str
    priority: str
    reasoning_summary: str
    predictive_summary: Dict[str, Any]
    evidence: List[Dict[str, Any]]
    contributing_engines: List[str]
    safety: Dict[str, Any]
    errors: List[str] = field(default_factory=list)


# ============================================================
# NORMALIZATION
# ============================================================

def _safe_text(value: Any) -> str:
    if value is None:
        return ""

    return str(value).strip()


def _safe_dict(value: Any) -> Dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)

    return {}


# ============================================================
# REASONING SUMMARY
# ============================================================

def _build_reasoning_summary(
    reasoning_result: Any,
) -> str:
    """
    Preserve the reasoning engine's result without attempting
    to reinterpret or fabricate structured reasoning fields.
    """

    text = _safe_text(reasoning_result)

    if not text:
        return "No reasoning result was available."

    return text


# ============================================================
# PREDICTIVE SUMMARY
# ============================================================

def _build_predictive_summary(
    prediction: Dict[str, Any],
    decision: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Preserve the authoritative predictive fields produced by
    the existing predictive intelligence engine.
    """

    prediction = _safe_dict(prediction)
    decision = _safe_dict(decision)

    return {
        "overall_risk": prediction.get(
            "overall_risk"
        ),
        "risk_score": prediction.get(
            "risk_score"
        ),
        "confidence": prediction.get(
            "confidence"
        ),
        "modules": prediction.get(
            "modules"
        ),
        "critical": prediction.get(
            "critical"
        ),
        "high": prediction.get(
            "high"
        ),
        "medium": prediction.get(
            "medium"
        ),
        "insufficient_data": prediction.get(
            "insufficient_data"
        ),
        "action": prediction.get(
            "action",
            decision.get("action"),
        ),
        "priority": prediction.get(
            "priority",
            decision.get("priority"),
        ),
        "action_reason": prediction.get(
            "action_reason"
        ),
        "message": prediction.get(
            "message"
        ),
        "selected_module": decision.get(
            "selected_module"
        ),
        "selected_risk": decision.get(
            "selected_risk"
        ),
        "selected_risk_score": decision.get(
            "selected_risk_score"
        ),
    }


# ============================================================
# EVIDENCE
# ============================================================

def _build_evidence(
    prediction: Dict[str, Any],
    decision: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Build transparent evidence records from existing
    predictive outputs.

    No new evidence is invented.
    """

    evidence: List[Dict[str, Any]] = []

    if prediction.get("overall_risk") is not None:
        evidence.append(
            {
                "source": "Predictive Intelligence",
                "type": "overall_risk",
                "value": prediction.get(
                    "overall_risk"
                ),
            }
        )

    if prediction.get("risk_score") is not None:
        evidence.append(
            {
                "source": "Predictive Intelligence",
                "type": "risk_score",
                "value": prediction.get(
                    "risk_score"
                ),
            }
        )

    if prediction.get("confidence") is not None:
        evidence.append(
            {
                "source": "Predictive Intelligence",
                "type": "confidence",
                "value": prediction.get(
                    "confidence"
                ),
            }
        )

    if decision.get("selected_module") is not None:
        evidence.append(
            {
                "source": "Predictive Decision Summary",
                "type": "selected_module",
                "value": decision.get(
                    "selected_module"
                ),
            }
        )

    if decision.get("selected_risk") is not None:
        evidence.append(
            {
                "source": "Predictive Decision Summary",
                "type": "selected_risk",
                "value": decision.get(
                    "selected_risk"
                ),
            }
        )

    if decision.get("selected_risk_score") is not None:
        evidence.append(
            {
                "source": "Predictive Decision Summary",
                "type": "selected_risk_score",
                "value": decision.get(
                    "selected_risk_score"
                ),
            }
        )

    return evidence


# ============================================================
# SYNTHESIS
# ============================================================

def synthesize_decision(
    trace_id: str,
    reasoning_result: Any,
    prediction: Dict[str, Any],
    decision_summary: Dict[str, Any],
    trace_regression: Optional[
        Dict[str, Any]
    ] = None,
) -> DecisionSynthesisResult:
    """
    Synthesize existing reasoning and predictive intelligence
    into one advisory-only result.
    """

    prediction = _safe_dict(
        prediction
    )

    decision_summary = _safe_dict(
        decision_summary
    )

    trace_regression = _safe_dict(
        trace_regression
    )

    reasoning_summary = (
        _build_reasoning_summary(
            reasoning_result
        )
    )

    predictive_summary = (
        _build_predictive_summary(
            prediction,
            decision_summary,
        )
    )

    evidence = _build_evidence(
        prediction,
        decision_summary,
    )

    decision = _safe_text(
        decision_summary.get(
            "action"
        )
        or prediction.get(
            "action"
        )
        or "MONITOR"
    )

    confidence = _safe_text(
        prediction.get(
            "confidence"
        )
        or "INSUFFICIENT_DATA"
    )

    priority = _safe_text(
        decision_summary.get(
            "priority"
        )
        or prediction.get(
            "priority"
        )
        or "UNKNOWN"
    )

    safety = {
        "level": SAFETY_LEVEL,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "predictive_safety_valid": (
            trace_regression.get(
                "regression_passed",
                True,
            )
        ),
    }

    errors: List[str] = []

    if not reasoning_summary:
        errors.append(
            "Reasoning result unavailable."
        )

    if not prediction:
        errors.append(
            "Predictive result unavailable."
        )

    return DecisionSynthesisResult(
        trace_id=trace_id,
        status=(
            SYNTHESIS_STATUS
            if not errors
            else "PARTIAL"
        ),
        decision=decision,
        confidence=confidence,
        priority=priority,
        reasoning_summary=reasoning_summary,
        predictive_summary=predictive_summary,
        evidence=evidence,
        contributing_engines=[
            "reasoning",
            "predictive",
        ],
        safety=safety,
        errors=errors,
    )


# ============================================================
# PUBLIC DICTIONARY RESULT
# ============================================================

def synthesize_decision_dict(
    trace_id: str,
    reasoning_result: Any,
    prediction: Dict[str, Any],
    decision_summary: Dict[str, Any],
    trace_regression: Optional[
        Dict[str, Any]
    ] = None,
) -> Dict[str, Any]:
    """
    Return the 7F result as a dictionary suitable for
    orchestration context storage.
    """

    result = synthesize_decision(
        trace_id=trace_id,
        reasoning_result=reasoning_result,
        prediction=prediction,
        decision_summary=decision_summary,
        trace_regression=trace_regression,
    )

    return {
        "integration_layer": SYNTHESIS_VERSION,
        "status": result.status,
        "trace_id": result.trace_id,
        "decision": result.decision,
        "confidence": result.confidence,
        "priority": result.priority,
        "reasoning_summary": result.reasoning_summary,
        "predictive_summary": result.predictive_summary,
        "evidence": result.evidence,
        "contributing_engines": (
            result.contributing_engines
        ),
        "safety": result.safety,
        "errors": result.errors,
    }


# ============================================================
# SAFETY
# ============================================================

def get_synthesis_safety() -> Dict[str, Any]:
    """
    Return the immutable 7F safety boundary.
    """

    return {
        "level": SAFETY_LEVEL,
        "execution_allowed": False,
        "automatic_action_allowed": False,
    }


# ============================================================
# 7F REGRESSION
# ============================================================

def get_decision_synthesis_regression() -> Dict[str, Any]:
    """
    Validate 7F against the real reasoning and predictive
    interfaces already present in HOPE.
    """

    from reasoning.engine import reason

    from core.predictive_intelligence import (
        get_predictive_decision_summary,
        get_predictive_decision_trace_regression,
        get_system_prediction,
    )

    trace_id = "7F-REGRESSION"

    reasoning_result = reason(
        "compare Java and Python"
    )

    prediction = get_system_prediction()

    decision_summary = (
        get_predictive_decision_summary()
    )

    trace_regression = (
        get_predictive_decision_trace_regression()
    )

    result = synthesize_decision(
        trace_id=trace_id,
        reasoning_result=reasoning_result,
        prediction=prediction,
        decision_summary=decision_summary,
        trace_regression=trace_regression,
    )

    safety = get_synthesis_safety()

    checks = {
        "status_ready": (
            result.status == "READY"
        ),
        "reasoning_available": (
            bool(result.reasoning_summary)
        ),
        "prediction_available": (
            bool(result.predictive_summary)
        ),
        "decision_available": (
            bool(result.decision)
        ),
        "confidence_preserved": (
            result.confidence
            == prediction.get(
                "confidence"
            )
        ),
        "priority_preserved": (
            result.priority
            == (
                decision_summary.get(
                    "priority"
                )
                or prediction.get(
                    "priority"
                )
            )
        ),
        "evidence_generated": (
            len(result.evidence) > 0
        ),
        "reasoning_engine_present": (
            "reasoning"
            in result.contributing_engines
        ),
        "predictive_engine_present": (
            "predictive"
            in result.contributing_engines
        ),
        "trace_preserved": (
            result.trace_id == trace_id
        ),
        "predictive_trace_valid": (
            trace_regression.get(
                "regression_passed"
            )
            is True
        ),
        "safety_level_advisory": (
            safety["level"]
            == "ADVISORY_ONLY"
        ),
        "execution_blocked": (
            safety[
                "execution_allowed"
            ]
            is False
            and result.safety[
                "execution_allowed"
            ]
            is False
        ),
        "automatic_action_blocked": (
            safety[
                "automatic_action_allowed"
            ]
            is False
            and result.safety[
                "automatic_action_allowed"
            ]
            is False
        ),
    }

    return {
        "integration_layer": SYNTHESIS_VERSION,
        "integration_status": (
            "READY"
            if all(checks.values())
            else "FAILED"
        ),
        "trace_id": result.trace_id,
        "decision": result.decision,
        "confidence": result.confidence,
        "priority": result.priority,
        "evidence_count": len(
            result.evidence
        ),
        "contributing_engines": (
            result.contributing_engines
        ),
        "execution_allowed": (
            result.safety[
                "execution_allowed"
            ]
        ),
        "automatic_action_allowed": (
            result.safety[
                "automatic_action_allowed"
            ]
        ),
        "checks": checks,
        "regression_passed": all(
            checks.values()
        ),
    }