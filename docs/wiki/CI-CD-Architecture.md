# 🏗️ Arquitectura de CI/CD

El corazón operativo de este monorepo reside en su automatización. Contamos con tres flujos de trabajo principales que garantizan la calidad, seguridad y entrega constante.

## 1. Pipeline de Despliegue (`despliegue.yml`)
Gestiona la sincronización del contenido estático con la nube.
- **Trigger:** Push a `main` o `dev`.
- **Estrategia:** 
  - Para `aws-s3-*`: Sincronización directa vía AWS SDK usando OIDC para autenticación.
  - Para `aws-amplify-*`: Delegación al Amplify Console para despliegues por rama con entornos aislados.

## 2. Escaneo de Seguridad (`security-scan.yml`)
Nuestra "Guardia de Calidad" que protege la integridad del código.
- **Componentes:**
  - **Secret Scan:** TruffleHog analiza el historial de Git buscando brechas.
  - **Detect Secrets:** Escaneo de archivos actuales comparando contra [.secrets.baseline](../../.secrets.baseline).
  - **Dependency Review:** Auditoría de vulnerabilidades en nuevas dependencias (CVEs).
  - **Linters:** `yamllint` y `markdownlint` aseguran que el código sea legible y profesional.

## 3. Sincronización de Wiki (`wiki-sync.yml`)
Implementación de **"Documentation as Code"**.
- **Lógica:** Cualquier cambio en la carpeta `docs/wiki/` dispara una sincronización automática con el repositorio de la GitHub Wiki.
- **Beneficio:** La documentación técnica nunca se desincroniza del estado actual del sistema.

---

## 🛠️ Stack Tecnológico de CI/CD
- **Runner:** `ubuntu-latest`
- **Auth:** OpenID Connect (OIDC) para AWS.
- **Scanners:** TruffleHog, detect-secrets, GitHub Dependency Graph.
- **Estilo:** Markdown-CLI, Yamllint.
