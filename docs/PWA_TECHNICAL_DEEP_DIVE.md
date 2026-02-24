# 🎓 Deep Dive: Ingeniería PWA (Service Workers & Caché)

Este documento detalla la arquitectura técnica detrás de las capacidades de **Progressive Web App (PWA)** de los portafolios, enfocándose en la resiliencia y el rendimiento.

---

## 🧠 El Service Worker (`service-worker.js`)

Nuestra implementación utiliza un patrón de **"Offline-First"** optimizado para activos estáticos.

### 1. Estrategia de Caché: `Cache-First`
Para los recursos definidos en la constante `ASSETS` (CSS, JS, iconos), el sistema inter intercepta la petición y:
1. Busca en el almacenamiento de `caches`.
2. Si lo encuentra, lo sirve inmediatamente (latencia < 10ms).
3. Si no, intenta obtenerlo de la red.

### 2. Gestión de Navegación y Resiliencia
En caso de que el usuario intente navegar a una página nueva mientras está offline:
```javascript
if (event.request.mode === 'navigate') {
    event.respondWith(
        fetch(event.request).catch(() => {
            return caches.match(OFFLINE_URL); // El mítico "offline.html"
        })
    );
}
```
**Lógica**: Esta pieza de código es el "seguro de vida" de la experiencia de usuario, garantizando que nunca vean el dinosaurio de Chrome, sino una página de marca profesional.

---

## 🔄 El Ciclo de Vida (Lifecycle)

### Instalación (`install`)
- Se abre la caché identificada por `CACHE_NAME` (vladimir-portfolio-vX).
- Se ejecuta `cache.addAll(ASSETS)` de forma atómica. Si un solo archivo falla, la instalación falla, evitando estados inconsistentes.
- `self.skipWaiting()`: Fuerza al nuevo Service Worker a tomar el control inmediatamente.

### Activación (`activate`)
- Implementa una lógica de **"Garbage Collection"**:
  - Filtra las claves de la caché.
  - Elimina cualquier caché que no coincida con la versión actual (`CACHE_NAME`).
  - `self.clients.claim()`: Permite al Service Worker empezar a interceptar peticiones sin esperar a que se recargue la página.

---

## 📏 Especificaciones Técnicas del Manifest (`manifest.webmanifest`)

- **`display: standalone`**: Elimina la barra de direcciones del navegador, haciendo que la web se comporte como una App nativa.
- **`background_color` & `theme_color`**: Coordinados con el diseño Glassmorphism de la web para una transición visual fluida durante el arranque.
- **Iconografía**: Uso de un formato SVG que permite escalabilidad infinita sin pérdida de calidad.

---

## ⚡ Rendimiento (Web Vitals)

- **LCP (Largest Contentful Paint)**: Optimizado mediante la precarga de la hero section en el Service Worker.
- **FID (First Input Delay)**: Minimizado al servir el JS principal desde la caché local instantáneamente.

---
*La PWA no es un extra; es la base de la disponibilidad técnica de este portafolio.*
