# ☁️ Guía Paso a Paso: Caso L (FinOps & Governance)

Esta guía detalla cómo implementar la gobernanza financiera e identidades seguras en tu cuenta de AWS.

---

## 🪜 Fase 1: Control de Presupuesto (AWS Budgets)

1.  **Crear el Budget**:
    - Ve a la consola de **AWS Billing and Cost Management** -> **Budgets**.
    - Botón **Create budget**.
    - Elige **Cost budget** (Recomendado).
2.  **Configuración**:
    - **Name**: `Vladimir-Monthly-Budget`.
    - **Amount**: `$5.00 USD` (Umbral de seguridad para laboratorios).
    - **Alerts**: Configura una alerta al **85%** de uso real y otra al **100%** de uso proyectado.
3.  **Canal de Notificación**:
    - Ingresa tu correo electrónico para recibir alertas SNS inmediatas.

---

## 🪜 Fase 2: Identidad Segura (GitLab OIDC)

*Eliminaremos la necesidad de usar `AWS_ACCESS_KEY_ID` y `AWS_SECRET_ACCESS_KEY`.*

1.  **Identity Provider**:
    - Ve a **IAM** -> **Identity Providers** -> **Add provider**.
    - **Provider type**: `OpenID Connect`.
    - **Provider URL**: `https://gitlab.com`.
    - **Audience**: `https://gitlab.com`.
2.  **Crear Rol de Confianza**:
    - Crea un rol con una política de confianza que permita a GitLab asumir el rol basándose en tu `project_path`.
    - Adjunta solo los permisos necesarios (Least Privilege).

---

## 🪜 Fase 3: Gobernanza de IAM & SCP

1.  **Límite de Región**:
    - Aplica una política que deniegue cualquier acción fuera de tu región principal (ej: `us-east-1`), excepto en servicios globales como IAM o Route53.
2.  **Etiquetado Obligatorio (Tagging)**:
    - Implementa una regla que impida crear recursos si no llevan el tag `Project = Caso-L` y `Owner = Vladimir`.

---

## 🪜 Fase 4: Visualización Financiera

1.  **Cost Explorer**:
    - Habilita Cost Explorer para ver gráficos históricos.
    - Crea un reporte guardado filtrado por los tags definidos en la Fase 3.

---

## 🧹 Limpieza
A diferencia de los casos anteriores, **estos recursos deben permanecer activos**. 
- Los presupuestos y el IAM OIDC no generan costos significativos y son tu red de seguridad para futuros proyectos.

---
_Misión: Mantener la nube bajo control total._
