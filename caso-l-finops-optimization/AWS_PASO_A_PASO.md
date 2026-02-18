# ☁️ Guía de Ingeniería: Caso L (FinOps & Governance)

Esta guía detalla la implementación de la **Excelencia Operativa** mediante control de costos, seguridad de identidades "Passwordless" y gobernanza de infraestructura.

---

## 🪜 Fase 1: Control Financiero Proactivo (AWS Budgets)

1.  **Navegación**: En la consola de AWS, busca **Billing and Cost Management (Facturación y gestión de costos)**. En el menú lateral izquierdo, selecciona **Budgets (Presupuestos)**.
2.  **Creación**: Haz clic en el botón naranja **Create budget (Crear presupuesto)**.
3.  **Tipo**: Selecciona **Cost budget - Recommended (Presupuesto de costos - Recomendado)** y presiona **Next (Siguiente)**.
4.  **Detalles del Presupuesto**:
    - **Budget name (Nombre del presupuesto)**: `Vladimir-Monthly-Alert`.
    - **Period (Periodo)**: `Monthly` (Mensual).
    - **Budget effective date (Fecha efectiva)**: `Fixed date` (Fecha fija).
    - **Budget amount (Monto)**: Elige `Fixed` (Fijo) e ingresa `$5.00`. (Este es tu límite de seguridad).
5.  **Configuración de Alertas**:
    - Haz clic en **Add an alert threshold (Agregar umbral de alerta)**.
    - **Threshold (Umbral)**: `85%`.
    - **Trigger (Desencadenante)**: `Actual` (Real).
    - **Notification (Notificación)**: Ingresa tu correo electrónico personal.
    - Agrega una segunda alerta al `100%` con el Trigger en `Forecasted` (Proyectado).
6.  **Confirmación**: Revisa los detalles y haz clic en **Create budget (Crear presupuesto)**.

---

## 🪜 Fase 2: Identidad Zero-Trust (GitLab OIDC / Passwordless)

*Objetivo: Desplegar en AWS desde GitLab sin usar Access Keys permanentes.*

1.  **Configurar Proveedor de Identidad**:
    - Ve a **IAM (Gestión de acceso e identidades)** -> **Identity Providers (Proveedores de identidad)** -> **Add provider (Agregar proveedor)**.
    - **Provider type (Tipo de proveedor)**: `OpenID Connect`.
    - **Provider URL (URL del proveedor)**: `https://gitlab.com`. (Haz clic en **Get thumbprint (Obtener huella digital)**).
    - **Audience (Audiencia)**: `https://gitlab.com`.
2.  **Crear el Rol de Despliegue (Método Directo)**:
    - Ve a **IAM** -> **Roles (Roles)** -> **Create role (Crear rol)**.
    - **Trusted entity type (Tipo de entidad de confianza)**: Selecciona **Custom trust policy (Política de confianza personalizada)**.
    - **Código**: Borra lo que haya en el editor y pega el siguiente JSON completo:
    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": {
            "Federated": "arn:aws:iam::689978033715:oidc-provider/gitlab.com"
          },
          "Action": "sts:AssumeRoleWithWebIdentity",
          "Condition": {
            "StringEquals": {
              "gitlab.com:aud": "https://gitlab.com"
            },
            "StringLike": {
              "gitlab.com:sub": "project_path:vladimir.acuna.dev-group/proyectos-aws-gitlab:ref_type:branch:ref:main"
            }
          }
        }
      ]
    }
    ```
    - Haz clic en **Next (Siguiente)**.
3.  **Agregar Permisos (Paso 2 del Asistente)**:
    - En la pantalla "Add permissions", busca y selecciona políticas como `AmazonS3FullAccess` y `CloudFrontFullAccess` (para este caso de uso).
    - Haz clic en **Next (Siguiente)**.
4.  **Asignar Nombre y Crear (Paso 3 del Asistente)**:
    - **Role name (Nombre del rol)**: Escribe `GitLabDeployRole`. (¡Este es el campo obligatorio que te falta!).
    - Ve al final de la página y haz clic en **Create role (Crear rol)**.

> [!TIP]
> **¿Problemas con la consola? (Solución Rápida)**
> Si el asistente de AWS falla o se queda cargando, puedes crear el rol instantáneamente usando la terminal (CloudShell o local). Copia y pega este bloque completo:
>
> 1. Crea el archivo de confianza:
>    ```bash
>    echo '{ "Version": "2012-10-17", "Statement": [ { "Effect": "Allow", "Principal": { "Federated": "arn:aws:iam::689978033715:oidc-provider/gitlab.com" }, "Action": "sts:AssumeRoleWithWebIdentity", "Condition": { "StringEquals": { "gitlab.com:aud": "https://gitlab.com" }, "StringLike": { "gitlab.com:sub": "project_path:vladimir.acuna.dev-group/proyectos-aws-gitlab:ref_type:branch:ref:main" } } } ] }' > trust.json
>    ```
> 2. Crea el rol y adjunta permisos:
>    ```bash
>    aws iam create-role --role-name GitLabDeployRole --assume-role-policy-document file://trust.json
>    aws iam attach-role-policy --role-name GitLabDeployRole --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
>    aws iam attach-role-policy --role-name GitLabDeployRole --policy-arn arn:aws:iam::aws:policy/CloudFrontFullAccess
>    ```
4.  **Permisos**: Adjunta permisos de lectura/escritura limitados a S3 y CloudFront.

---

## 🪜 Fase 3: Gobernanza y Guardrails (IAM & Tagging)
    
1.  **Crear Política de Restricción de Región**:
    - Ve a **IAM** -> **Policies (Políticas)** -> **Create policy (Crear política)**.
    - Pestaña **JSON**. Borra todo y pega este código (Bloquea todo fuera de US East 1 y 2):
    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "DenyOutsideRegions",
                "Effect": "Deny",
                "NotAction": [
                    "cloudfront:*",
                    "iam:*",
                    "route53:*",
                    "support:*",
                    "budgets:*"
                ],
                "Resource": "*",
                "Condition": {
                    "StringNotEquals": {
                        "aws:RequestedRegion": [
                            "us-east-1",
                            "us-east-2"
                        ]
                    }
                }
            }
        ]
    }
    ```
    - **Next** -> Nombre: `DenyNonUSRegions` -> **Create policy**.

