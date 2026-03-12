# 🏗️ Arquitectura: Caso A — AWS Amplify (CI/CD Nativo)

> **Stack**: AWS Amplify + GitLab Auto-Mirroring
> **Nivel**: 0 — Fundamentos de Deploy Continuo

---

## 🎯 Visión General

El Caso A demuestra la forma más accesible de llevar una aplicación web a producción en AWS:
**cero configuración de servidores, cero gestión de certificados SSL, cero CDN manual**.
Amplify lo resuelve todo de forma nativa.

El patrón de **GitLab → espejo en GitHub/CodeCommit → Amplify** es común en organizaciones
que ya tienen pipelines en GitLab pero quieren aprovechar la integración nativa de Amplify.

---

## 📐 Diagrama 1: Flujo de Deploy Completo

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#6C4DE6', 'secondaryColor': '#FF9900', 'tertiaryColor': '#f4f4f4', 'fontsize': '16px' }}}%%
graph TB
    subgraph Dev["💻 Desarrollador"]
        Push["git push\nmain / dev"]
    end

    subgraph GitLab["🦊 GitLab CI/CD"]
        Mirror["Auto-Mirror\na GitHub/CodeCommit"]
    end

    subgraph Amplify["☁️ AWS Amplify"]
        direction TB
        Trigger["🔔 Webhook Trigger\n(detección de push)"]
        Build["🏗️ Build Stage\namplify.yml\nnpm install + npm run build"]
        Deploy["🚀 Deploy Stage\nS3 + CloudFront\n(gestionado por Amplify)"]
        CDN["🌐 CloudFront CDN\nSSL automático\nHTTPS + Headers de seguridad"]
    end

    subgraph Extras["🔧 Amplify Extras"]
        direction TB
        Preview["✨ Branch Preview\n(por rama: feature/*)"]
        BasicAuth["🔐 Basic Auth\n(ramas no-prod)"]
        Notify["📧 Notificaciones\nEmail / SNS"]
    end

    Push --> Mirror
    Mirror --> Trigger
    Trigger --> Build
    Build --> Deploy
    Deploy --> CDN
    Deploy -.-> Preview
    Deploy -.-> BasicAuth
    Deploy -.-> Notify

    style Push fill:#6C4DE6,color:#fff
    style Amplify fill:#FF9900,color:#fff,stroke:#e68a00,stroke-width:2px
    style CDN fill:#2496ED,color:#fff
    style Extras fill:#f5f5f5,stroke:#333
```

---

## 📐 Diagrama 2: Flujo de Request del Usuario Final

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'fontsize': '16px' }}}%%
sequenceDiagram
    participant U as 🌍 Usuario
    participant CF as ☁️ CloudFront (CDN)
    participant S3 as 🪣 S3 (Origen)
    participant Cache as 💾 Cache Edge

    U->>CF: GET https://app.amplifyapp.com/
    CF->>Cache: ¿Está en caché?

    alt Cache HIT (común)
        Cache-->>CF: HTML/CSS/JS cached
        CF-->>U: 200 OK (desde edge, ~ms)
    else Cache MISS (primer acceso o TTL expirado)
        CF->>S3: GET /index.html
        S3-->>CF: 200 OK + archivo
        CF->>Cache: Guardar en cache edge
        CF-->>U: 200 OK (desde S3, ~100ms)
    end

    Note over U,CF: SSL/TLS gestionado automáticamente por Amplify
    Note over CF,S3: Acceso privado S3 → CloudFront (OAI automático)
```

---

## 📐 Diagrama 3: Estrategia Multi-Rama (Branch Deploys)

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#27AE60', 'fontsize': '16px' }}}%%
graph TB
    subgraph Ramas["🎋 Ramas del Repositorio"]
        direction TB
        Main["main\n(producción)"]
        Dev["dev\n(staging)"]
        Feature["feature/nueva-ui\n(preview)"]
    end

    subgraph Amplify["☁️ AWS Amplify Apps"]
        direction TB
        Prod["🟢 Producción\nhttps://main.d1xxx.amplifyapp.com\ncdn: activo, auth: desactivado"]
        Staging["🟡 Staging\nhttps://dev.d1xxx.amplifyapp.com\nbasic auth: usuario/pass"]
        Preview["🔵 Preview\nhttps://feature-nueva-ui.d1xxx.amplifyapp.com\n(auto-eliminado al hacer merge)"]
    end

    Main --> Prod
    Dev --> Staging
    Feature --> Preview

    style Prod fill:#27AE60,color:#fff,stroke:#1e8449,stroke-width:2px
    style Staging fill:#F39C12,color:#fff,stroke:#d68910,stroke-width:2px
    style Preview fill:#2980B9,color:#fff,stroke:#21618c,stroke-width:2px
```

---

## 🔧 Componentes y Roles

| Componente | Servicio | Función | Costo |
|---|---|---|---|
| **Build Engine** | AWS Amplify | Ejecuta `amplify.yml`, instala dependencias, genera build | Free Tier: 1000 min/mes |
| **Storage** | S3 (oculto) | Almacena el artefacto de build (HTML/CSS/JS) | Free Tier: 5GB |
| **CDN** | CloudFront (oculto) | Distribuye el contenido globalmente con caché edge | Free Tier: 1TB transfer/mes |
| **SSL** | ACM (automático) | Certificado HTTPS sin configuración manual | Gratis |
| **DNS** | Route 53 (opcional) | Dominio propio (ej: `app.tudominio.com`) | $0.50/zona/mes |
| **Mirroring** | GitLab CI | Sincroniza GitLab → repositorio compatible con Amplify | Gratis |

---

## 💡 Por Qué Este Patrón

| Ventaja | Detalle |
|---|---|
| **Zero Config** | No gestionas servidores, balanceadores ni certificados |
| **Deploy automático** | Push a `main` → en producción en ~2 minutos |
| **Branch previews** | Cada rama tiene su propia URL pública para QA |
| **Escalamiento automático** | CloudFront escala a millones de requests sin intervención |
| **Rollback instantáneo** | Amplify guarda historial de deploys, rollback en 1 click |

---

## 🔗 Referencias

- [README del Caso A](../README.md)
- [Guía Paso a Paso AWS](../AWS_PASO_A_PASO.md)
- [Documentación oficial Amplify](https://docs.aws.amazon.com/amplify/latest/userguide/)
