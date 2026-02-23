# ☁️ AWS Paso a Paso: S3 + GitHub Actions (OIDC)

Esta guía explica cómo configurar el despliegue automatizado de este portafolio en un bucket de S3.

## 1. Configuración del Bucket S3

1. **Crear Bucket:** En la consola de S3, crea un bucket (ej. `mi-pagina-scrum-123`).
2. **Propiedades:** Habilita "Static website hosting" y configura `index.html` como documento de índice.
3. **Permisos:** 
   - Desactiva "Block all public access" (si vas a servirlo directamente desde S3).
   - Crea una **Bucket Policy** que permita `s3:GetObject` a todos (o usa CloudFront para mayor seguridad).

## 2. Configuración de Identidad (OIDC)

En lugar de usar Access Keys permanentes, usamos **GitHub OIDC**:

1. En AWS IAM, crea un **Identity Provider** de tipo "OpenID Connect".
   - Provider URL: `https://token.actions.githubusercontent.com`
   - Audience: `sts.amazonaws.com`
2. Crea un **Role de IAM** para GitHub Actions con una política de confianza que limite el acceso a tu repositorio y rama `main`.
3. Adjunta una política al rol que permita `s3:PutObject`, `s3:ListBucket` y `s3:DeleteObject` solo en el bucket específico.

## 3. Configuración en GitHub

Agrega los siguientes **Secrets** en tu repositorio:
- `AWS_ACCESS_KEY_ID`: (Opcional si usas OIDC completo, pero requerido por algunos workflows tradicionales).
- `AWS_SECRET_ACCESS_KEY`: (Igual que arriba).
- **Nota:** El flujo actual en este monorepo usa credenciales configuradas en secretos para la acción de sincronización.

## 4. El Workflow de Despliegue

El archivo `.github/workflows/despliegue.yml` realiza las siguientes tareas:
1. Checkout del código.
2. Configuración de credenciales de AWS.
3. Ejecución de `aws s3 sync ./aws-s3-scrum-mi-sitio-1 s3://TU-BUCKET --delete`.

## 5. Acceso

Tu portafolio estará disponible en la URL de endpoint de S3 (ej. `http://mi-pagina-scrum-123.s3-website.us-east-2.amazonaws.com`).
