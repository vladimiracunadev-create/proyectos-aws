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

A medida que avanzas por las carpetas, la complejidad y el profesionalismo aumentan:

### 🐣 Caso A: AWS Amplify (Velocidad Total)
**Objetivo**: Despliegue en 5 minutos. AWS hace toda la "magia" (hosting, SSL, CDN) de forma automática.
*   **Ideal para**: Prototipos y Frontends rápidos.

### 🛠️ Caso B: GitLab CI + S3 (El Camino Artesanal)
**Objetivo**: Entender los cimientos. Tú configuras el "camión" (Pipeline) para que lleve los archivos al bucket.
*   **Aprendizaje**: Permisos IAM, Buckets y automatización manual.

### 🏗️ Caso C: Terraform (Infraestructura como Código)
**Objetivo**: Profesionalización profesional. Los servidores y redes se escriben en texto, no se clickean.
*   **Aprendizaje**: Remote State, CloudFront OAC y seguridad de red.

### ⚡ Caso D: Serverless Basic (Lógica Reactiva)
**Objetivo**: Añadir "cerebro" al portafolio. Formularios que guardan datos sin servidores encendidos 24/7.
*   **Stack**: Gateway + Lambda + DynamoDB.

### 🐳 Caso G: Dockerización (Microservicios)
**Objetivo**: Independencia total. Empaquetamos la app con todo su sistema operativo para que nunca falle por "problemas de entorno".

### ☸️ Caso K: Kubernetes en AWS (Orquestación EKS)
**Objetivo**: El nivel máximo. Kubernetes manejando flotas de contenedores directamente en la infraestructura de **AWS (EKS)**.
*   **Enfoque**: Alta disponibilidad, auto-recuperación y escalado masivo industrial.

---

## 🚀 ¿Cómo se conecta todo?

1.  **Haces un cambio** en tu PC (o en tu DevContainer).
2.  **Validación**: Corres `make lint` para que el "policía" revise el código.
3.  **Push**: Subes a GitLab.
4.  **Pipeline**: El robot de GitLab despierta, audita la seguridad con `tfsec` y despliega en AWS.

---
¿Listo para aprender? **¡Empieza explorando las carpetas y rompiendo cosas!** Es la mejor forma de dominar la nube. 🚀🦾
