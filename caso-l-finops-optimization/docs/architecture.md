# 🏗️ Arquitectura: Caso L — FinOps & Governance (Excelencia Operativa)

> **Stack**: AWS Budgets + GitLab OIDC + IAM Governance + S3 Hosting
> **Nivel**: 11 — Gobernanza Financiera y Zero-Trust

---

## 🎯 Visión General

El Caso L no construye una nueva aplicación: **asegura y gobierna todo lo que ya existe**.
Es la capa de madurez que toda organización necesita antes de escalar:

1. **¿Cuánto gastas?** → AWS Budgets con alertas proactivas.
2. **¿Quién tiene acceso?** → IAM Governance con privilegio mínimo y restricciones de región.
3. **¿Cómo se autentica el pipeline?** → OIDC (Zero-Trust, sin keys permanentes).

---

## 📐 Diagrama 1: Autenticación OIDC — GitLab CI → AWS (Zero-Trust)

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'fontsize': '16px' }}}%%
sequenceDiagram
    participant GitLab as 🦊 GitLab CI Runner
    participant OIDC as 🔐 GitLab OIDC Provider
    participant STS as ☁️ AWS STS
    participant IAM as 🔑 AWS IAM
    participant S3 as 🪣 AWS S3

    Note over GitLab: Pipeline inicia (push a main)
    GitLab->>OIDC: Solicita JWT Token\n(GITLAB_OIDC_TOKEN)
    OIDC-->>GitLab: JWT firmado\n{sub: project_path, aud: gitlab.com}

    GitLab->>STS: AssumeRoleWithWebIdentity\n(JWT)

    STS->>IAM: Verificar Trust Policy\n¿Coincide project path?
    IAM-->>STS: Autorizado ✅

    STS-->>GitLab: Credenciales temporales\n(1 hora de duración)

    GitLab->>S3: aws s3 sync ...
    S3-->>GitLab: 200 OK

    Note over GitLab,S3: Las credenciales expiran solas.\nSin ACCESS KEY permanente.
```

---

## 📐 Diagrama 2: Arquitectura Completa FinOps & Governance

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#E74C3C', 'secondaryColor': '#2496ED', 'tertiaryColor': '#f4f4f4', 'fontsize': '16px' }}}%%
graph TB
    subgraph CI["🦊 GitLab CI Pipeline"]
        direction TB
        OIDC_Token["🔐 GITLAB_OIDC_TOKEN\n(JWT efímero)"]
        Deploy_Job["🚀 Job: deploy_case_l\naws s3 sync"]
    end

    subgraph AWS_Auth["🔑 AWS IAM (Zero-Trust)"]
        direction TB
        IdP["🆔 Identity Provider\n(OIDC: gitlab.com)"]
        Role["👤 IAM Role: DeployRole\nTrust: GitLab OIDC"]
        STS["☁️ AWS STS\nAssumeRole"]
    end

    subgraph AWS_FinOps["💰 AWS Billing & Budgets"]
        direction TB
        Budget["💰 Monthly Budget\nAlertas: 85% / 100%"]
        SNS["🔔 SNS Notification\n→ Email alert"]
        CostExplorer["📊 Cost Explorer API"]
    end

    subgraph AWS_IAM_Gov["🛡️ IAM Governance"]
        direction TB
        RegionPolicy["🚫 DenyNonUSRegions\nWhitelist: us-east-1/2"]
        TagPolicy["🏷️ EnforceTagging\nExige Project + FinOps tags"]
    end

    subgraph S3_Hosting["🌐 Dashboard FinOps"]
        direction TB
        Bucket["🪣 S3 Static Website"]
        Dashboard["📊 Dashboard HTML/JS\nChart.js + Boto3 Data"]
        CostsJSON["📄 costs.json"]
    end

    OIDC_Token --> STS
    STS --> IdP
    STS --> Role
    Role -->|"Temp keys"| Deploy_Job
    Deploy_Job --> Bucket
    CostExplorer --> CostsJSON
    CostsJSON --> Bucket
    Budget --> SNS
    Dashboard --> CostsJSON
    RegionPolicy -.- Role
    TagPolicy -.- Role

    style Role fill:#E74C3C,color:#fff
    style Budget fill:#F39C12,color:#fff
    style Dashboard fill:#2496ED,color:#fff
    style OIDC_Token fill:#8E44AD,color:#fff
```

