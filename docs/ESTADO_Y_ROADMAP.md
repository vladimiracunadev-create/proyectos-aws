# 📍 Estado Actual y Hoja de Ruta

> **Autor:** Vladimir Acuna
> **Ultima actualizacion:** 17 de marzo de 2026
> **Proposito:** Radiografia del repositorio — que hay, que falta, que viene, en que orden.

---

## Estado general

```
Madurez técnica:     ████████░░  80%  — 11/~13 casos core completados
Documentación:       █████████░  90%  — completa, actualizada, navegable
Skills y flujos:     █████████░  95%  — 11 skills cubren todos los workflows
FinOps:              ████████░░  80%  — falta conectar datos reales en calculadora
Evidencia visual:    ███████░░░  70%  — Caso H sin VISUALIZATION.md
Casos futuros:       ████░░░░░░  40%  — M en Fase 0, I proyectado
```

---

## Mapa de progresion de casos

```mermaid
graph TB
    subgraph T1["Tier 1 — Hosting"]
        A["✅ Caso A\nAmplify"]
        B["✅ Caso B\nS3 + GitLab CI"]
    end

    subgraph T2["Tier 2 — IaC y Backend"]
        C["✅ Caso C\nTerraform + CloudFront"]
        D["✅ Caso D\nServerless Basic"]
        E["✅ Caso E\nDynamoDB Single Table"]
        G["✅ Caso G\nEvent Driven"]
    end

    subgraph T25["Tier 2.5 — Seguridad y Observabilidad"]
        F["✅ Caso F\nCognito + JWT + WAF"]
        H["✅ Caso H\nCloudWatch + X-Ray"]
    end

    subgraph T3["Tier 3 — Contenedores"]
        J["✅ Caso J\nECS Fargate + ALB"]
        K["✅ Caso K\nKubernetes EKS"]
    end

    subgraph T4["Tier 4 — Gobernanza y Resiliencia"]
        L["✅ Caso L\nFinOps + OIDC"]
        M["🔄 Caso M\nResiliencia Failover\n(Fase 0)"]
    end

    subgraph T5["Tier 5 — IA y Avanzado"]
        I["⏳ Caso I\nGenAI Bedrock"]
        N["⏳ Caso N\nCI/CD Avanzado"]
        O["⏳ Caso O\nObservabilidad Distribuida"]
    end

    A --> B --> C --> D --> E
    E --> F & G
    F --> H
    G --> H
    H --> J --> K --> L --> M --> I
    M --> N
    I --> O

    style A fill:#2ea043,color:#fff
    style B fill:#2ea043,color:#fff
    style C fill:#2ea043,color:#fff
    style D fill:#2ea043,color:#fff
    style E fill:#2ea043,color:#fff
    style F fill:#2ea043,color:#fff
    style G fill:#2ea043,color:#fff
    style H fill:#2ea043,color:#fff
    style J fill:#2ea043,color:#fff
    style K fill:#2ea043,color:#fff
    style L fill:#2ea043,color:#fff
    style M fill:#f0883e,color:#fff
    style I fill:#8b949e,color:#fff
    style N fill:#8b949e,color:#fff
    style O fill:#8b949e,color:#fff
```

---

## Lo que esta solido hoy

### Casos completados (11)

| Caso | Nombre | Tecnologia principal | Demo / Evidencia |
|---|---|---|---|
| A | AWS Amplify | Amplify Hosting | Demo en vivo |
| B | S3 + GitLab CI | S3 Website + CI/CD | Demo en vivo |
| C | Terraform + CloudFront | Terraform IaC + CDN | Demo en vivo |
| D | Serverless Basic | Lambda + API GW + DynamoDB | Demo en vivo |
| E | DynamoDB Persistence | Single Table + GSI + Transacciones | Demo en vivo |
| F | Security First | Cognito + JWT Authorizer + WAF | Demo en vivo |
| G | Event Driven | EventBridge + SQS + DLQ + SNS | Demo en vivo |
| H | Observability | CloudWatch + X-Ray + Dashboard IaC | Demo en vivo |
| J | Contenedores ECS | Docker + ECR + Fargate + ALB | Reporte de evidencia |
| K | Kubernetes EKS | EKS + kubectl + Terraform | Reporte de evidencia |
| L | FinOps Governance | Budgets + OIDC + Cost Explorer | Demo en vivo |

