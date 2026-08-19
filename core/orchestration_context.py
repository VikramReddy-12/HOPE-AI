"""
HOPE AI — 7D Cross-Engine Orchestration Context

Provides an isolated, traceable context object for information
flow between HOPE intelligence engines.

7D responsibilities:
    - Maintain request-level orchestration context
    - Store selected engines and pipeline
    - Store engine outputs
    - Preserve cross-engine information
    - Track stage execution metadata
    - Preserve safety state
    - Provide deterministic context snapshots

This module does NOT execute engines.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


# ============================================================
# VERSION
# ============================================================

CONTEXT_VERSION = "7D"


# ============================================================
# TIME
# ============================================================

def _utc_timestamp() -> str:
    """
    Return a UTC ISO-8601 timestamp.
    """

    return datetime.now(
        timezone.utc
    ).isoformat()


# ============================================================
# ENGINE CONTEXT RECORD
# ============================================================

@dataclass
class EngineContextRecord:
    """
    Information produced or consumed by one engine.
    """

    engine_id: str
    stage: str

    input_data: Dict[str, Any] = field(
        default_factory=dict
    )

    output_data: Dict[str, Any] = field(
        default_factory=dict
    )

    status: str = "READY"

    timestamp: str = ""

    trace_id: str = ""

    def __post_init__(self) -> None:
        """
        Populate the timestamp automatically when required.
        """

        if not self.timestamp:
            self.timestamp = _utc_timestamp()


# ============================================================
# ORCHESTRATION CONTEXT
# ============================================================

@dataclass
class OrchestrationContext:
    """
    Shared request-level context.

    The context belongs to one orchestration request and should
    never be treated as global mutable system state.
    """

    trace_id: str

    command: str = ""

    intent: str = ""

    requested_capabilities: List[str] = field(
        default_factory=list
    )

    selected_engines: List[str] = field(
        default_factory=list
    )

    pipeline: List[str] = field(
        default_factory=list
    )

    engine_outputs: Dict[str, Any] = field(
        default_factory=dict
    )

    stage_outputs: Dict[str, Any] = field(
        default_factory=dict
    )

    engine_records: List[EngineContextRecord] = field(
        default_factory=list
    )

    knowledge_context: Dict[str, Any] = field(
        default_factory=dict
    )

    memory_context: Dict[str, Any] = field(
        default_factory=dict
    )

    reasoning_context: Dict[str, Any] = field(
        default_factory=dict
    )

    prediction_context: Dict[str, Any] = field(
        default_factory=dict
    )

    validation_context: Dict[str, Any] = field(
        default_factory=dict
    )

    safety: Dict[str, Any] = field(
        default_factory=lambda: {
            "level": "ADVISORY_ONLY",
            "execution_allowed": False,
            "automatic_action_allowed": False,
        }
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    created_at: str = field(
        default_factory=_utc_timestamp
    )

    updated_at: str = field(
        default_factory=_utc_timestamp
    )

    version: str = CONTEXT_VERSION

    # ========================================================
    # TIMESTAMP
    # ========================================================

    def touch(self) -> None:
        """
        Update the context modification timestamp.
        """

        self.updated_at = _utc_timestamp()

    # ========================================================
    # ENGINE OUTPUT
    # ========================================================

    def set_engine_output(
        self,
        engine_id: str,
        stage: str,
        output: Any,
    ) -> None:
        """
        Store output produced by an engine.
        """

        self.engine_outputs[
            engine_id
        ] = output

        self.stage_outputs[
            stage
        ] = output

        self.engine_records.append(
            EngineContextRecord(
                engine_id=engine_id,
                stage=stage,
                output_data=_safe_dict(output),
                status="READY",
                trace_id=self.trace_id,
            )
        )

        self.touch()

    # ========================================================
    # ENGINE INPUT
    # ========================================================

    def set_engine_input(
        self,
        engine_id: str,
        stage: str,
        input_data: Dict[str, Any],
    ) -> None:
        """
        Record information supplied to an engine.
        """

        self.engine_records.append(
            EngineContextRecord(
                engine_id=engine_id,
                stage=stage,
                input_data=dict(input_data),
                status="INPUT_READY",
                trace_id=self.trace_id,
            )
        )

        self.touch()

    # ========================================================
    # ENGINE OUTPUT RETRIEVAL
    # ========================================================

    def get_engine_output(
        self,
        engine_id: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieve the latest output of an engine.
        """

        return self.engine_outputs.get(
            engine_id,
            default,
        )

    # ========================================================
    # STAGE OUTPUT RETRIEVAL
    # ========================================================

    def get_stage_output(
        self,
        stage: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieve the latest output associated with a stage.
        """

        return self.stage_outputs.get(
            stage,
            default,
        )

    # ========================================================
    # KNOWLEDGE CONTEXT
    # ========================================================

    def update_knowledge(
        self,
        data: Dict[str, Any],
    ) -> None:
        """
        Update shared knowledge context.
        """

        self.knowledge_context.update(
            data
        )

        self.touch()

    # ========================================================
    # MEMORY CONTEXT
    # ========================================================

    def update_memory(
        self,
        data: Dict[str, Any],
    ) -> None:
        """
        Update shared memory context.
        """

        self.memory_context.update(
            data
        )

        self.touch()

    # ========================================================
    # REASONING CONTEXT
    # ========================================================

    def update_reasoning(
        self,
        data: Dict[str, Any],
    ) -> None:
        """
        Update shared reasoning context.
        """

        self.reasoning_context.update(
            data
        )

        self.touch()

    # ========================================================
    # PREDICTION CONTEXT
    # ========================================================

    def update_prediction(
        self,
        data: Dict[str, Any],
    ) -> None:
        """
        Update shared predictive context.
        """

        self.prediction_context.update(
            data
        )

        self.touch()

    # ========================================================
    # VALIDATION CONTEXT
    # ========================================================

    def update_validation(
        self,
        data: Dict[str, Any],
    ) -> None:
        """
        Update shared validation context.
        """

        self.validation_context.update(
            data
        )

        self.touch()

    # ========================================================
    # SAFETY
    # ========================================================

    def update_safety(
        self,
        data: Dict[str, Any],
    ) -> None:
        """
        Update safety state while preserving the
        mandatory execution boundary.
        """

        self.safety.update(
            data
        )

        # 7D must never weaken the safety boundary.
        self.safety[
            "execution_allowed"
        ] = False

        self.safety[
            "automatic_action_allowed"
        ] = False

        self.touch()

    # ========================================================
    # METADATA
    # ========================================================

    def add_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Add request-level metadata.
        """

        self.metadata[
            key
        ] = value

        self.touch()

    # ========================================================
    # SNAPSHOT
    # ========================================================

    def snapshot(self) -> Dict[str, Any]:
        """
        Return a serializable snapshot of the complete context.
        """

        return asdict(
            self
        )

    # ========================================================
    # SUMMARY
    # ========================================================

    def summary(self) -> Dict[str, Any]:
        """
        Return a compact context summary.
        """

        return {
            "version": self.version,
            "trace_id": self.trace_id,
            "command": self.command,
            "intent": self.intent,
            "requested_capabilities": list(
                self.requested_capabilities
            ),
            "selected_engines": list(
                self.selected_engines
            ),
            "pipeline": list(
                self.pipeline
            ),
            "engine_output_count": len(
                self.engine_outputs
            ),
            "stage_output_count": len(
                self.stage_outputs
            ),
            "record_count": len(
                self.engine_records
            ),
            "safety": dict(
                self.safety
            ),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


# ============================================================
# SAFE OUTPUT CONVERSION
# ============================================================

def _safe_dict(
    value: Any,
) -> Dict[str, Any]:
    """
    Convert common output values into a dictionary
    suitable for trace storage.
    """

    if isinstance(
        value,
        dict,
    ):
        return dict(
            value
        )

    if value is None:
        return {}

    return {
        "value": value
    }


# ============================================================
# CONTEXT FACTORY
# ============================================================

def create_orchestration_context(
    trace_id: str,
    command: str = "",
    intent: str = "",
    requested_capabilities: Optional[
        List[str]
    ] = None,
    selected_engines: Optional[
        List[str]
    ] = None,
    pipeline: Optional[
        List[str]
    ] = None,
    safety: Optional[
        Dict[str, Any]
    ] = None,
) -> OrchestrationContext:
    """
    Create a fresh request-level orchestration context.
    """

    context = OrchestrationContext(
        trace_id=trace_id,
        command=command,
        intent=intent,
        requested_capabilities=list(
            requested_capabilities or []
        ),
        selected_engines=list(
            selected_engines or []
        ),
        pipeline=list(
            pipeline or []
        ),
    )

    if safety:
        context.update_safety(
            safety
        )
    else:
        context.update_safety(
            {}
        )

    return context


# ============================================================
# CONTEXT VALIDATION
# ============================================================

def validate_context(
    context: OrchestrationContext,
) -> Dict[str, Any]:
    """
    Validate the 7D context contract.
    """

    errors: List[str] = []

    if not context.trace_id:
        errors.append(
            "trace_id is required."
        )

    if not isinstance(
        context.requested_capabilities,
        list,
    ):
        errors.append(
            "requested_capabilities must be a list."
        )

    if not isinstance(
        context.selected_engines,
        list,
    ):
        errors.append(
            "selected_engines must be a list."
        )

    if not isinstance(
        context.pipeline,
        list,
    ):
        errors.append(
            "pipeline must be a list."
        )

    if not isinstance(
        context.engine_outputs,
        dict,
    ):
        errors.append(
            "engine_outputs must be a dictionary."
        )

    if not isinstance(
        context.stage_outputs,
        dict,
    ):
        errors.append(
            "stage_outputs must be a dictionary."
        )

    if context.safety.get(
        "execution_allowed",
        False,
    ):
        errors.append(
            "7D context cannot allow execution."
        )

    if context.safety.get(
        "automatic_action_allowed",
        False,
    ):
        errors.append(
            "7D context cannot allow automatic actions."
        )

    return {
        "valid": not errors,
        "errors": errors,
        "trace_id": context.trace_id,
        "version": context.version,
    }


# ============================================================
# VERSION
# ============================================================

def get_context_version() -> str:
    """
    Return the current 7D context version.
    """

    return CONTEXT_VERSION