---

## 📐 Diagrama 3: Flujo de Alertas de Presupuesto

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#F39C12', 'fontsize': '16px' }}}%%
graph TB
    subgraph AWS_Billing["💳 AWS Billing"]
        direction TB
        Usage["📈 Consumo real\nde servicios AWS"]
    end

    subgraph Budgets["💰 AWS Budgets"]
        direction TB
        Check["🔍 Evaluación 24h\nActual vs Umbrales"]
        T85["🟡 Umbral 85%\nActual ≥ $4.25"]
        T100["🔴 Umbral 100%\nProyectado ≥ $5.00"]
    end

    subgraph Alert["🚨 Notificación"]
        direction TB
        SNS2["🔔 SNS Topic"]
        Email["📧 Email inmediato\nAlerta de umbral"]
    end

    subgraph Action["✋ Acción Manual"]
        direction TB
        Review["🔍 Revisar Cost Explorer"]
        Stop["🛑 Detener recursos\n(Scale to zero / Destroy)"]
    end

    Usage --> Check
    Check --> T85 --> SNS2
    Check --> T100 --> SNS2
    SNS2 --> Email
    Email --> Review
    Review --> Stop

    style T85 fill:#F39C12,color:#fff
    style T100 fill:#E74C3C,color:#fff
    style Email fill:#27AE60,color:#fff
```

---

## 📐 Diagrama 4: IAM Governance (Restricción de Región)

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#E74C3C', 'fontsize': '16px' }}}%%
graph TB
    subgraph Request["📝 Request IAM"]
        Action["🏃 ec2 run-instances\neu-west-1 (Irlanda)"]
    end

    subgraph Policy["🛡️ Policy: DenyNonUSRegions"]
        direction TB
        Eval["🔍 Evalúa condición:\nRequestedRegion\nin [us-east-1, us-east-2]?"]
        Deny["🔴 DENY ❌\nExplicit Deny"]
        Allow["🟢 ALLOW ✅"]
    end

    subgraph Excepciones["🌐 Global Services"]
        GlobalSvcs["IAM, CloudFront,\nRoute 53, Budgets"]
    end

    Action --> Eval
    Eval -->|"Not in whitelist"| Deny
    Eval -->|"In whitelist"| Allow
    GlobalSvcs -.->|"Exempt"| Allow

    style Deny fill:#E74C3C,color:#fff
    style Allow fill:#27AE60,color:#fff
    style GlobalSvcs fill:#8E44AD,color:#fff
```

---

## 🔧 Componentes y Roles

| Componente | Servicio | Función |
|---|---|---|
| **OIDC IdP** | IAM Identity Provider | Permite a GitLab asumir roles sin keys permanentes |
| **Rol de Deploy** | IAM Role | Credenciales temporales (1h) para el pipeline |
| **Presupuesto** | AWS Budgets | Alerta antes de que el gasto se dispare |
| **Dashboard** | S3 + HTML/JS | Visualiza costos reales en tiempo casi-real |
| **Datos** | Cost Explorer + Budgets API | Fuente de verdad de costos (via boto3) |
| **Governance** | IAM Policies | Bloquea regiones no autorizadas y exige tags |

---

## 💡 Por Qué OIDC es Superior a IAM Keys Permanentes

| Característica | IAM Keys (Caso B) | OIDC (Caso L) |
|---|---|---|
| **Duración** | Permanentes (hasta rotar) | 1 hora (expire automático) |
| **Almacenamiento** | Variable GitLab (riesgo) | No se almacena nada |
| **Auditoría** | Difícil de rastrear | CloudTrail muestra `role-session-name: GitLabRunner-{pipelineId}` |
| **Rotación** | Manual (olvidable) | No aplica (son efímeras) |
| **Blast radius** | Keys filtradas = cuenta comprometida | Token expirado = inútil |

---

## 🔗 Referencias

- [README del Caso L](../README.md)
- [Guía Paso a Paso AWS](../AWS_PASO_A_PASO.md)
- [Ver Demo en Vivo](http://finops-vladimir-portfolio-case-l.s3-website.us-east-2.amazonaws.com)
