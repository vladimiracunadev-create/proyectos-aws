const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

const path = require('path');

// Middleware para servir archivos estáticos (el frontend premium)
app.use(express.static(path.join(__dirname, 'public')));

// API Endpoint para el estado del contenedor
app.get('/api/status', (req, res) => {
    res.json({
        status: 'success',
        platform: 'AWS ECS Fargate',
        container: 'Docker Industrial',
        message: 'Hola Vladimir! Tu App está funcionando con diseño Premium 🚀',
        timestamp: new Date().toISOString(),
        env: process.env.NODE_ENV || 'development'
    });
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
