# Íconos de la ronda 1 (botones de acción, botones de arriba, pausa y menú principal)
# Estilo: el de la barra del Modo libre — 40×40, contorno café #5a4426 (2 px, esquinas redondas), colores planos y un brillito blanco.
O='#5a4426'
def S(w=2): return f'stroke="{O}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"'
R='#e5534b'; B='#5ab4e8'; Y='#f5cd4a'; G='#6cc070'; P='#f59ac0'; V='#a77bd6'; N='#f2a03d'; W='#fffdf6'; M='#d29a5b'; GR='#c9ced6'; SK='#f6c9a0'; DB='#3f7fc0'; SA='#e9c98a'
HL='stroke="#fff" stroke-width="1.8" stroke-linecap="round" fill="none" opacity=".75"'
I={}
# flechas
I['arriba']=f'<path d="M20 4.5 33.5 19H25.5v15h-11V19H6.5z" fill="{B}" {S(2.2)}/><path d="M18.5 10l-6 6.5" {HL}/>'
I['abajo']=f'<path d="M20 35.5 33.5 21H25.5V6h-11v15H6.5z" fill="{B}" {S(2.2)}/><path d="M18 9.5v8" {HL}/>'
I['izq']=f'<path d="M4.5 20 19 6.5v8h16v11H19v8z" fill="{B}" {S(2.2)}/><path d="M10.5 18.5l6-5.5" {HL}/>'
I['der']=f'<path d="M35.5 20 21 6.5v8H5v11h16v8z" fill="{B}" {S(2.2)}/><path d="M8.5 17.5h8" {HL}/>'
I['arribaabajo']=f'<path d="M20 3 31 14h-6.5v12H31L20 37 9 26h6.5V14H9z" fill="{B}" {S(2.2)}/><path d="M18 9.5l-4 4" {HL}/>'
I['play']=f'<path d="M11 6.5c0-1.6 1.7-2.5 3-1.7l20 13.4c1.2.8 1.2 2.6 0 3.4L14 35c-1.3.9-3-.1-3-1.7z" fill="{G}" {S(2.2)}/><path d="M15 11v8" {HL}/>'
I['check']=f'<path d="M7 21.5l8.5 8.5L33.5 10" fill="none" stroke="{O}" stroke-width="8.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M7 21.5l8.5 8.5L33.5 10" fill="none" stroke="{G}" stroke-width="4.6" stroke-linecap="round" stroke-linejoin="round"/>'
I['cerrar']=f'<path d="M10 10l20 20M30 10L10 30" stroke="{O}" stroke-width="8.5" stroke-linecap="round"/><path d="M10 10l20 20M30 10L10 30" stroke="{R}" stroke-width="4.6" stroke-linecap="round"/>'
# agua
I['gota']=f'<path d="M20 4.5S8.5 18 8.5 25a11.5 11.5 0 0 0 23 0C31.5 18 20 4.5 20 4.5z" fill="{B}" {S(2.2)}/><path d="M14.5 24.5a6 6 0 0 0 4 6" {HL}/>'
I['gotas']=(f'<path d="M14 6S6 15.5 6 20.5a8 8 0 0 0 16 0C22 15.5 14 6 14 6z" fill="{B}" {S(2)}/>'
            f'<path d="M28 15s-6 7-6 10.6a6 6 0 0 0 12 0C34 22 28 15 28 15z" fill="{B}" {S(2)}/>'
            f'<path d="M17.5 27.5s-3.8 4.4-3.8 6.6a3.8 3.8 0 0 0 7.6 0c0-2.2-3.8-6.6-3.8-6.6z" fill="{B}" {S(1.8)}/><path d="M10 20a4 4 0 0 0 2.6 4" {HL}/>')
