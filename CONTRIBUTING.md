# Guía de Contribución

Este repositorio es un ecosistema de ingeniería progresivo. Para mantener
el estándar de calidad y seguridad, sigue estas directrices.

---

## Inicio rápido

```bash
git clone https://github.com/vladimiracunadev-create/proyectos-aws.git
cd proyectos-aws
git checkout dev

# Instalar pre-commit (auditoría local de secretos y calidad)
pip install pre-commit
pre-commit install

# Construir tooling y verificar
make tooling-build
make tooling-validate
```

Para configuración detallada: [docs/INSTALL.md](docs/INSTALL.md)

---

## Hub CLI

| Comando | Descripción |
|:---|:---|
| `.\hub.ps1 list-projects` | Lista todos los casos detectados |
| `.\hub.ps1 validate` | Ejecuta validaciones en Docker |
| `.\hub.ps1 help` | Ayuda completa |
| `./hub.sh list-projects` | Equivalente en Linux/macOS |

---

## Flujo de trabajo (Git Flow simplificado)

1. **Rama de trabajo:** Siempre sobre `dev`, nunca directo a `main`
2. **Validar localmente:** `.\hub.ps1 validate` antes de cada commit
3. **Commits descriptivos:** `feat: add lambda demo`, `fix: correct s3 path`, `docs: update cert coverage`
4. **Pull Request:** de `dev` → `main`. El PR template guía el checklist
5. **No push directo a `main`:** Protegida por CODEOWNERS

---

## Estándares de código

### Al añadir un caso nuevo

Cada caso nuevo (`caso-XX-nombre/`) debe incluir:

- [ ] `README.md` con badges de estado, trimestre, AWS, Actions y certificaciones
- [ ] Tabla de capacidades nuevas (AWS + GitHub Actions)
- [ ] Diagrama de flujo del objetivo
- [ ] Tabla de certificaciones relevantes (DVA-C02 / SAA-C03 / SOA-C02)
- [ ] Navegación anterior / siguiente entre casos
- [ ] Workflow en `.github/workflows/` si el caso tiene deploy

### Seguridad

- Nunca incluir secrets, credenciales ni API keys en el código
- El pre-commit hook bloqueará automáticamente si detecta patrones sensibles
- Usar OIDC desde el Caso 03 en adelante — no secrets estáticos
- Permisos IAM mínimos necesarios

### Documentación

- Actualizar `CHANGELOG.md` si es feature o fix significativo
- Actualizar `docs/CERT_COVERAGE.md` si el caso cubre nuevos dominios de certificación
- Actualizar `docs/FINOPS_COSTOS.md` con costo estimado del caso nuevo
- Actualizar `ROADMAP.md` marcando el caso como completado (`[x]`)

---

## Convenciones de commits

| Prefijo | Cuándo usarlo |
|:---|:---|
| `feat:` | Nuevo caso o nueva capacidad |
| `fix:` | Corrección de bug |
| `docs:` | Solo documentación |
| `chore:` | Mantenimiento (deps, configs) |
| `refactor:` | Cambio de estructura sin nueva funcionalidad |
| `security:` | Cambios de seguridad, IAM, OIDC |
| `ci:` | Cambios en workflows de GitHub Actions |

---

## Releases

Los releases se crean con tags semver. Al pushear `v*.*.*`,
el workflow `release.yml` crea automáticamente el GitHub Release.

```bash
git tag v5.0.0
git push origin v5.0.0
```

---

*Gracias por contribuir a que este portafolio siga siendo un ejemplo de excelencia técnica.*
