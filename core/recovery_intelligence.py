"""
HOPE Recovery Intelligence Engine

Analyzes persistent HOPE recovery history and produces:

- Recovery statistics
- Problem-module detection
- Module reliability
- Recovery pattern detection
- Recovery insights
- Recovery recommendations
- Intelligent recommendations
- Recovery trend analysis
- Module recovery trends
- Trend summaries
- Trend recommendations
- Predictive failure intelligence
- Module risk scores
- Failure predictions
- Predictive summaries
- Predictive recommendations
- Recovery intelligence reports
"""

from collections import Counter
from datetime import datetime, timedelta

from core.recovery_log import (
    get_recovery_history,
)


# ============================================================
# LOAD RECOVERY DATA
# ============================================================

def _get_history():
    """
    Load persistent recovery history.

    Returns:
        list: Recovery events.
    """

    history = get_recovery_history()

    if not isinstance(history, list):
        return []

    return history


# ============================================================
# RECOVERY STATISTICS
# ============================================================

def get_recovery_statistics():
    """
    Calculate recovery statistics.

    Returns:
        dict: Recovery statistics.
    """

    history = _get_history()

    total = len(history)

    successful = 0
    failed = 0

    for event in history:

        result = str(
            event.get("result", "")
        ).upper().strip()

        if result == "SUCCESS":

            successful += 1

        elif result in [
            "FAILED",
            "FAILURE",
            "ERROR",
        ]:

            failed += 1

    if total > 0:

        success_rate = (
            successful / total
        ) * 100

    else:

        success_rate = 0.0

    return {
        "total": total,
        "successful": successful,
        "failed": failed,
        "success_rate": round(
            success_rate,
            2
        ),
    }


# ============================================================
# PROBLEM MODULES
# ============================================================

def get_problem_modules():
    """
    Identify modules that have appeared in recovery events.

    Returns:
        list: Module information ordered by frequency.
    """

    history = _get_history()

    if not history:
        return []

    module_counter = Counter()

    for event in history:

        module = event.get(
            "module",
            "Unknown Module"
        )

        module_counter[module] += 1

    problems = []

    for module, count in module_counter.most_common():

        problems.append({
            "module": module,
            "events": count,
        })

    return problems


# ============================================================
# MOST AFFECTED MODULE
# ============================================================

def get_most_affected_module():
    """
    Return the module with the most recovery events.

    Returns:
        dict or None: Most affected module.
    """

    problems = get_problem_modules()

    if not problems:
        return None

    return problems[0]


# ============================================================
# REPEATED FAILURE DETECTION
# ============================================================

def get_repeated_failures():
    """
    Identify modules that have required recovery more than once.

    Returns:
        list: Modules with repeated recovery events.
    """

    problems = get_problem_modules()

    return [
        problem
        for problem in problems
        if problem["events"] > 1
    ]


# ============================================================
# MODULE RELIABILITY
# ============================================================

def get_module_reliability():
    """
    Calculate recovery reliability for each affected module.

    Returns:
        list: Module reliability information.
    """

    history = _get_history()

    if not history:
        return []

    module_data = {}

    for event in history:

        module = event.get(
            "module",
            "Unknown Module"
        )

        result = str(
            event.get("result", "")
        ).upper().strip()

        if module not in module_data:

            module_data[module] = {
                "module": module,
                "events": 0,
                "successful": 0,
                "failed": 0,
            }

        module_data[module]["events"] += 1

        if result == "SUCCESS":

            module_data[module]["successful"] += 1

        elif result in [
            "FAILED",
            "FAILURE",
            "ERROR",
        ]:

            module_data[module]["failed"] += 1

    reliability = []

    for data in module_data.values():

        events = data["events"]
        successful = data["successful"]

        if events > 0:

            success_rate = (
                successful / events
            ) * 100

        else:

            success_rate = 0.0

        reliability.append({
            "module": data["module"],
            "events": events,
            "successful": data["successful"],
            "failed": data["failed"],
            "success_rate": round(
                success_rate,
                2
            ),
        })

    reliability.sort(
        key=lambda item: item["events"],
        reverse=True
    )

    return reliability


# ============================================================
# RECOVERY PATTERN DETECTION
# ============================================================

