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

// Assuming you are using JavaScript to handle page loading
document.addEventListener('DOMContentLoaded', (event) => {
    let deferredPrompt;
  
    window.addEventListener('beforeinstallprompt', (e) => {
      // Prevent the mini-infobar from appearing on mobile
      e.preventDefault();
  
      // Stash the event so it can be triggered later
      deferredPrompt = e;
  
      // Update UI notify the user they can install the PWA
      // You can use a button, link, or any UI element
      // For example:
      // showInstallButton();
    });
  
    // Optionally, you can add an event listener to a button or element
    // to trigger the install prompt
    // document.getElementById('installButton').addEventListener('click', (e) => {
    //   deferredPrompt.prompt();
    //   deferredPrompt.userChoice.then((choiceResult) => {
    //     if (choiceResult.outcome === 'accepted') {
    //       console.log('User accepted the install prompt');
    //     }
    //     deferredPrompt = null;
    //   });
    // });
  });