2.  **Crear Política de Etiquetado Obligatorio (Tagging)**:
    - Repite el proceso (**Create policy** -> **JSON**).
    - Pega este código (Exige tags `Project` y `FinOps` al crear recursos):
    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "RequireTags",
                "Effect": "Deny",
                "Action": [
                    "ec2:RunInstances",
                    "s3:CreateBucket"
                ],
                "Resource": "*",
                "Condition": {
                    "StringNotEquals": {
                        "aws:RequestTag/Project": "CloudPortfolio",
                        "aws:RequestTag/FinOps": "CaseL"
                    }
                }
            }
        ]
    }
    ```
    - **Next** -> Nombre: `EnforceTaggingPolicy` -> **Create policy**.

---

## 🪜 Fase 4: Configuración en GitLab CI/CD (El Puente)

*Para que GitLab pueda "hablar" con AWS sin contraseñas, configuraremos el proyecto con los datos exactos:*

1.  **Variables de Entorno (GitLab)**:
    - Ve a tu proyecto en GitLab.
    - En el menú izquierdo, ve a **Settings (Ajustes)** -> **CI/CD**.
    - Busca la sección **Variables** y haz clic en **Expand (Expandir)**.
    - Haz clic en **Add variable (Agregar variable)** para cada una de las siguientes (desmarca "Protect variable" si no estás en ramas protegidas, o asegúrate de estar en `main`):

    | Key (Clave) | Value (Valor) | Descripción |
    | :--- | :--- | :--- |
    | `AWS_ROLE_ARN` | `arn:aws:iam::689978033715:role/GitLabDeployRole` | El rol que creamos en la Fase 2. (Copia y pega este valor exacto). |
    | `AWS_REGION` | `us-east-2` | La región donde operamos (Ohio). |
    | `S3_BUCKET_CASE_L` | `finops-vladimir-portfolio-case-l` | Nombre único para tu bucket (puedes cambiarlo si ya existe). |

2.  **Configuración del Pipeline (`.gitlab-ci.yml`)**:
    - Abre el archivo `.gitlab-ci.yml` en la raíz de tu repositorio.
    - Agrega (o asegúrate de tener) este bloque para probar la conexión OIDC (puedes agregarlo al final o en la sección de deploy):

    ```yaml
    # Job de prueba para verificar que GitLab puede asumir el rol
    verify_oidc_connection:
      stage: deploy
      image: amazon/aws-cli:latest
      id_tokens:
        GITLAB_OIDC_TOKEN:
          aud: https://gitlab.com
      script:
        - echo "Iniciando autenticación OIDC..."
        - >
          export $(printf "AWS_ACCESS_KEY_ID=%s AWS_SECRET_ACCESS_KEY=%s AWS_SESSION_TOKEN=%s"
          $(aws sts assume-role-with-web-identity
          --role-arn ${AWS_ROLE_ARN}
          --role-session-name "GitLabRunner-${CI_PROJECT_ID}-${CI_PIPELINE_ID}"
          --web-identity-token ${GITLAB_OIDC_TOKEN}
          --duration-seconds 3600
          --query 'Credentials.[AccessKeyId,SecretAccessKey,SessionToken]'
          --output text))
        - aws sts get-caller-identity
        - echo "¡Conexión exitosa! Ahora somos el rol ${AWS_ROLE_ARN}"
    ```
    *(Nota: Este job imprimirá tu identidad de AWS en los logs del pipeline para confirmar que funciona).*

---

## 🪜 Fase 5: Infraestructura (S3 para Alojamiento Web)

*Crearemos el servidor web "serverless" usando comandos de AWS CLI (puedes ejecutarlos en tu terminal o en CloudShell).*

1.  **Definir Nombre del Bucket**:
    (Usa el mismo nombre que definiste en las variables de GitLab):
    ```bash
    export BUCKET_NAME="finops-vladimir-portfolio-case-l"
    export REGION="us-east-2"
    ```

2.  **Crear el Bucket**:
    ```bash
    aws s3 mb s3://$BUCKET_NAME --region $REGION
    ```

3.  **Configurar Acceso Público (Sitio Web Estático)**:
    *Para este caso de uso (Portfolio Free Tier), usaremos un bucket público estándar.*
    
    a. **Desactivar Bloqueo de Acceso Público**:
    ```bash
    aws s3api put-public-access-block --bucket $BUCKET_NAME --public-access-block-configuration "BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false"
    ```
    
    b. **Añadir Política de Lectura Pública**:
    Crea un archivo `policy.json` con este contenido (cambia `NOMBRE_DE_TU_BUCKET` por tu nombre real):
    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": "arn:aws:s3:::NOMBRE_DE_TU_BUCKET/*"
            }
        ]
    }
    ```
    Y aplícala:
    ```bash
    aws s3api put-bucket-policy --bucket $BUCKET_NAME --policy file://policy.json
    ```

