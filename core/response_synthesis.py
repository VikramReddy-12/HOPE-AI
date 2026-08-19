"""
HOPE AI — 7H Intelligent Response Synthesis

Purpose
-------
Convert the structured intelligence produced by 7F/7G into a
deterministic, human-readable response without changing the
underlying decision.

7H does NOT:
    - execute actions
    - modify system state
    - generate new predictions
    - generate new reasoning
    - override 7F decisions
    - increase confidence
    - invent evidence
    - authorize automatic actions

Safety
------
ADVISORY_ONLY
execution_allowed = False
automatic_action_allowed = False
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


# ============================================================
# VERSION / STATUS
# ============================================================

RESPONSE_SYNTHESIS_VERSION = "7H"
RESPONSE_SYNTHESIS_STATUS = "READY"

SAFETY_LEVEL = "ADVISORY_ONLY"
EXECUTION_ALLOWED = False
AUTOMATIC_ACTION_ALLOWED = False


# ============================================================
# RESULT MODEL
# ============================================================

@dataclass
class IntelligentResponse:
    """
    Structured human-facing response generated from an existing
    7F/7G intelligence result.
    """

    trace_id: str
    status: str
    response: str
    decision: str
    confidence: str
    priority: str
    evidence: List[Dict[str, Any]]
    contributing_engines: List[str]
    safety: Dict[str, Any]
    source_layer: str
    errors: List[str] = field(default_factory=list)


# ============================================================
# NORMALIZATION
# ============================================================

def _text(value: Any, default: str = "") -> str:
    """
    Convert a value to clean display text.
    """

    if value is None:
        return default

    text = str(value).strip()

    return text if text else default


def _normalize_decision(value: Any) -> str:
    """
    Normalize the synthesized decision.
    """

    return _text(
        value,
        "UNAVAILABLE",
    ).upper()


def _normalize_confidence(value: Any) -> str:
    """
    Normalize confidence without changing its meaning.
    """

    return _text(
        value,
        "INSUFFICIENT_DATA",
    ).upper()


def _normalize_priority(value: Any) -> str:
    """
    Normalize priority without changing its meaning.
    """

    return _text(
        value,
        "UNAVAILABLE",
    ).upper()


def _normalize_engines(
    engines: Any,
) -> List[str]:
    """
    Normalize contributing engine names.
    """

    if not isinstance(engines, (list, tuple)):
        return []

    result: List[str] = []

    for engine in engines:
        value = _text(engine)

        if value and value not in result:
            result.append(value)

    return result


def _normalize_evidence(
    evidence: Any,
) -> List[Dict[str, Any]]:
    """
    Preserve evidence supplied by 7F/7G.

    Evidence is copied rather than modified so 7H cannot
    accidentally change upstream intelligence.
    """

    if not isinstance(evidence, list):
        return []

    normalized: List[Dict[str, Any]] = []

    for item in evidence:
        if isinstance(item, dict):
            normalized.append(dict(item))
        else:
            normalized.append(
                {
                    "value": item,
                }
            )

    return normalized


# ============================================================
# SAFETY
# ============================================================

def _build_safety(
    source_safety: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Build the immutable 7H safety boundary.

    Upstream data cannot enable execution or automatic action.
    """

    safety = dict(
        source_safety
        if isinstance(source_safety, dict)
        else {}
    )

    safety["safety_level"] = SAFETY_LEVEL

    # These values are intentionally forced.
    safety["execution_allowed"] = False
    safety["automatic_action_allowed"] = False

    return safety


def validate_response_safety(
    response: IntelligentResponse,
) -> Dict[str, Any]:
    """
    Validate the 7H safety boundary.
    """

    errors: List[str] = []

    if response.safety.get(
        "execution_allowed"
    ) is not False:
        errors.append(
            "7H execution boundary was weakened."
        )

    if response.safety.get(
        "automatic_action_allowed"
    ) is not False:
        errors.append(
            "7H automatic-action boundary was weakened."
        )

    if response.safety.get(
        "safety_level"
    ) != SAFETY_LEVEL:
        errors.append(
            "7H safety level is invalid."
        )

    return {
        "valid": not errors,
        "errors": errors,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "safety_level": SAFETY_LEVEL,
    }


