# Arquitectura Integral del Sistema: AWS-GitLab Monorepo

Este documento es la **fuente de verdad tecnica** del repositorio. Describe la evolucion desde hosting estatico hasta arquitecturas empresariales de alta disponibilidad, unificando los casos ya implementados y los siguientes niveles planificados.

---

## Vision ejecutiva

El proyecto sigue una arquitectura de **Monorepo Evolutivo**, disenado para demostrar la madurez de un Ingeniero Cloud a traves de niveles de complejidad crecientes. Cada nivel resuelve problemas concretos de escalabilidad, seguridad, persistencia, costos y continuidad operacional usando servicios administrados de AWS.

### Pilares de excelencia

- **IaC primero**: Todo recurso relevante en AWS tiene una definicion declarativa (`Terraform`, `SAM`, `YAML`).
- **Seguridad desde el inicio**: Analisis estatico, escaneo de secretos y minimizacion de privilegios.
- **Observabilidad y costo**: La operacion incluye FinOps, trazabilidad y decision tecnica orientada a impacto.
- **Evolucion por casos**: Cada carpeta agrega una capacidad nueva sobre la anterior, no un ejercicio aislado.

---

## Mapa de evolucion arquitectonica

### Tier 1: Fundamentos y hosting estático (Casos A, B)

*Enfoque: velocidad de entrega y automatización básica.*

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#6C4DE6', 'secondaryColor': '#FF9900', 'tertiaryColor': '#f4f4f4', 'fontsize': '16px' }}}%%
graph TB
    subgraph Tier1_A["🟢 Nivel 0: ClickOps"]
        direction TB
        A1[🦊 GitLab] -->|Mirror| A2[☁️ AWS Amplify]
        A2 -->|Auto-Deploy| A3[📦 S3 + CloudFront]
    end

    subgraph Tier1_B["🟢 Nivel 1: Pipeline Manual"]
        direction TB
        B1[🏃 GitLab Runner] -->|AWS CLI| B2[🪣 S3 Bucket]
        B2 -->|Hosting| B3[🌐 Website Endpoint]
    end

    style Tier1_A fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style Tier1_B fill:#f1f8e9,stroke:#558b2f,stroke-width:2px
```

### Tier 2: IaC, serverless, persistencia y eventos (Casos C, D, E, G)

*Enfoque: reproducibilidad, backend reactivo y modelado de datos por patrones de acceso.*

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#844FBA', 'edgeColor': '#2496ED', 'fontsize': '16px' }}}%%
graph TB
    subgraph Tier2_C["🔵 Caso C: IaC & CDN"]
        direction TB
        C1[🏗️ Terraform] -->|OAC| C2[☁️ CloudFront]
        C2 -->|Private Fetch| C3[🪣 S3 Bucket]
    end

    subgraph Tier2_D["🔵 Caso D: Serverless API"]
        direction TB
        D1[🌐 API Gateway] -->|Invoca| D2[⚡ Lambda]
        D2 -->|CRUD básico| D3[🗄️ DynamoDB]
    end

    subgraph Tier2_E["🟠 Caso E: Persistence Pro"]
        direction TB
        E1[📱 Landing / Frontend] --> E2[🌐 API Gateway HTTP]
        E2 --> E3[⚡ Lambda Orders]
        E3 --> E4[🗄️ DynamoDB Single Table]
        E4 -.-> E5[📊 GSI Estado]
        E4 -.-> E6[📊 GSI Producto]
    end

    subgraph Tier2_G["🟡 Caso G: Event Driven"]
        direction TB
        G1[🌐 API Gateway HTTP] --> G2[⚡ Lambda Publisher]
        G2 --> G3[📨 EventBridge]
        G3 --> G4[📬 SQS Queue]
        G4 --> G5[⚡ Lambda Consumer]
        G4 -. redrive .-> G6[🧯 DLQ]
        G5 --> G7[📣 SNS]
    end

    style Tier2_C fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style Tier2_D fill:#e1f5fe,stroke:#0277bd,stroke-width:2px
    style Tier2_E fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    style Tier2_G fill:#fff8e1,stroke:#ff8f00,stroke-width:2px
```

### Tier 2.5: Seguridad y Observabilidad (Casos F, H)

*Enfoque: perimetro de identidad, validacion nativa de tokens y monitoreo como codigo.*

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#7b2ff7', 'edgeColor': '#c77dff', 'fontsize': '16px' }}}%%
graph TB
    subgraph Tier_F["🔐 Caso F: Security First"]
        direction TB
        F1[☁️ WAF WebACL<br/>SQLi + Common Rules] -->|filtra| F2[🌐 API GW HTTP API<br/>JWT Authorizer]
        F2 -->|rutas publicas| F3[⚡ Lambda — register / login]
        F3 -->|sign_up / initiate_auth| F4[🔑 Cognito User Pool]
        F4 -->|Pre-Signup trigger| F5[⚡ Lambda Pre-SignUp]
        F2 -->|rutas protegidas — claims| F6[⚡ Lambda — profile]
    end

    subgraph Tier_H["📊 Caso H: Observability"]
        direction TB
        H1[🌐 API GW HTTP API] --> H2[⚡ Lambda + X-Ray]
        H2 -->|PutMetricData| H3[📊 CloudWatch Custom Metrics]
        H3 --> H4[🖥️ CW Dashboard IaC]
        H3 --> H5[🔔 CW Alarms]
    end

    style Tier_F fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    style Tier_H fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
