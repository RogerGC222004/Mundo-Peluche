
// ---------- Generador del relieve (no va en el juego: corre una vez y escribe RL_DATA) ----------
const rlRidge=(x,z,o=4)=>{ let s=0, a=.5, f=1, w=0; for(let i=0;i<o;i++){ const n=1-Math.abs(2*rlNoise(x*f+i*31.7,z*f+i*7.9)-1); s+=a*n*n; w+=a; a*=.5; f*=2.1; } return s/w; };
// montañas: [ángulo, radio, base, altura, tipo] (tipo 1 = nevada, 0 = verde)
const RL_PEAKS=[
  // cordillera nevada del sur (con un paso en medio, hacia la playa de Papa caliente)
  [-2.13,905,150,195,1],[-1.97,870,165,248,1],[-1.82,935,140,182,1],[-1.36,880,150,212,1],[-1.21,925,170,262,1],[-1.07,875,135,176,1],
  [-2.05,760,95,92,1],[-1.88,785,90,84,1],[-1.30,770,95,96,1],[-1.15,790,85,80,1],[-1.62,980,120,120,1],[-1.50,985,110,104,1],
  // montañas verdes del norte
  [1.08,860,140,118,0],[1.27,800,120,92,0],[1.50,880,150,128,0],[1.72,830,130,104,0],[1.93,900,140,116,0],[1.62,1010,110,84,0],
  // montañas verdes del oeste
  [2.95,860,140,112,0],[3.12,930,150,132,0],[-3.05,870,140,118,0],[-2.92,960,120,96,0],[3.02,760,90,64,0]
].map(([a,r,R,h,t])=>{ const [x,z]=polar(a,r); return {x,z,R,h,t}; });
// cañones y sus recovecos: puntos [ángulo, radio]
const RL_CANYONS=[
  {pts:[[.10,600],[.16,700],[.13,780],[.21,860],[.18,940],[.24,1040]], w:11},
  {pts:[[.52,610],[.45,690],[.50,760],[.40,830],[.44,900],[.36,960],[.40,1050]], w:10},
  {pts:[[.21,860],[.31,840],[.40,830]], w:8}
].map(c=>({w:c.w, pts:c.pts.map(([a,r])=>polar(a,r))}));
const RL_POCKETS=[[.155,705,9],[.205,850,10],[.47,700,8],[.42,905,9],[.31,842,11],[.225,1000,8]].map(([a,r,R])=>{ const [x,z]=polar(a,r); return {x,z,R}; });
const RL_CAN=RL_CANYONS.map(c=>({...rlLine(rlSpline(c.pts,4)), w:c.w}));
// ---- lo que no se toca (llanos de los lugares) ----
const RL_KEEP=[[0,0,45,100],[PG.x,PG.z,PG.R+10,PG.R+48],[LAKE.x,LAKE.z,LAKE.R+12,LAKE.R+46],[452,0,45,95],[-203,-33,22,60],[24,-88,22,55],
  [55,-45,25,70],[170,170,28,75],[-260,60,26,72],[431,-301,25,70],[-500,-17,27,72],[409,380,24,68],
  // playas de la costa nueva: juegos de la arena, muelle, el cuco y el cohete
  ...[[1.37,-10,45,95],[4.71,-40,52,100],[3.93,-10,45,95],[.15,-10,45,95],[5.38,-15,42,88],[5.5,-16,26,62],[.72,-50,30,72]].map(([a,off,r0,r1])=>{ const r=COAST_X*coastRN(a)+off; return [Math.cos(a)*r, Math.sin(a)*r, r0, r1]; })];
function rlAirCorr(x,z){ const [u,v]=airportUV(x,z), du=Math.max(-90-u,0), dv=Math.max(Math.abs(v+55)-125,0); return 1-smooth(0,45,Math.hypot(du,dv)); }   // aeropuerto y su pasillo hasta el mar
function rlKeep(x,z){ let k=Math.max(airportFlat(x,z), rlAirCorr(x,z), fairFlat(x,z));
  for(const [cx,cz,r0,r1] of RL_KEEP){ const dx=x-cx, dz=z-cz; if(Math.abs(dx)>r1||Math.abs(dz)>r1) continue; k=Math.max(k,1-smooth(r0,r1,Math.hypot(dx,dz))); }
  const d=Math.hypot(x,z), a=Math.atan2(z,x), td=Math.abs(d-trackRadius(a)); k=Math.max(k,1-smooth(TRACK_W/2+10,TRACK_W/2+42,td));   // la pista
  return k; }