I['ola']=(f'<path d="M3.5 30c4 0 4.5-3 8-3s4 3 8 3 4.5-3 8-3 4 3 9 3v6.5h-33z" fill="{DB}" {S(2)}/>'
          f'<path d="M3.5 27V22C5 12 13 6.5 21 7c7 .4 11 5 10.5 10-.4 4-4.2 6-7.2 4.6-2.6-1.2-2.2-4.6.2-5.2-2.6-3-9.5-2.4-12.5 3.2C10 23 9 26 3.5 27z" fill="{B}" {S(2)}/>'
          f'<path d="M24 16c-2-1.5-6-.6-7.5 2" {HL}/>')
I['burbujas']=(f'<circle cx="15" cy="23" r="10" fill="#cfeaff" {S(2)}/><circle cx="29" cy="12" r="6.5" fill="#cfeaff" {S(2)}/><circle cx="31" cy="29" r="4.5" fill="#cfeaff" {S(1.8)}/>'
               f'<path d="M9.5 20a6 6 0 0 1 4-4.5M26 9.5a3.5 3.5 0 0 1 2.5-1.8" {HL} stroke-width="2.2"/>')
I['regadera']=(f'<path d="M6 10h11a4 4 0 0 1 4 4v3" fill="none" stroke="{O}" stroke-width="6" stroke-linecap="round"/><path d="M6 10h11a4 4 0 0 1 4 4v3" fill="none" stroke="{GR}" stroke-width="2.6" stroke-linecap="round"/>'
               f'<path d="M12.5 17h17l-2.5 5h-12z" fill="{GR}" {S(2)}/>'
               f'<g stroke="{B}" stroke-width="2.4" stroke-linecap="round"><path d="M15 26l-1.5 4M20.5 26v5M26 26l1.5 4M17.5 33l-.8 2.5M24 33l.8 2.5"/></g>')
I['cubeta']=(f'<path d="M8.5 15h23l-2.6 19.5H11.1z" fill="{B}" {S(2.2)}/><ellipse cx="20" cy="15" rx="11.5" ry="3.4" fill="#cfeaff" {S(2)}/>'
             f'<path d="M8.5 15C9 5 31 5 31.5 15" fill="none" {S(2)}/><path d="M13 21l1 9" {HL}/>')
# objetos y juguetes
I['tabla']=(f'<g transform="rotate(45 20 20)"><path d="M20 .8c4.6 5 6.6 11.8 6.6 19.2 0 9.8-2.8 17.6-6.6 17.6s-6.6-7.8-6.6-17.6C13.4 12.6 15.4 5.8 20 .8z" fill="{N}" {S(2.2)}/>'
            f'<path d="M20 7.5v27" stroke="{W}" stroke-width="3" stroke-linecap="round"/><path d="M20 7.5v27" stroke="{R}" stroke-width="1.2" stroke-linecap="round"/><path d="M16.6 9c-.9 2.4-1.3 5-1.4 7.5" {HL}/></g>')
I['mochila']=(f'<path d="M14 9.5a6 6 0 0 1 12 0" fill="none" {S(2.4)}/><rect x="8.5" y="10" width="23" height="25" rx="7" fill="{R}" {S(2.2)}/>'
              f'<path d="M8.5 18c4 3.5 19 3.5 23 0" fill="none" {S(2)}/><rect x="13.5" y="23" width="13" height="8.5" rx="3" fill="#f2847c" {S(1.8)}/><circle cx="20" cy="19.5" r="1.6" fill="{Y}" {S(1.2)}/><path d="M12.5 13.5v3" {HL}/>')
I['candado']=(f'<path d="M12.5 18v-5a7.5 7.5 0 0 1 15 0v5" fill="none" stroke="{O}" stroke-width="6.4"/><path d="M12.5 18v-5a7.5 7.5 0 0 1 15 0v5" fill="none" stroke="{GR}" stroke-width="2.8"/>'
              f'<rect x="7.5" y="17" width="25" height="18" rx="4.5" fill="{Y}" {S(2.2)}/><path d="M20 23.5v5" stroke="{O}" stroke-width="3" stroke-linecap="round"/><circle cx="20" cy="23.5" r="2.4" fill="{O}"/><path d="M11.5 21v8" {HL}/>')
