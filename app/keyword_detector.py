"""
Keyword detection and topic extraction for StudySync AI.
Scans calendar event titles for configured trigger keywords.
"""
import os
import re
from typing import Optional
from app.logger import get_logger

logger = get_logger(__name__)


def get_keywords() -> list[str]:
    """
    Load trigger keywords from environment variable.
    Returns list of lowercase keywords.
    """
    raw = os.getenv("TRIGGER_KEYWORDS", "exam,test,ca,assessment,quiz")
    keywords = [k.strip().lower() for k in raw.split(",") if k.strip()]
    logger.info("Loaded trigger keywords", extra={"keywords": keywords})
    return keywords


def detect_keyword(event_title: str, keywords: Optional[list[str]] = None) -> Optional[str]:
    """
    Check if an event title contains a trigger keyword.
    Returns the matched keyword (lowercase) or None if no match.

    Args:
        event_title: The Google Calendar event title
        keywords: Optional list of keywords to check. Loads from env if not provided.

    Returns:
        The matched keyword string, or None
    """
    if not event_title:
        return None

    if keywords is None:
        keywords = get_keywords()

    title_lower = event_title.lower()

    for keyword in keywords:
        kw_lower = keyword.lower()
        # Use word boundary at start only so "exam" matches "examination"
        pattern = re.compile(r'\b' + re.escape(kw_lower), re.IGNORECASE)
        if pattern.search(title_lower):
            logger.info(
                "Keyword matched in event title",
                extra={"keyword": kw_lower, "event_title": event_title}
            )
            return kw_lower

    return None


def extract_topic(event_title: str, matched_keyword: str) -> str:
    """
    Extract the study topic from an event title by removing the matched keyword.

    Examples:
        "Azure Cloud Exam"  + "exam"  → "Azure Cloud"
        "CA Final Test"     + "test"  → "CA Final"
        "Data Structures"   + "exam"  → "Data Structures" (keyword not in title, return as-is)

    Args:
        event_title: The original event title
        matched_keyword: The keyword that was detected

    Returns:
        Cleaned topic string
    """
    # Remove the keyword (case-insensitive)
    pattern = re.compile(r'\b' + re.escape(matched_keyword) + r'\b', re.IGNORECASE)
    topic = pattern.sub("", event_title)

    # Clean up: remove extra spaces, hyphens, pipes that may be left
    topic = re.sub(r'[-|:]+', ' ', topic)
    topic = re.sub(r'\s+', ' ', topic).strip()

    if not topic:
        # If removing the keyword left nothing, return original title
        topic = event_title.strip()

    logger.info(
        "Topic extracted from event",
        extra={"original_title": event_title, "keyword": matched_keyword, "topic": topic}
    )

    return topic
