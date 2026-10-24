/* Shared navigation usability helpers */
(function(){
  var menus=document.querySelectorAll('.gacc-2027-mobile-menu');
  if(!menus.length)return;
  document.addEventListener('click',function(e){
    menus.forEach(function(menu){if(menu.open&&!menu.contains(e.target))menu.open=false;});
  });
  document.addEventListener('keydown',function(e){
    if(e.key==='Escape')menus.forEach(function(menu){
      if(menu.open){menu.open=false;menu.querySelector('summary')?.focus();}
    });
  });
  window.addEventListener('resize',function(){
    if(window.innerWidth>1420)menus.forEach(function(menu){menu.open=false;});
  });
})();

/* GA4 engagement measurement. No completion is inferred from opening a third-party form. */
(function(){
  function track(name, detail){
    if(typeof window.gtag==='function') window.gtag('event',name,detail);
  }
  document.addEventListener('click',function(event){
    var target=event.target;
    if(!target || !target.closest) return;
    var link=target.closest('a[href]');
    if(!link) return;

    // The homepage modal already emits this event, so do not double-count it.
    if(link.hasAttribute('data-gacc-signup-open') &&
       !document.getElementById('gacc-signup-dialog')){
      track('email_signup_open',{
        source:'site_navigation',
        page_path:location.pathname
      });
    }

    // This page previously had no dealer PDF/contact engagement measurement.
    if(/(?:^|\/)dealer-hub\.html$/.test(location.pathname)){
      var destination;
      try { destination=new URL(link.href,location.href); }catch(_){return;}
      if(/\.pdf$/i.test(destination.pathname)){
        track('dealer_pdf_download',{
          file_name:decodeURIComponent(destination.pathname.split('/').pop()),
          link_url:destination.href
        });
      }else if(destination.protocol==='mailto:' || destination.protocol==='tel:'){
        track('contact_click',{
          contact_type:destination.protocol.slice(0,-1),
          page_path:location.pathname
        });
      }
    }
  });
})();
