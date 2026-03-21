"""Tests unitarios para Caso F: Security First (Cognito + JWT + WAF)."""
import json
from unittest.mock import MagicMock, patch

import pytest

import app


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _make_event(method="GET", path="/", body=None, claims=None, api_version="v2"):
    if api_version == "v1":
        event = {
            "httpMethod": method,
            "path": path,
            "requestContext": {},
            "body": json.dumps(body) if body is not None else None,
        }
        if claims is not None:
            event["requestContext"]["authorizer"] = {"claims": claims}
        return event

    event = {
        "requestContext": {
            "http": {"method": method}
        },
        "rawPath": path,
        "body": json.dumps(body) if body is not None else None,
    }
    if claims is not None:
        event["requestContext"]["authorizer"] = {"jwt": {"claims": claims}}
    return event


def _mock_cognito():
    return MagicMock()


# ---------------------------------------------------------------------------
# _utc_now
# ---------------------------------------------------------------------------

def test_utc_now_returns_iso_string():
    ts = app._utc_now()
    assert "T" in ts
    assert ts.endswith("+00:00")


# ---------------------------------------------------------------------------
# _load_body
# ---------------------------------------------------------------------------

def test_load_body_parses_json():
    event = {"body": '{"email": "a@b.com"}'}
    data = app._load_body(event)
    assert data["email"] == "a@b.com"


def test_load_body_empty_body_returns_empty_dict():
    event = {"body": None}
    data = app._load_body(event)
    assert data == {}


def test_load_body_invalid_json_raises_value_error():
    event = {"body": "not-json"}
    with pytest.raises(ValueError, match="JSON"):
        app._load_body(event)


# ---------------------------------------------------------------------------
# _require_fields
# ---------------------------------------------------------------------------

def test_require_fields_ok():
    app._require_fields({"email": "a@b.com", "password": "Abc12345"}, ["email", "password"])


def test_require_fields_missing_raises():
    with pytest.raises(ValueError, match="email"):
        app._require_fields({"password": "x"}, ["email", "password"])


def test_require_fields_empty_string_raises():
    with pytest.raises(ValueError, match="email"):
        app._require_fields({"email": "   ", "password": "x"}, ["email", "password"])


# ---------------------------------------------------------------------------
# _cognito_error_response
# ---------------------------------------------------------------------------

def _make_client_error(code):
    from botocore.exceptions import ClientError
    return ClientError({"Error": {"Code": code, "Message": code}}, "operation")


@pytest.mark.parametrize("code,expected_status", [
    ("UsernameExistsException", 409),
    ("NotAuthorizedException", 401),
    ("UserNotConfirmedException", 403),
    ("InvalidPasswordException", 400),
    ("UserNotFoundException", 404),
    ("TooManyRequestsException", 429),
    ("LimitExceededException", 429),
    ("InvalidParameterException", 400),
    ("UnknownException", 500),
])
def test_cognito_error_response(code, expected_status):
    exc = _make_client_error(code)
    response = app._cognito_error_response(exc)
    assert response["statusCode"] == expected_status
    body = json.loads(response["body"])
    assert body["ok"] is False
    assert "error" in body


# ---------------------------------------------------------------------------
# handle_register
# ---------------------------------------------------------------------------

def test_handle_register_success():
    mock_cog = _mock_cognito()
    mock_cog.sign_up.return_value = {"UserSub": "abc-123", "UserConfirmed": True}

    with patch.object(app, "cognito_client", mock_cog):
        event = _make_event("POST", "/auth/register", body={"email": "user@test.com", "password": "Pass1234"})
        response = app.handle_register(event)

    assert response["statusCode"] == 201
    body = json.loads(response["body"])
    assert body["ok"] is True
    assert body["userSub"] == "abc-123"
    mock_cog.sign_up.assert_called_once()


def test_handle_register_missing_email_returns_400():
    # Errors propagate through handler() — call via router
    event = _make_event("POST", "/auth/register", body={"password": "Pass1234"})
    response = app.handler(event, None)
    assert response["statusCode"] == 400
    assert json.loads(response["body"])["ok"] is False


def test_handle_register_missing_password_returns_400():
    event = _make_event("POST", "/auth/register", body={"email": "u@test.com"})
    response = app.handler(event, None)
    assert response["statusCode"] == 400


def test_handle_register_cognito_error_username_exists():
    mock_cog = _mock_cognito()
    mock_cog.sign_up.side_effect = _make_client_error("UsernameExistsException")

    with patch.object(app, "cognito_client", mock_cog):
        event = _make_event("POST", "/auth/register", body={"email": "u@test.com", "password": "Pass1234"})
        response = app.handler(event, None)

    assert response["statusCode"] == 409


# ---------------------------------------------------------------------------
# handle_login
# ---------------------------------------------------------------------------

def test_handle_login_success():
    mock_cog = _mock_cognito()
    mock_cog.initiate_auth.return_value = {
        "AuthenticationResult": {
            "AccessToken": "access-token-value",
            "IdToken": "id-token-value",
            "RefreshToken": "refresh-token-value",
            "TokenType": "Bearer",
            "ExpiresIn": 3600,
        }
    }

    with patch.object(app, "cognito_client", mock_cog):
        event = _make_event("POST", "/auth/login", body={"email": "user@test.com", "password": "Pass1234"})
        response = app.handle_login(event)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["ok"] is True
    assert body["accessToken"] == "access-token-value"
    assert body["tokenType"] == "Bearer"


