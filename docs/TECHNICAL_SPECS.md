# Especificaciones Tecnicas y Requerimientos

Este documento resume que necesitas para ejecutar, validar y extender el monorepo en otra maquina, incluyendo el `Caso E` ya resuelto.

---

## Requerimientos de hardware

### Minimos

- **Sistema operativo**: Windows 10/11, macOS 11+ o Linux moderno
- **Procesador**: 2 nucleos
- **Memoria RAM**: 4 GB
- **Conectividad**: acceso a Internet para proveedores, imagenes y despliegues

### Recomendados

- **Procesador**: 4 nucleos o mas
- **Memoria RAM**: 8 GB o superior
- **Espacio libre**: al menos 2 GB para dependencias, builds, Docker y artefactos SAM

---

## Requerimientos de software

Para operar el repositorio completo:

1. **Git**
2. **Node.js LTS**
3. **AWS CLI** configurado con credenciales validas
4. **Terraform** 1.14 o superior
5. **Docker Desktop** o Docker Engine
6. **kubectl** para el Caso K
7. **Make**

Para trabajar especificamente con `Caso E`:

1. **Python 3.12** o compatible
2. **AWS SAM CLI**
3. **Docker** si usaras `sam local`

Comandos de verificacion recomendados:

```bash
git --version
aws --version
sam --version
python --version
terraform version
docker --version
kubectl version --client
```

---

## Permisos AWS requeridos

El usuario o rol que despliegue debe tener permisos suficientes segun el caso.

### Base general

- `s3:*` acotado a buckets del proyecto o al bucket de artefactos/estado
- `cloudfront:*` donde aplique el Caso C
- `iam:CreateRole`, `iam:AttachRolePolicy`, `iam:PassRole` para despliegues controlados
- `cloudformation:*` para stacks administrados por Terraform o SAM

### Caso E: permisos minimos esperables

- `apigateway:*` o permisos equivalentes sobre HTTP API
- `lambda:*` o permisos de creacion/actualizacion/invocacion de funciones
- `dynamodb:*` o permisos sobre tabla, indices y escritura/lectura
- `logs:*` para CloudWatch Logs de Lambda
- `cloudformation:*` para crear y actualizar el stack `caso-e-dynamodb-persistence`
- `s3:*` sobre el bucket temporal que usa SAM para empaquetado

### FinOps y auditoria

- `budgets:ViewBudget`
- `ce:GetCostAndUsage`
- `ce:GetCostForecast`
- `ec2:Describe*`
- `eks:ListClusters`
- `rds:DescribeDBInstances`

---

## Instalacion en otra maquina

```bash
# 1. Clonar repositorio
git clone <url-del-repo>
cd proyectos-aws-gitlab

# 2. Instalar tooling general
make install

# 3. Configurar AWS
aws configure

# 4. Validar herramientas
make lint
aws sts get-caller-identity
sam --version
```

### Flujo minimo para Caso E

```bash
cd caso-e-dynamodb-persistence/backend
sam build
sam deploy --guided
```

Luego:

```bash
curl "$API_BASE_URL/orders/status/PENDING"
```

Y tambien puedes abrir:

- [caso-e-dynamodb-persistence/README.md](../caso-e-dynamodb-persistence/README.md)
- [caso-e-dynamodb-persistence/AWS_PASO_A_PASO.md](../caso-e-dynamodb-persistence/AWS_PASO_A_PASO.md)

---

## Nota operativa

El repositorio debe reflejar siempre el estado real del despliegue. Si un caso ya esta desplegado y validado, su documentacion global, roadmap y resumen tecnico deben indicarlo explicitamente.
