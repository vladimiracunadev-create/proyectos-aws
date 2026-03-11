# Guia Paso a Paso AWS - Caso E

## 0. Definicion de operativo

Para este repositorio, el Caso E solo debe marcarse como operativo cuando se cumplan estos puntos:

- `sam build` termina sin errores.
- `sam deploy --guided` crea el stack en AWS.
- Responden correctamente los endpoints `POST /orders`, `GET /customers/{customerId}/orders`, `GET /orders/status/{status}` y `GET /products/{productId}/orders`.
- El frontend apunta a la `ApiBaseUrl` real y devuelve respuestas validas.
- Se documenta la URL final o las evidencias del despliegue.

Este caso crea una API serverless para practicar **Amazon DynamoDB** con enfoque en modelado
NoSQL real. La infraestructura se despliega con **AWS SAM** y el frontend sirve como cliente
de prueba para validar los patrones de acceso.

---

## 1. Requisitos previos

Necesitas tener instalado:

- AWS CLI configurado con una cuenta valida.
- AWS SAM CLI.
- Python 3.12 o compatible para pruebas locales.

Verifica:

```bash
aws sts get-caller-identity
sam --version
```

---

## 2. Estructura que vas a desplegar

Dentro de `caso-e-dynamodb-persistence/backend/template.yaml` se crean:

- 1 tabla DynamoDB con `pk/sk`
- 2 GSIs (`gsi1`, `gsi2`)
- 1 HTTP API
- 1 Lambda

La tabla usa `PAY_PER_REQUEST`, asi que no debes estimar capacidad manual.

---

## 3. Compilar la aplicacion

```bash
cd caso-e-dynamodb-persistence/backend
sam build
```

Esto empaqueta la Lambda y valida la plantilla.

---

## 4. Desplegar por primera vez

```bash
sam deploy --guided
```

Valores recomendados:

- `Stack Name`: `caso-e-dynamodb-persistence`
- `AWS Region`: `us-east-1` o `us-east-2`
- `Confirm changes before deploy`: `Y`
- `Allow SAM CLI IAM role creation`: `Y`
- `Disable rollback`: `N`
- `Save arguments to samconfig.toml`: `Y`

Cuando termine, SAM mostrara la salida `ApiBaseUrl`.

---

## 5. Probar la API en AWS

### Crear una orden

```bash
curl -X POST "$API_BASE_URL/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "customerId": "cust-001",
    "customerName": "Acme SPA",
    "productId": "prod-erp",
    "productName": "ERP Suite",
    "total": 1499.99,
    "status": "PENDING"
  }'
```

### Consultar por cliente

```bash
curl "$API_BASE_URL/customers/cust-001/orders"
```

### Consultar por estado

```bash
curl "$API_BASE_URL/orders/status/PENDING"
```

### Consultar por producto

```bash
curl "$API_BASE_URL/products/prod-erp/orders"
```

---

## 6. Probar en local con eventos de ejemplo

Desde la carpeta `backend/`:

```bash
sam local invoke OrdersApiFunction --event events/create-order.json
sam local invoke OrdersApiFunction --event events/get-customer-orders.json
sam local invoke OrdersApiFunction --event events/get-orders-by-status.json
sam local invoke OrdersApiFunction --event events/get-product-orders.json
```

Si prefieres levantar la API completa localmente:

```bash
sam local start-api
```

Luego el frontend puede apuntar a `http://127.0.0.1:3000`.

---

## 7. Conectar el frontend

Abre `caso-e-dynamodb-persistence/frontend/index.html` en tu navegador o publicalo en Amplify/S3.

En el campo `API base URL`, pega una de estas opciones:

- URL de `sam local start-api`
- URL de `ApiBaseUrl` entregada por SAM en AWS

Flujo recomendado de prueba:

1. Crear una orden.
2. Consultar por cliente.
3. Consultar por estado.
4. Consultar por producto.

Asi validas que la misma escritura soporta varios accesos sin scans.

---

## 8. Como leer el modelo DynamoDB

La tabla guarda al menos dos tipos de items:

### Item de negocio `ORDER`

```text
PK      = CUSTOMER#cust-001
SK      = ORDER#2026-03-11T18:00:00Z#uuid
GSI1PK  = STATUS#PENDING
GSI1SK  = 2026-03-11T18:00:00Z#uuid
GSI2PK  = PRODUCT#prod-erp
GSI2SK  = 2026-03-11T18:00:00Z#uuid
```

### Item de auditoria `AUDIT`

```text
PK = ORDER#uuid
SK = EVENT#2026-03-11T18:00:00Z
```

Esto permite:

- agrupar ordenes por cliente
- buscar por estado
- buscar por producto
- mantener trazabilidad de eventos

---

## 9. Paso a paso en la consola AWS

Si quieres revisar visualmente lo desplegado:

1. Abre **CloudFormation** y entra al stack `caso-e-dynamodb-persistence`.
2. Revisa la pestaña **Resources** para ver tabla, API y Lambda.
3. En **Lambda**, abre la funcion `OrdersApiFunction`.
4. En **DynamoDB**, abre la tabla `persistence_pro_orders`.
5. Revisa la seccion **Indexes** para confirmar `gsi1` y `gsi2`.
6. En **API Gateway**, valida las rutas `/orders`, `/customers/...`, `/orders/status/...` y `/products/...`.

---

## 10. Limpieza

Cuando termines el laboratorio:

```bash
sam delete --stack-name caso-e-dynamodb-persistence
```

Esto elimina API Gateway, Lambda y DynamoDB.

---

## 11. Extension recomendada

La evolucion natural de este caso es:

- enviar eventos a SQS o EventBridge
- agregar actualizacion de estados con auditoria
- crear dashboards operativos para pedidos `PENDING` y `PAID`

Eso conecta directamente con el futuro **Caso G - Event Driven**.
