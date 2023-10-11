// var cacheName = 'leave-mgt';
// console.log(cacheName)


// self.addEventListener('install', event => {
//     event.waitUntil(
//       caches.open(cacheName).then(cache => {
//         return cache.addAll([
//           '/',
//           '/manifest.webmanifest',
//           '/assets/frappe/css/bootstrap.css',
//           '/assets/frappe/js/bootstrap-4-web.bundle.js',
//           '/assets/frappe/js/jquery-bootstrap.js',
//           '/assets/frappe/js/frappe-web.bundle.js'
          
//         ]);
//       })
//     );
//   });
  
//   self.addEventListener('fetch', event => {
//     event.respondWith(
//       caches.match(event.request).then(response => {
//         return response || fetch(event.request);
//       })
//     );
//   });
