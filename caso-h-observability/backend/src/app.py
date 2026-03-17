import json
import os
from datetime import datetime, timezone

import boto3

STACK_NAME = os.environ.get("STACK_NAME", "caso-h-observability")
METRIC_NAMESPACE = os.environ.get("METRIC_NAMESPACE", "CasoH")

cloudwatch = boto3.client("cloudwatch")


# ---------------------------------------------------------------------------
# Landing Page HTML
# ---------------------------------------------------------------------------
LANDING_PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Caso H | Observability & Health</title>
  <style>
    :root {
      --bg: #07111b;
      --panel: rgba(10, 22, 38, 0.86);
      --panel-soft: rgba(255, 255, 255, 0.04);
      --line: rgba(115, 190, 255, 0.16);
      --text: #eef7ff;
      --muted: #9ab8cb;
      --accent: #4cc9f0;
      --accent-2: #7ef0b8;
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
        radial-gradient(circle at right, rgba(126, 240, 184, 0.18), transparent 22%),
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
    .story, .pillars {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 14px;
    }
    .story-card strong { display: block; margin-bottom: 6px; }
    .story-card p { color: var(--muted); line-height: 1.48; }
    .pillar {
      border-radius: 20px;
      border: 1px solid rgba(255,255,255,0.08);
      background: var(--panel-soft);
      padding: 18px;
    }
    .pillar-icon { font-size: 2rem; margin-bottom: 10px; }
    .pillar strong { display: block; margin-bottom: 4px; font-size: 1.05rem; }
    .pillar span { color: var(--muted); font-size: 0.9rem; line-height: 1.5; }
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
    .chip.green {
      background: rgba(126, 240, 184, 0.12);
      border-color: rgba(126, 240, 184, 0.22);
      color: var(--ok);
    }
    .actions {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
      gap: 10px;
      margin-top: 14px;
    }
    button {
      cursor: pointer;
      font-weight: 800;
      padding: 13px 16px;
      border-radius: 14px;
      border: none;
      font: inherit;
      transition: transform 120ms ease, filter 120ms ease;
    }
    button:hover { transform: translateY(-1px); filter: brightness(1.08); }
    .primary { background: linear-gradient(135deg, var(--accent), #8ae0ff); color: #08111a; }
    .secondary { background: linear-gradient(135deg, var(--accent-2), #b4ffd8); color: #08111a; }
    .links { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 14px; }
    a.link-btn {
      display: inline-block;
      text-decoration: none;
      padding: 12px 16px;
      border-radius: 14px;
      font-weight: 800;
      color: #08111a;
      background: linear-gradient(135deg, var(--accent), #8ae0ff);
    }
    .response-head {
      display: flex; justify-content: space-between; gap: 12px;
      align-items: center; flex-wrap: wrap; margin-bottom: 12px;
    }
    .badges { display: flex; flex-wrap: wrap; gap: 10px; }
    .badge {
      display: inline-flex; align-items: center; gap: 8px;
      padding: 9px 12px; border-radius: 999px;
      border: 1px solid rgba(255,255,255,0.08);
      background: rgba(255,255,255,0.04);
      color: var(--muted); font-size: 0.92rem;
    }
    .badge.ok { color: var(--ok); }
    .badge.warn { color: var(--warn); }
    .badge.danger { color: var(--danger); }
    pre {
      margin: 0; padding: 16px;
      background: rgba(2, 7, 17, 0.92);
      border-radius: 14px;
      border: 1px solid rgba(255,255,255,0.06);
      color: #c7f9cc; overflow: auto;
    }
    .result-card { margin-bottom: 0; }
    .result-card header {
      display: flex; justify-content: space-between;
      gap: 10px; margin-bottom: 10px; flex-wrap: wrap;
    }
    code.inline {
      color: #fff1b8; background: rgba(255,255,255,0.06);
      padding: 2px 6px; border-radius: 6px;
    }
    @media (max-width: 920px) { .hero-grid { grid-template-columns: 1fr; } }
    @media (max-width: 640px) {
      .shell { width: min(100% - 18px, 1200px); padding-top: 18px; }
    }
  </style>
</head>
<body>
  <main class="shell">
    <section class="hero">
      <p class="eyebrow">Caso H · Nivel 7 · Observability & Health</p>
      <h1>Convierte tu infraestructura en una caja de cristal</h1>
      <p class="lead">
        Este caso implementa los tres pilares de la observabilidad en AWS: <code class="inline">metricas</code>,
        <code class="inline">logs</code> y <code class="inline">trazas</code>. Cada invocacion queda registrada
        en CloudWatch. Cada salto entre servicios queda trazado en X-Ray.
        Las alarmas disparan antes de que el usuario note el problema.
      </p>

      <div class="hero-grid">
        <div class="mini-panel">
          <h2>Los tres pilares</h2>
          <div class="pillars">
            <div class="pillar">
              <div class="pillar-icon">📊</div>
              <strong>Metricas</strong>
              <span>CloudWatch: invocaciones, errores, latencia p99 y metricas custom de negocio en namespace <code class="inline">CasoH</code>.</span>
            </div>
            <div class="pillar">
              <div class="pillar-icon">📋</div>
              <strong>Logs</strong>
              <span>CloudWatch Logs con correlacion por traza. Queries con Logs Insights para analisis rapido.</span>
            </div>
            <div class="pillar">
              <div class="pillar-icon">🔗</div>
              <strong>Trazas</strong>
              <span>AWS X-Ray activo por SAM Globals. Service map, timeline y subsegmentos por invocacion.</span>
            </div>
          </div>
        </div>

        <div class="mini-panel">
          <h2>Estado del despliegue</h2>
          <div class="stats">
            <div class="stat">
              <strong>X-Ray</strong>
              <span>Tracing activo en todas las Lambdas</span>
            </div>
            <div class="stat">
              <strong>IaC</strong>
              <span>Dashboard definido en CloudFormation</span>
            </div>
            <div class="stat">
              <strong>2</strong>
              <span>Alarmas activas (errores y latencia)</span>
            </div>
            <div class="stat">
              <strong>CasoH</strong>
              <span>Namespace de metricas custom</span>
            </div>
          </div>
          <div class="chips">
            <span class="chip">GET /health</span>
            <span class="chip">POST /metrics</span>
            <span class="chip green">X-Ray ON</span>
            <span class="chip green">Dashboard IaC</span>
          </div>
        </div>
      </div>
    </section>

    <section class="panel">
      <h2>Por que este caso importa</h2>
      <div class="story">
        <article class="story-card">
          <strong>Que problema resuelve</strong>
          <p>Sin observabilidad, un error en produccion puede pasar horas sin detectarse. Con este caso, las alarmas disparan antes de que el usuario lo note y X-Ray te dice exactamente en que punto fallo.</p>
        </article>
        <article class="story-card">
          <strong>Que demuestra a un reclutador</strong>
          <p>Que defines observabilidad como codigo, no como configuracion manual. El dashboard y las alarmas nacen con el stack y mueren con el: cero deuda operativa.</p>
        </article>
        <article class="story-card">
          <strong>Como se conecta con el portafolio</strong>
          <p>Este caso instrumenta los endpoints de los Casos D, E y G. Cada invocacion de esas APIs genera trazas en X-Ray y metricas en CloudWatch que puedes ver en el dashboard.</p>
        </article>
      </div>
    </section>

    <section class="panel">
      <h2>Demo en vivo</h2>
      <div class="actions">
        <button id="healthBtn" class="secondary" type="button">Probar health check</button>
        <button id="metricsBtn" class="primary" type="button">Publicar metrica custom</button>
      </div>
      <div class="links">
        <a class="link-btn" href="/health">Health HTML</a>
        <a class="link-btn" href="/health?format=json">Health JSON</a>
      </div>
    </section>

    <section class="panel">
      <div class="response-head">
        <h2>Respuesta</h2>
        <div class="badges">
          <span id="statusBadge" class="badge">Esperando accion</span>
          <span class="badge ok">X-Ray trazado</span>
          <span class="badge warn">CloudWatch registrado</span>
        </div>
      </div>
      <div class="result-card">
        <header>
          <strong>JSON de respuesta</strong>
          <span style="color:var(--muted)">Cada llamada genera una traza en X-Ray</span>
        </header>
        <pre id="output">Esperando acciones...</pre>
      </div>
    </section>
  </main>

  <script>
    const outputEl = document.getElementById("output");
    const statusBadgeEl = document.getElementById("statusBadge");

    function setBadge(label, kind) {
      statusBadgeEl.className = "badge";
      if (kind) statusBadgeEl.classList.add(kind);
      statusBadgeEl.textContent = label;
    }

    async function readResponse(response) {
      const text = await response.text();
      try { return JSON.parse(text); } catch (_) { return { raw: text }; }
    }

    document.getElementById("healthBtn").addEventListener("click", async function() {
      setBadge("Consultando health...", "warn");
      try {
        const response = await fetch("/health?format=json");
        const data = await readResponse(response);
        outputEl.textContent = JSON.stringify({ status: response.status, data }, null, 2);
        setBadge("Health OK — traza registrada en X-Ray", "ok");
      } catch (error) {
        outputEl.textContent = JSON.stringify({ error: error.message }, null, 2);
        setBadge("Error de red", "danger");
      }
    });

    document.getElementById("metricsBtn").addEventListener("click", async function() {
      setBadge("Publicando metrica a CloudWatch...", "warn");
      try {
        const response = await fetch("/metrics", { method: "POST" });
        const data = await readResponse(response);
        outputEl.textContent = JSON.stringify({ status: response.status, data }, null, 2);
        setBadge(response.ok ? "Metrica publicada en CasoH/HealthChecks" : "Error al publicar", response.ok ? "ok" : "danger");
      } catch (error) {
        outputEl.textContent = JSON.stringify({ error: error.message }, null, 2);
        setBadge("Error de red", "danger");
      }
    });
  </script>
</body>
</html>"""


HEALTH_PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Caso H | Health Check</title>
  <style>
    :root {
      --bg: #08111a; --panel: rgba(10, 22, 38, 0.88);
      --line: rgba(126, 240, 184, 0.18); --text: #eef7ff; --muted: #9db9cb;
      --accent: #7ef0b8; --accent-2: #4cc9f0; --shadow: 0 28px 70px rgba(0,0,0,0.35);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0; font-family: "Segoe UI", sans-serif; color: var(--text);
      background:
        radial-gradient(circle at top left, rgba(76,201,240,0.18), transparent 24%),
        radial-gradient(circle at right, rgba(126,240,184,0.18), transparent 22%),
        linear-gradient(180deg, #07101a 0%, #0d1b2a 100%);
    }
    .shell { width: min(1000px, calc(100% - 28px)); margin: 0 auto; padding: 40px 0 60px; }
    .hero {
      border: 1px solid var(--line); border-radius: 24px;
      background: var(--panel); box-shadow: var(--shadow);
      backdrop-filter: blur(16px); padding: 32px; margin-bottom: 18px;
    }
    .eyebrow {
      margin: 0 0 10px; color: var(--accent);
      text-transform: uppercase; letter-spacing: 0.18em; font-size: 0.78rem;
    }
    h1 { margin: 0; font-size: clamp(1.8rem, 5vw, 3rem); }
    .lead { color: var(--muted); margin: 14px 0 0; line-height: 1.58; }
    .stats {
      display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
      gap: 12px; margin-top: 22px;
    }
    .stat {
      padding: 16px; border-radius: 18px;
      border: 1px solid rgba(255,255,255,0.08); background: rgba(255,255,255,0.04);
    }
    .stat strong { display: block; font-size: 1.3rem; margin-bottom: 4px; color: var(--accent); }
    .stat span { color: var(--muted); font-size: 0.9rem; }
    pre {
      margin: 22px 0 0; padding: 18px; border-radius: 18px;
      background: rgba(2,7,17,0.92); border: 1px solid rgba(255,255,255,0.08);
      color: #c7f9cc; overflow: auto;
    }
    .actions { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 22px; }
    a.button {
      display: inline-block; text-decoration: none; padding: 12px 18px;
      border-radius: 14px; font-weight: 800; color: #08111a;
      background: linear-gradient(135deg, var(--accent), #b4ffd8);
    }
    a.button.sec { background: linear-gradient(135deg, var(--accent-2), #8ae0ff); }
  </style>
</head>
<body>
  <main class="shell">
    <section class="hero">
      <p class="eyebrow">Caso H · Health Check · X-Ray Trazado</p>
      <h1>Estado operativo del servicio de observabilidad</h1>
      <p class="lead">
        Este endpoint confirma que la Lambda esta respondiendo y que X-Ray esta activo.
        En curl o scripts entrega JSON. En navegador muestra esta vista explicativa.
      </p>
      <div class="stats">
        <div class="stat">
          <strong>__HEALTH_STATUS__</strong>
          <span>Estado del servicio</span>
        </div>
        <div class="stat">
          <strong>X-Ray</strong>
          <span>__XRAY_STATUS__</span>
        </div>
        <div class="stat">
          <strong>CasoH</strong>
          <span>Namespace de metricas custom</span>
        </div>
        <div class="stat">
          <strong>us-east-2</strong>
          <span>Region de despliegue</span>
        </div>
      </div>
      <pre>__HEALTH_JSON__</pre>
      <div class="actions">
        <a class="button" href="/">Landing principal</a>
        <a class="button sec" href="/health?format=json">Ver como JSON</a>
      </div>
    </section>
  </main>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _utc_now():
    return datetime.now(timezone.utc).isoformat()


def _query_params(event):
    return event.get("queryStringParameters") or {}


def _wants_html(event):
    headers = event.get("headers") or {}
    accept = headers.get("accept") or headers.get("Accept") or ""
    user_agent = headers.get("user-agent") or headers.get("User-Agent") or ""
    force_json = (_query_params(event).get("format") or "").lower() == "json"
    if force_json:
        return False
    return "text/html" in accept.lower() or "mozilla" in user_agent.lower()


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


def _health_payload():
    return {
        "status": "ok",
        "service": STACK_NAME,
        "xray": "active",
        "metricNamespace": METRIC_NAMESPACE,
        "timestamp": _utc_now(),
    }


def _publish_metric():
    """Publica la metrica custom HealthChecks/Count en CloudWatch."""
    cloudwatch.put_metric_data(
        Namespace=METRIC_NAMESPACE,
        MetricData=[
            {
                "MetricName": "HealthChecks",
                "Dimensions": [
                    {"Name": "Service", "Value": STACK_NAME},
                ],
                "Value": 1,
                "Unit": "Count",
            }
        ],
    )


# ---------------------------------------------------------------------------
# Route handlers
# ---------------------------------------------------------------------------
def _handle_root(_event):
    return _html_response(LANDING_PAGE)


def _handle_health(event):
    payload = _health_payload()
    if _wants_html(event):
        health_json = json.dumps(payload, indent=2)
        html = HEALTH_PAGE.replace("__HEALTH_STATUS__", payload["status"])
        html = html.replace("__XRAY_STATUS__", payload["xray"])
        html = html.replace("__HEALTH_JSON__", health_json)
        return _html_response(html)
    return _json_response(200, payload)


def _handle_metrics(_event):
    try:
        _publish_metric()
        return _json_response(200, {
            "message": "Metrica publicada correctamente.",
            "namespace": METRIC_NAMESPACE,
            "metricName": "HealthChecks",
            "service": STACK_NAME,
            "timestamp": _utc_now(),
        })
    except Exception as exc:
        return _json_response(500, {
            "error": "No se pudo publicar la metrica.",
            "detail": str(exc),
            "timestamp": _utc_now(),
        })


# ---------------------------------------------------------------------------
# Main handler
# ---------------------------------------------------------------------------
def handler(event, _context):
    request_ctx = (event.get("requestContext") or {}).get("http", {})
    method = request_ctx.get("method", "GET").upper()
    path = event.get("rawPath", "/")

    print(json.dumps({
        "method": method,
        "path": path,
        "service": STACK_NAME,
        "timestamp": _utc_now(),
    }))

    if path == "/" or path == "":
        return _handle_root(event)
    if path == "/health":
        return _handle_health(event)
    if path == "/metrics" and method == "POST":
        return _handle_metrics(event)

    return _json_response(404, {
        "error": "Ruta no encontrada.",
        "availableRoutes": ["GET /", "GET /health", "POST /metrics"],
    })