I['timbre']=(f'<path d="M20 5.5c-6.5 0-10 5-10 11.5v7L6.5 29.5h27L30 24v-7c0-6.5-3.5-11.5-10-11.5z" fill="{Y}" {S(2.2)}/>'
             f'<circle cx="20" cy="32.5" r="3.4" fill="{N}" {S(2)}/><circle cx="20" cy="4.5" r="1.9" fill="{N}" {S(1.6)}/><path d="M14.5 13.5c0-2 1-3.5 2.6-4.3" {HL}/>')
I['robot']=(f'<path d="M20 4.5v5" {S(2.2)}/><circle cx="20" cy="4.3" r="2.4" fill="{R}" {S(1.6)}/><rect x="7.5" y="10" width="25" height="20" rx="6" fill="{GR}" {S(2.2)}/>'
            f'<circle cx="14.5" cy="18.5" r="3.3" fill="{B}" {S(1.8)}/><circle cx="25.5" cy="18.5" r="3.3" fill="{B}" {S(1.8)}/><rect x="13" y="24" width="14" height="3.4" rx="1.7" fill="{W}" {S(1.6)}/>'
            f'<path d="M7.5 17H4.5v7h3M32.5 17h3v7h-3" fill="{GR}" {S(1.8)}/><rect x="13" y="30" width="14" height="5.5" rx="2" fill="{GR}" {S(2)}/>')
I['casita']=(f'<path d="M8.5 19v15.5h23V19" fill="{W}" {S(2.2)}/><path d="M4.5 20.5 20 6.5l15.5 14z" fill="{R}" {S(2.2)}/>'
             f'<rect x="16" y="24.5" width="8" height="10" rx="1.6" fill="{M}" {S(1.8)}/><rect x="25.5" y="22" width="4.5" height="4.5" fill="{B}" {S(1.4)}/>')
I['llaveinglesa']=(f'<path d="M24.5 4.8a8 8 0 0 0-6.4 10.8L6 27.7a3.6 3.6 0 1 0 5.1 5.1l12.1-12.1a8 8 0 0 0 10.8-6.4l-5.3 1.4-4-4 1.4-5.3z" fill="{GR}" {S(2.2)}/>'
                   f'<circle cx="8.6" cy="30.3" r="1.5" fill="{O}"/>')
I['mano']=(f'<path d="M12 21V11.5a2.6 2.6 0 0 1 5.2 0V19V8.5a2.6 2.6 0 0 1 5.2 0V19V10a2.6 2.6 0 0 1 5.2 0v10.5V15a2.5 2.5 0 0 1 5 0v8.5c0 7.5-5 12-11.4 12-4.6 0-7.4-2.4-9.8-6l-4.2-6.3c-1.4-2.1 1-4.4 3-3l2.6 1.8z" fill="{SK}" {S(2)}/>'
           f'<path d="M14 26c1 1.6 2.6 2.6 4.4 3" {HL} opacity=".5"/>')
I['empujar']=(f'<g transform="rotate(90 20 20)"><path d="M12 21V11.5a2.6 2.6 0 0 1 5.2 0V19V8.5a2.6 2.6 0 0 1 5.2 0V19V10a2.6 2.6 0 0 1 5.2 0v10.5V15a2.5 2.5 0 0 1 5 0v8.5c0 7.5-5 12-11.4 12-4.6 0-7.4-2.4-9.8-6l-4.2-6.3c-1.4-2.1 1-4.4 3-3l2.6 1.8z" fill="{SK}" {S(2)}/></g>'
              f'<path d="M3.5 13h4M2.5 20h4M3.5 27h4" stroke="{O}" stroke-width="2.2" stroke-linecap="round"/>')
