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
curl "$API_BASE_URL/health?format=json"
curl -X POST "$API_BASE_URL/events/orders" \
  -H "Content-Type: application/json" \
  -d '{"customerId":"cust-001","status":"CREATED"}'
```

URL desplegada actualmente:

- [Caso G - Landing + API](https://ajcjvroq0a.execute-api.us-east-2.amazonaws.com/)
- [Caso G - Health HTML](https://ajcjvroq0a.execute-api.us-east-2.amazonaws.com/health)
- [Caso G - Health JSON](https://ajcjvroq0a.execute-api.us-east-2.amazonaws.com/health?format=json)

---

## Caso H rapido

```bash
cd caso-h-observability/backend
sam build && sam deploy --guided
```

Validaciones utiles:

```bash
# Landing con metricas
curl "$API_H_URL/"

# Health check
curl "$API_H_URL/health"

# Publicar metrica custom
curl -X POST "$API_H_URL/metrics" \
  -H "Content-Type: application/json" \
  -d '{"metricName":"DemoMetric","value":1,"unit":"Count"}'

# Listar metricas
curl "$API_H_URL/metrics"
```

URL desplegada actualmente:

- [Caso H - Landing + API](https://z7evf8mrzf.execute-api.us-east-2.amazonaws.com/)
- [Caso H - Health](https://z7evf8mrzf.execute-api.us-east-2.amazonaws.com/health)

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

## Caso F rapido

```bash
cd caso-f-security-cognito/backend
sam build && sam deploy --guided
# DeployWAF: false (por defecto, sin costo base)
```

Validaciones utiles:

```bash
# Registrar usuario
curl -s -X POST "$API_F_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@demo.com","password":"Demo1234"}' | jq .

# Login + guardar token
TOKEN=$(curl -s -X POST "$API_F_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@demo.com","password":"Demo1234"}' | jq -r '.accessToken')

# Perfil protegido (JWT validado por API GW)
curl -s "$API_F_URL/profile" -H "Authorization: $TOKEN" | jq .

# Verificar que /profile rechaza sin token
curl -s -o /dev/null -w "%{http_code}" "$API_F_URL/profile"
# Esperado: 403
```

---

## Documentacion clave

| Documento | Uso |
| :--- | :--- |
| [README.md](../README.md) | Vista general del monorepo |
| [docs/ARCHITECTURE.md](ARCHITECTURE.md) | Arquitectura integral |
| [docs/COMPLETED_CASES_GUIDE.md](COMPLETED_CASES_GUIDE.md) | Lectura simple de casos completados |
| [docs/FILE_STRUCTURE.md](FILE_STRUCTURE.md) | Mapa de carpetas |
| [caso-e-dynamodb-persistence/README.md](../caso-e-dynamodb-persistence/README.md) | Resumen del Caso E |
| [caso-e-dynamodb-persistence/AWS_PASO_A_PASO.md](../caso-e-dynamodb-persistence/AWS_PASO_A_PASO.md) | Deploy y validacion del Caso E |
| [caso-f-security-cognito/README.md](../caso-f-security-cognito/README.md) | Resumen del Caso F |
| [caso-f-security-cognito/AWS_PASO_A_PASO.md](../caso-f-security-cognito/AWS_PASO_A_PASO.md) | Deploy y validacion del Caso F |
| [caso-g-event-driven/README.md](../caso-g-event-driven/README.md) | Resumen del Caso G |
| [caso-g-event-driven/AWS_PASO_A_PASO.md](../caso-g-event-driven/AWS_PASO_A_PASO.md) | Deploy y validacion del Caso G |
| [caso-h-observability/README.md](../caso-h-observability/README.md) | Resumen del Caso H |
| [caso-h-observability/AWS_PASO_A_PASO.md](../caso-h-observability/AWS_PASO_A_PASO.md) | Deploy y validacion del Caso H |

---

## Workflow tipico

```bash
make tooling-validate
git add .
git commit -m "docs: sync case e documentation"
git push origin main
```

---

_Ultima actualizacion: 2026-03-17_
