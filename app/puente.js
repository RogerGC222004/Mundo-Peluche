// Puente entre el juego y Android (solo funciona dentro de la app; en la web no hace nada).
// - Anuncios con premio de AdMob para los botones ▶ del juego (window.MundoAds).
//   Configuración para niños y familias: contenido apto para todos (G), sin anuncios personalizados.
// - Botón "atrás" de Android: cierra lo que esté abierto, pausa el juego o minimiza la app desde el menú.
(function(){
  var C=window.Capacitor; if(!C || !C.isNativePlatform || !C.isNativePlatform()) return;
  var CFG=window.__MP_APP||{};
  var P=function(n){ return (C.Plugins && C.Plugins[n]) || (C.registerPlugin ? C.registerPlugin(n) : null); };
  var AdMob=P('AdMob'), App=P('App');

  // ---------- privacidad (v253) ----------
  // Herramienta de privacidad de Google (UMP, certificada para Europa y Reino Unido). El juego está marcado para menores de la edad de
  // consentimiento: así Google NO le pregunta nada al jugador y solo hay anuncios no personalizados. Se revisa cada vez que se abre la app,
  // antes de pedir anuncios. Si Google dice que hace falta, el juego muestra «Opciones de privacidad de anuncios» en Para papás.
  var priv={need:false, status:'', canAds:true, done:false};
  function privUpd(i){ if(i){ priv.status=String(i.status||''); priv.need=i.privacyOptionsRequirementStatus==='REQUIRED'; priv.canAds=i.canRequestAds!==false; } priv.done=true; return i; }
  function consent(){ return AdMob.requestConsentInfo({tagForUnderAgeOfConsent:true}).then(privUpd)
    .then(function(i){ return i && i.status==='REQUIRED' && i.isConsentFormAvailable ? AdMob.showConsentForm().then(privUpd) : i; })
    .catch(function(){ priv.done=true; return null; }); }   // (si falla, se sigue: los anuncios ya van marcados para niños y sin personalizar)

  // ---------- anuncios ----------
  var ready=null;
  function init(){ if(!ready) ready=consent().then(function(){ return AdMob.initialize({tagForChildDirectedTreatment:true, tagForUnderAgeOfConsent:true, maxAdContentRating:'General', initializeForTesting:!!CFG.pruebas}); })
    .catch(function(e){ ready=null; throw e; }); return ready; }
  if(AdMob && !CFG.pruebas){   // v178: con anuncios de prueba no se usa AdMob (el juego muestra su propio "ratito de juego")
    setTimeout(function(){ init().catch(function(){}); },4000);   // se prepara solo, sin estorbar la carga
    window.MundoPriv={ get need(){ return priv.need; }, get status(){ return priv.status; }, get done(){ return priv.done; },
      open:function(){ return AdMob.showPrivacyOptionsForm().then(consent); } };
    window.MundoAds={ show:function(){ return new Promise(function(res){
      var got=false, done=false, hs=[];
      function fin(v){ if(done) return; done=true; hs.forEach(function(h){ Promise.resolve(h).then(function(x){ try{ x.remove(); }catch(e){} }); }); res(v); }
      function on(ev,f){ hs.push(AdMob.addListener(ev,f)); }
      on('onRewardedVideoAdReward',function(){ got=true; });
      on('onRewardedVideoAdDismissed',function(){ setTimeout(function(){ fin(got); },400); });
      on('onRewardedVideoAdFailedToShow',function(){ fin(false); });
      on('onRewardedVideoAdFailedToLoad',function(){ fin(false); });
      init().then(function(){ if(!priv.canAds) throw new Error('sin permiso'); return AdMob.prepareRewardVideoAd({adId:CFG.premio, isTesting:!!CFG.pruebas, npa:true}); })
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
