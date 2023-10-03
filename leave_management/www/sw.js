var cacheName = 'leave-mgt';

self.addEventListener('install', event => {
    console.log("hellleleo")
    event.waitUntil(
      caches.open(cacheName).then(cache => {
        return cache.addAll([
          '/',
          '/index.html',
          '/manifest.webmanifest',
          '/app',

    
        ]);
      })
    );
  });
  
  self.addEventListener('fetch', event => {
    console.log(event)
    event.respondWith(
      caches.match(event.request).then(response => {
        return response || fetch(event.request);
      })
    );
  });