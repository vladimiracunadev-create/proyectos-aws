import json
import os
from datetime import datetime, timezone

import boto3
from botocore.exceptions import ClientError


COGNITO_CLIENT_ID = os.environ.get("COGNITO_CLIENT_ID", "")
COGNITO_USER_POOL_ID = os.environ.get("COGNITO_USER_POOL_ID", "")
DEPLOYMENT_MODE = os.environ.get("DEPLOYMENT_MODE", "demo-http-jwt")
PERIMETER_MODE = os.environ.get("PERIMETER_MODE", "native-authorizer")
SUPPORT_PAGE_URL = os.environ.get("SUPPORT_PAGE_URL", "").strip()
DEMO_PAGE_URL = os.environ.get("DEMO_PAGE_URL", "").strip()

cognito_client = boto3.client("cognito-idp")


# ---------------------------------------------------------------------------
# Landing Page HTML
# ---------------------------------------------------------------------------
DEMO_LANDING_PAGE = r"""<!DOCTYPE html>
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
    input, textarea {
      width: 100%; border-radius: 14px; border: 1px solid rgba(255,255,255,0.12);
      padding: 12px 14px; color: var(--text); background: rgba(255,255,255,0.05); font: inherit;
    }
    textarea { min-height: 124px; resize: vertical; }
    input:focus, textarea:focus { outline: none; border-color: var(--accent); }
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
    .hero-actions { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 16px; }
    .token-actions { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 12px; }
    .link-button {
      display: inline-flex; align-items: center; justify-content: center; min-height: 46px;
      padding: 12px 16px; border-radius: 14px; text-decoration: none; font-weight: 800;
      background: linear-gradient(135deg, #4cc9f0, #4361ee); color: #fff;
      border: 1px solid rgba(255,255,255,0.08);
    }
    .copy-btn {
      width: auto; background: rgba(255,255,255,0.06); color: var(--text);
      border: 1px solid rgba(255,255,255,0.1);
    }
    @media (max-width: 900px) { .hero-grid { grid-template-columns: 1fr; } }
    @media (max-width: 640px) { .shell { width: min(100% - 18px, 1200px); } .step-tab { font-size: 0.78rem; padding: 10px 6px; } }
  </style>
</head>
<body>
  <main class="shell">
    <section class="hero">
      <p class="eyebrow">Caso F · Nivel 5 · Security First</p>
      <h1>Identidad y perimetro: Cognito + Authorizer nativo + WAF</h1>
      <p class="lead">
        Estas viendo el producto completo del Caso F. Aqui demostramos identidad,
        autenticacion y autorizacion nativa con Cognito + HTTP API + JWT Authorizer,
        para resolver seguridad perimetral sin escribir criptografia manual en Lambda.
        El enlace WAF abre la evidencia complementaria del perimetro avanzado.
      </p>
      <div class="hero-grid">
        <div class="mini-panel">
          <div class="stats">
            <div class="stat"><strong>JWT</strong><span>Validado por API GW</span></div>
            <div class="stat"><strong>Cognito</strong><span>User Pool + Auth Flow</span></div>
            <div class="stat"><strong>WAF</strong><span>En pagina auxiliar enlazada</span></div>
            <div class="stat"><strong>0 crypto</strong><span>manual dentro de Lambda</span></div>
          </div>
          <div class="chips">
            <span class="chip">POST /auth/register</span>
            <span class="chip">POST /auth/login</span>
            <span class="chip green">GET /profile (protegido)</span>
            <span class="chip">GET /health</span>
          </div>
        </div>
        <div class="mini-panel">
          <h2>Que estas viendo y como se conecta con WAF</h2>
          <div class="story">
            <article class="story-card">
              <strong>Que estamos haciendo aqui</strong>
              <p>Validamos identidad real: crear usuario, iniciar sesion y abrir un endpoint protegido con claims entregados por Cognito.</p>
            </article>
            <article class="story-card">
              <strong>Que problema resuelve</strong>
              <p>Evita que la Lambda tenga que validar JWT manualmente. La verificacion ocurre antes, en API Gateway.</p>
            </article>
            <article class="story-card">
              <strong>Que ya demostraste al llegar a /profile</strong>
              <p>Que el usuario es autentico y que el token puede abrir una ruta protegida sin criptografia escrita a mano.</p>
            </article>
            <article class="story-card">
              <strong>Por que existe la pagina WAF</strong>
              <p>Porque la segunda capa no responde "quien eres", sino "que trafico ni siquiera deberia entrar". La veras con el mismo token, pero con otro front door.</p>
            </article>
          </div>
          <div class="hero-actions">
            __SUPPORT_LINK__
          </div>
        </div>
      </div>
    </section>

    <section class="panel">
      <h2>Producto en vivo: flujo completo de identidad</h2>
      <p class="helper">Sigue los tres pasos para ver lo que resuelve el producto: alta de usuario, emision de token y acceso protegido sin criptografia manual en la Lambda.</p>

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
        <button class="btn-primary" id="btn-login">Iniciar sesion y obtener tokens</button>
        <p class="helper" id="login-msg"></p>
        <div id="token-display" style="display:none">
          <p class="helper">Token recomendado para <code class="inline">GET /profile</code> (ID Token):</p>
          <div class="token-box" id="token-value"></div>
          <div class="token-actions">
            <button class="copy-btn" id="btn-copy-token" type="button">Copiar token para la pagina WAF</button>
          </div>
          <p class="helper" id="token-bridge-msg">Este mismo token se usa en la pagina WAF enlazada para demostrar que la identidad es la misma y lo que cambia es la capa perimetral.</p>
        </div>
      </div>

      <div class="step-panel" id="panel-3">
        <p class="helper">Con el token en memoria, llama al endpoint <code class="inline">GET /profile</code>. En este DEMO, API Gateway HTTP API valida el JWT automaticamente antes de invocar la Lambda.</p>
        <button class="btn-secondary" id="btn-profile">Llamar /profile con token</button>
        <p class="helper" id="profile-msg"></p>
      </div>
    </section>

    <section class="panel">
      <div class="response-head">
        <h2>Respuesta</h2>
        <div class="badges">
          <span class="badge" id="statusBadge">Esperando accion</span>
          <span class="badge ok">Authorizer nativo activo</span>
          <span class="badge warn">Cognito User Pool activo</span>
        </div>
      </div>
      <pre id="output">Completa los pasos del formulario para ver la respuesta de la API...</pre>
    </section>

    <section class="panel">
      <h2>Por que este caso importa</h2>
      <div class="story">
        <article class="story-card">
          <strong>Primera capa: identidad</strong>
          <p>Este DEMO responde "quien eres". Cognito emite el token y API Gateway comprueba que ese token es valido antes de llegar a tu codigo.</p>
        </article>
        <article class="story-card">
          <strong>Segunda capa: perimetro</strong>
          <p>La pagina WAF responde "que solicitudes se frenan antes de entrar". Ahi veras bloqueos 403 por trafico sospechoso antes de API Gateway.</p>
        </article>
        <article class="story-card">
          <strong>Por que no es la misma URL</strong>
          <p>AWS permite JWT Authorizer nativo en HTTP API, pero WAF se asocia a REST API. Por eso el aprendizaje se divide en dos front doors conectados a la misma historia de seguridad.</p>
        </article>
      </div>
      <div class="waf-note">
        DEMO principal: <code class="inline">backend/template.yaml</code> con HTTP API, Cognito y JWT Authorizer.
        Cuando termines <code class="inline">GET /profile</code>, abre la pagina WAF y usa este mismo token para ver la segunda capa. El costo temporal y la ventana de uso se documentan en <code class="inline">VISUALIZATION.md</code>.
      </div>
    </section>
  </main>

  <script>
    const outputEl = document.getElementById("output");
    const statusBadgeEl = document.getElementById("statusBadge");
    let profileToken = null;

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

    function buildUrl(path) {
      const pagePath = window.location.pathname || "/";
      const basePath = pagePath === "/" ? "/" : pagePath.replace(/\/?$/, "/");
      const cleanPath = String(path || "").replace(/^\/+/, "");
      return `${window.location.origin}${basePath}${cleanPath}`;
    }

    async function apiCall(path, options) {
      const response = await fetch(buildUrl(path), {
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

      showOutput({
        step: "login",
        status,
        data: {
          ...data,
          accessToken: data.accessToken ? data.accessToken.slice(0, 40) + "..." : undefined,
          idToken: data.idToken ? data.idToken.slice(0, 40) + "..." : undefined,
          refreshToken: data.refreshToken ? data.refreshToken.slice(0, 40) + "..." : undefined,
        },
      });

      if (status === 200) {
        profileToken = data.idToken || data.accessToken;
        msgEl.textContent = "Tokens emitidos. Avanza al paso 3 y luego reutiliza este mismo token en la pagina WAF.";
        setBadge("Login OK - token del DEMO listo", "ok");
        document.getElementById("token-display").style.display = "block";
        document.getElementById("token-value").textContent = (profileToken || "").slice(0, 80) + "...";
        activateStep(3);
      } else {
        msgEl.textContent = data.error || "Credenciales incorrectas.";
        setBadge("Error login", "danger");
      }
    });

    document.getElementById("btn-profile").addEventListener("click", async () => {
      const msgEl = document.getElementById("profile-msg");
      if (!profileToken) { msgEl.textContent = "Primero inicia sesion para obtener el token."; return; }
      msgEl.textContent = "Llamando /profile...";
      setBadge("Consultando perfil...", "warn");

      const { status, data } = await apiCall("/profile", {
        method: "GET",
        headers: { Authorization: `Bearer ${profileToken}` },
      });

      showOutput({ step: "profile", status, data });
      if (status === 200) {
        msgEl.textContent = "Perfil obtenido. Ya validaste identidad. El siguiente paso es abrir la pagina WAF y probar este mismo token en la segunda capa.";
        setBadge("Perfil OK - identidad demostrada", "ok");
      } else {
        msgEl.textContent = data.error || "Token invalido o expirado.";
        setBadge("Token rechazado", "danger");
      }
    });

    document.getElementById("btn-copy-token").addEventListener("click", async () => {
      const msgEl = document.getElementById("token-bridge-msg");
      if (!profileToken) {
        msgEl.textContent = "Primero inicia sesion para obtener el token del DEMO.";
        return;
      }
      try {
        await navigator.clipboard.writeText(profileToken);
        msgEl.textContent = "Token copiado. Abre la pagina WAF y pegalo en la prueba del mismo usuario con otro front door.";
      } catch (_) {
        msgEl.textContent = "No se pudo copiar automaticamente. Selecciona el token y copialo manualmente.";
      }
    });
  </script>
</body>
</html>"""