### Infraestructura de documentacion

```mermaid
flowchart TB
    subgraph Raiz["📁 Raiz"]
        direction TB
        RM["README.md"]
        CL["CHANGELOG.md"]
        RD["ROADMAP.md"]
        CJ["AWS_CLOUD_JOURNEY.md"]
    end

    subgraph Docs["📂 docs/"]
        direction TB
        AR["ARCHITECTURE.md"]
        FS["FILE_STRUCTURE.md"]
        FC["FINOPS_COSTOS.md"]
        SK["SKILLS.md"]
        CN["CONCEPTOS_NUBE.md"]
        RC["RECRUITER.md"]
        ES["ESTADO_Y_ROADMAP.md"]
        CE["cert-saa / cert-dva / cert-soa"]
    end

    subgraph Skills["🛠️ skills/ (11)"]
        direction TB
        S1["aws-case-scaffolder"]
        S2["sam-serverless-workflow"]
        S3["lambda-test-patterns"]
        S4["architecture-doc-standard"]
        S5["caso-completion-checklist"]
        S6["visualizacion-evidencia"]
        S7["docs-portal-sync"]
        S8["gitlab-aws-pipeline-editor"]
        S9["terraform-aws-demo-patterns"]
        S10["finops-audit-and-budgeting"]
        S11["repo-status-analysis"]
    end

    subgraph Portal["🌐 GitLab Pages"]
        direction TB
        PO["index.html — sidebar"]
        CA["apps/cost-calculator"]
    end

    RM --> Docs
    RM --> Skills
    RM --> Portal
    CJ --> Docs
```

### Sistema de skills (11)

```mermaid
flowchart LR
    Q1{{"¿Que\nnecesito\nhacer?"}}

    Q1 -->|Caso nuevo| SC["aws-case-scaffolder"]
    Q1 -->|Deploy SAM| SW["sam-serverless-workflow"]
    Q1 -->|Tests Lambda| TP["lambda-test-patterns"]
    Q1 -->|architecture.md| AD["architecture-doc-standard"]
    Q1 -->|Completar caso| CH["caso-completion-checklist"]
    Q1 -->|Evidencia / destroy| VE["visualizacion-evidencia"]
    Q1 -->|Docs / portal| DS["docs-portal-sync"]
    Q1 -->|CI/CD pipeline| GP["gitlab-aws-pipeline-editor"]
    Q1 -->|Terraform| TF["terraform-aws-demo-patterns"]
    Q1 -->|Costos FinOps| FA["finops-audit-and-budgeting"]
    Q1 -->|Estado / roadmap| RS["repo-status-analysis"]

    style SC fill:#1f6feb,color:#fff
    style SW fill:#1f6feb,color:#fff
    style TP fill:#1f6feb,color:#fff
    style AD fill:#1f6feb,color:#fff
    style CH fill:#1f6feb,color:#fff
    style VE fill:#1f6feb,color:#fff
    style DS fill:#1f6feb,color:#fff
    style GP fill:#1f6feb,color:#fff
    style TF fill:#1f6feb,color:#fff
    style FA fill:#1f6feb,color:#fff
    style RS fill:#1f6feb,color:#fff
```

---

## Lo que esta pendiente o incompleto

### Gaps actuales

