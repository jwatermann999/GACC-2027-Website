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