// ---- el relieve natural (sin río) ----
function rlNatural(x,z){ const d=Math.hypot(x,z), a=Math.atan2(z,x), cN=d/coastRN(a);
  const coastFade=1-smooth(.8,.95,cN);
  if(coastFade<=0 && cN>1) return 0;
  const keep=rlKeep(x,z), rt=trackRadius(a);
  const out=smooth(rt+45,rt+175,d);   // afuera de la pista empieza lo nuevo
  // adentro: ondulación suave (la isla de antes ya tiene sus cerros)
  let h=(1-out)*Math.max(0,rlFbm(x/75,z/75,3)-.4)*11*smooth(60,120,d);
  if(out>0){
    let hh=Math.max(1.5,7+(rlFbm(x/230+40,z/230,4)-.5)*30+(rlNoise(x/70,z/70)-.5)*7);   // colinas y valles
    let mt=0;
    for(const P of RL_PEAKS){ const dx=x-P.x, dz=z-P.z; if(Math.abs(dx)>P.R*2.2||Math.abs(dz)>P.R*2.2) continue; const q=(dx*dx+dz*dz)/(P.R*P.R);
      const m=P.h*Math.exp(-q*1.7)*(.72+.5*rlRidge(x/(P.R*.55)+P.x*.01,z/(P.R*.55)))*(1+(rlNoise(x/38,z/38)-.5)*.12*Math.exp(-q));
      mt=Math.max(mt,m)+Math.min(mt,m)*.25; }
    // meseta del este
    const M=RL_MESA, mk=rlMesaK(x,z);
    if(mk>0) hh=Math.max(hh, hh*(1-mk)+(M.h+(rlFbm(x/60,z/60,3)-.5)*8)*mk);
    // terraza alta del río que termina en el acantilado curvo de la cascada
    { const F=RL_FALL, dx=x-F.x, dz=z-F.z, up=-(dx*F.nx+dz*F.nz), lat=Math.abs(-dx*F.nz+dz*F.nx);
      const cx=F.x-F.nx*260, cz=F.z-F.nz*260, rr=Math.hypot(x-cx,z-cz);
      const m=(1-smooth(-3,3,rr-260+(rlNoise(x/12,z/12)-.5)*6))*(1-smooth(150,240,lat))*(1-smooth(380,560,up));
      if(m>0) hh+=F.h*m; }
    h+=out*(hh+mt);
    // cañones (cortan la meseta y lo que encuentren)
    if(mk>0){ let floor=1e9; for(const C of RL_CAN){ const n=C.near(x,z); if(n.d<C.w+30){ const f=5.5+(rlNoise(x/18,z/18)-.5)*1.2+Math.pow(smooth(C.w*.55,C.w+9+(rlNoise(x/14,z/14)-.5)*6,n.d),1.5)*60; floor=Math.min(floor,f); } }
      for(const K of RL_POCKETS){ const pd=Math.hypot(x-K.x,z-K.z); if(pd<K.R+20) floor=Math.min(floor,5.5+Math.pow(smooth(K.R*.6,K.R+8,pd),1.5)*60); }
      if(floor<h) h=floor; }
  }
  let r=h*(1-keep)*coastFade;
  for(const P of RL_SEAPONDS){ const pd=Math.hypot(x-P.x,z-P.z); if(pd>P.R+12) continue; const b=pd<P.R ? SEA_Y-2.2*(1-(pd/P.R)*(pd/P.R)) : SEA_Y+(pd-P.R)*.35; if(b<r) r=b; }
  return r; }
