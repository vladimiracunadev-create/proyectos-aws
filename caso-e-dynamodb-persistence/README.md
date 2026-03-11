# Caso E: Persistence Pro (Modelado NoSQL)

[![Nivel-4](https://img.shields.io/badge/Nivel-4_Datos-green?style=for-the-badge)]()
[![Status](https://img.shields.io/badge/Status-Deployed-success?style=for-the-badge)]()

Este caso profundiza en el diseño de persistencia con **Amazon DynamoDB** usando un enfoque
orientado a **patrones de acceso**. La solución implementa una API serverless con
**API Gateway + Lambda + DynamoDB**, aplica **Single Table Design**, define **GSIs** para
consultas eficientes y registra eventos de auditoría con una escritura transaccional.

---

## Estado real

Estado actual del repositorio y de AWS:

- El scaffold del caso ya existe dentro del monorepo.
- El backend está implementado con AWS SAM y Python 3.12.
- El stack fue desplegado y validado en AWS el **11 de marzo de 2026**.
- La URL base operativa es `https://gqqm27j47c.execute-api.us-east-2.amazonaws.com`.
- La tabla desplegada es `persistence_pro_orders`.
- La raíz `/` expone una landing interactiva para probar la API en vivo.

Validación completada:

1. `sam build` ejecutado con éxito.
2. Stack `caso-e-dynamodb-persistence` desplegado en `us-east-2`.
3. Validados los endpoints de escritura y consulta.
4. Confirmado el acceso desde la landing pública de la API.
5. Confirmada la persistencia real en DynamoDB.

## Objetivo

Demostrar un nivel senior de modelado NoSQL:

- Diseñar una tabla única para varias entidades relacionadas.
- Escribir datos de negocio y auditoría en una sola transacción.
- Resolver consultas por cliente, estado y producto sin scans completos.
- Exponer la persistencia a través de una API serverless clara y reproducible.

## Stack

- **Frontend**: landing HTML servida desde la raíz de la API para explicar y probar el caso.
- **API**: API Gateway HTTP API.
- **Compute**: AWS Lambda en Python 3.12.
- **Persistencia**: DynamoDB con `pk/sk`, `gsi1` y `gsi2`.
- **IaC**: AWS SAM / CloudFormation.

## Endpoint desplegado

- **API Base URL**: `https://gqqm27j47c.execute-api.us-east-2.amazonaws.com`
- **Stack**: `caso-e-dynamodb-persistence`
- **Región**: `us-east-2`
- **Tabla**: `persistence_pro_orders`

## Patrones de acceso cubiertos

1. Crear una orden y registrar su evento de auditoría con una sola transacción.
2. Listar órdenes de un cliente usando la clave primaria.
3. Consultar órdenes por estado usando `GSI1`.
4. Consultar órdenes por producto usando `GSI2`.

## Estructura del caso

```text
caso-e-dynamodb-persistence/
|- README.md
|- AWS_PASO_A_PASO.md
|- amplify.yml
|- backend/
|  |- template.yaml
|  |- events/
|  |  |- create-order.json
|  |  |- get-customer-orders.json
|  |  |- get-orders-by-status.json
|  |  |- get-product-orders.json
|  |- src/
|     |- app.py
|- docs/
|  |- architecture.md
|- frontend/
   |- index.html
   |- app.js
   |- styles.css
```

## Ejecución local orientativa

```bash
cd caso-e-dynamodb-persistence/backend
sam build
sam local start-api
```

Luego abre `caso-e-dynamodb-persistence/frontend/index.html` o usa la landing desplegada en AWS.

## Lo que demuestra este caso

- Modelado orientado a consultas, no a joins relacionales.
- Separación entre clave primaria de escritura y claves secundarias de lectura.
- Uso de `TransactWriteItems` para consistencia entre entidades relacionadas.
- Trazabilidad básica con eventos de auditoría por orden.
- Una experiencia más clara para demostrar la API desde la propia URL pública.

---

## Enlaces relacionados

- [Arquitectura Mermaid](./docs/architecture.md)
- [Guía Paso a Paso AWS](./AWS_PASO_A_PASO.md)
- [Caso D - Base serverless previa](../caso-d-serverless-basic/README.md)
- [Arquitectura global](../docs/ARCHITECTURE.md)