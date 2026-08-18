"""
HOPE Predictive Intelligence Engine

Milestone 5 - Step 1C

This module extends the Recovery Intelligence layer by combining:

    - Current module health
    - Recovery history
    - Recovery patterns
    - Recovery trends
    - Module reliability

The purpose is to identify predictive signals and estimate
future system risk without pretending that insufficient data
is a reliable prediction.

This module does NOT replace recovery_intelligence.py.
It builds on top of it.
"""

from collections import Counter


# ============================================================
# EXISTING HOPE ENGINES
# ============================================================

from core.diagnostics import (
    check_modules,
    get_health,
)

from core.recovery_log import (
    get_recovery_history,
)

from core.recovery_intelligence import (
    get_recovery_statistics,
    get_problem_modules,
    detect_recovery_patterns,
    get_pattern_summary,
    get_module_reliability,
    get_recovery_trend,
    get_module_recovery_trends,
    get_trend_summary,
)


# ============================================================
# CONSTANTS
# ============================================================

MINIMUM_EVENTS_FOR_PREDICTION = 3

RISK_LOW = "LOW"
RISK_MEDIUM = "MEDIUM"
RISK_HIGH = "HIGH"
RISK_CRITICAL = "CRITICAL"
RISK_INSUFFICIENT = "INSUFFICIENT_DATA"

CONFIDENCE_LOW = "LOW"
CONFIDENCE_MEDIUM = "MEDIUM"
CONFIDENCE_HIGH = "HIGH"
CONFIDENCE_INSUFFICIENT = "INSUFFICIENT_DATA"


# ============================================================
# LOAD DATA
# ============================================================

def _get_history():
    """
    Load persistent recovery history safely.

    Returns:
        list: Recovery events.
    """

    try:
        history = get_recovery_history()

        if not isinstance(history, list):
            return []

        return history

    except Exception:
        return []


# ============================================================
# CURRENT MODULE HEALTH
# ============================================================

def _get_current_module_health():
    """
    Return the current health state of all HOPE modules.

    Returns:
        list: Module diagnostic information.
    """

    try:
        diagnostics = check_modules()

        if not isinstance(diagnostics, list):
            return []

        return diagnostics

    except Exception:
        return []


# ============================================================
# MODULE EVENT COUNTS
# ============================================================

def _get_module_event_counts():
    """
    Count recovery events for each module.

    Returns:
        dict: Module -> recovery event count.
    """

    history = _get_history()

    counts = Counter()

    for event in history:

        module = event.get(
            "module",
            "Unknown Module"
        )

        counts[module] += 1

    return dict(counts)


# ============================================================
# MODULE FAILURE COUNTS
# ============================================================

def _get_module_failure_counts():
    """
    Count failed recovery events for each module.

    Returns:
        dict: Module -> failed recovery count.
    """

    history = _get_history()

    failures = Counter()

    for event in history:

        module = event.get(
            "module",
            "Unknown Module"
        )

        result = str(
            event.get("result", "")
        ).upper().strip()

        if result in [
            "FAILED",
            "FAILURE",
            "ERROR",
        ]:
            failures[module] += 1

    return dict(failures)


# ============================================================
# RECOVERY SUCCESS RATES
# ============================================================

def _get_module_success_rates():
    """
    Calculate recovery success rate for each module.

    Returns:
        dict: Module -> success rate.
    """

    history = _get_history()

    totals = Counter()
    successful = Counter()

    for event in history:

        module = event.get(
            "module",
            "Unknown Module"
        )

        totals[module] += 1

        result = str(
            event.get("result", "")
        ).upper().strip()

        if result == "SUCCESS":
            successful[module] += 1

    rates = {}

    for module, total in totals.items():

        if total == 0:
            rates[module] = 0.0

        else:
            rates[module] = round(
                (
                    successful[module]
                    / total
                ) * 100,
                2
            )

    return rates


# ============================================================
# PREDICTIVE DATA SUFFICIENCY
# ============================================================

def _has_sufficient_history(
    total_events,
    module_events=None,
):
    """
    Determine whether enough historical data exists
    for a meaningful predictive assessment.

    Returns:
        bool
    """

    if total_events < MINIMUM_EVENTS_FOR_PREDICTION:
        return False

    if module_events is not None:

        if module_events < MINIMUM_EVENTS_FOR_PREDICTION:
            return False

    return True


# ============================================================
# PATTERN LOOKUP
# ============================================================

def _get_pattern_map():
    """
    Convert recovery pattern information into a lookup map.

    Returns:
        dict: Module -> pattern information.
    """

    try:
        patterns = detect_recovery_patterns()

    except Exception:
        patterns = []

    result = {}

    if not isinstance(patterns, list):
        return result

    for pattern in patterns:

        module = pattern.get(
            "module",
            "Unknown Module"
        )

        result[module] = pattern

    return result


# ============================================================
# TREND LOOKUP
# ============================================================

def _get_trend_map():
    """
    Convert module trend information into a lookup map.

    Returns:
        dict: Module -> trend information.
    """

    try:
        trends = get_module_recovery_trends()

    except Exception:
        trends = []

    result = {}

    if not isinstance(trends, list):
        return result

    for trend in trends:

        module = trend.get(
            "module",
            "Unknown Module"
        )

        result[module] = trend

    return result


# ============================================================
# CURRENT HEALTH LOOKUP
# ============================================================

def _get_health_map():
    """
    Convert diagnostics into a module health lookup.

    Returns:
        dict: Module -> diagnostic information.
    """

    diagnostics = _get_current_module_health()

    result = {}

    for module in diagnostics:

        name = module.get(
            "name",
            "Unknown Module"
        )

        result[name] = module

    return result


# ============================================================
# PREDICTIVE SIGNALS
# ============================================================

def get_predictive_signals():
    """
    Collect the raw signals used by HOPE Predictive Intelligence.

    Returns:
        dict: Predictive signal information.
    """

    statistics = get_recovery_statistics()

    history = _get_history()

    module_counts = _get_module_event_counts()
    failure_counts = _get_module_failure_counts()
    success_rates = _get_module_success_rates()

    patterns = _get_pattern_map()
    trends = _get_trend_map()
    health = _get_health_map()

    try:
        overall_trend = get_recovery_trend()

    except Exception:
        overall_trend = {
            "trend": "INSUFFICIENT_DATA"
        }

    try:
        trend_summary = get_trend_summary()

    except Exception:
        trend_summary = {
            "overall_trend": "INSUFFICIENT_DATA",
            "recent_events": 0,
            "previous_events": 0,
            "total_events": 0,
        }

    return {
        "total_recovery_events": statistics.get(
            "total",
            len(history)
        ),
        "successful_recoveries": statistics.get(
            "successful",
            0
        ),
        "failed_recoveries": statistics.get(
            "failed",
            0
        ),
        "success_rate": statistics.get(
            "success_rate",
            0.0
        ),
        "module_event_counts": module_counts,
        "module_failure_counts": failure_counts,
        "module_success_rates": success_rates,
        "patterns": patterns,
        "trends": trends,
        "health": health,
        "overall_health": get_health(),
        "overall_trend": overall_trend.get(
            "trend",
            "INSUFFICIENT_DATA"
        ),
        "trend_summary": trend_summary,
    }


# ============================================================
# RISK SCORE COMPONENTS
# ============================================================

def _failure_risk_component(
    events,
    failures,
):
    """
    Calculate the failure component of risk.

    Maximum contribution: 40 points.
    """

    if events <= 0:
        return 0

    failure_rate = (
        failures / events
    ) * 100

    score = failure_rate * 0.40

    return min(
        40,
        round(score)
    )


def _frequency_risk_component(events):
    """
    Calculate recovery-frequency risk.

    Maximum contribution: 20 points.
    """

    if events <= 1:
        return 0

    if events == 2:
        return 5

    if events == 3:
        return 10

    if events <= 5:
        return 15

    return 20


def _pattern_risk_component(pattern):
    """
    Calculate risk contribution from recovery patterns.

    Maximum contribution: 20 points.
    """

    if pattern == "CRITICAL":
        return 20

    if pattern == "HIGH_FREQUENCY":
        return 15

    if pattern == "REPEATED":
        return 10

    if pattern == "NORMAL":
        return 0

    return 0


def _trend_risk_component(trend):
    """
    Calculate risk contribution from recovery trends.

    Maximum contribution: 20 points.
    """

    if trend == "INCREASING":
        return 20

    if trend == "STABLE":
        return 5

    if trend == "DECREASING":
        return 0

    return 0


def _health_risk_component(health):
    """
    Calculate risk contribution from current module health.

    Maximum contribution: 20 points.

    Note:
        This component is applied only after the historical
        data sufficiency check.
    """

    if health == "ERROR":
        return 20

    if health == "OFFLINE":
        return 20

    if health == "UNKNOWN":
        return 20

    if health == "OK":
        return 0

    return 10


# ============================================================
# RISK CLASSIFICATION
# ============================================================

# ============================================================
# RISK CLASSIFICATION
# ============================================================

def _classify_risk(score):
    """
    Convert numerical predictive risk score
    into a risk level.

    Step 3A thresholds:

        0–24   : LOW
        25–49  : MEDIUM
        50–74  : HIGH
        75–100 : CRITICAL

    Returns:
        str: Risk classification.
    """

    if score >= 75:
        return RISK_CRITICAL

    if score >= 50:
        return RISK_HIGH

    if score >= 25:
        return RISK_MEDIUM

    return RISK_LOW


# ============================================================
# CONFIDENCE CLASSIFICATION
# ============================================================

def _classify_confidence(
    events,
    total_events,
):
    """
    Estimate confidence based on available history.

    Returns:
        str: Confidence classification.
    """

    if (
        events < MINIMUM_EVENTS_FOR_PREDICTION
        or total_events < MINIMUM_EVENTS_FOR_PREDICTION
    ):
        return CONFIDENCE_INSUFFICIENT

    if events >= 10 and total_events >= 10:
        return CONFIDENCE_HIGH

    if events >= 5 and total_events >= 5:
        return CONFIDENCE_MEDIUM

    return CONFIDENCE_LOW


# ============================================================
# STEP 6B — PREDICTIVE DATA QUALITY
# ============================================================


def _classify_data_quality(events):
    """
    Classify historical data quality based on event count.

    Returns:
        str: Data quality classification.
    """

    if events <= 0:
        return "NO_DATA"

    if events == 1:
        return "VERY_LOW"

    if events <= 3:
        return "LOW"

    if events <= 5:
        return "MODERATE"

    if events <= 10:
        return "GOOD"

    return "HIGH"


def _calculate_data_quality_score(quality):
    """
    Convert data quality classification into a score.

    Returns:
        int: Data quality score from 0 to 100.
    """

    scores = {
        "NO_DATA": 0,
        "VERY_LOW": 20,
        "LOW": 40,
        "MODERATE": 60,
        "GOOD": 80,
        "HIGH": 100,
    }

    return scores.get(
        quality,
        0
    )


# ============================================================
# STEP 6B-4 — MODULE DATA QUALITY PROFILE
# ============================================================


def get_module_data_quality_profile():
    """
    Generate historical data-quality profiles for each module.

    This evaluates the amount and basic reliability of historical
    recovery data without changing the existing predictive risk
    calculations.

    Returns:
        list: Module data-quality information.
    """

    signals = get_predictive_signals()

    event_counts = signals.get(
        "module_event_counts",
        {}
    )

    failure_counts = signals.get(
        "module_failure_counts",
        {}
    )

    success_rates = signals.get(
        "module_success_rates",
        {}
    )

    health_map = signals.get(
        "health",
        {}
    )

    patterns = signals.get(
        "patterns",
        {}
    )

    trends = signals.get(
        "trends",
        {}
    )

    total_events = signals.get(
        "total_recovery_events",
        0
    )

    modules = set()

    modules.update(event_counts.keys())
    modules.update(failure_counts.keys())
    modules.update(success_rates.keys())
    modules.update(health_map.keys())
    modules.update(patterns.keys())
    modules.update(trends.keys())

    profiles = []

    for module in sorted(modules):

        events = event_counts.get(
            module,
            0
        )

        failures = failure_counts.get(
            module,
            0
        )

        success_rate = success_rates.get(
            module,
            0.0
        )

        quality = _classify_data_quality(
            events
        )

        quality_score = _calculate_data_quality_score(
            quality
        )

        confidence = _classify_confidence(
            events,
            total_events
        )

        reliable = (
            confidence != CONFIDENCE_INSUFFICIENT
        )

        profiles.append({
            "module": module,
            "events": events,
            "failed": failures,
            "success_rate": success_rate,
            "data_quality": quality,
            "data_quality_score": quality_score,
            "confidence": confidence,
            "reliable": reliable,
        })

    return profiles


