# âŒ KILLED: PrÃ¡cticas NO Permitidas en este Repositorio

Este documento especifica explÃ­citamente las prÃ¡cticas de seguridad que **NO estÃ¡n permitidas** en este repositorio y proporciona alternativas seguras.

---

## ðŸš« Prohibiciones Absolutas

### âŒ 1. Credenciales AWS en el Repositorio

**NO PERMITIDO:**

- Archivos `.aws/credentials`
- Variables `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` hardcodeadas
- Archivos `.env` con credenciales AWS
- Claves IAM en cÃ³digo fuente
- Tokens de sesiÃ³n en commits

**RAZÃ“N:** Las credenciales comprometidas pueden resultar en:

- Acceso no autorizado a recursos AWS
- Costos inesperados por uso malicioso
- Violaciones de datos
- Compromiso de la cuenta AWS

---

### âŒ 2. Archivos de Estado de Terraform (.tfstate)

**NO PERMITIDO:**

- `*.tfstate`
- `*.tfstate.backup`
- Cualquier archivo de estado de Terraform en Git

**RAZÃ“N:**

- Los archivos `.tfstate` contienen informaciÃ³n sensible (IPs, IDs de recursos, outputs)
- Pueden contener secretos en texto plano
- Son archivos grandes que no deben versionarse

**ALTERNATIVA:**

- Usar backend remoto (S3 + DynamoDB para locking)
- Configurar `.gitignore` apropiadamente (âœ… ya configurado)

---

### âŒ 3. Secretos Hardcodeados

**NO PERMITIDO:**

- API keys en cÃ³digo
- Passwords en archivos de configuraciÃ³n
- Tokens de acceso en scripts
- Certificados privados (`.pem`, `.key`, `.p12`)

**RAZÃ“N:**

- ExposiciÃ³n pÃºblica en GitHub
- DifÃ­cil rotaciÃ³n de secretos
- ViolaciÃ³n de principios de seguridad

---

### âŒ 4. EjecuciÃ³n como Root en Contenedores

**NO PERMITIDO:**

- Contenedores Docker que corren como `root`
- ImÃ¡genes sin `USER` no-root especificado
- Pods de Kubernetes sin `securityContext`

**RAZÃ“N:**

- Principio de mÃ­nimo privilegio
- ReducciÃ³n de superficie de ataque
- PrevenciÃ³n de escalaciÃ³n de privilegios

**ALTERNATIVA:**

- âœ… Usar `USER` no-root en Dockerfile (ver `tooling/Dockerfile.tooling`)
- âœ… Configurar `securityContext` en Kubernetes (ver `k8s/tooling-job/job.yaml`)

---

## âœ… PrÃ¡cticas Recomendadas (Alternativas Seguras)

### 1. AutenticaciÃ³n con OIDC (OpenID Connect)

**Para GitHub Actions â†’ AWS:**

```yaml
# .github/workflows/deploy.yml
permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsRole
          aws-region: us-east-1
```

**Ventajas:**

- âœ… Sin credenciales de larga duraciÃ³n
- âœ… Tokens temporales automÃ¡ticos
- âœ… AuditorÃ­a completa en CloudTrail
- âœ… Permisos granulares por repositorio/rama

**ConfiguraciÃ³n en AWS:**

1. Crear Identity Provider OIDC en IAM
2. Crear rol IAM con trust policy para GitHub
3. Asignar permisos mÃ­nimos necesarios

---

### 2. GitHub Secrets para Variables Sensibles

**Para valores que no pueden ser pÃºblicos:**

```yaml
# .github/workflows/example.yml
env:
  API_KEY: ${{ secrets.API_KEY }}
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

**ConfiguraciÃ³n:**

1. Ir a Settings â†’ Secrets and variables â†’ Actions
2. Agregar secrets necesarios
3. Referenciar con `${{ secrets.SECRET_NAME }}`

---

### 3. AWS Systems Manager Parameter Store / Secrets Manager

**Para secretos en runtime:**

```bash
# Obtener secreto en tiempo de ejecuciÃ³n
aws ssm get-parameter --name /app/database/password --with-decryption
aws secretsmanager get-secret-value --secret-id prod/db/password
```

**Ventajas:**

- âœ… RotaciÃ³n automÃ¡tica de secretos
- âœ… EncriptaciÃ³n en reposo (KMS)
- âœ… AuditorÃ­a de accesos
- âœ… Versionado de secretos

---

### 4. Variables de Entorno (Localmente)

**Para desarrollo local:**

```bash
# .env (NUNCA commitear)
AWS_PROFILE=dev-profile
AWS_REGION=us-east-1

# Usar AWS CLI con profiles
aws configure --profile dev-profile
export AWS_PROFILE=dev-profile
```

**Asegurar con `.gitignore`:**

```gitignore
.env
.env.*
!.env.example
```

---

## ðŸ”’ Checklist de Seguridad para Contribuidores

Antes de hacer commit, verifica:

- [ ] No hay credenciales AWS en el cÃ³digo
- [ ] No hay archivos `.tfstate` en el commit
- [ ] No hay secretos hardcodeados
- [ ] Los archivos `.env` estÃ¡n en `.gitignore`
- [ ] Pre-commit hooks estÃ¡n instalados (`pre-commit install`)
- [ ] `detect-secrets` no reporta alertas
- [ ] Contenedores Docker usan usuario no-root
- [ ] Manifiestos K8s tienen `securityContext`

---

## ðŸ“š Referencias

- [AWS Security Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [GitHub OIDC with AWS](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services)
- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [Terraform Backend Configuration](https://developer.hashicorp.com/terraform/language/settings/backends/s3)

---

## ðŸš¨ Reporte de Incidentes

Si encuentras credenciales expuestas en este repositorio:

1. **NO** las uses ni las compartas
2. Reporta inmediatamente a travÃ©s de GitHub Security Advisories
3. Contacta al maintainer del repositorio
4. Las credenciales serÃ¡n rotadas inmediatamente

---

**Ãšltima actualizaciÃ³n:** 2026-02-04
**Mantenido por:** Equipo de Seguridad - proyectos-aws
