// Salas por internet con PeerJS (WebRTC), versión 2.
// Cada sala tiene 3 "lugares" de anfitrión: CODIGO, CODIGO-1 y CODIGO-2. Al entrar se prueba el primero:
//  · si alguien contesta, se entra como invitado;
//  · si nadie tiene ese lugar, uno se vuelve el anfitrión;
//  · si el lugar está ocupado por alguien que no contesta (por ejemplo un celular con la pantalla apagada), se prueba el siguiente.
// Todos mandan una señal de vida cada 2 s; a quien deja de mandarla se le quita (así no quedan peluches "fantasma" quietos).
// Un anfitrión en un lugar de atrás revisa de vez en cuando si el de adelante volvió, para que todos terminen juntos.
function makePeerNet(PREFIX){
  if(typeof Peer!=='function') return null;
  const ICE={config:{iceServers:[
    {urls:['stun:stun.l.google.com:19302','stun:stun1.l.google.com:19302']},
    {urls:'stun:global.stun.twilio.com:3478'},
    {urls:['turn:openrelay.metered.ca:80','turn:openrelay.metered.ca:443','turn:openrelay.metered.ca:443?transport=tcp'], username:'openrelayproject', credential:'openrelayproject'}
  ]}, debug:0};
  const SLOTS=3, HB=2000, DEAD=9000, OPEN_WAIT=5000, PROBE=12000;
  const randId=()=>{ const a=new Uint32Array(3); crypto.getRandomValues(a); return PREFIX+'p-'+[...a].map(v=>v.toString(36)).join(''); };
  function merge(base, patch){ const o={...(base||{})}; for(const k in patch){ if(patch[k]===null) delete o[k]; else o[k]=patch[k]; } return o; }
  function join(code){
    const base=PREFIX+String(code).replace(/[^A-Za-z0-9_-]/g,''), slotId=k=>k?base+'-'+k:base;
    const peersH=new Set(), connH=new Set();
    let closed=false, connected=false, notifyT=0, retryT=0, hbT=0, probeT=0, gen=0;
    let me=null, myId='', isHost=false, slot=-1, hostConn=null, hostSeen=0;
    const clients=new Map(), seen=new Map(), pres=new Map(); let myPres={};
    let firstDone=null, firstFail=null; const ready=new Promise((res,rej)=>{ firstDone=res; firstFail=rej; });
    const setConn=c=>{ if(c===connected) return; connected=c; connH.forEach(h=>{ try{h(c);}catch(e){} }); };
    const list=()=>{ const out=[]; if(myId) out.push({peer:myId, kind:'viewer', sameTab:true, presence:myPres});
      for(const [id,p] of pres) if(id!==myId) out.push({peer:id, kind:'viewer', presence:p}); return out; };
    const notify=()=>{ if(notifyT) return; notifyT=setTimeout(()=>{ notifyT=0; const ps=list(); peersH.forEach(h=>{ try{h({peers:ps});}catch(e){} }); },0); };
    const sendAll=(msg, except)=>{ for(const [id,c] of clients) if(id!==except && c.open){ try{ c.send(msg); }catch(e){} } };
    function stopAll(){
      gen++; clearInterval(hbT); clearInterval(probeT); clearTimeout(retryT); hbT=probeT=0;
      clients.forEach(c=>{ try{c.close();}catch(e){} }); clients.clear(); seen.clear();
      if(hostConn){ try{hostConn.close();}catch(e){} } hostConn=null;
      if(me){ try{ me.destroy(); }catch(e){} } me=null; isHost=false; slot=-1; pres.clear(); notify();
    }
    function restart(ms){ if(closed) return; setConn(false); stopAll(); const g=gen; retryT=setTimeout(()=>{ if(g===gen) tryClient(0); }, ms); }
    // quita a un invitado (se fue o dejó de mandar señal)
    function drop(id){ const c=clients.get(id); if(c){ clients.delete(id); try{c.close();}catch(e){} } seen.delete(id);
      if(pres.delete(id)){ sendAll({t:'x', id}); notify(); } }
    // ---- Invitado: probar el lugar k ----
    function tryClient(k,bounces=0){
      if(closed) return;
      if(bounces>=2){ k++; bounces=0; }      // ese lugar dice estar ocupado pero no contesta: probar el siguiente
      if(k>=SLOTS){ restart(1500+Math.random()*1500); return; }
      stopAll(); const g=gen;
      const p=new Peer(randId(), ICE); me=p;
      let decided=false;
      const giveUp=next=>{ if(decided||g!==gen) return; decided=true; next(); };
      p.on('open', id=>{ if(g!==gen) return; myId=id;
        const c=p.connect(slotId(k), {reliable:true});
        const to=setTimeout(()=>giveUp(()=>tryClient(k+1)), OPEN_WAIT);     // ocupado pero no contesta → siguiente lugar
        c.on('open', ()=>{ if(g!==gen) return; clearTimeout(to); decided=true; hostConn=c; slot=k; hostSeen=Date.now(); setConn(true);
          try{ c.send({t:'u', pr:myPres}); }catch(e){}
          hbT=setInterval(()=>{ if(g!==gen) return; if(Date.now()-hostSeen>DEAD){ restart(200+Math.random()*800); return; } try{ c.send({t:'hb'}); }catch(e){} }, HB);
          firstDone(); });
        c.on('data', m=>{ if(g!==gen || !m) return; hostSeen=Date.now();
          if(m.t==='init'){ pres.clear(); for(const kk in m.peers) if(kk!==myId) pres.set(kk, m.peers[kk]); notify(); }
          else if(m.t==='u' && m.id!==myId){ pres.set(m.id, m.pr); notify(); }
          else if(m.t==='x'){ pres.delete(m.id); notify(); }
          else if(m.t==='bye' && hostConn===c){ restart(300+Math.random()*600); } });
        const lost=()=>{ if(g!==gen) return; if(hostConn===c){ restart(300+Math.random()*1200); } else { clearTimeout(to); giveUp(()=>tryClient(k+1)); } };
        c.on('close', lost); c.on('error', lost);
      });
      p.on('error', e=>{ if(g!==gen) return;
        if(e.type==='peer-unavailable'){ giveUp(()=>tryHost(k,bounces)); return; }   // nadie tiene ese lugar → ser el anfitrión
        if(e.type==='browser-incompatible'){ firstFail({code:'not_permitted'}); return; }
        if(!decided){ decided=true; restart(2500); } else if(!hostConn) restart(2500);
      });
    }
    // ---- Anfitrión del lugar k ----
    function tryHost(k,bounces=0){
      if(closed) return;
      stopAll(); const g=gen;
      const p=new Peer(slotId(k), ICE); me=p; let opened=false;
      p.on('open', id=>{ if(g!==gen) return; opened=true; myId=id; isHost=true; slot=k; pres.clear(); setConn(true); notify(); firstDone();
        hbT=setInterval(()=>{ if(g!==gen) return; const now=Date.now(); sendAll({t:'hb'});
          for(const [cid,t] of seen) if(now-t>DEAD) drop(cid); }, HB);
        if(k>0) probeT=setInterval(()=>probeLower(g), PROBE);
      });
      p.on('connection', c=>{
        c.on('open', ()=>{ if(g!==gen){ try{c.close();}catch(e){} return; } clients.set(c.peer,c); seen.set(c.peer,Date.now());
          c.send({t:'init', peers:Object.fromEntries([[myId,myPres], ...pres])}); });
        c.on('data', m=>{ if(g!==gen || !m) return; seen.set(c.peer,Date.now());
          if(m.t!=='u' || typeof m.pr!=='object') return;
          const np=merge(pres.get(c.peer), m.pr);
          // el mismo jugador con otra conexión (recargó o se reconectó): quitar la vieja
          if(np.id) for(const [oid,op] of pres) if(oid!==c.peer && op && op.id===np.id) drop(oid);
          pres.set(c.peer,np); sendAll({t:'u', id:c.peer, pr:np}, c.peer); notify(); });
        const gone=()=>{ if(g===gen && clients.get(c.peer)===c) drop(c.peer); };
        c.on('close', gone); c.on('error', gone);
      });
      p.on('error', e=>{ if(g!==gen) return;
        if(!opened && e.type==='unavailable-id'){ setTimeout(()=>{ if(g===gen) tryClient(k,bounces+1); }, 300+Math.random()*500); return; }   // alguien lo tomó primero
        if(e.type==='browser-incompatible'){ firstFail({code:'not_permitted'}); return; }
        if(e.type==='peer-unavailable') return;          // un sondeo a otro lugar que no existe
        restart(2500+Math.random()*1500);
      });
      p.on('disconnected', ()=>{ if(g===gen && me===p){ try{ p.reconnect(); }catch(e){ restart(2000); } } });
    }
    // Anfitrión de un lugar de atrás: si el de adelante ya contesta, nos vamos allá (los invitados nos siguen solos)
    function probeLower(g){
      if(g!==gen || !me || !isHost) return;
      for(let j=0;j<slot;j++){ const c=me.connect(slotId(j),{reliable:true}); const to=setTimeout(()=>{ try{c.close();}catch(e){} }, OPEN_WAIT);
        c.on('open', ()=>{ clearTimeout(to); try{c.close();}catch(e){} if(g===gen && isHost && j<slot){ sendAll({t:'bye'}); setTimeout(()=>{ if(g===gen) tryClient(0); }, 150); } }); }
    }
    tryClient(0);
    const timeout=setTimeout(()=>firstFail({code:'timeout'}), 25000);
    addEventListener('pagehide', ()=>{ closed=true; stopAll(); });
    const room={
      code,
      presence(patch){ myPres=merge(myPres, patch);
        if(isHost) sendAll({t:'u', id:myId, pr:myPres});
        else if(hostConn && hostConn.open){ try{ hostConn.send({t:'u', pr:patch}); }catch(e){ return Promise.reject({code:'error'}); } }
        notify(); return Promise.resolve(); },
      peers:()=>list(),
      onPeers(h){ peersH.add(h); return ()=>peersH.delete(h); },
      onConnection(h){ connH.add(h); return ()=>connH.delete(h); },
      connected:()=>connected,
      async leave(){ closed=true; clearTimeout(timeout); stopAll(); },
      get isHost(){ return isHost; }, get slot(){ return slot; }
    };
    room.lobby=room;
    return ready.then(()=>{ clearTimeout(timeout); return room; }, e=>{ closed=true; stopAll(); throw e; });
  }
  return { join };
}
const peerNet = makePeerNet('mundopeluche-v1-');