# ============================================================
# PREDICTIVE SIGNAL CLASSIFICATION
# ============================================================

def _classify_recovery_frequency(events):
    """
    Classify recovery frequency for a module.

    Returns:
        str: Frequency classification.
    """

    if events <= 0:
        return "NONE"

    if events == 1:
        return "LOW"

    if events <= 3:
        return "MODERATE"

    if events <= 5:
        return "HIGH"

    return "VERY_HIGH"


# ============================================================
# FAILURE RATE SIGNAL
# ============================================================

def _classify_failure_rate(events, failures):
    """
    Classify the historical recovery failure rate.

    Returns:
        dict: Failure rate information.
    """

    if events <= 0:
        return {
            "failure_rate": 0.0,
            "signal": "NO_DATA",
        }

    failure_rate = (
        failures / events
    ) * 100

    if failure_rate == 0:
        signal = "LOW"

    elif failure_rate < 25:
        signal = "MODERATE"

    elif failure_rate < 50:
        signal = "HIGH"

    else:
        signal = "CRITICAL"

    return {
        "failure_rate": round(
            failure_rate,
            2
        ),
        "signal": signal,
    }


# ============================================================
# PATTERN SIGNAL
# ============================================================

def _classify_pattern_signal(pattern):
    """
    Convert recovery pattern into a predictive signal.
    """

    if pattern == "CRITICAL":
        return "CRITICAL"

    if pattern == "HIGH_FREQUENCY":
        return "WARNING"

    if pattern == "REPEATED":
        return "NOTICE"

    if pattern == "NORMAL":
        return "NEUTRAL"

    return "NO_DATA"


# ============================================================
# TREND SIGNAL
# ============================================================

def _classify_trend_signal(trend):
    """
    Convert recovery trend into a predictive signal.
    """

    if trend == "INCREASING":
        return "WARNING"

    if trend == "STABLE":
        return "NEUTRAL"

    if trend == "DECREASING":
        return "POSITIVE"

    return "NO_DATA"


# ============================================================
# HEALTH SIGNAL
# ============================================================

def _classify_health_signal(health):
    """
    Convert current module health into a predictive signal.
    """

    if health == "ERROR":
        return "CRITICAL"

    if health == "OFFLINE":
        return "CRITICAL"

    if health == "UNKNOWN":
        return "WARNING"

    if health == "OK":
        return "NORMAL"

    return "WARNING"


# ============================================================
# SIGNAL STRENGTH
# ============================================================

def _calculate_signal_strength(
    frequency_signal,
    failure_signal,
    pattern_signal,
    trend_signal,
    health_signal,
):
    """
    Calculate an overall predictive signal strength.

    Returns:
        str: Signal strength.
    """

    critical_signals = sum(
        1
        for signal in [
            failure_signal,
            pattern_signal,
            health_signal,
        ]
        if signal == "CRITICAL"
    )

    warning_signals = sum(
        1
        for signal in [
            pattern_signal,
            trend_signal,
            health_signal,
        ]
        if signal == "WARNING"
    )

    moderate_signals = sum(
        1
        for signal in [
            frequency_signal,
            failure_signal,
            pattern_signal,
            trend_signal,
        ]
        if signal in [
            "MODERATE",
            "NOTICE",
        ]
    )

    if critical_signals > 0:
        return "CRITICAL"

    if warning_signals >= 2:
        return "STRONG"

    if warning_signals == 1 or moderate_signals >= 2:
        return "MODERATE"

    return "LOW"


# ============================================================
# MODULE SIGNAL PROFILE
# ============================================================

def get_module_signal_profile(module):
    """
    Generate a detailed predictive signal profile
    for a specific module.

    Args:
        module (str): Module name.

    Returns:
        dict: Predictive signal profile.
    """

    signals = get_predictive_signals()

    events = signals[
        "module_event_counts"
    ].get(
        module,
        0
    )

    failures = signals[
        "module_failure_counts"
    ].get(
        module,
        0
    )

    success_rate = signals[
        "module_success_rates"
    ].get(
        module,
        0.0
    )

    pattern_info = signals[
        "patterns"
    ].get(
        module,
        {}
    )

    trend_info = signals[
        "trends"
    ].get(
        module,
        {}
    )

    health_info = signals[
        "health"
    ].get(
        module,
        {}
    )

    pattern = pattern_info.get(
        "pattern",
        "NO_DATA"
    )

    trend = trend_info.get(
        "trend",
        "INSUFFICIENT_DATA"
    )

    health = health_info.get(
        "health",
        "UNKNOWN"
    )

    frequency = _classify_recovery_frequency(
        events
    )

    failure = _classify_failure_rate(
        events,
        failures
    )

    pattern_signal = _classify_pattern_signal(
        pattern
    )

    trend_signal = _classify_trend_signal(
        trend
    )

    health_signal = _classify_health_signal(
        health
    )

    signal_strength = _calculate_signal_strength(
        frequency,
        failure["signal"],
        pattern_signal,
        trend_signal,
        health_signal,
    )

    confidence = _classify_confidence(
        events,
        signals["total_recovery_events"]
    )

    return {
        "module": module,
        "events": events,
        "failures": failures,
        "success_rate": success_rate,
        "frequency": frequency,
        "failure_rate": failure["failure_rate"],
        "failure_signal": failure["signal"],
        "pattern": pattern,
        "pattern_signal": pattern_signal,
        "trend": trend,
        "trend_signal": trend_signal,
        "health": health,
        "health_signal": health_signal,
        "signal_strength": signal_strength,
        "confidence": confidence,
    }


# ============================================================
# ALL MODULE SIGNAL PROFILES
# ============================================================

def get_predictive_signal_profiles():
    """
    Generate predictive signal profiles for all modules.

    Returns:
        list: Signal profiles.
    """

    signals = get_predictive_signals()

    modules = set()

    modules.update(
        signals["module_event_counts"].keys()
    )

    modules.update(
        signals["patterns"].keys()
    )

    modules.update(
        signals["trends"].keys()
    )

    modules.update(
        signals["health"].keys()
    )

    profiles = []

    for module in sorted(modules):

        profiles.append(
            get_module_signal_profile(module)
        )

    return profiles


# ============================================================
# STEP 3B — ENHANCED RISK SCORING COMPONENTS
# ============================================================


# ============================================================
# FAILURE RATE SCORE
# ============================================================

def _calculate_failure_rate_score(failure_rate):
    """
    Calculate risk points from historical failure rate.

    Maximum: 30 points.

    Returns:
        int: Failure-rate risk score.
    """

    if failure_rate <= 0:
        return 0

    if failure_rate < 25:
        return 10

    if failure_rate < 50:
        return 20

    return 30


# ============================================================
# RECOVERY FREQUENCY SCORE
# ============================================================

def _calculate_frequency_score(frequency):
    """
    Calculate risk points from recovery frequency.

    Maximum: 15 points.

    Returns:
        int: Recovery-frequency risk score.
    """

    if frequency == "NONE":
        return 0

    if frequency == "LOW":
        return 3

    if frequency == "MODERATE":
        return 7

    if frequency == "HIGH":
        return 11

    if frequency == "VERY_HIGH":
        return 15

    return 0


# ============================================================
# PATTERN SCORE
# ============================================================

def _calculate_pattern_score(pattern):
    """
    Calculate risk points from recovery pattern.

    Maximum: 15 points.

    Returns:
        int: Pattern risk score.
    """

    if pattern in [
        "NO_DATA",
        "NORMAL",
    ]:
        return 0

    if pattern == "REPEATED":
        return 7

    if pattern == "HIGH_FREQUENCY":
        return 11

    if pattern == "CRITICAL":
        return 15

    return 0


# ============================================================
# TREND SCORE
# ============================================================

def _calculate_trend_score(trend):
    """
    Calculate risk points from recovery trend.

    Maximum: 15 points.

    Returns:
        int: Trend risk score.
    """

    if trend in [
        "NO_DATA",
        "DECREASING",
    ]:
        return 0

    if trend == "STABLE":
        return 3

    if trend == "INCREASING":
        return 10

    return 0


# ============================================================
# HEALTH SCORE
# ============================================================

def _calculate_health_score(health):
    """
    Calculate risk points from current module health.

    Maximum: 15 points.

    Returns:
        int: Current-health risk score.
    """

    if health == "OK":
        return 0

    if health == "UNKNOWN":
        return 5

    if health in [
        "OFFLINE",
        "ERROR",
    ]:
        return 15

    return 5


# ============================================================
# SIGNAL STRENGTH SCORE
# ============================================================

def _calculate_signal_strength_score(signal_strength):
    """
    Calculate risk points from predictive signal strength.

    Maximum: 10 points.

    Returns:
        int: Signal-strength risk score.
    """

    if signal_strength == "LOW":
        return 0

    if signal_strength == "MODERATE":
        return 4

    if signal_strength == "STRONG":
        return 7

    if signal_strength == "CRITICAL":
        return 10

    return 0


# ============================================================
# RAW PREDICTIVE RISK SCORE
# ============================================================

def _calculate_raw_predictive_score(
    failure_rate,
    frequency,
    pattern,
    trend,
    health,
    signal_strength,
):
    """
    Calculate the raw predictive risk score
    before confidence adjustment.

    Maximum: 100 points.

    Returns:
        dict: Score breakdown and raw score.
    """

    failure_score = (
        _calculate_failure_rate_score(
            failure_rate
        )
    )

    frequency_score = (
        _calculate_frequency_score(
            frequency
        )
    )

    pattern_score = (
        _calculate_pattern_score(
            pattern
        )
    )

    trend_score = (
        _calculate_trend_score(
            trend
        )
    )

    health_score = (
        _calculate_health_score(
            health
        )
    )

    signal_score = (
        _calculate_signal_strength_score(
            signal_strength
        )
    )

    raw_score = (
        failure_score
        + frequency_score
        + pattern_score
        + trend_score
        + health_score
        + signal_score
    )

    raw_score = min(
        100,
        raw_score
    )

    return {
        "failure_score": failure_score,
        "frequency_score": frequency_score,
        "pattern_score": pattern_score,
        "trend_score": trend_score,
        "health_score": health_score,
        "signal_strength_score": signal_score,
        "raw_score": raw_score,
    }


# ============================================================
# STEP 3C — CONFIDENCE & EVIDENCE ADJUSTMENT
# ============================================================


# ============================================================
# CONFIDENCE ADJUSTMENT
# ============================================================

def _calculate_confidence_adjustment(confidence):
    """
    Determine the confidence multiplier used to adjust
    the raw predictive risk score.

    Returns:
        float: Confidence multiplier.
    """

    if confidence == "HIGH":
        return 1.00

    if confidence == "MEDIUM":
        return 0.90

    if confidence == "LOW":
        return 0.75

    return 0.00


# ============================================================
# CONFIDENCE-ADJUSTED PREDICTIVE SCORE
# ============================================================

def _calculate_confidence_adjusted_score(
    raw_score,
    confidence,
):
    """
    Apply confidence adjustment to a raw predictive score.

    Insufficient data produces no reliable predictive score.

    Returns:
        dict: Confidence-adjusted score information.
    """

    if confidence == "INSUFFICIENT_DATA":
        return {
            "raw_score": raw_score,
            "confidence": confidence,
            "adjustment": 0.00,
            "adjusted_score": 0,
            "reliable": False,
        }

    adjustment = _calculate_confidence_adjustment(
        confidence
    )

    adjusted_score = (
        raw_score * adjustment
    )

    adjusted_score = round(
        adjusted_score
    )

    adjusted_score = min(
        100,
        max(
            0,
            adjusted_score
        )
    )

    return {
        "raw_score": raw_score,
        "confidence": confidence,
        "adjustment": adjustment,
        "adjusted_score": adjusted_score,
        "reliable": True,
    }


# MODULE RISK SCORES
# ============================================================

