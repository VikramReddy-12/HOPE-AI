"""
HOPE AI — 8C Adaptive Orchestration

Purpose:
    Convert the existing 8B adaptive strategy result into a structured
    advisory orchestration recommendation.

Design:
    8C consumes 8B only.
    It preserves the authoritative decision, confidence, priority,
    adaptation state, strategy, learning signal, evidence, and
    contributing engines.

Safety:
    - advisory only
    - no execution
    - no automatic action
    - no self-modification
    - no decision override
"""

from __future__ import annotations

from typing import Any, Dict, List


# ============================================================
# VERSION / STATUS
# ============================================================

ADAPTIVE_ORCHESTRATION_VERSION = "8C"
ADAPTIVE_ORCHESTRATION_STATUS = "READY"

SAFETY_LEVEL = "ADVISORY_ONLY"

EXECUTION_ALLOWED = False
AUTOMATIC_ACTION_ALLOWED = False
SELF_MODIFICATION_ALLOWED = False
DECISION_OVERRIDE_ALLOWED = False


# ============================================================
# NORMALIZATION
# ============================================================

def _safe_string(
    value: Any,
    default: str = "",
) -> str:
    """
    Safely convert a value to a non-empty string.
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
# SAFETY
# ============================================================

def _build_safety() -> Dict[str, Any]:
    """
    Return the immutable 8C safety contract.
    """

    return {
        "safety_level": SAFETY_LEVEL,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
    }


def validate_adaptive_orchestration_safety() -> bool:
    """
    Validate the 8C safety boundary.
    """

    return (
        SAFETY_LEVEL == "ADVISORY_ONLY"
        and EXECUTION_ALLOWED is False
        and AUTOMATIC_ACTION_ALLOWED is False
        and SELF_MODIFICATION_ALLOWED is False
        and DECISION_OVERRIDE_ALLOWED is False
    )


def get_adaptive_orchestration_safety() -> Dict[str, Any]:
    """
    Return the 8C safety contract.
    """

    return _build_safety()


def get_adaptive_orchestration_status() -> Dict[str, Any]:
    """
    Return the 8C module status.
    """

    return {
        "layer": ADAPTIVE_ORCHESTRATION_VERSION,
        "status": ADAPTIVE_ORCHESTRATION_STATUS,
        "safety": _build_safety(),
    }


# ============================================================
# ORCHESTRATION CLASSIFICATION
# ============================================================

def _build_orchestration_mode(
    adaptation_state: str,
    strategy: str,
) -> str:
    """
    Convert adaptation state and strategy into a conservative
    advisory orchestration mode.
    """

    state = adaptation_state.upper()
    selected_strategy = strategy.upper()

    if state == "ADAPTATION_AVAILABLE":

        if selected_strategy == "REFINE":
            return "ADVISORY_REFINEMENT"

        if selected_strategy == "MONITOR_AND_REFINE":
            return "ADVISORY_MONITOR_AND_REFINE"

        return "ADVISORY_ADAPTATION"

    if state == "INSUFFICIENT_DATA":
        return "ADVISORY_EVIDENCE_COLLECTION"

    return "ADVISORY_MONITORING"


def _build_recommendation(
    decision: str,
    confidence: str,
    priority: str,
    adaptation_state: str,
    strategy: str,
    orchestration_mode: str,
) -> str:
    """
    Build a human-readable advisory recommendation.

    This function never authorizes execution.
    """

    return (
        "Maintain the existing decision and use the adaptive strategy "
        "for future advisory evaluation. "
        f"decision={decision}; "
        f"confidence={confidence}; "
        f"priority={priority}; "
        f"adaptation_state={adaptation_state}; "
        f"strategy={strategy}; "
        f"orchestration_mode={orchestration_mode}. "
        "No execution or automatic adaptation is authorized."
    )


# ============================================================
# 8C INTEGRATION
# ============================================================

def integrate_adaptive_orchestration(
    adaptive_strategy: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Convert an 8B adaptive strategy result into the 8C advisory
    orchestration result.

    The existing decision is preserved.

    8C does not:
        - execute actions
        - override decisions
        - modify system state
        - modify source code
        - perform automatic adaptation
    """

    source = _safe_dict(
        adaptive_strategy
    )

    # --------------------------------------------------------
    # TRACE
    # --------------------------------------------------------

    trace_id = _safe_string(
        source.get("trace_id"),
        "8C-TRACE-UNKNOWN",
    )

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    status = _safe_string(
        source.get("status"),
        ADAPTIVE_ORCHESTRATION_STATUS,
    )

    # --------------------------------------------------------
    # AUTHORITATIVE DECISION FIELDS
    # --------------------------------------------------------

    decision = _safe_string(
        source.get("decision"),
        "UNKNOWN",
    )

    confidence = _safe_string(
        source.get("confidence"),
        "UNKNOWN",
    )

    priority = _safe_string(
        source.get("priority"),
        "UNKNOWN",
    )

    # --------------------------------------------------------
    # ADAPTIVE FIELDS
    # --------------------------------------------------------

    adaptation_state = _safe_string(
        source.get("adaptation_state"),
        "INSUFFICIENT_DATA",
    )

    strategy = _safe_string(
        source.get("strategy"),
        "MONITOR",
    )

    learning_signal = _safe_string(
        source.get("learning_signal"),
        "INSUFFICIENT_DATA",
    )

    # --------------------------------------------------------
    # EVIDENCE
    # --------------------------------------------------------

    evidence = _safe_list(
        source.get("evidence")
    )

    # --------------------------------------------------------
    # CONTRIBUTING ENGINES
    # --------------------------------------------------------

    contributing_engines = [
        _safe_string(item)
        for item in _safe_list(
            source.get("contributing_engines")
        )
        if _safe_string(item)
    ]

    # --------------------------------------------------------
    # ORCHESTRATION MODE
    # --------------------------------------------------------

    orchestration_mode = _build_orchestration_mode(
        adaptation_state=adaptation_state,
        strategy=strategy,
    )

    # --------------------------------------------------------
    # RECOMMENDATION
    # --------------------------------------------------------

    recommendation = _build_recommendation(
        decision=decision,
        confidence=confidence,
        priority=priority,
        adaptation_state=adaptation_state,
        strategy=strategy,
        orchestration_mode=orchestration_mode,
    )

    # --------------------------------------------------------
    # ERRORS
    # --------------------------------------------------------

    errors = [
        str(item)
        for item in _safe_list(
            source.get("errors")
        )
        if str(item).strip()
    ]

    # --------------------------------------------------------
    # FINAL 8C RESULT
    # --------------------------------------------------------

    return {
        "layer": ADAPTIVE_ORCHESTRATION_VERSION,

        "trace_id": trace_id,

        "status": status,

        "decision": decision,

        "confidence": confidence,

        "priority": priority,

        "adaptation_state": adaptation_state,

        "strategy": strategy,

        "orchestration_mode": orchestration_mode,

        "orchestration_state": "READY",

        "learning_signal": learning_signal,

        "recommendation": recommendation,

        "evidence": evidence,

        "contributing_engines": contributing_engines,

        "safety": _build_safety(),

        "execution_allowed": False,

        "automatic_action_allowed": False,

        "self_modification_allowed": False,

        "decision_override_allowed": False,

        "errors": errors,
    }