I['pierna']=(f'<path d="M14 4.5h9l-1 15.5 8.5 8.5-6.4 6.4L14 25z" fill="{SK}" {S(2.2)}/><path d="M21.5 27.5l9-1.5c3 0 5 2 5 4.5v3h-11z" fill="{R}" {S(2.2)}/><path d="M24.5 32.5h11" stroke="{W}" stroke-width="2" stroke-linecap="round"/>'
             f'<path d="M3.5 18h5M2.5 24h6" stroke="{O}" stroke-width="2" stroke-linecap="round" opacity=".7"/>')
I['disco']=(f'<ellipse cx="20" cy="21" rx="16" ry="9.5" fill="{B}" {S(2.2)}/><ellipse cx="20" cy="19" rx="10.5" ry="5.2" fill="#8fcff2" {S(1.6)}/><ellipse cx="20" cy="18.5" rx="4.5" ry="2" fill="{W}" {S(1.4)}/>')
I['remolino']=(f'<circle cx="20" cy="20" r="15.5" fill="{V}" {S(2.2)}/><path d="M20 20.5c0-2 2.6-2.6 3.8-.8 1.8 2.6-.6 6.4-4.2 6.4-4.6 0-7-5-4.6-9 3-5 11-5 13.4 1" fill="none" stroke="{W}" stroke-width="2.6" stroke-linecap="round"/>')
I['resorte']=''.join(f'<ellipse cx="20" cy="{9+k*4.6}" rx="12" ry="3.6" fill="none" stroke="{O}" stroke-width="4.4"/><ellipse cx="20" cy="{9+k*4.6}" rx="12" ry="3.6" fill="none" stroke="{c}" stroke-width="2.4"/>' for k,c in enumerate([R,N,Y,G,B,V]))
I['llave']=(f'<circle cx="12.5" cy="15" r="8" fill="{Y}" {S(2.2)}/><circle cx="12.5" cy="15" r="2.8" fill="{W}" {S(1.6)}/>'
            f'<path d="M18 20.5l14 14M25.5 28l3.6-3.6M29.5 32l3-3" stroke="{O}" stroke-width="6.2" stroke-linecap="round"/><path d="M18 20.5l14 14M25.5 28l3.6-3.6M29.5 32l3-3" stroke="{Y}" stroke-width="2.8" stroke-linecap="round"/>')
I['cohete']=(f'<path d="M14.5 27.5c-3 1-5.5 4.5-5 8 3.5.5 7-2 8-5" fill="{N}" {S(1.8)}/><path d="M12 23l-5.5 1 3.5-6.5 5.5-.6M17 28l-1 5.5 6.5-3.5.6-5.5" fill="{R}" {S(2)}/>'
             f'<path d="M15 25 14.5 25.5 19 30c9-4 15.5-12 16-25-13 .5-21 7-25 16z" fill="{W}" {S(2.2)}/><circle cx="25.5" cy="14.5" r="3.6" fill="{B}" {S(1.8)}/><path d="M29 5.3c1.5 2 3.8 4.2 5.7 5.7l.3-6z" fill="{R}" {S(1.6)}/>')
I['diana']=(f'<circle cx="18" cy="22" r="14" fill="{W}" {S(2.2)}/><circle cx="18" cy="22" r="9.6" fill="{R}" {S(1.8)}/><circle cx="18" cy="22" r="5.4" fill="{W}" {S(1.6)}/><circle cx="18" cy="22" r="2" fill="{R}"/>'
            f'<path d="M18 22 33 7" stroke="{O}" stroke-width="2.4" stroke-linecap="round"/><path d="M33 7l-1-4M33 7l4 1M31 9l-1.2-4M31 9l4.2.8" stroke="{G}" stroke-width="2" stroke-linecap="round"/>')
