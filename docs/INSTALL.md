# Guía de Instalación y Quick Start

Tres caminos para empezar según tu entorno. Elige el que aplique.

---

## Opción A — Solo leer el código (sin instalar nada)

Explora directamente en GitHub:

- [README principal](../README.md) — mapa de los 11 casos
- [GitHub Actions Journey](../GITHUB_ACTIONS_JOURNEY.md) — narrativa completa
- [Casos completados](CASOS_COMPLETADOS.md) — validación con checklists
- Demos en vivo:
  - [caso-01 main](https://main.d3r1wuymolxagh.amplifyapp.com/)
  - [caso-01 dev](https://dev.d20m8tc0banvg.amplifyapp.com/)
  - [caso-02 S3](https://mi-pagina-scrum-123.s3.us-east-2.amazonaws.com/index.html)

---

## Opción B — Desarrollo local (recomendado)

### Requisitos mínimos

| Herramienta | Versión mínima | Para qué |
|:---|:---:|:---|
| Git | 2.40+ | Control de versiones |
| Docker Desktop | 24+ | Tooling de validación |
| AWS CLI | 2.x | Interactuar con AWS |
| Python | 3.11+ | pre-commit hooks |
| PowerShell | 7+ | Hub CLI en Windows |

### Instalación paso a paso

```bash
# 1. Clonar
git clone https://github.com/vladimiracunadev-create/proyectos-aws.git
cd proyectos-aws

# 2. Instalar pre-commit (auditoría local de secretos y calidad)
pip install pre-commit
pre-commit install

# 3. Construir imagen de tooling (AWS CLI + Terraform + Checkov + linters)
make tooling-build

# 4. Verificar que todo funciona
make tooling-validate

# 5. Ver todos los comandos disponibles
make help
```

### Verificación rápida

```bash
# Validaciones de seguridad y calidad
make security-scan

# Listar proyectos detectados
./hub.sh list-projects        # Linux / macOS / WSL
.\hub.ps1 list-projects       # Windows PowerShell

# Ejecutar validaciones en Docker
./hub.sh validate
.\hub.ps1 validate
```

---

## Opción C — Demo Kubernetes (opcional)

Requiere [`kind`](https://kind.sigs.k8s.io/) instalado además de Docker.

```bash
# Crear cluster local + desplegar el tooling job
make k8s-demo

# Ver resultado
kubectl get pods -n proyectos-aws-tooling

# Limpiar
make k8s-clean
```

---

## Credenciales AWS (para casos con deploy real)

Los casos 02+ requieren acceso a AWS. Configura tus credenciales locales:

```bash
aws configure
# AWS Access Key ID: <tu key>
# AWS Secret Access Key: <tu secret>
# Default region: us-east-2
# Default output format: json
```

> **Nota de seguridad:** Las credenciales locales son solo para desarrollo.
> El CI/CD usa OIDC (a partir del Caso 03) — sin secrets almacenados en GitHub.

Para el Caso 02 actual, configura los secrets en tu fork:
`Settings → Secrets and variables → Actions → New repository secret`

| Secret | Valor |
|:---|:---|
| `AWS_ACCESS_KEY_ID` | Tu access key ID |
| `AWS_SECRET_ACCESS_KEY` | Tu secret access key |

---

## Estructura del repositorio

```
proyectos-aws/
├── caso-01-amplify-hosting/    # ✅ Amplify CD (en producción)
├── caso-02-s3-github-actions/  # ✅ S3 + Actions (en producción)
├── caso-03-cloudfront-oidc/    # 🔜 Q2 2026
├── caso-04 ... caso-11/        # 🔜 Q2-Q4 2026
├── .github/
│   ├── workflows/              # CI/CD pipelines
│   ├── ISSUE_TEMPLATE/         # Templates de issues
│   ├── pull_request_template.md
│   ├── CODEOWNERS
│   └── dependabot.yml
├── docs/                       # Documentación técnica
├── tooling/                    # Docker tooling image
├── k8s/                        # Kubernetes manifests (demo)
├── GITHUB_ACTIONS_JOURNEY.md   # Narrativa del viaje
├── ROADMAP.md                  # Proyección 11 casos
└── Makefile                    # Comandos estandarizados
```

---

## Próximos pasos

Una vez configurado el entorno:

1. Lee [GITHUB_ACTIONS_JOURNEY.md](../GITHUB_ACTIONS_JOURNEY.md) para entender el propósito de cada caso
2. Explora [caso-01-amplify-hosting/README.md](../caso-01-amplify-hosting/README.md)
3. Revisa [ROADMAP.md](../ROADMAP.md) para ver qué viene
4. Si encuentras un bug: [abre un issue](https://github.com/vladimiracunadev-create/proyectos-aws/issues/new/choose)