def detect_recovery_patterns():
    """
    Detect advanced recovery patterns.

    Pattern classifications:

        NORMAL
            Module has only one recovery event.

        REPEATED
            Module has more than one recovery event.

        HIGH_FREQUENCY
            Module has three or more recovery events.

        CRITICAL
            Module has repeated failed recovery attempts.

    Returns:
        list: Detected recovery patterns.
    """

    reliability = get_module_reliability()

    patterns = []

    for module in reliability:

        name = module["module"]
        events = module["events"]
        failed = module["failed"]
        success_rate = module["success_rate"]

        # ----------------------------------------------------
        # Critical
        # ----------------------------------------------------

        if failed >= 2:

            pattern = "CRITICAL"

            description = (
                f"{name} has experienced "
                f"{failed} failed recovery attempts."
            )

        # ----------------------------------------------------
        # High Frequency
        # ----------------------------------------------------

        elif events >= 3:

            pattern = "HIGH_FREQUENCY"

            description = (
                f"{name} has required recovery "
                f"{events} times."
            )

        # ----------------------------------------------------
        # Repeated
        # ----------------------------------------------------

        elif events > 1:

            pattern = "REPEATED"

            description = (
                f"{name} has experienced "
                f"repeated recovery events."
            )

        # ----------------------------------------------------
        # Normal
        # ----------------------------------------------------

        else:

            pattern = "NORMAL"

            description = (
                f"{name} has required recovery "
                f"once."
            )

        patterns.append({
            "module": name,
            "pattern": pattern,
            "events": events,
            "successful": module["successful"],
            "failed": failed,
            "success_rate": success_rate,
            "description": description,
        })

    return patterns


# ============================================================
# PATTERN SUMMARY
# ============================================================

def get_pattern_summary():
    """
    Generate a high-level summary of detected
    recovery patterns.

    Returns:
        dict: Recovery pattern summary.
    """

    patterns = detect_recovery_patterns()

    if not patterns:

        return {
            "total_modules": 0,
            "normal": 0,
            "repeated": 0,
            "high_frequency": 0,
            "critical": 0,
            "overall_pattern": "NO_DATA",
        }

    normal = 0
    repeated = 0
    high_frequency = 0
    critical = 0

    for pattern in patterns:

        state = pattern["pattern"]

        if state == "NORMAL":

            normal += 1

        elif state == "REPEATED":

            repeated += 1

        elif state == "HIGH_FREQUENCY":

            high_frequency += 1

        elif state == "CRITICAL":

            critical += 1

    if critical > 0:

        overall = "CRITICAL"

    elif high_frequency > 0:

        overall = "HIGH_FREQUENCY"

    elif repeated > 0:

        overall = "REPEATED"

    else:

        overall = "NORMAL"

    return {
        "total_modules": len(patterns),
        "normal": normal,
        "repeated": repeated,
        "high_frequency": high_frequency,
        "critical": critical,
        "overall_pattern": overall,
    }


# ============================================================
# RECOVERY INSIGHTS
# ============================================================

def get_recovery_insights():
    """
    Analyze recovery history and generate
    intelligence insights.

    Returns:
        list: Recovery insights.
    """

    statistics = get_recovery_statistics()
    problems = get_problem_modules()
    repeated = get_repeated_failures()
    patterns = detect_recovery_patterns()

    insights = []

    total = statistics["total"]
    successful = statistics["successful"]
    failed = statistics["failed"]
    success_rate = statistics["success_rate"]

    if total == 0:

        insights.append(
            "No recovery events have been recorded yet."
        )

        return insights

    if success_rate == 100:

        insights.append(
            "All recorded recovery attempts "
            "were successful."
        )

    elif success_rate >= 80:

        insights.append(
            "HOPE has a high recovery success rate."
        )

    elif success_rate >= 50:

        insights.append(
            "HOPE has a moderate recovery success rate."
        )

    else:

        insights.append(
            "HOPE has a low recovery success rate."
        )

    if failed > 0:

        insights.append(
            f"{failed} recovery event(s) "
            "failed to restore the affected module."
        )

    if problems:

        most_affected = problems[0]

        insights.append(
            f"{most_affected['module']} is the most "
            f"frequently affected module with "
            f"{most_affected['events']} recovery event(s)."
        )

    if repeated:

        for problem in repeated:

            insights.append(
                f"{problem['module']} has experienced "
                f"repeated recovery events "
                f"({problem['events']} times)."
            )

    for pattern in patterns:

        if pattern["pattern"] == "HIGH_FREQUENCY":

            insights.append(
                f"⚠️ {pattern['module']} shows a "
                f"high-frequency recovery pattern "
                f"({pattern['events']} events)."
            )

        elif pattern["pattern"] == "CRITICAL":

            insights.append(
                f"❌ {pattern['module']} shows a "
                f"critical recovery pattern with "
                f"{pattern['failed']} failed recovery attempts."
            )

    if successful > 0 and failed == 0:

        insights.append(
            "Every recorded recovery attempt "
            "has restored the affected module successfully."
        )

    return insights


