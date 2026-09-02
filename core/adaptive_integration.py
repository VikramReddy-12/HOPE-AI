"""
HOPE Adaptive Integration Intelligence

8H - Adaptive Integration

Purpose:
    Integrate the adaptive intelligence layers 8A through 8G
    into one structured advisory result.

Design principles:
    - 8H coordinates adaptive intelligence outputs.
    - Existing decisions are preserved.
    - Existing confidence and priority are preserved.
    - Experience and learning signals are preserved.
    - Adaptation remains advisory only.
    - No automatic execution is permitted.
    - No self-modification is permitted.
    - No decision override is permitted.
    - Traceability is preserved.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


# ============================================================
# VERSION / STATUS
# ============================================================

ADAPTIVE_INTEGRATION_VERSION = "8H"
ADAPTIVE_INTEGRATION_STATUS = "READY"

SAFETY_LEVEL = "ADVISORY_ONLY"

EXECUTION_ALLOWED = False
AUTOMATIC_ACTION_ALLOWED = False
SELF_MODIFICATION_ALLOWED = False
DECISION_OVERRIDE_ALLOWED = False


# ============================================================
# SAFETY
# ============================================================

def _build_safety() -> Dict[str, Any]:
    """
    Return the immutable 8H safety contract.
    """

    return {
        "safety_level": SAFETY_LEVEL,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
    }


def validate_adaptive_integration_safety() -> bool:
    """
    Validate the complete 8H safety contract.
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
class AdaptiveIntegrationResult:
    """
    Structured 8H adaptive integration result.
    """

    trace_id: str

    status: str

    decision: str
    confidence: str
    priority: str

    adaptation_state: str
    strategy: str
    orchestration_state: str

    learning_signal: str
    experience_id: str

    response: str

    recommendation: str

    evidence: List[Dict[str, Any]] = field(
        default_factory=list
    )

    contributing_layers: List[str] = field(
        default_factory=list
    )

    safety: Dict[str, Any] = field(
        default_factory=_build_safety
    )

    errors: List[str] = field(
        default_factory=list
    )


# ============================================================
# LAYER EXTRACTION
# ============================================================

