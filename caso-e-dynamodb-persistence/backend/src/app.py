import json
import os
import time
import uuid
from datetime import datetime, timezone
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.types import TypeSerializer


TABLE_NAME = os.environ.get("TABLE_NAME", "persistence_pro_orders")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)
ddb_client = boto3.client("dynamodb")
serializer = TypeSerializer()


def response(status_code: int, body: dict) -> dict:
    return {
        "statusCode": status_code,
        "headers": {
            "content-type": "application/json",
            "access-control-allow-origin": "*",
            "access-control-allow-headers": "content-type",
            "access-control-allow-methods": "OPTIONS,GET,POST",
        },
        "body": json.dumps(body, ensure_ascii=False),
    }


def serialize_item(item: dict) -> dict:
    return {key: serializer.serialize(value) for key, value in item.items()}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def decimal_to_native(value):
    if isinstance(value, list):
        return [decimal_to_native(item) for item in value]
    if isinstance(value, dict):
        return {key: decimal_to_native(item) for key, item in value.items()}
    if isinstance(value, Decimal):
        return int(value) if value % 1 == 0 else float(value)
    return value


def load_body(event: dict) -> dict:
    raw = event.get("body") or "{}"
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError("JSON invalido") from exc


def require_fields(data: dict, fields: list[str]) -> None:
    missing = [field for field in fields if not str(data.get(field) or "").strip()]
    if missing:
        raise ValueError(f"Faltan campos obligatorios: {', '.join(missing)}")


def build_order_items(data: dict) -> tuple[dict, dict]:
    order_id = str(uuid.uuid4())
    created_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    ttl = int(time.time()) + 90 * 24 * 60 * 60

    customer_id = str(data["customerId"]).strip()
    customer_name = str(data["customerName"]).strip()
    product_id = str(data["productId"]).strip()
    product_name = str(data["productName"]).strip()
    status = str(data.get("status") or "PENDING").strip().upper()
    total = Decimal(str(data["total"]))

    order_item = {
        "pk": f"CUSTOMER#{customer_id}",
        "sk": f"ORDER#{created_at}#{order_id}",
        "entityType": "ORDER",
        "orderId": order_id,
        "customerId": customer_id,
        "customerName": customer_name,
        "productId": product_id,
        "productName": product_name,
        "status": status,
        "total": total,
        "createdAt": created_at,
        "gsi1pk": f"STATUS#{status}",
        "gsi1sk": f"{created_at}#{order_id}",
        "gsi2pk": f"PRODUCT#{product_id}",
        "gsi2sk": f"{created_at}#{order_id}",
        "ttl": ttl,
    }

    audit_item = {
        "pk": f"ORDER#{order_id}",
        "sk": f"EVENT#{created_at}",
        "entityType": "AUDIT",
        "orderId": order_id,
        "eventType": "ORDER_CREATED",
        "status": status,
        "customerId": customer_id,
        "createdAt": created_at,
        "ttl": ttl,
    }

    return order_item, audit_item


def create_order(event: dict) -> dict:
    data = load_body(event)
    require_fields(
        data,
        ["customerId", "customerName", "productId", "productName", "total"],
    )

    order_item, audit_item = build_order_items(data)

    ddb_client.transact_write_items(
        TransactItems=[
            {"Put": {"TableName": TABLE_NAME, "Item": serialize_item(order_item)}},
            {"Put": {"TableName": TABLE_NAME, "Item": serialize_item(audit_item)}},
        ]
    )

    payload = decimal_to_native(order_item)
    return response(201, {"ok": True, "message": "Orden creada", "order": payload})


def get_customer_orders(customer_id: str) -> dict:
    if not customer_id:
        raise ValueError("customerId es obligatorio")

    result = table.query(
        KeyConditionExpression=Key("pk").eq(f"CUSTOMER#{customer_id}")
        & Key("sk").begins_with("ORDER#"),
        ScanIndexForward=False,
    )
    items = decimal_to_native(result.get("Items", []))
    return response(200, {"ok": True, "items": items, "count": len(items)})


def get_orders_by_status(status: str) -> dict:
    normalized = status.strip().upper()
    if not normalized:
        raise ValueError("status es obligatorio")

    result = table.query(
        IndexName="gsi1",
        KeyConditionExpression=Key("gsi1pk").eq(f"STATUS#{normalized}"),
        ScanIndexForward=False,
    )
    items = decimal_to_native(result.get("Items", []))
    return response(200, {"ok": True, "items": items, "count": len(items)})


def get_product_orders(product_id: str) -> dict:
    if not product_id:
        raise ValueError("productId es obligatorio")

    result = table.query(
        IndexName="gsi2",
        KeyConditionExpression=Key("gsi2pk").eq(f"PRODUCT#{product_id}"),
        ScanIndexForward=False,
    )
    items = decimal_to_native(result.get("Items", []))
    return response(200, {"ok": True, "items": items, "count": len(items)})


def handler(event, context):
    del context
    request_context = event.get("requestContext") or {}
    http = request_context.get("http") or {}
    method = http.get("method") or ""
    path = http.get("path") or event.get("rawPath") or ""
    path_params = event.get("pathParameters") or {}

    try:
        if method == "OPTIONS":
            return response(200, {"ok": True})

        if method == "POST" and path.endswith("/orders"):
            return create_order(event)

        if method == "GET" and "/customers/" in path and path.endswith("/orders"):
            return get_customer_orders(path_params.get("customerId", ""))

        if method == "GET" and "/orders/status/" in path:
            return get_orders_by_status(path_params.get("status", ""))

        if method == "GET" and "/products/" in path and path.endswith("/orders"):
            return get_product_orders(path_params.get("productId", ""))

        return response(404, {"ok": False, "error": "Ruta no soportada"})
    except ValueError as exc:
        return response(400, {"ok": False, "error": str(exc)})
    except Exception as exc:
        return response(500, {"ok": False, "error": "Error interno", "detail": str(exc)})
