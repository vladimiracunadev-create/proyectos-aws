import json
from unittest.mock import MagicMock, patch

import pytest
import app


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _pub_event(method="GET", path="/", body=None, accept=None, user_agent=None, format_param=None):
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
        "body": json.dumps(body) if body is not None else None,
    }


def _sqs_event(records):
    return {"Records": [{"body": json.dumps(r)} for r in records]}


VALID_ORDER_BODY = {
    "customerId": "cust-001",
    "customerName": "Acme SPA",
    "status": "CREATED",
    "total": 249.90,
}


# ---------------------------------------------------------------------------
# Helpers (_utc_now, _wants_html)
# ---------------------------------------------------------------------------

def test_utc_now_is_iso_format():
    from datetime import datetime
    ts = app._utc_now()
    datetime.fromisoformat(ts)  # raises if not valid ISO


def test_wants_html_browser_ua():
    event = _pub_event(user_agent="Mozilla/5.0 (compatible)")
    assert app._wants_html(event) is True


def test_wants_html_accept_text_html():
    event = _pub_event(accept="text/html,application/xhtml+xml")
    assert app._wants_html(event) is True


def test_wants_html_json_accept():
    event = _pub_event(accept="application/json")
    assert app._wants_html(event) is False


def test_wants_html_force_json_param_overrides_browser():
    event = _pub_event(user_agent="Mozilla/5.0", format_param="json")
    assert app._wants_html(event) is False


# ---------------------------------------------------------------------------
# publisher_handler — GET /
# ---------------------------------------------------------------------------

def test_publisher_get_root_returns_html():
    result = app.publisher_handler(_pub_event("GET", "/"), None)
    assert result["statusCode"] == 200
    assert "text/html" in result["headers"]["Content-Type"]


# ---------------------------------------------------------------------------
# publisher_handler — GET /health
# ---------------------------------------------------------------------------

def test_publisher_get_health_json():
    result = app.publisher_handler(_pub_event("GET", "/health", accept="application/json"), None)
    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    assert body["status"] == "ok"
    assert body["service"] == "caso-g-event-driven"
    assert "eventBus" in body
    assert "timestamp" in body


def test_publisher_get_health_html():
    result = app.publisher_handler(_pub_event("GET", "/health", user_agent="Mozilla/5.0"), None)
    assert result["statusCode"] == 200
    assert "text/html" in result["headers"]["Content-Type"]


# ---------------------------------------------------------------------------
# publisher_handler — POST /events/orders
# ---------------------------------------------------------------------------

def test_publisher_missing_customer_id_returns_400():
    body = {k: v for k, v in VALID_ORDER_BODY.items() if k != "customerId"}
    result = app.publisher_handler(_pub_event("POST", "/events/orders", body=body), None)
    assert result["statusCode"] == 400
    assert "customerId" in json.loads(result["body"])["error"]


def test_publisher_invalid_json_returns_400():
    event = _pub_event("POST", "/events/orders")
    event["body"] = "not-valid-json"
    result = app.publisher_handler(event, None)
    assert result["statusCode"] == 400


def test_publisher_valid_order_returns_202():
    mock_events = MagicMock()
    mock_events.put_events.return_value = {
        "FailedEntryCount": 0,
        "Entries": [{"EventId": "evt-abc123"}],
    }

    with patch.object(app, "events_client", mock_events):
        result = app.publisher_handler(_pub_event("POST", "/events/orders", body=VALID_ORDER_BODY), None)

    assert result["statusCode"] == 202
    body = json.loads(result["body"])
    assert body["eventId"] == "evt-abc123"
    assert body["detailType"] == "OrderCreated"
    assert body["detail"]["customerId"] == "cust-001"


def test_publisher_eventbridge_failure_returns_500():
    mock_events = MagicMock()
    mock_events.put_events.return_value = {
        "FailedEntryCount": 1,
        "Entries": [{"ErrorCode": "InternalFailure"}],
    }

    with patch.object(app, "events_client", mock_events):
        result = app.publisher_handler(_pub_event("POST", "/events/orders", body=VALID_ORDER_BODY), None)

    assert result["statusCode"] == 500


def test_publisher_autogenerates_order_id():
    mock_events = MagicMock()
    mock_events.put_events.return_value = {
        "FailedEntryCount": 0,
        "Entries": [{"EventId": "evt-generated"}],
    }
    body = {k: v for k, v in VALID_ORDER_BODY.items() if k != "orderId"}

    with patch.object(app, "events_client", mock_events):
        result = app.publisher_handler(_pub_event("POST", "/events/orders", body=body), None)

    assert result["statusCode"] == 202
    detail = json.loads(result["body"])["detail"]
    assert detail["orderId"].startswith("ord-")


# ---------------------------------------------------------------------------
# consumer_handler
# ---------------------------------------------------------------------------

def _detail(order_id="ord-001", customer_id="cust-001", force_failure=False):
    return {
        "orderId": order_id,
        "customerId": customer_id,
        "status": "CREATED",
        "forceFailure": force_failure,
    }


def test_consumer_processes_single_record():
    mock_sns = MagicMock()

    with patch.object(app, "sns_client", mock_sns), \
         patch.object(app, "NOTIFICATIONS_TOPIC_ARN", "arn:aws:sns:us-east-2:123456:test-topic"):
        result = app.consumer_handler(_sqs_event([{"detail": _detail()}]), None)

    assert result["count"] == 1
    assert result["processed"][0]["status"] == "PROCESSED"
    assert result["processed"][0]["orderId"] == "ord-001"
    mock_sns.publish.assert_called_once()


def test_consumer_skips_sns_when_no_topic():
    mock_sns = MagicMock()

    with patch.object(app, "sns_client", mock_sns), \
         patch.object(app, "NOTIFICATIONS_TOPIC_ARN", ""):
        result = app.consumer_handler(_sqs_event([{"detail": _detail()}]), None)

    assert result["count"] == 1
    mock_sns.publish.assert_not_called()


def test_consumer_multiple_records():
    with patch.object(app, "NOTIFICATIONS_TOPIC_ARN", ""):
        result = app.consumer_handler(
            _sqs_event([{"detail": _detail("ord-1")}, {"detail": _detail("ord-2")}]),
            None,
        )
    assert result["count"] == 2


def test_consumer_force_failure_raises():
    with pytest.raises(RuntimeError):
        app.consumer_handler(_sqs_event([{"detail": _detail(force_failure=True)}]), None)


def test_consumer_detail_as_string_is_parsed():
    record = {"detail": json.dumps(_detail("ord-str"))}
    with patch.object(app, "NOTIFICATIONS_TOPIC_ARN", ""):
        result = app.consumer_handler(_sqs_event([record]), None)
    assert result["processed"][0]["orderId"] == "ord-str"
