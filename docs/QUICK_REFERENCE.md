# Quick Reference - proyectos-aws Tooling

Guia rapida de comandos para el sistema de tooling y para casos operativos del monorepo.

---

## Instalacion inicial

```bash
pip install pre-commit
pre-commit install
make tooling-build
```

---

## Comandos Make

```bash
make help
make tooling-build
make tooling-validate
make tooling-shell
make security-scan
make k8s-demo
make k8s-clean
make k8s-delete-cluster
make case-l-deploy
```

---

## Caso E rapido

```bash
cd caso-e-dynamodb-persistence/backend
sam build
sam deploy --guided
```

Validaciones utiles:

```bash
curl "$API_BASE_URL/customers/cust-001/orders"
curl "$API_BASE_URL/orders/status/PENDING"
curl "$API_BASE_URL/products/prod-erp/orders"
```

URL desplegada actualmente:

- [Caso E - API + landing](https://gqqm27j47c.execute-api.us-east-2.amazonaws.com/)

---

## Caso G rapido

```bash
cd caso-g-event-driven/backend
sam build
sam deploy --guided
```

Validaciones utiles:

```bash
curl "$API_BASE_URL/"
curl "$API_BASE_URL/health"
curl -X POST "$API_BASE_URL/events/orders" \
  -H "Content-Type: application/json" \
  -d '{"customerId":"cust-001","status":"CREATED"}'
```

URL desplegada actualmente:

- [Caso G - Landing + API](https://ajcjvroq0a.execute-api.us-east-2.amazonaws.com/)

---

## Hub CLI

### Linux/macOS

```bash
./hub.sh list-projects
./hub.sh validate
./hub.sh help
```

### Windows PowerShell

```powershell
.\hub.ps1 list-projects
.\hub.ps1 validate
.\hub.ps1 help
```

---

## Seguridad

```bash
pre-commit run --all-files
pre-commit run detect-secrets --all-files
```

Verificacion local:

```bash
./scripts/security-verify.sh
.\scripts\security-verify.ps1
```

---

## Kubernetes (kind)

```bash
make k8s-demo
kubectl get jobs -n tooling-demo
kubectl logs -n tooling-demo -l job-name=tooling-validate
make k8s-clean
```

---

## Docker

```bash
docker build -t proyectos-aws/tooling:1.0.0 -f tooling/Dockerfile.tooling tooling/
docker run --rm -v "$(pwd):/workspace:ro" proyectos-aws/tooling:1.0.0 /opt/tooling/scripts/validate.sh
docker run --rm -it -v "$(pwd):/workspace" proyectos-aws/tooling:1.0.0 /bin/bash
```

---

## Documentacion clave

| Documento | Uso |
| :--- | :--- |
| [README.md](../README.md) | Vista general del monorepo |
| [docs/ARCHITECTURE.md](ARCHITECTURE.md) | Arquitectura integral |
| [docs/FILE_STRUCTURE.md](FILE_STRUCTURE.md) | Mapa de carpetas |
| [caso-e-dynamodb-persistence/README.md](../caso-e-dynamodb-persistence/README.md) | Resumen del Caso E |
| [caso-e-dynamodb-persistence/AWS_PASO_A_PASO.md](../caso-e-dynamodb-persistence/AWS_PASO_A_PASO.md) | Deploy y validacion del Caso E |
| [caso-g-event-driven/README.md](../caso-g-event-driven/README.md) | Resumen del Caso G |
| [caso-g-event-driven/AWS_PASO_A_PASO.md](../caso-g-event-driven/AWS_PASO_A_PASO.md) | Deploy y validacion del Caso G |

---

## Workflow tipico

```bash
make tooling-validate
git add .
git commit -m "docs: sync case e documentation"
git push origin main
```

---

_Ultima actualizacion: 2026-03-12_