I['papalote']=(f'<path d="M22 3.5 33 15 22 28 11 15z" fill="{Y}" {S(2.2)}/><path d="M22 3.5v24.5M11 15h22" stroke="{O}" stroke-width="1.6"/><path d="M22 3.5 33 15H22zM22 15 11 15l11 13z" fill="{R}" stroke="none" opacity=".85"/>'
               f'<path d="M22 3.5 33 15 22 28 11 15z" fill="none" {S(2.2)}/><path d="M22 28c-3 3-1 5-5 6.5s-6 0-9 2" fill="none" stroke="{O}" stroke-width="1.6" stroke-linecap="round"/><path d="M15 33.5l2.5 2.5M10 35l1.5 2.6" stroke="{B}" stroke-width="2.4" stroke-linecap="round"/>')
I['globo']=(f'<path d="M20 4.5c-7 0-11.5 5.6-11.5 12 0 7.5 6.5 13 11.5 14 5-1 11.5-6.5 11.5-14 0-6.4-4.5-12-11.5-12z" fill="{R}" {S(2.2)}/>'
            f'<path d="M18 30.5h4l-2 2.6z" fill="{R}" {S(1.6)}/><path d="M20 33c-2 2.5 2 3 0 5.5" fill="none" stroke="{O}" stroke-width="1.6" stroke-linecap="round"/><path d="M13.5 12.5c.8-2.4 2.5-3.8 4.5-4.2" {HL} stroke-width="2.4"/>')
I['golpe']=(f'<path d="M20 2.5l3.6 9.5 9.4-5-3.8 9.6 9.3 2.6-9 4.4 5.6 8.5-9.8-2.6-.6 10.3-5.3-8.6-6.8 7.8 1.2-10.2L3 27l7.4-6.5L2.5 14.5l10 .4L11 4.8l7 7.4z" fill="{N}" {S(2)}/>'
            f'<path d="M20 11l2 5.6 5.6-1.4-3.4 4.8 4.6 3.2-5.6.4.2 5.6-3.6-4.4-4 4 .8-5.6-5.4-1.6 5-2.6-2.4-5.2 5 2.6z" fill="{Y}"/>')
I['dulce']=(f'<path d="M12.5 15.5 4 10.5l1.2 9.5L4 29.5l8.5-5M27.5 15.5 36 10.5 34.8 20l1.2 9.5-8.5-5" fill="{Y}" {S(2)}/>'
            f'<circle cx="20" cy="20" r="9" fill="{P}" {S(2.2)}/><path d="M14 15.5c3 2.5 9 2.5 12 0M13 22c3 3 11 3 14 0" fill="none" stroke="{W}" stroke-width="2" stroke-linecap="round" opacity=".85"/>')
I['pinata']=(f'<path d="M20 3v4" {S(1.8)}/><path d="M20 7l3.8 8.4 9.2 1-6.9 6.2 2 9-8.1-4.6-8.1 4.6 2-9L7 16.4l9.2-1z" fill="{P}" {S(2.2)}/>'
             f'<path d="M11 17.5h18M13.5 23.5h13" stroke="{Y}" stroke-width="2.4" stroke-linecap="round"/><path d="M16 26.5l-2.6 10M20 27.5v10M24 26.5l2.6 10" stroke="{B}" stroke-width="2" stroke-linecap="round"/>'
             f'<path d="M20 7l3.8 8.4 9.2 1-6.9 6.2 2 9-8.1-4.6-8.1 4.6 2-9L7 16.4l9.2-1z" fill="none" {S(2.2)}/>')
I['engrane']=(f'<path d="M17.5 3.5h5l.9 4.5 3 1.3 3.9-2.6 3.5 3.5-2.6 3.9 1.3 3 4.5.9v5l-4.5.9-1.3 3 2.6 3.9-3.5 3.5-3.9-2.6-3 1.3-.9 4.5h-5l-.9-4.5-3-1.3-3.9 2.6-3.5-3.5 2.6-3.9-1.3-3L3.5 22.5v-5l4.5-.9 1.3-3-2.6-3.9 3.5-3.5 3.9 2.6 3-1.3z" fill="{GR}" {S(2.2)}/>'
              f'<circle cx="20" cy="20" r="5.6" fill="{W}" {S(2)}/>')