WAF_LANDING_PAGE = r"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Caso F | WAF Support</title>
  <style>
    :root {
      --bg: #07151d;
      --panel: rgba(8, 28, 36, 0.9);
      --panel-soft: rgba(255, 255, 255, 0.04);
      --line: rgba(72, 187, 120, 0.22);
      --text: #eefaf7;
      --muted: #9cc8bd;
      --accent: #56d364;
      --accent-2: #0ea5a0;
      --ok: #8cf3c0;
      --warn: #ffd479;
      --danger: #ff9f9f;
      --shadow: 0 28px 70px rgba(0, 0, 0, 0.35);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0; font-family: "Segoe UI", sans-serif;
      color: var(--text);
      background:
        radial-gradient(circle at top left, rgba(14, 165, 160, 0.18), transparent 28%),
        radial-gradient(circle at right, rgba(86, 211, 100, 0.14), transparent 26%),
        linear-gradient(180deg, #07151d 0%, #0c1f29 100%);
    }
    .shell { width: min(1180px, calc(100% - 28px)); margin: 0 auto; padding: 28px 0 56px; }
    .hero, .panel {
      border: 1px solid var(--line); border-radius: 24px;
      background: var(--panel); backdrop-filter: blur(16px); box-shadow: var(--shadow);
    }
    .hero { padding: 28px; margin-bottom: 18px; }
    .eyebrow { margin: 0 0 10px; color: var(--accent); text-transform: uppercase; letter-spacing: 0.18em; font-size: 0.78rem; }
    h1 { margin: 0; font-size: clamp(2.2rem, 6vw, 4rem); line-height: 0.98; }
    h2 { margin: 0 0 12px; font-size: 1.2rem; }
    .lead { color: var(--muted); max-width: 76ch; margin: 14px 0 0; line-height: 1.58; }
    .hero-grid, .story { display: grid; gap: 16px; }
    .hero-grid { grid-template-columns: 1.05fr 0.95fr; margin-top: 22px; }
    .story { grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); }
    .mini-panel, .story-card {
      border-radius: 20px; border: 1px solid rgba(255,255,255,0.08);
      background: var(--panel-soft); padding: 16px;
    }
    .story-card strong { display: block; margin-bottom: 6px; }
    .story-card p { margin: 0; color: var(--muted); line-height: 1.45; }
    .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; }
    .stat {
      padding: 14px; border-radius: 18px; border: 1px solid rgba(255,255,255,0.08);
      background: rgba(255,255,255,0.04);
    }
    .stat strong { display: block; font-size: 1.2rem; margin-bottom: 4px; color: var(--accent); }
    .stat span { color: var(--muted); font-size: 0.9rem; }
    .panel { padding: 22px; margin-bottom: 18px; }
    .hero-actions { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 16px; }
    button, .link-button {
      display: inline-flex; align-items: center; justify-content: center; min-height: 48px;
      cursor: pointer; font-weight: 800; padding: 13px 16px; border-radius: 14px;
      border: none; font: inherit; text-decoration: none; transition: transform 120ms ease, filter 120ms ease;
    }
    button:hover, .link-button:hover { transform: translateY(-1px); filter: brightness(1.08); }
    .btn-primary { background: linear-gradient(135deg, var(--accent), var(--accent-2)); color: #fff; }
    .btn-secondary { background: linear-gradient(135deg, #38bdf8, #0ea5a0); color: #fff; }
    .link-button { background: linear-gradient(135deg, #56d364, #0891b2); color: #fff; }
    .badge {
      display: inline-flex; align-items: center; gap: 8px; padding: 9px 12px;
      border-radius: 999px; border: 1px solid rgba(255,255,255,0.08);
      background: rgba(255,255,255,0.04); color: var(--muted); font-size: 0.9rem;
    }
    .badge.ok { color: var(--ok); border-color: rgba(140,243,192,0.2); }
    .badge.warn { color: var(--warn); }
    .badge.danger { color: var(--danger); }
    pre {
      margin: 0; padding: 16px; border-radius: 14px;
      background: rgba(2, 8, 20, 0.92); border: 1px solid rgba(255,255,255,0.06);
      color: #c7fff0; overflow: auto; min-height: 110px; font-size: 0.88rem;
    }
    .helper { color: var(--muted); font-size: 0.92rem; margin-top: 8px; line-height: 1.5; }
    textarea {
      width: 100%; min-height: 132px; resize: vertical; border-radius: 14px;
      border: 1px solid rgba(255,255,255,0.12); padding: 12px 14px;
      color: var(--text); background: rgba(255,255,255,0.05); font: inherit;
    }
    textarea:focus { outline: none; border-color: var(--accent); }
    .note {
      padding: 16px; border-radius: 18px; background: rgba(255, 212, 121, 0.08);
      border: 1px solid rgba(255, 212, 121, 0.22); color: var(--warn); margin-top: 14px;
    }
    @media (max-width: 900px) { .hero-grid { grid-template-columns: 1fr; } }
    @media (max-width: 640px) { .shell { width: min(100% - 18px, 1180px); } }
  </style>
</head>
<body>
  <main class="shell">
    <section class="hero">
      <p class="eyebrow">Caso F · WAF Support · Security Perimeter</p>
      <h1>Mismo usuario, mismo token, otro front door con WAF</h1>
      <p class="lead">
        Esta URL no reemplaza al DEMO principal. Usa la misma identidad del DEMO
        para mostrar la segunda mitad de la historia: no solo quien entra, sino
        que solicitudes se frenan antes de llegar a la aplicacion. Lo nuevo aqui
        no es el usuario: es la capa de entrada REST API + Cognito Authorizer + WAF.
      </p>
      <div class="hero-grid">
        <div class="mini-panel">
          <div class="stats">
            <div class="stat"><strong>Misma identidad</strong><span>Reutiliza el User Pool del DEMO</span></div>
            <div class="stat"><strong>Mismo token</strong><span>Pega aqui el idToken del DEMO</span></div>
            <div class="stat"><strong>Nuevo front door</strong><span>REST API + Cognito Authorizer + WAF</span></div>
            <div class="stat"><strong>Nuevo resultado</strong><span>403 antes de llegar a Lambda</span></div>
          </div>
        </div>
        <div class="mini-panel">
          <h2>Como se conecta con el DEMO</h2>
          <div class="story">
            <article class="story-card">
              <strong>Lo que ya probaste</strong>
              <p>En el DEMO demostraste identidad: usuario real, login real y acceso real a <code>/profile</code>.</p>
            </article>
            <article class="story-card">
              <strong>Lo que cambia aqui</strong>
              <p>La identidad sigue siendo la misma, pero el camino cambia: ahora pasas por REST API con Cognito Authorizer y por un Web ACL antes de tocar la app.</p>
            </article>
            <article class="story-card">
              <strong>Lo que vas a demostrar</strong>
              <p>Que el mismo token del DEMO sigue siendo valido en otra puerta de entrada y que, ademas, WAF puede bloquear trafico sospechoso antes de la logica.</p>
            </article>
          </div>
          <div class="hero-actions">
            __DEMO_LINK__
          </div>
        </div>
      </div>
    </section>

    <section class="panel">
      <h2>Secuencia guiada para novatos</h2>
      <p class="helper">
        1. En el DEMO crea usuario, inicia sesion y copia el <code>idToken</code>.
        2. Pegalo aqui y llama a <code>/profile</code> para comprobar que la identidad es la misma.
        3. Luego ejecuta la prueba SQLi controlada para ver que WAF agrega una segunda capa.
      </p>
      <label for="demo-token">Pega aqui el mismo ID Token obtenido en el DEMO</label>
      <textarea id="demo-token" placeholder="Pega aqui el mismo idToken que obtuviste en el DEMO principal"></textarea>
      <div class="hero-actions">
        <button class="btn-primary" id="btn-profile">Probar /profile con token del DEMO</button>
        <button class="btn-primary" id="btn-health">Consultar /health</button>
        <button class="btn-secondary" id="btn-probe">Probar bloqueo WAF</button>
      </div>
      <p class="helper" id="probe-msg"></p>
    </section>

    <section class="panel">
      <h2>Respuesta</h2>
      <div class="hero-actions" style="margin-top:0;margin-bottom:12px;">
        <span class="badge" id="statusBadge">Esperando accion</span>
        <span class="badge ok">Perimetro explicado</span>
        <span class="badge warn">Costo temporal documentado</span>
      </div>
      <pre id="output">Usa los botones para ver el health y la respuesta del WAF.</pre>
    </section>

    <section class="panel">
      <h2>Como leer esta pagina</h2>
      <div class="story">
        <article class="story-card">
          <strong>Lo que se mantiene igual</strong>
          <p>Usuario, token y endpoint logico de perfil. La pregunta sigue siendo "quien eres".</p>
        </article>
        <article class="story-card">
          <strong>Lo que cambia</strong>
          <p>La puerta de entrada: aqui agregas REST API + Cognito Authorizer + WAF para responder "que ni siquiera deberia entrar".</p>
        </article>
        <article class="story-card">
          <strong>Lo que demuestra al final</strong>
          <p>No es un segundo producto. Es la misma historia de seguridad, completada con una capa perimetral que el DEMO barato no puede mostrar solo.</p>
        </article>
      </div>
      <div class="note">
        El control de costo y la ventana de vida de este stack se documentan en
        <code>VISUALIZATION.md</code>. La regla es simple: desplegar, capturar, explicar y destruir.
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

    function showOutput(data) {
      outputEl.textContent = JSON.stringify(data, null, 2);
    }

    function buildUrl(path) {
      const pagePath = window.location.pathname || "/";
      const basePath = pagePath === "/" ? "/" : pagePath.replace(/\/?$/, "/");
      const cleanPath = String(path || "").replace(/^\/+/, "");
      return `${window.location.origin}${basePath}${cleanPath}`;
    }

    async function call(path, options) {
      const response = await fetch(buildUrl(path), options || {});
      const text = await response.text();
      let data = { raw: text };
      try { data = JSON.parse(text); } catch (_) {}
      return { status: response.status, data };
    }

    document.getElementById("btn-profile").addEventListener("click", async () => {
      const msgEl = document.getElementById("probe-msg");
      const token = document.getElementById("demo-token").value.trim();
      if (!token) {
        msgEl.textContent = "Primero pega el mismo idToken obtenido en el DEMO.";
        return;
      }
      msgEl.textContent = "Probando /profile con el mismo token del DEMO...";
      setBadge("Probando misma identidad...", "warn");
      const { status, data } = await call("/profile", {
        headers: { Authorization: `Bearer ${token}` },
      });
      showOutput({ step: "shared-profile", status, data });
      if (status === 200) {
        msgEl.textContent = "Exito: el mismo token del DEMO funciono aqui. Ahora ya se entiende la relacion entre identidad y perimetro.";
        setBadge("Misma identidad validada", "ok");
      } else {
        msgEl.textContent = "El token no fue aceptado. Verifica que pegaste el idToken del DEMO principal y no un valor recortado.";
        setBadge("Token DEMO no valido", "danger");
      }
    });

    document.getElementById("btn-health").addEventListener("click", async () => {
      const msgEl = document.getElementById("probe-msg");
      msgEl.textContent = "Consultando /health...";
      setBadge("Consultando health...", "warn");
      const { status, data } = await call("/health");
      showOutput({ step: "health", status, data });
      if (status === 200) {
        msgEl.textContent = "Health OK. El despliegue auxiliar esta listo para la prueba controlada.";
        setBadge("Health OK", "ok");
      } else {
        msgEl.textContent = "No se pudo consultar /health.";
        setBadge("Health error", "danger");
      }
    });

    document.getElementById("btn-probe").addEventListener("click", async () => {
      const msgEl = document.getElementById("probe-msg");
      msgEl.textContent = "Ejecutando prueba SQLi controlada...";
      setBadge("Probando WAF...", "warn");
      const { status, data } = await call("/health?filter=%27%20or%201%3D1%20--");
      showOutput({ step: "waf-probe", status, data });
      if (status === 403) {
        msgEl.textContent = "WAF bloqueo la solicitud antes de la logica de negocio. Esa es la evidencia buscada.";
        setBadge("WAF bloqueo OK", "ok");
      } else {
        msgEl.textContent = "La respuesta no fue 403. Revisa la asociacion del WebACL o espera la propagacion.";
        setBadge("Revisar WAF", "danger");
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


def _landing_page():
    if DEPLOYMENT_MODE.startswith("visualization"):
        demo_link = (
            f'<a class="link-button" href="{DEMO_PAGE_URL}">Abrir DEMO principal</a>'
            if DEMO_PAGE_URL
            else '<span class="helper">Configura DEMO_PAGE_URL para enlazar este despliegue con el DEMO principal.</span>'
        )
        return WAF_LANDING_PAGE.replace("__DEMO_LINK__", demo_link)

    support_link = (
        f'<a class="link-button" href="{SUPPORT_PAGE_URL}">Abrir capa WAF: misma identidad, otro front door</a>'
        if SUPPORT_PAGE_URL
        else '<span class="helper">Activa SUPPORT_PAGE_URL para completar el recorrido: misma identidad en el DEMO, nueva capa perimetral en la pagina WAF.</span>'
    )
    return DEMO_LANDING_PAGE.replace("__SUPPORT_LINK__", support_link)


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


def _http_method(event):
    request_ctx = event.get("requestContext") or {}
    http_ctx = request_ctx.get("http") or {}
    return str(http_ctx.get("method") or event.get("httpMethod") or "").upper()


def _request_path(event):
    return event.get("rawPath") or event.get("path") or "/"


def _authorizer_claims(event):
    authorizer = (event.get("requestContext") or {}).get("authorizer") or {}
    jwt_claims = (authorizer.get("jwt") or {}).get("claims") or {}
    rest_claims = authorizer.get("claims") or {}
    return jwt_claims or rest_claims


def _available_routes():
    if DEPLOYMENT_MODE.startswith("visualization"):
        return ["GET /", "GET /health", "GET /profile"]
    return ["GET /", "GET /health", "POST /auth/register", "POST /auth/login", "GET /profile"]


def _as_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() == "true"
    return bool(value)


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
    # HTTP API JWT Authorizer -> requestContext.authorizer.jwt.claims
    # REST API Cognito Authorizer -> requestContext.authorizer.claims
    claims = _authorizer_claims(event)

    if not claims:
        return _json_response(401, {"ok": False, "error": "Token de autorizacion requerido."})

    return _json_response(200, {
        "ok": True,
        "email": claims.get("email", ""),
        "name": claims.get("name", claims.get("email", "")),
        "sub": claims.get("sub", ""),
        "emailVerified": _as_bool(claims.get("email_verified", False)),
        "timestamp": _utc_now(),
    })


def handle_health(_event):
    return _json_response(200, {
        "status": "ok",
        "service": "caso-f-security",
        "cognito": "configured" if COGNITO_USER_POOL_ID else "not-configured",
        "deploymentMode": DEPLOYMENT_MODE,
        "perimeterMode": PERIMETER_MODE,
        "productRole": "waf-support" if DEPLOYMENT_MODE.startswith("visualization") else "demo-primary",
        "linkedPage": DEMO_PAGE_URL if DEPLOYMENT_MODE.startswith("visualization") else SUPPORT_PAGE_URL,
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
    method = _http_method(event)
    path = _request_path(event)

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
            return _html_response(_landing_page())

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
            "availableRoutes": _available_routes(),
        })

    except ValueError as exc:
        return _json_response(400, {"ok": False, "error": str(exc)})
    except ClientError as exc:
        return _cognito_error_response(exc)
    except Exception as exc:
        return _json_response(500, {"ok": False, "error": "Error interno.", "detail": str(exc)})