// ---- el río: su fondo baja siempre (se calcula de lo que hay alrededor) ----
const RL_BED=(()=>{ const P=RL_RIVER.pts, L=RL_RIVER.L, n=P.length, bed=new Float32Array(n);
  let m=1e9; for(let i=0;i<n;i++){ const [x,z]=P[i], dd=Math.hypot(x,z), cN=dd/coastRN(Math.atan2(z,x)), nat=rlNatural(x,z)+shoreBaseN(cN); m=Math.min(m,nat-2.6); bed[i]=m; }
  for(let i=n-1;i>=0;i--){ bed[i]=Math.max(bed[i], SEA_Y-.75); if(L[n-1]-L[i]<1) bed[i]=SEA_Y-.75; }
  for(let i=1;i<n;i++) if(bed[i]>bed[i-1]) bed[i]=bed[i-1];
  // la cascada: el fondo cae de golpe (en un solo tramo de ~4 m), así el agua cae libre
  { let i0=-1; for(let i=1;i<n;i++) if((bed[i-1]-bed[i])/(L[i]-L[i-1])>1){ i0=i; break; }
    if(i0>0){ let ib=i0; while(ib<n-1 && (bed[ib]-bed[ib+1])/(L[ib+1]-L[ib])>.2) ib++; for(let k=i0;k<ib;k++) bed[k]=bed[ib]; } }
  for(let i=0;i<n;i++) bed[i]=Math.round(bed[i]*100)/100;
  return bed; })();
function rlBedAt(s){ const L=RL_RIVER.L, n=L.length; let lo=0, hi=n-1; while(hi-lo>1){ const m=(lo+hi)>>1; if(L[m]<=s) lo=m; else hi=m; } const t=(s-L[lo])/Math.max(1e-6,L[hi]-L[lo]); return RL_BED[lo]+(RL_BED[hi]-RL_BED[lo])*t; }
const RL_POND=(()=>{ const [x,z]=RL_RIVER.pts[0]; return {x,z,R:17, bed:RL_BED[0]}; })();
// poza al pie de la cascada (donde el fondo deja de caer en picada)
const RL_PLUNGE=(()=>{ const B=RL_BED, L=RL_RIVER.L; let i0=-1; for(let i=1;i<B.length;i++){ if((B[i-1]-B[i])/(L[i]-L[i-1])>1){ i0=i; } else if(i0>0) break; }
  let i=i0; while(i<B.length-1 && (B[i]-B[i+1])/(L[i+1]-L[i])>.2) i++; const base=B[i]; let j=i; while(j<B.length-1 && L[j]-L[i]<7) j++;
  const [x,z]=RL_RIVER.pts[j]; return {x,z,R:12, lvl:base+.75, bottom:base-2.0, s:L[j], sTop:L[i0-1], sBase:L[i]}; })();
const RLN={d:0,s:0,i:0};
function rlRiverCarve(x,z,h){ let n=RL_RIVER.near(x,z,RLN); const pd=Math.hypot(x-RL_POND.x,z-RL_POND.z);
  if(pd<RL_POND.R+40){ const b=RL_POND.bed+Math.pow(smooth(RL_POND.R*.7,RL_POND.R+30,pd),1.2)*40; if(b<h) h=b; }
  { const P=RL_PLUNGE, d=Math.hypot(x-P.x,z-P.z); if(d<P.R+25){ const b=d<P.R ? P.bottom+(P.lvl-.25-P.bottom)*Math.pow(d/P.R,2) : P.lvl-.25+(d-P.R)*.6; if(b<h) h=b; } }
  if(n.d>RL_RIVER_W/2+45) return h; const bed=rlBedAt(n.s), w=RL_RIVER_W/2;
  const prof=n.d<w ? -1.0*(1-(n.d/w)*(n.d/w)) : (n.d-w)*.45+Math.pow(Math.max(0,n.d-w-6),1.4)*.05;
  const c=bed+.35+prof; return Math.min(h,c); }
// ---- la rejilla ----
const RG={E:1460, S:5, N:0, h:null};
(function rlBuild(){ const N=RG.N=Math.round(2*RG.E/RG.S)+1, h=RG.h=new Float32Array(N*N);
  for(let j=0;j<N;j++) for(let i=0;i<N;i++){ const x=-RG.E+i*RG.S, z=-RG.E+j*RG.S; h[j*N+i]=rlRiverCarve(x,z,rlNatural(x,z)); } })();
