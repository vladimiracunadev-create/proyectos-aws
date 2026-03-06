# 🏗️ Arquitectura: Caso D — Serverless API (SAM + Lambda + DynamoDB)

> **Stack**: API Gateway + AWS Lambda + DynamoDB + AWS SAM
> **Nivel**: 3 — Backend Reactivo sin Servidores

---

## 🎯 Visión General

El Caso D introduce el paradigma **serverless**: no hay servidores que gestionar, no hay
capacidad que aprovisionar. La aplicación escala a cero cuando no hay tráfico (costo = $0)
y escala automáticamente bajo demanda.

AWS SAM (Serverless Application Model) es la capa de IaC específica para funciones Lambda,
APIs y tablas DynamoDB — equivalente a Terraform pero optimizado para serverless.

---

## 📐 Diagrama 1: Arquitectura Completa Serverless

```mermaid
graph TB
    subgraph Frontend["🌐 Frontend (Amplify / S3)"]
        UI["Interfaz Web\nReact / JS Vanilla\n(Caso A o B)"]
    end

    subgraph APILayer["☁️ AWS API Gateway (REST API)"]
        APIGW["API Gateway\nHTTPS Endpoint\nAutorización + Throttling\nCORS configurado"]
        Routes["/api/items GET\n/api/items POST\n/api/items/{id} PUT\n/api/items/{id} DELETE"]
    end

    subgraph Compute["⚡ AWS Lambda"]
        Lambda["Función Lambda\nRuntime: Node.js / Python\nMemoria: 128-512 MB\nTimeout: 30s\nCold start: ~200ms"]
        Layer["Lambda Layer\n(dependencias compartidas)"]
    end

    subgraph Data["🗄️ AWS DynamoDB"]
        Table["Tabla DynamoDB\nPK: id (String)\nTTL: opcional\nBilling: On-Demand\n(pago por request)"]
    end

    subgraph IAM["🔐 IAM"]
        Role["Execution Role\nLambda → DynamoDB\n(PutItem, GetItem, Query, Delete)"]
    end

    UI -->|"fetch/axios\nHTTPS + CORS"| APIGW
    APIGW --> Routes
    Routes -->|"Invoke Lambda"| Lambda
    Lambda --- Layer
    Lambda <-->|"SDK: DynamoDB.put/get/query"| Table
    Lambda --- Role

    style APIGW fill:#FF9900,color:#fff
    style Lambda fill:#F0AD4E,color:#333
    style Table fill:#3498DB,color:#fff
    style Role fill:#E74C3C,color:#fff
```

---

## 📐 Diagrama 2: Ciclo de Vida de una Request (con Cold Start)

```mermaid
sequenceDiagram
    participant C as 🌐 Cliente
    participant APIGW as 📡 API Gateway
    participant Lambda as ⚡ Lambda
    participant DDB as 🗄️ DynamoDB

    C->>APIGW: POST /api/items {"name": "producto"}
    APIGW->>APIGW: Autenticación + Throttle check

    alt Cold Start (primera invocación o tras inactividad)
        APIGW->>Lambda: Invoke (cold start)
        Note over Lambda: Inicializando contenedor\nDescargando runtime (~200-500ms)
        Lambda->>Lambda: Handler ejecuta
    else Warm Start (invocaciones subsecuentes)
        APIGW->>Lambda: Invoke (warm)
        Note over Lambda: Contenedor reutilizado\n(~1-5ms overhead)
    end

    Lambda->>DDB: PutItem {id: uuid, name: "producto", ...}
    DDB-->>Lambda: 200 OK {ConsumedCapacity: 1 WCU}
    Lambda-->>APIGW: 200 {id: "xxxx", name: "producto"}
    APIGW-->>C: 200 OK + JSON

    Note over C,DDB: Tiempo total: 50-600ms (según cold/warm)
```

---

## 📐 Diagrama 3: Escalamiento Automático Lambda

