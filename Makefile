# ==============================================================================
# PROYECTO AWS MONOREPO - MAKEFILE
# ==============================================================================
# Este archivo centraliza las tareas comunes del proyecto para facilitar
# el despliegue y mantenimiento desde cualquier sistema.

# Variables (pueden ser sobrescritas desde la línea de comandos)
S3_BUCKET ?= vladimir-caso-b-site-2026
REGION ?= us-east-2
TF_DIR = caso-c-terraform-s3

.PHONY: help install lint format serve upload deploy-b tf-init tf-plan tf-apply tf-security docker-build k8s-lint clean case-f-demo-build case-f-demo-deploy case-f-demo-destroy case-f-visualization-build case-f-visualization-deploy case-f-visualization-destroy case-h-build case-h-deploy case-h-destroy case-k-init case-k-deploy case-k-destroy finops-check test test-d test-e test-f test-g test-h smoke-d smoke-e smoke-f smoke-g smoke-h

help: ## Muestra este mensaje de ayuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

finops-check: ## 💰 Escanea recursos activos en AWS (Multi-Región) para evitar cobros
	@if [ -f /bin/bash ]; then \
		echo "Detectado entorno Bash. Ejecutando script .sh..."; \
		chmod +x ./scripts/aws-resource-audit.sh; \
		./scripts/aws-resource-audit.sh; \
	else \
		echo "Detectado entorno Windows/PowerShell. Ejecutando script .ps1..."; \
		powershell -ExecutionPolicy Bypass -File ./scripts/aws-resource-audit.ps1; \
	fi

case-l-deploy: ## Genera datos de FinOps y sincroniza el sitio estático S3
	@echo "Generando datos de costos..."
	python generate_finops_data.py
	@echo "Sincronizando a S3..."
	aws s3 sync caso-l-finops-optimization/app/public/ s3://finops-vladimir-portfolio-case-l --delete

serve: ## Levanta servidor local en puerto 8000 (requiere Python)
	@echo "Iniciando servidor en http://localhost:8000..."
	python -m http.server 8000

upload: ## Sincroniza cambios con el repositorio Git usando Python
	@echo "Subiendo cambios al repositorio..."
	python -c "import os; os.system('git add .'); os.system('git commit -m \"Actualización de documentación y portal\"'); os.system('git push')"

docker-build: ## Construye la imagen Docker de la API (Caso J)
	@echo "Construyendo imagen Docker..."
	cd caso-j-containers-ecs && docker build -t vladimir-api:latest .

k8s-lint: ## Valida los manifiestos de Kubernetes (Caso K)
	@echo "Validando manifiestos K8s..."
	kubectl apply --dry-run=client -f caso-k-kubernetes-eks/deployment.yaml

install: ## Instala las dependencias de Node.js (necesario para linting)
	npm install

lint: ## Ejecuta el análisis de calidad de código (JS y HTML)
	npm run lint

tf-security: ## Audita la seguridad de la infraestructura con tfsec
	@echo "Escaneando seguridad en $(TF_DIR)..."
	tfsec $(TF_DIR)

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


# ==========================================
# CASO F: Security First
# ==========================================
CASE_F_DIR = caso-f-security-cognito/backend

case-f-demo-build: ## Compila el Caso F en modo demo (HTTP API + JWT)
	@echo "Compilando Caso F demo..."
	cd $(CASE_F_DIR) && sam build

case-f-demo-deploy: case-f-demo-build ## Despliega el Caso F en modo demo sin costo base
	@echo "Desplegando Caso F demo en $(REGION)..."
	cd $(CASE_F_DIR) && sam deploy --stack-name caso-f-security-cognito --region $(REGION) --resolve-s3 --capabilities CAPABILITY_IAM --no-confirm-changeset --no-fail-on-empty-changeset

case-f-demo-destroy: ## Elimina el Caso F demo
	@echo "Eliminando Caso F demo..."
	cd $(CASE_F_DIR) && sam delete --stack-name caso-f-security-cognito --region $(REGION) --no-prompts

case-f-visualization-build: ## Compila el Caso F en modo visualization (REST API + WAF)
	@echo "Compilando Caso F visualization..."
	cd $(CASE_F_DIR) && sam build --template-file template-visualization.yaml

case-f-visualization-deploy: case-f-visualization-build ## Despliega el Caso F visualization (WAF activo: destruir tras capturas)
	@echo "Desplegando Caso F visualization en $(REGION)..."
	cd $(CASE_F_DIR) && sam deploy --template-file template-visualization.yaml --stack-name caso-f-security-cognito-visualization --region $(REGION) --resolve-s3 --capabilities CAPABILITY_IAM --no-confirm-changeset --no-fail-on-empty-changeset

case-f-visualization-destroy: ## Elimina el Caso F visualization y evita cobro del WAF
	@echo "Eliminando Caso F visualization..."
	cd $(CASE_F_DIR) && sam delete --stack-name caso-f-security-cognito-visualization --region $(REGION) --no-prompts

# ==========================================
# CASO H: Observability + CloudWatch + X-Ray
# ==========================================
CASE_H_DIR = caso-h-observability/backend

case-h-build: ## Compila el Caso H con AWS SAM
	@echo "Compilando Caso H..."
	cd $(CASE_H_DIR) && sam build

case-h-deploy: case-h-build ## Despliega el Caso H (Dashboard con costo fijo: destruir tras capturas)
	@echo "Desplegando Caso H en $(REGION)..."
	cd $(CASE_H_DIR) && sam deploy --stack-name caso-h-observability --region $(REGION) --resolve-s3 --capabilities CAPABILITY_IAM --no-confirm-changeset --no-fail-on-empty-changeset

