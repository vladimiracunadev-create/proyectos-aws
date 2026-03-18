import json
from decimal import Decimal
from unittest.mock import MagicMock, patch

import pytest
import app


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _event(method="GET", path="/", path_params=None, body=None):
    return {
        "requestContext": {"http": {"method": method, "path": path}},
        "rawPath": path,
        "pathParameters": path_params or {},
        "body": json.dumps(body) if body is not None else None,
    }


VALID_ORDER = {
    "customerId": "cust-001",
    "customerName": "Acme SPA",
    "productId": "prod-erp",
    "productName": "ERP Suite",
    "total": 1499.99,
    "status": "PENDING",
}


# ---------------------------------------------------------------------------
# decimal_to_native
# ---------------------------------------------------------------------------

def test_decimal_to_native_int():
    assert app.decimal_to_native(Decimal("5")) == 5
    assert isinstance(app.decimal_to_native(Decimal("5")), int)


def test_decimal_to_native_float():
    assert app.decimal_to_native(Decimal("1.5")) == 1.5
    assert isinstance(app.decimal_to_native(Decimal("1.5")), float)


def test_decimal_to_native_nested_dict():
    result = app.decimal_to_native({"total": Decimal("9.99"), "qty": Decimal("2")})
    assert result == {"total": 9.99, "qty": 2}


def test_decimal_to_native_nested_list():
    result = app.decimal_to_native([Decimal("1"), Decimal("2.5")])
    assert result == [1, 2.5]


def test_decimal_to_native_passthrough():
    assert app.decimal_to_native("texto") == "texto"
    assert app.decimal_to_native(42) == 42


# ---------------------------------------------------------------------------
# load_body
# ---------------------------------------------------------------------------

def test_load_body_valid_json():
    event = {"body": '{"key": "value"}'}
    assert app.load_body(event) == {"key": "value"}


def test_load_body_invalid_json_raises():
    with pytest.raises(ValueError):
        app.load_body({"body": "no-es-json"})


def test_load_body_missing_body_returns_empty():
    assert app.load_body({}) == {}


def test_load_body_null_body_returns_empty():
    assert app.load_body({"body": None}) == {}


# ---------------------------------------------------------------------------
# require_fields
# ---------------------------------------------------------------------------

def test_require_fields_all_present():
    app.require_fields({"a": "1", "b": "2"}, ["a", "b"])  # no exception


def test_require_fields_missing_one():
    with pytest.raises(ValueError) as exc:
        app.require_fields({"a": "1"}, ["a", "b"])
    assert "b" in str(exc.value)


def test_require_fields_whitespace_treated_as_missing():
    with pytest.raises(ValueError) as exc:
        app.require_fields({"a": "   "}, ["a"])
    assert "a" in str(exc.value)


# ---------------------------------------------------------------------------
# build_order_items
# ---------------------------------------------------------------------------

def test_build_order_items_structure():
    order, audit = app.build_order_items(VALID_ORDER)
    assert order["pk"] == "CUSTOMER#cust-001"
    assert order["sk"].startswith("ORDER#")
    assert order["entityType"] == "ORDER"
    assert "orderId" in order
    assert order["gsi1pk"] == "STATUS#PENDING"
    assert order["gsi2pk"] == "PRODUCT#prod-erp"
    assert "ttl" in order

    assert audit["pk"].startswith("ORDER#")
    assert audit["entityType"] == "AUDIT"
    assert audit["eventType"] == "ORDER_CREATED"


def test_build_order_items_default_status():
    data = {**VALID_ORDER}
    del data["status"]
    order, _ = app.build_order_items(data)
    assert order["gsi1pk"] == "STATUS#PENDING"


def test_build_order_items_custom_status():
    data = {**VALID_ORDER, "status": "paid"}
    order, _ = app.build_order_items(data)
    assert order["gsi1pk"] == "STATUS#PAID"
    assert order["status"] == "PAID"


# ---------------------------------------------------------------------------
# handler — OPTIONS
# ---------------------------------------------------------------------------

def test_handler_options():
    result = app.handler(_event("OPTIONS", "/orders"), None)
    assert result["statusCode"] == 200


# ---------------------------------------------------------------------------
# handler — POST /orders
# ---------------------------------------------------------------------------

def test_handler_post_orders_success():
    mock_client = MagicMock()

    with patch.object(app, "ddb_client", mock_client):
        result = app.handler(_event("POST", "/orders", body=VALID_ORDER), None)

    assert result["statusCode"] == 201
    body = json.loads(result["body"])
    assert body["ok"] is True
    assert "order" in body
    mock_client.transact_write_items.assert_called_once()


def test_handler_post_orders_missing_field():
    data = {k: v for k, v in VALID_ORDER.items() if k != "total"}
    result = app.handler(_event("POST", "/orders", body=data), None)
    assert result["statusCode"] == 400
    assert "total" in json.loads(result["body"])["error"]


def test_handler_post_orders_invalid_json():
    event = _event("POST", "/orders")
    event["body"] = "not-json"
    result = app.handler(event, None)
    assert result["statusCode"] == 400


# ---------------------------------------------------------------------------
# handler — GET queries
# ---------------------------------------------------------------------------

def test_handler_get_customer_orders():
    mock_table = MagicMock()
    mock_table.query.return_value = {"Items": []}

    with patch.object(app, "table", mock_table):
        result = app.handler(
            _event("GET", "/customers/cust-001/orders", path_params={"customerId": "cust-001"}),
            None,
        )

    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    assert body["ok"] is True
    assert isinstance(body["items"], list)


def test_handler_get_orders_by_status():
    mock_table = MagicMock()
    mock_table.query.return_value = {"Items": []}

    with patch.object(app, "table", mock_table):
        result = app.handler(
            _event("GET", "/orders/status/PENDING", path_params={"status": "PENDING"}),
            None,
        )

    assert result["statusCode"] == 200


def test_handler_get_product_orders():
    mock_table = MagicMock()
    mock_table.query.return_value = {"Items": []}

    with patch.object(app, "table", mock_table):
        result = app.handler(
            _event("GET", "/products/prod-erp/orders", path_params={"productId": "prod-erp"}),
            None,
        )

    assert result["statusCode"] == 200


def test_handler_get_root_returns_html():
    result = app.handler(_event("GET", "/"), None)
    assert result["statusCode"] == 200
    assert "text/html" in result["headers"]["content-type"]


def test_handler_unknown_route_returns_404():
    result = app.handler(_event("GET", "/ruta-inexistente"), None)
    assert result["statusCode"] == 404
