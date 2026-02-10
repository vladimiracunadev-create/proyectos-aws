# 📊 Reporte de Visualización y Resultados - Caso K (EKS)

> **Nota**: Este documento sirve como evidencia del despliegue exitoso del clúster de EKS, dado que la infraestructura se destruye tras la validación para optimizar costos.

---

## 🏗️ Resumen del Despliegue
Se ha implementado una arquitectura de orquestación industrial utilizando **AWS EKS**. A diferencia de arquitecturas de contenedores simples, aquí el plano de control gestiona activamente la salud y el escalado de la flota.

### Logros Técnicos:
- **Infraestructura**: VPC con 4 subredes (públicas/privadas), NAT Gateway y Clúster EKS version 1.27.
- **Orquestación**: 3 réplicas del pod `vladimir-api` distribuidas en nodos `t3.medium`.
- **Exposición**: Balanceador de carga elástico (ELB) con DNS único.

---

## 🖼️ Galería de Evidencias y Rutas en AWS

### 1. El Clúster EKS (Control Plane)
**Ruta en Consola AWS**: `Elastic Kubernetes Service` > `Clusters` > `vladimir-eks-cluster`.
- **Qué observar**: Verifica que el estado sea `Active` y explora la pestaña **Resources** para ver el estado de salud de los nodos y pods.

### 2. Dashboard con Glassmorphism (Punto de Salida)
**Ruta en Consola AWS**: `EC2` > `Load Balancers`.
- **Qué observar**: Busca el Load Balancer (ELB) de tipo `Network` o `Classic` creado automáticamente por Kubernetes. Copia el **DNS name** y pégalo en tu navegador para ver la interfaz moderna.

### 3. Nodos de Cómputo (Data Plane)
**Ruta en Consola AWS**: `Elastic Kubernetes Service` > `Clusters` > `vladimir-eks-cluster` > pestaña `Compute`.
- **Qué observar**: Verás el `Managed Node Group` y las instancias EC2 (`t3.medium`) que están sosteniendo la flota de contenedores.

### 4. Auto-Sanación (Self-Healing) en Acción
**Ruta en Consola AWS**: `Elastic Kubernetes Service` > `Clusters` > `vladimir-eks-cluster` > pestaña `Resources` > `Pods`.
- **Qué observar**: 
    1. Abre la web y anota el **Pod ID**.
    2. En la terminal (o consola), elimina un Pod.
    3. Refresca la lista en AWS y verás un pod con estado `Pending` o `ContainerCreating` reemplazando al anterior.
    4. Refresca la web y verás el nuevo **Pod ID**.

---

## 📈 Métricas de Verificación

| Característica | Resultado | Método de Validación |
| :--- | :--- | :--- |
| **Escalado** | 3/3 Pods Ready | `kubectl get pods` |
| **Salud** | Liveness/Readiness OK | Kubernetes Events |
| **Red** | Acceso Público ELB | HTTP GET a la URL de AWS |
| **FinOps** | Limpieza Exitosa | `terraform destroy` verificado |

---

## 🏁 Conclusión
El **Caso K** demuestra la capacidad de gestionar entornos productivos complejos, donde la infraestructura no es estática, sino un organismo vivo que se adapta y se recupera automáticamente.

---
*Documentación generada para el perfil de Vladimir Acuña.*
