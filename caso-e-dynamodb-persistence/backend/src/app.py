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


LANDING_PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Caso E | DynamoDB Persistence Pro</title>
  <style>
    :root {
      --bg: #07131c;
      --panel: rgba(10, 23, 34, 0.82);
      --line: rgba(157, 228, 255, 0.16);
      --text: #eef9ff;
      --muted: #98bbd2;
      --accent: #52d6a6;
      --accent-2: #28b8ff;
      --shadow: 0 24px 60px rgba(0, 0, 0, 0.28);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: "Segoe UI", sans-serif;
      color: var(--text);
      background:
        radial-gradient(circle at top left, rgba(40, 184, 255, 0.22), transparent 28%),
        radial-gradient(circle at right, rgba(82, 214, 166, 0.18), transparent 24%),
        linear-gradient(180deg, #07131c 0%, #0d1d2c 100%);
    }
    .shell { width: min(1180px, calc(100% - 28px)); margin: 0 auto; padding: 28px 0 56px; }
    .hero, .panel {
      border: 1px solid var(--line);
      border-radius: 24px;
      background: var(--panel);
      backdrop-filter: blur(14px);
      box-shadow: var(--shadow);
    }
    .hero { padding: 28px; margin-bottom: 18px; }
    .eyebrow {
      margin: 0 0 8px;
      color: var(--accent-2);
      text-transform: uppercase;
      letter-spacing: 0.18em;
      font-size: 0.78rem;
    }
    h1 { margin: 0; font-size: clamp(2.1rem, 6vw, 4rem); line-height: 0.96; }
    .lead { color: var(--muted); max-width: 70ch; margin: 14px 0 0; }
    .grid {
      display: grid;
      grid-template-columns: 1.2fr 0.8fr;
      gap: 18px;
      margin-bottom: 18px;
    }
    .panel { padding: 22px; }
    .panel h2 { margin: 0 0 12px; }
    .stats {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
      gap: 12px;
      margin-top: 18px;
    }
    .stat {
      padding: 14px;
      border-radius: 18px;
      background: rgba(255,255,255,0.04);
      border: 1px solid rgba(255,255,255,0.06);
    }
    .stat strong { display:block; font-size: 1.35rem; margin-bottom: 4px; }
    .stat span { color: var(--muted); font-size: 0.92rem; }
    .layout {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
      gap: 18px;
      margin-bottom: 18px;
    }
    label { display: block; margin: 10px 0 6px; color: #d8edff; font-size: 0.94rem; }
    input, select, button, pre {
      width: 100%;
      border-radius: 14px;
      border: 1px solid rgba(255,255,255,0.1);
    }
    input, select {
      padding: 12px 14px;
      color: var(--text);
      background: rgba(255,255,255,0.04);
    }
    button {
      padding: 12px 16px;
      margin-top: 14px;
      cursor: pointer;
      background: linear-gradient(135deg, var(--accent), var(--accent-2));
      color: #05131d;
      font-weight: 800;
    }
    .actions { display:flex; flex-wrap:wrap; gap:10px; margin-top: 10px; }
    .actions button { width: auto; margin-top: 0; }
    .hint, .list, .footnote { color: var(--muted); }
    .list { margin: 0; padding-left: 18px; }
    .code {
      margin-top: 14px;
      padding: 14px;
      border-radius: 18px;
      background: rgba(0,0,0,0.26);
      border: 1px solid rgba(255,255,255,0.07);
      font-family: Consolas, monospace;
      white-space: pre-wrap;
      word-break: break-word;
    }
    pre {
      min-height: 260px;
      margin: 0;
      padding: 18px;
      overflow: auto;
      background: rgba(0, 0, 0, 0.28);
      color: #dff4ff;
    }
    @media (max-width: 880px) {
      .grid { grid-template-columns: 1fr; }
      .shell { width: min(100% - 18px, 1180px); }
      .hero, .panel { padding: 18px; }
      .actions { flex-direction: column; }
      .actions button { width: 100%; }
    }
  </style>
</head>
<body>
  <main class="shell">
    <section class="hero">
      <p class="eyebrow">Caso E · DynamoDB · Single Table Design</p>
      <h1>Persistence Pro en AWS</h1>
      <p class="lead">
        Esta URL ya no devuelve un 404: ahora explica el caso, muestra qué resuelve la arquitectura
        y permite probar en vivo la API desplegada sobre API Gateway + Lambda + DynamoDB.
      </p>
      <div class="stats">
        <div class="stat"><strong>1 tabla</strong><span>`pk/sk` + 2 GSIs</span></div>
        <div class="stat"><strong>4 endpoints</strong><span>crear y consultar sin scans</span></div>
        <div class="stat"><strong>1 transacción</strong><span>ORDER + AUDIT atómicos</span></div>
        <div class="stat"><strong>Región</strong><span>us-east-2</span></div>
      </div>
    </section>

    <section class="grid">
      <article class="panel">
        <h2>Qué demuestra este caso</h2>
        <ul class="list">
          <li>Modelado por patrones de acceso en lugar de diseño relacional.</li>
          <li>Consulta por cliente usando la clave primaria.</li>
          <li>Consulta por estado y por producto usando GSI1 y GSI2.</li>
          <li>Persistencia transaccional para orden y evento de auditoría.</li>
        </ul>
        <div class="code">POST /orders
GET /customers/{customerId}/orders
GET /orders/status/{status}
GET /products/{productId}/orders</div>
      </article>

      <article class="panel">
        <h2>API desplegada</h2>
        <p class="hint">La base URL actual es esta misma. Todas las acciones de prueba usan el mismo origen.</p>
        <div class="code" id="baseUrl"></div>
        <p class="footnote">Si compartes esta URL, la persona ve la explicación y además puede ejecutar pruebas reales.</p>
      </article>
    </section>

    <section class="layout">
      <article class="panel">
        <h2>Crear orden</h2>
        <form id="orderForm">
          <label for="customerId">Customer ID</label>
          <input id="customerId" name="customerId" value="cust-001" required />

          <label for="customerName">Cliente</label>
          <input id="customerName" name="customerName" value="Acme SPA" required />

          <label for="productId">Product ID</label>
          <input id="productId" name="productId" value="prod-erp" required />

          <label for="productName">Producto</label>
          <input id="productName" name="productName" value="ERP Suite" required />

          <label for="status">Estado</label>
          <select id="status" name="status">
            <option value="PENDING">PENDING</option>
            <option value="PAID">PAID</option>
            <option value="CANCELLED">CANCELLED</option>
          </select>

          <label for="total">Total</label>
          <input id="total" name="total" type="number" step="0.01" value="1499.99" required />

          <button type="submit">Guardar orden en DynamoDB</button>
        </form>
      </article>

      <article class="panel">
        <h2>Consultas en vivo</h2>
        <label for="queryCustomerId">Customer ID</label>
        <input id="queryCustomerId" value="cust-001" />

        <label for="queryStatus">Estado</label>
        <input id="queryStatus" value="PENDING" />

        <label for="queryProductId">Product ID</label>
        <input id="queryProductId" value="prod-erp" />

        <div class="actions">
          <button type="button" data-query="customer">Órdenes por cliente</button>
          <button type="button" data-query="status">Órdenes por estado</button>
          <button type="button" data-query="product">Órdenes por producto</button>
        </div>
      </article>
    </section>

    <section class="panel">
      <h2>Respuesta</h2>
      <pre id="result">Esperando acciones...</pre>
    </section>
  </main>

  <script>
    const resultNode = document.getElementById("result");
    const form = document.getElementById("orderForm");
    const baseUrl = window.location.origin;
    document.getElementById("baseUrl").textContent = baseUrl;

    function setResult(payload) {
      resultNode.textContent = JSON.stringify(payload, null, 2);
    }

    async function request(path, options = {}) {
      const response = await fetch(`${baseUrl}${path}`, {
        headers: { "content-type": "application/json" },
        ...options,
      });
      const contentType = response.headers.get("content-type") || "";
      const payload = contentType.includes("application/json")
        ? await response.json()
        : { ok: response.ok, raw: await response.text() };

      if (!response.ok) {
        throw new Error(payload.error || payload.message || "Error desconocido");
      }

      return payload;
    }

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const formData = new FormData(form);
      const payload = Object.fromEntries(formData.entries());
      payload.total = Number(payload.total);
      setResult({ status: "Procesando..." });

      try {
        const response = await request("/orders", {
          method: "POST",
          body: JSON.stringify(payload),
        });
        setResult(response);
      } catch (error) {
        setResult({ ok: false, error: error.message });
      }
    });

    document.querySelectorAll("[data-query]").forEach((button) => {
      button.addEventListener("click", async () => {
        const query = button.dataset.query;
        const customerId = document.getElementById("queryCustomerId").value.trim();
        const status = document.getElementById("queryStatus").value.trim();
        const productId = document.getElementById("queryProductId").value.trim();

        const routes = {
          customer: `/customers/${customerId}/orders`,
          status: `/orders/status/${status}`,
          product: `/products/${productId}/orders`,
        };

        setResult({ status: "Consultando..." });

        try {
          const response = await request(routes[query], { method: "GET" });
          setResult(response);
        } catch (error) {
          setResult({ ok: false, error: error.message });
        }
      });
    });
  </script>
