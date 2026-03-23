# Arquitectura de CI/CD

El corazón operativo de este monorepo reside en su automatización. Contamos con tres workflows
principales que garantizan calidad, seguridad y entrega constante.

---

## 1. Pipeline de Despliegue (`despliegue.yml`)

Gestiona la sincronización del contenido estático con la nube.

- **Trigger:** Push a `main` con cambios en `caso-02-s3-github-actions/**`
- **Estrategia:**
  - `caso-02-s3-github-actions/`: Sincronización directa vía `aws s3 sync` con credenciales IAM
    _(migración a OIDC planificada en Caso 03)_
  - `caso-01-amplify-hosting/`: Delegación al Amplify Console — deploy automático por rama

---

## 2. Escaneo de Seguridad (`security-scan.yml`)

Nuestra "Guardia de Calidad" que protege la integridad del código.

| Componente | Herramienta | Qué detecta |
|:---|:---|:---|
| **Secret Scan** | TruffleHog | Secretos en el historial completo de Git |
| **Detect Secrets** | detect-secrets | Secretos en archivos actuales vs baseline |
| **Dependency Review** | actions/dependency-review-action | CVEs en dependencias nuevas (solo en PRs) |
| **Linters** | yamllint + markdownlint-cli | Calidad de YAML y Markdown |

---

## 3. Sincronización de Wiki (`wiki-sync.yml`)

Implementación de **"Documentation as Code"**.

- **Lógica:** Cualquier cambio en `docs/wiki/` dispara sincronización automática con la GitHub Wiki.
- **Beneficio:** La documentación nunca se desincroniza del estado actual del sistema.

---

## Stack Tecnológico de CI/CD

| Componente | Tecnología |
|:---|:---|
| **Runner** | `ubuntu-latest` |
| **Auth AWS** (actual) | Secrets estáticos (`AWS_ACCESS_KEY_ID`) |
| **Auth AWS** (Caso 03) | OIDC — `AssumeRoleWithWebIdentity` sin secrets |
| **Secret scanners** | TruffleHog + detect-secrets |
| **Dependency scanner** | GitHub Dependency Graph + actions/dependency-review |
| **Linters** | markdownlint-cli + yamllint |

---

## Flujo completo (estado actual)

```
Local (rama dev)
  └── pre-commit hooks (detect-secrets, yaml lint, terraform fmt)
      └── git push → GitHub
          ├── security-scan.yml (TruffleHog, lint, dependency review en PRs)
          ├── wiki-sync.yml (si cambia docs/wiki/)
          └── [merge a main]
              ├── despliegue.yml → aws s3 sync → caso-02 en S3
              └── Amplify Console → caso-01 (main + dev URLs)
```

---

> **Inmersión técnica:** Consulta [CI/CD Engineering Deep Dive](https://github.com/vladimiracunadev-create/proyectos-aws/blob/main/docs/CI_CD_ENGINEERING_DEEP_DIVE.md)
> para el análisis de bajo nivel de OIDC, JWT y deploy inmutable.
