# Íconos de la ronda 2 (pestañas y filtros de la tienda / Personalizar). Mismo estilo que la ronda 1.
from ic_r1 import S, O, R, B, Y, G, P, V, N, W, M, GR, SK, DB, SA, HL
I={}
BEAN='#9fd23c'
# el peluche (frijolito)
I['peluche']=(f'<path d="M12.5 27.5c-3.4 1.6-6 1-7-1M27.5 27.5c3.4 1.6 6 1 7-1" fill="none" stroke="{O}" stroke-width="5.6" stroke-linecap="round"/><path d="M12.5 27.5c-3.4 1.6-6 1-7-1M27.5 27.5c3.4 1.6 6 1 7-1" fill="none" stroke="{BEAN}" stroke-width="2.6" stroke-linecap="round"/>'
              f'<rect x="12.5" y="30" width="6" height="7.5" rx="3" fill="{BEAN}" {S(2)}/><rect x="21.5" y="30" width="6" height="7.5" rx="3" fill="{BEAN}" {S(2)}/>'
              f'<rect x="10.5" y="3" width="19" height="31" rx="9.5" fill="{BEAN}" {S(2.2)}/><ellipse cx="16.5" cy="13.5" rx="1.7" ry="2.6" fill="{O}"/><ellipse cx="23.5" cy="13.5" rx="1.7" ry="2.6" fill="{O}"/>'
              f'<path d="M17.5 18.5q2.5 2 5 0" fill="none" stroke="{O}" stroke-width="1.6" stroke-linecap="round"/><path d="M14 8a4.5 4.5 0 0 1 3-2.6" {HL}/>')
# paleta de pintor
I['paleta']=(f'<path d="M20 5C10.5 5 4 11 4 19c0 7.6 6 13.5 13.5 13.5 3.4 0 4.6-1.6 4-3.8-.6-2.4.4-4.4 3.2-4.4h3.6c4.4 0 7.7-2.8 7.7-7.2C36 10 28.5 5 20 5z" fill="#e8c48e" {S(2.2)}/>'
             f'<ellipse cx="13.5" cy="27" rx="3" ry="2.6" fill="#fbf4e6" {S(1.6)}/><circle cx="12" cy="17" r="3" fill="{R}" {S(1.4)}/><circle cx="18.5" cy="11" r="3" fill="{Y}" {S(1.4)}/><circle cx="26.5" cy="11.5" r="3" fill="{B}" {S(1.4)}/><circle cx="30.5" cy="18" r="2.7" fill="{G}" {S(1.4)}/>')
# bola de estambre
I['estambre']=(f'<path d="M30 31c3 2 5 2.5 7.5 1.5" fill="none" stroke="{O}" stroke-width="4.6" stroke-linecap="round"/><path d="M30 31c3 2 5 2.5 7.5 1.5" fill="none" stroke="#f07fae" stroke-width="2" stroke-linecap="round"/>'
               f'<circle cx="19" cy="20" r="14" fill="#f07fae" {S(2.2)}/>'
               f'<g fill="none" stroke="#c94f86" stroke-width="1.6" stroke-linecap="round"><path d="M8 14c6-1 14 2 18 8"/><path d="M6.5 21c6-1.5 14 1 20 9"/><path d="M12 31.5c1-7 6-14 15-18"/><path d="M17.5 33.5c0-6 4-12 13-14"/></g><path d="M11 12a10 10 0 0 1 6-4.5" {HL}/>')
# ojos
I['ojos']=(f'<ellipse cx="13" cy="20" rx="8" ry="11" fill="{W}" {S(2.2)}/><ellipse cx="27.5" cy="20" rx="8" ry="11" fill="{W}" {S(2.2)}/>'
           f'<ellipse cx="16" cy="22" rx="3.6" ry="4.6" fill="{O}"/><ellipse cx="30.5" cy="22" rx="3.6" ry="4.6" fill="{O}"/><circle cx="17.2" cy="20.4" r="1.2" fill="{W}"/><circle cx="31.7" cy="20.4" r="1.2" fill="{W}"/>')