# ============================================================
# EVIDENCE PRESENTATION
# ============================================================

def _evidence_label(
    item: Dict[str, Any],
) -> str:
    """
    Produce a deterministic human-readable evidence line.

    Existing evidence fields are preferred. No new factual
    evidence is created.
    """

    preferred_keys = (
        "message",
        "description",
        "reason",
        "detail",
        "signal",
        "evidence",
        "value",
    )

    for key in preferred_keys:
        if key in item:
            value = _text(item.get(key))

            if value:
                return value

    parts: List[str] = []

    for key, value in item.items():
        if value is None:
            continue

        if isinstance(value, (dict, list, tuple)):
            value = str(value)

        value_text = _text(value)

        if value_text:
            parts.append(
                f"{key}: {value_text}"
            )

    return "; ".join(parts)


def _format_evidence(
    evidence: List[Dict[str, Any]],
) -> List[str]:
    """
    Convert structured evidence into display lines.
    """

    lines: List[str] = []

    for item in evidence:
        label = _evidence_label(item)

        if label:
            lines.append(label)

    return lines


# ============================================================
# SUMMARY BUILDERS
# ============================================================

def _build_assessment(
    decision: str,
    confidence: str,
    priority: str,
) -> str:
    """
    Build a concise assessment statement using only
    existing decision metadata.
    """

    return (
        f"Current decision: {decision}. "
        f"Confidence: {confidence}. "
        f"Priority: {priority}."
    )


def _build_recommendation(
    decision: str,
) -> str:
    """
    Build a conservative advisory recommendation.

    This does not execute anything.
    """

    recommendations = {
        "MONITOR": (
            "Continue monitoring the relevant signals "
            "and review the situation as additional evidence "
            "becomes available."
        ),
        "REVIEW": (
            "Review the available evidence and reassess "
            "before taking any system-changing action."
        ),
        "INVESTIGATE": (
            "Investigate the available evidence further "
            "before making a consequential decision."
        ),
        "NO_ACTION": (
            "No immediate action is recommended by the "
            "current advisory assessment."
        ),
        "INSUFFICIENT_DATA": (
            "More reliable information is required before "
            "a stronger recommendation can be made."
        ),
    }

    return recommendations.get(
        decision,
        (
            "Treat this result as an advisory assessment "
            "and review the supporting evidence before acting."
        ),
    )


# ============================================================
# RESPONSE TEXT
# ============================================================

def _build_response_text(
    decision: str,
    confidence: str,
    priority: str,
    evidence: List[Dict[str, Any]],
    contributing_engines: List[str],
    reasoning_summary: str,
    predictive_summary: str,
    safety: Dict[str, Any],
    trace_id: str,
) -> str:
    """
    Build the final human-readable HOPE response.
    """

    lines: List[str] = []

    lines.append(
        "HOPE Intelligence Response"
    )
    lines.append(
        "=========================="
    )
    lines.append("")

    lines.append(
        f"Decision   : {decision}"
    )

    lines.append(
        f"Confidence : {confidence}"
    )

    lines.append(
        f"Priority   : {priority}"
    )

    lines.append("")

    lines.append(
        "Assessment:"
    )

    lines.append(
        _build_assessment(
            decision,
            confidence,
            priority,
        )
    )

    if reasoning_summary:
        lines.append("")
        lines.append("Reasoning:")
        lines.append(reasoning_summary)

    if predictive_summary:
        lines.append("")
        lines.append("Prediction:")
        lines.append(predictive_summary)

    evidence_lines = _format_evidence(
        evidence
    )

    if evidence_lines:
        lines.append("")
        lines.append("Evidence:")

        for item in evidence_lines:
            lines.append(
                f"• {item}"
            )

    if contributing_engines:
        lines.append("")
        lines.append(
            "Contributing Engines:"
        )

        for engine in contributing_engines:
            lines.append(
                f"• {engine}"
            )

    lines.append("")
    lines.append(
        "Recommendation:"
    )

    lines.append(
        _build_recommendation(
            decision
        )
    )

    lines.append("")
    lines.append("Safety:")
    lines.append(
        f"Level       : {safety.get('safety_level', SAFETY_LEVEL)}"
    )
    lines.append(
        "Execution   : False"
    )
    lines.append(
        "Automatic   : False"
    )

    lines.append("")
    lines.append(
        f"Trace       : {trace_id}"
    )

    return "\n".join(lines)