```mermaid
flowchart TB
    subgraph CRITICO["🔴 Prioritario"]
        direction TB
        G1["❌ Caso H — VISUALIZATION.md faltante"]
        G1N["unico caso con costo fijo sin reporte de evidencia"]
        G1 --- G1N
    end

    subgraph MEDIO["🟡 En progreso"]
        direction TB
        G2["🔄 Caso M — Fase 0 activa"]
        G2N["Scaffolding listo, implementacion pendiente"]
        G3["🔄 Wiki — submodulo desincronizado"]
        G3N["wiki/ del repo no se sincroniza al GitLab Wiki real"]
        G2 --- G2N
        G3 --- G3N
    end

    subgraph BAJO["🟢 Mejora futura"]
        direction TB
        G4["🔧 Calculadora — usa precios estaticos"]
        G4N["Podria conectarse a Cost Explorer real"]
        G5["🔧 Portal — visor basico de Markdown"]
        G5N["Podria mostrar estado de stacks en vivo"]
        G4 --- G4N
        G5 --- G5N
    end

    CRITICO --> MEDIO --> BAJO

    style G1 fill:#da3633,color:#fff
    style G2 fill:#f0883e,color:#fff
    style G3 fill:#f0883e,color:#fff
    style G4 fill:#d29922,color:#fff
    style G5 fill:#d29922,color:#fff
    style G1N fill:#21262d,color:#8b949e
    style G2N fill:#21262d,color:#8b949e
    style G3N fill:#21262d,color:#8b949e
    style G4N fill:#21262d,color:#8b949e
    style G5N fill:#21262d,color:#8b949e
```

---

## Mejoras futuras — ordenadas por impacto

### Prioridad Alta

#### 1. Caso H — VISUALIZATION.md
El unico caso con recurso de costo fijo (CloudWatch Dashboard $3/mes) que no tiene reporte de evidencia. Los casos J y K ya lo tienen. Usar `/visualizacion-evidencia caso-h`.

#### 2. Caso M Fase 1 — Resiliencia Multi-AZ

```mermaid
flowchart LR
    subgraph Fase1["Fase 1 — Multi-AZ (~$30/lab)"]
        ALB["ALB\nMulti-AZ"] --> ECS1["ECS Fargate\nAZ-1"]
        ALB --> ECS2["ECS Fargate\nAZ-2"]
        R53["Route 53\nHealth Checks"] --> ALB
    end

    subgraph Fase2["Fase 2 — Multi-Region (~$60/lab)"]
        R53B["Route 53\nFailover Policy"] --> Primary["Primary\nus-east-1"]
        R53B --> Secondary["Secondary\nus-west-2"]
    end

    Fase1 --> Fase2

    style Fase1 fill:#1f3a5f,color:#fff
    style Fase2 fill:#0d2137,color:#fff
```

Estrategia: deploy → validar failover real → destroy. Prerequisito: Caso K completado.

#### 3. Caso I — GenAI Bedrock (sin RAG)

```mermaid
flowchart LR
    Cliente["Cliente"] --> APIGW["API Gateway"]
    APIGW --> Lambda["Lambda\nPython 3.12"]
    Lambda --> Bedrock["Amazon Bedrock\nClaude Haiku"]
    Bedrock --> Lambda
    Lambda --> APIGW

    note["Costo: < $5/lab\nPay-per-token\nSin OpenSearch"]

    style Bedrock fill:#7b2d8b,color:#fff
    style note fill:#161b22,color:#8b949e
```

Claude Haiku via Bedrock en Lambda. Costo < $5 por laboratorio. **Sin OpenSearch Serverless** (minimo $350/mes — evitar).

---

### Prioridad Media

#### 4. Portal GitLab Pages mejorado

Estado actual vs estado futuro:

| Capacidad | Hoy | Futuro |
|---|---|---|
| Ver docs markdown | ✅ | ✅ |
| Calcular costos | ✅ (estatico) | ✅ (Cost Explorer real) |
| Estado de stacks | ❌ | ✅ via Lambda + API |
| CI status badges | ❌ | ✅ via GitLab API |
| Smoke test results | ❌ | ✅ desde artefactos CI |

#### 5. Calculadora de costos con datos reales

Conectar la calculadora de GitLab Pages a un endpoint Lambda que lea AWS Cost Explorer y devuelva el gasto real del mes. El Caso L ya tiene OIDC configurado — la infraestructura de autenticacion existe.

#### 6. Script de deploy-evidence-destroy automatizado