# peinado (carita con su cabello)
I['peinado']=(f'<circle cx="20" cy="22" r="13" fill="{SK}" {S(2.2)}/>'
              f'<path d="M7 22c-1-10 5-17 13.5-17C29 5 34.5 11 33 22c-2-4-4.6-6-8-6.6 0 2-2 3.4-4.2 3.6 1-1.4 1.2-3 .6-4.4C17.5 18 12 19 7 22z" fill="#8a5a33" {S(2.2)}/>'
              f'<circle cx="15.5" cy="25" r="1.5" fill="{O}"/><circle cx="24.5" cy="25" r="1.5" fill="{O}"/><path d="M18 29.5q2 1.4 4 0" fill="none" stroke="{O}" stroke-width="1.4" stroke-linecap="round"/><path d="M14 10c2-1.6 4.6-2.4 7-2.2" {HL}/>')
# crayola (color de cabello)
I['crayon']=(f'<g transform="rotate(45 20 20)"><path d="M15 9h10v26H15z" fill="#f2847c" {S(2.2)}/><path d="M15 9l5-7.5L25 9z" fill="{R}" {S(2.2)}/>'
             f'<path d="M15 16h10M15 28h10" stroke="{O}" stroke-width="1.6"/><path d="M15 17.5h10v9H15z" fill="{W}" stroke="none" opacity=".85"/><path d="M17.5 20h5M17.5 23.5h5" stroke="{R}" stroke-width="1.6" stroke-linecap="round"/><path d="M15 9h10v26H15z" fill="none" {S(2.2)}/></g>')
# cejas
I['cejas']=(f'<path d="M5 13c3-3.5 7.5-4.6 12-2.6" fill="none" stroke="{O}" stroke-width="5" stroke-linecap="round"/><path d="M23 9.5c4.4-1.6 8.6-.4 12 3.6" fill="none" stroke="{O}" stroke-width="5" stroke-linecap="round"/>'
            f'<path d="M5 13c3-3.5 7.5-4.6 12-2.6" fill="none" stroke="#8a5a33" stroke-width="2" stroke-linecap="round"/><path d="M23 9.5c4.4-1.6 8.6-.4 12 3.6" fill="none" stroke="#8a5a33" stroke-width="2" stroke-linecap="round"/>'
            f'<ellipse cx="11.5" cy="23" rx="4.6" ry="6.2" fill="{W}" {S(2)}/><ellipse cx="28.5" cy="23" rx="4.6" ry="6.2" fill="{W}" {S(2)}/><circle cx="12.5" cy="24.5" r="2.6" fill="{O}"/><circle cx="29.5" cy="24.5" r="2.6" fill="{O}"/>')
# boca
I['boca']=(f'<path d="M5 14c5 2 25 2 30 0-1 11-7.6 17-15 17S6 25 5 14z" fill="#b8323c" {S(2.2)}/>'
           f'<path d="M8.5 15.6h23l-.6 3.4H9.1z" fill="{W}"/><path d="M12.5 27c2-4 13-4 15 0-2 2.4-4.6 3.4-7.5 3.4S14.5 29.4 12.5 27z" fill="#f28fa6"/><path d="M5 14c5 2 25 2 30 0-1 11-7.6 17-15 17S6 25 5 14z" fill="none" {S(2.2)}/>')
# mejillas (carita feliz chapeada)
I['mejillas']=(f'<circle cx="20" cy="20" r="15.5" fill="{Y}" {S(2.2)}/><path d="M11 17.5q3-3.4 6 0M23 17.5q3-3.4 6 0" fill="none" stroke="{O}" stroke-width="2" stroke-linecap="round"/>'
               f'<ellipse cx="10.5" cy="23.5" rx="3.6" ry="2.4" fill="#f59ab0"/><ellipse cx="29.5" cy="23.5" rx="3.6" ry="2.4" fill="#f59ab0"/><path d="M15 25q5 5 10 0" fill="none" stroke="{O}" stroke-width="2" stroke-linecap="round"/><path d="M10 12a11 11 0 0 1 5.6-4.6" {HL}/>')
