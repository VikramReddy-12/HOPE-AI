"""
HOPE AI - 8K Adaptive Orchestrator
==================================

8K is the top-level advisory adapter for the 8A-8J
adaptive intelligence pipeline.

ARCHITECTURE
------------

7J remains authoritative.

7J
 |
 +--> 8A Adaptive Intelligence
 |
 +--> 8B Adaptive Strategy
 |
 +--> 8C Adaptive Orchestration
 |
 +--> 8D Adaptive Decision
 |
 +--> 8E Adaptive Response
 |
 +--> 8F Adaptive Learning
 |
 +--> 8G Adaptive Experience
 |
 +--> 8H Adaptive Integration
 |
 +--> 8J Adaptive Validation
 |
 +--> 8K Final Adaptive Result

IMPORTANT
---------

8K:

- does not replace 7J
- does not execute intelligence engines
- does not override decisions
- does not authorize automatic action
- does not authorize execution
- does not authorize self-modification

7J output remains authoritative.
"""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any, Dict, List


# ============================================================
# ADAPTIVE LAYER IMPORTS
# ============================================================

from core.adaptive_intelligence import (
    analyze_adaptation_dict,
)

from core.adaptive_strategy import (
    integrate_adaptive_strategy,
)

from core.adaptive_orchestration import (
    integrate_adaptive_orchestration,
)

from core.adaptive_decision import (
    integrate_adaptive_decision,
)

from core.adaptive_response import (
    integrate_adaptive_response,
)

from core.adaptive_learning import (
    integrate_adaptive_learning,
)

from core.adaptive_experience import (
    integrate_adaptive_experience,
)

from core.adaptive_integration import (
    integrate_adaptive_intelligence,
)

from core.adaptive_validation import (
    validate_adaptive_result,
)


# ============================================================
# VERSION
# ============================================================

ADAPTIVE_ORCHESTRATOR_VERSION = "8K"
ADAPTIVE_ORCHESTRATOR_STATUS = "READY"


# ============================================================
# GLOBAL SAFETY CONTRACT
# ============================================================

SAFETY_LEVEL = "ADVISORY_ONLY"

EXECUTION_ALLOWED = False
AUTOMATIC_ACTION_ALLOWED = False
SELF_MODIFICATION_ALLOWED = False
DECISION_OVERRIDE_ALLOWED = False


# ============================================================
# SAFETY
# ============================================================

def get_adaptive_orchestrator_safety() -> Dict[str, Any]:
    """
    Return the immutable 8K safety contract.
    """

    return {
        "safety_level": SAFETY_LEVEL,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
    }


def validate_adaptive_orchestrator_safety() -> bool:
    """
    Validate the complete 8K safety contract.
    """

    return (
        SAFETY_LEVEL == "ADVISORY_ONLY"
        and EXECUTION_ALLOWED is False
        and AUTOMATIC_ACTION_ALLOWED is False
        and SELF_MODIFICATION_ALLOWED is False
        and DECISION_OVERRIDE_ALLOWED is False
    )