def get_predictive_risk_scores():
    """
    Calculate enhanced predictive risk scores
    for all HOPE modules.

    Step 3D integrates:

        - Predictive signals
        - Recovery frequency
        - Failure rate
        - Recovery pattern
        - Recovery trend
        - Current module health
        - Signal strength
        - Confidence adjustment

    Returns:
        list: Enhanced module predictive risk information.
    """

    signals = get_predictive_signals()

    total_events = signals[
        "total_recovery_events"
    ]

    module_counts = signals[
        "module_event_counts"
    ]

    failure_counts = signals[
        "module_failure_counts"
    ]

    success_rates = signals[
        "module_success_rates"
    ]

    patterns = signals[
        "patterns"
    ]

    trends = signals[
        "trends"
    ]

    health = signals[
        "health"
    ]

    # --------------------------------------------------------
    # Generate Step 2 predictive signal profiles
    # --------------------------------------------------------

    signal_profiles = (
        get_predictive_signal_profiles()
    )

    profile_map = {
        profile["module"]: profile
        for profile in signal_profiles
    }

    # --------------------------------------------------------
    # Collect all known modules
    # --------------------------------------------------------

    modules = set()

    modules.update(
        module_counts.keys()
    )

    modules.update(
        patterns.keys()
    )

    modules.update(
        trends.keys()
    )

    modules.update(
        health.keys()
    )

    modules.update(
        profile_map.keys()
    )

    results = []

    # --------------------------------------------------------
    # Calculate enhanced risk for each module
    # --------------------------------------------------------

    for module in sorted(modules):

        events = module_counts.get(
            module,
            0
        )

        failures = failure_counts.get(
            module,
            0
        )

        success_rate = success_rates.get(
            module,
            0.0
        )

        pattern_info = patterns.get(
            module,
            {}
        )

        trend_info = trends.get(
            module,
            {}
        )

        health_info = health.get(
            module,
            {}
        )

        pattern = pattern_info.get(
            "pattern",
            "NO_DATA"
        )

        trend = trend_info.get(
            "trend",
            "INSUFFICIENT_DATA"
        )

        current_health = health_info.get(
            "health",
            "UNKNOWN"
        )

        # ----------------------------------------------------
        # Confidence
        # ----------------------------------------------------

        confidence = _classify_confidence(
            events,
            total_events
        )

        # ----------------------------------------------------
        # Insufficient historical data
        # ----------------------------------------------------

        if confidence == CONFIDENCE_INSUFFICIENT:

            results.append({
                "module": module,
                "risk_score": 0,
                "risk": RISK_INSUFFICIENT,
                "confidence": confidence,
                "events": events,
                "failed": failures,
                "success_rate": success_rate,
                "pattern": pattern,
                "trend": trend,
                "health": current_health,
                "raw_score": 0,
                "confidence_adjustment": 0.0,
                "signal_strength": "NO_DATA",
            })

            continue

        # ----------------------------------------------------
        # Retrieve predictive signal profile
        # ----------------------------------------------------

        profile = profile_map.get(
            module,
            {}
        )

        frequency = profile.get(
            "frequency",
            "NONE"
        )

        failure_rate = profile.get(
            "failure_rate",
            0.0
        )

        signal_strength = profile.get(
            "signal_strength",
            "LOW"
        )

        # ----------------------------------------------------
        # Calculate Step 3B raw score
        # ----------------------------------------------------

        raw_score_data = (
            _calculate_raw_predictive_score(
                failure_rate=failure_rate,
                frequency=frequency,
                pattern=pattern,
                trend=trend,
                health=current_health,
                signal_strength=signal_strength,
            )
        )

        raw_score = raw_score_data[
            "raw_score"
        ]

        # ----------------------------------------------------
        # Apply Step 3C confidence adjustment
        # ----------------------------------------------------

        adjusted_data = (
            _calculate_confidence_adjusted_score(
                raw_score,
                confidence,
            )
        )

        score = adjusted_data[
            "adjusted_score"
        ]

        # ----------------------------------------------------
        # Classify final risk
        # ----------------------------------------------------

        risk = _classify_risk(
            score
        )

        # ----------------------------------------------------
        # Store complete enhanced result
        # ----------------------------------------------------

        results.append({
            "module": module,

            "risk_score": score,

            "risk": risk,

            "confidence": confidence,

            "events": events,

            "failed": failures,

            "success_rate": success_rate,

            "pattern": pattern,

            "trend": trend,

            "health": current_health,

            # Step 3B information
            "frequency": frequency,

            "failure_rate": failure_rate,

            "signal_strength": signal_strength,

            "raw_score": raw_score,

            # Step 3C information
            "confidence_adjustment": (
                adjusted_data[
                    "adjustment"
                ]
            ),

            "reliable": (
                adjusted_data[
                    "reliable"
                ]
            ),

            # Detailed score breakdown
            "score_breakdown": {
                "failure_score": (
                    raw_score_data[
                        "failure_score"
                    ]
                ),

                "frequency_score": (
                    raw_score_data[
                        "frequency_score"
                    ]
                ),

                "pattern_score": (
                    raw_score_data[
                        "pattern_score"
                    ]
                ),

                "trend_score": (
                    raw_score_data[
                        "trend_score"
                    ]
                ),

                "health_score": (
                    raw_score_data[
                        "health_score"
                    ]
                ),

                "signal_strength_score": (
                    raw_score_data[
                        "signal_strength_score"
                    ]
                ),
            },
        })

    # --------------------------------------------------------
    # Highest-risk modules first
    # --------------------------------------------------------

    results.sort(
        key=lambda item: item[
            "risk_score"
        ],
        reverse=True
    )

    return results

# ============================================================
# STEP 4B — RISK ACTION DECISION
# ============================================================

def _determine_risk_action(
    risk,
    confidence,
):
    """
    Determine the recommended action based on
    predictive risk and confidence.

    Returns:
        dict: Risk decision information.
    """

    if risk == RISK_INSUFFICIENT:

        return {
            "action": "COLLECT_DATA",
            "priority": "LOW",
            "reason": (
                "Insufficient historical data "
                "for reliable risk assessment."
            ),
        }

    if risk == RISK_CRITICAL:

        return {
            "action": "INTERVENE",
            "priority": "CRITICAL",
            "reason": (
                "Critical predictive risk detected. "
                "Immediate intervention is recommended."
            ),
        }

    if risk == RISK_HIGH:

        return {
            "action": "INVESTIGATE",
            "priority": "HIGH",
            "reason": (
                "High predictive risk detected. "
                "Further investigation is recommended."
            ),
        }

    if risk == RISK_MEDIUM:

        return {
            "action": "MONITOR",
            "priority": "MEDIUM",
            "reason": (
                "Moderate predictive risk detected. "
                "Continued monitoring is recommended."
            ),
        }

    return {
        "action": "CONTINUE",
        "priority": "LOW",
        "reason": (
            "Predictive risk is currently low. "
            "Continue normal operation."
        ),
    }

# ============================================================
# STEP 4D — SYSTEM RISK ACTION DECISION
# ============================================================

def _determine_system_action(predictions):
    """
    Determine the overall system action from module predictions.

    Returns:
        dict: System-level action decision.
    """

    if not predictions:
        return {
            "action": "COLLECT_DATA",
            "priority": "LOW",
            "reason": (
                "No predictive module data is available yet."
            ),
        }

    critical = any(
        item.get("risk") == RISK_CRITICAL
        for item in predictions
    )

    high = any(
        item.get("risk") == RISK_HIGH
        for item in predictions
    )

    medium = any(
        item.get("risk") == RISK_MEDIUM
        for item in predictions
    )

    usable = [
        item
        for item in predictions
        if item.get("risk") != RISK_INSUFFICIENT
    ]

    if critical:
        return {
            "action": "INTERVENE",
            "priority": "CRITICAL",
            "reason": (
                "Critical predictive risk detected in one or "
                "more modules. Immediate system intervention "
                "is recommended."
            ),
        }

    if high:
        return {
            "action": "INVESTIGATE",
            "priority": "HIGH",
            "reason": (
                "High predictive risk detected in one or "
                "more modules. System investigation is "
                "recommended."
            ),
        }

    if medium:
        return {
            "action": "MONITOR",
            "priority": "MEDIUM",
            "reason": (
                "Moderate predictive risk detected. "
                "Continued system monitoring is recommended."
            ),
        }

    if not usable:
        return {
            "action": "COLLECT_DATA",
            "priority": "LOW",
            "reason": (
                "Insufficient historical data for a reliable "
                "system risk assessment."
            ),
        }

    return {
        "action": "CONTINUE",
        "priority": "LOW",
        "reason": (
            "System predictive risk is currently low. "
            "Continue normal operation."
        ),
    }


# ============================================================
# STEP 6C-2 — PREDICTIVE EXPLANATION INTELLIGENCE
# ============================================================


def _get_predictive_explanation(item):
    """
    Build a human-readable explanation for an existing
    predictive module assessment.

    This function interprets existing prediction data only.
    It does not calculate or modify risk, confidence, score,
    data quality, action, or priority.

    Args:
        item (dict): Existing module prediction.

    Returns:
        dict: Structured predictive explanation.
    """

    module = item.get(
        "module",
        "Unknown Module"
    )

    risk = item.get(
        "risk",
        RISK_INSUFFICIENT
    )

    risk_score = item.get(
        "risk_score",
        0
    )

    confidence = item.get(
        "confidence",
        CONFIDENCE_INSUFFICIENT
    )

    pattern = item.get(
        "pattern",
        "NO_DATA"
    )

    trend = item.get(
        "trend",
        "INSUFFICIENT_DATA"
    )

    action = item.get(
        "action",
        "COLLECT_DATA"
    )

    priority = item.get(
        "priority",
        "LOW"
    )

    data_quality = item.get(
        "data_quality",
        "NO_DATA"
    )

    data_quality_score = item.get(
        "data_quality_score",
        0
    )

    reliable = item.get(
        "data_quality_reliable",
        False
    )

    events = item.get(
        "events",
        0
    )

    failed = item.get(
        "failed",
        0
    )

    success_rate = item.get(
        "success_rate",
        0.0
    )

    signal_strength = item.get(
        "signal_strength",
        "NO_DATA"
    )

    evidence = []

    if events > 0:
        evidence.append(
            f"{events} historical events"
        )

        evidence.append(
            f"{failed} failures"
        )

        evidence.append(
            f"{success_rate}% success rate"
        )

    if pattern != "NO_DATA":
        evidence.append(
            f"{pattern} pattern"
        )

    if trend != "INSUFFICIENT_DATA":
        evidence.append(
            f"{trend} trend"
        )

    if signal_strength != "NO_DATA":
        evidence.append(
            f"{signal_strength} signal strength"
        )

    if risk == RISK_CRITICAL:

        explanation = (
            f"Critical predictive risk is present for "
            f"{module}. Immediate intervention is "
            f"recommended."
        )

    elif risk == RISK_HIGH:

        explanation = (
            f"High predictive risk is present for "
            f"{module}. System investigation is "
            f"recommended."
        )

    elif risk == RISK_MEDIUM:

        if confidence == CONFIDENCE_LOW:

            explanation = (
                f"Moderate predictive risk is present for {module}. "
                f"The available historical evidence is limited, "
                f"so continued monitoring is recommended."
            )

        else:

            explanation = (
                f"Moderate predictive risk is present "
                f"for {module}. Continued monitoring is recommended."
            )

    elif risk == RISK_LOW:

        explanation = (
            f"Predictive risk for {module} is currently "
            f"low. Normal operation can continue."
        )

    else:

        explanation = (
            f"{module} does not have enough historical data "
            f"for a reliable predictive assessment."
        )

    if data_quality == "NO_DATA":

        explanation += (
            " Additional historical data is required "
            "before a reliable prediction can be made."
        )

    elif data_quality in (
        "VERY_LOW",
        "LOW",
    ):

        explanation += (
            f" Data quality is {data_quality} "
            f"({data_quality_score}/100), so the "
            f"prediction should be interpreted cautiously."
        )

    elif not reliable:

        explanation += (
            " The available evidence is not yet "
            "considered sufficiently reliable."
        )

    return {
        "module": module,
        "risk": risk,
        "risk_score": risk_score,
        "confidence": confidence,
        "evidence": evidence,
        "data_quality": data_quality,
        "data_quality_score": data_quality_score,
        "reliable": reliable,
        "action": action,
        "priority": priority,
        "explanation": explanation,
    }


# ============================================================
# MODULE PREDICTIONS
# ============================================================

