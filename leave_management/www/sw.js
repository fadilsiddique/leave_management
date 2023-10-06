var cacheName = 'leave-mgt';
console.log(cacheName)


self.addEventListener('install', event => {
    console.log("hellleleo")
    event.waitUntil(
      caches.open(cacheName).then(cache => {
        return cache.addAll([
          '/',
          '/app',
          '/index',
          '/app/admin-portal',
          '/manifest.webmanifest',
          '/website_script.js',
          '/login'
          
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
