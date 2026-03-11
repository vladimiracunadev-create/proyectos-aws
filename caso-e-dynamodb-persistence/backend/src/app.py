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
      --bg: #08121b;
      --panel: rgba(9, 25, 37, 0.84);
      --panel-soft: rgba(255, 255, 255, 0.04);
      --line: rgba(142, 223, 255, 0.15);
      --text: #eff9ff;
      --muted: #9ebed3;
      --accent: #52d5a8;
      --accent-2: #29b8ff;
      --warn: #ffd479;
      --ok: #7ef0b8;
      --danger: #ff8b8b;
      --shadow: 0 24px 64px rgba(0, 0, 0, 0.3);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: "Segoe UI", sans-serif;
      color: var(--text);
      background:
        radial-gradient(circle at top left, rgba(41, 184, 255, 0.2), transparent 26%),
        radial-gradient(circle at right, rgba(82, 213, 168, 0.18), transparent 22%),
        linear-gradient(180deg, #07111a 0%, #0e1c29 100%);
    }
    .shell { width: min(1200px, calc(100% - 28px)); margin: 0 auto; padding: 28px 0 56px; }
    .hero, .panel {
      border: 1px solid var(--line);
      border-radius: 24px;
      background: var(--panel);
      backdrop-filter: blur(14px);
      box-shadow: var(--shadow);
    }
    .hero { padding: 28px; margin-bottom: 18px; }
    .eyebrow {
      margin: 0 0 10px;
      color: var(--accent-2);
      text-transform: uppercase;
      letter-spacing: 0.18em;
      font-size: 0.78rem;
    }
    h1 { margin: 0; font-size: clamp(2.2rem, 6vw, 4.2rem); line-height: 0.95; }
    h2 { margin: 0 0 12px; font-size: 1.25rem; }
    .lead { color: var(--muted); max-width: 72ch; margin: 14px 0 0; }
    .hero-grid {
      display: grid;
      grid-template-columns: 1.2fr 0.8fr;
      gap: 18px;
      margin-top: 22px;
    }
    .mini-panel {
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 20px;
      padding: 16px;
      background: rgba(255,255,255,0.04);
    }
    .stats {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: 12px;
    }
    .stat {
      padding: 14px;
      border-radius: 18px;
      background: rgba(255,255,255,0.04);
      border: 1px solid rgba(255,255,255,0.06);
    }
    .stat strong { display: block; font-size: 1.35rem; margin-bottom: 4px; }
    .stat span { color: var(--muted); font-size: 0.92rem; }
    .panel { padding: 22px; margin-bottom: 18px; }
    .story {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 14px;
    }
    .story-card {
      padding: 16px;
      border-radius: 20px;
      background: var(--panel-soft);
      border: 1px solid rgba(255,255,255,0.07);
    }
    .story-card strong { display: block; margin-bottom: 6px; }
    .story-card p { margin: 0; color: var(--muted); line-height: 1.45; }
    .layout {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 18px;
      margin-bottom: 18px;
    }
    .stack-list, .tips-list {
      margin: 0;
      padding-left: 18px;
      color: var(--muted);
    }
    .stack-list li, .tips-list li { margin-bottom: 8px; }
    label {
      display: block;
      margin: 12px 0 6px;
      color: #d9efff;
      font-size: 0.94rem;
    }
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
    .helper {
      margin-top: 8px;
      color: var(--muted);
      font-size: 0.92rem;
    }
    .primary-btn, .query-btn, .ghost-btn {
      cursor: pointer;
      font-weight: 800;
      transition: transform 120ms ease, filter 120ms ease, border-color 120ms ease;
    }
    .primary-btn:hover, .query-btn:hover, .ghost-btn:hover {
      transform: translateY(-1px);
      filter: brightness(1.04);
    }
    .primary-btn {
      padding: 13px 16px;
      margin-top: 14px;
      background: linear-gradient(135deg, var(--accent), var(--accent-2));
      color: #06131d;
    }
    .query-grid {
      display: grid;
      gap: 10px;
      margin-top: 12px;
    }
    .query-btn {
      text-align: left;
      padding: 14px;
      background: rgba(255,255,255,0.04);
      color: var(--text);
    }
    .query-btn.active {
      border-color: rgba(82, 213, 168, 0.42);
      background: linear-gradient(135deg, rgba(82, 213, 168, 0.18), rgba(41, 184, 255, 0.14));
    }
    .query-btn strong {
      display: block;
      margin-bottom: 3px;
      font-size: 0.98rem;
    }
    .query-btn span {
      color: var(--muted);
      font-size: 0.9rem;
    }
    .response-head {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: center;
      margin-bottom: 14px;
      flex-wrap: wrap;
    }
    .badge-row {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }
    .badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 10px 12px;
      border-radius: 999px;
      background: rgba(255,255,255,0.04);
      border: 1px solid rgba(255,255,255,0.08);
      color: var(--muted);
      font-size: 0.92rem;
    }
    .badge.ok { color: var(--ok); }
    .badge.warn { color: var(--warn); }
    .badge.danger { color: var(--danger); }
    .ghost-btn {
      width: auto;
      padding: 10px 12px;
      background: transparent;
      color: var(--text);
    }
    .summary-card {
      display: none;
      margin-bottom: 14px;
      padding: 16px;
      border-radius: 18px;
      background: rgba(255,255,255,0.04);
      border: 1px solid rgba(255,255,255,0.08);
    }
    .summary-card.visible { display: block; }
    .summary-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 12px;
      margin-top: 12px;
    }
    .summary-item {
      padding: 12px;
      border-radius: 16px;
      background: rgba(0,0,0,0.18);
      border: 1px solid rgba(255,255,255,0.06);
    }
    .summary-item strong {
      display: block;
      margin-bottom: 4px;
      font-size: 0.8rem;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--muted);
    }
    .summary-item span {
      display: block;
      word-break: break-word;
    }
    .cards {
      display: grid;
      gap: 12px;
      margin-bottom: 14px;
    }
    .result-card {
      padding: 16px;
      border-radius: 18px;
      background: rgba(255,255,255,0.04);
      border: 1px solid rgba(255,255,255,0.08);
    }
    .result-card header {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: baseline;
      margin-bottom: 10px;
      flex-wrap: wrap;
    }
    .result-card h3 {
      margin: 0;
      font-size: 1rem;
    }
    .result-card small {
      color: var(--muted);
    }
    .result-meta {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
      gap: 10px;
    }
    .result-meta div {
      padding: 10px 12px;
      border-radius: 14px;
      background: rgba(0,0,0,0.18);
    }
    .result-meta strong {
      display: block;
      font-size: 0.78rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--muted);
      margin-bottom: 4px;
    }
    pre {
      min-height: 180px;
      margin: 0;
      padding: 18px;
      overflow: auto;
      background: rgba(0, 0, 0, 0.28);
      color: #dff4ff;
    }
    .code-box {
      margin-top: 14px;
      padding: 14px;
      border-radius: 18px;
      background: rgba(0,0,0,0.26);
      border: 1px solid rgba(255,255,255,0.07);
      font-family: Consolas, monospace;
      white-space: pre-wrap;
      word-break: break-word;
    }
    @media (max-width: 960px) {
      .hero-grid, .layout { grid-template-columns: 1fr; }
    }
    @media (max-width: 720px) {
      .shell { width: min(100% - 18px, 1200px); }
      .hero, .panel { padding: 18px; }
    }
  </style>
