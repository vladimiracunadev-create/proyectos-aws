# 📘 Manual de Aprendizaje: La Guía del Novato

¡Bienvenido! 👋 Si estás aquí, es porque quieres entender qué hay "bajo el capó" de este proyecto. Piensa en este repositorio como un **Gimnasio de Arquitectura Cloud**. Cada carpeta es una máquina de ejercicios diferente que te prepara para retos reales en AWS.

---

## 🏗️ Los Fundamentos: ¿Qué estamos usando?

1.  **Git (La Máquina del Tiempo)**: Guarda el historial de todo para poder "volver al pasado" si rompemos algo.
2.  **GitLab (La Fábrica de Robots)**: No es solo donde vive el código; tiene robots (**CI/CD**) que automatizan el despliegue.
3.  **AWS (El Terreno en la Nube)**: Donde "viven" nuestras aplicaciones (S3, Lambda, CloudFront, EKS).
4.  **Makefile (El Control Remoto)**: Unifica comandos complejos bajo nombres cortos como `make deploy`.
5.  **Docker (La Oficina de Cristal)**: Permite que el proyecto funcione igual en cualquier máquina sin instalar nada.

---

## 🔬 Deep Dive: Análisis de los Casos

A medida que avanzas por las carpetas, la complejidad y el profesionalismo aumentan siguiendo este nuevo orden:

### 🐣 Caso A: AWS Amplify (Velocidad Total)
**Objetivo**: Despliegue en 5 minutos. AWS hace toda la "magia" (hosting, SSL, CDN) de forma automática. Ideal para frontends modernos.

### 🛠️ Caso B: GitLab CI + S3 (El Camino Artesanal)
**Objetivo**: Entender los cimientos. Tú configuras el "camión" (Pipeline) para que lleve los archivos al bucket. Aprendes sobre permisos IAM y sincronización.

### 🏗️ Caso C: Terraform (Infraestructura como Código)
**Objetivo**: Profesionalización Senior. Los servidores y redes se escriben en texto. Aprendes a compartir el "mapa" de la nube (Remote State) y proteger datos con CloudFront.

### ⚡ Caso D: Serverless Basic (Lógica Reactiva)
**Objetivo**: Añadir "cerebro" al sistema. Formularios que guardan datos usando Lambda y DynamoDB sin necesidad de servidores encendidos 24/7.

### 🟠 Casos E-I: Gestión Senior de Aplicaciones
- **E - Persistencia**: Modelado de datos profesional en DynamoDB.
- **F - Seguridad**: Autenticación con Cognito y protección WAF.
- **G - Eventos**: Arquitecturas asíncronas reactivas (EventBridge).
- **H - Observabilidad**: Encontrar fallos antes que el usuario (CloudWatch).
- **I - GenAI**: Integración de modelos de lenguaje (Bedrock).

### 🐳 Caso J: Dockerización (El Combo Industrial)
**Objetivo**: Independencia total. Aprendes el flujo **"Blueprint vs Factory"**:
*   **Docker (Blueprint)**: El plano de cómo se construye tu app.
*   **ECR (Almacén)**: Donde guardas tus apps terminadas.
*   **ECS (Director)**: Quien pone a funcionar tu app en **Fargate** (servidores invisibles). 
*   *Bonus:* Incluye un **Dashboard Premium** para ver los datos en vivo.

### ☸️ Caso K: Kubernetes en AWS (Orquestación EKS)
**Objetivo**: El nivel máximo. Kubernetes gestionando flotas de contenedores directamente en la infraestructura de AWS (Clusters Reales).
*   **Estado Final**: Despliegue validado con éxito.
*   **Nota**: El entorno se encuentra actualmente **Desactivado** para evitar altos costos de mantenimiento ($0.10/hora base), demostrando buenas prácticas de FinOps.

### 🟣 Caso L: FinOps (Optimización Financiera)
**Objetivo**: Excelencia operativa. Aprender a controlar los costos de la nube para que el proyecto sea sostenible y eficiente.

---

## 🚀 ¿Cómo se conecta todo?

1.  **Haces un cambio** en tu PC (o en tu DevContainer).
2.  **Validación local**: Corres `make lint` y `make tf-security`.
3.  **Push**: Subes a GitLab.
4.  **Pipeline**: El robot de GitLab despierta, audita la seguridad y despliega automáticamente en AWS.

---
¿Listo para aprender? **¡Empieza explorando las carpetas y rompiendo cosas!** Es la mejor forma de dominar el Cloud Computing. 🚀🦾