def _force_advisory_safety(
    data: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Enforce the 8K advisory-only boundary.

    Upstream adaptive data can never weaken this boundary.
    """

    result = dict(data)

    result["safety"] = (
        get_adaptive_orchestrator_safety()
    )

    result["execution_allowed"] = False
    result["automatic_action_allowed"] = False
    result["self_modification_allowed"] = False
    result["decision_override_allowed"] = False

    return result


# ============================================================
# NORMALIZATION
# ============================================================

def _dict(
    value: Any,
) -> Dict[str, Any]:
    """
    Safely convert dictionaries, dataclasses and
    mapping-like objects into dictionaries.
    """

    if isinstance(value, dict):
        return dict(value)

    if is_dataclass(value):
        try:
            return asdict(value)
        except Exception:
            return {}

    if value is None:
        return {}

    try:
        return dict(value)
    except (TypeError, ValueError):
        return {}


def _safe_list(
    value: Any,
) -> List[Any]:
    """
    Safely normalize list-like values.
    """

    if isinstance(value, list):
        return list(value)

    if isinstance(value, tuple):
        return list(value)

    return []


def _safe_string(
    value: Any,
    default: str = "",
) -> str:
    """
    Normalize a value to a string.
    """

    if value is None:
        return default

    text = str(value).strip()

    return text if text else default


def _first_value(
    *values: Any,
    default: Any = "",
) -> Any:
    """
    Return the first meaningful value.
    """

    for value in values:

        if value is None:
            continue

        if isinstance(value, str):

            if value.strip():
                return value

            continue

        if value != "":
            return value

    return default


def _nested_dict(
    source: Dict[str, Any],
    *keys: str,
) -> Dict[str, Any]:
    """
    Safely retrieve the first dictionary found under
    the supplied keys.
    """

    for key in keys:

        value = source.get(key)

        if isinstance(value, dict):
            return dict(value)

    return {}


# ============================================================
# 7J EXTRACTION
# ============================================================

def _extract_7j_payload(
    orchestration_result: Any,
) -> Dict[str, Any]:
    """
    Extract the complete authoritative 7J result.

    Supports:

    - OrchestrationResult dataclasses
    - dictionaries
    - mapping-like objects

    This function intentionally reads rather than modifies
    the original 7J result.
    """

    if orchestration_result is None:
        return {}

    result = _dict(orchestration_result)

    return result


def _extract_authoritative_7j_fields(
    orchestration_result: Any,
) -> Dict[str, Any]:
    """
    Extract authoritative fields from a real 7J
    OrchestrationResult.

    IMPORTANT:

    7J fields can exist at different levels.

    Therefore extraction checks:

        1. top-level 7J object
        2. 7J result payload
        3. 7J context
        4. decision_synthesis
        5. response_synthesis
        6. learning_feedback
        7. experience_memory

    8K does not invent authoritative values.
    """

    root = _extract_7j_payload(
        orchestration_result
    )

    result_payload = _dict(
        root.get("result")
    )

    context = _dict(
        root.get("context")
    )

    decision_synthesis = _nested_dict(
        result_payload,
        "decision_synthesis",
        "decision",
        "decision_result",
    )

    response_synthesis = _nested_dict(
        result_payload,
        "response_synthesis",
        "response",
    )

    learning_feedback = _nested_dict(
        result_payload,
        "learning_feedback",
        "learning",
    )

    experience_memory = _nested_dict(
        result_payload,
        "experience_memory",
        "experience",
    )

    experience = _nested_dict(
        experience_memory,
        "experience",
    )

    # --------------------------------------------------------
    # TRACE
    # --------------------------------------------------------

    trace_id = _first_value(
        root.get("trace_id"),
        result_payload.get("trace_id"),
        context.get("trace_id"),
        default="",
    )

    # --------------------------------------------------------
    # DECISION
    # --------------------------------------------------------

    decision = _first_value(
        root.get("decision"),
        result_payload.get("decision"),
        decision_synthesis.get("decision"),
        context.get("decision"),
        default="",
    )

    # --------------------------------------------------------
    # CONFIDENCE
    # --------------------------------------------------------

    confidence = _first_value(
        root.get("confidence"),
        result_payload.get("confidence"),
        decision_synthesis.get("confidence"),
        context.get("confidence"),
        default="",
    )

    # --------------------------------------------------------
    # PRIORITY
    # --------------------------------------------------------

    priority = _first_value(
        root.get("priority"),
        result_payload.get("priority"),
        decision_synthesis.get("priority"),
        context.get("priority"),
        default="",
    )

    # --------------------------------------------------------
    # STRATEGY
    # --------------------------------------------------------

    strategy = _first_value(
        root.get("strategy"),
        result_payload.get("strategy"),
        decision_synthesis.get("strategy"),
        context.get("strategy"),
        default="",
    )

    # --------------------------------------------------------
    # LEARNING SIGNAL
    # --------------------------------------------------------

    learning_signal = _first_value(
        root.get("learning_signal"),
        result_payload.get("learning_signal"),
        learning_feedback.get("learning_signal"),
        context.get("learning_signal"),
        default="",
    )

    # --------------------------------------------------------
    # RESPONSE
    # --------------------------------------------------------

    response = _first_value(
        root.get("response"),
        result_payload.get("response"),
        response_synthesis.get("response"),
        context.get("response"),
        default="",
    )

    # --------------------------------------------------------
    # EXPERIENCE
    # --------------------------------------------------------

    experience_id = _first_value(
        root.get("experience_id"),
        result_payload.get("experience_id"),
        experience_memory.get("experience_id"),
        experience.get("experience_id"),
        context.get("experience_id"),
        default="",
    )

    # --------------------------------------------------------
    # EXPERIENCE OBJECT
    # --------------------------------------------------------

    authoritative_experience = {}

    if experience:
        authoritative_experience = dict(
            experience
        )

    elif isinstance(
        result_payload.get("experience"),
        dict,
    ):
        authoritative_experience = dict(
            result_payload.get("experience")
        )

    elif isinstance(
        root.get("experience"),
        dict,
    ):
        authoritative_experience = dict(
            root.get("experience")
        )

    # Preserve experience ID.
    if experience_id:
        authoritative_experience[
            "experience_id"
        ] = experience_id

    # --------------------------------------------------------
    # EVIDENCE
    # --------------------------------------------------------

    evidence_candidates = [
        root.get("evidence"),
        result_payload.get("evidence"),
        decision_synthesis.get("evidence"),
        context.get("evidence"),
    ]

    evidence = []

    for candidate in evidence_candidates:

        if isinstance(candidate, list):
            evidence = list(candidate)
            break

    # --------------------------------------------------------
    # ENGINES
    # --------------------------------------------------------

    engine_candidates = [
        root.get("selected_engines"),
        root.get("contributing_engines"),
        result_payload.get("selected_engines"),
        result_payload.get("contributing_engines"),
        context.get("selected_engines"),
        context.get("contributing_engines"),
        decision_synthesis.get("selected_engines"),
        decision_synthesis.get("contributing_engines"),
    ]

    contributing_engines = []

    for candidate in engine_candidates:

        if isinstance(candidate, list):
            contributing_engines = list(candidate)
            break

    # --------------------------------------------------------
    # PIPELINE
    # --------------------------------------------------------

    pipeline = _safe_list(
        _first_value(
            root.get("pipeline"),
            result_payload.get("pipeline"),
            context.get("pipeline"),
            default=[],
        )
    )

    # --------------------------------------------------------
    # SELECTED ENGINES FALLBACK
    # --------------------------------------------------------

    if not contributing_engines:

        selected_engines = _safe_list(
            root.get("selected_engines")
        )

        if selected_engines:
            contributing_engines = (
                selected_engines
            )

    # --------------------------------------------------------
    # 7J STATUS
    # --------------------------------------------------------

    status = _first_value(
        root.get("status"),
        result_payload.get("status"),
        default="",
    )

    # --------------------------------------------------------
    # 7J SAFETY
    # --------------------------------------------------------

    source_safety = _dict(
        root.get("safety")
    )

    return {
        "trace_id": trace_id,
        "status": status,
        "decision": decision,
        "confidence": confidence,
        "priority": priority,
        "strategy": strategy,
        "learning_signal": learning_signal,
        "experience_id": experience_id,
        "experience": authoritative_experience,
        "response": response,
        "evidence": evidence,
        "contributing_engines": (
            contributing_engines
        ),
        "selected_engines": (
            list(contributing_engines)
        ),
        "pipeline": pipeline,
        "source_safety": source_safety,
        "root": root,
        "result_payload": result_payload,
        "context": context,
    }


# ============================================================
# FIELD PRESERVATION
# ============================================================

def _preserve_required_fields(
    result: Dict[str, Any],
    *,
    trace_id: str,
    decision: Any,
    confidence: Any,
    priority: Any,
    strategy: Any,
    learning_signal: Any,
    response: Any,
    evidence: List[Any],
    contributing_engines: List[Any],
    experience: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Restore authoritative 7J values after the adaptive
    pipeline has completed.

    Adaptive processing must never cause authoritative
    7J fields to disappear.
    """

    output = dict(result)

    output["trace_id"] = trace_id
    output["decision"] = decision
    output["confidence"] = confidence
    output["priority"] = priority
    output["strategy"] = strategy
    output["learning_signal"] = learning_signal

    if response not in (None, ""):
        output["response"] = response

    elif not output.get("response"):
        output["response"] = (
            "Adaptive advisory response generated."
        )

    output["evidence"] = list(evidence)

    # CRITICAL:
    # Preserve the actual 7J engines.
    output["contributing_engines"] = list(
        contributing_engines
    )

    if not output.get("experience"):
        output["experience"] = dict(
            experience
        )

    experience_id = _first_value(
        experience.get("experience_id"),
        default="",
    )

    if experience_id:
        output["experience_id"] = (
            experience_id
        )

    if not output.get("orchestration"):
        output["orchestration"] = {
            "layer": "8H",
            "status": "READY",
        }

    if not output.get("orchestration_state"):
        output["orchestration_state"] = (
            "READY"
        )

    return _force_advisory_safety(
        output
    )


# ============================================================
# 8A -> 8J CHAIN
# ============================================================

def run_adaptive_chain(
    *,
    trace_id: Any,
    decision: Any,
    confidence: Any,
    priority: Any,
    learning_signal: Any,
    evidence: Any,
    contributing_engines: Any,
    experience: Any,
    response: Any = "",
    strategy: Any = "",
) -> Dict[str, Any]:
    """
    Run the existing 8A-8J advisory pipeline.

    No intelligence engine is executed here.
    """

    trace = _safe_string(
        trace_id
    )

    if not trace:
        raise ValueError(
            "trace_id cannot be empty."
        )

    base_decision = decision
    base_confidence = confidence
    base_priority = priority
    base_learning_signal = learning_signal
    base_strategy = strategy

    base_evidence = _safe_list(
        evidence
    )

    base_engines = _safe_list(
        contributing_engines
    )

    base_experience = _dict(
        experience
    )

    base_response = response

    # ========================================================
    # 8A
    # ========================================================

    adaptive_intelligence = (
        analyze_adaptation_dict(
            trace_id=trace,
            decision=base_decision,
            confidence=base_confidence,
            priority=base_priority,
            learning_signal=base_learning_signal,
            evidence=base_evidence,
            contributing_engines=base_engines,
            source_experience_id=_first_value(
                base_experience.get(
                    "experience_id"
                ),
                default="",
            ),
        )
    )

    adaptive_intelligence = (
        _force_advisory_safety(
            _dict(
                adaptive_intelligence
            )
        )
    )

    # ========================================================
    # 8B
    # ========================================================

    adaptive_strategy = (
        integrate_adaptive_strategy(
            adaptive_intelligence
        )
    )

    adaptive_strategy = (
        _force_advisory_safety(
            _dict(
                adaptive_strategy
            )
        )
    )

    generated_strategy = _first_value(
        adaptive_strategy.get("strategy"),
        base_strategy,
        default="",
    )

    # ========================================================
    # 8C
    # ========================================================

    adaptive_orchestration = (
        integrate_adaptive_orchestration(
            adaptive_strategy
        )
    )

    adaptive_orchestration = (
        _force_advisory_safety(
            _dict(
                adaptive_orchestration
            )
        )
    )

    # ========================================================
    # 8D
    # ========================================================

    adaptive_decision = (
        integrate_adaptive_decision(
            adaptive_orchestration
        )
    )

    adaptive_decision = (
        _force_advisory_safety(
            _dict(
                adaptive_decision
            )
        )
    )

    # ========================================================
    # 8E
    # ========================================================

    adaptive_response = (
        integrate_adaptive_response(
            adaptive_decision
        )
    )

    adaptive_response = (
        _force_advisory_safety(
            _dict(
                adaptive_response
            )
        )
    )

    # ========================================================
    # 8F
    # ========================================================

    adaptive_learning = (
        integrate_adaptive_learning(
            adaptive_response
        )
    )

    adaptive_learning = (
        _force_advisory_safety(
            _dict(
                adaptive_learning
            )
        )
    )

    # ========================================================
    # 8G
    # ========================================================

    adaptive_experience_obj = (
        integrate_adaptive_experience(
            trace_id=trace,
            experience=base_experience,
            learning=adaptive_learning,
            decision=base_decision,
            confidence=base_confidence,
            priority=base_priority,
            evidence=base_evidence,
            contributing_engines=base_engines,
        )
    )

    adaptive_experience = (
        _force_advisory_safety(
            _dict(
                adaptive_experience_obj
            )
        )
    )

    # ========================================================
    # 8H
    # ========================================================

    adaptive_integration_obj = (
        integrate_adaptive_intelligence(
            trace_id=trace,
            adaptive_intelligence=adaptive_intelligence,
            adaptive_strategy=adaptive_strategy,
            adaptive_orchestration=adaptive_orchestration,
            adaptive_decision=adaptive_decision,
            adaptive_response=adaptive_response,
            adaptive_learning=adaptive_learning,
            adaptive_experience=adaptive_experience,
            decision=base_decision,
            confidence=base_confidence,
            priority=base_priority,
            response=base_response,
            evidence=base_evidence,
        )
    )

    adaptive_integration = (
        _force_advisory_safety(
            _dict(
                adaptive_integration_obj
            )
        )
    )

    # ========================================================
    # PRESERVE AUTHORITATIVE 7J DATA
    # ========================================================

    final_result = (
        _preserve_required_fields(
            adaptive_integration,
            trace_id=trace,
            decision=base_decision,
            confidence=base_confidence,
            priority=base_priority,
            strategy=generated_strategy,
            learning_signal=base_learning_signal,
            response=base_response,
            evidence=base_evidence,
            contributing_engines=base_engines,
            experience=base_experience,
        )
    )

    # ========================================================
    # 8J VALIDATION
    # ========================================================

    validation = validate_adaptive_result(
        final_result
    )

    final_result["validation"] = validation

    # ========================================================
    # SAFETY
    # ========================================================

    final_result = (
        _force_advisory_safety(
            final_result
        )
    )

    # ========================================================
    # ERRORS
    # ========================================================

    errors: List[str] = []

    validation_checks = _dict(
        validation.get("checks")
    )

    for check_name, passed in (
        validation_checks.items()
    ):

        if passed is False:
            errors.append(
                str(check_name)
            )

    final_result["errors"] = errors

    # ========================================================
    # METADATA
    # ========================================================

    final_result["layer"] = (
        ADAPTIVE_ORCHESTRATOR_VERSION
    )

    final_result["status"] = (
        ADAPTIVE_ORCHESTRATOR_STATUS
    )

    final_result["layers"] = [
        "7J",
        "8A",
        "8B",
        "8C",
        "8D",
        "8E",
        "8F",
        "8G",
        "8H",
        "8J",
        "8K",
    ]

    final_result["contributing_layers"] = [
        "7J",
        "8A",
        "8B",
        "8C",
        "8D",
        "8E",
        "8F",
        "8G",
        "8H",
        "8J",
        "8K",
    ]

    final_result["orchestration_state"] = (
        final_result.get(
            "orchestration_state",
            "READY",
        )
    )

    return final_result


# ============================================================
# REAL 7J -> 8K ADAPTER
# ============================================================

def build_adaptive_orchestrator_result(
    orchestration_result: Any,
) -> Dict[str, Any]:
    """
    Convert a REAL 7J OrchestrationResult into the
    complete 8K adaptive result.

    This is the critical real-integration entry point.

    It extracts:

        trace_id
        status
        decision
        confidence
        priority
        strategy
        learning_signal
        experience_id
        response
        evidence
        selected/contributing engines
        pipeline

    from the actual 7J result.

    7J remains authoritative.
    """

    if orchestration_result is None:

        return {
            "layer": ADAPTIVE_ORCHESTRATOR_VERSION,
            "status": "INVALID",
            "trace_id": "",
            "decision": "",
            "confidence": "",
            "priority": "",
            "adaptation_state": (
                "INSUFFICIENT_DATA"
            ),
            "strategy": "",
            "orchestration_state": "",
            "learning_signal": "",
            "experience_id": "",
            "response": "",
            "recommendation": "",
            "evidence": [],
            "contributing_layers": [],
            "contributing_engines": [],
            "safety": (
                get_adaptive_orchestrator_safety()
            ),
            "errors": [
                "No orchestration result was supplied."
            ],
        }

    fields = (
        _extract_authoritative_7j_fields(
            orchestration_result
        )
    )

    trace_id = fields["trace_id"]

    if not trace_id:

        return {
            "layer": ADAPTIVE_ORCHESTRATOR_VERSION,
            "status": "INVALID",
            "trace_id": "",
            "decision": "",
            "confidence": "",
            "priority": "",
            "adaptation_state": (
                "INSUFFICIENT_DATA"
            ),
            "strategy": "",
            "orchestration_state": "",
            "learning_signal": "",
            "experience_id": "",
            "response": "",
            "recommendation": "",
            "evidence": [],
            "contributing_layers": [],
            "contributing_engines": [],
            "safety": (
                get_adaptive_orchestrator_safety()
            ),
            "errors": [
                "7J result did not contain trace_id."
            ],
        }

    adaptive_result = run_adaptive_chain(
        trace_id=trace_id,
        decision=fields["decision"],
        confidence=fields["confidence"],
        priority=fields["priority"],
        learning_signal=fields[
            "learning_signal"
        ],
        evidence=fields["evidence"],
        contributing_engines=fields[
            "contributing_engines"
        ],
        experience=fields["experience"],
        response=fields["response"],
        strategy=fields["strategy"],
    )

    # --------------------------------------------------------
    # Preserve actual 7J metadata
    # --------------------------------------------------------

    adaptive_result["7j_status"] = (
        fields["status"]
    )

    adaptive_result["7j_selected_engines"] = (
        list(fields["selected_engines"])
    )

    adaptive_result["7j_pipeline"] = (
        list(fields["pipeline"])
    )

    adaptive_result["7j_safety"] = dict(
        fields["source_safety"]
    )

    # --------------------------------------------------------
    # Authoritative engine preservation
    # --------------------------------------------------------

    adaptive_result[
        "contributing_engines"
    ] = list(
        fields["contributing_engines"]
    )

    # --------------------------------------------------------
    # Authoritative decision preservation
    # --------------------------------------------------------

    adaptive_result["decision"] = (
        fields["decision"]
    )

    adaptive_result["confidence"] = (
        fields["confidence"]
    )

    adaptive_result["priority"] = (
        fields["priority"]
    )

    adaptive_result["strategy"] = (
        fields["strategy"]
        or adaptive_result.get(
            "strategy",
            "",
        )
    )

    adaptive_result["learning_signal"] = (
        fields["learning_signal"]
    )

    adaptive_result["experience_id"] = (
        fields["experience_id"]
    )

    if fields["response"]:
        adaptive_result["response"] = (
            fields["response"]
        )

    adaptive_result["evidence"] = list(
        fields["evidence"]
    )

    adaptive_result["trace_id"] = (
        fields["trace_id"]
    )

    # --------------------------------------------------------
    # Safety is always 8K controlled
    # --------------------------------------------------------

    adaptive_result = (
        _force_advisory_safety(
            adaptive_result
        )
    )

    # --------------------------------------------------------
    # Re-run validation after authoritative fields
    # are restored.
    # --------------------------------------------------------

    validation = validate_adaptive_result(
        adaptive_result
    )

    adaptive_result["validation"] = (
        validation
    )

    errors = []

    for name, passed in _dict(
        validation.get("checks")
    ).items():

        if passed is False:
            errors.append(
                str(name)
            )

    adaptive_result["errors"] = errors

    return adaptive_result


# ============================================================
# REGRESSION
# ============================================================

def get_adaptive_orchestration_regression() -> Dict[str, Any]:
    """
    Deterministic 8A-8J-8K regression.
    """

    sample_experience = {
        "experience_id": "EXP-8K-001",
        "reasoning": (
            "risk reasoning preserved"
        ),
        "predictive": (
            "predictive risk preserved"
        ),
    }

    sample_evidence = [
        {
            "source": "regression",
            "value": "test",
        }
    ]

    sample_engines = [
        "reasoning",
        "predictive_risk",
    ]

    result = run_adaptive_chain(
        trace_id="TEST-8K-001",
        decision=(
            "PREDICTIVE_RISK_ASSESSMENT"
        ),
        confidence="0.92",
        priority="HIGH",
        learning_signal=(
            "RISK_PATTERN_DETECTED"
        ),
        evidence=sample_evidence,
        contributing_engines=sample_engines,
        experience=sample_experience,
        response=(
            "Predictive risk assessment response"
        ),
        strategy="ADAPTIVE",
    )

    validation = _dict(
        result.get("validation")
    )

    validation_checks = _dict(
        validation.get("checks")
    )

    checks = {
        "status_ready": (
            result.get("status")
            == "READY"
        ),

        "trace_preserved": (
            result.get("trace_id")
            == "TEST-8K-001"
        ),

        "decision_populated": bool(
            result.get("decision")
        ),

        "confidence_populated": bool(
            result.get("confidence")
        ),

        "priority_populated": bool(
            result.get("priority")
        ),

        "strategy_populated": bool(
            result.get("strategy")
        ),

        "learning_signal_populated": bool(
            result.get("learning_signal")
        ),

        "experience_id_populated": bool(
            result.get("experience_id")
        ),

        "response_populated": bool(
            result.get("response")
        ),

        "evidence_preserved": (
            result.get("evidence")
            == sample_evidence
        ),

        "engines_preserved": (
            result.get(
                "contributing_engines"
            )
            == sample_engines
        ),

        "reasoning_preserved": (
            "reasoning"
            in result.get(
                "experience",
                {},
            )
        ),

        "predictive_preserved": (
            "predictive"
            in result.get(
                "experience",
                {},
            )
        ),

        "8j_validation": (
            validation.get(
                "validation_passed"
            )
            is True
        ),

        "8j_engines_preserved": (
            validation_checks.get(
                "engines_preserved"
            )
            is True
        ),

        "8j_global_safety_valid": (
            validation_checks.get(
                "global_safety_valid"
            )
            is True
        ),

        "safety_advisory": (
            result.get(
                "safety",
                {},
            ).get(
                "safety_level"
            )
            == "ADVISORY_ONLY"
        ),

        "execution_blocked": (
            result.get(
                "safety",
                {},
            ).get(
                "execution_allowed"
            )
            is False
        ),

        "automatic_action_blocked": (
            result.get(
                "safety",
                {},
            ).get(
                "automatic_action_allowed"
            )
            is False
        ),

        "self_modification_blocked": (
            result.get(
                "safety",
                {},
            ).get(
                "self_modification_allowed"
            )
            is False
        ),

        "decision_override_blocked": (
            result.get(
                "safety",
                {},
            ).get(
                "decision_override_allowed"
            )
            is False
        ),

        "all_layers_present": (
            all(
                layer in result.get(
                    "layers",
                    [],
                )
                for layer in [
                    "7J",
                    "8A",
                    "8B",
                    "8C",
                    "8D",
                    "8E",
                    "8F",
                    "8G",
                    "8H",
                    "8J",
                    "8K",
                ]
            )
        ),

        "global_safety_valid": (
            validate_adaptive_orchestrator_safety()
        ),
    }

    regression_passed = all(
        checks.values()
    )

    return {
        "integration_layer": "8K",

        "integration_status": (
            "READY"
            if regression_passed
            else "FAILED"
        ),

        "regression_passed": (
            regression_passed
        ),

        "checks": checks,

        "validation": validation,

        "errors": result.get(
            "errors",
            [],
        ),

        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
    }


# ============================================================
# STATUS
# ============================================================

def get_adaptive_orchestrator_status() -> Dict[str, Any]:
    """
    Return current 8K status.
    """

    return {
        "layer": ADAPTIVE_ORCHESTRATOR_VERSION,
        "status": ADAPTIVE_ORCHESTRATOR_STATUS,
        "safety_level": SAFETY_LEVEL,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
        "safety_valid": (
            validate_adaptive_orchestrator_safety()
        ),
    }


# ============================================================
# COMPATIBILITY ALIAS
# ============================================================

def get_adaptive_orchestration_status() -> Dict[str, Any]:
    """
    Compatibility alias.
    """

    return get_adaptive_orchestrator_status()


# ============================================================
# EXPORTS
# ============================================================

__all__ = [
    "get_adaptive_orchestrator_safety",
    "validate_adaptive_orchestrator_safety",
    "get_adaptive_orchestrator_status",
    "get_adaptive_orchestration_status",
    "run_adaptive_chain",
    "build_adaptive_orchestrator_result",
    "get_adaptive_orchestration_regression",
]


# ============================================================
# SELF TEST
# ============================================================

if __name__ == "__main__":

    regression = (
        get_adaptive_orchestration_regression()
    )

    print(
        "8A-8J / 8K REGRESSION:"
    )

    print(
        regression
    )