# ============================================================
# CORE SYNTHESIS
# ============================================================

def synthesize_response(
    trace_id: str,
    decision_synthesis: Dict[str, Any],
) -> IntelligentResponse:
    """
    Convert a 7F decision-synthesis result into a 7H
    human-readable response.

    7H does not recalculate the decision.
    """

    errors: List[str] = []

    if not trace_id:
        errors.append(
            "trace_id cannot be empty."
        )

    if not isinstance(
        decision_synthesis,
        dict,
    ):
        raise TypeError(
            "decision_synthesis must be a dictionary."
        )

    decision = _normalize_decision(
        decision_synthesis.get(
            "decision"
        )
    )

    confidence = _normalize_confidence(
        decision_synthesis.get(
            "confidence"
        )
    )

    priority = _normalize_priority(
        decision_synthesis.get(
            "priority"
        )
    )

    evidence = _normalize_evidence(
        decision_synthesis.get(
            "evidence",
            [],
        )
    )

    contributing_engines = _normalize_engines(
        decision_synthesis.get(
            "contributing_engines",
            [],
        )
    )

    reasoning_summary = _text(
        decision_synthesis.get(
            "reasoning_summary"
        )
    )

    predictive_summary = _text(
        decision_synthesis.get(
            "predictive_summary"
        )
    )

    source_layer = _text(
        decision_synthesis.get(
            "integration_layer",
            "7F",
        ),
        "7F",
    )

    safety = _build_safety(
        decision_synthesis.get(
            "safety"
        )
    )

    response_text = _build_response_text(
        decision=decision,
        confidence=confidence,
        priority=priority,
        evidence=evidence,
        contributing_engines=contributing_engines,
        reasoning_summary=reasoning_summary,
        predictive_summary=predictive_summary,
        safety=safety,
        trace_id=trace_id,
    )

    safety_validation = validate_response_safety(
        IntelligentResponse(
            trace_id=trace_id,
            status="READY",
            response=response_text,
            decision=decision,
            confidence=confidence,
            priority=priority,
            evidence=evidence,
            contributing_engines=contributing_engines,
            safety=safety,
            source_layer=source_layer,
            errors=list(errors),
        )
    )

    if not safety_validation["valid"]:
        errors.extend(
            safety_validation["errors"]
        )

    status = (
        "READY"
        if not errors
        else "FAILED"
    )

    return IntelligentResponse(
        trace_id=trace_id,
        status=status,
        response=response_text,
        decision=decision,
        confidence=confidence,
        priority=priority,
        evidence=evidence,
        contributing_engines=contributing_engines,
        safety=safety,
        source_layer=source_layer,
        errors=errors,
    )


# ============================================================
# DICTIONARY ADAPTER
# ============================================================

