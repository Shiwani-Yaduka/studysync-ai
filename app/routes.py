"""
Flask routes for StudySync AI.

Endpoints:
  GET  /health    → Kubernetes liveness/readiness probe
  POST /trigger   → Manually trigger the study guide pipeline (token-protected)
"""
import os
from flask import Blueprint, jsonify, request
from datetime import datetime, timezone
from app.logger import get_logger

logger = get_logger(__name__)
bp = Blueprint("main", __name__)


@bp.route("/health", methods=["GET"])
def health():
    """
    Health check endpoint.
    Used by Kubernetes liveness and readiness probes.
    Returns 200 if the app is running correctly.
    """
    return jsonify({
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "studysync-ai",
        "version": "1.0.0"
    }), 200


@bp.route("/trigger", methods=["POST"])
def trigger():
    """
    Manually trigger the calendar poll and study guide pipeline.
    Protected by a bearer token to prevent unauthorized triggering.

    Usage:
      curl -X POST http://localhost:5000/trigger \
           -H "Authorization: Bearer YOUR_TOKEN"
    """
    # Verify bearer token
    expected_token = os.getenv("TRIGGER_SECRET_TOKEN")
    if not expected_token:
        logger.error("TRIGGER_SECRET_TOKEN not configured")
        return jsonify({"error": "Server misconfiguration"}), 500

    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        logger.warning("Trigger endpoint called without Bearer token")
        return jsonify({"error": "Authorization header required. Format: Bearer <token>"}), 401

    token = auth_header.split(" ", 1)[1]
    if token != expected_token:
        logger.warning("Trigger endpoint called with invalid token")
        return jsonify({"error": "Invalid token"}), 403

    logger.info("Manual trigger received via /trigger endpoint")

    # Import here to avoid circular imports
    from app.scheduler import run_pipeline

    try:
        result = run_pipeline()
        return jsonify({
            "status": "success",
            "message": "Pipeline executed",
            "result": result
        }), 200
    except Exception as e:
        logger.error("Pipeline failed during manual trigger", extra={"error": str(e)})
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@bp.route("/events", methods=["GET"])
def get_events():
    from app.calendar_service import get_events_in_n_days

    try:
        events = get_events_in_n_days()

        formatted = []

        for event in events:
            formatted.append({
                "title": event.get("summary", "No Title"),
                "start": event.get("start", {}),
            })

        return jsonify(formatted), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route("/generate", methods=["POST"])
def generate():
    data = request.json
    topic = data.get("topic")

    if not topic:
        return jsonify({"error": "Topic required"}), 400

    try:
        from app.ai_agent import generate_study_guide

        guide = generate_study_guide(topic)

        return jsonify({
            "topic": topic,
            "guide": guide
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500