def _extract_adaptive_layers(
    adaptive_intelligence: Dict[str, Any],
    adaptive_strategy: Dict[str, Any],
    adaptive_orchestration: Dict[str, Any],
    adaptive_decision: Dict[str, Any],
    adaptive_response: Dict[str, Any],
    adaptive_learning: Dict[str, Any],
    adaptive_experience: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Preserve outputs from 8A through 8G.
    """

    intelligence = _safe_dict(
        adaptive_intelligence
    )

    strategy = _safe_dict(
        adaptive_strategy
    )

    orchestration = _safe_dict(
        adaptive_orchestration
    )

    decision = _safe_dict(
        adaptive_decision
    )

    response = _safe_dict(
        adaptive_response
    )

    learning = _safe_dict(
        adaptive_learning
    )

    experience = _safe_dict(
        adaptive_experience
    )

    return {
        "8A": intelligence,
        "8B": strategy,
        "8C": orchestration,
        "8D": decision,
        "8E": response,
        "8F": learning,
        "8G": experience,
    }


# ============================================================
# FIELD PRESERVATION
# ============================================================

def _first_available(
    layers: Dict[str, Dict[str, Any]],
    field_name: str,
    default: Any = "",
) -> Any:
    """
    Return the first available value for a field.

    Existing values are preserved rather than regenerated.
    """

    for layer in (
        "8G",
        "8F",
        "8E",
        "8D",
        "8C",
        "8B",
        "8A",
    ):
        value = layers[layer].get(
            field_name
        )

        if value is not None and value != "":
            return value

    return default


# ============================================================
# RECOMMENDATION
# ============================================================

def _build_recommendation(
    layers: Dict[str, Dict[str, Any]],
) -> str:
    """
    Build one advisory integration recommendation.
    """

    recommendation = _first_available(
        layers,
        "recommendation",
        "",
    )

    if recommendation:
        return _safe_string(
            recommendation
        )

    recommendation = _first_available(
        layers,
        "adaptation_recommendation",
        "",
    )

    if recommendation:
        return _safe_string(
            recommendation
        )

    learning_recommendation = _first_available(
        layers,
        "learning_recommendation",
        "",
    )

    if learning_recommendation:
        return _safe_string(
            learning_recommendation
        )

    return (
        "Adaptive intelligence is available as "
        "advisory input for future orchestration."
    )


# ============================================================
# INTEGRATION
# ============================================================

def integrate_adaptive_intelligence(
    *,
    trace_id: Any,
    adaptive_intelligence: Dict[str, Any],
    adaptive_strategy: Dict[str, Any],
    adaptive_orchestration: Dict[str, Any],
    adaptive_decision: Dict[str, Any],
    adaptive_response: Dict[str, Any],
    adaptive_learning: Dict[str, Any],
    adaptive_experience: Dict[str, Any],
    decision: Any = "",
    confidence: Any = "",
    priority: Any = "",
    response: Any = "",
    evidence: Any = None,
) -> AdaptiveIntegrationResult:
    """
    Integrate adaptive intelligence layers 8A through 8G.

    This function coordinates existing information only.
    It does not execute actions or replace decisions.
    """

    layers = _extract_adaptive_layers(
        adaptive_intelligence,
        adaptive_strategy,
        adaptive_orchestration,
        adaptive_decision,
        adaptive_response,
        adaptive_learning,
        adaptive_experience,
    )

    preserved_decision = _safe_string(
        decision,
        _first_available(
            layers,
            "decision",
            "UNKNOWN",
        ),
    )

    preserved_confidence = _safe_string(
        confidence,
        _first_available(
            layers,
            "confidence",
            "UNKNOWN",
        ),
    )

    preserved_priority = _safe_string(
        priority,
        _first_available(
            layers,
            "priority",
            "UNKNOWN",
        ),
    )

    preserved_response = _safe_string(
        response,
        _first_available(
            layers,
            "response",
            "",
        ),
    )

    adaptation_state = _safe_string(
        _first_available(
            layers,
            "adaptation_state",
            "",
        ),
        "ADAPTIVE_STATE_AVAILABLE",
    )

    strategy = _safe_string(
        _first_available(
            layers,
            "strategy",
            "",
        ),
        "ADAPTIVE_STRATEGY_AVAILABLE",
    )

    orchestration_state = _safe_string(
        _first_available(
            layers,
            "orchestration_state",
            "",
        ),
        "ADAPTIVE_ORCHESTRATION_AVAILABLE",
    )

    learning_signal = _safe_string(
        _first_available(
            layers,
            "learning_signal",
            "",
        ),
        "INSUFFICIENT_DATA",
    )

    experience_id = _safe_string(
        _first_available(
            layers,
            "experience_id",
            "",
        ),
        "EXPERIENCE_UNAVAILABLE",
    )

    combined_evidence: List[Dict[str, Any]] = []

    for item in _safe_list(evidence):
        if isinstance(item, dict):
            combined_evidence.append(
                dict(item)
            )

    for layer_name, layer_data in layers.items():
        layer_evidence = layer_data.get(
            "evidence"
        )

        if isinstance(layer_evidence, list):
            for item in layer_evidence:
                if isinstance(item, dict):
                    combined_evidence.append(
                        {
                            "source_layer": layer_name,
                            **dict(item),
                        }
                    )

    contributing_layers = [
        layer_name
        for layer_name, layer_data in layers.items()
        if layer_data
    ]

    return AdaptiveIntegrationResult(
        trace_id=_safe_string(
            trace_id,
            "8H-TRACE-UNAVAILABLE",
        ),
        status=ADAPTIVE_INTEGRATION_STATUS,
        decision=preserved_decision,
        confidence=preserved_confidence,
        priority=preserved_priority,
        adaptation_state=adaptation_state,
        strategy=strategy,
        orchestration_state=orchestration_state,
        learning_signal=learning_signal,
        experience_id=experience_id,
        response=preserved_response,
        recommendation=_build_recommendation(
            layers
        ),
        evidence=combined_evidence,
        contributing_layers=contributing_layers,
        safety=_build_safety(),
    )


# ============================================================
# REGRESSION
# ============================================================

def get_adaptive_integration_regression() -> Dict[str, Any]:
    """
    Run the complete 8H regression contract.
    """

    result = integrate_adaptive_intelligence(
        trace_id="8G-TEST-8H",

        adaptive_intelligence={
            "layer": "8A",
            "status": "READY",
        },

        adaptive_strategy={
            "layer": "8B",
            "status": "READY",
            "strategy": "CONSERVATIVE",
        },

        adaptive_orchestration={
            "layer": "8C",
            "status": "READY",
            "orchestration_state": "READY",
        },

        adaptive_decision={
            "layer": "8D",
            "status": "READY",
            "decision": "ADVISORY",
            "confidence": "MEDIUM",
            "priority": "NORMAL",
        },

        adaptive_response={
            "layer": "8E",
            "status": "READY",
            "response": "Adaptive response available.",
        },

        adaptive_learning={
            "layer": "8F",
            "status": "READY",
            "learning_signal": "COLLECT_OUTCOME",
        },

        adaptive_experience={
            "layer": "8G",
            "status": "READY",
            "experience_id": "7J-EXP-TEST",
            "adaptation_state": (
                "AWAITING_OUTCOME"
            ),
        },

        decision="ADVISORY",
        confidence="MEDIUM",
        priority="NORMAL",
        response="Adaptive response available.",
        evidence=[
            {
                "source": "8H",
                "value": "integration-test",
            }
        ],
    )

    checks = {
        "status_ready": (
            result.status
            == ADAPTIVE_INTEGRATION_STATUS
        ),

        "layer_8h": (
            ADAPTIVE_INTEGRATION_VERSION
            == "8H"
        ),

        "trace_preserved": (
            result.trace_id
            == "8G-TEST-8H"
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

        "adaptation_preserved": (
            bool(result.adaptation_state)
        ),

        "strategy_preserved": (
            bool(result.strategy)
        ),

        "orchestration_preserved": (
            bool(result.orchestration_state)
        ),

        "learning_signal_preserved": (
            result.learning_signal
            == "COLLECT_OUTCOME"
        ),

        "experience_preserved": (
            result.experience_id
            == "7J-EXP-TEST"
        ),

        "response_preserved": (
            bool(result.response)
        ),

        "evidence_preserved": (
            bool(result.evidence)
        ),

        "layers_preserved": (
            all(
                layer in result.contributing_layers
                for layer in (
                    "8A",
                    "8B",
                    "8C",
                    "8D",
                    "8E",
                    "8F",
                    "8G",
                )
            )
        ),

        "recommendation_generated": (
            bool(result.recommendation)
        ),

        "safety_advisory": (
            result.safety[
                "safety_level"
            ]
            == "ADVISORY_ONLY"
        ),

        "execution_blocked": (
            result.safety[
                "execution_allowed"
            ]
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
            validate_adaptive_integration_safety()
        ),
    }

    regression_passed = all(
        checks.values()
    )

    return {
        "integration_layer": "8H",

        "integration_status": (
            "READY"
            if regression_passed
            else "FAILED"
        ),

        "regression_passed": regression_passed,

        "trace_id": result.trace_id,

        "decision": result.decision,

        "confidence": result.confidence,

        "priority": result.priority,

        "adaptation_state": (
            result.adaptation_state
        ),

        "strategy": result.strategy,

        "orchestration_state": (
            result.orchestration_state
        ),

        "learning_signal": (
            result.learning_signal
        ),

        "experience_id": (
            result.experience_id
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

def get_adaptive_integration_status() -> Dict[str, Any]:
    """
    Return the current 8H module status.
    """

    return {
        "layer": ADAPTIVE_INTEGRATION_VERSION,
        "status": ADAPTIVE_INTEGRATION_STATUS,
        "safety_level": SAFETY_LEVEL,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
        "safety_valid": (
            validate_adaptive_integration_safety()
        ),
    }