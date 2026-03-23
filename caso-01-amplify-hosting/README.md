# Caso 01 — AWS Amplify: Continuous Deployment por Rama

## Resumen

| Campo | Valor |
|:---|:---|
| **Caso** | 01 |
| **Servicio AWS** | AWS Amplify Console |
| **Patrón** | Continuous Deployment multi-branch |
| **GitHub Actions** | Delegado a Amplify (trigger nativo por push) |
| **Estado** | ✅ Completado — En producción |
| **Demo main** | https://main.d3r1wuymolxagh.amplifyapp.com/ |
| **Demo dev** | https://dev.d20m8tc0banvg.amplifyapp.com/ |

---

## ¿Qué demuestra este caso?

**Problema resuelto:** Necesito publicar un sitio estático con despliegue automático por rama sin gestionar servidores, certificados SSL ni pipelines complejos.

**Solución:** AWS Amplify Console detecta cambios en las ramas `main` y `dev` del repositorio y despliega automáticamente en URLs únicas por entorno.

**Flujo:**

```
Push local → GitHub (rama dev o main)
    └── Amplify Console detecta el push
        ├── Rama main → https://main.d3r1wuymolxagh.amplifyapp.com
        └── Rama dev  → https://dev.d20m8tc0banvg.amplifyapp.com
```

---

## 🏗️ Diagrama de arquitectura

```mermaid
flowchart LR
    DEV[Dev Local\ngit push] --> GH[(GitHub\nmain - dev)]

    GH -->|webhook automatico| AMP[AWS Amplify Console\nCI/CD integrado]

    AMP -->|rama main| PROD[Produccion\nmain.amplifyapp.com]
    AMP -->|rama dev|  PREV[Preview\ndev.amplifyapp.com]

    AMP -.->|incluido| CDN[CloudFront\nCDN global]
    AMP -.->|incluido| SSL[ACM Certificate\nHTTPS automatico]
    AMP -.->|incluido| STOR[S3 Assets\nalmacenamiento]

    PROD --> USER[Usuario Final]
    PREV --> USER
```

---

## Stack Técnico

| Capa | Tecnología |
|:---|:---|
| **Hosting** | AWS Amplify Console (CDN global, SSL automático) |
| **CI/CD** | Amplify nativo (sin GitHub Actions en este caso) |
| **Frontend** | HTML5, CSS3, Vanilla JS (sin framework, sin build) |
| **PWA** | Service Worker + Web App Manifest |
| **i18n** | 6 idiomas: ES, EN, FR, IT, PT, ZH (data-attributes) |
| **API** | Static JSON (`/api/v1/`) — sin servidor |
| **3D** | Three.js vía Import Maps (sin compilación) |
| **PDF** | 30+ documentos × 6 idiomas (generados con Python reportlab) |

---

## Configuración clave (`amplify.yml`)

```yaml
version: 1
applications:
  - appRoot: caso-01-amplify-hosting
    frontend:
      phases:
        build:
          commands: []        # Sin build process — vanilla JS puro
      artifacts:
        baseDirectory: .
        files:
          - '**/*'
```

> **Por qué no hay build commands:** El sitio usa HTML/CSS/JS plano con Import Maps para Three.js.
> Amplify sirve los archivos tal cual, sin transpilación ni bundling.

---

## 📋 Pasos para reproducirlo desde cero

> Guía detallada con comandos exactos, errores comunes y verificaciones: **[AWS_PASO_A_PASO.md](./AWS_PASO_A_PASO.md)**

1. **Crear app en Amplify Console** → `All apps → New app → Host web app`
2. **Conectar repositorio GitHub** → seleccionar `proyectos-aws` → autorizar acceso
3. **Configurar branch mappings** → `main` (producción) + `dev` (preview) → Amplify genera URLs únicas por rama automáticamente
4. **Añadir `amplify.yml`** al raíz del repo con `appRoot: caso-01-amplify-hosting` (sin build commands si el sitio es vanilla JS)
5. **`git push`** → Amplify detecta el cambio, ejecuta el build y despliega en ~2 minutos
6. **Verificar** → abrir la URL de Amplify en el navegador; SSL y CDN ya están activos

> **Tiempo estimado:** 15 minutos la primera vez, < 2 min en deploys posteriores.

---

## Qué aprendí / Qué valida

1. **Multi-branch deploy nativo:** Amplify mapea ramas a URLs automáticamente. No necesitas configurar redirecciones ni entornos manualmente.
2. **SSL incluido:** Cada URL de Amplify tiene certificado ACM sin intervención.
3. **Limitación del modelo:** Sin GitHub Actions en el loop, no tengo control sobre el pipeline (no puedo añadir tests, linters o aprobaciones pre-deploy desde GitHub).
4. **Evolución natural:** Este caso es el punto de partida. El Caso 03 introduce OIDC + CloudFront para tener ese control.

---

## Diferencia con el Caso 02

| | Caso 01 (Amplify) | Caso 02 (S3 + Actions) |
|:---|:---|:---|
| **Pipeline** | Gestionado por Amplify | Controlado por GitHub Actions |
| **SSL** | Automático | Manual (requiere CloudFront) |
| **Control** | Limitado | Total (custom steps) |
| **OIDC** | No aplica | Pendiente (ver roadmap) |
| **CloudFront** | Incluido | Caso 03 |

---

## Archivos principales

```
caso-01-amplify-hosting/
├── index.html              # SPA principal con i18n inline
├── app.js                  # Lógica: vistas, idiomas, PDFs, theme
├── styles.css              # Design system completo
├── pwa.js                  # Install prompt + SW registration
├── service-worker.js       # Cache strategy (network-first)
├── manifest.webmanifest    # PWA metadata
├── robots.txt / sitemap.xml
├── llm.txt                 # Machine-readable metadata (llmstxt.org)
├── api/v1/                 # Static JSON API
│   ├── meta.json
│   ├── profile.json
│   ├── experience.json
│   ├── projects.json
│   ├── skills.json
│   └── artifacts.json
├── assets/                 # PDFs × 6 idiomas + icons
└── experiencia-3d/         # Three.js WebGL gallery (desactivada en prod)
    ├── index.html
    ├── css/
    └── js/
```