4.  **Activar Alojamiento Web**:
    ```bash
    aws s3 website s3://$BUCKET_NAME --index-document index.html
    ```
    
    **¡Listo!** Tu sitio web estará disponible en:
    `http://finops-vladimir-portfolio-case-l.s3-website-us-east-2.amazonaws.com`

---

## 🪜 Fase 6: Automatización CI/CD (Pipeline Final)

Agrega este job final a tu `.gitlab-ci.yml`. Este job se encargará de subir tu aplicación cada vez que hagas un cambio.

*Copia y pega esto al final de `.gitlab-ci.yml`:*

```yaml
# --- Despliegue Final a Producción (Case L) ---
deploy_case_l_final:
  stage: deploy
  image: 
    name: amazon/aws-cli:latest
    entrypoint: [""]
  id_tokens:
    GITLAB_OIDC_TOKEN:
      aud: https://gitlab.com
  script:
    - echo "Autenticando con AWS OIDC..."
    - >
      export $(printf "AWS_ACCESS_KEY_ID=%s AWS_SECRET_ACCESS_KEY=%s AWS_SESSION_TOKEN=%s"
      $(aws sts assume-role-with-web-identity
      --role-arn ${AWS_ROLE_ARN}
      --role-session-name "GitLabDeploy-${CI_PIPELINE_ID}"
      --web-identity-token ${GITLAB_OIDC_TOKEN}
      --duration-seconds 3600
      --query 'Credentials.[AccessKeyId,SecretAccessKey,SessionToken]'
      --output text))
    - echo "Desplegando archivos a S3..."
    # Sincroniza la carpeta pública de tu app con el bucket S3
    - aws s3 sync caso-l-finops-optimization/app/public/ s3://${S3_BUCKET_CASE_L} --delete
    - echo "✅ Despliegue completado."
    - echo "🌍 Tu sitio web: http://${S3_BUCKET_CASE_L}.s3-website-${AWS_REGION}.amazonaws.com"
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
      changes:
        - caso-l-finops-optimization/**/*
    - if: '$CI_PIPELINE_SOURCE == "web"'
```

---

## 🧹 Nota de Seguridad y Limpieza
Estos recursos (Budgets y IAM Roles) **deben permanecer activos**. No generan costos y son el "cinturón de seguridad" de tu cuenta de AWS.

---
_Manual técnico diseñado para asegurar la madurez operativa del proyecto._