I['castillo']=(f'<path d="M6 35V18h-1.5v-5h4v2.5h2.5V13h4v5H13.5v3.5h13V18h-1.5v-5h4v2.5H31.5V13h4v5H34v17z" fill="{SA}" {S(2.2)}/>'
               f'<path d="M16 35v-6.5a4 4 0 0 1 8 0V35" fill="{M}" {S(1.8)}/><path d="M20 21.5V9" {S(1.8)}/><path d="M20 9h7l-2 2.4 2 2.4h-7z" fill="{R}" {S(1.6)}/><circle cx="10" cy="25" r="1.3" fill="{O}" opacity=".55"/><circle cx="30" cy="27" r="1.3" fill="{O}" opacity=".55"/>')
I['bola']=(f'<path d="M10 35.5l2.5-5.5h15l2.5 5.5z" fill="{M}" {S(2.2)}/><circle cx="20" cy="18" r="13.5" fill="{V}" {S(2.2)}/>'
           f'<path d="M12 15.5a8.5 8.5 0 0 1 6.5-6" {HL} stroke-width="2.6"/><circle cx="24.5" cy="22" r="1.6" fill="{W}" opacity=".7"/><circle cx="16" cy="24" r="1" fill="{W}" opacity=".6"/>')
I['canasta']=(f'<path d="M10.5 16c0-8 19-8 19 0" fill="none" stroke="{O}" stroke-width="5.6" stroke-linecap="round"/><path d="M10.5 16c0-8 19-8 19 0" fill="none" stroke="{M}" stroke-width="2.4" stroke-linecap="round"/>'
              f'<path d="M5 16h30l-3.4 18.5H8.4z" fill="{M}" {S(2.2)}/><path d="M7 22h26M8 28h24M14 16l1.2 18.5M20 16v18.5M26 16l-1.2 18.5" stroke="{O}" stroke-width="1.4" opacity=".55"/>')
I['luna']=f'<path d="M24.5 4.5a15.5 15.5 0 1 0 11 24.5A13 13 0 0 1 24.5 4.5z" fill="{Y}" {S(2.2)}/><circle cx="15" cy="24" r="2" fill="#e0b23a"/><circle cx="21" cy="30" r="1.4" fill="#e0b23a"/>'
I['brillos']=(f'<path d="M15 4c1.2 6.5 3 8.6 9 10-6 1.4-7.8 3.5-9 10-1.2-6.5-3-8.6-9-10 6-1.4 7.8-3.5 9-10z" fill="{Y}" {S(2)}/>'
              f'<path d="M29 19.5c.8 4 1.8 5 5.5 6-3.7 1-4.7 2-5.5 6-.8-4-1.8-5-5.5-6 3.7-1 4.7-2 5.5-6z" fill="{Y}" {S(1.8)}/><path d="M30.5 4.5c.5 2.4 1.1 3 3.3 3.6-2.2.6-2.8 1.2-3.3 3.6-.5-2.4-1.1-3-3.3-3.6 2.2-.6 2.8-1.2 3.3-3.6z" fill="{Y}" {S(1.6)}/>')
I['nube']=f'<path d="M10.5 31.5h20a7 7 0 0 0 .5-14 9.5 9.5 0 0 0-18 2.4 5.8 5.8 0 0 0-2.5 11.6z" fill="#eef6fd" {S(2.2)}/><path d="M17 15a6 6 0 0 1 5-3" {HL} stroke="#cfe3f5" opacity="1"/>'
I['bandeja']=(f'<path d="M5 22h8.5l2.5 4h8l2.5-4H35v10.5a2.5 2.5 0 0 1-2.5 2.5h-25A2.5 2.5 0 0 1 5 32.5z" fill="{GR}" {S(2.2)}/>'
              f'<path d="M20 4v13.5M14 12l6 6 6-6" fill="none" stroke="{O}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/><path d="M20 4v13.5M14 12l6 6 6-6" fill="none" stroke="{G}" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>')