# ============================================================
# RECOVERY RECOMMENDATION
# ============================================================

def get_recovery_recommendation():
    """
    Generate a recommendation based on recovery history
    and detected recovery patterns.

    Returns:
        str: Recovery recommendation.
    """

    statistics = get_recovery_statistics()
    repeated = get_repeated_failures()
    pattern_summary = get_pattern_summary()

    total = statistics["total"]
    failed = statistics["failed"]
    success_rate = statistics["success_rate"]

    if total == 0:

        return (
            "No recovery history is available. "
            "No recommendation can be generated yet."
        )

    if pattern_summary["critical"] > 0:

        return (
            "Critical recovery patterns detected. "
            "Investigate repeated failed recoveries "
            "immediately."
        )

    if pattern_summary["high_frequency"] > 0:

        return (
            "One or more modules show high-frequency "
            "recovery events. Investigate the underlying "
            "cause before the problem becomes critical."
        )

    if failed > 0:

        return (
            "Investigate failed recovery events "
            "and the affected modules."
        )

    if repeated:

        module = repeated[0]["module"]

        return (
            f"{module} has experienced repeated failures. "
            "Investigate the underlying cause."
        )

    if success_rate == 100:

        return (
            "No immediate action required. "
            "All recorded recovery attempts were successful."
        )

    if success_rate >= 80:

        return (
            "Recovery performance is healthy. "
            "Continue monitoring affected modules."
        )

    return (
        "Monitor recovery events and investigate "
        "recurring module problems."
    )


# ============================================================
# INTELLIGENT RECOVERY RECOMMENDATION
# ============================================================

def get_intelligent_recommendation():
    """
    Generate an intelligent recovery recommendation
    based on detected recovery patterns.

    Returns:
        dict: Recommendation information.
    """

    summary = get_pattern_summary()
    patterns = detect_recovery_patterns()

    overall = summary.get(
        "overall_pattern",
        "NO_DATA"
    )

    # --------------------------------------------------------
    # No recovery data
    # --------------------------------------------------------

    if overall == "NO_DATA":

        return {
            "level": "INFO",
            "pattern": "NO_DATA",
            "action": "MONITOR",
            "modules": [],
            "message": (
                "No recovery history is available yet. "
                "Continue monitoring HOPE system health."
            ),
        }

    # --------------------------------------------------------
    # Critical
    # --------------------------------------------------------

    if overall == "CRITICAL":

        critical_modules = [
            pattern["module"]
            for pattern in patterns
            if pattern["pattern"] == "CRITICAL"
        ]

        return {
            "level": "CRITICAL",
            "pattern": "CRITICAL",
            "action": "INVESTIGATE_IMMEDIATELY",
            "modules": critical_modules,
            "message": (
                "Critical recovery patterns detected. "
                "Investigate the affected modules immediately."
            ),
        }

    # --------------------------------------------------------
    # High Frequency
    # --------------------------------------------------------

    if overall == "HIGH_FREQUENCY":

        affected_modules = [
            pattern["module"]
            for pattern in patterns
            if pattern["pattern"] == "HIGH_FREQUENCY"
        ]

        return {
            "level": "WARNING",
            "pattern": "HIGH_FREQUENCY",
            "action": "INVESTIGATE",
            "modules": affected_modules,
            "message": (
                "One or more modules are experiencing "
                "frequent recovery events. Investigate "
                "the underlying cause."
            ),
        }

    # --------------------------------------------------------
    # Repeated
    # --------------------------------------------------------

    if overall == "REPEATED":

        affected_modules = [
            pattern["module"]
            for pattern in patterns
            if pattern["pattern"] == "REPEATED"
        ]

        return {
            "level": "NOTICE",
            "pattern": "REPEATED",
            "action": "MONITOR",
            "modules": affected_modules,
            "message": (
                "Repeated recovery events have been detected. "
                "Continue monitoring the affected modules."
            ),
        }

    # --------------------------------------------------------
    # Normal
    # --------------------------------------------------------

    return {
        "level": "GOOD",
        "pattern": "NORMAL",
        "action": "NO_ACTION",
        "modules": [],
        "message": (
            "No immediate action required. "
            "Recovery activity is currently normal."
        ),
    }


