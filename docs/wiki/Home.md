# GitHub Actions Journey — Wiki

Documentación técnica del monorepo **proyectos-aws**: 11 casos progresivos que demuestran
GitHub Actions como plataforma de ingeniería sobre AWS.

> Repositorio complementario: [proyectos-aws-gitlab](https://gitlab.com/vladimir.acuna.dev-group/proyectos-aws-gitlab)
> — GitLab documenta el **qué** (servicios AWS). GitHub documenta el **cómo** (GitHub Actions).

---

## Estado actual

| Fase | Casos | Estado |
|:---|:---|:---:|
| Fundamentos | 01 Amplify, 02 S3+Actions | ✅ 2/2 completados |
| Seguridad de Identidad | 03 OIDC, 04 Environments | 🔜 Q2 2026 |
| Serverless & Testing | 05 Lambda, 06 DynamoDB+Matrix | 🔜 Q2-Q3 2026 |
| Plataforma GitHub | 07 Reusable, 08 Containers+GHCR | 🔜 Q3 2026 |
| Gobernanza | 09 FinOps, 10 Multi-región, 11 EKS | 🔜 Q4 2026 |

---

## Narrativa y casos

- [GitHub Actions Journey](https://github.com/vladimiracunadev-create/proyectos-aws/blob/main/GITHUB_ACTIONS_JOURNEY.md) — el viaje técnico completo (leer primero)
- [Casos Completados](https://github.com/vladimiracunadev-create/proyectos-aws/blob/main/docs/CASOS_COMPLETADOS.md) — validación y lecciones de los casos en producción
- [Roadmap](https://github.com/vladimiracunadev-create/proyectos-aws/blob/main/ROADMAP.md) — proyección de 11 casos con criterios de éxito
- [Caso 01: Amplify Hosting](https://github.com/vladimiracunadev-create/proyectos-aws/blob/main/caso-01-amplify-hosting/README.md)
- [Caso 02: S3 + GitHub Actions](https://github.com/vladimiracunadev-create/proyectos-aws/blob/main/caso-02-s3-github-actions/README.md)

---

## Ingeniería e Infraestructura

- [Arquitectura CI/CD](CI-CD-Architecture) — workflows explicados paso a paso
- [PWA Technical Deep Dive](https://github.com/vladimiracunadev-create/proyectos-aws/blob/main/docs/PWA_TECHNICAL_DEEP_DIVE.md) — Service Workers y estrategias de caché
- [CI/CD Engineering Deep Dive](https://github.com/vladimiracunadev-create/proyectos-aws/blob/main/docs/CI_CD_ENGINEERING_DEEP_DIVE.md) — OIDC, JWT, deploy inmutable
- [File Architecture](https://github.com/vladimiracunadev-create/proyectos-aws/blob/main/FILE_ARCHITECTURE.md) — anatomía del monorepo
- [System Specs](https://github.com/vladimiracunadev-create/proyectos-aws/blob/main/SYSTEM_SPECS.md) — hardware y software justificados
- [Tooling Guide](Tooling-Guide) — Docker, K8s, Hub CLI, Makefile

---

## Gobernanza

- [FinOps & Costos](https://github.com/vladimiracunadev-create/proyectos-aws/blob/main/docs/FINOPS_COSTOS.md) — desglose real de costos por caso
- [Cobertura de Certificaciones](https://github.com/vladimiracunadev-create/proyectos-aws/blob/main/docs/CERT_COVERAGE.md) — mapeo SAA-C03, DVA-C02, SOA-C02
- [Política de Seguridad](Security-Policy) — defensa en profundidad
- [Security Checklist](Security-Checklist) — auditoría por capas
- [Killed Practices](Killed-Practices) — lo que NO hacemos y por qué

---

## Para diferentes audiencias

- [Guía para Reclutadores](Recruiter-Guide) — valor de negocio, demos en vivo
- [Manual para Novatos](Manual-Novatos) — analogías y conceptos base de CI/CD y cloud
- [Setup de Entorno](https://github.com/vladimiracunadev-create/proyectos-aws/blob/main/ENVIRONMENT_SETUP.md) — guía para nuevos colaboradores
- [Troubleshooting](https://github.com/vladimiracunadev-create/proyectos-aws/blob/main/docs/TROUBLESHOOTING_GUIDE.md) — resolución de fallos comunes
- [Changelog](https://github.com/vladimiracunadev-create/proyectos-aws/blob/main/CHANGELOG.md) — historial de evolución
- [Glosario](https://github.com/vladimiracunadev-create/proyectos-aws/blob/main/GLOSSARY.md) — terminología técnica

---

## Flujo de trabajo

```
Local (rama dev)
  → pre-commit hooks (detect-secrets, YAML lint, Terraform fmt)
    → GitHub PR (dev → main)
      → security-scan.yml (TruffleHog, dependency-review, lint)
        → Merge a main
          → Amplify auto-deploy (caso-01)
          → despliegue.yml → S3 sync (caso-02)
          → wiki-sync.yml → esta Wiki
```

Todo cambio en `docs/wiki/` se sincroniza automáticamente con esta Wiki mediante `wiki-sync.yml`.
