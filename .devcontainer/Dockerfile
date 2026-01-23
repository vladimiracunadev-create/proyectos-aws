# Usar imagen base de Node (LTS)
FROM node:18-bullseye

# Configurar variables de entorno
ENV TERRAFORM_VERSION=1.14.3
ENV TFSEC_VERSION=v1.28.1

# Instalar dependencias base y herramientas
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    git \
    make \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Instalar AWS CLI
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -rf awscliv2.zip ./aws

# Instalar Terraform
RUN curl -LO "https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip" \
    && unzip "terraform_${TERRAFORM_VERSION}_linux_amd64.zip" \
    && mv terraform /usr/local/bin/ \
    && rm "terraform_${TERRAFORM_VERSION}_linux_amd64.zip"

# Instalar tfsec (Seguridad IaC)
RUN curl -L "https://github.com/aquasecurity/tfsec/releases/download/${TFSEC_VERSION}/tfsec-linux-amd64" -o /usr/local/bin/tfsec \
    && chmod +x /usr/local/bin/tfsec

# Configurar usuario no-root para desarrollo
USER node
WORKDIR /workspace

# El comando por defecto será abrir una terminal
CMD [ "bash" ]