# ============================================================
# RECOVERY TREND ANALYSIS
# ============================================================

def _parse_recovery_time(value):
    """
    Convert a recovery event timestamp into datetime.

    Expected format:
        DD-MM-YYYY HH:MM:SS AM/PM

    Returns:
        datetime or None
    """

    if not value:
        return None

    try:

        return datetime.strptime(
            value,
            "%d-%m-%Y %I:%M:%S %p"
        )

    except (TypeError, ValueError):

        return None


# ============================================================
# GET RECOVERY TREND
# ============================================================

def get_recovery_trend():
    """
    Analyze overall recovery activity over time.

    Compares the most recent 7-day period with
    the previous 7-day period.

    Returns:
        dict: Overall recovery trend.
    """

    history = _get_history()

    if not history:

        return {
            "trend": "INSUFFICIENT_DATA",
            "recent_events": 0,
            "previous_events": 0,
            "total_events": 0,
            "message": (
                "No recovery history is available yet."
            ),
        }

    dated_events = []

    for event in history:

        timestamp = _parse_recovery_time(
            event.get("time")
        )

        if timestamp is not None:

            dated_events.append({
                "event": event,
                "time": timestamp,
            })

    if len(dated_events) < 2:

        return {
            "trend": "INSUFFICIENT_DATA",
            "recent_events": len(dated_events),
            "previous_events": 0,
            "total_events": len(history),
            "message": (
                "More recovery history is required "
                "for reliable trend analysis."
            ),
        }

    dated_events.sort(
        key=lambda item: item["time"]
    )

    latest_time = dated_events[-1]["time"]

    recent_start = (
        latest_time - timedelta(days=7)
    )

    previous_start = (
        latest_time - timedelta(days=14)
    )

    recent_events = 0
    previous_events = 0

    for item in dated_events:

        event_time = item["time"]

        if event_time >= recent_start:

            recent_events += 1

        elif (
            event_time >= previous_start
            and event_time < recent_start
        ):

            previous_events += 1

    if recent_events > previous_events:

        trend = "INCREASING"

        message = (
            "Recovery activity is increasing "
            "compared with the previous period."
        )

    elif recent_events < previous_events:

        trend = "DECREASING"

        message = (
            "Recovery activity is decreasing "
            "compared with the previous period."
        )

    else:

        trend = "STABLE"

        message = (
            "Recovery activity is stable "
            "compared with the previous period."
        )

    return {
        "trend": trend,
        "recent_events": recent_events,
        "previous_events": previous_events,
        "total_events": len(history),
        "message": message,
    }


# ============================================================
# MODULE RECOVERY TRENDS
# ============================================================

def get_module_recovery_trends():
    """
    Analyze recovery trends for individual modules.

    Returns:
        list: Module recovery trend information.
    """

    history = _get_history()

    if not history:
        return []

    module_events = {}

    for event in history:

        module = event.get(
            "module",
            "Unknown Module"
        )

        timestamp = _parse_recovery_time(
            event.get("time")
        )

        if timestamp is None:
            continue

        if module not in module_events:

            module_events[module] = []

        module_events[module].append(
            timestamp
        )

    results = []

    for module, timestamps in module_events.items():

        timestamps.sort()

        if len(timestamps) < 2:

            results.append({
                "module": module,
                "trend": "INSUFFICIENT_DATA",
                "recent_events": len(timestamps),
                "previous_events": 0,
                "total_events": len(timestamps),
            })

            continue

        latest_time = timestamps[-1]

        recent_start = (
            latest_time - timedelta(days=7)
        )

        previous_start = (
            latest_time - timedelta(days=14)
        )

        recent_events = sum(
            1
            for timestamp in timestamps
            if timestamp >= recent_start
        )

        previous_events = sum(
            1
            for timestamp in timestamps
            if (
                timestamp >= previous_start
                and timestamp < recent_start
            )
        )

        if recent_events > previous_events:

            trend = "INCREASING"

        elif recent_events < previous_events:

            trend = "DECREASING"

        else:

            trend = "STABLE"

        results.append({
            "module": module,
            "trend": trend,
            "recent_events": recent_events,
            "previous_events": previous_events,
            "total_events": len(timestamps),
        })

    results.sort(
        key=lambda item: item["total_events"],
        reverse=True
    )

    return results


