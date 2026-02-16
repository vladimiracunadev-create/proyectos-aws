# ☸️ Caso K: Kubernetes en AWS (Orquestación EKS)

## 🚀 Despliegue Operativo (Caso K)

**¡El proyecto ya se encuentra en vivo!** Puedes acceder al dashboard premium desplegado en Amazon EKS aquí:

👉 **[Dashboard Operativo en AWS (ESTADO: DESACTIVADO POR COSTOS FINOPS)](http://k8s-default-vladimir-fd9bd8dc79-d4392d3db0728cc7.elb.us-east-1.amazonaws.com)**

---

[![Nivel-10](https://img.shields.io/badge/Nivel-10_Enterprise-blueviolet?style=for-the-badge)]()
[![Status](https://img.shields.io/badge/Status-Completado-green?style=for-the-badge)]()

> [!CAUTION]
> **ADVERTENCIA DE COSTOS CRÍTICA**: EKS no está incluido en el Free Tier de AWS. Este laboratorio tiene un costo aproximado de **$0.10 USD/hora** ($72 USD/mes) solo por el clúster, más NAT Gateway y cómputo. **Sigue la estrategia de limpieza inmediatamente después de verificar.** Ver [AWS_PASO_A_PASO.md](./AWS_PASO_A_PASO.md) para instrucciones de eliminación.

---

## 🎯 Objetivo
Maestría en orquestación. Aprenderás a gestionar clusters reales en la nube, autosanación de pods, balanceo de carga L7 y despliegues con cero tiempo de inactividad (Rolling Updates).

## 🏗️ Stack del Cluster
- **AWS EKS**: El plano de control avanzado.
- **Kubectl**: Tu terminal de mando para el clúster.
- **YAML Manifests**: La verdad absoluta del estado deseado.
- **Terraform**: Infraestructura como Código (VPC, Subnets, EKS).

## 💰 Gestión de Costos (Opción A)
Para minimizar el gasto, hemos implementado una estrategia de **"Fast Deploy & Destroy"**:
1. Desplegar (`make case-k-deploy`)
2. Validar el funcionamiento.
3. **Destruir inmediatamente** (`make case-k-destroy`).

## 🛠️ Comandos de Supervivencia
```bash
make case-k-init      # Inicializa los planos de infraestructura
make case-k-deploy    # Levanta el clúster y despliega la app
make case-k-destroy   # 🚨 BORRA TODO PARA EVITAR CARGOS EXTRAS
```

## 🖼️ Evidencia de Resultados
Dado que este clúster se destruye para optimizar costos, puedes ver las capturas y el reporte de funcionamiento aquí:
👉 **[Reporte de Visualización y Resultados](./VISUALIZATION.md)**

## 🔗 Enlaces Relacionados
- ⬅️ **[Regresar al Roadmap Principal](../README.md)**
- 🏗️ **[Arquitectura de Red](../docs/ARCHITECTURE.md)**
