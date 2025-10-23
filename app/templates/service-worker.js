const CACHE_NAME = 'serviplus-v1';
const urlsToCache = [
  '/serviplus',
  '/static/js/manifest.json',
  '/static/img/icon-192.png',
  '/static/img/icon-512.png'
];

// Install Service Worker
self.addEventListener('install', (event) => {
  console.log('[SW] 🔧 Instalando Service Worker...');
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[SW] ✅ Cache abierto');
        return cache.addAll(urlsToCache).catch((err) => {
          console.error('[SW] ❌ Error al cachear archivos:', err);
          // No fallar si algunos archivos no existen (como los iconos)
        });
      })
  );
  
  self.skipWaiting();
});

// Activate Service Worker
self.addEventListener('activate', (event) => {
  console.log('[SW] 🚀 Activando Service Worker...');
  
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('[SW] 🗑️ Eliminando cache antiguo:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  
  self.clients.claim();
  console.log('[SW] ✅ Service Worker activado');
});

// Fetch - Network first, fallback to cache
self.addEventListener('fetch', (event) => {
  event.respondWith(
    fetch(event.request)
      .then((response) => {
        // Solo cachear respuestas exitosas
        if (response && response.status === 200) {
          const responseToCache = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseToCache);
          });
        }
        return response;
      })
      .catch(() => {
        // Si falla la red, buscar en cache
        return caches.match(event.request);
      })
  );
});

// Push Notifications
self.addEventListener('push', (event) => {
  console.log('[SW] 📬 Push recibido');
  
  const title = 'SERVI-PLUS';
  const options = {
    body: event.data ? event.data.text() : 'Tienes una nueva notificación',
    icon: '/static/img/icon-192.png',
    badge: '/static/img/icon-192.png',
    vibrate: [200, 100, 200],
    tag: 'serviplus-notification',
    requireInteraction: false,
    data: {
      url: '/serviplus'
    }
  };

  event.waitUntil(
    self.registration.showNotification(title, options)
  );
});

// Notification Click
self.addEventListener('notificationclick', (event) => {
  console.log('[SW] 👆 Notificación clickeada');
  event.notification.close();
  
  event.waitUntil(
    clients.openWindow('/serviplus')
  );
});

// Log de inicio
console.log('[SW] 📝 Service Worker cargado desde:', self.location.href);