def get_module_predictions():
    """
    Generate predictive assessments for each module.

    Returns:
        list: Module prediction information.
    """

    scores = get_predictive_risk_scores()

    # --------------------------------------------------------
    # Step 6B-5 — Integrate Module Data Quality
    # --------------------------------------------------------

    quality_profiles = get_module_data_quality_profile()

    quality_map = {
        item["module"]: item
        for item in quality_profiles
    }

    predictions = []

    for item in scores:

        module = item["module"]
        risk = item["risk"]
        score = item["risk_score"]
        confidence = item["confidence"]

        pattern = item["pattern"]
        trend = item["trend"]

        # --------------------------------------------------------
        # Step 6C-4 — Preserve Historical Evidence
        # --------------------------------------------------------

        events = item.get(
            "events",
            0
        )

        failed = item.get(
            "failed",
            0
        )

        success_rate = item.get(
            "success_rate",
            0.0
        )

        signal_strength = item.get(
            "signal_strength",
            "NO_DATA"
        )

        quality_profile = quality_map.get(
            module,
            {}
        )

        data_quality = quality_profile.get(
            "data_quality",
            "NO_DATA"
        )

        data_quality_score = quality_profile.get(
            "data_quality_score",
            0
        )

        data_quality_reliable = quality_profile.get(
            "reliable",
            False
        )

        if risk == RISK_INSUFFICIENT:

            prediction = (
                f"{module} does not have enough "
                "historical data for a reliable "
                "predictive assessment."
            )

        elif risk == RISK_CRITICAL:

            prediction = (
                f"{module} shows critical predictive "
                "risk signals. Immediate investigation "
                "is recommended."
            )

        elif risk == RISK_HIGH:

            prediction = (
                f"{module} shows strong warning signals "
                "that may indicate increased future "
                "failure risk."
            )

        elif risk == RISK_MEDIUM:

            prediction = (
                f"{module} shows moderate predictive "
                "risk. Continued monitoring is recommended."
            )

        else:

            prediction = (
                f"{module} currently shows low predictive "
                "risk based on available historical signals."
            )

        # --------------------------------------------------------
        # Step 4B — Determine recommended action
        # --------------------------------------------------------

        decision = _determine_risk_action(
            risk,
            confidence,
        )

        module_prediction = {
            "module": module,
            "risk_score": score,
            "risk": risk,
            "confidence": confidence,
            "pattern": pattern,
            "trend": trend,
            "prediction": prediction,

            # Step 6C-4 — Historical Evidence
            "events": events,
            "failed": failed,
            "success_rate": success_rate,
            "signal_strength": signal_strength,

            # Step 6B-5 — Predictive Data Quality
            "data_quality": data_quality,
            "data_quality_score": data_quality_score,
            "data_quality_reliable": data_quality_reliable,

            # Step 4B — Risk Action Intelligence
            "action": decision["action"],
            "priority": decision["priority"],
            "action_reason": decision["reason"],
        }

        # --------------------------------------------------------
        # Step 6C-4 — Attach Predictive Explanation
        # --------------------------------------------------------

        explanation = _get_predictive_explanation(
            module_prediction
        )

        module_prediction["evidence"] = explanation[
            "evidence"
        ]

        module_prediction["explanation"] = explanation[
            "explanation"
        ]

        predictions.append(
            module_prediction
        )

    return predictions


# ============================================================
# SYSTEM PREDICTION
# ============================================================

def get_system_prediction():
    """
    Generate an overall predictive assessment for HOPE.

    Returns:
        dict: System prediction.
    """

    predictions = get_module_predictions()

    # --------------------------------------------------------
    # Step 4E — Determine overall system action
    # --------------------------------------------------------

    system_decision = _determine_system_action(
        predictions
    )

    if not predictions:

        return {
            "overall_risk": RISK_INSUFFICIENT,
            "risk_score": 0,
            "confidence": CONFIDENCE_INSUFFICIENT,
            "action": system_decision["action"],
            "priority": system_decision["priority"],
            "action_reason": system_decision["reason"],
            "message": (
                "No predictive module data is available yet."
            ),
        }

    insufficient = sum(
        1
        for item in predictions
        if item["risk"] == RISK_INSUFFICIENT
    )

    critical = sum(
        1
        for item in predictions
        if item["risk"] == RISK_CRITICAL
    )

    high = sum(
        1
        for item in predictions
        if item["risk"] == RISK_HIGH
    )

    medium = sum(
        1
        for item in predictions
        if item["risk"] == RISK_MEDIUM
    )

    usable_scores = [
        item["risk_score"]
        for item in predictions
        if item["risk"] != RISK_INSUFFICIENT
    ]

    # --------------------------------------------------------
    # No usable historical data
    # --------------------------------------------------------

    if not usable_scores:

        return {
            "overall_risk": RISK_INSUFFICIENT,
            "risk_score": 0,
            "confidence": CONFIDENCE_INSUFFICIENT,
            "action": system_decision["action"],
            "priority": system_decision["priority"],
            "action_reason": system_decision["reason"],
            "message": (
                "There is not enough historical data "
                "to make a reliable system prediction."
            ),
        }

    average_score = round(
        sum(usable_scores)
        / len(usable_scores)
    )

    if critical > 0:

        overall_risk = RISK_CRITICAL

    elif high > 0:

        overall_risk = RISK_HIGH

    elif medium > 0:

        overall_risk = RISK_MEDIUM

    else:

        overall_risk = RISK_LOW

    confidence = CONFIDENCE_LOW

    if insufficient == 0:

        confidence = CONFIDENCE_MEDIUM

        if len(predictions) >= 3:
            confidence = CONFIDENCE_HIGH

    return {
        "overall_risk": overall_risk,
        "risk_score": average_score,
        "confidence": confidence,
        "modules": len(predictions),
        "critical": critical,
        "high": high,
        "medium": medium,
        "insufficient_data": insufficient,
        "action": system_decision["action"],
        "priority": system_decision["priority"],
        "action_reason": system_decision["reason"],
        "message": (
            "HOPE predictive assessment is based on "
            "available module health and historical "
            "recovery signals."
        ),
    }


# ============================================================
# PREDICTIVE RECOMMENDATION
# ============================================================

def get_predictive_recommendation():
    """
    Generate a recommendation based on predictive analysis.

    Returns:
        dict: Recommendation information.
    """

    system = get_system_prediction()

    risk = system.get(
        "overall_risk",
        RISK_INSUFFICIENT
    )

    if risk == RISK_INSUFFICIENT:

        return {
            "level": "INFO",
            "action": "MONITOR",
            "risk": RISK_INSUFFICIENT,
            "message": (
                "There is not enough historical data "
                "to make a reliable predictive assessment. "
                "Continue monitoring HOPE."
            ),
        }

    if risk == RISK_CRITICAL:

        return {
            "level": "CRITICAL",
            "action": "INVESTIGATE_IMMEDIATELY",
            "risk": RISK_CRITICAL,
            "message": (
                "Critical predictive signals detected. "
                "Investigate affected modules immediately."
            ),
        }

    if risk == RISK_HIGH:

        return {
            "level": "WARNING",
            "action": "INVESTIGATE",
            "risk": RISK_HIGH,
            "message": (
                "High predictive risk detected. "
                "Investigate the affected modules "
                "before the condition worsens."
            ),
        }

    if risk == RISK_MEDIUM:

        return {
            "level": "NOTICE",
            "action": "MONITOR",
            "risk": RISK_MEDIUM,
            "message": (
                "Moderate predictive risk detected. "
                "Continue monitoring module health "
                "and recovery activity."
            ),
        }

    return {
        "level": "GOOD",
        "action": "NO_ACTION",
        "risk": RISK_LOW,
        "message": (
            "Predictive risk is currently low. "
            "Continue normal monitoring."
        ),
    }


# ============================================================
# STEP 6D-1 — PREDICTIVE ACTION INTELLIGENCE
# ============================================================

def _get_action_mode(risk, confidence, data_quality):
    """
    Determine how HOPE should present a predictive action.

    6D-1 is advisory only. It does not execute system actions.
    """
    if risk in [
        RISK_CRITICAL,
        RISK_HIGH,
    ]:
        return "HUMAN_REVIEW"

    if data_quality == "NO_DATA":
        return "DATA_COLLECTION"

    if confidence == CONFIDENCE_INSUFFICIENT:
        return "DATA_COLLECTION"

    return "ADVISORY"


def _get_recommended_steps(
    risk,
    action,
    confidence,
    data_quality,
    module,
):
    """
    Generate concrete advisory steps from an existing prediction.

    This function does not change the prediction or execute any
    system operation.
    """
    steps = []

    if action == "INTERVENE":
        steps.extend([
            f"Review the current health of {module}.",
            "Investigate the evidence behind the critical risk.",
            "Require human approval before any intervention.",
        ])

    elif action == "INVESTIGATE":
        steps.extend([
            f"Investigate the recent recovery history of {module}.",
            "Review failure and trend signals.",
            "Reassess the module after investigation.",
        ])

    elif action == "MONITOR":
        steps.extend([
            f"Continue monitoring {module}.",
            "Watch for increasing recovery frequency or failures.",
            "Collect additional historical data to improve confidence.",
        ])

    elif action == "COLLECT_DATA":
        steps.extend([
            f"Collect additional historical data for {module}.",
            "Continue monitoring the module while evidence is limited.",
            "Reassess predictive risk after sufficient data is available.",
        ])

    elif action == "CONTINUE":
        steps.extend([
            f"Continue normal operation of {module}.",
            "Maintain routine monitoring.",
        ])

    else:
        steps.append(
            f"Continue monitoring {module} and review new evidence."
        )

    if confidence == CONFIDENCE_INSUFFICIENT:
        steps.append(
            "Treat the current prediction as insufficient for a "
            "reliable risk decision."
        )

    elif data_quality in [
        "VERY_LOW",
        "LOW",
    ]:
        steps.append(
            "Interpret the prediction cautiously because data quality "
            "is limited."
        )

    return steps


def get_predictive_action_plan(item):
    """
    Convert an existing module prediction into a structured
    predictive action plan.

    This is the foundation of Milestone 6D. It interprets the
    existing prediction and creates an advisory action plan.

    It does NOT:
        - recalculate risk
        - change confidence
        - change data quality
        - modify the prediction
        - execute recovery
        - modify system modules

    Args:
        item (dict): Existing module prediction.

    Returns:
        dict: Structured predictive action plan.
    """
    if not isinstance(item, dict):
        item = {}

    module = item.get(
        "module",
        "Unknown Module"
    )

    risk = item.get(
        "risk",
        RISK_INSUFFICIENT
    )

    risk_score = item.get(
        "risk_score",
        0
    )

    confidence = item.get(
        "confidence",
        CONFIDENCE_INSUFFICIENT
    )

    data_quality = item.get(
        "data_quality",
        "NO_DATA"
    )

    data_quality_score = item.get(
        "data_quality_score",
        0
    )

    action = item.get(
        "action",
        "COLLECT_DATA"
    )

    priority = item.get(
        "priority",
        "LOW"
    )

    action_reason = item.get(
        "action_reason",
        "No predictive action reason is available."
    )

    # Preserve the original prediction explanation when available.
    # If a raw prediction is supplied without one, generate the
    # explanation from the existing prediction signals.
    explanation = item.get("explanation")

    if not explanation:
        explanation_data = _get_predictive_explanation(item)
        explanation = explanation_data.get(
            "explanation",
            "No predictive explanation is available."
        )

    mode = _get_action_mode(
        risk,
        confidence,
        data_quality
    )

    recommended_steps = _get_recommended_steps(
        risk,
        action,
        confidence,
        data_quality,
        module,
    )

    return {
        "module": module,
        "risk": risk,
        "risk_score": risk_score,
        "confidence": confidence,
        "data_quality": data_quality,
        "data_quality_score": data_quality_score,
        "action": action,
        "priority": priority,
        "mode": mode,
        "reason": action_reason,
        "action_reason": action_reason,
        "explanation": explanation,
        "recommended_steps": recommended_steps,
    }


def get_predictive_action_plans():
    """
    Generate advisory action plans for all predictive modules.

    Returns:
        list: Structured action plans.
    """
    predictions = get_module_predictions()

    return [
        get_predictive_action_plan(
            prediction
        )
        for prediction in predictions
    ]


# ============================================================
# STEP 6D-2 — ACTION PRIORITY ENGINE
# ============================================================

