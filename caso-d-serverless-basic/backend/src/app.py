import json
import os
import time
import uuid
from datetime import datetime, timezone

import boto3


ddb = boto3.resource("dynamodb")
TABLE_NAME = os.environ.get("TABLE_NAME", "portfolio_leads")
TABLE = ddb.Table(TABLE_NAME)


def _response(status_code: int, body: dict):
    """Devuelve JSON + headers CORS (modo demo)."""
    return {
        "statusCode": status_code,
        "headers": {
            "content-type": "application/json",
            "access-control-allow-origin": "*",
            "access-control-allow-headers": "content-type",
            "access-control-allow-methods": "OPTIONS,POST",
        },
        "body": json.dumps(body, ensure_ascii=False),
    }


def handler(event, context):
    http = (event.get("requestContext", {}) or {}).get("http", {}) or {}
    method = http.get("method") or ""

    if method == "OPTIONS":
        return _response(200, {"ok": True})

    if method and method != "POST":
        return _response(405, {"ok": False, "error": "Método no permitido"})

    raw = event.get("body") or "{}"
    try:
        data = json.loads(raw)
    except Exception:
        return _response(400, {"ok": False, "error": "JSON inválido"})

    # Honeypot anti-spam: si alguien rellena este campo oculto, ignoramos.
    if str(data.get("company") or "").strip():
        return _response(200, {"ok": True, "id": "ignored"})

    name = str(data.get("name") or "").strip()
    email = str(data.get("email") or "").strip()
    message = str(data.get("message") or "").strip()

    if not name or not email or not message:
        return _response(400, {"ok": False, "error": "Faltan campos: name/email/message"})

    if len(name) > 120:
        return _response(400, {"ok": False, "error": "Nombre demasiado largo"})
    if len(email) > 180:
        return _response(400, {"ok": False, "error": "Email demasiado largo"})
    if len(message) > 2000:
        return _response(400, {"ok": False, "error": "Mensaje demasiado largo (máx 2000)"})

    now = datetime.now(timezone.utc).isoformat()
    item_id = str(uuid.uuid4())

    item = {
        "pk": "LEAD",
        "sk": now,
        "id": item_id,
        "name": name,
        "email": email,
        "message": message,
        "createdAt": now,
        "sourceIp": http.get("sourceIp"),
        "userAgent": http.get("userAgent"),
        # TTL: auto-borrado en 30 días (útil para demo / privacidad)
        "ttl": int(time.time()) + 30 * 24 * 60 * 60,
    }

    TABLE.put_item(Item=item)
    return _response(200, {"ok": True, "id": item_id})