Para casos J y K, un script bash interactivo que:
1. Hace `terraform apply`
2. Espera confirmacion del usuario (las capturas)
3. Hace `terraform destroy` automaticamente tras confirmacion
4. Genera el resumen de costos del lab en el VISUALIZATION.md

---

### Prioridad Baja / Largo plazo

#### 7. Caso N — CI/CD avanzado

Pipelines multi-stage con ambientes reales (dev/staging/prod), deployment protection rules, revisiones de PR como gates de despliegue. Completaria el stack DevOps del repositorio.

#### 8. Caso O — Observabilidad distribuida

Trazas X-Ray entre multiples Lambdas en cadena, dashboards operacionales complejos, alertas con integracion externa. Prerequisito: Caso M completado.

#### 9. Ruta hacia certificacion AWS

```mermaid
flowchart LR
    Repo["Este\nrepositorio"]

    Repo -->|"80% cubierto"| SAA["☁️ SAA-C03\nSolutions Architect\nAssociate"]
    Repo -->|"60% cubierto"| DVA["💻 DVA-C02\nDeveloper\nAssociate"]
    Repo -->|"40% cubierto"| SOA["⚙️ SOA-C02\nSysOps\nAssociate"]

    SAA --> SAAD["Ver detalle →\ndocs/cert-saa-c03.md"]
    DVA --> DVAD["Ver detalle →\ndocs/cert-dva-c02.md"]
    SOA --> SOAD["Ver detalle →\ndocs/cert-soa-c02.md"]

    style SAA fill:#f90,color:#000
    style DVA fill:#f90,color:#000
    style SOA fill:#d29922,color:#000
    style SAAD fill:#21262d,color:#8b949e
    style DVAD fill:#21262d,color:#8b949e
    style SOAD fill:#21262d,color:#8b949e
```

Cada certificacion tiene su propio documento con dominios, temas requeridos y cobertura exacta por caso:
- 📄 [SAA-C03 — Solutions Architect Associate](cert-saa-c03.md): 80% cubierto — la más cercana
- 📄 [DVA-C02 — Developer Associate](cert-dva-c02.md): 60% cubierto — fuerte en Lambda y CI/CD
- 📄 [SOA-C02 — SysOps Associate](cert-soa-c02.md): 40% cubierto — requiere M y O para completar

---

## Tabla consolidada de mejoras

| # | Mejora | Prioridad | Esfuerzo | Costo lab | Prerequisito |
|---|---|---|---|---|---|
| 1 | Caso H VISUALIZATION.md | 🔴 Alta | 30 min | $0 | Ninguno |
| 2 | Caso M Fase 1 Multi-AZ | 🔴 Alta | 1-2 dias | ~$30 | Caso K ✅ |
| 3 | Caso I GenAI Bedrock | 🔴 Alta | 1 dia | < $5 | Caso H ✅ |
| 4 | Portal mejorado (estado stacks) | 🟡 Media | 1 dia | $0 | Caso L ✅ |
| 5 | Calculadora con Cost Explorer real | 🟡 Media | 1 dia | $0 | Caso L ✅ |
| 6 | Script deploy-evidence-destroy | 🟡 Media | 2-3 horas | $0 | J ✅, K ✅ |
| 7 | Caso N CI/CD avanzado | 🟢 Baja | 2-3 dias | $0 | Todos anteriores |
| 8 | Caso O Observabilidad distribuida | 🟢 Baja | 2-3 dias | < $5 | Caso M |
| 9 | Ruta certificacion AWS | 🟢 Baja | Estudio paralelo | $300 (examen) | Ninguno |

---

## Proxima sesion recomendada

```
1. /visualizacion-evidencia caso-h    ← 30 minutos, cierra el unico gap pendiente
2. Comandos SAM del Caso F            ← pendiente de la sesion anterior
3. Planificar Caso M Fase 1           ← siguiente nivel tecnico
```

---

*Documento generado el 17 de marzo de 2026 — refleja el estado real del repositorio tras las sesiones de implementacion de los casos F, H y la infraestructura de documentacion completa.*
