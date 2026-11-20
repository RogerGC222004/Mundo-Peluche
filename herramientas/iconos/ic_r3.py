# Íconos de la ronda 3 (Modo libre, editor de mapas/casitas, mis creaciones, opciones de criaturas y objetos). Mismo estilo.
from ic_r1 import S, O, R, B, Y, G, P, V, N, W, M, GR, SK, DB, SA, HL
I={}
LB='#8fcff2'; DG='#4f9a4a'; PU='#b58ce0'
def star(cx,cy,r1,r2,n=5,rot=-90):
    import math
    pts=[]
    for k in range(n*2):
        a=math.radians(rot+k*180/n); r=r1 if k%2==0 else r2
        pts.append(f'{cx+r*math.cos(a):.1f} {cy+r*math.sin(a):.1f}')
    return 'M'+' L'.join(pts)+'z'
# ---------- Modo libre: pestañas y apartados ----------
I['bloques']=(f'<rect x="4" y="21" width="15" height="14" rx="2" fill="{R}" {S(2.2)}/><rect x="21" y="21" width="15" height="14" rx="2" fill="{B}" {S(2.2)}/><rect x="12.5" y="6" width="15" height="14" rx="2" fill="{Y}" {S(2.2)}/>'
              f'<g fill="none" stroke="{W}" stroke-width="1.2" stroke-dasharray="1.8 1.6" opacity=".9"><rect x="6.6" y="23.6" width="9.8" height="8.8" rx="1"/><rect x="23.6" y="23.6" width="9.8" height="8.8" rx="1"/><rect x="15.1" y="8.6" width="9.8" height="8.8" rx="1"/></g>')
I['balon']=(f'<circle cx="20" cy="20" r="15.5" fill="{W}" {S(2.2)}/><path d="M20 13.5l5.6 4-2.1 6.6h-7l-2.1-6.6z" fill="{O}"/>'
            f'<path d="M20 13.5V5M25.6 17.5l8-2.6M23.5 24.1l4.8 6.8M16.5 24.1l-4.8 6.8M14.4 17.5l-8-2.6" stroke="{O}" stroke-width="1.8"/><path d="M15.6 4.7 20 7.6l4.4-2.9M33.4 13l-1.6 5.4 4 3.6M30.5 32.4l-5.4-.4L22.6 36M9.5 32.4l5.4-.4L17.4 36M6.6 13l1.6 5.4-4 3.6" fill="none" stroke="{O}" stroke-width="1.6" stroke-linejoin="round"/>')
I['noria']=(f'<path d="M12 36l8-17 8 17" fill="none" stroke="{O}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 36l8-17 8 17" fill="none" stroke="{GR}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<circle cx="20" cy="17" r="12.5" fill="none" stroke="{O}" stroke-width="4.6"/><circle cx="20" cy="17" r="12.5" fill="none" stroke="{P}" stroke-width="2"/>'
            f'<path d="M20 4.5v25M7.5 17h25M11.2 8.2l17.6 17.6M28.8 8.2 11.2 25.8" stroke="{O}" stroke-width="1.4"/>'
            + ''.join(f'<rect x="{x-2.6}" y="{y-2.2}" width="5.2" height="4.4" rx="1.2" fill="{c}" {S(1.4)}/>' for x,y,c in [(20,4.5,Y),(32.5,17,B),(20,29.5,G),(7.5,17,R),(28.8,8.2,N),(28.8,25.8,V),(11.2,25.8,B),(11.2,8.2,G)])
            + f'<circle cx="20" cy="17" r="2.4" fill="{Y}" {S(1.4)}/>')
I['arbol']=(f'<path d="M17.5 24h5v12h-5z" fill="{M}" {S(2)}/><path d="M20 3.5c-5 0-8.6 3.6-8.6 7.6-3.6 1-5.4 4.4-5.4 7.4 0 4.6 3.6 7.5 8 7.5h12c4.4 0 8-2.9 8-7.5 0-3-1.8-6.4-5.4-7.4 0-4-3.6-7.6-8.6-7.6z" fill="{G}" {S(2.2)}/>'
            f'<path d="M14 9.5a6.6 6.6 0 0 1 4-3.4" {HL}/><circle cx="25" cy="17" r="1.6" fill="{R}"/><circle cx="14.5" cy="20" r="1.6" fill="{R}"/>')
I['sillon']=(f'<path d="M8.5 20V12a5 5 0 0 1 5-5h13a5 5 0 0 1 5 5v8" fill="{V}" {S(2.2)}/><path d="M9 21h22v7H9z" fill="#c9a5ef" {S(2)}/>'
             f'<rect x="3" y="17" width="7" height="13.5" rx="3.4" fill="{V}" {S(2.2)}/><rect x="30" y="17" width="7" height="13.5" rx="3.4" fill="{V}" {S(2.2)}/><path d="M7 30.5v4.5M33 30.5v4.5" stroke="{O}" stroke-width="2.4" stroke-linecap="round"/><path d="M13 11.5a3 3 0 0 1 2.4-2" {HL}/>')
