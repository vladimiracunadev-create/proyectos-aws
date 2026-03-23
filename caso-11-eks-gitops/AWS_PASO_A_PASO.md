# Caso 11 — Guia paso a paso: EKS + GitOps con GitHub Actions

> Estado: Implementacion proyectada — Q4 2026.
> Tiempo estimado: 3 horas.

---

## Que resuelve este caso

Provisiona un cluster EKS con Terraform, configura IRSA para autenticar pods
sin credenciales estaticas, y establece un flujo GitOps donde GitHub Actions
actua como controlador de reconciliacion: lo que esta en Git es lo que corre
en el cluster.

---

## Prerrequisitos

| Requisito | Verificacion |
|:---|:---|
| Terraform >= 1.7 instalado | `terraform version` |
| kubectl instalado | `kubectl version --client` |
| eksctl instalado (opcional) | `eksctl version` |
| Caso 08 funcionando | Imagen en GHCR o ECR disponible |
| Permisos IAM para EKS | Ver paso 1 |

---

## Paso 1 — Permisos IAM para provisionar EKS

El rol de GitHub Actions necesita permisos adicionales para crear el cluster:

```json
{
  "Effect": "Allow",
  "Action": [
    "eks:CreateCluster",
    "eks:DescribeCluster",
    "eks:UpdateClusterConfig",
    "eks:ListClusters",
    "eks:CreateNodegroup",
    "eks:DescribeNodegroup",
    "ec2:CreateVpc",
    "ec2:CreateSubnet",
    "ec2:DescribeSubnets",
    "iam:CreateRole",
    "iam:AttachRolePolicy",
    "iam:CreateOpenIDConnectProvider"
  ],
  "Resource": "*"
}
```

---

## Paso 2 — Provisionar el cluster con Terraform

```hcl
# terraform/eks-cluster.tf
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name    = "caso-11-cluster"
  cluster_version = "1.32"

  vpc_id                         = module.vpc.vpc_id
  subnet_ids                     = module.vpc.private_subnets
  cluster_endpoint_public_access = true

  eks_managed_node_groups = {
    main = {
      instance_types = ["t3.small"]
      min_size       = 1
      max_size       = 3
      desired_size   = 2
    }
  }

  # Habilitar OIDC Provider (necesario para IRSA)
  enable_irsa = true
}
```

Aplicar:

```bash
cd caso-11-eks-gitops/terraform
terraform init
terraform plan -out=tfplan
terraform apply tfplan
```

Verificar el cluster:

```bash
aws eks describe-cluster \
  --name caso-11-cluster \
  --query "cluster.status" \
  --output text
# ACTIVE
```

---

## Paso 3 — Configurar IRSA (IAM Roles for Service Accounts)

IRSA permite que pods especificos asuman roles IAM sin credenciales en el contenedor.

```hcl
# terraform/irsa.tf
data "aws_iam_openid_connect_provider" "eks" {
  url = module.eks.cluster_oidc_issuer_url
}

resource "aws_iam_role" "app_irsa" {
  name = "caso-11-app-irsa"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = {
        Federated = data.aws_iam_openid_connect_provider.eks.arn
      }
      Action    = "sts:AssumeRoleWithWebIdentity"
      Condition = {
        StringEquals = {
          "${replace(module.eks.cluster_oidc_issuer_url, "https://", "")}:sub" =
            "system:serviceaccount:default:caso-11-app"
        }
      }
    }]
  })
}
```

---

## Paso 4 — Manifiestos Kubernetes

```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: caso-11
```

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: caso-11-app
  namespace: caso-11
spec:
  replicas: 2
  selector:
    matchLabels:
      app: caso-11-app
  template:
    metadata:
      labels:
        app: caso-11-app
      annotations:
        eks.amazonaws.com/role-arn: arn:aws:iam::<ACCOUNT_ID>:role/caso-11-app-irsa
    spec:
      serviceAccountName: caso-11-app
      containers:
        - name: app
          image: ghcr.io/<REPO>/caso-08:latest
          ports:
            - containerPort: 8080
          readinessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
