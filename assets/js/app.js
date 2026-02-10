const CONFIG = {
    docsPath: 'docs/',
    wikiPath: 'wiki/',
    defaultFile: 'README.md'
};

const elements = {
    content: document.getElementById('content'),
    navLinks: document.querySelectorAll('.nav-link')
};

async function loadMarkdown(path) {
    try {
        elements.content.innerHTML = '<div class="loading">Cargando documentación...</div>';
        const response = await fetch(path);
        if (!response.ok) throw new Error('Archivo no encontrado');

        const markdown = await response.text();
        const html = marked.parse(markdown);

        elements.content.innerHTML = html;
        window.scrollTo(0, 0);
        updateActiveLink(path);
    } catch (error) {
        elements.content.innerHTML = `
            <div class="error">
                <h2>Opps! Error al cargar</h2>
                <p>${error.message}</p>
                <a href="#README.md" class="btn">Volver al inicio</a>
            </div>
        `;
    }
}

function updateActiveLink(path) {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${path}`) {
            link.classList.add('active');
        }
    });
}

function handleRoute() {
    const hash = window.location.hash.substring(1) || CONFIG.defaultFile;
    loadMarkdown(hash);
}

window.addEventListener('hashchange', handleRoute);
window.addEventListener('load', handleRoute);

// Service Worker Registration
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js').then(reg => {
            console.log('SW registrado');
        }).catch(err => {
            console.error('SW fallo', err);
        });
    });
}