def synthesize_response_dict(
    trace_id: str,
    decision_synthesis: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Return the 7H result as a dictionary suitable for
    orchestration-context storage.
    """

    result = synthesize_response(
        trace_id=trace_id,
        decision_synthesis=decision_synthesis,
    )

    return {
        "integration_layer": RESPONSE_SYNTHESIS_VERSION,
        "status": result.status,
        "trace_id": result.trace_id,
        "response": result.response,
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
        "source_layer": result.source_layer,
        "safety": result.safety,
        "errors": result.errors,
    }


# ============================================================
# STATUS
# ============================================================

def get_response_synthesis_status() -> Dict[str, Any]:
    """
    Return the current 7H status.
    """

    return {
        "version": RESPONSE_SYNTHESIS_VERSION,
        "status": RESPONSE_SYNTHESIS_STATUS,
        "safety_level": SAFETY_LEVEL,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "safety_valid": True,
    }


# ============================================================
# REGRESSION
# ============================================================

def get_response_synthesis_regression() -> Dict[str, Any]:
    """
    Run the standalone 7H regression.

    This regression verifies that 7H preserves upstream
    decision intelligence and does not weaken safety.
    """

    trace_id = "7H-REGRESSION"

    source = {
        "integration_layer": "7F",
        "status": "READY",
        "trace_id": trace_id,
        "decision": "MONITOR",
        "confidence": "LOW",
        "priority": "MEDIUM",
        "reasoning_summary": (
            "Reasoning assessment is available."
        ),
        "predictive_summary": (
            "Predictive assessment indicates continued monitoring."
        ),
        "evidence": [
            {
                "type": "predictive_risk",
                "value": "MEDIUM",
            },
            {
                "type": "confidence",
                "value": "LOW",
            },
            {
                "type": "data_quality",
                "value": "LIMITED",
            },
            {
                "type": "reasoning",
                "value": "AVAILABLE",
            },
            {
                "type": "predictive",
                "value": "AVAILABLE",
            },
            {
                "type": "safety",
                "value": "ADVISORY_ONLY",
            },
        ],
        "contributing_engines": [
            "reasoning",
            "predictive",
        ],
        "safety": {
            "safety_level": SAFETY_LEVEL,
            "execution_allowed": False,
            "automatic_action_allowed": False,
        },
    }

    result = synthesize_response_dict(
        trace_id=trace_id,
        decision_synthesis=source,
    )

    safety = result.get(
        "safety",
        {},
    )

    response_text = result.get(
        "response",
        "",
    )

    checks = {
        "status_ready": (
            result.get("status")
            == "READY"
        ),
        "layer_7h": (
            result.get("integration_layer")
            == "7H"
        ),
        "trace_preserved": (
            result.get("trace_id")
            == trace_id
        ),
        "decision_preserved": (
            result.get("decision")
            == "MONITOR"
        ),
        "confidence_preserved": (
            result.get("confidence")
            == "LOW"
        ),
        "priority_preserved": (
            result.get("priority")
            == "MEDIUM"
        ),
        "evidence_generated": (
            result.get("evidence_count")
            == 6
        ),
        "reasoning_preserved": (
            "reasoning"
            in result.get(
                "contributing_engines",
                [],
            )
        ),
        "predictive_preserved": (
            "predictive"
            in result.get(
                "contributing_engines",
                [],
            )
        ),
        "response_generated": (
            isinstance(
                response_text,
                str,
            )
            and len(
                response_text.strip()
            )
            > 0
        ),
        "decision_in_response": (
            "MONITOR"
            in response_text
        ),
        "confidence_in_response": (
            "LOW"
            in response_text
        ),
        "priority_in_response": (
            "MEDIUM"
            in response_text
        ),
        "safety_advisory": (
            safety.get(
                "safety_level"
            )
            == SAFETY_LEVEL
        ),
        "execution_blocked": (
            safety.get(
                "execution_allowed"
            )
            is False
        ),
        "automatic_action_blocked": (
            safety.get(
                "automatic_action_allowed"
            )
            is False
        ),
    }

    return {
        "integration_layer": "7H",
        "integration_status": (
            "READY"
            if all(checks.values())
            else "FAILED"
        ),
        "trace_id": trace_id,
        "decision": result.get(
            "decision"
        ),
        "confidence": result.get(
            "confidence"
        ),
        "priority": result.get(
            "priority"
        ),
        "evidence_count": result.get(
            "evidence_count",
            0,
        ),
        "contributing_engines": result.get(
            "contributing_engines",
            [],
        ),
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "checks": checks,
        "regression_passed": all(
            checks.values()
        ),
    }


# ============================================================
# SAFE PRESENTATION ADAPTER
# ============================================================

def get_response_text(
    response: IntelligentResponse,
) -> str:
    """
    Return only the human-readable response text.

    The structured response remains available to the
    orchestration layer.
    """

    if not isinstance(
        response,
        IntelligentResponse,
    ):
        raise TypeError(
            "response must be an IntelligentResponse."
        )

    return response.response


# ============================================================
# PUBLIC EXPORTS
# ============================================================

__all__ = [
    "RESPONSE_SYNTHESIS_VERSION",
    "RESPONSE_SYNTHESIS_STATUS",
    "SAFETY_LEVEL",
    "EXECUTION_ALLOWED",
    "AUTOMATIC_ACTION_ALLOWED",
    "IntelligentResponse",
    "validate_response_safety",
    "synthesize_response",
    "synthesize_response_dict",
    "get_response_synthesis_status",
    "get_response_synthesis_regression",
    "get_response_text",
]