# ============================================================
# TREND SUMMARY
# ============================================================

def get_trend_summary():
    """
    Generate a high-level recovery trend summary.

    Returns:
        dict: Trend summary.
    """

    overall = get_recovery_trend()

    module_trends = get_module_recovery_trends()

    increasing = 0
    decreasing = 0
    stable = 0
    insufficient = 0

    for item in module_trends:

        trend = item["trend"]

        if trend == "INCREASING":

            increasing += 1

        elif trend == "DECREASING":

            decreasing += 1

        elif trend == "STABLE":

            stable += 1

        elif trend == "INSUFFICIENT_DATA":

            insufficient += 1

    return {
        "overall_trend": overall["trend"],
        "recent_events": overall["recent_events"],
        "previous_events": overall["previous_events"],
        "total_events": overall["total_events"],
        "increasing": increasing,
        "decreasing": decreasing,
        "stable": stable,
        "insufficient_data": insufficient,
    }


# ============================================================
# TREND RECOMMENDATION
# ============================================================

def get_trend_recommendation():
    """
    Generate a recommendation based on recovery trends.

    Returns:
        str: Trend recommendation.
    """

    trend = get_recovery_trend()

    overall = trend["trend"]

    if overall == "INSUFFICIENT_DATA":

        return (
            "More recovery history is required before "
            "a reliable recovery trend can be determined."
        )

    if overall == "INCREASING":

        return (
            "Recovery activity is increasing. "
            "Investigate the affected modules and "
            "identify the underlying cause."
        )

    if overall == "DECREASING":

        return (
            "Recovery activity is decreasing. "
            "Continue monitoring system stability."
        )

    return (
        "Recovery activity is stable. "
        "Continue normal system monitoring."
    )


# ============================================================
# RECOVERY TREND REPORT
# ============================================================

def get_recovery_trend_report():
    """
    Generate a formatted HOPE Recovery Trend report.

    Returns:
        str: Formatted recovery trend report.
    """

    trend = get_recovery_trend()

    module_trends = get_module_recovery_trends()

    recommendation = get_trend_recommendation()

    lines = [
        "📈 HOPE Recovery Trend Analysis",
        "",
        f"Overall Trend    : {trend['trend']}",
        f"Recent Events    : {trend['recent_events']}",
        f"Previous Events  : {trend['previous_events']}",
        f"Total Events     : {trend['total_events']}",
        "",
    ]

    if trend["trend"] == "INSUFFICIENT_DATA":

        lines.append(
            "⚠️ Trend Status"
        )

        lines.append(
            "More recovery history is required "
            "for reliable trend analysis."
        )

        lines.append("")

    else:

        lines.append(
            "📊 Trend Observation"
        )

        lines.append(
            trend["message"]
        )

        lines.append("")

    if module_trends:

        lines.append(
            "🧩 Module Recovery Trends"
        )

        for module in module_trends:

            lines.append(
                f"• {module['module']} "
                f"→ {module['trend']}"
            )

            lines.append(
                f"  Recent   : "
                f"{module['recent_events']}"
            )

            lines.append(
                f"  Previous : "
                f"{module['previous_events']}"
            )

            lines.append(
                f"  Total    : "
                f"{module['total_events']}"
            )

            lines.append("")

    lines.extend([
        "💡 Trend Recommendation:",
        recommendation,
    ])

    return "\n".join(lines)


# ============================================================
# PREDICTIVE FAILURE INTELLIGENCE
# ============================================================