I['montana']=(f'<path d="M3 31c5-14 9-21 13-21 5 0 5 12 10 12 3.6 0 5.6-5 11-5" fill="none" stroke="{O}" stroke-width="5.4" stroke-linecap="round"/><path d="M3 31c5-14 9-21 13-21 5 0 5 12 10 12 3.6 0 5.6-5 11-5" fill="none" stroke="{R}" stroke-width="2.6" stroke-linecap="round"/>'
              f'<path d="M8 22v14M14.5 11.5V36M20.5 15v21M27 21v15M33 18v18" stroke="{O}" stroke-width="1.6"/><path d="M4 36h33" stroke="{O}" stroke-width="2" stroke-linecap="round"/>'
              f'<rect x="10.5" y="6.5" width="8" height="5" rx="1.6" fill="{Y}" {S(1.6)}/><circle cx="12.5" cy="12.5" r="1.2" fill="{O}"/><circle cx="16.5" cy="12.5" r="1.2" fill="{O}"/>')
I['bolos']=(f'<path d="M12 5.5c-2 0-3 1.6-3 3.6 0 2.4 1.6 3.4 1.6 5.6 0 2.4-3.4 5-3.4 10.4 0 6 2.4 10.4 4.8 10.4s4.8-4.4 4.8-10.4c0-5.4-3.4-8-3.4-10.4 0-2.2 1.6-3.2 1.6-5.6 0-2-1-3.6-3-3.6z" fill="{W}" {S(2)}/>'
            f'<path d="M10.2 13.2h3.6M10.4 15.4h3.2" stroke="{R}" stroke-width="1.4"/><circle cx="26" cy="27" r="9" fill="{V}" {S(2.2)}/><circle cx="23.5" cy="23.5" r="1.4" fill="{O}"/><circle cx="27.5" cy="22.5" r="1.4" fill="{O}"/><circle cx="26" cy="26.4" r="1.4" fill="{O}"/>')
I['patineta']=(f'<path d="M3.5 21.5c0-1.6 1.4-2.6 3-2.6h27c1.6 0 3 1 3 2.6s-1.4 3-3 3h-27c-1.6 0-3-1.4-3-3z" fill="{N}" {S(2.2)}/><path d="M9 21.5h22" stroke="{Y}" stroke-width="2" stroke-dasharray="3 2.4"/>'
               f'<circle cx="10.5" cy="29.5" r="3.4" fill="{GR}" {S(2)}/><circle cx="29.5" cy="29.5" r="3.4" fill="{GR}" {S(2)}/><path d="M10.5 24.5v1.6M29.5 24.5v1.6" stroke="{O}" stroke-width="2"/>')
I['flor']=(''.join(f'<ellipse cx="20" cy="9.5" rx="5" ry="6.4" transform="rotate({a} 20 17)" fill="{P}" {S(2)}/>' for a in (0,72,144,216,288))
           + f'<circle cx="20" cy="17" r="4.6" fill="{Y}" {S(2)}/><path d="M20 22v14" stroke="{O}" stroke-width="5" stroke-linecap="round"/><path d="M20 22v14" stroke="{G}" stroke-width="2.2" stroke-linecap="round"/><path d="M20 31c3-4 7-4.6 9-4-1 3-4.6 5-9 4z" fill="{G}" {S(1.6)}/>')
I['brote']=(f'<path d="M20 36V20" stroke="{O}" stroke-width="5" stroke-linecap="round"/><path d="M20 36V20" stroke="{G}" stroke-width="2.2" stroke-linecap="round"/>'
            f'<path d="M20 21C20 13 14 8 5.5 8.5 5.5 17 11 21.5 20 21z" fill="{G}" {S(2.2)}/><path d="M20 19c0-6.6 4.6-11 13-11 0 7-4.4 11.6-13 11z" fill="#8bd47e" {S(2.2)}/>'
            f'<path d="M8 32.5c4-2 20-2 24 0" fill="none" stroke="{M}" stroke-width="3" stroke-linecap="round"/><path d="M9 12c2.4.6 5 2.4 6.6 5" {HL}/>')
I['playa']=(f'<path d="M2.5 35c3-6.4 10-9.6 17.5-9.6S34.5 28.6 37.5 35z" fill="{SA}" {S(2.2)}/>'
            f'<path d="M24 34 16.5 9" stroke="{O}" stroke-width="2.2" stroke-linecap="round"/><path d="M4.5 16C8 7 20 2.5 28 7.5z" fill="{R}" {S(2.2)}/><path d="M10 12.5 13.5 6M16.5 9.6l2.4-5.4M22.5 7.6l1.4-3.4" stroke="{W}" stroke-width="2.2"/>'
            f'<path d="M4.5 16C8 7 20 2.5 28 7.5z" fill="none" {S(2.2)}/><circle cx="31" cy="30.5" r="3" fill="{N}" {S(1.6)}/>')
I['copo']=(f'<g stroke="{O}" stroke-width="5.6" stroke-linecap="round"><path d="M20 3.5v33M5.7 11.8l28.6 16.4M5.7 28.2l28.6-16.4"/></g><g stroke="{LB}" stroke-width="2.6" stroke-linecap="round"><path d="M20 3.5v33M5.7 11.8l28.6 16.4M5.7 28.2l28.6-16.4"/></g>'
           f'<g fill="none" stroke="{LB}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 6.5l4 3.6 4-3.6M16 33.5l4-3.6 4 3.6M6 17l5.2-.6-1.4-5M34 17l-5.2-.6 1.4-5M6 23l5.2.6-1.4 5M34 23l-5.2.6 1.4 5"/></g>')
