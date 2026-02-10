# 🪜 AWS Paso a Paso - Caso K: Despliegue de EKS Industrial

Este documento detalla el proceso técnico para levantar un clúster de **Kubernetes (EKS)** en AWS, desplegar la aplicación con diseño premium y realizar la limpieza de recursos.

---

## 📋 Requisitos Previos
1. **AWS CLI** configurado con permisos de Administrador.
2. **Terraform** instalado (v1.0+).
3. **kubectl** instalado (compatible con la versión 1.27 de K8s).
4. **Docker** instalado para la gestión de imágenes (opcional si usas imágenes existentes).

---

## 🚀 Fase 1: Infraestructura (Terraform)

### Opción A: Usando Makefile (Recomendado)
```bash
# Navega a la raíz del proyecto
make case-k-init      # Inicializa los plugins de AWS y el estado remoto
make case-k-deploy    # Despliega VPC, Clúster EKS y Manifiestos
```

### Opción B: Comandos Nativos (Manual)
1. **Inicialización**:
   ```bash
   cd caso-k-kubernetes-eks/terraform
   terraform init
   ```
2. **Despliegue de Red y Clúster**:
   ```bash
   terraform apply -auto-approve
   ```
   *Nota: Este proceso toma entre 15 y 20 minutos.*

---

## ☸️ Fase 2: Conexión y Orquestación

### 1. Actualizar el Contexto de kubectl
Para que tu terminal hable con el nuevo clúster en la nube:
```bash
aws eks update-kubeconfig --region us-east-2 --name vladimir-eks-cluster
```

### 2. Despliegue de la Aplicación
```bash
kubectl apply -f caso-k-kubernetes-eks/deployment.yaml
```

### 3. Verificación de Recursos
```bash
kubectl get nodes        # Debes ver los nodos t3.medium en estado Ready
kubectl get pods         # Debes ver 3 pods de vladimir-api corriendo
kubectl get svc          # Copia la EXTERNAL-IP del LoadBalancer
```

---

## 🎨 Fase 3: Validación Visual
1. Espera 2-3 minutos a que el Load Balancer de AWS esté activo.
2. Pega la URL obtenida en tu navegador.
3. **Prueba de Fuego (Auto-Sanación)**:
   ```bash
   # Borra un pod manualmente
   kubectl delete pod <nombre-de-un-pod>
   # Observa cómo Kubernetes levanta uno nuevo instantáneamente
   kubectl get pods -w
   ```

---

## 🚨 Fase 4: Limpieza (FinOps)
**¡IMPORTANTE!** Para no generar cargos innecesarios en tu cuenta de AWS, ejecuta la limpieza inmediatamente después de tus pruebas.

### Opción A: Usando Makefile
```bash
make case-k-destroy
```

### Opción B: Manual
```bash
cd caso-k-kubernetes-eks/terraform
terraform destroy -auto-approve
```

---

## 🔍 Resolución de Problemas Comunes
- **Error: "Unauthorized" al usar kubectl**: Revisa que tus credenciales de `aws configure` sean las mismas que crearon el clúster.
- **Pods en estado "Pending"**: Verifica que los nodos tengan recursos suficientes (`kubectl describe node`).
- **ELB no carga**: Los Load Balancers clásicos de AWS pueden tardar hasta 5 minutos en propagar el DNS.

---
*Guía técnica profesional para el portafolio de Vladimir Acuña.*