def get_module_risk_scores():
    """
    Calculate a predictive risk score for each module.

    Risk factors:

        - Recovery frequency
        - Failed recovery attempts
        - Success rate
        - Recovery pattern
        - Recovery trend

    Returns:
        list: Module risk information.
    """

    reliability = get_module_reliability()
    patterns = detect_recovery_patterns()
    trends = get_module_recovery_trends()

    pattern_map = {
        item["module"]: item
        for item in patterns
    }

    trend_map = {
        item["module"]: item
        for item in trends
    }

    results = []

    for module in reliability:

        name = module["module"]

        events = module["events"]
        failed = module["failed"]
        success_rate = module["success_rate"]

        pattern = pattern_map.get(
            name,
            {}
        ).get(
            "pattern",
            "NORMAL"
        )

        trend = trend_map.get(
            name,
            {}
        ).get(
            "trend",
            "INSUFFICIENT_DATA"
        )

        score = 0

        # ----------------------------------------------------
        # Recovery frequency
        # ----------------------------------------------------

        if events >= 5:

            score += 40

        elif events >= 3:

            score += 25

        elif events >= 2:

            score += 10

        # ----------------------------------------------------
        # Failed recovery attempts
        # ----------------------------------------------------

        if failed >= 3:

            score += 40

        elif failed >= 2:

            score += 30

        elif failed == 1:

            score += 15

        # ----------------------------------------------------
        # Success rate
        # ----------------------------------------------------

        if success_rate < 50:

            score += 25

        elif success_rate < 80:

            score += 15

        elif success_rate < 95:

            score += 5

        # ----------------------------------------------------
        # Recovery pattern
        # ----------------------------------------------------

        if pattern == "CRITICAL":

            score += 30

        elif pattern == "HIGH_FREQUENCY":

            score += 20

        elif pattern == "REPEATED":

            score += 10

        # ----------------------------------------------------
        # Recovery trend
        # ----------------------------------------------------

        if trend == "INCREASING":

            score += 15

        elif trend == "DECREASING":

            score -= 5

        # ----------------------------------------------------
        # Keep score between 0 and 100
        # ----------------------------------------------------

        score = max(
            0,
            min(score, 100)
        )

        # ----------------------------------------------------
        # Risk classification
        # ----------------------------------------------------

        if events == 1 and failed == 0:

            risk = "INSUFFICIENT_DATA"

        elif score >= 75:

            risk = "CRITICAL"

        elif score >= 50:

            risk = "HIGH"

        elif score >= 25:

            risk = "MEDIUM"

        else:

            risk = "LOW"

        results.append({
            "module": name,
            "risk_score": score,
            "risk": risk,
            "events": events,
            "failed": failed,
            "success_rate": success_rate,
            "pattern": pattern,
            "trend": trend,
        })

    results.sort(
        key=lambda item: item["risk_score"],
        reverse=True
    )

    return results


# ============================================================
# FAILURE PREDICTIONS
# ============================================================

def get_failure_predictions():
    """
    Generate predictive failure information.

    Returns:
        list: Failure predictions.
    """

    risk_scores = get_module_risk_scores()

    predictions = []

    for module in risk_scores:

        name = module["module"]
        risk = module["risk"]
        score = module["risk_score"]

        # ----------------------------------------------------
        # Insufficient data
        # ----------------------------------------------------

        if risk == "INSUFFICIENT_DATA":

            prediction = (
                f"{name} does not have enough historical "
                "data for reliable failure prediction."
            )

        # ----------------------------------------------------
        # Critical
        # ----------------------------------------------------

        elif risk == "CRITICAL":

            prediction = (
                f"{name} shows a critical risk of "
                "future recovery or failure events."
            )

        # ----------------------------------------------------
        # High
        # ----------------------------------------------------

        elif risk == "HIGH":

            prediction = (
                f"{name} shows elevated risk of "
                "future recovery events."
            )

        # ----------------------------------------------------
        # Medium
        # ----------------------------------------------------

        elif risk == "MEDIUM":

            prediction = (
                f"{name} shows moderate recovery risk. "
                "Continue monitoring."
            )

        # ----------------------------------------------------
        # Low
        # ----------------------------------------------------

        else:

            prediction = (
                f"{name} currently shows low recovery risk."
            )

        predictions.append({
            "module": name,
            "risk_score": score,
            "risk": risk,
            "prediction": prediction,
            "pattern": module["pattern"],
            "trend": module["trend"],
        })

    return predictions


# ============================================================
# PREDICTIVE SUMMARY
# ============================================================

