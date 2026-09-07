import unittest

from core.capabilities import get_capability_regression
from core.capability_discovery import get_capability_discovery_regression
from core.tool_architecture import get_tool_architecture_regression
from core.tool_selection import get_tool_selection_regression
from core.action_policy import get_action_policy_regression
from core.controlled_execution import get_controlled_execution_regression
from core.action_results import get_action_results_regression
from core.action_audit import get_action_audit_regression
from core.capability_integration import get_capability_integration_regression

from core.adaptive_intelligence import get_adaptive_intelligence_regression
from core.adaptive_strategy import get_adaptive_strategy_regression
from core.adaptive_orchestration import get_adaptive_orchestration_regression
from core.adaptive_decision import get_adaptive_decision_regression
from core.adaptive_response import get_adaptive_response_regression
from core.adaptive_learning import get_adaptive_learning_regression
from core.adaptive_experience import get_adaptive_experience_regression
from core.adaptive_integration import get_adaptive_integration_regression
from core.adaptive_validation import get_adaptive_validation_regression
from core.adaptive_orchestrator import get_adaptive_orchestration_regression
from core.adaptive_governance import get_adaptive_governance_regression
from core.adaptive_oversight import get_adaptive_oversight_regression
from core.adaptive_accountability import get_adaptive_accountability_regression


