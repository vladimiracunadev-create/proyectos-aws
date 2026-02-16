# 📊 Reporte de Visualización y Resultados - Caso K (EKS)

## 🎯 ¿Por qué este documento?
Este reporte sirve como evidencia técnica del despliegue exitoso del **Caso K (Kubernetes EKS)**. Dada la naturaleza de los costos asociados, seguimos una estrategia de **"Evidencia Estática"** para demostrar la maestría en orquestación sin mantener costos activos.

---

## 🏗️ Resumen de la Implementación
Se ha migrado de una infraestructura puramente automatizada (Terraform) a una metodología híbrida que permite el despliegue manual desde la **Consola de AWS**, permitiendo un control total sobre cada componente.

### Logros Técnicos:
- **Networking**: VPC configurada con subredes públicas/privadas y NAT Gateways redundantes.
- **Cómputo**: Clúster EKS gestionando nodos `t3.medium`.
- **Estrategia FinOps**: Ciclo de vida "Deploy-Validate-Destroy" documentado.

---

## 🖼️ Galería de Evidencias (Flujo de Despliegue)

A continuación se presentan los espacios para las capturas de pantalla que validan cada fase del despliegue manual, siguiendo el orden del **Walkthrough**.

### 1. Infraestructura de Red (VPC)
> **Acción**: Captura de la consola de VPC mostrando la red `vladimir-eks`, las 4 subredes y los NAT Gateways creados.

![VPC Configuration](./img/vpc-config.png "Configuración de Red VPC en AWS")

### 2. Identidad y Accesos (IAM)

#### 2.1. Rol del Clúster (Control Plane)
> **Acción**: Captura del rol `Vladimir-EKS-Cluster-Role` mostrando la política `AmazonEKSClusterPolicy` adjunta.

![EKS Cluster Role](./img/eks-cluster-role.png "Rol IAM para el Clúster EKS")

#### 2.2. Rol de los Nodos (Worker Nodes)
> **Acción**: Captura del rol `Vladimir-EKS-Node-Role` mostrando las 3 políticas obligatorias (`WorkerNode`, `CNI`, `ECRReadOnly`).

![EKS Node Role](./img/eks-node-role.png "Rol IAM para los Nodos EKS")

### 3. El Clúster EKS (Control Plane)
> **Acción**: Sube una captura de `EKS > Clusters > vladimir-eks-cluster` mostrando el estado **Active**.

![EKS Cluster Active](./img/eks-cluster-active.png "EKS Cluster Active State")

### 4. Nodos de Cómputo (Managed Nodes / Auto Mode)
> **Acción**: Captura de la pestaña **"Informática" (Compute)**, **Nodes** o **Resources** dentro del clúster, mostrando los nodos creados automáticamente en estado **Ready**.

![EKS Compute Nodes](./img/eks-compute-nodes.png "Listado de Nodos Saludables en EKS")

### 5. Aplicación y Dashboard Premium (Glassmorphism)
> **Acción**: Captura del navegador accediendo a la App a través del DNS del Load Balancer.

![Dashboard Moderno](./img/eks-dashboard-glassmorphism.png "Dashboard Moderno con Glassmorphism")

### 6. Prueba de Auto-Sanación (Self-Healing)
> **Acción**: Collage mostrando el comando `kubectl delete pod` y la recuperación inmediata en la consola.

![Self-Healing Demo](./img/eks-self-healing-demo.png "Prueba de Auto-sanación exitosa")

---

## 📈 Tabla de Validación Final

| Hito | Estado | Método |
| :--- | :--- | :--- |
| **Infraestructura** | 🟢 Validado | Consola AWS (VPC/EKS) |
| **Orquestación** | 🟢 Validado | Pods distribuidos (3 réplicas) |
| **Connectivity** | 🟢 Validado | Load Balancer DNS Público |
| **FinOps** | ⚠️ Crítico | Eliminación verificada post-captura |

---

## 🏁 Conclusión
El **Caso K** es la pieza cumbre de orquestación en este portafolio, demostrando que Vladimir Acuña posee las habilidades para operar clústeres reales bajo estándares empresariales de AWS.

---
*Documentación generada para el portafolio de Vladimir Acuña.*
