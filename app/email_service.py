"""
Email delivery service for StudySync AI.
Converts Markdown study guides to HTML and delivers via SendGrid.
"""
import os
import markdown as md
from datetime import datetime, timezone
from prometheus_client import Counter
from app.logger import get_logger

logger = get_logger(__name__)

# ── Prometheus Metrics ────────────────────────────────────────────────────────
emails_sent_total = Counter(
    "studysync_emails_sent_total",
    "Total study guide emails sent",
    ["status"]  # success | failure
)


def _markdown_to_html(markdown_text: str) -> str:
    """
    Convert Markdown to HTML with styling.
    Wraps output in a simple inline-styled HTML email body.
    """
    html_body = md.markdown(
        markdown_text,
        extensions=["tables", "fenced_code", "nl2br"]
    )

    # Wrap in a simple, email-client-compatible HTML template
    html = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
             max-width: 680px; margin: 0 auto; padding: 20px; color: #1a1a2e;">

  <div style="background: linear-gradient(135deg, #1B2A4A 0%, #2563EB 100%);
              padding: 24px 32px; border-radius: 12px 12px 0 0; margin-bottom: 0;">
    <h1 style="color: #ffffff; margin: 0; font-size: 22px;">📚 StudySync AI</h1>
    <p style="color: #93C5FD; margin: 4px 0 0; font-size: 14px;">
      Your personalised study guide is ready
    </p>
  </div>

  <div style="background: #ffffff; padding: 32px; border: 1px solid #e5e7eb;
              border-top: none; border-radius: 0 0 12px 12px;">
    {html_body}
  </div>

  <p style="text-align: center; color: #9ca3af; font-size: 12px; margin-top: 16px;">
    Generated automatically by StudySync AI &nbsp;·&nbsp;
    {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}
  </p>
</body>
</html>
"""
    return html


def send_study_guide_email(topic: str, guide: str, event_date: str = "") -> bool:
    """
    Send the study guide to the configured recipient email.

    Args:
        topic: The exam topic (used in subject line)
        guide: Markdown-formatted study guide
        event_date: ISO date string of the exam (for subject line)

    Returns:
        True if sent successfully, False otherwise
    """
    import sendgrid
    from sendgrid.helpers.mail import Mail, Email, To, Content

    api_key = os.getenv("SENDGRID_API_KEY")
    recipient = os.getenv("RECIPIENT_EMAIL")
    sender = os.getenv("SENDER_EMAIL")

    if not all([api_key, recipient, sender]):
        raise ValueError(
            "Missing email configuration. Ensure SENDGRID_API_KEY, "
            "RECIPIENT_EMAIL, and SENDER_EMAIL are set."
        )

    # Format the date for the subject line
    try:
        from datetime import datetime as dt
        date_str = dt.fromisoformat(event_date.replace("Z", "+00:00")).strftime("%b %d, %Y")
    except Exception:
        date_str = event_date or "upcoming"

    subject = f"📚 StudySync: 7-Day Prep Guide — {topic} ({date_str})"

    html_content = _markdown_to_html(guide)

    message = Mail(
        from_email=Email(sender, "StudySync AI"),
        to_emails=To(recipient),
        subject=subject,
        html_content=Content("text/html", html_content),
    )

    # Also attach plain text version (good email practice)
    message.add_content(Content("text/plain", guide))

    try:
        sg = sendgrid.SendGridAPIClient(api_key=api_key)
        response = sg.send(message)

        if response.status_code in (200, 202):
            emails_sent_total.labels(status="success").inc()
            logger.info(
                "Study guide email sent",
                extra={
                    "recipient": recipient,
                    "topic": topic,
                    "subject": subject,
                    "status_code": response.status_code
                }
            )
            return True
        else:
            emails_sent_total.labels(status="failure").inc()
            logger.error(
                "SendGrid returned unexpected status",
                extra={"status_code": response.status_code, "body": response.body}
            )
            return False

    except Exception as e:
        emails_sent_total.labels(status="failure").inc()
        logger.error(
            "Failed to send email",
            extra={"error": str(e), "topic": topic}
        )
        raise