def test_handle_login_missing_fields_returns_400():
    # Errors propagate through handler() — call via router
    event = _make_event("POST", "/auth/login", body={"email": "u@test.com"})
    response = app.handler(event, None)
    assert response["statusCode"] == 400


def test_handle_login_wrong_credentials():
    mock_cog = _mock_cognito()
    mock_cog.initiate_auth.side_effect = _make_client_error("NotAuthorizedException")

    with patch.object(app, "cognito_client", mock_cog):
        event = _make_event("POST", "/auth/login", body={"email": "u@test.com", "password": "wrong"})
        response = app.handler(event, None)

    assert response["statusCode"] == 401


# ---------------------------------------------------------------------------
# handle_profile
# ---------------------------------------------------------------------------

def test_handle_profile_with_valid_claims():
    claims = {"sub": "abc-123", "email": "user@test.com", "name": "Test User", "email_verified": "true"}
    event = _make_event("GET", "/profile", claims=claims)
    response = app.handle_profile(event)
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["ok"] is True
    assert body["email"] == "user@test.com"
    assert body["sub"] == "abc-123"
    assert body["emailVerified"] is True


def test_handle_profile_with_rest_api_claims():
    claims = {"sub": "rest-123", "email": "rest@test.com", "name": "REST User", "email_verified": "true"}
    event = _make_event("GET", "/profile", claims=claims, api_version="v1")
    response = app.handle_profile(event)
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["ok"] is True
    assert body["email"] == "rest@test.com"
    assert body["emailVerified"] is True


def test_handle_profile_no_claims_returns_401():
    event = _make_event("GET", "/profile")
    response = app.handle_profile(event)
    assert response["statusCode"] == 401
    assert json.loads(response["body"])["ok"] is False


def test_handle_profile_empty_claims_returns_401():
    event = _make_event("GET", "/profile", claims={})
    response = app.handle_profile(event)
    assert response["statusCode"] == 401


# ---------------------------------------------------------------------------
# handle_health
# ---------------------------------------------------------------------------

def test_handle_health_configured():
    with patch.dict("os.environ", {"COGNITO_USER_POOL_ID": "us-east-2_ABC123"}):
        import importlib
        importlib.reload(app)
        event = _make_event("GET", "/health")
        response = app.handle_health(event)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["status"] == "ok"
    assert body["cognito"] == "configured"
    assert "deploymentMode" in body
    assert "perimeterMode" in body

    # Reload without env for subsequent tests
    import importlib
    importlib.reload(app)


def test_handle_health_not_configured():
    with patch.dict("os.environ", {}, clear=True):
        if "COGNITO_USER_POOL_ID" in __import__("os").environ:
            del __import__("os").environ["COGNITO_USER_POOL_ID"]
        event = _make_event("GET", "/health")
        response = app.handle_health(event)

    assert response["statusCode"] == 200
    assert json.loads(response["body"])["service"] == "caso-f-security"


# ---------------------------------------------------------------------------
# pre_signup_trigger
# ---------------------------------------------------------------------------

def test_pre_signup_trigger_auto_confirms():
    event = {"response": {}}
    result = app.pre_signup_trigger(event, None)
    assert result["response"]["autoConfirmUser"] is True
    assert result["response"]["autoVerifyEmail"] is True


# ---------------------------------------------------------------------------
# handler routing
# ---------------------------------------------------------------------------

def test_handler_options_returns_200():
    event = _make_event("OPTIONS", "/auth/register")
    response = app.handler(event, None)
    assert response["statusCode"] == 200


def test_handler_root_returns_html():
    event = _make_event("GET", "/")
    response = app.handler(event, None)
    assert response["statusCode"] == 200
    assert "text/html" in response["headers"]["Content-Type"]
    assert "Caso F" in response["body"]


def test_handler_health_route():
    event = _make_event("GET", "/health")
    response = app.handler(event, None)
    assert response["statusCode"] == 200
    assert json.loads(response["body"])["status"] == "ok"


def test_handler_health_route_rest_api_event():
    event = _make_event("GET", "/health", api_version="v1")
    response = app.handler(event, None)
    assert response["statusCode"] == 200
    assert json.loads(response["body"])["status"] == "ok"


def test_handler_register_route_missing_body_returns_400():
    event = _make_event("POST", "/auth/register")
    response = app.handler(event, None)
    assert response["statusCode"] == 400


def test_handler_login_route_missing_body_returns_400():
    event = _make_event("POST", "/auth/login")
    response = app.handler(event, None)
    assert response["statusCode"] == 400


def test_handler_profile_no_claims_returns_401():
    event = _make_event("GET", "/profile")
    response = app.handler(event, None)
    assert response["statusCode"] == 401


def test_handler_unknown_route_returns_404():
    event = _make_event("GET", "/unknown")
    response = app.handler(event, None)
    assert response["statusCode"] == 404
    body = json.loads(response["body"])
    assert body["ok"] is False
    assert "availableRoutes" in body


def test_handler_get_on_post_only_route_returns_404():
    event = _make_event("GET", "/auth/register")
    response = app.handler(event, None)
    assert response["statusCode"] == 404