```mermaid
graph LR
    subgraph Trafico["📈 Tráfico"]
        T0["0 requests\n(inactivo)"]
        T1["1 request"]
        T100["100 requests\nsimultáneas"]
        T1000["1,000 requests\nsimultáneas"]
    end

    subgraph Lambda["⚡ Lambda Concurrencia"]
        L0["0 instancias\n(destruidas por AWS)\n💰 Costo = $0"]
        L1["1 instancia\n(warm)"]
        L100["100 instancias\n(auto-scale)"]
        L1000["1,000 instancias\n(límite default de cuenta)"]
    end

    T0 --> L0
    T1 --> L1
    T100 --> L100
    T1000 --> L1000

    Note["💡 DynamoDB también escala automáticamente.\nBilling On-Demand: pagas por WCU/RCU usados,\nno por capacidad reservada."]

    style L0 fill:#95A5A6,color:#fff
    style L1 fill:#27AE60,color:#fff
    style L100 fill:#F39C12,color:#fff
    style L1000 fill:#E74C3C,color:#fff
    style Note fill:#EBF5FB,color:#333,stroke:#85C1E9
```

---

## 📐 Diagrama 4: AWS SAM — Definición de Infraestructura

```mermaid
graph TB
    subgraph SAM["📄 template.yaml (SAM)"]
        API["AWS::Serverless::Api\nStageName: prod\nCors: true"]
        Func["AWS::Serverless::Function\nHandler: index.handler\nRuntime: nodejs18.x\nEvents: ApiEvent"]
        DB["AWS::Serverless::SimpleTable\nor AWS::DynamoDB::Table\nBillingMode: PAY_PER_REQUEST"]
    end

    subgraph CLI["🔧 SAM CLI"]
        Build["sam build\n(empaqueta dependencias)"]
        Deploy["sam deploy\n--guided\n(sube a CloudFormation)"]
        Local["sam local start-api\n(test local sin AWS)"]
    end

    subgraph CF["☁️ CloudFormation Stack"]
        Stack["Stack: caso-d-serverless\nLambda + API GW + DynamoDB\nIAM Roles auto-generados"]
    end

    SAM --> Build
    Build --> Deploy
    Deploy --> Stack
    SAM -.->|"test local"| Local

    style Build fill:#F39C12,color:#fff
    style Deploy fill:#E74C3C,color:#fff
    style Stack fill:#FF9900,color:#fff
```

---

## 🔧 Componentes y Roles

| Componente | Servicio | Función | Costo |
|---|---|---|---|
| **API Gateway** | REST API | Endpoint HTTPS, routing, auth, throttling | Free Tier: 1M requests/mes |
| **Compute** | Lambda | Ejecuta lógica de negocio (stateless) | Free Tier: 1M invocaciones/mes |
| **Base de Datos** | DynamoDB | Persistencia NoSQL clave-valor | Free Tier: 25GB + 25 WCU/RCU |
| **IaC** | AWS SAM | Define Lambda + API + DDB en YAML | Gratis |
| **Deploy** | CloudFormation | Orquesta la creación de recursos desde SAM | Gratis |

---

## 💡 Cuándo Usar Serverless vs Contenedores

| Criterio | Serverless (Caso D) | Contenedores (Caso J/K) |
|---|---|---|
| **Latencia** | 50-600ms (cold start) | < 10ms (warm always) |
| **Costo bajo tráfico** | 💰 Muy bajo (pay per use) | 💸 Fijo aunque sin tráfico |
| **Estado** | Stateless obligatorio | Puede ser stateful |
| **Duración máxima** | 15 minutos | Sin límite |
| **Observabilidad** | CloudWatch Logs automático | Requiere setup |

---

## 🔗 Referencias

- [README del Caso D](../README.md)
- [Guía Paso a Paso AWS](../AWS_PASO_A_PASO.md)
- [Ver Demo](https://staging.d3oq987bpa7ls7.amplifyapp.com/)