def get_predictive_summary():
    """
    Generate a high-level predictive failure summary.

    Returns:
        dict: Predictive summary.
    """

    predictions = get_failure_predictions()

    if not predictions:

        return {
            "total_modules": 0,
            "low": 0,
            "medium": 0,
            "high": 0,
            "critical": 0,
            "insufficient_data": 0,
            "overall_risk": "NO_DATA",
        }

    low = 0
    medium = 0
    high = 0
    critical = 0
    insufficient = 0

    for prediction in predictions:

        risk = prediction["risk"]

        if risk == "LOW":

            low += 1

        elif risk == "MEDIUM":

            medium += 1

        elif risk == "HIGH":

            high += 1

        elif risk == "CRITICAL":

            critical += 1

        elif risk == "INSUFFICIENT_DATA":

            insufficient += 1

    if critical > 0:

        overall = "CRITICAL"

    elif high > 0:

        overall = "HIGH"

    elif medium > 0:

        overall = "MEDIUM"

    elif low > 0 and insufficient == 0:

        overall = "LOW"

    else:

        overall = "INSUFFICIENT_DATA"

    return {
        "total_modules": len(predictions),
        "low": low,
        "medium": medium,
        "high": high,
        "critical": critical,
        "insufficient_data": insufficient,
        "overall_risk": overall,
    }


# ============================================================
# PREDICTIVE RECOMMENDATION
# ============================================================

def get_predictive_recommendation():
    """
    Generate a recommendation based on predictive risk.

    Returns:
        str: Predictive recommendation.
    """

    summary = get_predictive_summary()

    overall = summary["overall_risk"]

    if overall == "NO_DATA":

        return (
            "No recovery history is available. "
            "Continue collecting recovery data."
        )

    if overall == "INSUFFICIENT_DATA":

        return (
            "There is not enough historical recovery data "
            "to make a reliable failure prediction. "
            "Continue monitoring HOPE."
        )

    if overall == "CRITICAL":

        return (
            "Critical failure risk detected. "
            "Investigate affected modules immediately."
        )

    if overall == "HIGH":

        return (
            "High recovery risk detected. "
            "Investigate affected modules and "
            "monitor them closely."
        )

    if overall == "MEDIUM":

        return (
            "Moderate recovery risk detected. "
            "Continue monitoring affected modules."
        )

    return (
        "Current predictive recovery risk is low. "
        "Continue normal monitoring."
    )


# ============================================================
# PREDICTIVE FAILURE REPORT
# ============================================================

def get_predictive_failure_report():
    """
    Generate a formatted predictive failure report.

    Returns:
        str: Predictive failure intelligence report.
    """

    summary = get_predictive_summary()

    predictions = get_failure_predictions()

    recommendation = get_predictive_recommendation()

    lines = [
        "🔮 HOPE Predictive Failure Intelligence",
        "",
        f"Overall Risk : {summary['overall_risk']}",
        f"Modules      : {summary['total_modules']}",
        "",
    ]

    # --------------------------------------------------------
    # Risk Distribution
    # --------------------------------------------------------

    lines.extend([
        "📊 Risk Distribution",
        f"  Low              : {summary['low']}",
        f"  Medium           : {summary['medium']}",
        f"  High             : {summary['high']}",
        f"  Critical         : {summary['critical']}",
        f"  Insufficient Data: "
        f"{summary['insufficient_data']}",
        "",
    ])

    # --------------------------------------------------------
    # Module Predictions
    # --------------------------------------------------------

    if predictions:

        lines.append(
            "🧠 Module Failure Predictions"
        )

        for prediction in predictions:

            lines.append(
                f"• {prediction['module']}"
            )

            lines.append(
                f"  Risk Score : "
                f"{prediction['risk_score']}/100"
            )

            lines.append(
                f"  Risk       : "
                f"{prediction['risk']}"
            )

            lines.append(
                f"  Pattern    : "
                f"{prediction['pattern']}"
            )

            lines.append(
                f"  Trend      : "
                f"{prediction['trend']}"
            )

            lines.append(
                f"  Prediction : "
                f"{prediction['prediction']}"
            )

            lines.append("")

    else:

        lines.append(
            "No module predictions are available."
        )

        lines.append("")

    # --------------------------------------------------------
    # Recommendation
    # --------------------------------------------------------

    lines.extend([
        "💡 Predictive Recommendation:",
        recommendation,
    ])

    return "\n".join(lines)


