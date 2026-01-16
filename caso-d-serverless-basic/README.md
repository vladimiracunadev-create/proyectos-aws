# caso-d-serverless-basic (Nivel 3) — Portafolio estático + Formulario Serverless

Este proyecto es un **demo real y pequeño** para aprender y demostrar un stack típico en AWS:

- **Frontend estático**: HTML/CSS/JS (publicado en **AWS Amplify Hosting**).
- **Backend serverless**: **API Gateway (HTTP API)** → **AWS Lambda** → **DynamoDB**.

> **Live Demo**: [👉 Ver Portafolio Interactivo](https://staging.d3oq987bpa7ls7.amplifyapp.com/)

La página principal incluye un **Formulario (Demo)** que, al enviar, **guarda el registro en DynamoDB**.

---

## Estructura

```
caso-d-serverless-basic/
  frontend/                 # tu portafolio (HTML/CSS/JS + PDFs)
    index.html
    styles.css
    app.js
    *.pdf
  backend/                  # SAM: API + Lambda + DynamoDB
    template.yaml
    src/
      app.py
  amplify.yml               # (opcional) para publicar solo /frontend en Amplify
  .gitignore
```

---

## 1) Deploy del Backend (API + Lambda + DynamoDB)

### Requisitos
- AWS CLI configurada (`aws configure`)
- AWS SAM CLI instalada (`sam --version`)

### Comandos

```bash
cd backend
sam build
sam deploy --guided
```

Al terminar, SAM/CloudFormation mostrará outputs. Copia el **ApiBaseUrl**, ejemplo:

```
ApiBaseUrl = https://xxxx.execute-api.sa-east-1.amazonaws.com
```

---

## 2) Conectar el Frontend al Backend (pegar URL del API)

Abre:

- `frontend/app.js`

Busca esta línea y pega tu URL real:

```js
const API_BASE = "Pega_aqui_tu_ApiBaseUrl";
```

Guarda los cambios.

---

## 3) Deploy del Frontend (Amplify)

Opción simple:
- En **AWS Amplify Hosting** publica la carpeta **`frontend/`**.

Este repo incluye un `amplify.yml` (opcional) que indica a Amplify que el artefacto está en `frontend/`.

---

## 4) Probar la demo

1. Abre tu sitio.
2. Menú superior → **Formulario (Demo)**.
3. Envía el formulario.
4. Revisa en AWS:
   - **DynamoDB → Tables → `portfolio_leads`**

---

## Notas importantes (para aprender bien)

- El frontend es **estático** (no “corre en servidor”): corre en el navegador.
- La parte “serverless” es el backend: **Lambda** sí ejecuta código en AWS, pero **sin administrar servidores**.
- Para mantener el demo ordenado, la tabla usa **TTL** para auto-borrar registros en 30 días.

### Seguridad (modo demo)
- CORS está en `*` para que funcione fácil.
- En producción, limita `AllowOrigins` al dominio real del sitio.

---

## Endpoints

- `POST /lead`

Body JSON esperado:

```json
{ "name": "...", "email": "...", "message": "..." }
```