I['paletadulce']=(f'<path d="M20 22v14" stroke="{O}" stroke-width="5" stroke-linecap="round"/><path d="M20 22v14" stroke="{W}" stroke-width="2.4" stroke-linecap="round"/>'
                  f'<circle cx="20" cy="14.5" r="11" fill="{P}" {S(2.2)}/><path d="M20 14.5c0-2 2.6-2.4 3.6-.6 1.4 2.6-1 5.6-4.4 5.4-4-.2-6.2-4.6-4.2-8.4 2.4-4.4 9.6-4.6 12.6.4" fill="none" stroke="{W}" stroke-width="2.6" stroke-linecap="round"/>')
I['espacio']=(f'<rect x="3" y="3" width="34" height="34" rx="9" fill="#2a2f6a" {S(2.2)}/><circle cx="25" cy="16" r="6.4" fill="{N}" {S(1.6)}/><ellipse cx="25" cy="16" rx="11" ry="3" fill="none" stroke="{Y}" stroke-width="1.8" transform="rotate(-20 25 16)"/>'
              f'<path d="{star(11,27,4.2,1.8)}" fill="{Y}"/><circle cx="10" cy="11" r="1.4" fill="{W}"/><circle cx="31" cy="30" r="1.4" fill="{W}"/><circle cx="18" cy="33" r="1" fill="{W}"/><circle cx="15" cy="7.5" r="1" fill="{W}"/>')
I['isla']=(f'<path d="M3 30c4-2 7 0 10 0s6-2 9-2 6 2 9 2 4-1 6 0v6H3z" fill="{B}" {S(2)}/><path d="M8 29c1-5 7-7.6 13-7.6S32 24 33 29z" fill="{SA}" {S(2.2)}/>'
           f'<path d="M20 23c0-6 .6-11 3-15.5" fill="none" stroke="{O}" stroke-width="4.4" stroke-linecap="round"/><path d="M20 23c0-6 .6-11 3-15.5" fill="none" stroke="{M}" stroke-width="2" stroke-linecap="round"/>'
           f'<path d="M23 7.5c-4-3-9-2.6-11.5.6 4-.4 7.4.4 11.5-.6zM23 7.5c3.4-3.6 8.6-3.6 11.4-.6-4 .2-7.6 1.6-11.4.6zM23 7.5c-2 2.6-5.6 4.4-8.6 4.4 1.6-3.4 5-5 8.6-4.4zM23 7.5c3.4 1 6 3.6 6.6 7-3.6-1-5.6-3.6-6.6-7z" fill="{G}" {S(1.8)}/>')
I['sol']=(''.join(f'<path d="M20 2.5v5" stroke="{O}" stroke-width="5" stroke-linecap="round" transform="rotate({a} 20 20)"/><path d="M20 2.5v5" stroke="{N}" stroke-width="2.4" stroke-linecap="round" transform="rotate({a} 20 20)"/>' for a in range(0,360,45))
          + f'<circle cx="20" cy="20" r="9.6" fill="{Y}" {S(2.2)}/><path d="M15 17a6 6 0 0 1 3.4-3.2" {HL}/>')
I['atardecer']=(f'<path d="M2.5 26.5h35v9h-35z" fill="#7d6bd0" {S(2)}/><path d="M7.5 26.5a12.5 12.5 0 0 1 25 0z" fill="{N}" {S(2.2)}/>'
                + ''.join(f'<path d="M20 5.5v4" stroke="{O}" stroke-width="2.4" stroke-linecap="round" transform="rotate({a} 20 26.5)"/>' for a in (-60,-30,0,30,60))
                + f'<path d="M7 31h8M19 31h14M11 34h18" stroke="{P}" stroke-width="1.8" stroke-linecap="round"/>')
NUBE=f'M10.5 24.5h20a6.6 6.6 0 0 0 .5-13.2 9 9 0 0 0-17 2.2 5.6 5.6 0 0 0-3.5 11z'
I['lluvia']=(f'<path d="{NUBE}" fill="#d9e4ee" {S(2.2)}/>'+''.join(f'<path d="M{x} {y}l-2 5" stroke="{B}" stroke-width="2.6" stroke-linecap="round"/>' for x,y in [(14,28.5),(21,28.5),(28,28.5),(17.5,33),(24.5,33)]))
I['tormenta']=(f'<path d="{NUBE}" fill="#9aa6b8" {S(2.2)}/><path d="M22 21l-6 9h5l-3 8 9-11h-5.4l3.4-6z" fill="{Y}" {S(1.8)}/>'
               + f'<path d="M12.5 28l-1.6 4M30 28l-1.6 4" stroke="{B}" stroke-width="2.4" stroke-linecap="round"/>')
I['niebla']=(f'<path d="{NUBE}" transform="translate(0 -4)" fill="#e6ebf0" {S(2.2)}/>'
             + ''.join(f'<path d="M{a} {y}h{b}" stroke="{O}" stroke-width="4.6" stroke-linecap="round"/><path d="M{a} {y}h{b}" stroke="{GR}" stroke-width="2" stroke-linecap="round"/>' for a,y,b in [(5,25,22),(13,30.5,22),(7,35.5,16)]))
I['solnube']=(''.join(f'<path d="M14 3v3.6" stroke="{O}" stroke-width="2.4" stroke-linecap="round" transform="rotate({a} 14 14)"/>' for a in range(-90,181,45))
              + f'<circle cx="14" cy="14" r="6.4" fill="{Y}" {S(2.2)}/><path d="M13 33h18.5a6 6 0 0 0 .4-12 8.4 8.4 0 0 0-15.8 2 5 5 0 0 0-3.1 10z" fill="{W}" {S(2.2)}/>')
