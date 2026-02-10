const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;
const path = require('path');

// Middleware para servir archivos estáticos
app.use(express.static(path.join(__dirname, 'public')));

// API Endpoint para el estado de Kubernetes
app.get('/api/status', (req, res) => {
    res.json({
        status: 'success',
        platform: 'AWS EKS (Elastic Kubernetes Service)',
        orchestrator: 'Kubernetes v1.27',
        pod_name: process.env.POD_NAME || 'local-pod',
        node_ip: process.env.NODE_IP || '127.0.0.1',
        namespace: process.env.POD_NAMESPACE || 'default',
        message: '¡Hola Vladimir! Tu flota de contenedores está bajo control ☸️',
        timestamp: new Date().toISOString()
    });
});

app.listen(PORT, () => {
    console.log(`EKS Server running on port ${PORT}`);
});