case-h-destroy: ## ELIMINA TODO EL CASO H sin tocar otros stacks del portafolio
	@echo "ELIMINANDO Caso H de forma segura..."
	cd $(CASE_H_DIR) && sam delete --stack-name caso-h-observability --region $(REGION) --no-prompts
	@echo "Caso H eliminado. Verifica dashboard, alarmas y API en consola AWS."


# ==========================================
# CASO J: Docker + ECS + ECR
# ==========================================
TF_J_DIR = caso-j-containers-ecs/terraform

case-j-init: ## Inicializa Terraform para el Caso J
	@echo "Inicializando Terraform en $(TF_J_DIR)..."
	cd $(TF_J_DIR) && terraform init -reconfigure

case-j-plan: ## Genera el plan de ejecución para Caso J
	@echo "Generando plan para Caso J..."
	cd $(TF_J_DIR) && terraform plan -out=tfplan

case-j-apply: ## Aplica la infraestructura del Caso J
	@echo "Aplicando infraestructura para Caso J..."
	cd $(TF_J_DIR) && terraform apply -auto-approve tfplan

case-j-destroy: ## 🚨 ELIMINA TODO EL CASO J (EVITA CARGOS EXTRAS)
	@echo "ATENCION: Destruyendo infraestructura de $(TF_J_DIR)..."
	cd $(TF_J_DIR) && terraform destroy -auto-approve

docker-login: ## Inicia sesión en ECR (requiere AWS CLI configurado)
	@echo "Iniciando sesión en ECR..."
	aws ecr get-login-password --region $(REGION) | docker login --username AWS --password-stdin $$(cd $(TF_J_DIR) && terraform output -raw ecr_repository_url | cut -d'/' -f1)

docker-push: docker-build ## Etiqueta y sube la imagen a ECR
	@echo "Subiendo imagen a ECR..."
	$(eval REPO_URL := $(shell cd $(TF_J_DIR) && terraform output -raw ecr_repository_url))
	docker tag vladimir-api:latest $(REPO_URL):latest
	docker push $(REPO_URL):latest
	@echo "Imagen subida exitosamente!"

# ==========================================
# CASO K: Kubernetes EKS
# ==========================================
TF_K_DIR = caso-k-kubernetes-eks/terraform

case-k-init: ## Inicializa Terraform para el Caso K
	@echo "Inicializando Terraform en $(TF_K_DIR)..."
	cd $(TF_K_DIR) && terraform init -reconfigure

case-k-deploy: case-k-init ## Despliega el clúster y la app (ADVERTENCIA: TIENE COSTO)
	@echo "ADVERTENCIA: Iniciando despliegue de EKS. Costo: $0.10/hr."
	cd $(TF_K_DIR) && terraform apply -auto-approve
	aws eks update-kubeconfig --region $(REGION) --name vladimir-eks-cluster
	kubectl apply -f caso-k-kubernetes-eks/deployment.yaml
	@echo "Despliegue completado! Verifica la URL del balanceador en la consola AWS."

case-k-destroy: ## 🚨 ELIMINA TODO EL CASO K (EVITA CARGOS EXTRAS)
	@echo "ELIMINANDO Caso K de forma permanente..."
	cd $(TF_K_DIR) && terraform destroy -auto-approve
	@echo "Limpieza completada exitosamente!"

# ==========================================
# TESTING (pytest — Python Lambdas)
# ==========================================

test-d: ## Ejecuta tests unitarios del Caso D (Lambda contact form)
	@echo "Testing Caso D..."
	python -m pytest caso-d-serverless-basic/backend/tests/ -v --tb=short

test-e: ## Ejecuta tests unitarios del Caso E (Lambda DynamoDB persistence)
	@echo "Testing Caso E..."
	python -m pytest caso-e-dynamodb-persistence/backend/tests/ -v --tb=short

test-f: ## Ejecuta tests unitarios del Caso F (Cognito + JWT)
	@echo "Testing Caso F..."
	python -m pytest caso-f-security-cognito/backend/tests/ -v --tb=short

test-g: ## Ejecuta tests unitarios del Caso G (Lambda event-driven)
	@echo "Testing Caso G..."
	python -m pytest caso-g-event-driven/backend/tests/ -v --tb=short

test-h: ## Ejecuta tests unitarios del Caso H (Lambda observability)
	@echo "Testing Caso H..."
	python -m pytest caso-h-observability/backend/tests/ -v --tb=short

test: test-d test-e test-f test-g test-h ## Ejecuta todos los tests unitarios de Lambdas

# ==========================================
# SMOKE TESTS (requieren API_*_URL definidas)
# ==========================================

smoke-d: ## Smoke test Caso D — requiere API_D_URL
	bash scripts/smoke/smoke_caso_d.sh

smoke-e: ## Smoke test Caso E — requiere API_E_URL
	bash scripts/smoke/smoke_caso_e.sh

smoke-f: ## Smoke test Caso F — requiere API_F_URL
	bash scripts/smoke/smoke_caso_f.sh

smoke-g: ## Smoke test Caso G — requiere API_G_URL
	bash scripts/smoke/smoke_caso_g.sh

smoke-h: ## Smoke test Caso H — requiere API_H_URL
	bash scripts/smoke/smoke_caso_h.sh

clean: ## Limpia archivos temporales de Node y Terraform
	@echo "Limpiando el proyecto..."
	rm -rf node_modules
	rm -rf $(TF_DIR)/.terraform
	rm -f $(TF_DIR)/tfplan
	rm -f $(TF_DIR)/*.tfstate*
	rm -rf $(TF_J_DIR)/.terraform
	rm -f $(TF_J_DIR)/tfplan
	rm -f $(TF_J_DIR)/*.tfstate*