I['fuente']=(f'<path d="M5 28h30v3.6a3.4 3.4 0 0 1-3.4 3.4H8.4A3.4 3.4 0 0 1 5 31.6z" fill="{GR}" {S(2.2)}/><path d="M7 28c4-1.6 22-1.6 26 0" fill="none" stroke="{B}" stroke-width="2.4"/>'
             f'<path d="M17.5 28V16h5v12" fill="{GR}" {S(2)}/><path d="M12 16h16" stroke="{O}" stroke-width="4.6" stroke-linecap="round"/><path d="M12 16h16" stroke="{GR}" stroke-width="2.2" stroke-linecap="round"/>'
             f'<path d="M20 14V9M20 9c-3-4.6-8-4.6-10 2M20 9c3-4.6 8-4.6 10 2" fill="none" stroke="{B}" stroke-width="2.4" stroke-linecap="round"/><circle cx="10" cy="14" r="1.4" fill="{B}"/><circle cx="30" cy="14" r="1.4" fill="{B}"/>')
I['goteo']=(f'<g transform="rotate(-35 15 16)"><path d="M8 7h14l-1.4 18a4 4 0 0 1-4 3.6h-3.2a4 4 0 0 1-4-3.6z" fill="#dff1fb" {S(2.2)}/><path d="M9 15h12l-.6 10a3 3 0 0 1-3 2.8h-4.8a3 3 0 0 1-3-2.8z" fill="{B}"/><path d="M8 7h14l-1.4 18a4 4 0 0 1-4 3.6h-3.2a4 4 0 0 1-4-3.6z" fill="none" {S(2.2)}/><path d="M6.5 7h17" stroke="{O}" stroke-width="2.4" stroke-linecap="round"/></g>'
            f'<path d="M27 17c.4 3 2 5 2 7.4M29.6 29.5s-2.4 2.8-2.4 4.2a2.4 2.4 0 0 0 4.8 0c0-1.4-2.4-4.2-2.4-4.2z" fill="{B}" stroke="{O}" stroke-width="1.6" stroke-linecap="round"/>')
I['llaveagua']=(f'<path d="M4 12.5h9v-3h6v3h11a6 6 0 0 1 6 6v3h-7v-2H19v3h-6v-3H4z" fill="{GR}" {S(2.2)}/><rect x="11.5" y="5" width="9" height="4" rx="2" fill="{R}" {S(1.8)}/>'
                f'<path d="M32.5 26s-3.4 4-3.4 6a3.4 3.4 0 0 0 6.8 0c0-2-3.4-6-3.4-6z" fill="{B}" {S(1.8)}/><path d="M6 15h6" {HL}/>')
I['pausa']=f'<rect x="8.5" y="6" width="8.5" height="28" rx="3" fill="{B}" {S(2.2)}/><rect x="23" y="6" width="8.5" height="28" rx="3" fill="{B}" {S(2.2)}/><path d="M11.5 10v6" {HL}/>'
I['cronometro']=(f'<rect x="16.5" y="2.5" width="7" height="4" rx="1.4" fill="{R}" {S(1.8)}/><path d="M30 9.5l2.6-2.6" stroke="{O}" stroke-width="3.4" stroke-linecap="round"/>'
                 f'<circle cx="20" cy="22" r="14" fill="{W}" {S(2.2)}/><circle cx="20" cy="22" r="10.6" fill="none" stroke="{GR}" stroke-width="1.4"/><path d="M20 22V14M20 22l5 3" stroke="{O}" stroke-width="2.4" stroke-linecap="round"/><circle cx="20" cy="22" r="1.8" fill="{R}"/>')
I['prendido']=f'<circle cx="20" cy="20" r="12" fill="{G}" {S(2.2)}/><path d="M14.5 17a6.4 6.4 0 0 1 4-3.6" {HL}/>'
I['apagado']=f'<circle cx="20" cy="20" r="12" fill="{W}" {S(2.2)}/><circle cx="20" cy="20" r="6.5" fill="none" stroke="{GR}" stroke-width="1.6"/>'
I['basquet']=(f'<circle cx="20" cy="20" r="15.5" fill="{N}" {S(2.2)}/><g fill="none" stroke="{O}" stroke-width="1.8"><path d="M4.5 20h31M20 4.5v31M9 9c4.6 4.6 4.6 17.4 0 22M31 9c-4.6 4.6-4.6 17.4 0 22"/></g><path d="M10.5 12.5a11 11 0 0 1 5-5" {HL}/>')
I['bumeran']=(f'<path d="M6 30.5C6 19 10 9 17 5.5c1.6-.8 3 .6 2.4 2.2C16.6 14 15.6 20 16.6 25c4.4-2.4 10.6-3 17-1.6 1.8.4 2 2.6.4 3.4C27 30.4 17 33 9.4 34 7.4 34.2 6 32.6 6 30.5z" fill="{N}" {S(2.2)}/>'
              f'<path d="M10.5 29c0-7 2-14 5.6-19.4M12 30.6c6-.6 12-2 17-4.4" fill="none" stroke="{W}" stroke-width="1.6" stroke-dasharray="2 2" stroke-linecap="round"/>')