# gato (orejitas)
I['gato']=(f'<path d="M6.5 16 7.5 3.5 17 10M33.5 16 32.5 3.5 23 10" fill="#f2a03d" {S(2.2)}/><path d="M9.5 12 10 7l4.4 3.4M30.5 12 30 7l-4.4 3.4" fill="#f59ab0"/>'
           f'<ellipse cx="20" cy="22" rx="15" ry="13" fill="#f2a03d" {S(2.2)}/><path d="M17 10.5l1.4 4M23 10.5l-1.4 4" stroke="#c9762a" stroke-width="2" stroke-linecap="round"/>'
           f'<ellipse cx="14" cy="21" rx="2" ry="2.8" fill="{O}"/><ellipse cx="26" cy="21" rx="2" ry="2.8" fill="{O}"/><path d="M18.4 25.5h3.2L20 27.4z" fill="#e5534b"/><path d="M20 27.4q-1.6 2.2-3.6 1M20 27.4q1.6 2.2 3.6 1" fill="none" stroke="{O}" stroke-width="1.3" stroke-linecap="round"/>'
           f'<path d="M3.5 24.5l7 .4M4 29l6.6-1.6M36.5 24.5l-7 .4M36 29l-6.6-1.6" stroke="{O}" stroke-width="1.2" stroke-linecap="round"/>')
# playera
I['playera']=(f'<path d="M14 5.5 4 10.5l3.4 8.5 4.6-2V35h16V17l4.6 2 3.4-8.5-10-5c-.6 2.6-3.2 4.4-6 4.4s-5.4-1.8-6-4.4z" fill="{B}" {S(2.2)}/>'
              f'<path d="M14 5.5c.6 2.6 3.2 4.4 6 4.4s5.4-1.8 6-4.4" fill="none" stroke="{O}" stroke-width="1.6"/><path d="M15.5 15v10" {HL}/>')
# pantalón
I['pantalon']=(f'<path d="M9.5 4.5h21l2.4 30.5h-9.2L20 15.5 16.3 35H7.1z" fill="{DB}" {S(2.2)}/><path d="M9.5 9.5h21" stroke="{O}" stroke-width="1.6"/>'
               f'<path d="M20 9.5v6M13 9.5c0 3 1.6 4.6 4 5M27 9.5c0 3-1.6 4.6-4 5" fill="none" stroke="#9cc6ef" stroke-width="1.4" stroke-dasharray="1.8 1.6" stroke-linecap="round"/><circle cx="20" cy="7" r="1.2" fill="{Y}"/>')
# tenis
I['tenis']=(f'<path d="M4 31.5c0-5 .6-9.5 2-13 1.6-3.6 6-3.6 7.4-.8 2.4 4.6 6 6 11.6 6.6 6.6.8 11 3.6 11 7.2v2.2H4z" fill="{R}" {S(2.2)}/>'
            f'<path d="M3.5 30.5h33v3.6a1.6 1.6 0 0 1-1.6 1.6H5.1a1.6 1.6 0 0 1-1.6-1.6z" fill="{W}" {S(2)}/><path d="M13.5 20.5l3.4-1.6M16 23.4l3.4-1.6M19 25.4l3-1.4" stroke="{W}" stroke-width="1.8" stroke-linecap="round"/><path d="M8 21.5c.4-1.6 1-2.6 2-3" {HL}/>')
# gorra
I['gorra']=(f'<path d="M5 26.5C5 15 11.5 8 20 8s14.5 6.5 15 15.5z" fill="{B}" {S(2.2)}/><path d="M20 8v15.5" stroke="{O}" stroke-width="1.4" opacity=".6"/>'
            f'<path d="M23 23.5c4-1.6 10-2.4 15 0-1.6 3.6-6 5-11 5-3 0-4.6-1.6-4-5z" fill="{DB}" {S(2.2)}/><circle cx="20" cy="7.6" r="2" fill="{Y}" {S(1.4)}/><path d="M10 17a10 10 0 0 1 5-6" {HL}/>')
# moño
I['mono']=(f'<path d="M20 19.5 6.5 10.5C4 9 2.5 10.5 3 13l1.6 7.6L3 27.4c-.4 2.4 1 3.8 3.4 2.6L20 21.5M20 19.5l13.5-9c2.5-1.5 4 0 3.5 2.5l-1.6 7.6 1.6 6.8c.4 2.4-1 3.8-3.4 2.6L20 21.5" fill="{P}" {S(2.2)}/>'
           f'<path d="M17.5 22l-4 12 3.6-1 2.4 3.2 1.4-13.4M22.5 22l4 12-3.6-1-2.4 3.2" fill="{P}" {S(1.8)}/><rect x="16.5" y="16.5" width="7" height="8" rx="2.6" fill="#f27aa8" {S(2)}/><path d="M7 14l2 5" {HL}/>')
