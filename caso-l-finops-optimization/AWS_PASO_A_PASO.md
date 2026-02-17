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
2.  **Crear el Rol de Despliegue (Parte 1: Asistente)**:
    - Ve a **IAM** -> **Roles (Roles)** -> **Create role (Crear rol)**.
    - **Trusted entity type (Tipo de entidad de confianza)**: `Web identity` (Identidad web).
    - **Identity provider (Proveedor de identidad)**: Selecciona `https://gitlab.com`.
    - **Audience (Audiencia)**: Selecciona `https://gitlab.com`.
    - **Importante**: Haz clic en **Next (Siguiente)**, asigna los permisos necesarios (o sáltalo por ahora), ponle nombre al rol (ej: `GitLabDeployRole`) y haz clic en **Create role (Crear rol)**.
3.  **Configurar Restricción de Repositorio (Parte 2: Edición)**:
    - Busca y entra al rol que acabas de crear.
    - Ve a la pestaña **Trust relationships (Relaciones de confianza)**.
    - Haz clic en **Edit trust policy (Editar política de confianza)**.
    - Modifica el JSON para agregar la restricción `StringLike`. Tu JSON debe verse similar a esto (manteniendo la estructura existente):
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
4.  **Permisos**: Adjunta permisos de lectura/escritura limitados a S3 y CloudFront.

---

## 🪜 Fase 3: Gobernanza y Guardrails (IAM & Tagging)

1.  **Restricción de Región (Policy)**:
    - Crea una política que deniegue cualquier servicio fuera de `us-east-1` o `us-east-2`. Esto evita gastos accidentales en regiones costosas.
2.  **Política de Etiquetado Obligatorio**:
    - Configura una **IAM Policy (Política de IAM)** que requiera que todo recurso (S3, EC2, etc.) tenga el Tag: `Project: CloudPortfolio` y `FinOps: CaseL`. Sin estos tags, la creación falla.

---

## 🪜 Fase 5: Configuración en GitLab CI/CD (El Puente)

*Para que GitLab pueda "hablar" con AWS sin contraseñas, debemos configurar el proyecto:*

1.  **Variables de Entorno (GitLab)**:
    - Ve a **Settings (Ajustes)** -> **CI/CD** -> **Variables (Variables)**.
    - Agrega `AWS_ROLE_ARN`: El ARN del rol que creaste en la Fase 2 (ej: `arn:aws:iam::123:role/GitLabDeployRole`).
    - Agrega `AWS_REGION`: `us-east-1`.
2.  **Configuración del Pipeline (`.gitlab-ci.yml`)**:
    - Debes declarar el uso de **ID Tokens**. Este es el "pasaporte" que GitLab le presenta a AWS:
    ```yaml
    variables:
      # Este es el token OIDC que AWS validará
      ID_TOKEN: $[[ inputs.id_token ]] 

    deploy_job:
      id_tokens:
        GITLAB_OIDC_TOKEN:
          aud: https://gitlab.com
      script:
        - # Comandos para asumir el rol usando el TOKEN
    ```

---

## 🪜 Fase 6: Despliegue de Alta Disponibilidad a Costo Cero

1.  **Arquitectura**: La App de Monitoreo (`app/public/index.html`) se aloja en un **S3 Bucket** configurado para **Static Website Hosting (Alojamiento de sitios web estáticos)**.
2.  **Optimización CloudFront**:
    - Se crea una **CloudFront Distribution (Distribución de CloudFront)** apuntando al bucket.
    - Se habilita **HTTPS gratuito** y compresión **Brotli/Gzip** para velocidad máxima.
3.  **Costo**: Esta arquitectura entra 100% en el **AWS Free Tier**, costando **$0 USD** para un portafolio personal.

---

## 🪜 Fase 5: Automatización CI/CD (Pipeline Final)

1.  **Job de Despliegue**: GitLab CI asume el rol creado en la Fase 2 usando el token OIDC temporal.
2.  **Sincronización**: Se ejecuta `aws s3 sync caso-l-finops-optimization/app/public/ s3://tu-bucket --delete`.
3.  **Invalidación**: Se ejecuta `aws cloudfront create-invalidation` para refrescar el caché del dashboard.

---

## 🧹 Nota de Seguridad y Limpieza
Estos recursos (Budgets y IAM Roles) **deben permanecer activos**. No generan costos y son el "cinturón de seguridad" de tu cuenta de AWS.

---
_Manual técnico diseñado para asegurar la madurez operativa del proyecto._