I['llanta']=(f'<circle cx="20" cy="20" r="15.5" fill="#3d3f47" {S(2.2)}/><circle cx="20" cy="20" r="8" fill="{GR}" {S(2)}/><circle cx="20" cy="20" r="2.6" fill="{O}"/>'
             + ''.join(f'<path d="M20 5.5v3.4" stroke="#6b6e78" stroke-width="2.6" stroke-linecap="round" transform="rotate({a} 20 20)"/>' for a in range(0,360,30)))
I['control']=(f'<path d="M9 11h22c4 0 6.6 3 7 7.4l.6 7.4c.4 4.4-4 6.6-7 3.6l-3.6-3.6H12l-3.6 3.6c-3 3-7.4.8-7-3.6l.6-7.4C2.4 14 5 11 9 11z" fill="{GR}" {S(2.2)}/>'
              f'<path d="M10.5 15.5v6M7.5 18.5h6" stroke="{O}" stroke-width="2.6" stroke-linecap="round"/><circle cx="27.5" cy="16.5" r="1.9" fill="{R}"/><circle cx="31" cy="20" r="1.9" fill="{B}"/><circle cx="24" cy="20" r="1.9" fill="{Y}"/><circle cx="27.5" cy="23.4" r="1.9" fill="{G}"/>')
I['caja']=(f'<path d="M5 13 20 6.5 35 13v16L20 35.5 5 29z" fill="{M}" {S(2.2)}/><path d="M5 13l15 6.5L35 13M20 19.5v16" fill="none" stroke="{O}" stroke-width="2"/>'
           f'<path d="M12.5 9.7l15 6.5v5.6l-3-1.2v-5.6" fill="#f0d4a4" {S(1.6)}/>')
I['guino']=(f'<circle cx="20" cy="20" r="15.5" fill="{Y}" {S(2.2)}/><ellipse cx="14" cy="17" rx="2" ry="3" fill="{O}"/><path d="M23 17q3.6-2.6 6.4 0" fill="none" stroke="{O}" stroke-width="2.2" stroke-linecap="round"/>'
            f'<path d="M13 24.5q7 6 14 0" fill="none" stroke="{O}" stroke-width="2.2" stroke-linecap="round"/><path d="M10 11a11 11 0 0 1 5.6-4.6" {HL}/>')
# ---------- editores (mapas, casitas) y mis creaciones ----------
I['cajaherr']=(f'<path d="M14.5 13V9.5a2.6 2.6 0 0 1 2.6-2.6h5.8a2.6 2.6 0 0 1 2.6 2.6V13" fill="none" stroke="{O}" stroke-width="2.6"/>'
               f'<rect x="4" y="13" width="32" height="20" rx="3" fill="{R}" {S(2.2)}/><path d="M4 21h32" stroke="{O}" stroke-width="2"/><rect x="17" y="19" width="6" height="5" rx="1.2" fill="{GR}" {S(1.6)}/><path d="M7.5 16.5h6" {HL}/>')
I['basura']=(f'<path d="M8 12h24l-2.2 21.6a2.6 2.6 0 0 1-2.6 2.4H12.8a2.6 2.6 0 0 1-2.6-2.4z" fill="{GR}" {S(2.2)}/><path d="M5 12h30" stroke="{O}" stroke-width="2.6" stroke-linecap="round"/>'
             f'<path d="M15 12V8a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v4" fill="none" stroke="{O}" stroke-width="2.2"/><path d="M15 17v13M20 17v13M25 17v13" stroke="{O}" stroke-width="1.8" stroke-linecap="round"/>')
I['deshacer']=(f'<path d="M14 9.5 5.5 16.5l8.5 7z" fill="{B}" {S(2.2)}/><path d="M12 16.5h12a9 9 0 0 1 0 18h-6" fill="none" stroke="{O}" stroke-width="7" stroke-linecap="round"/><path d="M12 16.5h12a9 9 0 0 1 0 18h-6" fill="none" stroke="{B}" stroke-width="3.4" stroke-linecap="round"/>'
               f'<path d="M14 9.5 5.5 16.5l8.5 7z" fill="{B}" {S(2.2)}/>')
I['rehacer']=f'<g transform="translate(40 0) scale(-1 1)">{I["deshacer"]}</g>'
I['pincel']=(f'<path d="M33.5 4.5c1.4 1.4.8 3.4-.6 4.8L21 21.2l-2.2-2.2L30.7 5.1c1.4-1.4 1.4-2 2.8-.6z" fill="{M}" {S(2.2)}/><path d="M17.4 20.4l2.2 2.2" stroke="{O}" stroke-width="6" stroke-linecap="round"/><path d="M17.4 20.4l2.2 2.2" stroke="{GR}" stroke-width="3" stroke-linecap="round"/>'
             f'<path d="M15.5 22.5c3 0 4.2 2 3.6 4.4-1 4-6.6 8-13.6 7.6 2.4-2.4 2-5 2.6-7.6.6-2.6 3.6-4.4 7.4-4.4z" fill="{B}" {S(2.2)}/>')
I['ojo']=(f'<path d="M3 20c4-7 10-11 17-11s13 4 17 11c-4 7-10 11-17 11S7 27 3 20z" fill="{W}" {S(2.2)}/><circle cx="20" cy="20" r="7" fill="{B}" {S(2)}/><circle cx="20" cy="20" r="3.4" fill="{O}"/><circle cx="22.2" cy="17.8" r="1.4" fill="{W}"/>')
I['escuadra']=(f'<path d="M5 35V5l30 30z" fill="{Y}" {S(2.2)}/><path d="M11 29V19.5l9.5 9.5z" fill="#fbf4e6" {S(1.8)}/>'
               + ''.join(f'<path d="M5 {y}h{w}" stroke="{O}" stroke-width="1.6"/>' for y,w in [(10,4),(15,3),(20,4),(25,3),(30,4)]))