```

### Tier 3: Contenedores y orquestación (Casos J, K)

*Enfoque: portabilidad industrial y gestión de flotas.*

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#2496ED', 'tertiaryColor': '#326CE5', 'fontsize': '16px' }}}%%
graph TB
    subgraph SupplyChain["📦 Container Supply Chain"]
        direction TB
        J1[🐳 Docker] --> J2[📦 AWS ECR]
        J2 --> J3[🚀 ECS Fargate]
        J2 --> J4[☸️ EKS Cluster]
    end

    J3 --> ALB[⚖️ ALB / Ingress]
    J4 --> ALB
    ALB --> User[🌍 Usuario]

    style SupplyChain fill:#f5f5f5,stroke:#333,stroke-width:2px
    style J3 fill:#FF9900,color:#fff
    style J4 fill:#326CE5,color:#fff
```

### Tier 4: Gobernanza, FinOps y resiliencia (Casos L, M)

*Enfoque: excelencia operativa y continuidad de negocio.*

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#F39C12', 'edgeColor': '#E74C3C', 'fontsize': '16px' }}}%%
graph TB
    subgraph Tier4_L["🟣 Governance & FinOps"]
        direction TB
        L1[🔑 GitLab OIDC] -->|Auth| L2[🔐 IAM Role]
        L2 -->|Monitor| L3[💰 Cost Control]
    end

    subgraph Tier4_M["🔴 Resilience & Failover"]
        direction TB
        M1[🌐 Route 53] -->|Route| M2[🟢 Region Primary]
        M1 -.->|Failover| M3[🟡 Region Standby]
    end

    style Tier4_L fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    style Tier4_M fill:#ffebee,stroke:#c62828,stroke-width:2px
```

---

## Donde encajan los Casos E y G

El `Caso E` ya no es una idea futura: es el modulo de persistencia avanzada que demuestra como pasar de una API serverless simple a un backend con modelado NoSQL real.

Capacidades ya resueltas:

- tabla unica con `pk/sk`
- consultas por cliente, estado y producto sin scans completos
- escritura transaccional de `ORDER + AUDIT`
- landing publica en `/` para explicar y probar el caso
- despliegue validado en AWS en `us-east-2`

Esto lo convierte en el puente natural entre el `Caso D` y el `Caso G`.

El `Caso G` ya valida el siguiente salto de madurez:

- landing publica en `/` para explicar el despliegue y probarlo en vivo
- publicacion de eventos en EventBridge
- desacoplamiento productor/consumidor con SQS
- aislamiento de fallos con DLQ
- notificacion posterior por SNS
- validacion real en AWS con endpoint publico en `us-east-2`

---

## Patrones de diseno estandar

### 1. Professional Deployment Tier

Para los casos de infraestructura y backend:

- **Scan**: validaciones de seguridad y consistencia
- **Plan/Build**: generacion de artefactos reproducibles
- **Deploy**: despliegue controlado en AWS
- **Validation**: smoke tests, links operativos y documentacion

### 2. Persistencia orientada a consultas

El `Caso E` introduce una decision clave del monorepo: en NoSQL se modela por preguntas de negocio, no por normalizacion relacional.

Patrones resueltos:

- cliente -> ordenes
- estado -> ordenes
- producto -> ordenes
- orden -> eventos de auditoria

### 3. Integracion asincrona y contratos de eventos

El `Caso G` agrega un patron igual de importante: no todo debe resolverse en la misma llamada HTTP.

Patrones resueltos:

- aceptar un evento con `202 Accepted`
- separar productor y consumidor
- amortiguar carga con SQS
- reintentar y aislar errores con DLQ
- extender procesamiento con SNS sin tocar la API de entrada

### 4. Zero-Trust Identity

La direccion objetivo del repositorio es operar con credenciales efimeras via `OIDC`, reduciendo el uso de llaves IAM permanentes en pipelines y automatizaciones.

---

## Comparativa de runtimes

| Criterio | Lambda | ECS Fargate | EKS |
|---|---|---|---|
| **Escalamiento** | Instantaneo (a cero) | Rapido | Industrial |
| **Costo** | Pago por uso | Por tiempo de task | Base fija + nodos |
| **Complejidad** | Baja | Media | Alta |
| **Caso ideal** | APIs, eventos, integracion | Apps empaquetadas | Plataformas de microservicios |

---

## Estrategia de seguridad integral

1. **Proteccion de datos**: CloudFront privado con OAC donde aplica, y persistencia en servicios gestionados.
2. **Shift-left security**: El pipeline detecta errores de seguridad antes del despliegue.
3. **Gobernanza regional**: Preferencia operativa por `us-east-2`, con restricciones y control de costos.
4. **Segregacion por patron**: En `Caso E`, las lecturas operativas se resuelven por GSIs en vez de scans masivos.

---

## Modelo FinOps

La arquitectura prioriza costo bajo o controlado:

- `Lambda` para cargas esporadicas y costo cercano a cero cuando no hay trafico.
- `DynamoDB PAY_PER_REQUEST` para no sobredimensionar capacidad.
- `TTL` para expiracion automatica de datos temporales cuando corresponda.
- entornos de contenedores hibernados cuando no estan en uso.

---

## Confiabilidad

| Escenario | Mecanismo | RTO esperado | RPO esperado |
|---|---|---|---|
| Fallo de funcion | Reintento serverless / nueva invocacion | Segundos | 0 o minimo |
| Error de consumidor asincrono | Reintentos SQS + DLQ | Segundos a minutos | 0 o minimo |
| Caida de AZ | Multi-AZ en servicios administrados | < 60 segundos | 0 o minimo |
| Caida de region | Route 53 Failover (futuro Caso M) | < 120 segundos | < 5 minutos |

---

> Mantenido por Vladimir Acuna.
> Este documento debe reflejar siempre el estado real del repositorio, no un estado aspiracional.
