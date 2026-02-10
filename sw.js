const CACHE_NAME = 'docs-v1';
const ASSETS = [
    './',
    './index.html',
    './assets/css/styles.css',
    './assets/js/app.js',
    'https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap',
    'https://cdn.jsdelivr.net/npm/marked/marked.min.js'
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS))
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request).then(response => {
            return response || fetch(event.request);
        })
    );
});