I['pin']=f'<path d="M20 36s-11-12.5-11-20.5a11 11 0 0 1 22 0C31 23.5 20 36 20 36z" fill="{R}" {S(2.2)}/><circle cx="20" cy="15.5" r="4.4" fill="{W}" {S(1.8)}/>'
I['amigos']=(f'<path d="M23 34.5c0-5 2.6-8.5 7-8.5s7 3.5 7 8.5z" fill="{P}" {S(2)}/><circle cx="30" cy="19" r="5.2" fill="{P}" {S(2)}/>'
             f'<path d="M3 34.5c0-6.5 3.6-11 9.5-11s9.5 4.5 9.5 11z" fill="{B}" {S(2.2)}/><circle cx="12.5" cy="14.5" r="6.8" fill="{B}" {S(2.2)}/><path d="M9 12a3.6 3.6 0 0 1 2.4-2.4" {HL}/>')
I['estrella']=f'<path d="M20 3.5l4.9 10 11 1.6-8 7.7 1.9 10.9L20 28.6l-9.8 5.1 1.9-10.9-8-7.7 11-1.6z" fill="{Y}" {S(2.2)}/><path d="M17.5 13.5l-1.6 3.4" {HL}/>'
I['rompecabezas']=(f'<path d="M7 11h7.5a4 4 0 1 1 8 0H30v7.5a4 4 0 1 1 0 8V34h-7.5a4 4 0 1 0-8 0H7v-7.5a4 4 0 1 0 0-8z" fill="{G}" {S(2.2)}/><path d="M10.5 15v5" {HL}/>')
I['escalera']=(f'<path d="M11.5 3.5 8 36.5M28.5 3.5 32 36.5" stroke="{O}" stroke-width="5.6" stroke-linecap="round"/><path d="M11.5 3.5 8 36.5M28.5 3.5 32 36.5" stroke="{M}" stroke-width="2.4" stroke-linecap="round"/>'
               f'<path d="M10.8 10h18.4M10 18h20M9.2 26h21.6M8.5 33h23" stroke="{O}" stroke-width="5" stroke-linecap="round"/><path d="M10.8 10h18.4M10 18h20M9.2 26h21.6M8.5 33h23" stroke="{M}" stroke-width="2" stroke-linecap="round"/>')
I['herramientas']=(f'<path d="M8.5 33.5 27 15" stroke="{O}" stroke-width="6.2" stroke-linecap="round"/><path d="M8.5 33.5 27 15" stroke="{M}" stroke-width="2.8" stroke-linecap="round"/>'
                   f'<path d="M21 9.5 28.5 2l9 9-4 4-3-3-3 3-4-4 3-3z" fill="{GR}" {S(2)}/>'
                   f'<path d="M29.5 26.5a6 6 0 0 1 7 4.6l-3.5-.4-1.8 1.8.4 3.5a6 6 0 0 1-4.6-7L14 16a6 6 0 0 1-7-4.6l3.5.4 1.8-1.8-.4-3.5a6 6 0 0 1 4.6 7z" fill="{GR}" {S(1.8)}/>')
I['huella']=(f'<path d="M20 20.5c-5.5 0-10.5 6-10.5 9.8 0 3 2.4 4.4 5 4.4 2.2 0 3.4-1.1 5.5-1.1s3.3 1.1 5.5 1.1c2.6 0 5-1.4 5-4.4 0-3.8-5-9.8-10.5-9.8z" fill="{P}" {S(2.2)}/>'
             + ''.join(f'<ellipse cx="{x}" cy="{y}" rx="3.4" ry="4.4" transform="rotate({a} {x} {y})" fill="{P}" {S(2)}/>' for x,y,a in [(8,15,-25),(15,8.5,-8),(25,8.5,8),(32,15,25)]))
