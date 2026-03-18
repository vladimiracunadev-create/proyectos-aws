import json
from datetime import datetime
from unittest.mock import MagicMock, patch

import app


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _event(method="GET", path="/", accept=None, user_agent=None, format_param=None):
    headers = {}
    if accept:
        headers["accept"] = accept
    if user_agent:
        headers["user-agent"] = user_agent
    qsp = {}
    if format_param:
        qsp["format"] = format_param
    return {
        "requestContext": {"http": {"method": method}},
        "rawPath": path,
        "headers": headers,
        "queryStringParameters": qsp,
    }


# ---------------------------------------------------------------------------
# _utc_now
# ---------------------------------------------------------------------------

def test_utc_now_is_valid_iso():
    ts = app._utc_now()
    datetime.fromisoformat(ts)  # raises ValueError if invalid


# ---------------------------------------------------------------------------
# _wants_html
# ---------------------------------------------------------------------------

def test_wants_html_browser_ua():
    assert app._wants_html(_event(user_agent="Mozilla/5.0 (Windows NT 10.0)")) is True


def test_wants_html_accept_header():
    assert app._wants_html(_event(accept="text/html,application/xhtml+xml")) is True


def test_wants_html_json_accept_returns_false():
    assert app._wants_html(_event(accept="application/json")) is False


def test_wants_html_force_json_param_overrides_browser():
    assert app._wants_html(_event(user_agent="Mozilla/5.0", format_param="json")) is False


# ---------------------------------------------------------------------------
# _health_payload
# ---------------------------------------------------------------------------

def test_health_payload_structure():
    payload = app._health_payload()
    assert payload["status"] == "ok"
    assert payload["xray"] == "active"
    assert payload["metricNamespace"] == "CasoH"
    assert "service" in payload
    assert "timestamp" in payload
    datetime.fromisoformat(payload["timestamp"])


# ---------------------------------------------------------------------------
# handler — GET / (landing)
# ---------------------------------------------------------------------------

def test_handler_root_returns_html():
    result = app.handler(_event("GET", "/"), None)
    assert result["statusCode"] == 200
    assert "text/html" in result["headers"]["Content-Type"]


def test_handler_empty_path_returns_html():
    result = app.handler(_event("GET", ""), None)
    assert result["statusCode"] == 200
    assert "text/html" in result["headers"]["Content-Type"]


# ---------------------------------------------------------------------------
# handler — GET /health
# ---------------------------------------------------------------------------

def test_handler_health_json():
    result = app.handler(_event("GET", "/health", accept="application/json"), None)
    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    assert body["status"] == "ok"
    assert body["xray"] == "active"
    assert body["metricNamespace"] == "CasoH"


def test_handler_health_html_for_browser():
    result = app.handler(_event("GET", "/health", user_agent="Mozilla/5.0"), None)
    assert result["statusCode"] == 200
    assert "text/html" in result["headers"]["Content-Type"]


# ---------------------------------------------------------------------------
# handler — POST /metrics
# ---------------------------------------------------------------------------

def test_handler_post_metrics_success():
    mock_cw = MagicMock()

    with patch.object(app, "cloudwatch", mock_cw):
        result = app.handler(_event("POST", "/metrics"), None)

    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    assert body["namespace"] == "CasoH"
    assert body["metricName"] == "HealthChecks"
    mock_cw.put_metric_data.assert_called_once()

    call_kwargs = mock_cw.put_metric_data.call_args[1]
    assert call_kwargs["Namespace"] == "CasoH"
    assert call_kwargs["MetricData"][0]["MetricName"] == "HealthChecks"
    assert call_kwargs["MetricData"][0]["Value"] == 1


def test_handler_post_metrics_cloudwatch_error_returns_500():
    mock_cw = MagicMock()
    mock_cw.put_metric_data.side_effect = Exception("CloudWatch simulated failure")

    with patch.object(app, "cloudwatch", mock_cw):
        result = app.handler(_event("POST", "/metrics"), None)

    assert result["statusCode"] == 500
    body = json.loads(result["body"])
    assert "error" in body
    assert "detail" in body


# ---------------------------------------------------------------------------
# handler — unknown route
# ---------------------------------------------------------------------------

def test_handler_unknown_route_returns_404():
    result = app.handler(_event("GET", "/ruta-desconocida"), None)
    assert result["statusCode"] == 404
    body = json.loads(result["body"])
    assert "availableRoutes" in body


def test_handler_metrics_get_returns_404():
    result = app.handler(_event("GET", "/metrics"), None)
    assert result["statusCode"] == 404
