"""
APScheduler integration for StudySync AI.
Runs the calendar poll job on a daily schedule.
"""
import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from prometheus_client import Counter
from app.logger import get_logger
from app.calendar_service import get_events_in_n_days
from app.keyword_detector import detect_keyword, extract_topic, get_keywords

logger = get_logger(__name__)

# ── Prometheus Metrics ────────────────────────────────────────────────────────
polls_total = Counter(
    "studysync_polls_total",
    "Total number of calendar poll executions",
    ["status"]  # success | failure
)
events_found_total = Counter(
    "studysync_events_found_total",
    "Total calendar events matching keywords"
)

_scheduler = None


def run_pipeline() -> dict:
    """
    The core StudySync pipeline:
    1. Fetch calendar events N days ahead
    2. Check each event for trigger keywords
    3. For each match, run the AI agent and send email

    Returns:
        Dict with pipeline execution summary
    """
    logger.info("StudySync pipeline starting")
    results = {
        "events_checked": 0,
        "keyword_matches": [],
        "guides_sent": 0,
        "errors": []
    }

    try:
        events = get_events_in_n_days()
        results["events_checked"] = len(events)
        keywords = get_keywords()

        for event in events:
            title = event.get("summary", "")
            start = event.get("start", {}).get("dateTime") or event.get("start", {}).get("date", "")

            matched_keyword = detect_keyword(title, keywords)
            if not matched_keyword:
                continue

            topic = extract_topic(title, matched_keyword)
            events_found_total.inc()
            results["keyword_matches"].append({
                "title": title,
                "keyword": matched_keyword,
                "topic": topic,
                "event_date": start
            })

            logger.info(
                "Keyword match found — starting AI pipeline",
                extra={"topic": topic, "event_date": start}
            )

            # Phase 3 hook: AI agent and email (filled in later)
            try:
                from app.ai_agent import generate_study_guide
                from app.email_service import send_study_guide_email
                guide = generate_study_guide(topic)
                send_study_guide_email(topic=topic, guide=guide, event_date=start)
                results["guides_sent"] += 1
            except ImportError:
                # AI agent not yet implemented — log and continue
                logger.warning(
                    "AI agent not yet implemented — skipping email",
                    extra={"topic": topic}
                )
            except Exception as e:
                error_msg = f"Failed to generate/send guide for '{topic}': {e}"
                logger.error(error_msg)
                results["errors"].append(error_msg)

        polls_total.labels(status="success").inc()
        logger.info("Pipeline completed successfully", extra={"summary": results})
        return results

    except Exception as e:
        polls_total.labels(status="failure").inc()
        logger.error("Pipeline failed", extra={"error": str(e)})
        raise


def start_scheduler(app):
    """
    Start the background scheduler attached to the Flask app.
    Fires run_pipeline() daily at the configured hour.
    """
    global _scheduler

    hour = int(os.getenv("SCHEDULER_HOUR", "8"))
    minute = int(os.getenv("SCHEDULER_MINUTE", "0"))
    # hour = None
    # minute = "*/1"

    timezone_str = os.getenv("TIMEZONE", "Asia/Kolkata")

    _scheduler = BackgroundScheduler(timezone=timezone_str)
    _scheduler.add_job(
        func=run_pipeline,
        # trigger=CronTrigger(hour=hour, minute=minute, timezone=timezone_str),
        trigger=CronTrigger(minute=minute, timezone=timezone_str),
        id="daily_calendar_poll",
        name="Daily calendar poll",
        replace_existing=True,
        misfire_grace_time=3600  # If missed, still run if within 1 hour
    )
    _scheduler.start()

    logger.info(
        "Scheduler started",
        extra={"hour": hour, "minute": minute, "timezone": timezone_str}
    )
    return _scheduler


def stop_scheduler():
    """Gracefully stop the scheduler."""
    # global _scheduler
    if _scheduler and _scheduler.running:
        _scheduler.shutdown(wait=False)
        logger.info("Scheduler stopped")
