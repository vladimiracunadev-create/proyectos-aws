# Arquitectura: Caso H — Observability & Health

> Stack: API Gateway + Lambda + AWS X-Ray + CloudWatch Dashboard + CloudWatch Alarms
> Nivel: 7 — Observabilidad como código

---

## Vision general

Este caso implementa los tres pilares de observabilidad sobre la infraestructura serverless
ya existente. No despliega nueva lógica de negocio: instrumenta lo que ya existe con
trazas (X-Ray), métricas (CloudWatch custom) y alertas proactivas (CloudWatch Alarms).

El principio rector: **la observabilidad es código, no configuración manual**.
El dashboard y las alarmas nacen con el stack SAM y mueren con él.

---

## Diagrama 1: Flujo principal con X-Ray

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#4cc9f0', 'edgeColor': '#7ef0b8'}}}%%
sequenceDiagram
    participant U as Navegador / curl
    participant API as API Gateway HTTP API
    participant L as Lambda HealthDashboardFunction
    participant XR as AWS X-Ray
    participant CW as CloudWatch

    U->>API: GET / (landing)
    API->>L: Invocacion HTTP
    L-->>XR: Segmento de traza (auto)
    L-->>API: 200 HTML Premium
    API-->>U: Landing interactiva

    U->>API: GET /health
    API->>L: Invocacion HTTP
    L-->>XR: Subsegmento: health_payload
    L-->>API: 200 HTML o JSON
    API-->>U: Estado del servicio

    U->>API: POST /metrics
    API->>L: Invocacion HTTP
    L->>CW: PutMetricData (CasoH/HealthChecks)
    CW-->>L: OK
    L-->>XR: Subsegmento: put_metric_data
    L-->>API: 200 JSON
    API-->>U: Metrica publicada
```

---

## Diagrama 2: Arquitectura AWS completa

```mermaid
graph TB
    subgraph Client["Cliente"]
        U["Usuario / curl / Browser"]
    end

    subgraph Ingress["Capa de ingreso"]
        API["API Gateway HTTP API"]
        L["Lambda HealthDashboardFunction\n(Python 3.12 · X-Ray Active)"]
    end

    subgraph Observability["Capa de Observabilidad (IaC)"]
        XR["AWS X-Ray\nService Map + Traces"]
        CW["CloudWatch\nNamespace: CasoH"]
        DASH["CloudWatch Dashboard\ncaso-h-observability"]
        ALM1["Alarm: caso-h-lambda-errors\n≥ 1 error en 60s"]
        ALM2["Alarm: caso-h-lambda-duration-p99\np99 > 3000ms"]
        LOGS["CloudWatch Logs\n/aws/lambda/HealthDashboardFunction"]
    end

    U --> API
    API --> L
    L -->|traza automatica| XR
    L -->|PutMetricData| CW
    L -->|stdout estructurado| LOGS
    CW --> DASH
    CW --> ALM1
    CW --> ALM2

    style Ingress fill:#FFF8E1,stroke:#FFB300,stroke-width:2px
    style Observability fill:#E8F5E9,stroke:#43A047,stroke-width:2px
```

---

## Diagrama 3: Mapa de métricas y alarmas

```mermaid
graph LR
    subgraph AWS_Lambda["Métricas AWS/Lambda (built-in)"]
        INV["Invocations"]
        ERR["Errors"]
        DUR["Duration"]
        THR["Throttles"]
    end

    subgraph CasoH_NS["Métricas CasoH (custom)"]
        HC["HealthChecks / Count\nDimensión: Service=caso-h-observability"]
    end

    subgraph Alarms["CloudWatch Alarms"]
        A1["⚠️ caso-h-lambda-errors\nERR ≥ 1 en 60s"]
        A2["⚠️ caso-h-lambda-duration-p99\np99 > 3000ms en 60s"]
    end

    ERR --> A1
    DUR --> A2

    style AWS_Lambda fill:#FFF3E0,stroke:#EF6C00,stroke-width:2px
    style CasoH_NS fill:#E3F2FD,stroke:#1565C0,stroke-width:2px
    style Alarms fill:#FFEBEE,stroke:#E53935,stroke-width:2px
```

---

## Diagrama 4: X-Ray Service Map (esperado post-deploy)

```mermaid
graph LR
    A["AWS::APIGateway\nHTTP API"] --> B["AWS::Lambda\nHealthDashboardFunction"]
    B --> C["AWS::CloudWatch\nPutMetricData"]

    style A fill:#E8EAF6,stroke:#3949AB,stroke-width:2px
    style B fill:#FFF3E0,stroke:#EF6C00,stroke-width:2px
    style C fill:#E0F2F1,stroke:#00897B,stroke-width:2px
```

---

## Decisiones de diseño

| Decisión | Motivo |
|---|---|
| `Tracing: Active` en SAM Globals | Instrumenta todas las Lambdas sin modificar el código |
| Dashboard inline en CloudFormation | Se crea y destruye con el stack; cero deuda operativa |
| Namespace custom `CasoH` | Separa métricas de negocio de las métricas built-in de AWS |
| Alarma sobre `Errors` Sum(60s) ≥ 1 | Detecta cualquier error inmediatamente |
| Alarma sobre `Duration p99` > 3000ms | Detecta degradación de latencia antes que el usuario |
| `/health` HTML + JSON | Consistencia con Caso G; funciona para humanos y scripts |
| `PutMetricData` desde Lambda | Demuestra la integración activa con CloudWatch desde código |

---

## Qué aprende un reclutador

- Que defines observabilidad como código (IaC), no clics en la consola.
- Que entiendes los tres pilares: métricas, logs y trazas.
- Que differencias métricas técnicas (errores, latencia) de métricas de negocio.
- Que las alarmas son proactivas, no reactivas.
- Que X-Ray permite correlacionar una petición a través de múltiples servicios.

---

## Siguiente paso natural

El paso lógico después de este caso es:

- Conectar X-Ray con los stacks del Caso G (EventBridge) para ver el service map completo.
- Añadir métricas de cola SQS en el dashboard (profundidad, mensajes en DLQ).
- Implementar el Caso F (Cognito) para añadir métricas de autenticación.
