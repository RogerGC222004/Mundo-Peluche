// Puente entre el juego y Android (solo funciona dentro de la app; en la web no hace nada).
// - Anuncios con premio de AdMob para los botones ▶ del juego (window.MundoAds).
//   Configuración para niños y familias: contenido apto para todos (G), sin anuncios personalizados.
// - Botón "atrás" de Android: cierra lo que esté abierto, pausa el juego o minimiza la app desde el menú.
(function(){
  var C=window.Capacitor; if(!C || !C.isNativePlatform || !C.isNativePlatform()) return;
  var CFG=window.__MP_APP||{};
  var P=function(n){ return (C.Plugins && C.Plugins[n]) || (C.registerPlugin ? C.registerPlugin(n) : null); };
  var AdMob=P('AdMob'), App=P('App');

  // ---------- anuncios ----------
  var ready=null;
  function init(){ if(!ready) ready=AdMob.initialize({tagForChildDirectedTreatment:true, tagForUnderAgeOfConsent:true, maxAdContentRating:'General', initializeForTesting:!!CFG.pruebas})
    .catch(function(e){ ready=null; throw e; }); return ready; }
  if(AdMob){
    setTimeout(function(){ init().catch(function(){}); },4000);   // se prepara solo, sin estorbar la carga
    window.MundoAds={ show:function(){ return new Promise(function(res){
      var got=false, done=false, hs=[];
      function fin(v){ if(done) return; done=true; hs.forEach(function(h){ Promise.resolve(h).then(function(x){ try{ x.remove(); }catch(e){} }); }); res(v); }
      function on(ev,f){ hs.push(AdMob.addListener(ev,f)); }
      on('onRewardedVideoAdReward',function(){ got=true; });
      on('onRewardedVideoAdDismissed',function(){ setTimeout(function(){ fin(got); },400); });
      on('onRewardedVideoAdFailedToShow',function(){ fin(false); });
      on('onRewardedVideoAdFailedToLoad',function(){ fin(false); });
      init().then(function(){ return AdMob.prepareRewardVideoAd({adId:CFG.premio, isTesting:!!CFG.pruebas, npa:true}); })
        .then(function(){ return AdMob.showRewardVideoAd(); })
        .then(function(r){ if(r && (r.amount!=null || r.type!=null)) got=true; })
        .catch(function(){ fin(false); });
      setTimeout(function(){ fin(got); },180000);   // por si nunca avisa
    }); } };
  }

  // ---------- botón atrás ----------
  // el juego decide (window.mundoAtras): cierra lo abierto o pausa; si ya estás en el menú, la app se minimiza
  if(App) App.addListener('backButton',function(){
    var handled=false; try{ handled=!!(window.mundoAtras && window.mundoAtras()); }catch(e){}
    if(!handled && App.minimizeApp) App.minimizeApp();
  });
})();