# ============================================================
# COMPLETE RECOVERY INTELLIGENCE REPORT
# ============================================================

def get_recovery_intelligence_report():
    """
    Generate the complete HOPE Recovery Intelligence report.

    Includes:

        - Statistics
        - Affected modules
        - Recovery patterns
        - Recovery insights
        - Intelligent recommendation
        - Predictive failure intelligence

    Returns:
        str: Formatted intelligence report.
    """

    statistics = get_recovery_statistics()

    problems = get_problem_modules()

    insights = get_recovery_insights()

    recommendation = get_recovery_recommendation()

    intelligent = get_intelligent_recommendation()

    pattern_summary = get_pattern_summary()

    patterns = detect_recovery_patterns()

    predictive_summary = get_predictive_summary()

    predictive_recommendation = (
        get_predictive_recommendation()
    )

    lines = [
        "🧠 HOPE Recovery Intelligence",
        "",
        f"Total Events     : {statistics['total']}",
        f"Successful       : {statistics['successful']}",
        f"Failed           : {statistics['failed']}",
        f"Success Rate     : "
        f"{statistics['success_rate']:.2f}%",
        "",
    ]

    # --------------------------------------------------------
    # Problem Modules
    # --------------------------------------------------------

    if problems:

        lines.append(
            "📊 Affected Modules"
        )

        for problem in problems:

            lines.append(
                f"  • {problem['module']} "
                f"— {problem['events']} event(s)"
            )

        lines.append("")

    # --------------------------------------------------------
    # Recovery Patterns
    # --------------------------------------------------------

    lines.append(
        "🧩 Recovery Patterns"
    )

    lines.append(
        f"Overall Pattern : "
        f"{pattern_summary['overall_pattern']}"
    )

    if patterns:

        for pattern in patterns:

            lines.append(
                f"  • {pattern['module']} "
                f"→ {pattern['pattern']}"
            )

            lines.append(
                f"    Events: {pattern['events']} | "
                f"Success: {pattern['successful']} | "
                f"Failed: {pattern['failed']} | "
                f"Rate: {pattern['success_rate']:.2f}%"
            )

            lines.append(
                f"    {pattern['description']}"
            )

    else:

        lines.append(
            "  • No recovery patterns detected."
        )

    lines.append("")

    # --------------------------------------------------------
    # Recovery Insights
    # --------------------------------------------------------

    if insights:

        lines.append(
            "🔎 Recovery Insights"
        )

        for insight in insights:

            lines.append(
                f"  • {insight}"
            )

        lines.append("")

    # --------------------------------------------------------
    # Existing Recommendation
    # --------------------------------------------------------

    lines.extend([
        "💡 Recommendation:",
        recommendation,
        "",
    ])

    # --------------------------------------------------------
    # Intelligent Recommendation
    # --------------------------------------------------------

    lines.extend([
        "🧠 Intelligent Recommendation:",
        f"  Level   : {intelligent['level']}",
        f"  Pattern : {intelligent['pattern']}",
        f"  Action  : {intelligent['action']}",
    ])

    if intelligent.get("modules"):

        lines.append(
            "  Modules : "
            + ", ".join(
                intelligent["modules"]
            )
        )

    lines.extend([
        "",
        f"  {intelligent['message']}",
        "",
    ])

    # --------------------------------------------------------
    # Predictive Failure Intelligence
    # --------------------------------------------------------

    lines.extend([
        "🔮 Predictive Failure Intelligence",
        "",
        f"Overall Risk : "
        f"{predictive_summary['overall_risk']}",
        f"Modules      : "
        f"{predictive_summary['total_modules']}",
        "",
        "📊 Risk Distribution",
        f"  Low              : "
        f"{predictive_summary['low']}",
        f"  Medium           : "
        f"{predictive_summary['medium']}",
        f"  High             : "
        f"{predictive_summary['high']}",
        f"  Critical         : "
        f"{predictive_summary['critical']}",
        f"  Insufficient Data: "
        f"{predictive_summary['insufficient_data']}",
        "",
        "💡 Predictive Recommendation:",
        predictive_recommendation,
    ])

    return "\n".join(lines)