"""
HOPE-AI 9A Capability Registry

Defines the capabilities currently available to HOPE.

This layer only describes capabilities.
It does not execute actions.
"""

LAYER = "9A"
STATUS_READY = "READY"


CAPABILITIES = {
    "knowledge": {
        "name": "Knowledge",
        "description": "Answer knowledge-based questions.",
        "available": True,
        "execution_required": False,
    },
    "memory": {
        "name": "Memory",
        "description": "Store and recall user information.",
        "available": True,
        "execution_required": False,
    },
    "conversation": {
        "name": "Conversation",
        "description": "Maintain conversation context and history.",
        "available": True,
        "execution_required": False,
    },
    "reasoning": {
        "name": "Reasoning",
        "description": "Reason over available information.",
        "available": True,
        "execution_required": False,
    },
    "goals": {
        "name": "Goals",
        "description": "Manage long-term goals and progress.",
        "available": True,
        "execution_required": False,
    },
    "planning": {
        "name": "Planning",
        "description": "Create and manage plans.",
        "available": True,
        "execution_required": False,
    },
    "adaptive_intelligence": {
        "name": "Adaptive Intelligence",
        "description": "Evaluate and adapt intelligent decisions.",
        "available": True,
        "execution_required": False,
    },
    "governance": {
        "name": "Governance",
        "description": "Apply governance constraints to adaptive intelligence.",
        "available": True,
        "execution_required": False,
    },
    "oversight": {
        "name": "Oversight",
        "description": "Provide advisory oversight of governed results.",
        "available": True,
        "execution_required": False,
    },
    "accountability": {
        "name": "Accountability",
        "description": "Maintain accountability and audit boundaries.",
        "available": True,
        "execution_required": False,
    },
}


def get_capabilities():
    """Return a copy of the registered capabilities."""
    return {
        key: dict(value)
        for key, value in CAPABILITIES.items()
    }


def get_capability(name):
    """Return one registered capability, or None if unavailable."""
    return CAPABILITIES.get(name)


def is_capability_available(name):
    """Return whether a capability is registered and available."""
    capability = CAPABILITIES.get(name)

    if capability is None:
        return False

    return capability["available"] is True


def get_capability_status():
    """Return the current 9A capability registry status."""
    return {
        "layer": LAYER,
        "status": STATUS_READY,
        "capability_count": len(CAPABILITIES),
        "available_capabilities": [
            key
            for key, value in CAPABILITIES.items()
            if value["available"] is True
        ],
        "execution_enabled": False,
    }


def get_capability_regression():
    """Validate the 9A capability registry."""
    capabilities = get_capabilities()

    checks = {
        "layer_9a": LAYER == "9A",
        "status_ready": STATUS_READY == "READY",
        "capabilities_available": len(capabilities) > 0,
        "knowledge_available": is_capability_available("knowledge"),
        "memory_available": is_capability_available("memory"),
        "conversation_available": is_capability_available("conversation"),
        "reasoning_available": is_capability_available("reasoning"),
        "goals_available": is_capability_available("goals"),
        "planning_available": is_capability_available("planning"),
        "adaptive_available": is_capability_available(
            "adaptive_intelligence"
        ),
        "governance_available": is_capability_available("governance"),
        "oversight_available": is_capability_available("oversight"),
        "accountability_available": is_capability_available(
            "accountability"
        ),
        "unknown_capability_blocked": not is_capability_available(
            "voice"
        ),
        "execution_disabled": get_capability_status()[
            "execution_enabled"
        ] is False,
    }

    return {
        "integration_layer": LAYER,
        "integration_status": STATUS_READY,
        "regression_passed": all(checks.values()),
        "checks": checks,
        "capabilities": capabilities,
        "execution_enabled": False,
    }


if __name__ == "__main__":
    print("9A CAPABILITY REGISTRY REGRESSION:")
    print(get_capability_regression())
