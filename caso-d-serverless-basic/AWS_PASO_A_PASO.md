# ☁️ Guía Paso a Paso: Serverless con AWS SAM (Caso D)

Este caso introduce **Backend Logic** usando tecnologías Serverless: API Gateway para recibir peticiones y Lambda para procesarlas, con persistencia en DynamoDB. Usamos **AWS SAM (Serverless Application Model)** para definir todo.

---

## 🛠️ 1. Prerrequisitos

1.  **AWS CLI** configurado.
2.  **AWS SAM CLI** instalado. (Verifica con `sam --version`).
3.  **Node.js** instalado (para construir las Lambdas).

---

## 🚀 2. Flujo de Trabajo (SAM CLI)

El archivo `template.yaml` en esta carpeta define toda tu infraestructura.

### Paso A: Construir (Build)
Prepara el código de tus funciones Lambda y dependencias.

```bash
cd caso-d-serverless-basic
sam build
```

### Paso B: Desplegar (Deploy)
Sube tu código y crea la infraestructura (API, Lambda, Tabla DynamoDB) en una sola operación guiada.

```bash
sam deploy --guided
```

Sigue las instrucciones en pantalla:
*   **Stack Name**: `caso-d-serverless`
*   **Region**: `us-east-2`
*   **Confirm changes before deploy**: `y`
*   **Allow SAM CLI IAM role creation**: `y`
*   **Deploy here**: `y`

---

## 👀 3. Verificación

Al finalizar, SAM te mostrará outputs, incluyendo la **API Gateway Endpoint URL**.

Ejemplo: `https://abcd123.execute-api.us-east-2.amazonaws.com/Prod/`

1.  Copia esa URL.
2.  Úsala en tu navegador o Postman.
3.  ¡Estás interactuando con una función Lambda real!

---

## 🧹 4. Limpieza

Para eliminar la pila completa de CloudFormation:

```bash
sam delete --stack-name caso-d-serverless
```
*(Confirma con `y`).*
