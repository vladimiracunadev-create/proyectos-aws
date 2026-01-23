# Multi-stage construction
FROM node:18-bullseye-slim AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

# Final production image
FROM node:18-bullseye-slim
WORKDIR /app
COPY --from=builder /app /app
EXPOSE 3000
CMD [ "node", "server.js" ]
