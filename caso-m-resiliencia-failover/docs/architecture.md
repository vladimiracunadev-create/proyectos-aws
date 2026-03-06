# 🏗️ Arquitectura Objetivo: Caso M (Resiliencia & Failover)

> **Estado**: Documentación de arquitectura futura. No hay recursos AWS desplegados en Fase 0.
> Esta arquitectura es la **meta** que se implementará en Fases 1-3.

---

## 🎯 Visión General

La arquitectura del Caso M se basa en el principio de **eliminar todo Single Point of Failure
(SPOF)** en capas:

1. **Capa de Cómputo**: Múltiples instancias/tasks distribuidos en múltiples AZs.
2. **Capa de Red/Balanceo**: ALB distribuyendo tráfico entre AZs con health checks activos.
3. **Capa de DNS/Routing Global**: Route 53 con Failover Routing Policy detectando fallos
   regionales y redirigiendo automáticamente.
4. **Capa de Datos**: (Fase 3) Replicación cross-region de datos críticos.

---

## 📐 Diagrama 1: Arquitectura Multi-AZ (Nivel A — Fase 1)

```mermaid
graph TB
    subgraph Internet
        Client["🌍 Cliente / Usuario"]
    end

    subgraph Region["🇺🇸 AWS us-east-1 (Región Primaria)"]
        ALB["⚖️ Application Load Balancer\nDNS: api-primary.us-east-1.elb.amazonaws.com\nHealth Check: /healthz cada 15s"]

        subgraph AZ_A["📍 us-east-1a"]
            Task_A1["🐳 ECS Task / EC2\nApp Instance A1\n/healthz → 200 OK"]
        end

        subgraph AZ_B["📍 us-east-1b"]
            Task_B1["🐳 ECS Task / EC2\nApp Instance B1\n/healthz → 200 OK"]
        end

        subgraph AZ_C["📍 us-east-1c"]
            Task_C1["🐳 ECS Task / EC2\nApp Instance C1\n/healthz → 200 OK"]
        end

        CloudWatch["📊 CloudWatch\nMétricas ALB\nAlarmas"]
    end

    Client -->|"HTTPS"| ALB
    ALB -->|"Round-Robin / Least Connections"| Task_A1
    ALB -->|"Round-Robin / Least Connections"| Task_B1
    ALB -->|"Round-Robin / Least Connections"| Task_C1
    ALB -.->|"Health Check"| CloudWatch

    style ALB fill:#FF9900,color:#fff
    style Task_A1 fill:#2496ED,color:#fff
    style Task_B1 fill:#2496ED,color:#fff
    style Task_C1 fill:#2496ED,color:#fff
    style CloudWatch fill:#7C4DFF,color:#fff
```

### Flujo de Fallo Multi-AZ

```mermaid
sequenceDiagram
    participant C as 🌍 Cliente
    participant ALB as ⚖️ ALB
    participant T1 as 🐳 Task A1 (us-east-1a)
    participant T2 as 🐳 Task B1 (us-east-1b)
    participant CW as 📊 CloudWatch

    C->>ALB: GET /api/resource
    ALB->>T1: proxy request
    T1-->>ALB: 200 OK

    Note over T1: 💥 AZ us-east-1a FALLA

    ALB->>T1: GET /healthz (Health Check)
    T1--xALB: ⏱️ Timeout / Connection Refused

    Note over ALB: Después de 2 checks fallidos:\nMarca T1 como UNHEALTHY

    ALB->>CW: Alarma: UnHealthyHostCount > 0
    C->>ALB: GET /api/resource (nueva request)
    ALB->>T2: proxy request (T1 excluido)
    T2-->>ALB: 200 OK
    ALB-->>C: 200 OK

    Note over C,T2: ✅ El cliente nunca nota el fallo
```

---

## 📐 Diagrama 2: Arquitectura Multi-Región (Nivel B — Fase 2)

```mermaid
graph TB
    subgraph Internet
        Client["🌍 Cliente / Usuario"]
        R53["🔄 AWS Route 53\nFailover Routing Policy\nTTL: 60s\nHealth Check: cada 30s"]
    end

    subgraph Primary["🇺🇸 AWS us-east-1 (PRIMARIA — Activa)"]
        ALB_P["⚖️ ALB Primario\nHealthy en condiciones normales"]
        ECS_P["📦 ECS Fargate\ndesired=2, Multi-AZ"]
        Data_P["🗄️ RDS / DynamoDB\n(datos maestros)"]
    end

    subgraph Secondary["🌎 AWS us-west-2 (SECUNDARIA — Warm Standby)"]
        ALB_S["⚖️ ALB Secundario\n(en standby, siempre activo)"]
        ECS_S["📦 ECS Fargate\ndesired=1, puede escalar"]
        Data_S["🗄️ RDS Read Replica /\nDynamoDB Global Tables\n(replicación async)"]
    end

    Client -->|"DNS Query: api.dominio.com"| R53
    R53 -->|"✅ Respuesta: ip-primaria (Normal)"| Client
    R53 -.->|"🔍 Health Check al ALB Primario"| ALB_P

    Client -->|"HTTPS (Normal)"| ALB_P
    ALB_P --> ECS_P
    ECS_P <--> Data_P
    Data_P -.->|"Replicación async"| Data_S

    Note1["💥 FAILOVER:\n1. ALB Primario falla health check\n2. Route 53 detecta (30s)\n3. DNS cambia a ip-secundaria (TTL 60s)\n4. Clientes reconectan a us-west-2"]

    Client -.->|"HTTPS (Post-Failover)"| ALB_S
    ALB_S -.-> ECS_S
    ECS_S -.-> Data_S

    style ALB_P fill:#FF9900,color:#fff
    style ALB_S fill:#FF6B35,color:#fff
    style ECS_P fill:#2496ED,color:#fff
    style ECS_S fill:#6B9BD2,color:#fff
    style R53 fill:#E74C3C,color:#fff
    style Note1 fill:#FFF3CD,color:#333,stroke:#F0AD4E
```

