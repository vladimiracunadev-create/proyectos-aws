# 🚀 Quick Reference - proyectos-aws Tooling

Guía rápida de comandos para el sistema de tooling.

---

## 📦 Instalación Inicial

```bash
# 1. Instalar pre-commit (opcional pero recomendado)
pip install pre-commit
pre-commit install

# 2. Construir imagen de tooling
make tooling-build
```

---

## 🛠️ Comandos Make

```bash
make help                  # Muestra ayuda con todos los comandos
make tooling-build         # Construye imagen Docker de tooling
make tooling-validate      # Ejecuta validaciones (terraform, yaml, markdown)
make tooling-shell         # Abre shell interactivo en contenedor
make security-scan         # Ejecuta escaneo de secretos con pre-commit
make k8s-demo             # Despliega job de validación en kind
make k8s-clean            # Limpia recursos de Kubernetes
make k8s-delete-cluster   # Elimina cluster kind
```

---

## 🎯 Hub CLI

### Linux/Mac

```bash
./hub.sh list-projects     # Lista proyectos aws-*
./hub.sh validate          # Ejecuta validaciones
./hub.sh help              # Muestra ayuda
```

### Windows PowerShell

```powershell
.\hub.ps1 list-projects    # Lista proyectos aws-*
.\hub.ps1 validate         # Ejecuta validaciones
.\hub.ps1 help             # Muestra ayuda
```

---

## 🔒 Seguridad

### Pre-commit Hooks

```bash
# Instalar hooks
pre-commit install

# Ejecutar manualmente
pre-commit run --all-files

# Ejecutar hook específico
pre-commit run detect-secrets --all-files
```

### Verificación de Seguridad

```bash
# Linux/Mac
./scripts/security-verify.sh

# Windows
.\scripts\security-verify.ps1
```

---

## ☸️ Kubernetes (kind)

### Setup

```bash
# Instalar kind (Linux/Mac)
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind

# Instalar kind (Windows - Chocolatey)
choco install kind
```

### Uso

```bash
# Desplegar demo
make k8s-demo

# Ver estado del job
kubectl get jobs -n tooling-demo

# Ver logs
kubectl logs -n tooling-demo -l job-name=tooling-validate

# Ver configuración de seguridad
kubectl get job -n tooling-demo tooling-validate -o yaml | grep -A 10 securityContext

# Limpiar recursos
make k8s-clean

# Eliminar cluster
make k8s-delete-cluster
```

---

## 🐳 Docker

### Comandos Básicos

```bash
# Construir imagen
docker build -t proyectos-aws/tooling:1.0.0 -f tooling/Dockerfile.tooling tooling/

# Ejecutar validaciones
docker run --rm -v "$(pwd):/workspace:ro" proyectos-aws/tooling:1.0.0 /opt/tooling/scripts/validate.sh

# Shell interactivo
docker run --rm -it -v "$(pwd):/workspace" proyectos-aws/tooling:1.0.0 /bin/bash

# Verificar usuario
docker run --rm proyectos-aws/tooling:1.0.0 whoami
# Debe retornar: tooling
```

---

## 📚 Documentación

| Documento | Descripción |
| :--- | :--- |
| [README.md](../README.md) | Descripción general del proyecto |
| [SECURITY.md](../SECURITY.md) | Política de seguridad y OIDC |
| [docs/TOOLING.md](TOOLING.md) | Guía completa de tooling |
| [docs/killed.md](killed.md) | Prácticas prohibidas |
| [docs/SECURITY_CHECKLIST.md](SECURITY_CHECKLIST.md) | Auditoría de seguridad |

---

## 🧪 Smoke Tests

```bash
# Test 1: Build
make tooling-build

# Test 2: Validate
make tooling-validate

# Test 3: Hub CLI
./hub.sh list-projects

# Test 4: Security
./scripts/security-verify.sh

# Test 5: Kubernetes (requiere kind)
make k8s-demo
kubectl logs -n tooling-demo -l job-name=tooling-validate
make k8s-clean
```

---

## 🔧 Troubleshooting

### Docker no está corriendo

```bash
# Linux
sudo systemctl start docker

# Mac/Windows
# Abrir Docker Desktop
```

### Permisos en scripts (Linux/Mac)

```bash
chmod +x hub.sh
chmod +x scripts/security-verify.sh
chmod +x tooling/scripts/validate.sh
```

### Pre-commit no instalado

```bash
pip install pre-commit
pre-commit install
```

### kind no instalado

```bash
# Linux/Mac
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind

# Windows
choco install kind
```

---

## 🎯 Workflow Típico

```bash
# 1. Hacer cambios en el código
vim aws-amplify-mi-sitio-1/index.html

# 2. Ejecutar validaciones
make tooling-validate

# 3. Verificar seguridad
./scripts/security-verify.sh

# 4. Commit (pre-commit hooks se ejecutan automáticamente)
git add .
git commit -m "feat: actualizar landing page"

# 5. Push
git push origin dev
```

---

## 📞 Soporte

- **Issues:** GitHub Issues
- **Documentación:** [docs/TOOLING.md](TOOLING.md)
- **Seguridad:** [SECURITY.md](../SECURITY.md)

---

**Última actualización:** 2026-02-04  
**Versión:** 1.0.0
