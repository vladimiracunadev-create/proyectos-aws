# ☁️ Guía de Ingeniería: Caso L (FinOps & Governance)

Esta guía detalla la implementación de la **Excelencia Operativa** mediante control de costos, seguridad de identidades "Passwordless" y gobernanza de infraestructura.

---

## 🪜 Fase 1: Control Financiero Proactivo (AWS Budgets)

1.  **Navegación**: En la consola de AWS, busca **Billing and Cost Management**. En el menú lateral izquierdo, selecciona **Budgets**.
2.  **Creación**: Haz clic en el botón naranja **Create budget**.
3.  **Tipo**: Selecciona **Cost budget - Recommended** y presiona **Next**.
4.  **Detalles del Presupuesto**:
    - **Budget name**: `Vladimir-Monthly-Alert`.
    - **Period**: `Monthly` (Mensual).
    - **Budget effective date**: `Fixed date`.
    - **Budget amount**: Elige `Fixed` e ingresa `$5.00`. (Este es tu límite de seguridad).
5.  **Configuración de Alertas**:
    - Haz clic en **Add an alert threshold**.
    - **Threshold**: `85%`.
    - **Trigger**: `Actual` (Real).
    - **Notification**: Ingresa tu correo electrónico personal.
    - Agrega una segunda alerta al `100%` con el Trigger en `Forecasted` (Proyectado).
6.  **Confirmación**: Revisa los detalles y haz clic en **Create budget**.

---

## 🪜 Fase 2: Identidad Zero-Trust (GitLab OIDC / Passwordless)

*Objetivo: Desplegar en AWS desde GitLab sin usar Access Keys permanentes.*

1.  **Configurar Proveedor de Identidad**:
    - Ve a **IAM** -> **Identity Providers** -> **Add provider**.
    - **Provider type**: `OpenID Connect`.
    - **Provider URL**: `https://gitlab.com`. (Haz clic en **Get thumbprint**).
    - **Audience**: `https://gitlab.com`.
2.  **Crear el Rol de Despliegue**:
    - Ve a **IAM** -> **Roles** -> **Create role**.
    - **Trusted entity type**: `Web identity`.
    - **Identity provider**: Selecciona `https://gitlab.com`.
    - **Audience**: Selecciona `https://gitlab.com`.
3.  **Políticas de Confianza (Trust Relationship)**:
    - Edita la política para restringir el acceso solo a tu repositorio específico:
    ```json
    "StringLike": {
      "gitlab.com:sub": "project_path:vladimir.acuna.dev-group/proyectos-aws-gitlab:ref_type:branch:ref:main"
    }
    ```
4.  **Permisos**: Adjunta permisos de lectura/escritura limitados a S3 y CloudFront.

---

## 🪜 Fase 3: Gobernanza y Guardrails (IAM & Tagging)

1.  **Restricción de Región (Policy)**:
    - Crea una política que deniegue cualquier servicio fuera de `us-east-1` o `us-east-2`. Esto evita gastos accidentales en regiones costosas.
2.  **Política de Etiquetado Obligatorio**:
    - Configura una **IAM Policy** que requiera que todo recurso (S3, EC2, etc.) tenga el Tag: `Project: CloudPortfolio` y `FinOps: CaseL`. Sin estos tags, la creación falla.

---

## 🪜 Fase 4: Despliegue de Alta Disponibilidad a Costo Cero

1.  **Arquitectura**: La App de Monitoreo (`app/public/index.html`) se aloja en un **S3 Bucket** configurado para Static Website Hosting.
2.  **Optimización CloudFront**:
    - Se crea una **CloudFront Distribution** apuntando al bucket.
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
