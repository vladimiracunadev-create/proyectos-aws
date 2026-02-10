# ☸️ Caso K: Kubernetes en AWS (Orquestación EKS)

[![Nivel-10](https://img.shields.io/badge/Nivel-10_Enterprise-blueviolet?style=for-the-badge)]()
[![Status](https://img.shields.io/badge/Status-Nuevo-blue?style=for-the-badge)]()

> [!CAUTION]
> **ADVERTENCIA DE COSTOS**: EKS no está incluido en el Free Tier de AWS. Este laboratorio tiene un costo aproximado de **$0.10 USD/hora**. Sigue la estrategia de limpieza inmediatamente después de verificar.

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

## 🔗 Enlaces Relacionados
- ⬅️ **[Regresar al Roadmap Principal](../README.md)**
- 🏗️ **[Arquitectura de Red](../docs/ARCHITECTURE.md)**