I['pregunta']=(f'<circle cx="20" cy="20" r="15.5" fill="{B}" {S(2.2)}/><path d="M14.5 15c0-3.4 2.6-5.6 5.6-5.6 3.4 0 5.6 2.2 5.6 5 0 4.4-5.6 4.6-5.6 8.6" fill="none" stroke="{W}" stroke-width="3.6" stroke-linecap="round"/><circle cx="20" cy="29" r="2.2" fill="{W}"/>')
I['carrito']=(f'<path d="M2.5 7h5l4 18.5h19.5l3.5-13.5H9.5" fill="none" stroke="{O}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>'
              f'<path d="M9.8 12h24.7l-3.5 13.5H12.5z" fill="{B}" {S(2.2)}/><path d="M16 15.5l1 6.6M22 15.5v6.6M28 15.5l-1 6.6" stroke="{W}" stroke-width="1.6" stroke-linecap="round"/>'
              f'<circle cx="14.5" cy="31.5" r="3.2" fill="{GR}" {S(2)}/><circle cx="28" cy="31.5" r="3.2" fill="{GR}" {S(2)}/>')
I['casasintecho']=(f'<path d="M8.5 19v15.5h23V19" fill="{W}" {S(2.2)}/><path d="M8.5 19h23" stroke="{O}" stroke-width="2.2" stroke-dasharray="3 2.6" stroke-linecap="round"/>'
                   f'<rect x="16" y="24.5" width="8" height="10" rx="1.6" fill="{M}" {S(1.8)}/><rect x="25.5" y="22" width="4.5" height="4.5" fill="{B}" {S(1.4)}/><path d="M7 15l3-6M33 15l-3-6M20 6v6" stroke="{R}" stroke-width="2.4" stroke-linecap="round" opacity=".8"/>')
I['estrellavacia']=f'<path d="M20 3.5l4.9 10 11 1.6-8 7.7 1.9 10.9L20 28.6l-9.8 5.1 1.9-10.9-8-7.7 11-1.6z" fill="{W}" {S(2.2)}/><path d="M20 10.5l2.6 5.4 6 .8-4.4 4.2 1 6L20 24l-5.2 2.9 1-6-4.4-4.2 6-.8z" fill="none" stroke="{Y}" stroke-width="1.8" stroke-linejoin="round"/>'
I['playizq']=f'<g transform="translate(40 0) scale(-1 1)"><path d="M11 6.5c0-1.6 1.7-2.5 3-1.7l20 13.4c1.2.8 1.2 2.6 0 3.4L14 35c-1.3.9-3-.1-3-1.7z" fill="{G}" {S(2.2)}/></g>'
I['lapiz']=(f'<path d="M27 4.5 35.5 13 14 34.5l-10 1.5 1.5-10z" fill="{Y}" {S(2.2)}/><path d="M27 4.5 35.5 13l-4 4L23 8.5z" fill="{P}" {S(2)}/><path d="M5.5 26 14 34.5" stroke="{O}" stroke-width="2"/>'
            f'<path d="M5.5 26 4 36l10-1.5z" fill="#f5d9b0" {S(1.8)}/><path d="M4.6 32l-.6 4 4-.6z" fill="{O}"/><path d="M21 12.5 9 24.5" stroke="#e0b23a" stroke-width="1.8" stroke-linecap="round"/>')
I['lupa']=(f'<path d="M24.5 24.5 35 35" stroke="{O}" stroke-width="7.4" stroke-linecap="round"/><path d="M24.5 24.5 35 35" stroke="{M}" stroke-width="4" stroke-linecap="round"/>'
           f'<circle cx="16" cy="16" r="11.5" fill="#dff1fb" stroke="{O}" stroke-width="2.6"/><circle cx="16" cy="16" r="11.5" fill="none" stroke="{GR}" stroke-width="1.2" opacity=".6"/><path d="M10 14a6.6 6.6 0 0 1 4-4.4" {HL}/>')
# ---------- crear criatura / objeto: tamaño, cómo se porta, velocidad, qué hace (por nombre) ----------
def bicho(cx,cy,s,c=PU):   # una criaturita redonda (como las que armas)
    return (f'<g transform="translate({cx} {cy}) scale({s})"><path d="M-6 9v4M6 9v4" stroke="{O}" stroke-width="4.6" stroke-linecap="round"/><path d="M-6 9v4M6 9v4" stroke="{c}" stroke-width="2.2" stroke-linecap="round"/>'
            f'<ellipse cx="0" cy="0" rx="11" ry="10" fill="{c}" {S(2.2/s)}/><circle cx="-4" cy="-2" r="1.9" fill="{O}"/><circle cx="4" cy="-2" r="1.9" fill="{O}"/><path d="M-2.4 3q2.4 2 4.8 0" fill="none" stroke="{O}" stroke-width="{1.4/s:.2f}" stroke-linecap="round"/></g>')