---

## 📐 Diagrama 3: Opción Alternativa con Global Accelerator (Fase 3)

```mermaid
graph LR
    Client["🌍 Cliente"]
    GA["⚡ AWS Global Accelerator\n2 IPs Anycast estáticas\nSLA 99.99%\nRTO < 30s (vs ~60s Route53)"]
    ALB_P["⚖️ ALB us-east-1\n(Endpoint Primario)"]
    ALB_S["⚖️ ALB us-west-2\n(Endpoint Secundario)"]

    Client -->|"IP Anycast fija"| GA
    GA -->|"Peso 100 (normal)"| ALB_P
    GA -.->|"Peso 0 → 100 (failover)"| ALB_S

    Note["📝 Ventaja vs Route 53:\n- IPs estáticas (sin TTL DNS)\n- Failover en TCP layer (más rápido)\n- Ideal para clientes móviles con IPs cacheadas\n⚠️ Costo: $18 USD/mes fijo + transfer"]

    style GA fill:#9B59B6,color:#fff
    style ALB_P fill:#FF9900,color:#fff
    style ALB_S fill:#FF6B35,color:#fff
    style Note fill:#F0F0F0,color:#333
```

---

## 📊 Consideraciones RTO/RPO

### Definiciones (en lenguaje simple)

| Término | Definición | Analogía |
|---|---|---|
| **RTO** (Recovery Time Objective) | ¿Cuánto tiempo puede estar caído el sistema? | "Cuánto tardamos en reabrir la tienda tras un corte de luz" |
| **RPO** (Recovery Point Objective) | ¿Cuántos datos podemos perder? | "¿Desde qué hora del último backup volvemos?" |

### Objetivos por Fase

| Fase | Escenario | RTO Objetivo | RPO Objetivo | Mecanismo |
|---|---|---|---|---|
| **Fase 1** | Caída de 1 instancia/task | < 30 segundos | 0 (stateless) | ALB Health Check + auto-replace |
| **Fase 1** | Caída de 1 AZ completa | < 60 segundos | 0 (stateless) | ALB Multi-AZ routing |
| **Fase 2** | Caída de región primaria | < 120 segundos | < 5 minutos | Route 53 Failover + Warm Standby |
| **Fase 3** | Caída de región (con GA) | < 30 segundos | < 1 minuto | Global Accelerator + DynamoDB Global Tables |

### Por Qué Esto Importa para un Reclutador

> **Un SRE mide su éxito en segundos, no en horas.**
>
> La diferencia entre un sistema con RTO de 4 horas (restaurar desde backup) y uno con RTO de
> 60 segundos (failover automático) es exactamente lo que separa un hobby project de un sistema
> que soporta millones de usuarios 24/7. Este caso demuestra el segundo.

---

## 🔧 Componentes de la Arquitectura

| Componente | Servicio AWS | Propósito | Costo Referencial |
|---|---|---|---|
| **Balanceo de Carga** | Application Load Balancer (ALB) | Distribuir tráfico entre AZs + health checks | ~$16/mes |
| **Cómputo** | ECS Fargate / EC2 ASG | Ejecutar la aplicación (sin estado) | ~$10-30/mes |
| **Imágenes** | ECR (Elastic Container Registry) | Almacenar imágenes Docker | Free Tier: 500MB |
| **DNS & Failover** | Route 53 | Resolución DNS + Failover automático | $0.50/zona + $0.75/HC |
| **Monitoreo** | CloudWatch | Métricas, alarmas, dashboards | Free Tier generoso |
| **IaC** | Terraform | Infraestructura reproducible | Gratis |
| **(Fase 3) Routing** | Global Accelerator | RTO < 30s, IPs estáticas | $18/mes + transfer |
| **(Fase 3) DB Global** | DynamoDB Global Tables | Replicación multi-región automática | Por uso |

---

## 🔗 Referencias

- [AWS Well-Architected: Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [Route 53 Failover Routing](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy-failover.html)
- [ALB Health Checks](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html)
- [AWS Global Accelerator](https://docs.aws.amazon.com/global-accelerator/latest/dg/what-is-global-accelerator.html)
- [DynamoDB Global Tables](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GlobalTables.html)
