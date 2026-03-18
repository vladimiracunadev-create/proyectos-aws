import json
from unittest.mock import MagicMock, patch

import app


def _event(method="POST", body=None):
    return {
        "requestContext": {
            "http": {"method": method, "sourceIp": "1.2.3.4", "userAgent": "pytest"}
        },
        "body": json.dumps(body) if body is not None else None,
    }


# ---------------------------------------------------------------------------
# OPTIONS
# ---------------------------------------------------------------------------

def test_options_returns_200():
    result = app.handler(_event("OPTIONS"), None)
    assert result["statusCode"] == 200
    assert json.loads(result["body"])["ok"] is True


# ---------------------------------------------------------------------------
# Method guard
# ---------------------------------------------------------------------------

def test_non_post_returns_405():
    result = app.handler(_event("GET"), None)
    assert result["statusCode"] == 405


def test_delete_returns_405():
    result = app.handler(_event("DELETE"), None)
    assert result["statusCode"] == 405


# ---------------------------------------------------------------------------
# JSON parsing
# ---------------------------------------------------------------------------

def test_invalid_json_returns_400():
    event = _event("POST")
    event["body"] = "not-valid-json"
    result = app.handler(event, None)
    assert result["statusCode"] == 400
    assert "JSON" in json.loads(result["body"])["error"]


# ---------------------------------------------------------------------------
# Honeypot
# ---------------------------------------------------------------------------

def test_honeypot_company_field_returns_200_ignored():
    result = app.handler(_event("POST", {"company": "Spammer Inc", "name": "x", "email": "x@x.com", "message": "hi"}), None)
    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    assert body["id"] == "ignored"


# ---------------------------------------------------------------------------
# Field validation
# ---------------------------------------------------------------------------

def test_missing_all_fields_returns_400():
    result = app.handler(_event("POST", {}), None)
    assert result["statusCode"] == 400


def test_missing_message_returns_400():
    result = app.handler(_event("POST", {"name": "Ana", "email": "a@b.com"}), None)
    assert result["statusCode"] == 400


def test_name_too_long_returns_400():
    result = app.handler(_event("POST", {"name": "x" * 121, "email": "a@b.com", "message": "hola"}), None)
    assert result["statusCode"] == 400


def test_email_too_long_returns_400():
    result = app.handler(_event("POST", {"name": "Ana", "email": "a" * 181, "message": "hola"}), None)
    assert result["statusCode"] == 400


def test_message_too_long_returns_400():
    result = app.handler(_event("POST", {"name": "Ana", "email": "a@b.com", "message": "x" * 2001}), None)
    assert result["statusCode"] == 400


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------

def test_valid_lead_writes_dynamo_and_returns_200():
    mock_table = MagicMock()

    with patch.object(app, "TABLE", mock_table):
        result = app.handler(
            _event("POST", {"name": "Ana", "email": "ana@test.com", "message": "Hola desde pytest"}),
            None,
        )

    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    assert body["ok"] is True
    assert "id" in body

    mock_table.put_item.assert_called_once()
    item = mock_table.put_item.call_args[1]["Item"]
    assert item["pk"] == "LEAD"
    assert item["name"] == "Ana"
    assert item["email"] == "ana@test.com"


def test_valid_lead_trims_whitespace():
    mock_table = MagicMock()

    with patch.object(app, "TABLE", mock_table):
        result = app.handler(
            _event("POST", {"name": "  Ana  ", "email": "  ana@test.com  ", "message": "  mensaje  "}),
            None,
        )

    assert result["statusCode"] == 200
    item = mock_table.put_item.call_args[1]["Item"]
    assert item["name"] == "Ana"
    assert item["email"] == "ana@test.com"
    assert item["message"] == "mensaje"
