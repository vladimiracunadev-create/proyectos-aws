# Arquitectura: Caso G - Event Driven

> Stack: API Gateway + Lambda + EventBridge + SQS + SNS + AWS SAM
> Nivel: 6 - Integracion asincrona y desacoplamiento por eventos

---

## Vision general

Este caso modela una arquitectura donde la escritura inicial y el procesamiento posterior ya no
ocurren en la misma transaccion ni en el mismo servicio. El productor solo publica un hecho de
negocio. A partir de ahi, el bus de eventos y la cola desacoplan tiempos, reintentos y errores.

El escenario representado es simple pero muy util para entrevistas y aprendizaje:

- una orden es creada
- el health check puede leerse como HTML o como JSON segun quien lo consuma
- el evento se publica en EventBridge
- una regla lo enruta a SQS
- una Lambda lo consume y emite una notificacion
- si algo falla repetidamente, el mensaje termina en DLQ

---

## Diagrama 1: Flujo principal de publicacion

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#FF9900', 'edgeColor': '#1D4ED8', 'tertiaryColor': '#f4f4f4' }}}%%
sequenceDiagram
    participant UI as Navegador / Demo local
    participant API as API Gateway
    participant PUB as Lambda Publisher
    participant EB as EventBridge Bus
    participant Q as SQS Orders Queue
    participant CON as Lambda Consumer
    participant SNS as SNS Topic

    UI->>API: POST /events/orders
    API->>PUB: Invocacion HTTP
    PUB->>PUB: Valida payload
    PUB->>EB: PutEvents(OrderCreated)
    EB-->>PUB: eventId
    PUB-->>API: 202 Accepted
    API-->>UI: Evento aceptado
    EB->>Q: Enrutamiento por regla
    Q->>CON: Batch de mensajes
    CON->>SNS: Publish resumen
    SNS-->>CON: OK
```

---

## Diagrama 2: Ruta de error y DLQ

```mermaid
graph TB
    E["Evento OrderCreated"] --> B["EventBridge Rule"]
    B --> Q["SQS Orders Queue"]
    Q --> C["Lambda Consumer"]
    C -->|OK| N["SNS Notification"]
    C -->|Error| R["Reintento automatico"]
    R --> Q
    Q -->|maxReceiveCount superado| D["SQS DLQ"]

    style Q fill:#E3F2FD,stroke:#1E88E5,stroke-width:2px
    style C fill:#FFF3E0,stroke:#FB8C00,stroke-width:2px
    style D fill:#FFEBEE,stroke:#E53935,stroke-width:2px
    style N fill:#E8F5E9,stroke:#43A047,stroke-width:2px
```

---

## Diagrama 3: Arquitectura completa AWS

```mermaid
graph TB
    subgraph Client["Cliente"]
        U["Usuario / Browser"]
    end

    subgraph Ingress["Capa de ingreso"]
        API["API Gateway HTTP API"]
        PUB["Lambda OrderPublisherFunction"]
    end

    subgraph Events["Capa event-driven"]
        EB["EventBridge Bus caso-g-orders-bus"]
        RULE["Rule OrderCreatedRule"]
        Q["SQS orders-processing-queue"]
        DLQ["SQS orders-processing-dlq"]
    end

    subgraph Processing["Procesamiento"]
        CON["Lambda OrderConsumerFunction"]
        SNS["SNS processing-notifications"]
    end

    U --> API
    API --> PUB
    PUB --> EB
    EB --> RULE
    RULE --> Q
    Q --> CON
    CON --> SNS
    Q -. redrive .-> DLQ

    style Ingress fill:#FFF8E1,stroke:#FFB300,stroke-width:2px
    style Events fill:#E8EAF6,stroke:#3949AB,stroke-width:2px
    style Processing fill:#E0F2F1,stroke:#00897B,stroke-width:2px
```

---

## Diagrama 4: Contrato del evento

```mermaid
graph LR
    A["source: caso.g.orders"] --> D["detail-type: OrderCreated"]
    D --> E["detail.orderId"]
    D --> F["detail.customerId"]
    D --> G["detail.status"]
    D --> H["detail.total"]
    D --> I["detail.items[]"]
    D --> J["detail.forceFailure?"]

    style A fill:#FFF3E0,stroke:#EF6C00,stroke-width:2px
    style D fill:#E3F2FD,stroke:#1565C0,stroke-width:2px
```

---

## Decisiones de diseno

| Decision | Motivo |
|---|---|
| EventBridge como bus principal | Permite publicar eventos sin conocer a los consumidores. |
| SQS entre regla y consumidor | Absorbe picos de carga y desacopla el ritmo de procesamiento. |
| DLQ separada | Facilita troubleshooting sin perder mensajes problematicos. |
| Lambda publisher separada de consumer | Hace visible la diferencia entre ingesta y procesamiento. |
| SNS al final del flujo | Permite extender notificaciones o fan-out sin tocar el productor. |
| `202 Accepted` en la API | Refuerza el modelo asincrono: aceptar no significa procesar de inmediato. |
| `/health` con HTML y JSON | Permite explicar el chequeo a humanos sin romper scripts y monitoreo. |

---

## Que aprende un reclutador de este caso

- que sabes diferenciar integracion sincrona de asincrona
- que entiendes reintentos, redrive policy y DLQ
- que puedes modelar contratos de eventos
- que sabes preparar una base para observabilidad real

---

## Siguiente paso natural

El paso natural es complementar este caso con:

- metricas de profundidad de cola
- alarmas sobre DLQ
- correlacion por `eventId`
- dashboards y trazas distribuidas en el futuro Caso H
