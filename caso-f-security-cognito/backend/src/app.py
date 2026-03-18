import json
import os
from datetime import datetime, timezone

import boto3
from botocore.exceptions import ClientError


COGNITO_CLIENT_ID = os.environ.get("COGNITO_CLIENT_ID", "")
COGNITO_USER_POOL_ID = os.environ.get("COGNITO_USER_POOL_ID", "")

cognito_client = boto3.client("cognito-idp")


# ---------------------------------------------------------------------------
# Landing Page HTML
# ---------------------------------------------------------------------------
LANDING_PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Caso F | Security First</title>
  <style>
    :root {
      --bg: #07091b;
      --panel: rgba(12, 15, 40, 0.88);
      --panel-soft: rgba(255, 255, 255, 0.04);
      --line: rgba(168, 85, 247, 0.22);
      --text: #eef0ff;
      --muted: #9b9dc8;
      --accent: #c77dff;
      --accent-2: #7b2ff7;
      --ok: #7ef0b8;
      --warn: #ffd479;
      --danger: #ff9797;
      --shadow: 0 28px 70px rgba(0, 0, 0, 0.4);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0; font-family: "Segoe UI", sans-serif;
      color: var(--text);
      background:
        radial-gradient(circle at top left, rgba(123, 47, 247, 0.22), transparent 28%),
        radial-gradient(circle at right, rgba(199, 125, 255, 0.14), transparent 26%),
        linear-gradient(180deg, #07091b 0%, #0d0f2a 100%);
    }
    .shell { width: min(1200px, calc(100% - 28px)); margin: 0 auto; padding: 28px 0 56px; }
    .hero, .panel {
      border: 1px solid var(--line); border-radius: 24px;
      background: var(--panel); backdrop-filter: blur(16px); box-shadow: var(--shadow);
    }
    .hero { padding: 28px; margin-bottom: 18px; }
    .eyebrow { margin: 0 0 10px; color: var(--accent); text-transform: uppercase; letter-spacing: 0.18em; font-size: 0.78rem; }
    h1 { margin: 0; font-size: clamp(2.2rem, 6vw, 4.2rem); line-height: 0.96; }
    h2 { margin: 0 0 12px; font-size: 1.2rem; }
    .lead { color: var(--muted); max-width: 74ch; margin: 14px 0 0; line-height: 1.58; }
    .hero-grid { display: grid; grid-template-columns: 1.15fr 0.85fr; gap: 18px; margin-top: 22px; }
    .mini-panel { border-radius: 20px; border: 1px solid rgba(255,255,255,0.08); background: var(--panel-soft); padding: 16px; }
    .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 12px; }
    .stat { padding: 14px; border-radius: 18px; border: 1px solid rgba(255,255,255,0.08); background: rgba(255,255,255,0.04); }
    .stat strong { display: block; font-size: 1.3rem; margin-bottom: 4px; color: var(--accent); }
    .stat span { color: var(--muted); font-size: 0.9rem; }
    .panel { padding: 22px; margin-bottom: 18px; }
    .story { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; }
    .story-card { padding: 16px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.07); background: var(--panel-soft); }
    .story-card strong { display: block; margin-bottom: 6px; }
    .story-card p { margin: 0; color: var(--muted); line-height: 1.45; }
    .chips { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 14px; }
    .chip { padding: 9px 12px; border-radius: 999px; background: rgba(199,125,255,0.12); border: 1px solid rgba(199,125,255,0.24); font-size: 0.9rem; }
    .chip.green { background: rgba(126,240,184,0.12); border-color: rgba(126,240,184,0.24); color: var(--ok); }
    label { display: block; margin: 12px 0 6px; color: #d9d9ff; font-size: 0.94rem; }
    input {
      width: 100%; border-radius: 14px; border: 1px solid rgba(255,255,255,0.12);
      padding: 12px 14px; color: var(--text); background: rgba(255,255,255,0.05); font: inherit;
    }
    input:focus { outline: none; border-color: var(--accent); }
    button {
      width: 100%; cursor: pointer; font-weight: 800; padding: 13px 16px;
      border-radius: 14px; border: none; font: inherit;
      transition: transform 120ms ease, filter 120ms ease;
    }
    button:hover { transform: translateY(-1px); filter: brightness(1.08); }
    button:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
    .btn-primary { background: linear-gradient(135deg, var(--accent), var(--accent-2)); color: #fff; margin-top: 14px; }
    .btn-secondary { background: linear-gradient(135deg, #4cc9f0, #7b2ff7); color: #fff; margin-top: 10px; }
    .step-tabs { display: flex; gap: 0; margin-bottom: 20px; border-radius: 16px; overflow: hidden; border: 1px solid rgba(255,255,255,0.08); }
    .step-tab {
      flex: 1; padding: 12px; text-align: center; font-size: 0.88rem; font-weight: 700;
      background: rgba(255,255,255,0.03); color: var(--muted); cursor: default;
      border-right: 1px solid rgba(255,255,255,0.08); transition: background 200ms;
    }
    .step-tab:last-child { border-right: none; }
    .step-tab.active { background: rgba(199,125,255,0.15); color: var(--accent); }
    .step-tab.done { background: rgba(126,240,184,0.1); color: var(--ok); }
    .step-panel { display: none; }
    .step-panel.visible { display: block; }
    .response-head { display: flex; justify-content: space-between; gap: 12px; align-items: center; flex-wrap: wrap; margin-bottom: 12px; }
    .badges { display: flex; flex-wrap: wrap; gap: 10px; }
    .badge {
      display: inline-flex; align-items: center; gap: 8px; padding: 9px 12px;
      border-radius: 999px; border: 1px solid rgba(255,255,255,0.08);
      background: rgba(255,255,255,0.04); color: var(--muted); font-size: 0.9rem;
    }
    .badge.ok { color: var(--ok); border-color: rgba(126,240,184,0.2); }
    .badge.warn { color: var(--warn); }
    .badge.danger { color: var(--danger); }
    pre {
      margin: 0; padding: 16px; border-radius: 14px;
      background: rgba(2, 4, 20, 0.92); border: 1px solid rgba(255,255,255,0.06);
      color: #c7c9ff; overflow: auto; min-height: 100px; font-size: 0.88rem;
    }
    .helper { color: var(--muted); font-size: 0.9rem; margin-top: 8px; line-height: 1.48; }
    code.inline { color: #c77dff; background: rgba(199,125,255,0.1); padding: 2px 6px; border-radius: 6px; }
    .token-box {
      margin-top: 14px; padding: 14px; border-radius: 16px;
      background: rgba(126,240,184,0.06); border: 1px solid rgba(126,240,184,0.16);
      word-break: break-all; font-size: 0.82rem; color: var(--ok); font-family: monospace;
    }
    .waf-note { padding: 16px; border-radius: 18px; background: rgba(255,148,71,0.08); border: 1px solid rgba(255,148,71,0.22); color: var(--warn); margin-top: 14px; font-size: 0.9rem; }
    @media (max-width: 900px) { .hero-grid { grid-template-columns: 1fr; } }
    @media (max-width: 640px) { .shell { width: min(100% - 18px, 1200px); } .step-tab { font-size: 0.78rem; padding: 10px 6px; } }
  </style>
</head>
<body>
  <main class="shell">
    <section class="hero">
      <p class="eyebrow">Caso F · Nivel 5 · Security First</p>
      <h1>Identidad y perimetro: Cognito + JWT + WAF</h1>
      <p class="lead">
        Esta demo implementa el modelo de seguridad perimetral en AWS.
        Rutas publicas para autenticacion, rutas protegidas con token JWT validado
        por API Gateway y WAF opcional para bloquear trafico malicioso antes de que
        llegue a tu codigo.
      </p>
      <div class="hero-grid">
        <div class="mini-panel">
          <div class="stats">
            <div class="stat"><strong>JWT</strong><span>Validado por API GW</span></div>
            <div class="stat"><strong>Cognito</strong><span>User Pool + Auth Flow</span></div>
            <div class="stat"><strong>WAF</strong><span>Opcional (2 reglas managed)</span></div>
            <div class="stat"><strong>0 config</strong><span>manual de JWT en Lambda</span></div>
          </div>
          <div class="chips">
            <span class="chip">POST /auth/register</span>
            <span class="chip">POST /auth/login</span>
            <span class="chip green">GET /profile (protegido)</span>
            <span class="chip">GET /health</span>
          </div>
        </div>
        <div class="mini-panel">
          <h2>Que hace cada capa</h2>
          <div class="story">
            <article class="story-card">
              <strong>Cognito User Pool</strong>
              <p>Gestiona identidades: registro, login y emision de tokens JWT estandar.</p>
            </article>
            <article class="story-card">
              <strong>JWT Authorizer</strong>
              <p>API Gateway valida el token sin que tu Lambda escriba ni una linea de criptografia.</p>
            </article>
            <article class="story-card">
              <strong>WAF (opcional)</strong>
              <p>Bloquea SQLi, XSS e IPs con mala reputacion antes de que el trafico llegue al API.</p>
            </article>
          </div>
        </div>
      </div>
    </section>

    <section class="panel">
      <h2>Demo en vivo del flujo completo</h2>
      <p class="helper">Sigue los tres pasos: registrate, inicia sesion y llama al endpoint protegido con tu token JWT.</p>

      <div class="step-tabs">
        <div class="step-tab active" id="tab-1">1. Registrar</div>
        <div class="step-tab" id="tab-2">2. Iniciar sesion</div>
        <div class="step-tab" id="tab-3">3. Perfil protegido</div>
      </div>

      <div class="step-panel visible" id="panel-1">
        <label for="reg-email">Email</label>
        <input id="reg-email" type="email" placeholder="tu@email.com" />
        <label for="reg-password">Contrasena (min. 8 caracteres, mayuscula y numero)</label>
        <input id="reg-password" type="password" placeholder="MinSegura1!" />
        <button class="btn-primary" id="btn-register">Crear cuenta en Cognito</button>
        <p class="helper" id="reg-msg"></p>
      </div>

      <div class="step-panel" id="panel-2">
        <label for="login-email">Email</label>
        <input id="login-email" type="email" placeholder="tu@email.com" />
        <label for="login-password">Contrasena</label>
        <input id="login-password" type="password" placeholder="MinSegura1!" />
        <button class="btn-primary" id="btn-login">Iniciar sesion y obtener JWT</button>
        <p class="helper" id="login-msg"></p>
        <div id="token-display" style="display:none">
          <p class="helper">Token JWT obtenido (Access Token):</p>
          <div class="token-box" id="token-value"></div>
        </div>
      </div>

      <div class="step-panel" id="panel-3">
        <p class="helper">Con el token JWT en memoria, llama al endpoint <code class="inline">GET /profile</code>. API Gateway valida el token automaticamente antes de pasarlo a la Lambda.</p>
        <button class="btn-secondary" id="btn-profile">Llamar /profile con JWT</button>
        <p class="helper" id="profile-msg"></p>
      </div>
    </section>

    <section class="panel">
      <div class="response-head">
        <h2>Respuesta</h2>
        <div class="badges">
          <span class="badge" id="statusBadge">Esperando accion</span>
          <span class="badge ok">JWT valido por API GW</span>
          <span class="badge warn">Cognito User Pool activo</span>
        </div>
      </div>
      <pre id="output">Completa los pasos del formulario para ver la respuesta de la API...</pre>
    </section>

    <section class="panel">
      <h2>Por que este caso importa</h2>
      <div class="story">
        <article class="story-card">
          <strong>Sin codigo de criptografia</strong>
          <p>La validacion JWT la hace API Gateway nativamente con el JWT Authorizer de Cognito. Tu Lambda nunca toca el token.</p>
        </article>
        <article class="story-card">
          <strong>Perimetro antes de la logica</strong>
          <p>WAF bloquea SQLi, XSS e IPs maliciosas antes de que el trafico llegue a API Gateway. Dos capas de defensa independientes.</p>
        </article>
        <article class="story-card">
          <strong>Prerequisito para el Caso I</strong>
          <p>Los endpoints de IA generativa necesitan autenticacion y perimetro antes de exponerse. Caso F habilita Caso I.</p>
        </article>
      </div>
      <div class="waf-note">
        WAF WebACL tiene un costo base de ~$5 USD/mes independiente del trafico. Para demos, se despliega con
        <code class="inline">DeployWAF=false</code> (por defecto) y se activa solo cuando el caso requiere validacion real del perimetro.
        Destruye siempre con <code class="inline">sam delete</code> al terminar.
      </div>
    </section>
  </main>

  <script>
    const BASE = window.location.origin;
    const outputEl = document.getElementById("output");
    const statusBadgeEl = document.getElementById("statusBadge");
    let accessToken = null;
    let currentEmail = "";

    function setBadge(label, kind) {
      statusBadgeEl.className = "badge";
      if (kind) statusBadgeEl.classList.add(kind);
      statusBadgeEl.textContent = label;
    }

    function showOutput(data) {
      outputEl.textContent = JSON.stringify(data, null, 2);
    }

    function activateStep(step) {
      document.querySelectorAll(".step-tab").forEach((t, i) => {
        t.classList.remove("active", "done");
        if (i + 1 < step) t.classList.add("done");
        if (i + 1 === step) t.classList.add("active");
      });
      document.querySelectorAll(".step-panel").forEach((p, i) => {
        p.classList.toggle("visible", i + 1 === step);
      });
    }

    async function apiCall(path, options) {
      const response = await fetch(BASE + path, {
        headers: { "Content-Type": "application/json", ...((options || {}).headers || {}) },
        ...options,
      });
      const text = await response.text();
      try { return { status: response.status, data: JSON.parse(text) }; }
      catch (_) { return { status: response.status, data: { raw: text } }; }
    }

    document.getElementById("btn-register").addEventListener("click", async () => {
      const email = document.getElementById("reg-email").value.trim();
      const password = document.getElementById("reg-password").value;
      const msgEl = document.getElementById("reg-msg");

      if (!email || !password) { msgEl.textContent = "Completa email y contrasena."; return; }
      msgEl.textContent = "Registrando...";
      setBadge("Registrando...", "warn");

      const { status, data } = await apiCall("/auth/register", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });

      showOutput({ step: "register", status, data });
      if (status === 201) {
        currentEmail = email;
        msgEl.textContent = "Cuenta creada. Avanza al paso 2.";
        setBadge("Registro OK", "ok");
        document.getElementById("login-email").value = email;
        document.getElementById("login-password").value = password;
        activateStep(2);
      } else {
        msgEl.textContent = data.error || "Error al registrar.";
        setBadge("Error registro", "danger");
      }
    });

    document.getElementById("btn-login").addEventListener("click", async () => {
      const email = document.getElementById("login-email").value.trim();
      const password = document.getElementById("login-password").value;
      const msgEl = document.getElementById("login-msg");

      if (!email || !password) { msgEl.textContent = "Completa email y contrasena."; return; }
      msgEl.textContent = "Autenticando...";
      setBadge("Autenticando...", "warn");

      const { status, data } = await apiCall("/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });

      showOutput({ step: "login", status, data: { ...data, accessToken: data.accessToken ? data.accessToken.slice(0, 40) + "..." : undefined } });

      if (status === 200) {
        accessToken = data.accessToken;
        msgEl.textContent = "Token JWT obtenido. Avanza al paso 3.";
        setBadge("Login OK — JWT obtenido", "ok");
        document.getElementById("token-display").style.display = "block";
        document.getElementById("token-value").textContent = (accessToken || "").slice(0, 80) + "...";
        activateStep(3);
      } else {
        msgEl.textContent = data.error || "Credenciales incorrectas.";
        setBadge("Error login", "danger");
      }
    });

    document.getElementById("btn-profile").addEventListener("click", async () => {
      const msgEl = document.getElementById("profile-msg");
      if (!accessToken) { msgEl.textContent = "Primero inicia sesion para obtener el token."; return; }
      msgEl.textContent = "Llamando /profile...";
      setBadge("Consultando perfil...", "warn");

      const { status, data } = await apiCall("/profile", {
        method: "GET",
        headers: { Authorization: accessToken },
      });

      showOutput({ step: "profile", status, data });
      if (status === 200) {
        msgEl.textContent = "Perfil obtenido. El token JWT fue validado por API Gateway automaticamente.";
        setBadge("Perfil OK — JWT validado", "ok");
      } else {
        msgEl.textContent = data.error || "Token invalido o expirado.";
        setBadge("Token rechazado", "danger");
      }
    });
  </script>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _utc_now():
    return datetime.now(timezone.utc).isoformat()


def _json_response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(body, ensure_ascii=False),
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


def _load_body(event):
    raw = event.get("body") or "{}"
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError("JSON invalido") from exc


def _require_fields(data, fields):
    missing = [f for f in fields if not str(data.get(f) or "").strip()]
    if missing:
        raise ValueError(f"Campos requeridos: {', '.join(missing)}")


def _cognito_error_response(exc):
    code = exc.response["Error"]["Code"]
    error_map = {
        "UsernameExistsException": (409, "El usuario ya existe con ese email."),
        "NotAuthorizedException": (401, "Email o contrasena incorrectos."),
        "UserNotConfirmedException": (403, "Cuenta no confirmada. Revisa tu email."),
        "InvalidPasswordException": (400, "La contrasena no cumple los requisitos: minimo 8 caracteres, mayuscula y numero."),
        "UserNotFoundException": (404, "Usuario no encontrado."),
        "TooManyRequestsException": (429, "Demasiados intentos. Espera un momento."),
        "LimitExceededException": (429, "Limite de intentos alcanzado. Espera un momento."),
        "InvalidParameterException": (400, "Parametros invalidos en la solicitud."),
    }
    status, message = error_map.get(code, (500, f"Error AWS Cognito: {code}"))
    return _json_response(status, {"ok": False, "error": message, "code": code})


# ---------------------------------------------------------------------------
# Route handlers
# ---------------------------------------------------------------------------

def handle_register(event):
    data = _load_body(event)
    _require_fields(data, ["email", "password"])

    email = str(data["email"]).strip().lower()
    password = str(data["password"])
    name = str(data.get("name") or email.split("@")[0]).strip()

    response = cognito_client.sign_up(
        ClientId=COGNITO_CLIENT_ID,
        Username=email,
        Password=password,
        UserAttributes=[
            {"Name": "email", "Value": email},
            {"Name": "name", "Value": name},
        ],
    )

    return _json_response(201, {
        "ok": True,
        "message": "Usuario registrado correctamente.",
        "userSub": response["UserSub"],
        "confirmed": response.get("UserConfirmed", False),
    })


def handle_login(event):
    data = _load_body(event)
    _require_fields(data, ["email", "password"])

    email = str(data["email"]).strip().lower()
    password = str(data["password"])

    response = cognito_client.initiate_auth(
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={
            "USERNAME": email,
            "PASSWORD": password,
        },
        ClientId=COGNITO_CLIENT_ID,
    )

    result = response["AuthenticationResult"]
    return _json_response(200, {
        "ok": True,
        "accessToken": result["AccessToken"],
        "idToken": result["IdToken"],
        "refreshToken": result["RefreshToken"],
        "tokenType": result["TokenType"],
        "expiresIn": result["ExpiresIn"],
    })


def handle_profile(event):
    # API Gateway JWT Authorizer inyecta los claims en requestContext.authorizer.jwt.claims
    authorizer = (event.get("requestContext") or {}).get("authorizer") or {}
    claims = authorizer.get("jwt", {}).get("claims", {})

    if not claims:
        return _json_response(401, {"ok": False, "error": "Token de autorizacion requerido."})

    return _json_response(200, {
        "ok": True,
        "email": claims.get("email", ""),
        "name": claims.get("name", claims.get("email", "")),
        "sub": claims.get("sub", ""),
        "emailVerified": claims.get("email_verified", False),
        "timestamp": _utc_now(),
    })


def handle_health(_event):
    return _json_response(200, {
        "status": "ok",
        "service": "caso-f-security",
        "cognito": "configured" if COGNITO_USER_POOL_ID else "not-configured",
        "timestamp": _utc_now(),
    })


# ---------------------------------------------------------------------------
# Cognito Pre-Signup Trigger
# ---------------------------------------------------------------------------

def pre_signup_trigger(event, _context):
    """Auto-confirma usuarios para entorno demo.
    NO usar en produccion — elimina el flujo de verificacion de email."""
    event["response"]["autoConfirmUser"] = True
    event["response"]["autoVerifyEmail"] = True
    return event


# ---------------------------------------------------------------------------
# Main handler
# ---------------------------------------------------------------------------

def handler(event, _context):
    request_ctx = (event.get("requestContext") or {}).get("http", {})
    method = request_ctx.get("method", "").upper()
    path = event.get("rawPath", "/")

    print(json.dumps({
        "method": method,
        "path": path,
        "service": "caso-f-security",
        "timestamp": _utc_now(),
    }))

    try:
        if method == "OPTIONS":
            return _json_response(200, {"ok": True})

        if path in ("/", ""):
            return _html_response(LANDING_PAGE)

        if path == "/health":
            return handle_health(event)

        if path == "/auth/register" and method == "POST":
            return handle_register(event)

        if path == "/auth/login" and method == "POST":
            return handle_login(event)

        if path == "/profile" and method == "GET":
            return handle_profile(event)

        return _json_response(404, {
            "ok": False,
            "error": "Ruta no encontrada.",
            "availableRoutes": ["GET /", "GET /health", "POST /auth/register", "POST /auth/login", "GET /profile"],
        })

    except ValueError as exc:
        return _json_response(400, {"ok": False, "error": str(exc)})
    except ClientError as exc:
        return _cognito_error_response(exc)
    except Exception as exc:
        return _json_response(500, {"ok": False, "error": "Error interno.", "detail": str(exc)})
