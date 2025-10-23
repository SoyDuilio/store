const CACHE_NAME = 'serviplus-v2';
const urlsToCache = [
  '/serviplus',
  '/static/js/manifest.json',
  '/static/img/icon-192.png',
  '/static/img/icon-512.png'
];

// ==================== INSTALL ====================
self.addEventListener('install', (event) => {
  console.log('[SW] 🔧 Instalando Service Worker v2...');
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[SW] ✅ Cache abierto:', CACHE_NAME);
        return cache.addAll(urlsToCache).catch((err) => {
          console.error('[SW] ❌ Error al cachear archivos:', err);
        });
      })
  );
  
  self.skipWaiting();
});

// ==================== ACTIVATE ====================
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
  console.log('[SW] ✅ Service Worker activado y en control');
});

// ==================== FETCH ====================
self.addEventListener('fetch', (event) => {
  event.respondWith(
    fetch(event.request)
      .then((response) => {
        if (response && response.status === 200) {
          const responseToCache = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseToCache);
          });
        }
        return response;
      })
      .catch(() => {
        return caches.match(event.request);
      })
  );
});

// ==================== PUSH NOTIFICATIONS ====================
self.addEventListener('push', (event) => {
  console.log('[SW] 📬 Push notification recibida');
  
  let notificationData = {
    title: 'SERVI-PLUS',
    body: 'Tienes una nueva notificación',
    icon: '/static/img/icon-192.png',
    badge: '/static/img/icon-192.png'
  };
  
  if (event.data) {
    try {
      notificationData = event.data.json();
    } catch (e) {
      notificationData.body = event.data.text();
    }
  }
  
  const options = {
    body: notificationData.body || 'Nueva notificación de SERVI-PLUS',
    icon: notificationData.icon || '/static/img/icon-192.png',
    badge: notificationData.badge || '/static/img/icon-192.png',
    image: notificationData.image,
    vibrate: notificationData.vibrate || [200, 100, 200],
    tag: notificationData.tag || 'serviplus-notification',
    requireInteraction: notificationData.requireInteraction || false,
    actions: notificationData.actions || [],
    data: notificationData.data || {}
  };

  event.waitUntil(
    self.registration.showNotification(notificationData.title || 'SERVI-PLUS', options)
  );
});

// ==================== NOTIFICATION CLICK ====================
self.addEventListener('notificationclick', (event) => {
  console.log('[SW] 👆 Notificación clickeada');
  console.log('[SW] Acción:', event.action);
  console.log('[SW] Datos:', event.notification.data);
  
  event.notification.close();
  
  const action = event.action;
  const data = event.notification.data || {};
  
  let targetUrl = '/serviplus';
  
  if (action === 'ver-detalles' || action === 'ver') {
    if (data.servicio_id) {
      targetUrl = `/serviplus?servicio=${data.servicio_id}`;
    } else {
      targetUrl = '/serviplus?action=servicios';
    }
  } else if (action === 'chat') {
    if (data.profesional_id) {
      targetUrl = `/serviplus?action=chat&profesional=${data.profesional_id}`;
    } else {
      targetUrl = '/serviplus?action=mensajes';
    }
  } else if (action === 'tracking') {
    if (data.servicio_id) {
      targetUrl = `/serviplus?action=tracking&servicio=${data.servicio_id}`;
    }
  } else if (action === 'ignorar' || action === 'dismiss') {
    console.log('[SW] Usuario ignoró la notificación');
    return;
  } else {
    if (data.url) {
      targetUrl = data.url;
    } else if (data.servicio_id) {
      targetUrl = `/serviplus?servicio=${data.servicio_id}`;
    }
  }
  
  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true })
      .then((clientList) => {
        for (let client of clientList) {
          if (client.url.includes('/serviplus') && 'focus' in client) {
            return client.focus().then(() => {
              if ('navigate' in client) {
                return client.navigate(targetUrl);
              }
            });
          }
        }
        
        if (clients.openWindow) {
          return clients.openWindow(targetUrl);
        }
      })
  );
});

// ==================== NOTIFICATION CLOSE ====================
self.addEventListener('notificationclose', (event) => {
  console.log('[SW] 🔕 Notificación cerrada sin interacción');
});

console.log('[SW] 📝 Service Worker v2 cargado desde:', self.location.href);