</head>
<body>
  <main class="shell">
    <section class="hero">
      <p class="eyebrow">Caso E · DynamoDB · Single Table Design</p>
      <h1>Persistence Pro en AWS</h1>
      <p class="lead">
        Esta demo explica la arquitectura y además la deja probar en vivo. No es solo una portada:
        cada acción de esta pantalla ejecuta consultas reales sobre API Gateway + Lambda + DynamoDB.
      </p>

      <div class="hero-grid">
        <div class="mini-panel">
          <div class="stats">
            <div class="stat"><strong>1 tabla</strong><span>`pk/sk` + 2 GSIs</span></div>
            <div class="stat"><strong>4 endpoints</strong><span>sin scans</span></div>
            <div class="stat"><strong>1 transacción</strong><span>ORDER + AUDIT</span></div>
            <div class="stat"><strong>Región</strong><span>us-east-2</span></div>
          </div>
        </div>
        <div class="mini-panel">
          <h2>API base URL</h2>
          <div class="code-box" id="baseUrl"></div>
          <p class="helper">Puedes compartir esta misma URL: muestra el contexto del caso y también permite probar la API.</p>
        </div>
      </div>
    </section>

    <section class="panel">
      <h2>Qué está pasando realmente</h2>
      <div class="story">
        <div class="story-card">
          <strong>1. Escribes una orden</strong>
          <p>El formulario ejecuta `POST /orders` y guarda el item principal junto con un evento de auditoría.</p>
        </div>
        <div class="story-card">
          <strong>2. Consultas por patrón</strong>
          <p>Los botones de consulta disparan lecturas distintas: por cliente, por estado o por producto.</p>
        </div>
        <div class="story-card">
          <strong>3. Ves datos reales</strong>
          <p>La respuesta ya no se muestra solo como JSON crudo: también se resume en tarjetas legibles.</p>
        </div>
      </div>
    </section>

    <section class="layout">
      <article class="panel">
        <h2>Crear orden</h2>
        <ul class="tips-list">
          <li>Usa esta acción para comprobar la escritura transaccional.</li>
          <li>La orden queda indexada por cliente, estado y producto.</li>
          <li>Luego puedes consultar esa misma orden con los botones de la derecha.</li>
        </ul>

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

          <button class="primary-btn" type="submit">Guardar orden en DynamoDB</button>
          <p class="helper">Consejo: deja estos valores y prueba primero la escritura, luego usa las consultas con los mismos filtros.</p>
        </form>
      </article>

      <article class="panel">
        <h2>Consultas en vivo</h2>
        <ul class="stack-list">
          <li><strong>Cliente</strong>: usa la clave primaria `CUSTOMER#id`.</li>
          <li><strong>Estado</strong>: usa `GSI1` para paneles operativos.</li>
          <li><strong>Producto</strong>: usa `GSI2` para vistas por catálogo.</li>
        </ul>

        <label for="queryCustomerId">Customer ID</label>
        <input id="queryCustomerId" value="cust-001" />

        <label for="queryStatus">Estado</label>
        <input id="queryStatus" value="PENDING" />

        <label for="queryProductId">Product ID</label>
        <input id="queryProductId" value="prod-erp" />

        <div class="query-grid">
          <button type="button" class="query-btn" data-query="customer">
            <strong>Órdenes por cliente</strong>
            <span>Ideal para historial y vista tipo CRM.</span>
          </button>
          <button type="button" class="query-btn" data-query="status">
            <strong>Órdenes por estado</strong>
            <span>Ideal para operaciones: pending, paid o cancelled.</span>
          </button>
          <button type="button" class="query-btn" data-query="product">
            <strong>Órdenes por producto</strong>
            <span>Ideal para ver demanda y consumo por SKU.</span>
          </button>
        </div>
      </article>
    </section>

    <section class="panel">
      <div class="response-head">
        <div>
          <h2>Resultado de la prueba</h2>
          <p class="helper" id="responseMessage">Pulsa una acción para ver la respuesta resumida y también el JSON completo.</p>
        </div>
        <div class="badge-row">
          <span class="badge" id="statusBadge">Sin ejecutar</span>
          <span class="badge warn" id="countBadge">0 items</span>
          <button type="button" class="ghost-btn" id="toggleRaw">Ocultar JSON</button>
        </div>
      </div>

      <div class="summary-card" id="summaryCard">
        <strong id="summaryTitle">Sin resumen todavía</strong>
        <div class="summary-grid" id="summaryGrid"></div>
      </div>

      <div class="cards" id="cards"></div>
      <pre id="result">Esperando acciones...</pre>
    </section>
  </main>

  <script>
    const resultNode = document.getElementById("result");
    const form = document.getElementById("orderForm");
    const baseUrl = window.location.origin;
    const responseMessage = document.getElementById("responseMessage");
    const statusBadge = document.getElementById("statusBadge");
    const countBadge = document.getElementById("countBadge");
    const summaryCard = document.getElementById("summaryCard");
    const summaryTitle = document.getElementById("summaryTitle");
    const summaryGrid = document.getElementById("summaryGrid");
    const cardsNode = document.getElementById("cards");
    const toggleRawButton = document.getElementById("toggleRaw");
    document.getElementById("baseUrl").textContent = baseUrl;

    let rawVisible = true;

    function setBadges(kind, count, message) {
      statusBadge.textContent = message;
      statusBadge.className = `badge ${kind}`;
      countBadge.textContent = `${count} item${count === 1 ? "" : "s"}`;
    }

    function renderSummary(items, meta = {}) {
      summaryGrid.innerHTML = "";

      if (!items.length && !meta.order) {
        summaryCard.classList.remove("visible");
        return;
      }

      summaryCard.classList.add("visible");

      if (meta.order) {
        summaryTitle.textContent = "Orden creada correctamente";
        [
          ["Order ID", meta.order.orderId],
          ["Cliente", meta.order.customerName],
          ["Producto", meta.order.productName],
          ["Estado", meta.order.status],
          ["Total", meta.order.total],
          ["Creado", meta.order.createdAt],
        ].forEach(([label, value]) => {
          const item = document.createElement("div");
          item.className = "summary-item";
          item.innerHTML = `<strong>${label}</strong><span>${value ?? "-"}</span>`;
          summaryGrid.appendChild(item);
        });
        return;
      }

      summaryTitle.textContent = "Consulta completada";
      [
        ["Total de resultados", meta.count ?? items.length],
        ["Consulta", meta.label || "N/A"],
        ["Primer order ID", items[0]?.orderId || "-"],
        ["Primer cliente", items[0]?.customerName || "-"],
      ].forEach(([label, value]) => {
        const item = document.createElement("div");
        item.className = "summary-item";
        item.innerHTML = `<strong>${label}</strong><span>${value}</span>`;
        summaryGrid.appendChild(item);
      });
    }

    function renderCards(items) {
      cardsNode.innerHTML = "";

      if (!items.length) {
        return;
      }

      items.slice(0, 6).forEach((item, index) => {
        const card = document.createElement("article");
        card.className = "result-card";
        card.innerHTML = `
          <header>
            <h3>Resultado ${index + 1}</h3>
            <small>${item.createdAt || item.sk || "sin fecha"}</small>
          </header>
          <div class="result-meta">
            <div><strong>Order ID</strong><span>${item.orderId || "-"}</span></div>
            <div><strong>Cliente</strong><span>${item.customerName || item.customerId || "-"}</span></div>
            <div><strong>Producto</strong><span>${item.productName || item.productId || "-"}</span></div>
            <div><strong>Estado</strong><span>${item.status || "-"}</span></div>
            <div><strong>Total</strong><span>${item.total ?? "-"}</span></div>
            <div><strong>PK / SK</strong><span>${item.pk || "-"} / ${item.sk || "-"}</span></div>
          </div>
        `;
        cardsNode.appendChild(card);
      });
    }

    function setResult(payload, options = {}) {
      const items = payload.items || [];
      const order = payload.order || null;
      const count = payload.count ?? (order ? 1 : items.length);
      responseMessage.textContent = options.message || "Respuesta recibida desde la API.";
      renderSummary(items, { count, order, label: options.label });
      renderCards(order ? [order] : items);
      resultNode.textContent = JSON.stringify(payload, null, 2);
      setBadges("ok", count, payload.ok === false ? "Con error" : "OK");
    }

    function setPending(message) {
      responseMessage.textContent = message;
      summaryCard.classList.remove("visible");
      cardsNode.innerHTML = "";
      resultNode.textContent = JSON.stringify({ status: message }, null, 2);
      setBadges("warn", 0, "Procesando");
    }

    function setError(message) {
      responseMessage.textContent = "La llamada falló. Revisa el detalle abajo.";
      summaryCard.classList.remove("visible");
      cardsNode.innerHTML = "";
      resultNode.textContent = JSON.stringify({ ok: false, error: message }, null, 2);
      setBadges("danger", 0, "Error");
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

    toggleRawButton.addEventListener("click", () => {
      rawVisible = !rawVisible;
      resultNode.style.display = rawVisible ? "block" : "none";
      toggleRawButton.textContent = rawVisible ? "Ocultar JSON" : "Mostrar JSON";
    });

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const formData = new FormData(form);
      const payload = Object.fromEntries(formData.entries());
      payload.total = Number(payload.total);
      setPending("Guardando orden en DynamoDB...");

      try {
        const response = await request("/orders", {
          method: "POST",
          body: JSON.stringify(payload),
        });
        setResult(response, {
          message: "La orden fue creada y ya quedó indexada para las consultas secundarias.",
          label: "Creación de orden",
        });
      } catch (error) {
        setError(error.message);
      }
    });

    document.querySelectorAll("[data-query]").forEach((button) => {
      button.addEventListener("click", async () => {
        document.querySelectorAll("[data-query]").forEach((item) => item.classList.remove("active"));
        button.classList.add("active");

        const query = button.dataset.query;
        const customerId = document.getElementById("queryCustomerId").value.trim();
        const status = document.getElementById("queryStatus").value.trim();
        const productId = document.getElementById("queryProductId").value.trim();

        const routes = {
          customer: {
            path: `/customers/${customerId}/orders`,
            label: "Consulta por cliente",
            pending: "Consultando historial del cliente...",
          },
          status: {
            path: `/orders/status/${status}`,
            label: "Consulta por estado",
            pending: "Consultando órdenes operativas por estado...",
          },
          product: {
            path: `/products/${productId}/orders`,
            label: "Consulta por producto",
            pending: "Consultando órdenes por producto...",
          },
        };

        const config = routes[query];
        setPending(config.pending);

        try {
          const response = await request(config.path, { method: "GET" });
          setResult(response, {
            message: `${config.label} ejecutada correctamente.`,
            label: config.label,
          });
        } catch (error) {
          setError(error.message);
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