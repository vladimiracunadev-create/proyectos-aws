# Caso E: Persistence Pro (Modelado NoSQL)

[![Nivel-4](https://img.shields.io/badge/Nivel-4_Datos-green?style=for-the-badge)]()
[![Status](https://img.shields.io/badge/Status-Proyectado-lightgrey?style=for-the-badge)]()

Este caso lleva el laboratorio serverless al siguiente nivel: una API sobre **Amazon DynamoDB**
diseñada desde los **patrones de acceso** y no desde las tablas relacionales. La implementación
demuestra **Single Table Design**, **GSI**, **transacciones** y consultas eficientes por cliente,
estado y producto.

---

## Estado real

Estado actual del repositorio:

- El scaffold del caso ya existe.
- La API, el template SAM, los eventos de prueba y el frontend demo ya están creados.
- La arquitectura Mermaid y la guía paso a paso ya están documentadas.
- Aún falta desplegar y validar en AWS para marcarlo como `COMPLETADO`.

Criterio para pasar a `COMPLETADO`:

1. Ejecutar `sam build` sin errores.
2. Ejecutar `sam deploy --guided`.
3. Probar los 4 endpoints en AWS.
4. Confirmar que el frontend consulta la API desplegada.
5. Guardar la URL real y evidencias del despliegue.

## Objetivo

Aprender a modelar persistencia NoSQL de forma senior:

- Diseñar una sola tabla para múltiples entidades.
- Escribir datos de negocio y auditoría en una transacción atómica.
- Resolver consultas frecuentes usando claves compuestas y GSIs.
- Exponer la persistencia mediante una API serverless con AWS SAM.

## Stack

- **Frontend**: HTML + CSS + JavaScript para probar escrituras y lecturas.
- **API**: API Gateway HTTP API.
- **Compute**: AWS Lambda en Python 3.12.
- **Persistencia**: DynamoDB con `pk/sk`, `gsi1` y `gsi2`.
- **IaC**: AWS SAM / CloudFormation.

## Patrones de acceso cubiertos

1. Crear una orden y registrar su evento de auditoría con una sola transacción.
2. Listar órdenes de un cliente.
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

## Ejecucion local orientativa

```bash
cd caso-e-dynamodb-persistence/backend
sam build
sam local start-api
```

Luego abre `caso-e-dynamodb-persistence/frontend/index.html` y configura `API_BASE_URL`
con la URL publicada por SAM local o por API Gateway.

## Lo que demuestra este caso

- Modelado orientado a consultas, no a joins.
- Separación entre clave primaria de escritura y claves secundarias de lectura.
- Uso de `TransactWriteItems` para garantizar consistencia entre entidades relacionadas.
- Trazabilidad básica con eventos de auditoría por orden.

---

## Enlaces relacionados

- [Arquitectura Mermaid](./docs/architecture.md)
- [Guia Paso a Paso AWS](./AWS_PASO_A_PASO.md)
- [Caso D - Base serverless previa](../caso-d-serverless-basic/README.md)
- [Arquitectura global](../docs/ARCHITECTURE.md)
