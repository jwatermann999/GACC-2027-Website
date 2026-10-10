// GACC app service worker. Network-first, no offline caching of dealer forms or prices.
self.addEventListener('install', event => self.skipWaiting());
self.addEventListener('activate', event => event.waitUntil(self.clients.claim()));
self.addEventListener('fetch', event => { /* Keep content live and current. */ });