</body>
</html>
"""


def response_json(status_code: int, body: dict) -> dict:
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


def response_html(status_code: int, html: str) -> dict:
    return {
        "statusCode": status_code,
        "headers": {
            "content-type": "text/html; charset=utf-8",
        },
        "body": html,
    }


def serialize_item(item: dict) -> dict:
    return {key: serializer.serialize(value) for key, value in item.items()}


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
    return response_json(201, {"ok": True, "message": "Orden creada", "order": payload})


def get_customer_orders(customer_id: str) -> dict:
    if not customer_id:
        raise ValueError("customerId es obligatorio")

    result = table.query(
        KeyConditionExpression=Key("pk").eq(f"CUSTOMER#{customer_id}")
        & Key("sk").begins_with("ORDER#"),
        ScanIndexForward=False,
    )
    items = decimal_to_native(result.get("Items", []))
    return response_json(200, {"ok": True, "items": items, "count": len(items)})


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
    return response_json(200, {"ok": True, "items": items, "count": len(items)})


def get_product_orders(product_id: str) -> dict:
    if not product_id:
        raise ValueError("productId es obligatorio")

    result = table.query(
        IndexName="gsi2",
        KeyConditionExpression=Key("gsi2pk").eq(f"PRODUCT#{product_id}"),
        ScanIndexForward=False,
    )
    items = decimal_to_native(result.get("Items", []))
    return response_json(200, {"ok": True, "items": items, "count": len(items)})


def handler(event, context):
    del context
    request_context = event.get("requestContext") or {}
    http = request_context.get("http") or {}
    method = http.get("method") or ""
    path = http.get("path") or event.get("rawPath") or ""
    path_params = event.get("pathParameters") or {}

    try:
        if method == "OPTIONS":
            return response_json(200, {"ok": True})

        if method == "GET" and path == "/":
            return response_html(200, LANDING_PAGE)

        if method == "POST" and path.endswith("/orders"):
            return create_order(event)

        if method == "GET" and "/customers/" in path and path.endswith("/orders"):
            return get_customer_orders(path_params.get("customerId", ""))

        if method == "GET" and "/orders/status/" in path:
            return get_orders_by_status(path_params.get("status", ""))

        if method == "GET" and "/products/" in path and path.endswith("/orders"):
            return get_product_orders(path_params.get("productId", ""))

        return response_json(404, {"ok": False, "error": "Ruta no soportada"})
    except ValueError as exc:
        return response_json(400, {"ok": False, "error": str(exc)})
    except Exception as exc:
        return response_json(500, {"ok": False, "error": "Error interno", "detail": str(exc)})