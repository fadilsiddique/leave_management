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


  self.addEventListener('DOMContentLoaded', (event) => {
    let deferredPrompt;
  
    window.addEventListener('beforeinstallprompt', (e) => {
      // Prevent the mini-infobar from appearing on mobile
      e.preventDefault();
  
      // Stash the event so it can be triggered later
      deferredPrompt = e;
  
      // Show a button or UI element to indicate the user can install the PWA
      showInstallButton();
    });
  
    function showInstallButton() {
      // Display an install button
      let installButton = document.createElement('button');
      installButton.textContent = 'Install App';
      installButton.addEventListener('click', (e) => {
        // Trigger the install prompt
        deferredPrompt.prompt();
  
        // Wait for the user to respond to the prompt
        deferredPrompt.userChoice.then((choiceResult) => {
          if (choiceResult.outcome === 'accepted') {
            console.log('User accepted the install prompt');
          }
          deferredPrompt = null;
        });
      });
  
      // Add the install button to your UI
      self.body.appendChild(installButton);
    }
  });
  