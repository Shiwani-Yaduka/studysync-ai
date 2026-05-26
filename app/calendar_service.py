"""
Google Calendar API integration for StudySync AI.
Uses a Service Account for server-side authentication.
"""
import os
import json
from datetime import datetime, timedelta, timezone
from typing import Optional
from googleapiclient.discovery import build
from google.oauth2 import service_account
from app.logger import get_logger

logger = get_logger(__name__)

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def get_calendar_client():
    """
    Build an authenticated Google Calendar API client.
    Credentials are loaded from the GOOGLE_CREDENTIALS_JSON environment variable.

    Returns:
        Google Calendar API service object

    Raises:
        ValueError: If GOOGLE_CREDENTIALS_JSON is not set or invalid
    """
    credentials_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
    if not credentials_json:
        raise ValueError(
            "GOOGLE_CREDENTIALS_JSON environment variable is not set. "
            "Set it to the contents of your service account JSON file."
        )

    try:
        credentials_dict = json.loads(credentials_json)
    except json.JSONDecodeError as e:
        raise ValueError(f"GOOGLE_CREDENTIALS_JSON is not valid JSON: {e}")

    credentials = service_account.Credentials.from_service_account_info(
        credentials_dict,
        scopes=SCOPES
    )

    service = build("calendar", "v3", credentials=credentials, cache_discovery=False)
    logger.info("Google Calendar client initialized successfully")
    return service


def get_events_in_n_days(days_ahead: Optional[int] = None) -> list[dict]:
    """
    Fetch Google Calendar events occurring exactly N days from today.

    The time window is midnight to midnight on the target date
    in the configured timezone.

    Args:
        days_ahead: Number of days ahead to look. Defaults to DAYS_AHEAD env var (7).

    Returns:
        List of event dicts from Google Calendar API
    """
    if days_ahead is None:
        days_ahead = int(os.getenv("DAYS_AHEAD", "7"))

    calendar_id = os.getenv("GOOGLE_CALENDAR_ID")
    if not calendar_id:
        raise ValueError("GOOGLE_CALENDAR_ID environment variable is not set")

    # Calculate the target date window
    now = datetime.now(timezone.utc)
    target_date = now + timedelta(days=days_ahead)

    # Start of target day (midnight UTC)
    time_min = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
    # End of target day (23:59:59 UTC)
    time_max = target_date.replace(hour=23, minute=59, second=59, microsecond=0)

    logger.info(
        "Querying Google Calendar",
        extra={
            "calendar_id": calendar_id,
            "days_ahead": days_ahead,
            "time_min": time_min.isoformat(),
            "time_max": time_max.isoformat(),
        }
    )

    try:
        service = get_calendar_client()
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=time_min.isoformat(),
            timeMax=time_max.isoformat(),
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        events = events_result.get("items", [])

        logger.info(
            "Calendar query complete",
            extra={"events_found": len(events), "days_ahead": days_ahead}
        )

        return events

    except Exception as e:
        logger.error(
            "Failed to query Google Calendar",
            extra={"error": str(e), "error_type": type(e).__name__}
        )
        raise