SUELO=f'<path d="M3 36.5h34" stroke="{O}" stroke-width="2" stroke-linecap="round"/>'
I['tamchico']=SUELO+bicho(20,30,.5)
I['tamnormal']=SUELO+bicho(20,26.5,.85)
I['tamgrande']=SUELO+bicho(20,22.6,1.25)
I['tamgigante']=SUELO+bicho(20,19.2,1.62)+f'<path d="M3 4.5v31M1.5 4.5h3M1.5 35.5h3" stroke="{O}" stroke-width="1.4" opacity=".55"/>'
def gema(cx,cy,s,c=B):
    return f'<g transform="translate({cx} {cy}) scale({s})"><path d="{star(0,0,12,5.2)}" fill="{Y}" {S(2.2/s)}/></g>'
I['objchico']=SUELO+gema(20,30.5,.45)
I['objnormal']=SUELO+gema(20,25,.85)
I['objgrande']=SUELO+gema(20,19.5,1.38)
I['pasea']=(bicho(23,18,.95)+f'<g fill="{O}" opacity=".55"><ellipse cx="5" cy="35" rx="1.8" ry="1.2"/><ellipse cx="10" cy="32.5" rx="1.8" ry="1.2"/><ellipse cx="15" cy="35" rx="1.8" ry="1.2"/><ellipse cx="20" cy="32.5" rx="1.8" ry="1.2"/></g>')
I['sigue']=(bicho(13,22,.85)+f'<path d="M31 16.5c-2.6-4-8-1.4-6 2.6l6 6 6-6c2-4-3.4-6.6-6-2.6z" fill="{R}" {S(1.8)}/><path d="M24 29.5h10" stroke="{O}" stroke-width="2" stroke-linecap="round" stroke-dasharray="2 2.4"/>')
I['huye']=(bicho(24,20,.9)+f'<path d="M3 15h7M2 21h8M4 27h6" stroke="{O}" stroke-width="2.2" stroke-linecap="round"/><path d="M6 9.5c2-1.6 4-1.6 6 0" fill="none" stroke="{B}" stroke-width="2" stroke-linecap="round" opacity=".7"/>')
I['brinca']=(bicho(25,14,.82)+f'<path d="M4 34c3-12 9-20 14-21" fill="none" stroke="{O}" stroke-width="2" stroke-linecap="round" stroke-dasharray="2.4 2.4"/>'+SUELO)
I['vuela']=(f'<path d="M11 15c-6-6-11-2-9 3 2.4 4 6 3.4 9 1M29 15c6-6 11-2 9 3-2.4 4-6 3.4-9 1" fill="{W}" {S(2)}/>'+bicho(20,18,.95)+f'<path d="M20 36v-4M16.5 35l1.6-3M23.5 35l-1.6-3" stroke="{B}" stroke-width="2" stroke-linecap="round" opacity=".7"/>')
I['quieta']=(SUELO+bicho(17,24,1.05)+f'<g fill="none" stroke="{B}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M28 6h6l-6 6h6"/><path d="M31 14.5h3.6l-3.6 3.6h3.6"/></g>')
I['tortuga']=(f'<ellipse cx="33" cy="25" rx="4.4" ry="3.6" fill="#8bd47e" {S(2)}/><circle cx="34.4" cy="24" r="1" fill="{O}"/><path d="M9 30v4M27 30v4" stroke="{O}" stroke-width="4.6" stroke-linecap="round"/><path d="M9 30v4M27 30v4" stroke="#8bd47e" stroke-width="2.2" stroke-linecap="round"/>'
              f'<path d="M3.5 30c0-10 6.6-17 14.5-17S32.5 20 32.5 30z" fill="{DG}" {S(2.2)}/><path d="M11 30l3-8.5h8l3 8.5M14 21.5 18 15l4 6.5" fill="none" stroke="#2f6b2b" stroke-width="1.6"/><path d="M3 30h30" stroke="{O}" stroke-width="2.2" stroke-linecap="round"/>')
I['sonrisa']=(f'<circle cx="20" cy="20" r="15.5" fill="{Y}" {S(2.2)}/><ellipse cx="14.5" cy="16.5" rx="2" ry="3" fill="{O}"/><ellipse cx="25.5" cy="16.5" rx="2" ry="3" fill="{O}"/>'
              f'<path d="M13 23.5q7 5.6 14 0" fill="none" stroke="{O}" stroke-width="2.2" stroke-linecap="round"/><path d="M10 11a11 11 0 0 1 5.6-4.6" {HL}/>')
I['rayo']=f'<path d="M24 3 8 22.5h10L14.5 37 32 15.5H21.5z" fill="{Y}" {S(2.2)}/><path d="M21 9l-6 8" {HL}/>'
I['cargar']=(f'<circle cx="20" cy="13" r="8" fill="{B}" {S(2.2)}/><path d="M16 10a4.4 4.4 0 0 1 2.6-2.4" {HL}/>'
             f'<path d="M3 25c4-2 8-2.4 11 0l5 4h-6M37 25c-4-2-8-2.4-11 0l-5 4h6" fill="{SK}" {S(2)}/><path d="M3 25c2 4 6 9 13 9h8c7 0 11-5 13-9" fill="{SK}" {S(2.2)}/>')
I['lanzar']=(f'<circle cx="13" cy="25" r="8" fill="{R}" {S(2.2)}/><path d="M10 22a4.4 4.4 0 0 1 2.6-2.4" {HL}/>'
             f'<path d="M22 22C24 10 34 8 35 18c.6 6-4 9-9 7" fill="none" stroke="{O}" stroke-width="5.4" stroke-linecap="round"/><path d="M22 22C24 10 34 8 35 18c.6 6-4 9-9 7" fill="none" stroke="{B}" stroke-width="2.4" stroke-linecap="round"/>'
             f'<path d="M28 21l-4 4.6 5.6 1.8z" fill="{B}" {S(1.8)}/>')
