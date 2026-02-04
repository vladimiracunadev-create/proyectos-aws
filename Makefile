# Makefile para proyectos-aws
# Proporciona comandos para tooling, validación, y Kubernetes

.PHONY: help tooling-build tooling-validate tooling-shell security-scan k8s-demo k8s-clean

# Variables
TOOLING_IMAGE := proyectos-aws/tooling:1.0.0
TOOLING_IMAGE_LATEST := proyectos-aws/tooling:latest
WORKSPACE := $(shell pwd)
K8S_NAMESPACE := tooling-demo

# Colors para output
GREEN := \033[0;32m
YELLOW := \033[1;33m
NC := \033[0m # No Color

help: ## Muestra esta ayuda
	@echo "=========================================="
	@echo "🛠️  Makefile - proyectos-aws"
	@echo "=========================================="
	@echo ""
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""

tooling-build: ## Construye la imagen Docker de tooling
	@echo "$(GREEN)🔨 Construyendo imagen de tooling...$(NC)"
	docker build -t $(TOOLING_IMAGE) -t $(TOOLING_IMAGE_LATEST) -f tooling/Dockerfile.tooling tooling/
	@echo "$(GREEN)✅ Imagen construida: $(TOOLING_IMAGE)$(NC)"

tooling-validate: ## Ejecuta validaciones en contenedor Docker
	@echo "$(GREEN)🔍 Ejecutando validaciones...$(NC)"
	docker run --rm \
		-v "$(WORKSPACE):/workspace:ro" \
		$(TOOLING_IMAGE) \
		/opt/tooling/scripts/validate.sh

tooling-shell: ## Abre shell interactivo en contenedor de tooling
	@echo "$(GREEN)🐚 Abriendo shell en contenedor de tooling...$(NC)"
	docker run --rm -it \
		-v "$(WORKSPACE):/workspace" \
		$(TOOLING_IMAGE) \
		/bin/bash

security-scan: ## Ejecuta escaneo de secretos y dependencias
	@echo "$(GREEN)🔒 Ejecutando escaneo de seguridad...$(NC)"
	@if command -v pre-commit > /dev/null; then \
		pre-commit run detect-secrets --all-files || true; \
	else \
		echo "$(YELLOW)⚠️  pre-commit no instalado. Instala con: pip install pre-commit$(NC)"; \
	fi

k8s-demo: ## Despliega job de validación en kind (requiere kind)
	@echo "$(GREEN)☸️  Desplegando demo en Kubernetes...$(NC)"
	@if ! command -v kind > /dev/null; then \
		echo "$(YELLOW)⚠️  kind no instalado. Instala desde: https://kind.sigs.k8s.io/$(NC)"; \
		exit 1; \
	fi
	@if ! kind get clusters | grep -q "proyectos-aws"; then \
		echo "$(GREEN)📦 Creando cluster kind...$(NC)"; \
		kind create cluster --name proyectos-aws; \
	fi
	@echo "$(GREEN)📤 Cargando imagen en kind...$(NC)"
	kind load docker-image $(TOOLING_IMAGE) --name proyectos-aws
	@echo "$(GREEN)🚀 Aplicando manifiestos de Kubernetes...$(NC)"
	kubectl apply -k k8s/tooling-job/
	@echo "$(GREEN)✅ Job desplegado. Verifica con: kubectl logs -n $(K8S_NAMESPACE) -l job-name=tooling-validate$(NC)"

k8s-clean: ## Limpia recursos de Kubernetes
	@echo "$(GREEN)🧹 Limpiando recursos de Kubernetes...$(NC)"
	kubectl delete -k k8s/tooling-job/ --ignore-not-found=true
	@echo "$(GREEN)✅ Recursos eliminados$(NC)"

k8s-delete-cluster: ## Elimina el cluster kind
	@echo "$(YELLOW)⚠️  Eliminando cluster kind...$(NC)"
	kind delete cluster --name proyectos-aws || true
	@echo "$(GREEN)✅ Cluster eliminado$(NC)"

# Default target
.DEFAULT_GOAL := help