def _determine_action_priority(
    risk,
    risk_score,
    confidence,
    data_quality,
    action,
):
    """
    Determine the urgency of an existing predictive action.

    Priority is derived from the existing prediction and does not
    recalculate or modify predictive risk.

    Returns:
        str: CRITICAL, HIGH, MEDIUM, or LOW.
    """
    if risk == RISK_CRITICAL:
        return "CRITICAL"

    if risk == RISK_HIGH:
        return "HIGH"

    if risk == RISK_MEDIUM:
        return "MEDIUM"

    if risk == RISK_LOW:
        return "LOW"

    if risk == RISK_INSUFFICIENT:
        return "LOW"

    if action == "INTERVENE":
        return "CRITICAL"

    if action == "INVESTIGATE":
        return "HIGH"

    if action == "MONITOR":
        return "MEDIUM"

    return "LOW"


def get_predictive_action_priority(item):
    """
    Add an independently determined priority to an existing
    predictive action plan.

    This function does not execute actions and does not change
    the original predictive risk assessment.

    Args:
        item (dict): Existing predictive action plan or prediction.

    Returns:
        dict: Action plan with priority intelligence.
    """
    if not isinstance(item, dict):
        item = {}

    plan = dict(item)

    risk = plan.get(
        "risk",
        RISK_INSUFFICIENT
    )

    risk_score = plan.get(
        "risk_score",
        0
    )

    confidence = plan.get(
        "confidence",
        CONFIDENCE_INSUFFICIENT
    )

    data_quality = plan.get(
        "data_quality",
        "NO_DATA"
    )

    action = plan.get(
        "action",
        "COLLECT_DATA"
    )

    priority = _determine_action_priority(
        risk,
        risk_score,
        confidence,
        data_quality,
        action,
    )

    plan["priority"] = priority

    plan["priority_reason"] = (
        f"Action priority is {priority} based on "
        f"{risk} predictive risk."
    )

    return plan


def get_predictive_action_priorities():
    """
    Generate prioritized advisory action plans for all modules.

    Returns:
        list: Action plans with priority intelligence.
    """
    plans = get_predictive_action_plans()

    return [
        get_predictive_action_priority(
            plan
        )
        for plan in plans
    ]


# ============================================================
# STEP 6D-3 — ACTION PLAN GENERATION
# ============================================================

def _get_action_plan_trigger(risk, action):
    """
    Determine what condition should cause HOPE to reassess the plan.
    """
    if risk == RISK_CRITICAL or action == "INTERVENE":
        return "Immediate review of critical evidence and system condition."

    if risk == RISK_HIGH or action == "INVESTIGATE":
        return "Reassess when investigation identifies new failure or recovery signals."

    if risk == RISK_MEDIUM or action == "MONITOR":
        return "Reassess if risk, failure frequency, or recovery frequency increases."

    if risk == RISK_INSUFFICIENT or action == "COLLECT_DATA":
        return "Reassess after sufficient historical data has been collected."

    return "Reassess when meaningful new predictive evidence becomes available."


def _get_action_plan_review(risk, confidence, data_quality):
    """
    Determine when the advisory plan should be reviewed.
    """
    if risk == RISK_CRITICAL:
        return "Immediate human review."

    if risk == RISK_HIGH:
        return "Review after investigation or significant new evidence."

    if confidence == CONFIDENCE_INSUFFICIENT:
        return "Review after additional historical data is available."

    if data_quality in ["VERY_LOW", "LOW"]:
        return "Review after additional historical data improves data quality."

    return "Review when new predictive evidence becomes available."


def _get_action_plan_steps(plan):
    """
    Convert recommended steps into numbered action-plan steps.
    """
    steps = plan.get("recommended_steps", [])

    if not isinstance(steps, list):
        steps = [str(steps)]

    return [
        {
            "step": index,
            "instruction": str(step),
        }
        for index, step in enumerate(steps, start=1)
    ]


def get_predictive_action_plan_details(item):
    """
    Generate a structured advisory action plan from an existing
    predictive action-priority result.

    This function does not execute any action and does not modify
    the underlying prediction.
    """
    if not isinstance(item, dict):
        item = {}

    plan = dict(item)

    risk = plan.get("risk", RISK_INSUFFICIENT)
    action = plan.get("action", "COLLECT_DATA")
    confidence = plan.get(
        "confidence",
        CONFIDENCE_INSUFFICIENT
    )
    data_quality = plan.get("data_quality", "NO_DATA")

    # Build the complete action-plan foundation when the caller
    # provides a raw prediction. If the caller already provides
    # recommended_steps, preserve the existing action plan.
    if "recommended_steps" not in plan:
        plan = get_predictive_action_plan(plan)

    # Ensure priority intelligence exists.
    if "priority_reason" not in plan:
        plan = get_predictive_action_priority(plan)

    plan["plan_steps"] = _get_action_plan_steps(plan)

    plan["trigger"] = _get_action_plan_trigger(
        risk,
        action,
    )

    plan["review"] = _get_action_plan_review(
        risk,
        confidence,
        data_quality,
    )

    plan["plan_mode"] = plan.get(
        "mode",
        "ADVISORY"
    )

    plan["plan_status"] = "READY"

    return plan


def get_predictive_action_plan_details_all():
    """
    Generate detailed advisory action plans for all predictive modules.
    """
    plans = get_predictive_action_priorities()

    return [
        get_predictive_action_plan_details(plan)
        for plan in plans
    ]


def get_predictive_action_plan_report(item):
    """
    Format a single predictive action plan for human-readable output.
    """
    plan = get_predictive_action_plan_details(item)

    lines = [
        "🧭 HOPE Predictive Action Plan",
        "",
        f"Module       : {plan.get('module', 'Unknown Module')}",
        f"Risk         : {plan.get('risk', RISK_INSUFFICIENT)}",
        f"Risk Score   : {plan.get('risk_score', 0)}/100",
        f"Confidence   : {plan.get('confidence', CONFIDENCE_INSUFFICIENT)}",
        f"Data Quality : {plan.get('data_quality', 'NO_DATA')}",
        f"Action       : {plan.get('action', 'COLLECT_DATA')}",
        f"Priority     : {plan.get('priority', 'LOW')}",
        f"Mode         : {plan.get('plan_mode', 'ADVISORY')}",
        f"Status       : {plan.get('plan_status', 'READY')}",
        "",
        "Plan:",
    ]

    for step in plan.get("plan_steps", []):
        lines.append(
            f"  {step['step']}. {step['instruction']}"
        )

    lines.extend([
        "",
        "Trigger:",
        f"  {plan.get('trigger', 'Reassess when new evidence is available.')}",
        "",
        "Review:",
        f"  {plan.get('review', 'Review when new predictive evidence becomes available.')}",
    ])

    return "\n".join(lines)


def get_predictive_action_plan_reports():
    """
    Generate human-readable action-plan reports for all modules.
    """
    plans = get_predictive_action_plan_details_all()

    return [
        get_predictive_action_plan_report(plan)
        for plan in plans
    ]


# ============================================================
# STEP 6D-4 — ACTION SAFETY RULES
# ============================================================

def _determine_action_safety(risk, action, confidence, data_quality):
    """
    Determine whether a predictive recommendation may be treated
    as advisory, requires human review, or is limited to data
    collection.

    6D-4 is a safety layer only. It never executes an action.
    """
    if risk == RISK_CRITICAL or action == "INTERVENE":
        return {
            "safety_level": "HUMAN_REVIEW_REQUIRED",
            "execution_allowed": False,
            "automatic_action_allowed": False,
            "reason": (
                "Critical or intervention-level prediction requires "
                "human review before any system-changing action."
            ),
        }

    if risk == RISK_HIGH or action == "INVESTIGATE":
        return {
            "safety_level": "HUMAN_REVIEW_REQUIRED",
            "execution_allowed": False,
            "automatic_action_allowed": False,
            "reason": (
                "High-risk or investigation-level prediction requires "
                "human review. No automatic system change is permitted."
            ),
        }

    if (
        risk == RISK_INSUFFICIENT
        or confidence == CONFIDENCE_INSUFFICIENT
        or data_quality == "NO_DATA"
    ):
        return {
            "safety_level": "DATA_COLLECTION_ONLY",
            "execution_allowed": False,
            "automatic_action_allowed": False,
            "reason": (
                "Insufficient evidence is available. HOPE may recommend "
                "data collection and monitoring, but must not execute "
                "system-changing actions."
            ),
        }

    return {
        "safety_level": "ADVISORY_ONLY",
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "reason": (
            "Predictive recommendations are advisory only. No automatic "
            "system-changing action is permitted."
        ),
    }


def get_predictive_action_safety(item):
    """
    Add safety controls to an existing predictive action plan.

    This function explicitly prevents predictive output from being
    interpreted as permission to execute a system-changing action.
    """
    if not isinstance(item, dict):
        item = {}

    plan = dict(item)

    risk = plan.get("risk", RISK_INSUFFICIENT)
    action = plan.get("action", "COLLECT_DATA")
    confidence = plan.get(
        "confidence",
        CONFIDENCE_INSUFFICIENT
    )
    data_quality = plan.get("data_quality", "NO_DATA")

    safety = _determine_action_safety(
        risk,
        action,
        confidence,
        data_quality,
    )

    # Keep the predictive action reason intact. Safety is a separate
    # decision layer and must not overwrite the original explanation.
    plan["safety_level"] = safety["safety_level"]
    plan["execution_allowed"] = safety["execution_allowed"]
    plan["automatic_action_allowed"] = safety["automatic_action_allowed"]
    plan["safety_reason"] = safety["reason"]

    return plan


def get_predictive_action_safety_all():
    """
    Generate safety-classified action plans for all modules.
    """
    plans = get_predictive_action_plan_details_all()

    return [
        get_predictive_action_safety(plan)
        for plan in plans
    ]


def get_predictive_safe_action_plan(item):
    """
    Build the complete 6D action plan with safety controls.

    The result is advisory and cannot authorize automatic
    system-changing actions.
    """
    plan = get_predictive_action_plan_details(item)

    # Final boundary guarantee: a safe action plan must carry a
    # predictive explanation. If an older/intermediate plan does not,
    # derive it from the prediction signals here.
    if not plan.get("explanation"):
        explanation_data = _get_predictive_explanation(plan)
        plan["explanation"] = explanation_data.get(
            "explanation",
            "No predictive explanation is available."
        )

    return get_predictive_action_safety(plan)


def get_predictive_safe_action_plan_report(item):
    """
    Format the complete predictive action plan and its safety
    controls for human-readable output.

    This is presentation only. It never executes an action.
    """
    plan = get_predictive_safe_action_plan(item)

    explanation = plan.get("explanation")
    if not explanation:
        explanation_data = _get_predictive_explanation(plan)
        explanation = explanation_data.get(
            "explanation",
            "No predictive explanation is available."
        )

    lines = [
        "🛡️ HOPE Predictive Safe Action Plan",
        "",
        f"Module       : {plan.get('module', 'Unknown Module')}",
        f"Risk         : {plan.get('risk', RISK_INSUFFICIENT)}",
        f"Risk Score   : {plan.get('risk_score', 0)}/100",
        f"Confidence   : {plan.get('confidence', CONFIDENCE_INSUFFICIENT)}",
        f"Data Quality : {plan.get('data_quality', 'NO_DATA')}",
        f"Action       : {plan.get('action', 'COLLECT_DATA')}",
        f"Priority     : {plan.get('priority', 'LOW')}",
        f"Mode         : {plan.get('plan_mode', 'ADVISORY')}",
        f"Status       : {plan.get('plan_status', 'READY')}",
        "",
        "Safety:",
        f"  Level      : {plan.get('safety_level', 'ADVISORY_ONLY')}",
        f"  Execution  : {plan.get('execution_allowed', False)}",
        f"  Automatic  : {plan.get('automatic_action_allowed', False)}",
        "",
        "Safety Reason:",
        f"  {plan.get('safety_reason', 'No safety reason is available.')}",
        "",
        "Plan:",
    ]

    for step in plan.get("plan_steps", []):
        lines.append(
            f"  {step['step']}. {step['instruction']}"
        )

    lines.extend([
        "",
        "Trigger:",
        f"  {plan.get('trigger', 'Reassess when new evidence is available.')}",
        "",
        "Review:",
        f"  {plan.get('review', 'Review when new predictive evidence becomes available.')}",
    ])

    return "\n".join(lines)


# ============================================================
# STEP 6D-5 — PREDICTIVE ACTION REPORT
# ============================================================