I['mapa']=(f'<path d="M4.5 8.5 14 5l12 4 9.5-3.5v26L26 35l-12-4-9.5 3.5z" fill="{SA}" {S(2.2)}/><path d="M14 5v26M26 9v26" stroke="{O}" stroke-width="1.6" opacity=".6"/>'
           f'<path d="M8 27c4-1 4-7 8.5-8s6 5 10.5 2.5 3-7 5-9" fill="none" stroke="{R}" stroke-width="2" stroke-dasharray="2.6 2.4" stroke-linecap="round"/><circle cx="31.5" cy="12" r="2.2" fill="{R}" {S(1.4)}/>')
I['grua']=(f'<path d="M9 35V7.5h4.5V35" fill="{Y}" {S(2)}/><path d="M9 13h27v4.5H9z" fill="{Y}" {S(2)}/><path d="M9 7.5l4.5 5.5M9 17.5l4.5 5M9 23l4.5 5.5M9 29l4.5 5" stroke="{O}" stroke-width="1.4"/>'
           f'<path d="M30 17.5v9" stroke="{O}" stroke-width="1.8"/><path d="M27.5 26.5h5l-1 3.5h-3z" fill="{GR}" {S(1.6)}/><path d="M4.5 13h4.5v4.5H4.5z" fill="{GR}" {S(1.8)}/><path d="M5 35.5h13" stroke="{O}" stroke-width="2.4" stroke-linecap="round"/>')

# emoji → ícono (sin el FE0F)
E={'⬆':'arriba','↑':'arriba','⬇':'abajo','↓':'abajo','←':'izq','→':'der','↕':'arribaabajo','▶':'play','✓':'check','✔':'check','✕':'cerrar','✖':'cerrar',
   '💧':'gota','💦':'gotas','🌊':'ola','🫧':'burbujas','🚿':'regadera','🪣':'cubeta','🏄':'tabla','🎒':'mochila','🔒':'candado','🔔':'timbre','🤖':'robot',
   '🏠':'casita','🔧':'llaveinglesa','✋':'mano','🫸':'empujar','🦵':'pierna','🥏':'disco','🌀':'remolino','🪀':'resorte','🔑':'llave','🚀':'cohete','🎯':'diana',
   '🪁':'papalote','🎈':'globo','💥':'golpe','🍬':'dulce','🪅':'pinata','⚙':'engrane','🏰':'castillo','🔮':'bola','🧺':'canasta','🌙':'luna','✨':'brillos',
   '☁':'nube','📥':'bandeja','📍':'pin','👥':'amigos','⭐':'estrella','🧩':'rompecabezas','🪜':'escalera','🛠':'herramientas','🐾':'huella','🗺':'mapa','🏗':'grua'}
NOM={'arriba':'Saltar / arriba','abajo':'Bajar','izq':'Atrás / izquierda','der':'Derecha','arribaabajo':'Subir y bajar','play':'Jugar','check':'Listo','cerrar':'Cerrar',
 'gota':'Gota','gotas':'Salpicar','ola':'Ola','burbujas':'Burbujas','regadera':'Regadera','cubeta':'Cubeta','tabla':'Tabla de surf','mochila':'Mochila','candado':'Candado',
 'timbre':'Timbre','robot':'Robot','casita':'Casa','llaveinglesa':'Llave inglesa','mano':'Agarrar','empujar':'Empujar','pierna':'Patear','disco':'Disco volador',
 'remolino':'Remolino','resorte':'Resorte','llave':'Llave','cohete':'Cohete','diana':'Diana','papalote':'Papalote','globo':'Globo','golpe':'Golpe','dulce':'Dulce',
 'pinata':'Piñata','engrane':'Ajustes','castillo':'Castillo / molde','bola':'Bola mágica','canasta':'Canasta','luna':'Luna','brillos':'Brillos','nube':'Nube',
 'bandeja':'Recibir','pin':'Lugar','amigos':'Amigos','estrella':'Estrella','rompecabezas':'Rompecabezas','escalera':'Escalera','herramientas':'Herramientas',
 'huella':'Mascotas','mapa':'Mapa','grua':'Construir'}
