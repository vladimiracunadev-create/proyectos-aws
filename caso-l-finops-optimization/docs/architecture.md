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
sequenceDiagram
    participant GitLab as 🦊 GitLab CI Runner
    participant OIDC as 🔐 GitLab OIDC Provider
    participant STS as ☁️ AWS STS
    participant IAM as 🔑 AWS IAM
    participant S3 as 🪣 AWS S3

    Note over GitLab: Pipeline inicia (push a main)
    GitLab->>OIDC: Solicita JWT Token\n(GITLAB_OIDC_TOKEN)
    OIDC-->>GitLab: JWT firmado\n{sub: project_path/..., aud: gitlab.com}

    GitLab->>STS: AssumeRoleWithWebIdentity\n--role-arn arn:aws:iam::ACCOUNT:role/GitLabDeployRole\n--web-identity-token JWT

    STS->>IAM: Verificar Trust Policy\n¿gitlab.com:sub coincide con el path del proyecto?
    IAM-->>STS: Autorizado ✅

    STS-->>GitLab: Credenciales temporales\n(AccessKeyId + SecretKey + SessionToken)\nDuración: 3600s (1 hora)

    GitLab->>S3: aws s3 sync ...\n(usando credenciales temporales)
    S3-->>GitLab: 200 OK

    Note over GitLab,S3: Las credenciales expiran solas.\nNo hay ACCESS KEY permanente en ningún lado.
```

---

## 📐 Diagrama 2: Arquitectura Completa FinOps & Governance

```mermaid
graph TB
    subgraph CI["🦊 GitLab CI Pipeline"]
        OIDC_Token["GITLAB_OIDC_TOKEN\n(JWT efímero, 1h)"]
        Deploy_Job["Job: deploy_case_l_final\nimage: aws-cli\nscript: aws s3 sync"]
    end

    subgraph AWS_Auth["🔐 AWS IAM (Zero-Trust)"]
        IdP["Identity Provider\n(OIDC: gitlab.com)\n+ Thumbprint SSL"]
        Role["IAM Role: GitLabDeployRole\nTrust: gitlab.com:sub = project_path\nPermissions: S3FullAccess\nDuration: 1h max"]
        STS["AWS STS\nAssumeRoleWithWebIdentity"]
    end

    subgraph AWS_FinOps["💰 AWS Billing & Budgets"]
        Budget["Budget: Vladimir-Monthly-Alert\nMonto: $5.00 USD\nAlertas: 85% real + 100% proyectado"]
        SNS["SNS Notification\n→ Email personal"]
        CostExplorer["Cost Explorer\n(datos reales de gasto)"]
    end

    subgraph AWS_IAM_Gov["🛡️ IAM Governance"]
        RegionPolicy["Policy: DenyNonUSRegions\nBloquea regiones fuera de us-east-1/2\n(excepto IAM, CloudFront, Route53)"]
        TagPolicy["Policy: EnforceTaggingPolicy\nExige tags Project + FinOps\nal crear recursos EC2/S3"]
    end

    subgraph S3_Hosting["🌐 S3 + Dashboard FinOps"]
        Bucket["S3 Bucket (Website Hosting)\nfinops-vladimir-portfolio-case-l"]
        Dashboard["Dashboard HTML/JS\n(lee costs.json desde S3)\nGráficos: Chart.js\nSemáforo de riesgo financiero"]
        CostsJSON["costs.json\n(generado por Python boto3\ndesde Cost Explorer + Budgets API)"]
    end

    OIDC_Token --> STS
    STS --> IdP
    STS --> Role
    Role -->|"Temp credentials"| Deploy_Job
    Deploy_Job -->|"aws s3 sync"| Bucket
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
graph LR
    subgraph AWS_Billing["💳 AWS Billing"]
        Usage["Consumo real\nde servicios AWS\n(acumulado mensual)"]
    end

    subgraph Budgets["💰 AWS Budgets (automático)"]
        Check["Evaluación cada 24h:\n¿Gasto actual / proyectado\nsupera umbrales?"]
        T85["Umbral 85%\nActual ≥ $4.25"]
        T100["Umbral 100%\nProyectado ≥ $5.00"]
    end

    subgraph Alert["🚨 Notificación"]
        SNS2["SNS Topic"]
        Email["📧 Email inmediato\n'Tu gasto alcanzó $4.25'"]
    end

    subgraph Action["✋ Acción Manual"]
        Review["Revisar Cost Explorer\n¿Qué servicio generó el costo?"]
        Stop["Detener recursos:\nterraform destroy\naws ecs update-service --desired 0"]
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
graph TB
    subgraph Request["📝 Request IAM"]
        Action["aws ec2 run-instances\n--region eu-west-1 (Irlanda)"]
    end

    subgraph Policy["🛡️ SCP / IAM Policy: DenyNonUSRegions"]
        Eval["Evalúa condición:\naws:RequestedRegion == eu-west-1\n¿Está en whitelist [us-east-1, us-east-2]?"]
        Deny["DENY ❌\n(Explicit Deny siempre gana)"]
        Allow["ALLOW ✅"]
    end

    subgraph Excepciones["🌐 Excepciones (Globales)"]
        GlobalSvcs["IAM, CloudFront, Route 53\nSupport, Budgets\n(servicios globales, no tienen región)"]
    end

    Action --> Eval
    Eval -->|"Región no en whitelist"| Deny
    Eval -->|"Región en whitelist"| Allow
    GlobalSvcs -.->|"NotAction: exentos"| Allow

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