# sudadera con gorro
I['sudadera']=(f'<path d="M13 9.5 5 13l-1.4 18 4.6 1L10 20v15.5h20V20l1.8 12 4.6-1L35 13l-8-3.5" fill="{N}" {S(2.2)}/>'
               f'<path d="M12.5 11.5C12 5.5 15.5 3.5 20 3.5s8 2 7.5 8c-1.6 3-4.6 4.6-7.5 4.6s-5.9-1.6-7.5-4.6z" fill="#f7b968" {S(2.2)}/><path d="M17.5 15.5v6M22.5 15.5v6" stroke="{W}" stroke-width="1.6" stroke-linecap="round"/>'
               f'<path d="M13.5 26.5h13v7h-13z" fill="#f7b968" {S(1.8)}/><path d="M15 6.5a6 6 0 0 1 3.4-1.6" {HL}/>')
# guante
I['guante']=(f'<path d="M11 26V12.5a2.8 2.8 0 0 1 5.6 0V10a2.8 2.8 0 0 1 5.6 0v1.4a2.8 2.8 0 0 1 5.6 0V17l1.4-1.6c1.6-1.8 4.6-.4 3.8 2.2L30 27.5z" fill="{G}" {S(2.2)}/>'
             f'<rect x="9.5" y="26" width="21.5" height="9" rx="2.6" fill="#a8dca6" {S(2.2)}/><path d="M12 29.5h16.5M12 32h16.5" stroke="{O}" stroke-width="1" opacity=".45"/><path d="M13.8 13v8" {HL}/>')
# calcetín
I['calcetin']=(f'<path d="M12 3.5h13v17.5l7 6.4c2.6 2.4 1.4 7.6-3 7.6h-6.6c-2.6 0-4.4-.8-6.2-2.6L12 28z" fill="{W}" {S(2.2)}/>'
               f'<path d="M12 3.5h13v4.6H12z" fill="{R}" {S(1.8)}/><path d="M12 13h13v3.6H12zM12 20.5h13.4l1.4 1.4" fill="{R}" stroke="none"/><path d="M23 33.5c1-3.6 4-5.6 7.6-5.4" fill="none" stroke="{R}" stroke-width="3"/>'
               f'<path d="M12 3.5h13v17.5l7 6.4c2.6 2.4 1.4 7.6-3 7.6h-6.6c-2.6 0-4.4-.8-6.2-2.6L12 28z" fill="none" {S(2.2)}/>')
# lentes de sol
I['lentesol']=(f'<path d="M3 15.5h34" stroke="{O}" stroke-width="3" stroke-linecap="round"/><path d="M4.5 15.5h13c0 7-2.6 11-7 11-4 0-6-4.6-6-11zM22.5 15.5h13c0 7-2 11-6 11-4.4 0-7-4-7-11z" fill="#3a3f4a" {S(2.2)}/>'
               f'<path d="M7.5 18.5l3.4 3.6M25.5 18.5l3.4 3.6" stroke="{W}" stroke-width="1.8" stroke-linecap="round" opacity=".6"/>')
# arcoíris
I['arcoiris']=(''.join(f'<path d="M{4+k*3} 29a{16-k*3} {16-k*3} 0 0 1 {32-k*6} 0" fill="none" stroke="{O}" stroke-width="5.4"/><path d="M{4+k*3} 29a{16-k*3} {16-k*3} 0 0 1 {32-k*6} 0" fill="none" stroke="{c}" stroke-width="3"/>' for k,c in enumerate([R,Y,G,B]))
               + f'<path d="M2.5 34.5h8a3.6 3.6 0 0 0 0-7.2 4 4 0 0 0-7.6 1A3 3 0 0 0 2.5 34.5zM29.5 34.5h8a3.6 3.6 0 0 0 .2-7.2 4 4 0 0 0-7.6 1 3 3 0 0 0-.6 6.2z" fill="{W}" {S(1.8)}/>')