def get_predictive_action_report(item):
    """
    Build one complete user-facing report from the 6D predictive
    action pipeline.

    The report combines:
        prediction
        action
        priority
        plan
        trigger/review
        safety

    This function is presentation only. It never executes actions.
    """
    plan = get_predictive_safe_action_plan(item)

    # Final presentation boundary: guarantee that the report has
    # a predictive explanation even when an intermediate/raw object
    # does not carry one.
    explanation = plan.get("explanation")

    if not explanation:
        explanation_data = _get_predictive_explanation(plan)
        explanation = explanation_data.get(
            "explanation",
            "No predictive explanation is available."
        )

    lines = [
        "🛡️ HOPE Predictive Action Report",
        "",
        "Prediction:",
        f"Module       : {plan.get('module', 'Unknown Module')}",
        f"Risk         : {plan.get('risk', RISK_INSUFFICIENT)}",
        f"Risk Score   : {plan.get('risk_score', 0)}/100",
        f"Confidence   : {plan.get('confidence', CONFIDENCE_INSUFFICIENT)}",
        f"Data Quality : {plan.get('data_quality', 'NO_DATA')}",
        "",
        "Decision:",
        f"Action       : {plan.get('action', 'COLLECT_DATA')}",
        f"Priority     : {plan.get('priority', 'LOW')}",
        f"Mode         : {plan.get('plan_mode', 'ADVISORY')}",
        f"Status       : {plan.get('plan_status', 'READY')}",
        "",
        "Why:",
        f"{explanation}",
        "",
        "Action Plan:",
    ]

    for step in plan.get("plan_steps", []):
        lines.append(
            f"{step['step']}. {step['instruction']}"
        )

    lines.extend([
        "",
        "Trigger:",
        f"{plan.get('trigger', 'Reassess when new predictive evidence becomes available.')}",
        "",
        "Review:",
        f"{plan.get('review', 'Review when new predictive evidence becomes available.')}",
        "",
        "Safety:",
        f"Level      : {plan.get('safety_level', 'ADVISORY_ONLY')}",
        f"Execution  : {plan.get('execution_allowed', False)}",
        f"Automatic  : {plan.get('automatic_action_allowed', False)}",
        "",
        "Safety Reason:",
        f"{plan.get('safety_reason', 'No automatic system-changing action is permitted.')}",
    ])

    return "\n".join(lines)


def get_predictive_action_reports():
    """
    Generate complete predictive action reports for all modules.
    """
    plans = get_predictive_action_safety_all()

    return [
        get_predictive_action_report(plan)
        for plan in plans
    ]


# ============================================================
# PREDICTIVE REPORT
# ============================================================

def get_predictive_report():
    """
    Generate the complete HOPE Predictive Intelligence report.

    Returns:
        str: Formatted predictive report.
    """

    system = get_system_prediction()
    predictions = get_module_predictions()
    recommendation = get_predictive_recommendation()

    # --------------------------------------------------------
    # Step 4F — Expose system action decision
    # --------------------------------------------------------

    system_action = system.get(
        "action",
        "COLLECT_DATA"
    )

    system_priority = system.get(
        "priority",
        "LOW"
    )

    system_action_reason = system.get(
        "action_reason",
        "No system action reason is available."
    )

    lines = [
        "🔮 HOPE Predictive Intelligence",
        "",
        f"Overall Risk : "
        f"{system.get('overall_risk', RISK_INSUFFICIENT)}",
        f"Risk Score   : "
        f"{system.get('risk_score', 0)}/100",
        f"Confidence   : "
        f"{system.get('confidence', CONFIDENCE_INSUFFICIENT)}",
        f"Modules      : "
        f"{system.get('modules', len(predictions))}",
        "",
        "🎯 System Decision",
        f"Action       : {system_action}",
        f"Priority     : {system_priority}",
        f"Reason       : {system_action_reason}",
        "",
        "📊 Predictive Risk Distribution",
        f"Low              : "
        f"{sum(1 for p in predictions if p['risk'] == RISK_LOW)}",
        f"Medium           : "
        f"{sum(1 for p in predictions if p['risk'] == RISK_MEDIUM)}",
        f"High             : "
        f"{sum(1 for p in predictions if p['risk'] == RISK_HIGH)}",
        f"Critical         : "
        f"{sum(1 for p in predictions if p['risk'] == RISK_CRITICAL)}",
        f"Insufficient Data: "
        f"{sum(1 for p in predictions if p['risk'] == RISK_INSUFFICIENT)}",
        "",
        "🧠 Module Predictions",
    ]

    if not predictions:

        lines.append(
            "• No predictive module data available."
        )

    else:

        for prediction in predictions:

            lines.extend([
                "",
                f"• {prediction['module']}",
                f"  Risk Score    : {prediction['risk_score']}/100",
                f"  Risk          : {prediction['risk']}",
                f"  Confidence    : {prediction['confidence']}",
                f"  Pattern       : {prediction['pattern']}",
                f"  Trend         : {prediction['trend']}",
                f"  Prediction    : {prediction['prediction']}",
                f"  Data Quality  : {prediction.get('data_quality', 'NO_DATA')}",
                f"  Quality Score : {prediction.get('data_quality_score', 0)}/100",
                f"  Reliable      : {prediction.get('data_quality_reliable', False)}",
            ])

            evidence = prediction.get(
                "evidence",
                []
            )

            if evidence:

                lines.append(
                    "  Evidence:"
                )

                for evidence_item in evidence:

                    lines.append(
                        f"    • {evidence_item}"
                    )

            explanation = prediction.get(
                "explanation",
                ""
            )

            if explanation:

                lines.extend([
                    "  Why:",
                    f"    {explanation}",
                ])

    lines.extend([
        "",
        "💡 Predictive Recommendation:",
        f"Level  : {recommendation['level']}",
        f"Action : {recommendation['action']}",
        "",
        recommendation["message"],
    ])

    return "\n".join(lines)


# ============================================================
# SIMPLE ALIAS
# ============================================================

def get_predictive_risk():
    """
    Return the overall predictive system risk.

    Returns:
        dict: Overall predictive risk.
    """

    return get_system_prediction()


# ============================================================
# MODULE SELF-TEST
# ============================================================

if __name__ == "__main__":

    print(
        get_predictive_report()
    )

def get_predictive_safe_action_plan_reports():
    """
    Generate human-readable safe action-plan reports for all modules.
    """
    plans = get_predictive_action_safety_all()

    return [
        get_predictive_safe_action_plan_report(plan)
        for plan in plans
    ]

# ============================================================
# STEP 6E-1 — PREDICTIVE ACTION INTEGRATION
# ============================================================

def _normalize_6e_text(value):
    """
    Normalize legacy joined-word presentation artifacts at the 6E
    integration boundary only.

    This does not change predictive calculations or 6D source logic.
    """
    replacements = {
        "monitoringis": "monitoring is",
        "predictionshould": "prediction should",
        "historicaldata": "historical data",
        "areliable": "a reliable",
        "Dataquality": "Data quality",
        "dataquality": "data quality",
        "islimited": "is limited",
        "Continuemonitoring": "Continue monitoring",
        "Continue monitoring": "Continue monitoring",
    }

    result = str(value)
    for old, new in replacements.items():
        result = result.replace(old, new)

    return result


def _normalize_6e_steps(value):
    """Normalize text inside 6E action-plan step structures."""
    if not isinstance(value, list):
        return value

    normalized = []
    for step in value:
        if isinstance(step, dict):
            item = dict(step)
            if "instruction" in item:
                item["instruction"] = _normalize_6e_text(
                    item["instruction"]
                )
            normalized.append(item)
        else:
            normalized.append(_normalize_6e_text(step))

    return normalized


def get_predictive_action_decision(item):
    """
    Integrate the completed 6D predictive action pipeline into one
    normalized decision object.

    6E-1 is an integration boundary only:
        prediction
            -> explanation
            -> action
            -> priority
            -> action plan
            -> safety

    This function does not recalculate predictive risk, does not
    execute actions, and does not authorize automatic system changes.

    The existing 6D safety decision remains authoritative.
    """
    if not isinstance(item, dict):
        item = {}

    # Consume the completed 6D safe action plan. This preserves the
    # frozen 6D logic and keeps safety as the final authority.
    safe_plan = get_predictive_safe_action_plan(item)

    # Normalize the integration contract without changing the
    # underlying 6D fields.
    decision = {
        "module": safe_plan.get(
            "module",
            "Unknown Module"
        ),
        "risk": safe_plan.get(
            "risk",
            RISK_INSUFFICIENT
        ),
        "risk_score": safe_plan.get(
            "risk_score",
            0
        ),
        "confidence": safe_plan.get(
            "confidence",
            CONFIDENCE_INSUFFICIENT
        ),
        "data_quality": safe_plan.get(
            "data_quality",
            "NO_DATA"
        ),
        "data_quality_score": safe_plan.get(
            "data_quality_score",
            0
        ),
        "action": safe_plan.get(
            "action",
            "COLLECT_DATA"
        ),
        "priority": safe_plan.get(
            "priority",
            "LOW"
        ),
        "mode": safe_plan.get(
            "plan_mode",
            safe_plan.get("mode", "ADVISORY")
        ),
        "status": safe_plan.get(
            "plan_status",
            "READY"
        ),
        "explanation": _normalize_6e_text(
            safe_plan.get(
                "explanation",
                "No predictive explanation is available."
            )
        ),
        "recommended_steps": _normalize_6e_steps(
            safe_plan.get(
                "recommended_steps",
                []
            )
        ),
        "plan_steps": _normalize_6e_steps(
            safe_plan.get(
                "plan_steps",
                []
            )
        ),
        "trigger": _normalize_6e_text(
            safe_plan.get(
                "trigger",
                "Reassess when new predictive evidence becomes available."
            )
        ),
        "review": _normalize_6e_text(
            safe_plan.get(
                "review",
                "Review when new predictive evidence becomes available."
            )
        ),
        "safety_level": safe_plan.get(
            "safety_level",
            "ADVISORY_ONLY"
        ),
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "safety_reason": _normalize_6e_text(
            safe_plan.get(
                "safety_reason",
                "Predictive recommendations are advisory only. "
                "No automatic system-changing action is permitted."
            )
        ),
    }

    # 6E-1 safety invariant:
    # predictive output never becomes execution authority.
    decision["execution_allowed"] = bool(
        safe_plan.get("execution_allowed", False)
    ) and False

    decision["automatic_action_allowed"] = bool(
        safe_plan.get("automatic_action_allowed", False)
    ) and False

    decision["integration_layer"] = "6E-1"
    decision["integration_status"] = "READY"

    return decision


def get_predictive_action_decisions():
    """
    Generate normalized 6E-1 predictive action decisions for all
    predictive modules.

    The decisions are advisory integration objects only.
    No action is executed.
    """
    predictions = get_module_predictions()

    return [
        get_predictive_action_decision(prediction)
        for prediction in predictions
    ]


def get_predictive_action_decision_report(item):
    """
    Format one 6E-1 integrated predictive action decision.

    Presentation only. This function never executes an action.
    """
    decision = get_predictive_action_decision(item)

    lines = [
        "🔗 HOPE Predictive Action Decision",
        "",
        f"Module       : {decision.get('module', 'Unknown Module')}",
        f"Risk         : {decision.get('risk', RISK_INSUFFICIENT)}",
        f"Risk Score   : {decision.get('risk_score', 0)}/100",
        f"Confidence   : {decision.get('confidence', CONFIDENCE_INSUFFICIENT)}",
        f"Data Quality : {decision.get('data_quality', 'NO_DATA')}",
        f"Action       : {decision.get('action', 'COLLECT_DATA')}",
        f"Priority     : {decision.get('priority', 'LOW')}",
        f"Mode         : {decision.get('mode', 'ADVISORY')}",
        f"Status       : {decision.get('status', 'READY')}",
        "",
        "Why:",
        f"{decision.get('explanation', 'No predictive explanation is available.')}",
        "",
        "Safety:",
        f"Level      : {decision.get('safety_level', 'ADVISORY_ONLY')}",
        f"Execution  : {decision.get('execution_allowed', False)}",
        f"Automatic  : {decision.get('automatic_action_allowed', False)}",
        "",
        "Integration:",
        f"Layer      : {decision.get('integration_layer', '6E-1')}",
        f"Status     : {decision.get('integration_status', 'READY')}",
    ]

    return "\n".join(lines)


def get_predictive_action_decision_reports():
    """
    Generate human-readable 6E-1 integrated action-decision reports
    for all predictive modules.
    """
    decisions = get_predictive_action_decisions()

    return [
        get_predictive_action_decision_report(decision)
        for decision in decisions
    ]

