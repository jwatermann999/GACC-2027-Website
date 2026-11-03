/* Preview protection: never allow test submissions to reach an active form handler.
   Intentional external sponsor and partner links remain functional. */
(function() {
  document.addEventListener('submit', function(event) {
    event.preventDefault();
    event.stopImmediatePropagation();
    window.alert('This is a design preview. No information was submitted. Please use the live GACC website for real requests.');
  }, true);
})();
