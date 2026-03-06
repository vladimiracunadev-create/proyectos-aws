# 🏗️ Arquitectura: Caso C — Terraform + CloudFront + S3 (IaC Profesional)

> **Stack**: Terraform + S3 (OAC) + CloudFront + Remote State
> **Nivel**: 2 — Infraestructura como Código (IaC)

---

## 🎯 Visión General

El Caso C eleva el Caso B al estándar profesional en tres dimensiones:

1. **Seguridad**: S3 privado con **Origin Access Control (OAC)** — nadie accede al bucket
   directamente, solo CloudFront.
2. **Performance**: CDN global con caché en edge locations — latencia < 50ms para usuarios
   en cualquier continente.
3. **Reproducibilidad**: Toda la infraestructura declarada en Terraform — se puede destruir
   y recrear en minutos, sin clicks manuales.

---

## 📐 Diagrama 1: Arquitectura Completa (Terraform Managed)

```mermaid
graph TB
    subgraph Internet
        User["🌍 Usuario\n(cualquier región)"]
    end

    subgraph CloudFront_Layer["☁️ AWS CloudFront (CDN Global)"]
        CF["📡 CloudFront Distribution\nHTTPS + TLS 1.2+\nCache TTL: 1 año (assets)\nOrigen: S3 via OAC\nHTTP → HTTPS redirect"]
        EdgeCache["💾 Edge Cache\n400+ ubicaciones globales"]
    end

    subgraph S3_Layer["🪣 AWS S3 (Privado)"]
        Bucket["S3 Bucket\nAcceso público: BLOQUEADO ✅\nSolo CloudFront puede leer\n(via OAC — Origin Access Control)"]
        OAC["🔐 Origin Access Control\nRemplaza OAI (legado)\nFirma requests con SigV4"]
    end

    subgraph IaC["🔧 Terraform (IaC)"]
        TF_State["📦 Remote State\nS3 + DynamoDB Lock\nus-east-2"]
        TF_Plan["terraform plan\n→ tfplan"]
        TF_Apply["terraform apply\n(GitLab CI)"]
    end

    User -->|"HTTPS"| CF
    CF --> EdgeCache
    EdgeCache -->|"Miss: fetch origin"| OAC
    OAC --> Bucket
    TF_Apply --> CF
    TF_Apply --> Bucket
    TF_Apply --> OAC
    TF_State -.->|"Bloquea\napply concurrentes"| TF_Apply

    style CF fill:#FF9900,color:#fff
    style Bucket fill:#569A31,color:#fff
    style OAC fill:#E74C3C,color:#fff
    style TF_Apply fill:#844FBA,color:#fff
```

---

## 📐 Diagrama 2: Flujo de Request con CloudFront Cache

```mermaid
sequenceDiagram
    participant U as 🌍 Usuario (Madrid)
    participant EdgeMAD as 📡 Edge Madrid
    participant EdgeUS as 📡 Edge US-East
    participant S3 as 🪣 S3 (Ohio)

    U->>EdgeMAD: GET https://d3xxx.cloudfront.net/index.html
    EdgeMAD->>EdgeMAD: ¿Cache HIT?

    alt CACHE HIT (petición repetida)
        EdgeMAD-->>U: 200 OK (TTL restante: 23h) ⚡ ~5ms
    else CACHE MISS (primera vez o TTL expirado)
        EdgeMAD->>EdgeUS: Fetch desde región origen

        alt Regional Cache HIT
            EdgeUS-->>EdgeMAD: 200 OK (desde regional cache)
        else Fetch from origin
            EdgeUS->>S3: GET /index.html (firmado con OAC/SigV4)
            S3-->>EdgeUS: 200 OK + HTML
            EdgeUS-->>EdgeMAD: 200 OK + HTML (guardado en cache regional)
        end

        EdgeMAD->>EdgeMAD: Guarda en cache local (TTL: 1 año para assets)
        EdgeMAD-->>U: 200 OK ~80ms
    end
```

---

## 📐 Diagrama 3: Flujo de Terraform en GitLab CI

```mermaid
graph LR
    subgraph Dev["💻 Dev"]
        PR["Merge Request\ncon cambios en\ncaso-c-terraform-s3/"]
    end

    subgraph CI["🦊 GitLab CI Pipeline"]
        Plan["🟡 plan_case_c\n(stage: plan-infrastructure)\nterraform init\nterraform plan -out=tfplan\nArtefacto: tfplan (1h)"]
        Apply["🔴 deploy_case_c\n(stage: deploy)\nterraform apply tfplan\n(necesita OKs del plan)"]
        Security["🔐 scan_infrastructure\n(stage: security)\ntfsec caso-c-terraform-s3\nComprueba misconfigs"]
    end

    subgraph AWS["☁️ AWS"]
        RemoteState["S3 Remote State\nDynamoDB Lock"]
        Resources["CloudFront + S3 + OAC\n+ Bucket Policy"]
    end

    PR --> Security
    PR --> Plan
    Plan -->|"needs: plan_case_c"| Apply
    Plan <-->|"terraform init\nlee/escribe state"| RemoteState
    Apply -->|"terraform apply"| Resources

    style Plan fill:#F39C12,color:#fff
    style Apply fill:#E74C3C,color:#fff
    style Security fill:#8E44AD,color:#fff
```

---

## 🔧 Componentes y Roles

| Componente | Servicio | Función | Por Qué es Mejor que Caso B |
|---|---|---|---|
| **CDN** | CloudFront | Cache global, HTTPS, redirect HTTP→HTTPS | Caso B no tiene CDN |
| **OAC** | CloudFront Origin Access Control | S3 privado, solo CloudFront accede | Caso B: bucket público |
| **IaC** | Terraform | Infraestructura reproducible y versionada | Caso B: config manual |
| **Remote State** | S3 + DynamoDB | Estado compartido + lock contra race conditions | Caso B: sin estado |
| **Security Scan** | tfsec | Detecta misconfigurations en el código Terraform | Caso B: sin análisis |

---

## 🔐 Seguridad: OAC vs Acceso Público (Comparativa)

```mermaid
graph LR
    subgraph Sin_OAC["❌ Sin OAC (Caso B — S3 Público)"]
        UA["Usuario A"] -->|"HTTP directo"| S3a["S3 PÚBLICO"]
        Hacker["😈 Atacante"] -->|"HTTP directo ¡también!"| S3a
    end

    subgraph Con_OAC["✅ Con OAC (Caso C — S3 Privado)"]
        UB["Usuario B"] -->|"HTTPS"| CF2["CloudFront\n(WAF, Rate Limit)"]
        CF2 -->|"SigV4 firmado"| S3b["S3 PRIVADO\n(acceso público bloqueado)"]
        Hacker2["😈 Atacante"] -->|"403 Forbidden"| S3b
    end

    style S3a fill:#E74C3C,color:#fff
    style S3b fill:#27AE60,color:#fff
    style CF2 fill:#FF9900,color:#fff
```

---

## 🔗 Referencias

- [README del Caso C](../README.md)
- [Guía Paso a Paso AWS](../AWS_PASO_A_PASO.md)
- [Ver Demo en Vivo](https://d3otfpeykrm536.cloudfront.net/)
