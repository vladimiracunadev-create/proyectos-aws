# ðŸ—ï¸ Arquitectura de CI/CD

El corazÃ³n operativo de este monorepo reside en su automatizaciÃ³n. Contamos con tres flujos de trabajo principales que garantizan la calidad, seguridad y entrega constante.

## 1. Pipeline de Despliegue (`despliegue.yml`)
Gestiona la sincronizaciÃ³n del contenido estÃ¡tico con la nube.
- **Trigger:** Push a `main` o `dev`.
- **Estrategia:**
  - Para `aws-s3-*`: SincronizaciÃ³n directa vÃ­a AWS SDK usando OIDC para autenticaciÃ³n.
  - Para `aws-amplify-*`: DelegaciÃ³n al Amplify Console para despliegues por rama con entornos aislados.

## 2. Escaneo de Seguridad (`security-scan.yml`)
Nuestra "Guardia de Calidad" que protege la integridad del cÃ³digo.
- **Componentes:**
  - **Secret Scan:** TruffleHog analiza el historial de Git buscando brechas.
  - **Detect Secrets:** Escaneo de archivos actuales comparando contra [.secrets.baseline](../../.secrets.baseline).
  - **Dependency Review:** AuditorÃ­a de vulnerabilidades en nuevas dependencias (CVEs).
  - **Linters:** `yamllint` y `markdownlint` aseguran que el cÃ³digo sea legible y profesional.

## 3. SincronizaciÃ³n de Wiki (`wiki-sync.yml`)
ImplementaciÃ³n de **"Documentation as Code"**.
- **LÃ³gica:** Cualquier cambio en la carpeta `docs/wiki/` dispara una sincronizaciÃ³n automÃ¡tica con el repositorio de la GitHub Wiki.
- **Beneficio:** La documentaciÃ³n tÃ©cnica nunca se desincroniza del estado actual del sistema.

---

## ðŸ› ï¸ Stack TecnolÃ³gico de CI/CD
- **Runner:** `ubuntu-latest`
- **Auth:** OpenID Connect (OIDC) para AWS.
- **Scanners:** TruffleHog, detect-secrets, GitHub Dependency Graph.
- **Estilo:** Markdown-CLI, Yamllint.