class TestAdaptiveLayers(unittest.TestCase):

    def test_9a(self):
        result = get_capability_regression()

        self.assertTrue(result["regression_passed"])
        self.assertEqual(result["integration_layer"], "9A")
        self.assertEqual(result["integration_status"], "READY")
        self.assertFalse(result["execution_enabled"])

        capabilities = result["capabilities"]

        self.assertIn("knowledge", capabilities)
        self.assertIn("memory", capabilities)
        self.assertIn("conversation", capabilities)
        self.assertIn("reasoning", capabilities)
        self.assertIn("goals", capabilities)
        self.assertIn("planning", capabilities)
        self.assertIn("adaptive_intelligence", capabilities)
        self.assertIn("governance", capabilities)
        self.assertIn("oversight", capabilities)
        self.assertIn("accountability", capabilities)

        self.assertNotIn("voice", capabilities)

    def test_9b(self):
        result = get_capability_discovery_regression()

        self.assertTrue(result["regression_passed"])
        self.assertEqual(result["integration_layer"], "9B")
        self.assertEqual(result["integration_status"], "READY")
        self.assertFalse(result["execution_enabled"])

        self.assertTrue(result["checks"]["memory_discovered"])
        self.assertTrue(result["checks"]["knowledge_discovered"])
        self.assertTrue(result["checks"]["planning_discovered"])
        self.assertTrue(result["checks"]["unknown_not_invented"])
        self.assertTrue(result["checks"]["execution_disabled"])
        self.assertTrue(result["checks"]["tool_selection_disabled"])
        self.assertTrue(result["checks"]["permission_disabled"])

        self.assertEqual(
            result["memory_result"]["discovered_capabilities"],
            ["memory"],
        )

        self.assertEqual(
            result["knowledge_result"]["discovered_capabilities"],
            ["knowledge"],
        )

        self.assertEqual(
            result["planning_result"]["discovered_capabilities"],
            ["planning"],
        )

        self.assertEqual(
            result["unknown_result"]["discovered_capabilities"],
            [],
        )

    def test_9c(self):
        result = get_tool_architecture_regression()

        self.assertTrue(result["regression_passed"])
        self.assertEqual(result["integration_layer"], "9C")
        self.assertEqual(result["integration_status"], "READY")
        self.assertFalse(result["execution_enabled"])

        checks = result["checks"]

        self.assertTrue(checks["tools_available"])
        self.assertTrue(checks["knowledge_tool_registered"])
        self.assertTrue(checks["memory_store_registered"])
        self.assertTrue(checks["memory_recall_registered"])
        self.assertTrue(checks["knowledge_capability_mapping"])
        self.assertTrue(checks["memory_capability_mapping"])
        self.assertTrue(checks["unknown_tool_blocked"])
        self.assertTrue(checks["execution_disabled"])
        self.assertTrue(checks["selection_disabled"])
        self.assertTrue(checks["permission_disabled"])

        tools = result["tools"]

        self.assertIn("knowledge_lookup", tools)
        self.assertIn("memory_store", tools)
        self.assertIn("memory_recall", tools)

        knowledge_tool = tools["knowledge_lookup"]

        self.assertEqual(
            knowledge_tool["capability"],
            "knowledge",
        )

        self.assertFalse(
            knowledge_tool["execution_enabled"]
        )

        memory_store = tools["memory_store"]

        self.assertEqual(
            memory_store["capability"],
            "memory",
        )

        self.assertFalse(
            memory_store["execution_enabled"]
        )

        memory_recall = tools["memory_recall"]

        self.assertEqual(
            memory_recall["capability"],
            "memory",
        )

        self.assertFalse(
            memory_recall["execution_enabled"]
        )

    def test_9d(self):
        result = get_tool_selection_regression()

        self.assertTrue(result["regression_passed"])
        self.assertEqual(result["integration_layer"], "9D")
        self.assertEqual(result["integration_status"], "READY")
        self.assertTrue(result["checks"]["layer_9d"])
        self.assertTrue(result["checks"]["status_ready"])
        self.assertTrue(result["checks"]["memory_store_selected"])
        self.assertTrue(result["checks"]["memory_recall_selected"])
        self.assertTrue(result["checks"]["knowledge_selected"])
        self.assertTrue(result["checks"]["unknown_no_tool_selected"])
        self.assertTrue(result["checks"]["selection_enabled"])
        self.assertTrue(result["checks"]["execution_disabled"])
        self.assertTrue(result["checks"]["permission_disabled"])

        self.assertFalse(result["execution_enabled"])
        self.assertFalse(result["permission_enabled"])

    def test_9e(self):
        result = get_action_policy_regression()

        self.assertTrue(result["regression_passed"])
        self.assertEqual(result["integration_layer"], "9E")
        self.assertEqual(result["integration_status"], "READY")

        checks = result["checks"]

        self.assertTrue(checks["layer_9e"])
        self.assertTrue(checks["status_ready"])
        self.assertTrue(checks["memory_tool_evaluated"])
        self.assertTrue(checks["knowledge_tool_evaluated"])
        self.assertTrue(checks["memory_requires_human_review"])
        self.assertTrue(checks["knowledge_requires_human_review"])
        self.assertTrue(checks["unknown_request_has_no_evaluations"])
        self.assertTrue(checks["execution_disabled"])
        self.assertTrue(checks["automatic_action_disabled"])
        self.assertTrue(checks["self_modification_disabled"])
        self.assertTrue(checks["decision_override_disabled"])

        self.assertFalse(result["execution_enabled"])
        self.assertFalse(result["automatic_action_allowed"])
        self.assertFalse(result["self_modification_allowed"])
        self.assertFalse(result["decision_override_allowed"])

    def test_9f(self):
        result = get_controlled_execution_regression()

        self.assertTrue(result["regression_passed"])
        self.assertEqual(result["integration_layer"], "9F")
        self.assertEqual(result["integration_status"], "READY")

        checks = result["checks"]

        self.assertTrue(checks["layer_9f"])
        self.assertTrue(checks["status_ready"])
        self.assertTrue(checks["registered_tool_reaches_gate"])
        self.assertTrue(checks["registered_tool_not_executed"])
        self.assertTrue(checks["unknown_tool_blocked"])
        self.assertTrue(checks["human_review_not_executed"])
        self.assertTrue(checks["execution_disabled"])
        self.assertTrue(checks["automatic_action_disabled"])
        self.assertTrue(checks["self_modification_disabled"])
        self.assertTrue(checks["decision_override_disabled"])
        self.assertTrue(checks["human_review_preserved"])

        self.assertFalse(result["execution_enabled"])
        self.assertFalse(result["automatic_action_allowed"])
        self.assertFalse(result["self_modification_allowed"])
        self.assertFalse(result["decision_override_allowed"])

    def test_9g(self):
        result = get_action_results_regression()

        self.assertTrue(result["regression_passed"])
        self.assertEqual(result["integration_layer"], "9G")
        self.assertEqual(result["integration_status"], "READY")

        checks = result["checks"]

        self.assertTrue(checks["layer_9g"])
        self.assertTrue(checks["status_ready"])
        self.assertTrue(checks["human_review_normalized"])
        self.assertTrue(checks["human_review_required"])
        self.assertTrue(checks["human_review_not_success"])
        self.assertTrue(checks["blocked_normalized"])
        self.assertTrue(checks["blocked_not_success"])
        self.assertTrue(checks["tool_identity_preserved"])
        self.assertTrue(checks["unknown_tool_identity_preserved"])
        self.assertTrue(checks["execution_disabled"])
        self.assertTrue(checks["automatic_action_disabled"])
        self.assertTrue(checks["self_modification_disabled"])
        self.assertTrue(checks["decision_override_disabled"])

        self.assertFalse(result["execution_enabled"])
        self.assertFalse(result["automatic_action_allowed"])
        self.assertFalse(result["self_modification_allowed"])
        self.assertFalse(result["decision_override_allowed"])

        self.assertEqual(
            result["human_review_result"]["result_status"],
            "HUMAN_REVIEW",
        )

        self.assertEqual(
            result["blocked_result"]["result_status"],
            "BLOCKED",
        )

    def test_9h(self):
        result = get_action_audit_regression()

        self.assertTrue(result["regression_passed"])
        self.assertEqual(result["integration_layer"], "9H")
        self.assertEqual(result["integration_status"], "READY")

        checks = result["checks"]

        self.assertTrue(checks["layer_9h"])
        self.assertTrue(checks["status_ready"])
        self.assertTrue(checks["memory_audit_created"])
        self.assertTrue(checks["memory_tool_preserved"])
        self.assertTrue(checks["memory_result_preserved"])
        self.assertTrue(checks["memory_review_preserved"])
        self.assertTrue(checks["memory_not_executed"])
        self.assertTrue(checks["unknown_audit_created"])
        self.assertTrue(checks["unknown_tool_preserved"])
        self.assertTrue(checks["unknown_result_preserved"])
        self.assertTrue(checks["records_available"])
        self.assertTrue(checks["memory_record_retrievable"])
        self.assertTrue(checks["unknown_record_retrievable"])
        self.assertTrue(checks["audit_available"])
        self.assertTrue(checks["execution_disabled"])
        self.assertTrue(checks["automatic_action_disabled"])
        self.assertTrue(checks["self_modification_disabled"])
        self.assertTrue(checks["decision_override_disabled"])

        self.assertFalse(result["execution_enabled"])
        self.assertFalse(result["automatic_action_allowed"])
        self.assertFalse(result["self_modification_allowed"])
        self.assertFalse(result["decision_override_allowed"])

        self.assertEqual(
            result["memory_record"]["audit_record"]["tool_id"],
            "memory_store",
        )

        self.assertEqual(
            result["memory_record"]["audit_record"]["result_status"],
            "HUMAN_REVIEW",
        )

        self.assertEqual(
            result["unknown_record"]["audit_record"]["tool_id"],
            "unknown_tool",
        )

        self.assertEqual(
            result["unknown_record"]["audit_record"]["result_status"],
            "BLOCKED",
        )

    def test_9i(self):
        result = get_capability_integration_regression()

        self.assertTrue(result["regression_passed"])
        self.assertEqual(result["integration_layer"], "9I")
        self.assertEqual(result["integration_status"], "READY")

        checks = result["checks"]

        self.assertTrue(checks["layer_9i"])
        self.assertTrue(checks["status_ready"])
        self.assertTrue(checks["integration_enabled"])

        self.assertTrue(
            checks["memory_capability_discovered"]
        )
        self.assertTrue(
            checks["memory_tool_selected"]
        )
        self.assertTrue(
            checks["memory_policy_evaluated"]
        )
        self.assertTrue(
            checks["memory_action_result_created"]
        )
        self.assertTrue(
            checks["memory_result_requires_review"]
        )
        self.assertTrue(
            checks["memory_audit_created"]
        )

        self.assertTrue(
            checks["knowledge_capability_discovered"]
        )
        self.assertTrue(
            checks["knowledge_tool_selected"]
        )
        self.assertTrue(
            checks["knowledge_policy_evaluated"]
        )
        self.assertTrue(
            checks["knowledge_action_result_created"]
        )
        self.assertTrue(
            checks["knowledge_result_requires_review"]
        )
        self.assertTrue(
            checks["knowledge_audit_created"]
        )

        self.assertTrue(
            checks["unknown_capability_not_invented"]
        )
        self.assertTrue(
            checks["unknown_no_tool_selected"]
        )
        self.assertTrue(
            checks["unknown_no_action_result"]
        )
        self.assertTrue(
            checks["unknown_no_audit"]
        )

        self.assertTrue(
            checks["execution_disabled"]
        )
        self.assertTrue(
            checks["automatic_action_disabled"]
        )
        self.assertTrue(
            checks["self_modification_disabled"]
        )
        self.assertTrue(
            checks["decision_override_disabled"]
        )

        self.assertFalse(
            result["execution_enabled"]
        )
        self.assertFalse(
            result["automatic_action_allowed"]
        )
        self.assertFalse(
            result["self_modification_allowed"]
        )
        self.assertFalse(
            result["decision_override_allowed"]
        )

    def test_8a(self):
        result = get_adaptive_intelligence_regression()
        self.assertTrue(result["regression_passed"])

    def test_8b(self):
        result = get_adaptive_strategy_regression()
        self.assertTrue(result["regression_passed"])

    def test_8c(self):
        result = get_adaptive_orchestration_regression()
        self.assertTrue(result["regression_passed"])

    def test_8d(self):
        result = get_adaptive_decision_regression()
        self.assertTrue(result["regression_passed"])

    def test_8e(self):
        result = get_adaptive_response_regression()
        self.assertTrue(result["regression_passed"])

    def test_8f(self):
        result = get_adaptive_learning_regression()
        self.assertTrue(result["regression_passed"])

    def test_8g(self):
        result = get_adaptive_experience_regression()
        self.assertTrue(result["regression_passed"])

    def test_8h(self):
        result = get_adaptive_integration_regression()
        self.assertTrue(result["regression_passed"])

    def test_8j(self):
        result = get_adaptive_validation_regression()
        self.assertTrue(result["regression_passed"])

    def test_8k(self):
        result = get_adaptive_orchestration_regression()
        self.assertTrue(result["regression_passed"])

    def test_8l(self):
        result = get_adaptive_governance_regression()
        self.assertTrue(result["regression_passed"])

    def test_8m(self):
        result = get_adaptive_oversight_regression()
        self.assertTrue(result["regression_passed"])

    def test_8n(self):
        result = get_adaptive_accountability_regression()

        self.assertTrue(result["regression_passed"])
        self.assertEqual(result["integration_layer"], "8N")
        self.assertEqual(result["integration_status"], "READY")

        output = result["result"]

        self.assertEqual(output["accountability_layer"], "8N")
        self.assertEqual(output["accountability_status"], "READY")
        self.assertEqual(
            output["accountability_state"],
            "ACCOUNTABILITY_ADVISORY",
        )

        self.assertEqual(
            output["accountability"]["accountability_level"],
            "ADVISORY_ONLY",
        )

        self.assertTrue(
            output["accountability"]["human_review_required"]
        )

        self.assertTrue(
            output["accountability"]["audit_available"]
        )

        self.assertFalse(output["execution_allowed"])
        self.assertFalse(output["automatic_action_allowed"])
        self.assertFalse(output["self_modification_allowed"])
        self.assertFalse(output["decision_override_allowed"])

        self.assertFalse(
            output["accountability"]["execution_allowed"]
        )

        self.assertFalse(
            output["accountability"]["automatic_action_allowed"]
        )

        self.assertFalse(
            output["accountability"]["self_modification_allowed"]
        )

        self.assertFalse(
            output["accountability"]["decision_override_allowed"]
        )


if __name__ == "__main__":
    unittest.main()