I['foco']=(f'<path d="M20 4c-6.6 0-11 4.6-11 10.6 0 4.4 2.4 6.6 4.4 9 1 1.2 1.6 2.6 1.6 4.4h10c0-1.8.6-3.2 1.6-4.4 2-2.4 4.4-4.6 4.4-9C31 8.6 26.6 4 20 4z" fill="{Y}" {S(2.2)}/>'
           f'<rect x="15" y="28" width="10" height="7" rx="2" fill="{GR}" {S(2)}/><path d="M15.4 31.4h9.2" stroke="{O}" stroke-width="1.4"/><path d="M17 22c0-3 3-3 3-6m0 0c0 3 3 3 3 6" fill="none" stroke="{N}" stroke-width="1.6" stroke-linecap="round"/><path d="M13.5 11a6.6 6.6 0 0 1 3.4-3.6" {HL}/>'
           + ''.join(f'<path d="M20 0.5v-0" />' for _ in []))

I['casalista']=(f'<path d="M24 31.5h-2.6v-4.6h6.8v4.6" fill="none"/><path d="M4.5 19v15.5h21V19" fill="{W}" {S(2.2)}/><path d="M1.5 20.5 15 8l13.5 12.5z" fill="{B}" {S(2.2)}/>'
                f'<rect x="11.5" y="24.5" width="7" height="10" rx="1.4" fill="{M}" {S(1.8)}/><path d="M32 34.5v-6" stroke="{O}" stroke-width="2.2"/><circle cx="32" cy="23.5" r="6" fill="{G}" {S(2)}/><path d="M2 35.5h36" stroke="{O}" stroke-width="2" stroke-linecap="round"/><circle cx="7" cy="31.5" r="1.6" fill="{P}"/><circle cx="23" cy="32" r="1.6" fill="{Y}"/>')
E={'🧱':'bloques','⚽':'balon','🎡':'noria','🌳':'arbol','🛋':'sillon','🎢':'montana','🎳':'bolos','🛹':'patineta','🌸':'flor','🌱':'brote','🏖':'playa',
   '❄':'copo','🍭':'paletadulce','🌌':'espacio','🏝':'isla','☀':'sol','🌇':'atardecer','🌧':'lluvia','⛈':'tormenta','🌫':'niebla','🌤':'solnube',
   '⛲':'fuente','🫗':'goteo','🚰':'llaveagua','⏸':'pausa','⏱':'cronometro','🟢':'prendido','⚪':'apagado','🏀':'basquet','🪃':'bumeran','🛞':'llanta',
   '🎮':'control','📦':'caja','😉':'guino','🧰':'cajaherr','🗑':'basura','↶':'deshacer','↷':'rehacer','🖌':'pincel','👁':'ojo','📐':'escuadra','❓':'pregunta',
   '🛒':'carrito','🏚':'casasintecho','★':'estrella','☆':'estrellavacia','◀':'playizq','▲':'arriba','▼':'abajo','✏':'lapiz','🔍':'lupa','⚡':'rayo','💡':'foco','🐢':'tortuga','🙂':'sonrisa','🏡':'casalista'}
NOM={'bloques':'Bloques','balon':'Física (balón)','noria':'Parque','arbol':'Naturaleza / jardín','sillon':'Casa (muebles)','montana':'Se mueven','bolos':'Juguetes','patineta':'Vehículos',
     'flor':'Plantas / flor','brote':'Pasto','playa':'Arena','copo':'Nieve','paletadulce':'Dulce','espacio':'Espacio','isla':'Como en la isla','sol':'Día / soleado','atardecer':'Atardecer',
     'lluvia':'Lluvia','tormenta':'Tormenta','niebla':'Niebla','solnube':'Tu planicie','fuente':'Fuente','goteo':'Goteo','llaveagua':'Se llenó (llave)','pausa':'Cerrar / pausa',
     'cronometro':'Cronómetro','prendido':'Prendida','apagado':'Apagada','basquet':'Basquetbol','bumeran':'Bumerán','llanta':'Llanta','control':'Juego','caja':'Mis creaciones',
     'guino':'Guiño','cajaherr':'Herramientas','basura':'Quitar / borrar','deshacer':'Deshacer','rehacer':'Rehacer','pincel':'Pintar','ojo':'Caminar / ver','escuadra':'Diseño',
     'pregunta':'Ayuda','carrito':'Tienda','casasintecho':'Sin techo','estrellavacia':'Favorita (vacía)','playizq':'Esconder panel','lapiz':'Editar','lupa':'Buscar / acercar',
     'tamchico':'Tamaño: chiquita','tamnormal':'Tamaño: normal','tamgrande':'Tamaño: grande','tamgigante':'Tamaño: gigante','objchico':'Objeto chico','objnormal':'Objeto normal','objgrande':'Objeto grande',
     'pasea':'Pasea','sigue':'Te sigue','huye':'Huye de ti','brinca':'Brinca','vuela':'Vuela','quieta':'Se queda quieta','tortuga':'Lenta','sonrisa':'Normal','rayo':'Rápida',
     'casalista':'Casas listas','cargar':'Solo cargar','lanzar':'Lanzar (regresa)','foco':'Luz'}
