# ðŸ” Security Policy

Gracias por ayudar a mantener este repositorio seguro.

---

## âœ… Supported Versions

Este repositorio es un monorepo de portafolio. Se considera â€œsoportadaâ€ la rama:

- `main` (Ãºltima versiÃ³n)

La rama `dev` es para integraciÃ³n y pruebas.

---

## ðŸš¨ Reporting a Vulnerability

Si encuentras una vulnerabilidad:

1. **Evita** abrir un issue pÃºblico con detalles explotables.
2. Reporta de forma privada por uno de estos medios (elige el que usarÃ¡s):
   - **GitHub Security Advisories** (recomendado si el repo lo permite)
   - Email: `TU_EMAIL_DE_SEGURIDAD@ejemplo.com` *(reemplazar)*

Incluye:

- DescripciÃ³n clara del problema
- Pasos para reproducir
- Impacto estimado
- Prueba de concepto (si aplica) sin causar daÃ±o
- RecomendaciÃ³n/mitigaciÃ³n propuesta (si la tienes)

---

## â±ï¸ Tiempos de respuesta (best effort)

- ConfirmaciÃ³n de recepciÃ³n: 48â€“72 horas
- EvaluaciÃ³n inicial: 7 dÃ­as
- Fix/mitigaciÃ³n: segÃºn severidad y alcance

---

## ðŸ”’ Buenas prÃ¡cticas del repo

### GestiÃ³n de Secretos

- âŒ **NUNCA** commitear secretos (keys, tokens, credenciales AWS)
- âœ… Usar GitHub Secrets para CI/CD
- âœ… Usar AWS OIDC para autenticaciÃ³n sin credenciales de larga duraciÃ³n
- âœ… Consultar [killed.md](docs/killed.md) para prÃ¡cticas prohibidas y alternativas

### Pre-commit Hooks

Este repositorio usa `pre-commit` para prevenir commits inseguros:

```bash
# Instalar pre-commit hooks
pip install pre-commit
pre-commit install

# Ejecutar manualmente
pre-commit run --all-files
```

Los hooks incluyen:

- `detect-secrets`: Previene commit de secretos
- `check-yaml`: Valida sintaxis YAML
- `terraform_fmt`: Formatea archivos Terraform
- `detect-private-key`: Detecta claves privadas

### AutenticaciÃ³n AWS con OIDC

**ConfiguraciÃ³n recomendada para GitHub Actions:**

1. **En AWS IAM:**
   - Crear Identity Provider OIDC para GitHub
   - Crear rol con trust policy:

     ```json
     {
       "Version": "2012-10-17",
       "Statement": [{
         "Effect": "Allow",
         "Principal": {
           "Federated": "arn:aws:iam::ACCOUNT_ID:oidc-provider/token.actions.githubusercontent.com"
         },
         "Action": "sts:AssumeRoleWithWebIdentity",
         "Condition": {
           "StringEquals": {
             "token.actions.githubusercontent.com:sub": "repo:OWNER/REPO:ref:refs/heads/main"
           }
         }
       }]
     }
     ```

2. **En GitHub Actions:**

   ```yaml
   permissions:
     id-token: write
     contents: read

   - uses: aws-actions/configure-aws-credentials@v4
     with:
       role-to-assume: arn:aws:iam::ACCOUNT_ID:role/GitHubActionsRole
       aws-region: us-east-1
   ```

### Escaneo de Seguridad Automatizado

El repositorio ejecuta automÃ¡ticamente en cada push a `main`:

- **Secret scanning** con TruffleHog (GitHub Actions).
- **Detect Secrets** comparando con `.secrets.baseline` (UTF-8).
- **Dependency scanning** en Pull Requests (vulnerabilidades moderadas+).
- **Linter YAML/Markdown** para asegurar calidad de cÃ³digo.

> [!NOTE]
> Los escaneos de seguridad estÃ¡n configurados para reportar hallazgos sin bloquear el despliegue (`continue-on-error: true`), permitiendo visibilidad constante sin detener la agilidad de desarrollo.

Ver: `.github/workflows/security-scan.yml`

### Permisos IAM MÃ­nimos

- Aplicar principio de mÃ­nimo privilegio
- Usar roles especÃ­ficos por entorno (dev/prod)
- Habilitar MFA para usuarios IAM
- Rotar credenciales regularmente (si se usan)

### Workflow de Cambios

- Todo cambio a `main` debe ser vÃ­a Pull Request
- PRs requieren revisiÃ³n de cÃ³digo
- CI/CD debe pasar antes de merge
- Usar ramas protegidas en GitHub