# baile (frijolito bailando con notas)
I['baile']=(f'<path d="M12 18 4.5 9.5M28 18l7.5-8.5" fill="none" stroke="{O}" stroke-width="5.6" stroke-linecap="round"/><path d="M12 18 4.5 9.5M28 18l7.5-8.5" fill="none" stroke="{BEAN}" stroke-width="2.6" stroke-linecap="round"/>'
            f'<rect x="12" y="31" width="5.6" height="6.5" rx="2.8" fill="{BEAN}" {S(2)}/><rect x="22.4" y="31" width="5.6" height="6.5" rx="2.8" fill="{BEAN}" {S(2)}/>'
            f'<rect x="11" y="7" width="18" height="27.5" rx="9" fill="{BEAN}" {S(2.2)}/><path d="M15.5 15.5q1.4-1.6 2.8 0M21.7 15.5q1.4-1.6 2.8 0" fill="none" stroke="{O}" stroke-width="1.6" stroke-linecap="round"/><path d="M16.5 20q3.5 3 7 0" fill="{O}" stroke="{O}" stroke-width="1.4" stroke-linejoin="round"/>'
            f'<g fill="{V}" stroke="{O}" stroke-width="1.2"><ellipse cx="34" cy="25.5" rx="2.6" ry="2"/><path d="M36.3 25.2V17.5l2.4 1.4" fill="none" stroke-width="1.6"/><ellipse cx="5.5" cy="26.5" rx="2.4" ry="1.9"/><path d="M7.6 26.2v-6.6" fill="none" stroke-width="1.6"/></g>')
# cuadro (pantallas de carga)
I['cuadro']=(f'<rect x="3.5" y="6" width="33" height="28" rx="2.6" fill="{M}" {S(2.2)}/><rect x="8" y="10.5" width="24" height="19" fill="#bfe3f7" {S(1.6)}/>'
             f'<circle cx="26.5" cy="15.5" r="2.8" fill="{Y}"/><path d="M8 25l6-6.6 5 4.6 4-3 9 7.6v2H8z" fill="{G}"/><rect x="8" y="10.5" width="24" height="19" fill="none" {S(1.6)}/>')
# lentes
I['lentes']=(f'<path d="M14.5 19.5c2-2.4 9-2.4 11 0M2.5 16.5l2-1.4M37.5 16.5l-2-1.4" fill="none" stroke="{O}" stroke-width="2.4" stroke-linecap="round"/>'
             f'<circle cx="10" cy="21" r="6.6" fill="#dff1fb" stroke="{O}" stroke-width="3"/><circle cx="30" cy="21" r="6.6" fill="#dff1fb" stroke="{O}" stroke-width="3"/><path d="M7 19.5l2.4-2.4M27 19.5l2.4-2.4" stroke="{W}" stroke-width="1.8" stroke-linecap="round"/>')
# bufanda
I['bufanda']=(f'<ellipse cx="20" cy="15" rx="13" ry="6.5" fill="none" stroke="{O}" stroke-width="9.4"/><ellipse cx="20" cy="15" rx="13" ry="6.5" fill="none" stroke="{R}" stroke-width="5.6"/>'
              f'<path d="M9.5 16.5v4M15 18.6v4M21 19.4v4M27 18.6v4" stroke="{W}" stroke-width="2" opacity=".9"/>'
              f'<path d="M24 19.5 26 35h7.4l-2.6-16.4z" fill="{R}" {S(2.2)}/><path d="M25 24.5h6.6M25.6 29.5h6.8" stroke="{W}" stroke-width="2"/><path d="M27 35v2.4M29.6 35v2.4M32.2 35v2.4" stroke="{O}" stroke-width="1.6" stroke-linecap="round"/>')

E={'🧸':'peluche','🎨':'paleta','🧶':'estambre','👀':'ojos','💇':'peinado','🖍':'crayon','🤨':'cejas','👄':'boca','😊':'mejillas','🐱':'gato',
   '👕':'playera','👖':'pantalon','👟':'tenis','🧢':'gorra','🎀':'mono','🧥':'sudadera','🧤':'guante','🧦':'calcetin','🕶':'lentesol','🌈':'arcoiris',
   '💃':'baile','🖼':'cuadro','👓':'lentes','🧣':'bufanda'}
NOM={'peluche':'Cuerpo (peluche)','paleta':'Tono de piel','estambre':'Estambre (Amigurumi, suéteres)','ojos':'Ojos','peinado':'Peinado','crayon':'Color de cabello',
     'cejas':'Cejas','boca':'Boca','mejillas':'Mejillas','gato':'Orejitas','playera':'Arriba / camisas','pantalon':'Abajo','tenis':'Zapatos','gorra':'Gorros y gorras',
     'mono':'Accesorios / cabeza','sudadera':'Sudaderas','guante':'Guantes','calcetin':'Calcetines','lentesol':'Gafas','arcoiris':'Colores especiales',
     'baile':'Gestos','cuadro':'Pantallas de carga','lentes':'Filtro: cara','bufanda':'Filtro: cuello'}
