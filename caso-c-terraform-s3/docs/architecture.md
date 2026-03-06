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
graph TD
    subgraph Dev["💻 Dev"]
        PR["Merge Request\ncon cambios en\ncaso-c-terraform-s3/"]
    end

    subgraph CI["🦊 GitLab CI Pipeline"]
        direction TB
        Security["🔐 scan_infrastructure\n(stage: security)\ntfsec + ignores documentados\nValida HCL estándar"]
        
        subgraph BuildDeploy["🚀 Despliegue"]
            Plan["🟡 plan_case_c\n(stage: plan-infrastructure)\nterraform plan -out=tfplan"]
            Apply["🔴 deploy_case_c\n(stage: deploy)\nterraform apply tfplan"]
            Invalidate["🧹 invalidate_cloudfront_c\n(stage: deploy)\naws-cli: invalidation /*"]
        end
    end

    subgraph AWS["☁️ AWS"]
        RemoteState["S3 Remote State\nDynamoDB Lock"]
        Resources["CloudFront + S3 + OAC"]
    end

    PR --> Security
    Security --> Plan
    Plan -->|"needs: plan_case_c"| Apply
    Apply -->|"needs: deploy_case_c"| Invalidate
    
    Plan <-->|"Lock/State"| RemoteState
    Apply -->|"Crea recursos"| Resources
    Invalidate -->|"Limpia caché"| Resources

    style Plan fill:#F39C12,color:#fff
    style Apply fill:#E74C3C,color:#fff
    style Security fill:#8E44AD,color:#fff
    style Invalidate fill:#3498DB,color:#fff
```

---

## 🔧 Componentes y Roles

| Componente | Servicio | Función | Por Qué es Mejor que Caso B |
|---|---|---|---|
| **CDN** | CloudFront | Cache global, HTTPS, redirect HTTP→HTTPS | Caso B no tiene CDN |
| **OAC** | CloudFront Origin Access Control | S3 privado, solo CloudFront accede | Caso B: bucket público |
| **IaC** | Terraform | Infraestructura reproducible y versionada | Caso B: config manual |
| **Security Scan** | tfsec | Auditoría estática (shift-left security) | Caso B: sin análisis |
| **CD Automation** | GitLab CI | Pipeline multi-stage (Scan -> Plan -> Apply -> Invalidate) | Caso B: sync directo |

---

## 🔐 Seguridad: Decisiones de Diseño (Trade-offs)

En este proyecto de **portafolio**, se han tomado decisiones conscientes para balancear seguridad y costos:

1. **S3 Block Public Access**: El bucket es 100% privado.
2. **OAC (Origin Access Control)**: Se eliminó el uso de OAI (legado) por OAC (estándar actual).
3. **tfsec Ignores**: Se utilizan `#tfsec:ignore` para controles que implican costos fijos (WAF, KMS) o infraestructura adicional compleja (Logging buckets), manteniendo la transparencia técnica.
4. **HCL Estándar**: Se corrigió el uso de sintaxis experimental (`action` blocks) por HCL 1.0/2.0 compatible, garantizando estabilidad.

---

## 🔗 Referencias

- [README del Caso C](../README.md)
- [Guía Paso a Paso AWS](../AWS_PASO_A_PASO.md)
- [Ver Demo en Vivo](https://d3otfpeykrm536.cloudfront.net/)
