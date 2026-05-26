"""
AI Research Agent for StudySync AI.
Searches the web via Tavily, then synthesises results via Gemini into a study guide.
"""
import os
import time
from datetime import datetime, timezone
from jinja2 import Environment, FileSystemLoader, select_autoescape
from prometheus_client import Counter, Histogram
from app.logger import get_logger

logger = get_logger(__name__)

# ── Prometheus Metrics ────────────────────────────────────────────────────────
ai_requests_total = Counter(
    "studysync_ai_requests_total",
    "Total AI agent API calls",
    ["status"]  # success | failure | rate_limited
)
ai_duration_seconds = Histogram(
    "studysync_ai_duration_seconds",
    "AI agent end-to-end duration in seconds",
    buckets=[1, 5, 10, 20, 30, 60, 120]
)

# ── Jinja2 Template Environment ───────────────────────────────────────────────
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = Environment(
    loader=FileSystemLoader(template_dir),
    autoescape=select_autoescape([])  # No HTML escaping for Markdown output
)


def _search_web(topic: str, num_results: int = 5) -> list[dict]:
    """
    Search the web for study resources using Tavily API.

    Args:
        topic: The exam topic to search for
        num_results: Number of results to retrieve

    Returns:
        List of result dicts with keys: title, url, content
    """
    from tavily import TavilyClient

    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("TAVILY_API_KEY environment variable not set")

    client = TavilyClient(api_key=api_key)
    query = f"{topic} study guide documentation best resources tutorial"

    logger.info("Searching web", extra={"query": query})

    response = client.search(
        query=query,
        max_results=num_results,
        search_depth="advanced"
    )

    results = response.get("results", [])
    logger.info("Web search complete", extra={"results_count": len(results)})
    return results


def _call_gemini(prompt: str, max_retries: int = 3) -> str:
    """
    Call Gemini API to generate the study guide.
    Implements exponential backoff for rate limit errors.

    Args:
        prompt: The full synthesis prompt
        max_retries: Maximum retry attempts on rate limit errors

    Returns:
        Generated Markdown text
    """
    import google.generativeai as genai

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")  # Fast, generous free tier

    for attempt in range(max_retries):
        try:
            logger.info("Calling Gemini API", extra={"attempt": attempt + 1})
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,      # Low temperature for factual, consistent output
                    max_output_tokens=1500,
                )
            )
            return response.text

        except Exception as e:
            error_str = str(e).lower()
            if "429" in error_str or "rate" in error_str or "quota" in error_str:
                ai_requests_total.labels(status="rate_limited").inc()
                wait_seconds = (2 ** attempt) * 5  # 5s, 10s, 20s
                logger.warning(
                    "Gemini rate limited — retrying",
                    extra={"attempt": attempt + 1, "wait_seconds": wait_seconds}
                )
                time.sleep(wait_seconds)
            else:
                raise

    raise RuntimeError(f"Gemini API failed after {max_retries} attempts")


def generate_study_guide(topic: str, event_date: str = "") -> str:
    """
    Main entry point: generate a complete Markdown study guide for a topic.

    Steps:
    1. Search the web for study resources
    2. Render the synthesis prompt using the Jinja2 template
    3. Call Gemini to produce the Markdown study guide

    Args:
        topic: The exam topic (e.g., "Azure Cloud")
        event_date: ISO string of the exam date (for display in the guide)

    Returns:
        Markdown-formatted study guide string

    Raises:
        Exception: If web search or AI synthesis fails after retries
    """
    start_time = time.time()

    try:
        # Step 1: Web search
        search_results = _search_web(topic)

        # Step 2: Render prompt template
        template = jinja_env.get_template("study_guide_prompt.j2")
        days_ahead = int(os.getenv("DAYS_AHEAD", "7"))
        prompt = template.render(
            topic=topic,
            search_results=search_results,
            event_date=event_date,
            days_ahead=days_ahead,
            generated_at=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        )

        # Step 3: Generate with Gemini
        guide = _call_gemini(prompt)

        duration = time.time() - start_time
        ai_duration_seconds.observe(duration)
        ai_requests_total.labels(status="success").inc()

        logger.info(
            "Study guide generated successfully",
            extra={
                "topic": topic,
                "duration_seconds": round(duration, 2),
                "guide_length": len(guide),
            },
        )

        return guide

    except Exception as e:
        duration = time.time() - start_time
        ai_duration_seconds.observe(duration)
        ai_requests_total.labels(status="failure").inc()

        logger.error(
            "Study guide generation failed",
            extra={"topic": topic, "error": str(e), "duration_seconds": round(duration, 2)}
        )
        raise
