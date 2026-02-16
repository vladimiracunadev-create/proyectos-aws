# ☁️ Guía Paso a Paso: Caso L (FinOps & Governance)

Esta guía detalla cómo implementar la gobernanza financiera e identidades seguras en tu cuenta de AWS.

---

## 🪜 Fase 1: Control de Presupuesto (AWS Budgets)
... (anteriormente definido) ...

## 🪜 Fase 2: Identidad Segura (GitLab OIDC / Passwordless)
... (anteriormente definido) ...

## 🪜 Fase 3: Despliegue de la App de Monitoreo (Estrategia FinOps)
Para que el tablero sea una "App de Producción" pero con **Costo $0**:
1.  **Infraestructura (Terraform)**:
    - Definir un bucket **S3** configurado como `website`.
    - Configurar **CloudFront** como CDN para habilitar HTTPS de forma gratuita (AWS Certificate Manager).
2.  **Pipeline de Despliegue**:
    - GitLab CI sincronizará la carpeta `app/public/` hacia S3 cada vez que haya cambios en `main`.
    - **Resultado**: El Dashboard de Monitoreo tendrá su propia URL de AWS (`https://d123.cloudfront.net`) independiente de GitLab.

---

## 🪜 Fase 3: Gobernanza de IAM & SCP

1.  **Límite de Región**:
    - Aplica una política que deniegue cualquier acción fuera de tu región principal (ej: `us-east-1`), excepto en servicios globales como IAM o Route53.
2.  **Etiquetado Obligatorio (Tagging)**:
    - Implementa una regla que impida crear recursos si no llevan el tag `Project = Caso-L` y `Owner = Vladimir`.

---

## 🪜 Fase 4: Visualización Financiera (Dashboard Premium)

1.  **Hosting Estático**: Siguiendo los principios de FinOps (ahorro de costos), este dashboard se aloja como contenido estático en **S3 o GitLab Pages**. No requiere una instancia EC2 o EKS dedicada, lo que reduce el gasto a casi **$0 USD**.
2.  **Visualización**: Abre el archivo `app/public/index.html` para ver el diseño Glassmorphism con métricas proyectadas.

---

## 🧹 Limpieza
A diferencia de los casos anteriores, **estos recursos deben permanecer activos**. 
- Los presupuestos y el IAM OIDC no generan costos significativos y son tu red de seguridad para futuros proyectos.

---
_Misión: Mantener la nube bajo control total._
