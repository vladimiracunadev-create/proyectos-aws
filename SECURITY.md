# 🔐 Security Policy

Gracias por ayudar a mantener este repositorio seguro.

---

## ✅ Supported Versions
Este repositorio es un monorepo de portafolio. Se considera “soportada” la rama:

- `main` (última versión)

La rama `dev` es para integración y pruebas.

---

## 🚨 Reporting a Vulnerability

Si encuentras una vulnerabilidad:

1. **Evita** abrir un issue público con detalles explotables.
2. Reporta de forma privada por uno de estos medios (elige el que usarás):
   - **GitHub Security Advisories** (recomendado si el repo lo permite)
   - Email: `TU_EMAIL_DE_SEGURIDAD@ejemplo.com` *(reemplazar)*

Incluye:
- Descripción clara del problema
- Pasos para reproducir
- Impacto estimado
- Prueba de concepto (si aplica) sin causar daño
- Recomendación/mitigación propuesta (si la tienes)

---

## ⏱️ Tiempos de respuesta (best effort)
- Confirmación de recepción: 48–72 horas
- Evaluación inicial: 7 días
- Fix/mitigación: según severidad y alcance

---

## 🔒 Buenas prácticas del repo

### Gestión de Secretos
- ❌ **NUNCA** commitear secretos (keys, tokens, credenciales AWS)
- ✅ Usar GitHub Secrets para CI/CD
- ✅ Usar AWS OIDC para autenticación sin credenciales de larga duración
- ✅ Consultar [killed.md](docs/killed.md) para prácticas prohibidas y alternativas

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

### Autenticación AWS con OIDC

**Configuración recomendada para GitHub Actions:**

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

El repositorio ejecuta automáticamente:
- **Secret scanning** con TruffleHog (GitHub Actions)
- **Dependency scanning** en Pull Requests
- **YAML/Markdown linting** en cada push

Ver: `.github/workflows/security-scan.yml`

### Permisos IAM Mínimos
- Aplicar principio de mínimo privilegio
- Usar roles específicos por entorno (dev/prod)
- Habilitar MFA para usuarios IAM
- Rotar credenciales regularmente (si se usan)

### Workflow de Cambios
- Todo cambio a `main` debe ser vía Pull Request
- PRs requieren revisión de código
- CI/CD debe pasar antes de merge
- Usar ramas protegidas en GitHub
