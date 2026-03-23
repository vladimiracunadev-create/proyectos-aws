# Caso 06 — DynamoDB + Matrix Builds

![Estado](https://img.shields.io/badge/estado-📋%20Planificado-lightgrey?style=flat-square)
![Trimestre](https://img.shields.io/badge/trimestre-Q3%202026-blue?style=flat-square)
![AWS](https://img.shields.io/badge/AWS-DynamoDB%20·%20Lambda-FF9900?style=flat-square&logo=amazonaws&logoColor=white)
![Actions](https://img.shields.io/badge/GitHub_Actions-Matrix%20Strategy-2088FF?style=flat-square&logo=githubactions&logoColor=white)

---

## 🎯 Objetivo

Añadir persistencia real (DynamoDB) y demostrar **matrix strategy**:
el mismo código probado en múltiples runtimes y regiones en paralelo.

---

## 🔑 Lo que introduce

### En AWS

| Servicio | Para qué |
|:---|:---|
| **DynamoDB** | Base de datos NoSQL serverless (CRUD real desde Lambda) |
| **DynamoDB Streams** | Eventos de cambio para futuros casos event-driven |
| **IAM** | Política mínima necesaria para que Lambda acceda a DynamoDB |

### En GitHub Actions

| Capacidad nueva | Descripción |
|:---|:---|
| `strategy.matrix` | Define combinaciones: runtimes × regiones |
| `fail-fast: false` | Una celda que falla no cancela las demás |
| Matrix output en summary | Tabla de resultados por combinación en el workflow summary |

---

## 🏗️ Arquitectura proyectada

```mermaid
flowchart TB
    DEV[Dev Local\ngit push] --> GH[(GitHub)]

    GH --> MAT{Matrix Strategy\nfail-fast: false}

    MAT --> J1[python3.11\nus-east-1]
    MAT --> J2[python3.11\nus-east-2]
    MAT --> J3[python3.12\nus-east-1]
    MAT --> J4[python3.12\nus-east-2]

    J1 --> LAMBDA[Lambda\nCRUD handler]
    J2 --> LAMBDA
    J3 --> LAMBDA
    J4 --> LAMBDA
    LAMBDA <-->|GetItem - PutItem\nDeleteItem| DDB[DynamoDB\nSingle-table\nPK + SK]

    DDB -->|Streams| EVT[DynamoDB Streams\ncasos event-driven]
```

## 🔄 Matrix en acción (objetivo)

```yaml
strategy:
  fail-fast: false
  matrix:
    runtime: [python3.11, python3.12]
    region:  [us-east-1, us-east-2]

# Resultado: 4 jobs en paralelo
# python3.11 × us-east-1   ✅
# python3.11 × us-east-2   ✅
# python3.12 × us-east-1   ✅
# python3.12 × us-east-2   ✅
```

---

## 🗄️ Modelo de datos DynamoDB

```json
{
  "PK":        "USER#vladimir",
  "SK":        "PROJECT#caso-06",
  "title":     "DynamoDB Matrix Demo",
  "status":    "active",
  "createdAt": "2026-Q3"
}
```

---

## 📋 Implementación proyectada — pasos clave

> Guia detallada con comandos exactos, errores comunes y verificaciones: **[AWS_PASO_A_PASO.md](./AWS_PASO_A_PASO.md)**

1. **Crear tabla DynamoDB** → `On-demand` capacity mode · PK: `PK` (String) + SK: `SK` (String) · habilitar Streams
2. **Lambda con permisos mínimos** → IAM policy con solo `dynamodb:GetItem`, `dynamodb:PutItem`, `dynamodb:DeleteItem`, `dynamodb:Query` sobre esta tabla
3. **Definir la matrix en el workflow:**

   ```yaml
   strategy:
     fail-fast: false
     matrix:
       runtime: [python3.11, python3.12]
       region:  [us-east-1, us-east-2]
   ```

4. **`${{ matrix.runtime }}`** y **`${{ matrix.region }}`** como variables en el step de deploy
5. **Revisar el workflow summary** → GitHub muestra tabla de resultados por combinación
6. **Verificar DynamoDB** → AWS Console → `Explore items` → confirmar items escritos por la Lambda

> **Principio clave:** `fail-fast: false` es fundamental — una región fallida no cancela las pruebas en las demás.

---

## 📜 Certificaciones relevantes

![DVA-C02](https://img.shields.io/badge/DVA--C02-Development%2032%25-FF6B6B?style=flat-square)
![SAA-C03](https://img.shields.io/badge/SAA--C03-Resilient%20Arch%2026%25-4ECDC4?style=flat-square)

| Certificación | Temas que cubre este caso |
|:---|:---|
| **DVA-C02** | DynamoDB data modeling, partition keys, capacity modes, Streams |
| **SAA-C03** | DynamoDB vs RDS trade-offs, single-table design, global tables |
| **SOA-C02** | DynamoDB monitoring (CloudWatch), backup & point-in-time recovery |

---

## ⬅️ Anterior · Siguiente ➡️

| | Caso |
|:---|:---|
| ⬅️ Anterior | [Caso 05 — Lambda + API GW](../caso-05-lambda-api-gateway/README.md) |
| ➡️ Siguiente | [Caso 07 — Reusable Workflows](../caso-07-reusable-workflows/README.md) |