# ============================================================
# STEP 6E-3 — PREDICTIVE DECISION SUMMARY
# ============================================================

def _determine_6e3_system_decision(decisions):
    """
    Determine the highest-priority system-level predictive decision
    from the completed 6E-1 decision objects.

    6E-3 is an aggregation layer only.

    It does NOT:
        - recalculate predictive risk
        - modify module decisions
        - execute actions
        - authorize automatic actions

    The existing 6D safety decision remains authoritative.
    """
    if not decisions:
        return {
            "action": "COLLECT_DATA",
            "priority": "LOW",
            "safety_level": "DATA_COLLECTION_ONLY",
            "reason": (
                "No predictive decisions are available. "
                "Additional predictive data is required."
            ),
        }

    priority_order = {
        "CRITICAL": 4,
        "HIGH": 3,
        "MEDIUM": 2,
        "LOW": 1,
    }

    safety_order = {
        "HUMAN_REVIEW_REQUIRED": 3,
        "DATA_COLLECTION_ONLY": 2,
        "ADVISORY_ONLY": 1,
    }

    selected = max(
        decisions,
        key=lambda item: (
            priority_order.get(item.get("priority"), 0),
            safety_order.get(item.get("safety_level"), 0),
            item.get("risk_score", 0),
        ),
    )

    return {
        "action": selected.get("action", "COLLECT_DATA"),
        "priority": selected.get("priority", "LOW"),
        "safety_level": selected.get(
            "safety_level",
            "ADVISORY_ONLY",
        ),
        "reason": selected.get(
            "safety_reason",
            "No predictive decision reason is available.",
        ),
    }


def get_predictive_decision_summary():
    """
    Generate the 6E-3 system-level predictive decision summary.

    This consumes completed 6E-1 decisions only.

    Returns:
        dict: System-level predictive decision summary.

    Safety:
        This function never executes an action and never grants
        execution authority.
    """
    decisions = get_predictive_action_decisions()

    if not decisions:
        return {
            "integration_layer": "6E-3",
            "integration_status": "READY",
            "modules": 0,
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "insufficient_data": 0,
            "selected_module": None,
            "selected_risk": RISK_INSUFFICIENT,
            "selected_risk_score": 0,
            "action": "COLLECT_DATA",
            "priority": "LOW",
            "safety_level": "DATA_COLLECTION_ONLY",
            "execution_allowed": False,
            "automatic_action_allowed": False,
            "reason": (
                "No predictive decisions are available. "
                "Additional predictive data is required."
            ),
        }

    critical = sum(
        1 for item in decisions
        if item.get("risk") == RISK_CRITICAL
    )
    high = sum(
        1 for item in decisions
        if item.get("risk") == RISK_HIGH
    )
    medium = sum(
        1 for item in decisions
        if item.get("risk") == RISK_MEDIUM
    )
    low = sum(
        1 for item in decisions
        if item.get("risk") == RISK_LOW
    )
    insufficient = sum(
        1 for item in decisions
        if item.get("risk") == RISK_INSUFFICIENT
    )

    priority_order = {
        "CRITICAL": 4,
        "HIGH": 3,
        "MEDIUM": 2,
        "LOW": 1,
    }
    safety_order = {
        "HUMAN_REVIEW_REQUIRED": 3,
        "DATA_COLLECTION_ONLY": 2,
        "ADVISORY_ONLY": 1,
    }

    selected = max(
        decisions,
        key=lambda item: (
            priority_order.get(item.get("priority"), 0),
            safety_order.get(item.get("safety_level"), 0),
            item.get("risk_score", 0),
        ),
    )

    system_decision = _determine_6e3_system_decision(decisions)

    # 6E-3 safety invariant:
    # aggregation can never create execution authority.
    execution_allowed = False
    automatic_action_allowed = False

    return {
        "integration_layer": "6E-3",
        "integration_status": "READY",
        "modules": len(decisions),
        "critical": critical,
        "high": high,
        "medium": medium,
        "low": low,
        "insufficient_data": insufficient,
        "selected_module": selected.get(
            "module",
            "Unknown Module",
        ),
        "selected_risk": selected.get(
            "risk",
            RISK_INSUFFICIENT,
        ),
        "selected_risk_score": selected.get(
            "risk_score",
            0,
        ),
        "action": system_decision["action"],
        "priority": system_decision["priority"],
        "safety_level": system_decision["safety_level"],
        "execution_allowed": execution_allowed,
        "automatic_action_allowed": automatic_action_allowed,
        "reason": system_decision["reason"],
    }


def get_predictive_decision_summary_report():
    """
    Generate a human-readable 6E-3 predictive decision summary.

    Presentation only.
    No action is executed.
    """
    summary = get_predictive_decision_summary()

    lines = [
        "🧭 HOPE Predictive Decision Summary",
        "",
        "Integration:",
        f"Layer          : {summary.get('integration_layer', '6E-3')}",
        f"Status         : {summary.get('integration_status', 'READY')}",
        "",
        "Decision:",
        f"Selected Module: {summary.get('selected_module', 'None')}",
        f"Risk           : {summary.get('selected_risk', RISK_INSUFFICIENT)}",
        f"Risk Score     : {summary.get('selected_risk_score', 0)}/100",
        f"Action         : {summary.get('action', 'COLLECT_DATA')}",
        f"Priority       : {summary.get('priority', 'LOW')}",
        "",
        "Risk Distribution:",
        f"Critical       : {summary.get('critical', 0)}",
        f"High           : {summary.get('high', 0)}",
        f"Medium         : {summary.get('medium', 0)}",
        f"Low            : {summary.get('low', 0)}",
        f"Insufficient   : {summary.get('insufficient_data', 0)}",
        "",
        "Safety:",
        f"Level          : {summary.get('safety_level', 'ADVISORY_ONLY')}",
        f"Execution      : {summary.get('execution_allowed', False)}",
        f"Automatic      : {summary.get('automatic_action_allowed', False)}",
        "",
        "Reason:",
        f"{summary.get('reason', 'No predictive decision reason is available.')}",
    ]

    return "\n".join(lines)



# ============================================================
# STEP 6E-4 — PREDICTIVE EXECUTION BOUNDARY
# ============================================================

def _determine_6e4_execution_boundary(decision):
    """
    Determine the execution boundary for a completed 6E decision.

    6E-4 is a hard execution gate. It consumes the completed 6E-1
    decision object and never changes its predictive risk, action,
    priority, or safety classification.

    Safety contract:
        - Predictive output is never execution authority.
        - Automatic system-changing actions are always blocked.
        - Human-review decisions remain blocked until an external,
          explicitly authorized workflow handles them.
        - Insufficient-data decisions remain data-collection only.
    """
    if not isinstance(decision, dict):
        decision = {}

    safety_level = decision.get(
        "safety_level",
        "ADVISORY_ONLY",
    )

    action = decision.get(
        "action",
        "COLLECT_DATA",
    )

    execution_allowed = bool(
        decision.get("execution_allowed", False)
    )

    automatic_action_allowed = bool(
        decision.get("automatic_action_allowed", False)
    )

    if safety_level == "HUMAN_REVIEW_REQUIRED":
        boundary = "HUMAN_REVIEW_REQUIRED"
        reason = (
            "Execution is blocked. This predictive decision requires "
            "human review before any system-changing action."
        )

    elif safety_level == "DATA_COLLECTION_ONLY":
        boundary = "DATA_COLLECTION_ONLY"
        reason = (
            "Execution is blocked because predictive evidence is "
            "insufficient. Only data collection and monitoring may be "
            "recommended."
        )

    else:
        boundary = "ADVISORY_ONLY"
        reason = (
            "Execution is blocked. Predictive recommendations are "
            "advisory only and cannot authorize system-changing actions."
        )

    # 6E-4 hard safety invariant.
    # Never inherit permission from an upstream object.
    return {
        "execution_boundary": boundary,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "requested_action": action,
        "upstream_execution_allowed": execution_allowed,
        "upstream_automatic_action_allowed": automatic_action_allowed,
        "reason": reason,
        "integration_layer": "6E-4",
        "integration_status": "READY",
    }


def get_predictive_execution_boundary(decision):
    """
    Apply the 6E-4 hard execution boundary to one predictive decision.

    This function is a safety gate only. It does not execute, queue,
    schedule, approve, or trigger any system-changing operation.
    """
    return _determine_6e4_execution_boundary(decision)


def get_predictive_execution_boundaries():
    """
    Generate 6E-4 execution boundaries for all 6E-1 decisions.

    Returns:
        list: One hard execution-boundary object per predictive module.
    """
    decisions = get_predictive_action_decisions()

    return [
        get_predictive_execution_boundary(decision)
        for decision in decisions
    ]


def get_predictive_execution_boundary_report(decision):
    """
    Generate a human-readable 6E-4 execution-boundary report.

    Presentation only. No action is executed.
    """
    boundary = get_predictive_execution_boundary(decision)

    module = "Unknown Module"
    if isinstance(decision, dict):
        module = decision.get(
            "module",
            "Unknown Module",
        )

    lines = [
        "🛡️ HOPE Predictive Execution Boundary",
        "",
        f"Module       : {module}",
        f"Requested    : {boundary.get('requested_action', 'COLLECT_DATA')}",
        f"Boundary     : {boundary.get('execution_boundary', 'ADVISORY_ONLY')}",
        f"Execution    : {boundary.get('execution_allowed', False)}",
        f"Automatic    : {boundary.get('automatic_action_allowed', False)}",
        "",
        "Safety:",
        f"{boundary.get('reason', 'Execution is blocked.')}",
        "",
        "Integration:",
        f"Layer        : {boundary.get('integration_layer', '6E-4')}",
        f"Status       : {boundary.get('integration_status', 'READY')}",
    ]

    return "\n".join(lines)


def get_predictive_execution_boundary_reports():
    """
    Generate 6E-4 execution-boundary reports for all modules.
    """
    decisions = get_predictive_action_decisions()

    return [
        get_predictive_execution_boundary_report(decision)
        for decision in decisions
    ]


# ============================================================
# STEP 6E-5 — PREDICTIVE DECISION AUDIT / TRACEABILITY
# ============================================================

