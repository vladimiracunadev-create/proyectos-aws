# ==========================================
# ETAPA 1: Builder (Construcción)
# ==========================================
FROM node:18-bullseye-slim AS builder

WORKDIR /app

# Copiamos archivos de dependencias primero para aprovechar la caché de capas
COPY package*.json ./

# Instalamos solo dependencias de producción para mantener la imagen limpia
# Si hubiera paso de compilación (TypeScript), aquí se instalarían las devDependencies también
RUN npm ci --only=production

# ==========================================
# ETAPA 2: Runner (Producción)
# ==========================================
FROM node:18-bullseye-slim

# Instalamos dumb-init para manejar correctamente señales de sistema (PID 1)
RUN apt-get update && apt-get install -y --no-install-recommends dumb-init curl \
    && rm -rf /var/lib/apt/lists/*

ENV NODE_ENV=production
WORKDIR /app

# Copiamos desde la etapa builder
COPY --from=builder /app/node_modules ./node_modules
COPY . .

# Usamos el usuario 'node' (UID 1000) que viene por defecto en la imagen oficial
# Esto es CRÍTICO para seguridad (evitar correr como root)
USER node

EXPOSE 3000

# Healthcheck integrado en la imagen
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/ || exit 1

# Usamos dumb-init como entrypoint
ENTRYPOINT ["/usr/bin/dumb-init", "--"]

CMD ["node", "server.js"]
