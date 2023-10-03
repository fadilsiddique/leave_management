var cacheName = 'leave-mgt';

self.addEventListener('install', event => {
    event.waitUntil(
      caches.open(cacheName).then(cache => {
        return cache.addAll([
          '/',
          '/index.html',
          '/public/manifest.json'
    
        ]);
      })
    );
  });
  
  self.addEventListener('fetch', event => {
    event.respondWith(
      caches.match(event.request).then(response => {
        return response || fetch(event.request);
      })
    );
  });