def _build_6e5_trace_id(decision):
    """
    Build a deterministic trace identifier for one predictive decision.

    The trace ID is derived only from the decision content. It does not
    create persistence, execute actions, or alter the decision itself.
    """
    import hashlib
    import json

    if not isinstance(decision, dict):
        decision = {}

    trace_payload = {
        "module": decision.get("module", "Unknown Module"),
        "risk": decision.get("risk", RISK_INSUFFICIENT),
        "risk_score": decision.get("risk_score", 0),
        "action": decision.get("action", "COLLECT_DATA"),
        "priority": decision.get("priority", "LOW"),
        "safety_level": decision.get("safety_level", "ADVISORY_ONLY"),
        "execution_allowed": bool(
            decision.get("execution_allowed", False)
        ),
        "automatic_action_allowed": bool(
            decision.get("automatic_action_allowed", False)
        ),
    }

    encoded = json.dumps(
        trace_payload,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    return "6E5-" + hashlib.sha256(encoded).hexdigest()[:16].upper()


def get_predictive_decision_audit(
    decision,
    source_prediction=None,
):
    """
    Build a complete 6E-5 predictive decision audit record.

    Traceability chain:
        original prediction
        -> 6E-1 decision
        -> 6D safety
        -> 6E-4 execution boundary

    The original prediction is the authoritative source for
    input evidence and predictive assessment. The normalized
    decision remains the source for action/priority/mode, while
    safety and execution-boundary fields remain sourced from
    their validated layers.

    6E-5 is an audit/traceability layer only. It does not:
        - recalculate predictive risk
        - modify a predictive decision
        - authorize execution
        - execute or queue an action
        - persist an audit record
    """
    if not isinstance(decision, dict):
        decision = {}

    if not isinstance(source_prediction, dict):
        source_prediction = {}

    # Preserve the original prediction as the traceability source.
    module = source_prediction.get(
        "module",
        decision.get("module", "Unknown Module"),
    )

    boundary = get_predictive_execution_boundary(decision)

    trace_source = dict(decision)
    trace_source["module"] = module

    trace_id = _build_6e5_trace_id(trace_source)

    return {
        "trace_id": trace_id,
        "integration_layer": "6E-5",
        "integration_status": "READY",
        "audit_status": "COMPLETE",
        "audit_complete": True,

        # Stage 1 — original source/input context
        "input": {
            "module": module,
            "events": source_prediction.get("events", 0),
            "failed": source_prediction.get("failed", 0),
            "success_rate": source_prediction.get(
                "success_rate",
                0.0,
            ),
            "pattern": source_prediction.get(
                "pattern",
                "NO_DATA",
            ),
            "trend": source_prediction.get(
                "trend",
                "INSUFFICIENT_DATA",
            ),
            "signal_strength": source_prediction.get(
                "signal_strength",
                "NONE",
            ),
            "data_quality": source_prediction.get(
                "data_quality",
                "NO_DATA",
            ),
            "data_quality_score": source_prediction.get(
                "data_quality_score",
                0,
            ),
        },

        # Stage 2 — original predictive assessment
        "prediction": {
            "risk": source_prediction.get(
                "risk",
                decision.get("risk", RISK_INSUFFICIENT),
            ),
            "risk_score": source_prediction.get(
                "risk_score",
                decision.get("risk_score", 0),
            ),
            "confidence": source_prediction.get(
                "confidence",
                decision.get(
                    "confidence",
                    CONFIDENCE_INSUFFICIENT,
                ),
            ),
            "prediction": source_prediction.get(
                "prediction",
                "No predictive assessment is available.",
            ),
            "explanation": source_prediction.get(
                "explanation",
                "No predictive explanation is available.",
            ),
        },

        # Stage 3 — validated 6E-1 decision
        "decision": {
            "action": decision.get(
                "action",
                "COLLECT_DATA",
            ),
            "priority": decision.get(
                "priority",
                "LOW",
            ),
            "mode": decision.get(
                "mode",
                "ADVISORY",
            ),
            "status": decision.get(
                "status",
                "READY",
            ),
            "reason": decision.get(
                "reason",
                decision.get(
                    "action_reason",
                    "No predictive decision reason is available.",
                ),
            ),
        },

        # Stage 4 — 6D safety authority
        "safety": {
            "safety_level": decision.get(
                "safety_level",
                "ADVISORY_ONLY",
            ),
            "execution_allowed": False,
            "automatic_action_allowed": False,
            "reason": decision.get(
                "safety_reason",
                "Predictive recommendations are advisory only. "
                "No automatic system-changing action is permitted.",
            ),
        },

        # Stage 5 — 6E-4 hard execution boundary
        "boundary": boundary,

        # 6E-5 invariant
        "execution_allowed": False,
        "automatic_action_allowed": False,
    }


def get_predictive_decision_audits():
    """
    Generate complete 6E-5 audit records for all predictive modules.

    Each audit joins the original module prediction with its
    corresponding validated 6E-1 decision. This preserves the
    complete traceability chain instead of reconstructing source
    evidence from the normalized decision object.
    """
    predictions = get_module_predictions()
    decisions = get_predictive_action_decisions()

    audits = []

    for prediction, decision in zip(
        predictions,
        decisions,
    ):
        audits.append(
            get_predictive_decision_audit(
                decision,
                source_prediction=prediction,
            )
        )

    return audits


def get_predictive_decision_audit_report(decision):
    """
    Generate a human-readable 6E-5 audit/traceability report.

    Presentation only. No action is executed.
    """
    audit = get_predictive_decision_audit(decision)

    input_data = audit["input"]
    prediction = audit["prediction"]
    decision_data = audit["decision"]
    safety = audit["safety"]
    boundary = audit["boundary"]

    lines = [
        "🔎 HOPE Predictive Decision Audit",
        "",
        f"Trace ID     : {audit.get('trace_id', 'UNKNOWN')}",
        f"Module       : {input_data.get('module', 'Unknown Module')}",
        f"Audit Status : {audit.get('audit_status', 'INCOMPLETE')}",
        "",
        "Input:",
        f"  Events        : {input_data.get('events', 0)}",
        f"  Failures      : {input_data.get('failed', 0)}",
        f"  Success Rate  : {input_data.get('success_rate', 0.0)}%",
        f"  Pattern       : {input_data.get('pattern', 'NO_DATA')}",
        f"  Trend         : {input_data.get('trend', 'INSUFFICIENT_DATA')}",
        f"  Signal        : {input_data.get('signal_strength', 'NONE')}",
        f"  Data Quality  : {input_data.get('data_quality', 'NO_DATA')}",
        f"  Quality Score : {input_data.get('data_quality_score', 0)}/100",
        "",
        "Prediction:",
        f"  Risk         : {prediction.get('risk', RISK_INSUFFICIENT)}",
        f"  Risk Score   : {prediction.get('risk_score', 0)}/100",
        f"  Confidence   : {prediction.get('confidence', CONFIDENCE_INSUFFICIENT)}",
        f"  Assessment   : {prediction.get('prediction', 'No predictive assessment is available.')}",
        f"  Explanation  : {prediction.get('explanation', 'No predictive explanation is available.')}",
        "",
        "Decision:",
        f"  Action       : {decision_data.get('action', 'COLLECT_DATA')}",
        f"  Priority     : {decision_data.get('priority', 'LOW')}",
        f"  Mode         : {decision_data.get('mode', 'ADVISORY')}",
        f"  Status       : {decision_data.get('status', 'READY')}",
        f"  Reason       : {decision_data.get('reason', 'No predictive decision reason is available.')}",
        "",
        "Safety:",
        f"  Level        : {safety.get('safety_level', 'ADVISORY_ONLY')}",
        f"  Execution    : {safety.get('execution_allowed', False)}",
        f"  Automatic    : {safety.get('automatic_action_allowed', False)}",
        f"  Reason       : {safety.get('reason', 'Execution is blocked.')}",
        "",
        "Boundary:",
        f"  Layer        : {boundary.get('integration_layer', '6E-4')}",
        f"  Boundary     : {boundary.get('execution_boundary', 'ADVISORY_ONLY')}",
        f"  Execution    : {boundary.get('execution_allowed', False)}",
        f"  Automatic    : {boundary.get('automatic_action_allowed', False)}",
        f"  Reason       : {boundary.get('reason', 'Execution is blocked.')}",
        "",
        "Trace:",
        "  Input → Prediction → Decision → Safety → Boundary",
        "",
        "6E-5 Audit:",
        f"  Complete     : {audit.get('audit_complete', False)}",
        f"  Execution    : {audit.get('execution_allowed', False)}",
        f"  Automatic    : {audit.get('automatic_action_allowed', False)}",
    ]

    return "\n".join(lines)


def get_predictive_decision_audit_reports():
    """
    Generate 6E-5 audit/traceability reports for all modules.
    """
    decisions = get_predictive_action_decisions()

    return [
        get_predictive_decision_audit_report(decision)
        for decision in decisions
    ]

# ============================================================
# STEP 6E-6 — FULL PREDICTIVE DECISION TRACE REPORT
# ============================================================

def get_predictive_decision_trace_report(audit):
    """
    Generate a complete human-readable 6E-6 trace report.

    Traceability chain:
        input -> prediction -> decision -> safety -> boundary

    Presentation/traceability only. This function does not
    recalculate risk, modify decisions, authorize execution,
    or execute actions.
    """
    if not isinstance(audit, dict):
        audit = {}

    input_data = audit.get("input", {})
    prediction = audit.get("prediction", {})
    decision = audit.get("decision", {})
    safety = audit.get("safety", {})
    boundary = audit.get("boundary", {})

    module = input_data.get(
        "module",
        "Unknown Module",
    )

    lines = [
        "🔎 HOPE Predictive Decision Trace",
        "",
        "Trace:",
        f"Trace ID      : {audit.get('trace_id', 'UNKNOWN')}",
        f"Layer         : {audit.get('integration_layer', '6E-6')}",
        f"Status        : {audit.get('integration_status', 'READY')}",
        f"Audit Status  : {audit.get('audit_status', 'UNKNOWN')}",
        "",
        "Input:",
        f"Module        : {module}",
        f"Events        : {input_data.get('events', 0)}",
        f"Failures      : {input_data.get('failed', 0)}",
        f"Success Rate  : {input_data.get('success_rate', 0.0)}%",
        f"Pattern       : {input_data.get('pattern', 'NO_DATA')}",
        f"Trend         : {input_data.get('trend', 'INSUFFICIENT_DATA')}",
        f"Signal        : {input_data.get('signal_strength', 'NONE')}",
        f"Data Quality  : {input_data.get('data_quality', 'NO_DATA')}",
        f"Quality Score : {input_data.get('data_quality_score', 0)}/100",
        "",
        "Prediction:",
        f"Risk          : {prediction.get('risk', RISK_INSUFFICIENT)}",
        f"Risk Score    : {prediction.get('risk_score', 0)}/100",
        f"Confidence    : {prediction.get('confidence', CONFIDENCE_INSUFFICIENT)}",
        f"Assessment    : {prediction.get('prediction', 'No predictive assessment is available.')}",
        f"Explanation   : {prediction.get('explanation', 'No predictive explanation is available.')}",
        "",
        "Decision:",
        f"Action        : {decision.get('action', 'COLLECT_DATA')}",
        f"Priority      : {decision.get('priority', 'LOW')}",
        f"Mode          : {decision.get('mode', 'ADVISORY')}",
        f"Status        : {decision.get('status', 'READY')}",
        f"Reason        : {decision.get('reason', 'No predictive decision reason is available.')}",
        "",
        "Safety:",
        f"Level         : {safety.get('safety_level', 'ADVISORY_ONLY')}",
        f"Execution     : {safety.get('execution_allowed', False)}",
        f"Automatic     : {safety.get('automatic_action_allowed', False)}",
        f"Reason        : {safety.get('reason', 'No safety reason available.')}",
        "",
        "Execution Boundary:",
        f"Boundary      : {boundary.get('execution_boundary', 'ADVISORY_ONLY')}",
        f"Requested     : {boundary.get('requested_action', decision.get('action', 'COLLECT_DATA'))}",
        f"Execution     : {boundary.get('execution_allowed', False)}",
        f"Automatic     : {boundary.get('automatic_action_allowed', False)}",
        f"Reason        : {boundary.get('reason', 'No execution-boundary reason available.')}",
        "",
        "Trace Chain:",
        "Input → Prediction → Decision → Safety → Boundary",
        "",
        "6E-6 Invariant:",
        f"Execution     : {audit.get('execution_allowed', False)}",
        f"Automatic     : {audit.get('automatic_action_allowed', False)}",
    ]

    return "\n".join(lines)


def get_predictive_decision_trace_reports():
    """
    Generate complete 6E-6 trace reports for all predictive modules.

    Uses the validated 6E-5 audit records as the trace source.
    """
    audits = get_predictive_decision_audits()

    return [
        get_predictive_decision_trace_report(audit)
        for audit in audits
    ]


def get_predictive_decision_trace_regression():
    """
    Run the 6E-6 trace/report regression checks.

    Validation only. No action is executed.
    """
    audits = get_predictive_decision_audits()
    reports = [
        get_predictive_decision_trace_report(audit)
        for audit in audits
    ]

    forbidden = (
        "monitoringis",
        "predictionshould",
        "historicaldata",
        "areliable",
        "Dataquality",
        "islimited",
        "Continuemonitoring",
    )

    audits_complete = all(
        isinstance(audit, dict)
        and audit.get("audit_complete") is True
        and audit.get("audit_status") == "COMPLETE"
        for audit in audits
    )

    reports_generated = all(
        isinstance(report, str)
        and "HOPE Predictive Decision Trace" in report
        for report in reports
    )

    presentation_clean = not any(
        bad in report
        for report in reports
        for bad in forbidden
    )

    unsafe_audits = sum(
        bool(audit.get("execution_allowed", False))
        or bool(audit.get("automatic_action_allowed", False))
        for audit in audits
    )

    unsafe_boundaries = sum(
        bool(
            audit.get("boundary", {}).get(
                "execution_allowed",
                False,
            )
        )
        or bool(
            audit.get("boundary", {}).get(
                "automatic_action_allowed",
                False,
            )
        )
        for audit in audits
    )

    return {
        "integration_layer": "6E-6",
        "integration_status": "READY",
        "audits": len(audits),
        "reports": len(reports),
        "audits_complete": audits_complete,
        "reports_generated": reports_generated,
        "presentation_clean": presentation_clean,
        "unsafe_audits": unsafe_audits,
        "unsafe_boundaries": unsafe_boundaries,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "regression_passed": (
            len(audits) == len(reports)
            and len(audits) > 0
            and audits_complete
            and reports_generated
            and presentation_clean
            and unsafe_audits == 0
            and unsafe_boundaries == 0
        ),
    }
