import json
import os
import uuid
from datetime import datetime, timezone

import boto3


EVENT_BUS_NAME = os.environ.get("EVENT_BUS_NAME", "caso-g-orders-bus")
NOTIFICATIONS_TOPIC_ARN = os.environ.get("NOTIFICATIONS_TOPIC_ARN", "")

events_client = boto3.client("events")
sns_client = boto3.client("sns")


LANDING_PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Caso G | Event Driven</title>
  <style>
    :root {
      --bg: #07111b;
      --panel: rgba(10, 22, 38, 0.86);
      --panel-soft: rgba(255, 255, 255, 0.04);
      --line: rgba(115, 190, 255, 0.16);
      --text: #eef7ff;
      --muted: #9ab8cb;
      --accent: #ff9900;
      --accent-2: #4cc9f0;
      --ok: #7ef0b8;
      --warn: #ffd479;
      --danger: #ff9797;
      --shadow: 0 28px 70px rgba(0, 0, 0, 0.35);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: "Segoe UI", sans-serif;
      color: var(--text);
      background:
        radial-gradient(circle at top left, rgba(76, 201, 240, 0.18), transparent 24%),
        radial-gradient(circle at right, rgba(255, 153, 0, 0.18), transparent 22%),
        linear-gradient(180deg, #07101a 0%, #0d1b2a 100%);
    }
    .shell { width: min(1200px, calc(100% - 28px)); margin: 0 auto; padding: 28px 0 56px; }
    .hero, .panel {
      border: 1px solid var(--line);
      border-radius: 24px;
      background: var(--panel);
      backdrop-filter: blur(16px);
      box-shadow: var(--shadow);
    }
    .hero { padding: 28px; margin-bottom: 18px; }
    .eyebrow {
      margin: 0 0 10px;
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: 0.18em;
      font-size: 0.78rem;
    }
    h1 { margin: 0; font-size: clamp(2.3rem, 6vw, 4.4rem); line-height: 0.96; }
    h2 { margin: 0 0 12px; font-size: 1.2rem; }
    .lead { color: var(--muted); max-width: 74ch; margin: 14px 0 0; line-height: 1.58; }
    .hero-grid {
      display: grid;
      grid-template-columns: 1.15fr 0.85fr;
      gap: 18px;
      margin-top: 22px;
    }
    .mini-panel, .story-card, .stat, .summary-card, .result-card {
      border-radius: 20px;
      border: 1px solid rgba(255,255,255,0.08);
      background: var(--panel-soft);
    }
    .mini-panel, .story-card, .stat, .summary-card, .result-card { padding: 16px; }
    .stats {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: 12px;
    }
    .stat strong { display: block; font-size: 1.35rem; margin-bottom: 4px; }
    .stat span { color: var(--muted); font-size: 0.92rem; }
    .panel { padding: 22px; margin-bottom: 18px; }
    .story, .summary-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 14px;
    }
    .story-card strong, .summary-item strong {
      display: block;
      margin-bottom: 6px;
    }
    .story-card p, .summary-item span, .helper, .chip-note, .list li, .status {
      color: var(--muted);
      line-height: 1.48;
    }
    .layout {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 18px;
    }
    .chips {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 14px;
    }
    .chip {
      padding: 9px 12px;
      border-radius: 999px;
      background: rgba(76, 201, 240, 0.12);
      border: 1px solid rgba(76, 201, 240, 0.22);
      font-size: 0.92rem;
    }
    .list {
      margin: 0;
      padding-left: 18px;
    }
    .list li { margin-bottom: 8px; }
    label {
      display: block;
      margin: 12px 0 6px;
      color: #dbf0ff;
      font-size: 0.94rem;
    }
    input, textarea, button, pre {
      width: 100%;
      border-radius: 14px;
      border: 1px solid rgba(255,255,255,0.1);
      font: inherit;
    }
    input, textarea {
      padding: 12px 14px;
      color: var(--text);
      background: rgba(255,255,255,0.04);
    }
    textarea { resize: vertical; min-height: 220px; }
    .actions {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
      margin-top: 14px;
    }
    button {
      cursor: pointer;
      font-weight: 800;
      padding: 13px 16px;
      transition: transform 120ms ease, filter 120ms ease;
    }
    button:hover {
      transform: translateY(-1px);
      filter: brightness(1.04);
    }
    .primary {
      background: linear-gradient(135deg, var(--accent), #ffbe5c);
      color: #08111a;
    }
    .secondary {
      background: linear-gradient(135deg, var(--accent-2), #8ae0ff);
      color: #08111a;
    }
    .response-head {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: center;
      flex-wrap: wrap;
      margin-bottom: 12px;
    }
    .badges {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }
    .badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 9px 12px;
      border-radius: 999px;
      border: 1px solid rgba(255,255,255,0.08);
      background: rgba(255,255,255,0.04);
      color: var(--muted);
      font-size: 0.92rem;
    }
    .badge.ok { color: var(--ok); }
    .badge.warn { color: var(--warn); }
    .badge.danger { color: var(--danger); }
    .summary-card { margin-bottom: 14px; display: none; }
    .summary-card.visible { display: block; }
    .summary-item {
      padding: 12px;
      border-radius: 16px;
      background: rgba(0,0,0,0.16);
      border: 1px solid rgba(255,255,255,0.06);
    }
    .summary-item strong {
      font-size: 0.78rem;
      color: var(--muted);
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }
    .cards {
      display: grid;
      gap: 12px;
      margin-bottom: 14px;
    }
    .result-card header {
      display: flex;
      justify-content: space-between;
      gap: 10px;
      margin-bottom: 10px;
      flex-wrap: wrap;
    }
    pre {
      margin: 0;
      padding: 16px;
      background: rgba(2, 7, 17, 0.92);
      color: #c7f9cc;
      overflow: auto;
    }
    code.inline {
      color: #fff1b8;
      background: rgba(255,255,255,0.06);
      padding: 2px 6px;
      border-radius: 6px;
    }
    @media (max-width: 920px) {
      .hero-grid, .layout { grid-template-columns: 1fr; }
    }
    @media (max-width: 640px) {
      .shell { width: min(100% - 18px, 1200px); padding-top: 18px; }
      .actions { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <main class="shell">
    <section class="hero">
      <p class="eyebrow">Caso G · Nivel 6 · Event Driven</p>
      <h1>Desacoplar para escalar sin bloquear el flujo</h1>
      <p class="lead">
        Esta API demuestra como pasar de una operacion sincrona a un flujo asincrono en AWS.
        Aqui no intentamos procesarlo todo en la misma llamada HTTP: aceptamos el evento,
        lo publicamos en <code class="inline">EventBridge</code>, lo amortiguamos en
        <code class="inline">SQS</code>, lo procesamos con una Lambda dedicada y aislamos
        fallos con <code class="inline">DLQ</code>.
      </p>

      <div class="hero-grid">
        <div class="mini-panel">
          <h2>Que estas haciendo aqui</h2>
          <div class="story">
            <article class="story-card">
              <strong>Publicar un hecho de negocio</strong>
              <p>En vez de invocar servicios acoplados en cadena, publicas un evento <code class="inline">OrderCreated</code> que otros componentes pueden consumir sin romper al productor.</p>
            </article>
            <article class="story-card">
              <strong>Separar entrada y procesamiento</strong>
              <p>La API responde rapido con <code class="inline">202 Accepted</code> porque aceptar un evento no significa procesarlo en ese mismo instante.</p>
            </article>
            <article class="story-card">
              <strong>Preparar una plataforma operable</strong>
              <p>El patron permite absorber picos, reintentar errores y construir observabilidad sobre colas, consumidores y mensajes fallidos.</p>
            </article>
          </div>
        </div>

        <div class="mini-panel">
          <h2>Estado del despliegue</h2>
          <div class="stats">
            <div class="stat">
              <strong>VALIDADO</strong>
              <span>Stack desplegado en us-east-2</span>
            </div>
            <div class="stat">
              <strong>202</strong>
              <span>Respuesta esperada al publicar eventos</span>
            </div>
            <div class="stat">
              <strong>DLQ</strong>
              <span>Mensajes fallidos quedan aislados</span>
            </div>
            <div class="stat">
              <strong>SNS</strong>
              <span>Notificacion posterior al procesamiento</span>
            </div>
          </div>
          <div class="chips">
            <span class="chip">Bus: __EVENT_BUS_NAME__</span>
            <span class="chip">Ruta: POST /events/orders</span>
            <span class="chip">Health: GET /health</span>
            <span class="chip">Patron: OrderCreated</span>
          </div>
        </div>
      </div>
    </section>

    <section class="panel">
      <h2>Por que este despliegue importa</h2>
      <div class="story">
        <article class="story-card">
          <strong>Que problema resuelve</strong>
          <p>Evita que una API de entrada quede esperando tareas lentas o fragiles como notificaciones, integraciones o enriquecimiento de datos.</p>
        </article>
        <article class="story-card">
          <strong>Que ganaste al sumarlo</strong>
          <p>Ahora tienes desacoplamiento, capacidad de reintento, tolerancia a picos y una base natural para alarmas, metricas y trazas futuras.</p>
        </article>
        <article class="story-card">
          <strong>Como se conecta con el portafolio</strong>
          <p>Extiende el Caso E: primero persistes o aceptas un hecho, luego lo conviertes en evento y habilitas procesamiento asincrono sin tocar al cliente.</p>
        </article>
      </div>
    </section>

    <section class="panel">
      <h2>Consideraciones agregadas al despliegue</h2>
      <div class="layout">
        <div class="mini-panel">
          <ul class="list">
            <li><strong>Respuesta asincrona:</strong> se usa <code class="inline">202 Accepted</code> para expresar que el trabajo quedo aceptado, no finalizado.</li>
            <li><strong>Regla de EventBridge:</strong> filtra por <code class="inline">source</code> y <code class="inline">detail-type</code> para mantener contratos claros.</li>
            <li><strong>SQS como buffer:</strong> desacopla la velocidad de entrada del ritmo del consumidor.</li>
            <li><strong>DLQ:</strong> evita perder mensajes cuando el consumidor falla varias veces.</li>
          </ul>
        </div>
        <div class="mini-panel">
          <ul class="list">
            <li><strong>SNS al final:</strong> deja listo un punto de extension para alertas o integraciones posteriores.</li>
            <li><strong>Payload trazable:</strong> cada evento incluye <code class="inline">orderId</code>, <code class="inline">customerId</code> y timestamp.</li>
            <li><strong>Prueba de error:</strong> puedes enviar <code class="inline">forceFailure: true</code> para validar la ruta de DLQ.</li>
            <li><strong>Observabilidad futura:</strong> este patron prepara naturalmente el terreno para el Caso H.</li>
          </ul>
        </div>
      </div>
    </section>

    <section class="panel">
      <h2>Demo en vivo del flujo</h2>
      <label for="payload">Payload a publicar</label>
      <textarea id="payload">{
  "orderId": "ord-demo-landing",
  "customerId": "cust-landing-001",
  "customerName": "Acme SPA",
  "status": "CREATED",
  "total": 249.90,
  "items": [
    { "sku": "sku-erp", "quantity": 1 }
  ]
}</textarea>
      <div class="helper">
        Consejo: agrega <code class="inline">"forceFailure": true</code> si quieres probar el camino de error hacia la DLQ.
      </div>
      <div class="actions">
        <button id="healthBtn" class="secondary" type="button">Probar health</button>
        <button id="publishBtn" class="primary" type="button">Publicar evento</button>
      </div>
    </section>

    <section class="panel">
      <div class="response-head">
        <h2>Respuesta y lectura de negocio</h2>
        <div class="badges">
          <span id="statusBadge" class="badge">Esperando accion</span>
          <span class="badge ok">Arquitectura desacoplada</span>
          <span class="badge warn">Procesamiento asincrono</span>
        </div>
      </div>

      <div id="summaryCard" class="summary-card">
        <strong>Que significa esta respuesta</strong>
        <div id="statusText" class="status"></div>
        <div id="summaryGrid" class="summary-grid"></div>
      </div>

      <div class="cards">
        <article class="result-card">
          <header>
            <strong>JSON completo</strong>
            <span class="status">Ideal para validar el contrato del evento</span>
          </header>
          <pre id="output">Esperando acciones...</pre>
        </article>
      </div>
    </section>
  </main>

  <script>
    const payloadEl = document.getElementById("payload");
    const outputEl = document.getElementById("output");
    const statusBadgeEl = document.getElementById("statusBadge");
    const summaryCardEl = document.getElementById("summaryCard");
    const statusTextEl = document.getElementById("statusText");
    const summaryGridEl = document.getElementById("summaryGrid");

    function writeOutput(title, payload) {
      outputEl.textContent = title + "\\n\\n" + JSON.stringify(payload, null, 2);
    }

    function setBadge(label, kind) {
      statusBadgeEl.className = "badge";
      if (kind) {
        statusBadgeEl.classList.add(kind);
      }
      statusBadgeEl.textContent = label;
    }

    function renderSummary(items, message) {
      summaryCardEl.classList.add("visible");
      statusTextEl.textContent = message;
      summaryGridEl.innerHTML = items.map(function(item) {
        return '<div class="summary-item"><strong>' + item.label + '</strong><span>' + item.value + '</span></div>';
      }).join("");
    }

    async function readResponse(response) {
      const text = await response.text();
      try {
        return JSON.parse(text);
      } catch (_error) {
        return { raw: text };
      }
    }

    document.getElementById("healthBtn").addEventListener("click", async function() {
      setBadge("Consultando health", "warn");
      try {
        const response = await fetch("/health");
        const data = await readResponse(response);
        writeOutput("Health check", { status: response.status, data: data });
        renderSummary(
          [
            { label: "HTTP", value: String(response.status) },
            { label: "Servicio", value: data.service || "caso-g-event-driven" },
            { label: "Bus", value: data.eventBus || "__EVENT_BUS_NAME__" }
          ],
          "La API esta viva y lista para aceptar eventos. Este paso valida la puerta de entrada antes de probar el flujo asincrono."
        );
        setBadge("Health OK", "ok");
      } catch (error) {
        writeOutput("Error", { message: error.message });
        renderSummary([], "La validacion de health fallo. Revisa la API antes de probar la publicacion de eventos.");
        setBadge("Health con error", "danger");
      }
    });

    document.getElementById("publishBtn").addEventListener("click", async function() {
      let payload;
      try {
        payload = JSON.parse(payloadEl.value);
      } catch (_error) {
        writeOutput("Error", { message: "El payload no es JSON valido." });
        renderSummary([], "Primero corrige el JSON. El contrato del evento es importante porque EventBridge y los consumidores dependen de el.");
        setBadge("Payload invalido", "danger");
        return;
      }

      setBadge("Publicando evento", "warn");
      try {
        const response = await fetch("/events/orders", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
        const data = await readResponse(response);
        writeOutput("Publicacion de evento", { status: response.status, data: data });

        const detail = data.detail || {};
        renderSummary(
          [
            { label: "HTTP", value: String(response.status) },
            { label: "Event ID", value: data.eventId || "Sin eventId" },
            { label: "Order ID", value: detail.orderId || payload.orderId || "Autogenerado" },
            { label: "Customer", value: detail.customerId || payload.customerId || "N/D" }
          ],
          response.status === 202
            ? "La API acepto el evento y lo entrego al flujo asincrono. Ahora el procesamiento ocurre fuera de esta llamada HTTP."
            : "La API no acepto el evento. Revisa la estructura del payload y los logs del productor."
        );

        setBadge(response.status === 202 ? "Evento aceptado" : "Publicacion con error", response.status === 202 ? "ok" : "danger");
      } catch (error) {
        writeOutput("Error", { message: error.message });
        renderSummary([], "No se pudo publicar el evento. Revisa conectividad, CORS o estado de la API.");
        setBadge("Error de red", "danger");
      }
    });
  </script>
</body>
</html>
"""


def _json_response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(body),
    }


def _html_response(html):
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/html; charset=utf-8",
            "Access-Control-Allow-Origin": "*",
        },
        "body": html,
    }


def _utc_now():
    return datetime.now(timezone.utc).isoformat()


def publisher_handler(event, _context):
    route_method = (event.get("requestContext") or {}).get("http", {}).get("method", "")
    raw_path = event.get("rawPath", "")

    if route_method == "GET" and raw_path == "/":
        return _html_response(LANDING_PAGE.replace("__EVENT_BUS_NAME__", EVENT_BUS_NAME))

    if route_method == "GET" and raw_path == "/health":
        return _json_response(
            200,
            {
                "status": "ok",
                "service": "caso-g-event-driven",
                "timestamp": _utc_now(),
                "eventBus": EVENT_BUS_NAME,
            },
        )

    try:
        body = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return _json_response(400, {"error": "Invalid JSON body"})

    order_id = body.get("orderId") or f"ord-{uuid.uuid4().hex[:10]}"
    customer_id = body.get("customerId")

    if not customer_id:
        return _json_response(400, {"error": "customerId is required"})

    detail = {
        "orderId": order_id,
        "customerId": customer_id,
        "customerName": body.get("customerName", "Unknown customer"),
        "status": body.get("status", "CREATED"),
        "total": body.get("total", 0),
        "items": body.get("items", []),
        "forceFailure": body.get("forceFailure", False),
        "createdAt": _utc_now(),
    }

    result = events_client.put_events(
        Entries=[
            {
                "Source": "caso.g.orders",
                "DetailType": "OrderCreated",
                "Detail": json.dumps(detail),
                "EventBusName": EVENT_BUS_NAME,
            }
        ]
    )

    failed = result.get("FailedEntryCount", 0)
    if failed:
        return _json_response(
            500,
            {
                "error": "EventBridge rejected the event",
                "details": result.get("Entries", []),
            },
        )

    entry = (result.get("Entries") or [{}])[0]

    return _json_response(
        202,
        {
            "message": "Event accepted for asynchronous processing",
            "eventId": entry.get("EventId"),
            "bus": EVENT_BUS_NAME,
            "detailType": "OrderCreated",
            "detail": detail,
        },
    )


def consumer_handler(event, _context):
    processed = []

    for record in event.get("Records", []):
        body = json.loads(record["body"])
        detail = body.get("detail", {})
        if isinstance(detail, str):
            detail = json.loads(detail)

        if detail.get("forceFailure"):
            raise RuntimeError(
                f"Forced failure for order {detail.get('orderId', 'unknown-order')}"
            )

        summary = {
            "orderId": detail["orderId"],
            "customerId": detail["customerId"],
            "status": "PROCESSED",
            "processedAt": _utc_now(),
        }

        if NOTIFICATIONS_TOPIC_ARN:
            sns_client.publish(
                TopicArn=NOTIFICATIONS_TOPIC_ARN,
                Subject="Caso G order processed",
                Message=json.dumps(summary),
            )

        processed.append(summary)

    return {"processed": processed, "count": len(processed)}
