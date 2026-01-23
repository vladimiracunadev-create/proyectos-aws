# ==============================================================================
# PROYECTO AWS MONOREPO - MAKEFILE
# ==============================================================================
# Este archivo centraliza las tareas comunes del proyecto para facilitar
# el despliegue y mantenimiento desde cualquier sistema.

# Variables (pueden ser sobrescritas desde la línea de comandos)
S3_BUCKET ?= vladimir-caso-b-site-2026
REGION ?= us-east-2
TF_DIR = caso-c-terraform-s3

.PHONY: help install lint format deploy-b tf-init tf-plan tf-apply clean

help: ## Muestra este mensaje de ayuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Instala las dependencias de Node.js (necesario para linting)
	npm install

lint: ## Ejecuta el análisis de calidad de código (JS y HTML)
	npm run lint

format: ## Formatea el código automáticamente usando Prettier
	npm run format

deploy-b: ## Sincroniza el Caso B con AWS S3
	@echo "Desplegando Caso B a S3 ($(S3_BUCKET))..."
	aws s3 sync caso-b-gitlab-s3/ s3://$(S3_BUCKET)/ --delete --exclude "*.md" --region $(REGION)

tf-init: ## Inicializa Terraform para el Caso C
	@echo "Inicializando Terraform en $(TF_DIR)..."
	cd $(TF_DIR) && terraform init -reconfigure

tf-plan: ## Genera el plan de ejecución de infraestructura
	@echo "Generando plan para Caso C..."
	cd $(TF_DIR) && terraform plan -out=tfplan

tf-apply: ## Aplica los cambios de infraestructura del Caso C
	@echo "Aplicando infraestructura para Caso C..."
	cd $(TF_DIR) && terraform apply -auto-approve tfplan

tf-destroy: ## Destruye la infraestructura del Caso C
	@echo "ATENCION: Destruyendo infraestructura de $(TF_DIR)..."
	cd $(TF_DIR) && terraform destroy -auto-approve

clean: ## Limpia archivos temporales de Node y Terraform
	@echo "Limpiando el proyecto..."
	rm -rf node_modules
	rm -rf $(TF_DIR)/.terraform
	rm -f $(TF_DIR)/tfplan
	rm -f $(TF_DIR)/*.tfstate*