```

```yaml
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: caso-11-hpa
  namespace: caso-11
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: caso-11-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

---

## Paso 5 — Conectar kubectl al cluster

```bash
aws eks update-kubeconfig \
  --name caso-11-cluster \
  --region us-east-1

kubectl get nodes
# NAME                          STATUS   ROLES    AGE
# ip-10-0-1-100.ec2.internal    Ready    <none>   5m
```

---

## Paso 6 — Workflow GitOps

```yaml
name: Caso 11 — EKS GitOps

on:
  push:
    branches: [main]
    paths:
      - 'caso-11-eks-gitops/k8s/**'

permissions:
  id-token: write
  contents: read

jobs:
  gitops-deploy:
    name: Reconciliar cluster EKS
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ vars.AWS_ROLE_ARN }}
          aws-region: us-east-1

      - name: Configurar kubectl
        run: |
          aws eks update-kubeconfig \
            --name caso-11-cluster \
            --region us-east-1

      - name: Aplicar manifiestos
        run: kubectl apply -f caso-11-eks-gitops/k8s/

      - name: Esperar rollout
        run: |
          kubectl rollout status deployment/caso-11-app \
            --namespace caso-11 \
            --timeout=5m

      - name: Smoke test
        id: smoke
        run: |
          ALB=$(kubectl get ingress caso-11-ingress \
            --namespace caso-11 \
            --output jsonpath='{.status.loadBalancer.ingress[0].hostname}')
          STATUS=$(curl -s -o /dev/null -w "%{http_code}" "https://${ALB}/health")
          echo "status=$STATUS"
          [ "$STATUS" = "200" ] || exit 1

      - name: Rollback si smoke test falla
        if: failure() && steps.smoke.conclusion == 'failure'
        run: |
          kubectl rollout undo deployment/caso-11-app \
            --namespace caso-11
          echo "Rollback completado"
```

---

## Paso 7 — Verificacion

```bash
# Estado del deployment
kubectl get deployment caso-11-app --namespace caso-11
# NAME           READY   UP-TO-DATE   AVAILABLE   AGE
# caso-11-app    2/2     2            2           10m

# Pods en ejecucion
kubectl get pods --namespace caso-11
# NAME                          READY   STATUS    RESTARTS   AGE
# caso-11-app-xxx-yyy           1/1     Running   0          5m

# Historial de rollouts
kubectl rollout history deployment/caso-11-app --namespace caso-11
# REVISION  CHANGE-CAUSE
# 1         <none>
# 2         <none>

# Verificar IRSA en el pod
kubectl exec -it <pod-name> --namespace caso-11 -- \
  env | grep AWS_ROLE_ARN
# AWS_ROLE_ARN=arn:aws:iam::<ACCOUNT>:role/caso-11-app-irsa
```

---

## Errores comunes y soluciones

### `error: You must be logged in to the server (Unauthorized)`

Causa: El rol de GitHub Actions no tiene permisos en el cluster EKS.
El cluster tiene su propia lista de acceso en `aws-auth` ConfigMap.

Solucion: Añadir el rol al ConfigMap:

```bash
kubectl edit configmap aws-auth --namespace kube-system
# Añadir bajo mapRoles:
# - rolearn: arn:aws:iam::<ACCOUNT>:role/<GITHUB_ROLE>
#   username: github-actions
#   groups:
#     - system:masters
```

---

### El HPA no escala (External Metrics Server no instalado)

Causa: EKS no incluye el Metrics Server por defecto.

Solucion:

```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

---

### `ImagePullBackOff` desde GHCR en EKS

Causa: Los nodos EKS no tienen acceso a GHCR si la imagen es privada.

Solucion: Crear un ImagePullSecret en el cluster:

```bash
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=<GITHUB_USER> \
  --docker-password=<GITHUB_TOKEN> \
  --namespace caso-11
```

Referenciar en el deployment con `imagePullSecrets`.

---

## Siguiente paso

Este es el caso final del repositorio.

-> [README del repositorio](../README.md): vision completa del proyecto.
