# Guía Paso a Paso AWS - Caso E

## 0. Definición de operativo

Para este repositorio, el Caso E se considera operativo cuando se cumplen estos puntos:

- `sam build` termina sin errores.
- `sam deploy` crea el stack en AWS.
- Responden correctamente los endpoints `POST /orders`, `GET /customers/{customerId}/orders`, `GET /orders/status/{status}` y `GET /products/{productId}/orders`.
- La landing en la raíz `/` permite explicar y probar la API.
- Se documenta la URL final y la tabla desplegada.

Estado actual validado el **2026-03-11**:

- `sam build` ejecutado con éxito.
- Stack desplegado: `caso-e-dynamodb-persistence`.
- Región: `us-east-2`.
- API Base URL: `https://gqqm27j47c.execute-api.us-east-2.amazonaws.com`.
- Tabla DynamoDB: `persistence_pro_orders`.

Este caso crea una API serverless para practicar **Amazon DynamoDB** con un enfoque real de modelado
NoSQL. La infraestructura se despliega con **AWS SAM** y la landing pública sirve como interfaz de
prueba para validar los patrones de acceso.

---

## 1. Requisitos previos

Necesitas tener instalado:

- AWS CLI configurado con una cuenta válida.
- AWS SAM CLI.
- Python 3.12 o compatible para pruebas locales.
- Docker, si quieres usar `sam local` de forma completa.

Verifica:

```bash
aws sts get-caller-identity
sam --version
python --version
```

---

## 2. Estructura que vas a desplegar

Dentro de `caso-e-dynamodb-persistence/backend/template.yaml` se crean:

- 1 tabla DynamoDB con `pk/sk`
- 2 GSIs (`gsi1`, `gsi2`)
- 1 HTTP API
- 1 Lambda
- 1 ruta raíz `/` que devuelve una landing HTML

La tabla usa `PAY_PER_REQUEST`, así que no necesitas estimar capacidad manual.

---

## 3. Compilar la aplicación

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
- `AWS Region`: `us-east-2`
- `Confirm changes before deploy`: `Y`
- `Allow SAM CLI IAM role creation`: `Y`
- `Disable rollback`: `N`
- `Save arguments to samconfig.toml`: `Y`

También puedes usar un despliegue no interactivo como el que se ejecutó en este caso:

```bash
sam deploy \
  --stack-name caso-e-dynamodb-persistence \
  --region us-east-2 \
  --resolve-s3 \
  --capabilities CAPABILITY_IAM \
  --no-confirm-changeset \
  --no-fail-on-empty-changeset
```

---

## 5. URL operativa resultante

Tras el despliegue validado, la salida real fue:

- **API Base URL**: `https://gqqm27j47c.execute-api.us-east-2.amazonaws.com`
- **Tabla**: `persistence_pro_orders`

La raíz `/` devuelve una página web que explica el caso y permite probar la API en vivo.

---

## 6. Probar la API en AWS

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

## 7. Probar en local con eventos de ejemplo

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

## 8. Conectar el frontend o usar la landing pública

Tienes dos formas de probar el caso:

1. Abrir `caso-e-dynamodb-persistence/frontend/index.html` y configurar la `API base URL`.
2. Abrir directamente `https://gqqm27j47c.execute-api.us-east-2.amazonaws.com/`.

La landing pública ya incluye:

- explicación del caso
- formulario de creación de órdenes
- consultas por cliente, estado y producto
- resultados resumidos y JSON completo

---

## 9. Cómo leer el modelo DynamoDB

La tabla guarda al menos dos tipos de items.

### Item de negocio `ORDER`

```text
PK      = CUSTOMER#cust-001
SK      = ORDER#2026-03-11T18:00:00Z#uuid
GSI1PK  = STATUS#PENDING
GSI1SK  = 2026-03-11T18:00:00Z#uuid
GSI2PK  = PRODUCT#prod-erp
GSI2SK  = 2026-03-11T18:00:00Z#uuid
```

### Item de auditoría `AUDIT`

```text
PK = ORDER#uuid
SK = EVENT#2026-03-11T18:00:00Z
```

Esto permite:

- agrupar órdenes por cliente
- buscar por estado
- buscar por producto
- mantener trazabilidad de eventos

---

## 10. Paso a paso en la consola AWS

Si quieres revisar visualmente lo desplegado:

1. Abre **CloudFormation** y entra al stack `caso-e-dynamodb-persistence`.
2. Revisa la pestaña **Resources** para ver tabla, API y Lambda.
3. En **Lambda**, abre la función `OrdersApiFunction`.
4. En **DynamoDB**, abre la tabla `persistence_pro_orders`.
5. Revisa la sección **Indexes** para confirmar `gsi1` y `gsi2`.
6. En **API Gateway**, valida las rutas `/`, `/orders`, `/customers/...`, `/orders/status/...` y `/products/...`.

---

## 11. Limpieza

Cuando termines el laboratorio:

```bash
sam delete --stack-name caso-e-dynamodb-persistence --region us-east-2
```

Esto elimina API Gateway, Lambda y DynamoDB.

---

## 12. Extensión recomendada

La evolución natural de este caso es:

- enviar eventos a SQS o EventBridge
- agregar actualización de estados con auditoría
- crear dashboards operativos para pedidos `PENDING` y `PAID`
- publicar métricas de negocio y observabilidad en el futuro Caso H

Eso conecta directamente con el ya validado **Caso G - Event Driven**.