# ============================================================
# 8C REGRESSION
# ============================================================

def get_adaptive_orchestration_regression() -> Dict[str, Any]:
    """
    Deterministic regression for the 8C contract.

    This verifies that 8C:
        - identifies itself as 8C
        - preserves trace_id
        - preserves decision
        - preserves confidence
        - preserves priority
        - preserves adaptation state
        - preserves strategy
        - preserves learning signal
        - produces the expected advisory orchestration mode
        - preserves the safety boundary
        - blocks execution
        - blocks automatic action
        - blocks self-modification
        - blocks decision override
    """

    source = {
        "trace_id": "8C-REGRESSION-TRACE",

        "status": "READY",

        "decision": "TEST_DECISION",

        "confidence": "HIGH",

        "priority": "HIGH",

        "adaptation_state": "ADAPTATION_AVAILABLE",

        "strategy": "REFINE",

        "learning_signal": "LEARNING_SIGNAL_AVAILABLE",

        "evidence": [
            {
                "source": "8B",
                "type": "regression",
                "value": "test",
            }
        ],

        "contributing_engines": [
            "test_engine",
        ],

        "errors": [],
    }

    result = integrate_adaptive_orchestration(
        source
    )

    checks = {
        "layer": (
            result.get("layer")
            == "8C"
        ),

        "trace_id": (
            result.get("trace_id")
            == source["trace_id"]
        ),

        "decision_preserved": (
            result.get("decision")
            == source["decision"]
        ),

        "confidence_preserved": (
            result.get("confidence")
            == source["confidence"]
        ),

        "priority_preserved": (
            result.get("priority")
            == source["priority"]
        ),

        "adaptation_state_preserved": (
            result.get("adaptation_state")
            == source["adaptation_state"]
        ),

        "strategy_preserved": (
            result.get("strategy")
            == source["strategy"]
        ),

        "learning_signal_preserved": (
            result.get("learning_signal")
            == source["learning_signal"]
        ),

        "orchestration_mode": (
            result.get("orchestration_mode")
            == "ADVISORY_REFINEMENT"
        ),

        "safety": (
            validate_adaptive_orchestration_safety()
        ),

        "execution_blocked": (
            result.get("execution_allowed")
            is False
        ),

        "automatic_action_blocked": (
            result.get("automatic_action_allowed")
            is False
        ),

        "self_modification_blocked": (
            result.get("self_modification_allowed")
            is False
        ),

        "decision_override_blocked": (
            result.get("decision_override_allowed")
            is False
        ),
    }

    return {
        "layer": "8C",

        "regression_passed": all(
            checks.values()
        ),

        "checks": checks,

        "result": result,
    }