# Íconos de la ronda 4 (avisos, tutoriales, zonas, minijuegos, huerto, taller de vehículos, libro de planetas…). Mismo estilo.
from ic_r1 import S, O, R, B, Y, G, P, V, N, W, M, GR, SK, DB, SA, HL
I={}
DG='#4f9a4a'; LG='#8bd47e'; BR='#8a5a33'
def circ(c): return f'<circle cx="20" cy="20" r="13.5" fill="{c}" {S(2.2)}/><path d="M13 15.5a8 8 0 0 1 4.6-4.4" {HL}/>'
def heart(c,extra=''): return f'<path d="M20 34.5S4.5 25 4.5 14.6C4.5 9.4 8.4 5.5 13 5.5c3.2 0 5.6 1.8 7 4.4 1.4-2.6 3.8-4.4 7-4.4 4.6 0 8.5 3.9 8.5 9.1C35.5 25 20 34.5 20 34.5z" fill="{c}" {S(2.2)}/><path d="M10 12.5a4.4 4.4 0 0 1 3.6-3" {HL}/>'+extra
# ---------- bajo el agua ----------
I['coral']=(f'<path d="M18 36V25c-4-1-7-4.6-7.6-10M18 27c4-.4 7-3 8-8M18 31c-6 0-10-3-11.4-7M26 19c.4-4 3-6 5.6-6.6M11 15c-1.6-3-1-6 1-8" fill="none" stroke="{O}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M18 36V25c-4-1-7-4.6-7.6-10M18 27c4-.4 7-3 8-8M18 31c-6 0-10-3-11.4-7M26 19c.4-4 3-6 5.6-6.6M11 15c-1.6-3-1-6 1-8" fill="none" stroke="#f2847c" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M6 36.5h28" stroke="{O}" stroke-width="2" stroke-linecap="round"/><circle cx="30" cy="31" r="2" fill="{Y}" {S(1.4)}/>')
I['hojas']=(f'<path d="M20 36C20 24 14 14 5 9c0 10 5 19 15 21M20 36c0-12 6-22 15-27 0 10-5 19-15 21M20 36V10" fill="{G}" {S(2.2)}/>'
            f'<path d="M20 36C20 24 14 14 5 9M20 36c0-12 6-22 15-27" fill="none" stroke="{O}" stroke-width="1.4" opacity=".5"/><path d="M20 36V6" stroke="{O}" stroke-width="2.2" stroke-linecap="round"/><path d="M20 30c0-8-2-14-6-20 4 4 6 10 6 20z" fill="{LG}"/>')
I['roca']=(f'<path d="M4 31.5 9 17l9-7 10 3 8 9 .5 9.5z" fill="{GR}" {S(2.2)}/><path d="M9 17l7 5 2-12M16 22l12-9M16 22l4 9.5M28 13l2 18.5" fill="none" stroke="{O}" stroke-width="1.4" opacity=".45"/><path d="M11 18l4-3" {HL}/>')
I['ancla']=(f'<circle cx="20" cy="7" r="3.6" fill="none" stroke="{O}" stroke-width="5.4"/><circle cx="20" cy="7" r="3.6" fill="none" stroke="{GR}" stroke-width="2.2"/>'
            f'<path d="M20 11v24M12.5 16h15M6 23c0 7 6.6 12 14 12s14-5 14-12" fill="none" stroke="{O}" stroke-width="6" stroke-linecap="round"/><path d="M20 11v24M12.5 16h15M6 23c0 7 6.6 12 14 12s14-5 14-12" fill="none" stroke="{GR}" stroke-width="2.8" stroke-linecap="round"/>'
            f'<path d="M3 26l3-4.6 3.6 4M37 26l-3-4.6-3.6 4" fill="{GR}" {S(1.8)}/>')
I['ballena']=(f'<path d="M3.5 24c0-8 7-13 15-13 9 0 14.5 6 15.5 10 1-2 2.4-4.6 4-5-.4 3.6-1 6.6-3 8.6 1.4 1.4 2.4 3.6 2.6 5.6-2.4-.6-4.4-2.4-5.6-4-2 6.6-7.6 9.6-14.6 9.6C9 35.8 3.5 31 3.5 24z" fill="{DB}" {S(2.2)}/>'
              f'<path d="M5 27c4 4 10 6 17 6" fill="none" stroke="#9cc6ef" stroke-width="2.4" stroke-linecap="round"/><circle cx="11" cy="21" r="1.7" fill="{O}"/><path d="M15 9.5c-1-2.4-.6-4.6 1-6.4M15 9.5c-2-1-4-1-5.6.6M15 9.5c2-1.4 4-1.4 6 0" fill="none" stroke="{B}" stroke-width="2" stroke-linecap="round"/>')
# ---------- minijuegos ----------
I['papa']=(f'<path d="M7 25c-3-6 1-15 9-17 6-1.6 13 0 16.6 5 3.6 5 2.4 13-3.6 17-6 4-18.6 2.6-22-5z" fill="#d9a35c" {S(2.2)}/>'
           f'<g fill="{BR}"><circle cx="14" cy="15" r="1.3"/><circle cx="24" cy="13" r="1.1"/><circle cx="27" cy="23" r="1.3"/><circle cx="16" cy="25" r="1.1"/></g><path d="M11 13a8 8 0 0 1 4-3" {HL}/>')
I['voleibol']=(f'<circle cx="20" cy="20" r="15.5" fill="{W}" {S(2.2)}/><g fill="none" stroke="{O}" stroke-width="1.8"><path d="M20 4.5c-2 6-1 11 3 15.5M23 20c-6 1.6-11 6-12 13.5M23 20c4.6 2.6 10 2.6 12.4-1.4"/><path d="M6.6 12c5 0 9 2 12 7"/></g>'
               f'<path d="M20 4.5c-2 6-1 11 3 15.5L35.4 18.6C34.8 10.6 28.4 4.5 20 4.5z" fill="{Y}" opacity=".85"/><path d="M11 33.5c1-7.5 6-11.9 12-13.5l12.4-1.4" fill="none" stroke="{O}" stroke-width="1.8"/><path d="M11 33.5A15.5 15.5 0 0 0 31 31l-8-11c-6 1.6-11 6-12 13.5z" fill="{B}" opacity=".8"/><circle cx="20" cy="20" r="15.5" fill="none" {S(2.2)}/>')
I['meta']=(f'<path d="M8 36V4" stroke="{O}" stroke-width="2.6" stroke-linecap="round"/><path d="M8 5h26v17H8z" fill="{W}" {S(2.2)}/>'
           + ''.join(f'<rect x="{8+c*6.5}" y="{5+r*5.66}" width="6.5" height="5.66" fill="{O}"/>' for r in range(3) for c in range(4) if (r+c)%2==0)
           + f'<path d="M8 5h26v17H8z" fill="none" {S(2.2)}/>')
I['coche']=(f'<path d="M4 27v-5.6c0-1.6 1-2.6 2.6-3L10.5 17l3.6-6.4c.6-1 1.6-1.6 2.6-1.6h9c1.2 0 2.2.6 2.8 1.6L32 17l2.6.6c1.6.4 2.6 1.6 2.6 3.2V27z" fill="{R}" {S(2.2)}/>'
            f'<path d="M14.5 17l2.6-5h4.4v5zM24 17v-5h3.6l2.6 5z" fill="#dff1fb" {S(1.6)}/><circle cx="11.5" cy="27.5" r="4.4" fill="#3d3f47" {S(2)}/><circle cx="28.5" cy="27.5" r="4.4" fill="#3d3f47" {S(2)}/><circle cx="11.5" cy="27.5" r="1.6" fill="{GR}"/><circle cx="28.5" cy="27.5" r="1.6" fill="{GR}"/><rect x="33" y="20" width="3" height="2.4" rx="1" fill="{Y}"/>')
I['manzana']=(f'<path d="M20 12c-3-2-10-2.6-12.6 3.4-2.4 6 .6 15 5.6 18.6 2.4 1.6 4.6.8 7 0 2.4.8 4.6 1.6 7 0 5-3.6 8-12.6 5.6-18.6C30 9.4 23 10 20 12z" fill="{R}" {S(2.2)}/>'
              f'<path d="M20 12c0-3 .6-5.4 2.4-7.4" fill="none" stroke="{O}" stroke-width="2.4" stroke-linecap="round"/><path d="M21.5 8c2-3 6-3.4 8-2.4-1.4 3-4.4 4-8 2.4z" fill="{G}" {S(1.6)}/><path d="M11.5 17a5 5 0 0 1 3-3" {HL}/>')
I['ostra']=(f'<path d="M4 24c0-9 7-15 16-15s16 6 16 15c-4 2-10 3-16 3S8 26 4 24z" fill="#b7a6c9" {S(2.2)}/><path d="M9 15.5l5 9M15.5 11l2.4 14.4M24.5 11l-2.4 14.4M31 15.5l-5 9" stroke="{O}" stroke-width="1.4" opacity=".5"/>'
            f'<path d="M4 24c4 6 9 9 16 9s12-3 16-9c-4 2-10 3-16 3S8 26 4 24z" fill="#cdbfdc" {S(2.2)}/><circle cx="20" cy="27" r="4" fill="{W}" {S(1.6)}/><path d="M18.4 25.6a2 2 0 0 1 1.4-1" stroke="#fff" stroke-width="1.2" fill="none"/>')
I['silla']=(f'<path d="M11 4.5h17a2 2 0 0 1 2 2v15H9v-15a2 2 0 0 1 2-2z" fill="{M}" {S(2.2)}/><path d="M14 8.5v9M20 8.5v9M26 8.5v9" stroke="{O}" stroke-width="1.6" opacity=".5"/>'
            f'<rect x="6.5" y="21" width="27" height="5" rx="2" fill="#e8b97a" {S(2.2)}/><path d="M9 26v10M31 26v10M13 26v6M27 26v6" stroke="{O}" stroke-width="2.6" stroke-linecap="round"/>')
I['escondidas']=(f'<circle cx="20" cy="21" r="14.5" fill="#e0a868" {S(2.2)}/><ellipse cx="20" cy="27" rx="9" ry="6.4" fill="#f5d2a6" {S(1.8)}/><path d="M16.5 29q3.5 2.4 7 0" fill="none" stroke="{O}" stroke-width="2" stroke-linecap="round"/>'
                 f'<path d="M5 13.5c3-3.4 9-3 11 1 1.6 3 .6 7-3 8.4-4 1.6-9 .4-9.6-3.4-.4-2.4.4-4.6 1.6-6z" fill="{SK}" {S(2)}/><path d="M35 13.5c-3-3.4-9-3-11 1-1.6 3-.6 7 3 8.4 4 1.6 9 .4 9.6-3.4.4-2.4-.4-4.6-1.6-6z" fill="{SK}" {S(2)}/>'
                 f'<path d="M7.5 15l4.6 2.4M6.4 18.4l5.6 1.4M28 17.4l4.6-2.4M28 19.8l5.6-1.4" stroke="{O}" stroke-width="1.4" stroke-linecap="round" opacity=".55"/><path d="M11 9a11 11 0 0 1 5-3" {HL}/>')
I['moneda']=(f'<circle cx="20" cy="20" r="15.5" fill="#f2b632" {S(2.2)}/><circle cx="20" cy="20" r="11" fill="{Y}" stroke="#d9952a" stroke-width="1.6"/>'
             f'<path d="M20 12.2l2.4 4.9 5.4.8-3.9 3.8.9 5.3-4.8-2.5-4.8 2.5.9-5.3-3.9-3.8 5.4-.8z" fill="#f2b632" stroke="#d9952a" stroke-width="1.2" stroke-linejoin="round"/><path d="M10 13a11 11 0 0 1 4.6-4.6" {HL}/>')
# ---------- huerto y frutas ----------
I['zanahoria']=(f'<path d="M29 11 7.5 33.5c-1 1-2.6 0-2-1.4L19.5 8c2.4-3 7-2.6 9.4.4 1 1.2 1 2.2.1 2.6z" fill="{N}" {S(2.2)}/><path d="M12 22.5l3 2.4M16 17.5l2.6 2M10 28l2 1.6" stroke="#c9762a" stroke-width="1.6" stroke-linecap="round"/>'
                f'<path d="M27.5 9.5c1-4 4-6 7-5.6-.4 3-2.6 5.6-6 6.6M28.5 10.5c3-1.6 6.6-1 8 1-2.6 1.6-5.6 1.4-8-.4M26.5 8.5c-.4-3 .6-6 3-7 .6 2.6-.4 5.4-2.4 7.4" fill="{G}" {S(1.8)}/>')
I['lechuga']=(f'<path d="M20 35.5c-9 0-15.5-5.6-15.5-13 0-3 1.4-4.4 1-7-.4-2.4 1.6-4 3.6-3.6 1-2.6 3.6-4 6-3 1.4-2.4 3.6-3.4 4.9-3.4s3.5 1 4.9 3.4c2.4-1 5 .4 6 3 2-.4 4 1.2 3.6 3.6-.4 2.6 1 4 1 7 0 7.4-6.5 13-15.5 13z" fill="{LG}" {S(2.2)}/>'
              f'<path d="M20 35c-6 0-10-4.4-10-10.4 0-4 2-6.6 4-8 2-1.4 4-1.4 6-1.4s4 0 6 1.4c2 1.4 4 4 4 8C30 30.6 26 35 20 35z" fill="#5cb85a" {S(1.8)}/><path d="M20 35V18M20 26l-5-4M20 29l5-4.4" fill="none" stroke="#e8f7c8" stroke-width="1.8" stroke-linecap="round"/><path d="M10 13.5a5 5 0 0 1 3-2" {HL}/>')
I['tomate']=(f'<circle cx="20" cy="22" r="13.5" fill="{R}" {S(2.2)}/><path d="M20 10.5l-3-4.4 1.6 4-5.6-1 4.4 2.4-4 2.4 6-.6.6 3.6 1-3.6 4 2.6-2.4-3.6 5.4-1-5.4-.4 2-3.4z" fill="{G}" {S(1.6)}/><path d="M12 19a8 8 0 0 1 3.4-4" {HL}/>')
I['maiz']=(f'<path d="M20 4c-5 0-7.6 7-7.6 15S15 35 20 35s7.6-8 7.6-16S25 4 20 4z" fill="{Y}" {S(2.2)}/>'
           f'<g stroke="#d9a52a" stroke-width="1.2"><path d="M13 13h14M12.6 18h14.8M12.8 23h14.4M14 28h12M17 8.5v24M23 8.5v24M20 4.5v30"/></g>'
           f'<path d="M20 35c-4-4-9-8-11-15 4 1 7 3 9 6M20 35c4-4 9-8 11-15-4 1-7 3-9 6" fill="{G}" {S(2)}/>')
I['fresa']=(f'<path d="M20 36c-6-3-13-11-13-19 0-4 3-6 6.6-6 2.4 0 4.4 1 6.4 1s4-1 6.4-1c3.6 0 6.6 2 6.6 6 0 8-7 16-13 19z" fill="{R}" {S(2.2)}/>'
            f'<g fill="{Y}"><ellipse cx="14" cy="18" rx=".9" ry="1.4"/><ellipse cx="20" cy="17" rx=".9" ry="1.4"/><ellipse cx="26" cy="18" rx=".9" ry="1.4"/><ellipse cx="17" cy="23" rx=".9" ry="1.4"/><ellipse cx="23" cy="23" rx=".9" ry="1.4"/><ellipse cx="20" cy="29" rx=".9" ry="1.4"/></g>'
            f'<path d="M20 12 14 9l3 4.4-6 .2 6.4 1.4L20 13l2.6 2 6.4-1.4-6-.2L26 9z" fill="{G}" {S(1.6)}/><path d="M20 12V5" stroke="{O}" stroke-width="2" stroke-linecap="round"/>')
I['calabaza']=(f'<path d="M20 11c-4-2-12-1-14.5 6-2 6 0 14 6 16.6 3 1.4 6 1 8.5-.6 2.5 1.6 5.5 2 8.5.6 6-2.6 8-10.6 6-16.6C32 10 24 9 20 11z" fill="{N}" {S(2.2)}/>'
               f'<path d="M20 11c-3 3-4 8-4 12s1 8 4 10.6c3-2.6 4-6.6 4-10.6s-1-9-4-12M12 13c-2 3-2.6 7-2 11M28 13c2 3 2.6 7 2 11" fill="none" stroke="#c9622a" stroke-width="1.6"/>'
               f'<path d="M20 11c0-3 1-5 3-6.6" fill="none" stroke="{O}" stroke-width="3.4" stroke-linecap="round"/><path d="M20 11c0-3 1-5 3-6.6" fill="none" stroke="{DG}" stroke-width="1.6" stroke-linecap="round"/>')
I['sandia']=(f'<path d="M3.5 13.5h33A16.5 16.5 0 0 1 3.5 13.5z" fill="{DG}" {S(2.2)}/><path d="M7 13.5h26A13 13 0 0 1 7 13.5z" fill="{W}"/><path d="M8.5 13.5h23a11.5 11.5 0 0 1-23 0z" fill="#f2665e"/>'
             f'<g fill="{O}"><ellipse cx="14" cy="17" rx=".9" ry="1.5"/><ellipse cx="20" cy="20" rx=".9" ry="1.5"/><ellipse cx="26" cy="17" rx=".9" ry="1.5"/><ellipse cx="17" cy="23" rx=".9" ry="1.5"/><ellipse cx="23" cy="23" rx=".9" ry="1.5"/></g><path d="M3.5 13.5h33" {S(2.2)}/>')
I['naranja']=(f'<circle cx="20" cy="21.5" r="13.5" fill="{N}" {S(2.2)}/><g fill="#e08a2a"><circle cx="15" cy="20" r=".9"/><circle cx="23" cy="17" r=".9"/><circle cx="26" cy="25" r=".9"/><circle cx="17" cy="28" r=".9"/></g>'
              f'<path d="M20 8.5c3-3 7-3.4 9.6-2-1.6 3-5.6 4-9.6 2z" fill="{G}" {S(1.6)}/><path d="M12 18a8 8 0 0 1 3.4-4" {HL}/>')
I['coco']=(f'<circle cx="20" cy="21" r="14" fill="{BR}" {S(2.2)}/><path d="M9 15c2-3 4-5 7-6M10 25c-1-3 0-6 1-8M26 9c3 1 6 4 7 7" fill="none" stroke="#5a3a1f" stroke-width="1.4" stroke-linecap="round"/>'
           f'<circle cx="16.5" cy="17" r="1.8" fill="#3a2414"/><circle cx="23.5" cy="17" r="1.8" fill="#3a2414"/><circle cx="20" cy="22.5" r="1.8" fill="#3a2414"/>')
I['mango']=(f'<path d="M27 8.5c6 3.4 8.6 11 5.6 18.4-3 7.4-11.6 10.6-18.6 7.6C7 31.6 4.6 24 7.6 17.4 11 10 20.4 4.8 27 8.5z" fill="#f7b632" {S(2.2)}/>'
            f'<path d="M27.6 10c4.6 3 6.4 9.4 4 15.4-1.2 3-3.2 5.2-5.6 6.4 1.6-4 1.2-9-1.4-13.4-1.6-2.8-2.4-5.6-1.4-8.4.8-.6 2.6-.6 4.4 0z" fill="{R}" opacity=".55"/>'
            f'<path d="M27 8.5c-.2-2.4.6-4.4 2.4-5.6" fill="none" stroke="{O}" stroke-width="2.2" stroke-linecap="round"/><path d="M29.2 4.6c3-1.6 6.6-1 8 1.4-2.8 1.6-6 1.4-8-1.4z" fill="{G}" {S(1.6)}/><path d="M11 18c1.4-3 3.6-5 6.4-6.4" {HL}/>')
I['platano']=(f'<path d="M30.5 5.5c2 9 0 17-5 22.5s-12 8-19 7.4c-1.6-.2-2-2-.6-2.6 6-2.6 11-6 14.4-11.6 3.4-5.6 4.6-10 5-15.4z" fill="{Y}" {S(2.2)}/>'
              f'<path d="M25.3 5.3l1.2-2.4 3.6.6.4 2z" fill="{BR}" {S(1.6)}/><path d="M25 12c-1 6-4 11-9 15" fill="none" stroke="#d9a52a" stroke-width="1.6" stroke-linecap="round"/><path d="M4.8 33.5l1.2 1.4" stroke="{O}" stroke-width="2.4" stroke-linecap="round"/>')
I['chocolate']=(f'<path d="M8 6h24v28H8z" fill="#7a4a2a" {S(2.2)}/><path d="M8 15.3h24M8 24.6h24M20 6v28" stroke="#5a3418" stroke-width="1.8"/><path d="M8 22l24-6v18H8z" fill="{R}" {S(2.2)}/><path d="M11 27h18" stroke="{W}" stroke-width="2" stroke-dasharray="3 2" opacity=".8"/>')
I['dona']=(f'<circle cx="20" cy="20" r="15" fill="#e2a35c" {S(2.2)}/><path d="M6.5 18c0-7 6-12.5 13.5-12.5S33.5 11 33.5 18c-1.6 2-3 .4-4.6 1.6-1.6 1.4-2.4-.6-4.4.4-2 1-3.4-.6-5 .6-1.6 1-3-.4-4.6.4-2 1-3-.8-4.6.4-1.6 1.2-2.6-.4-3.8-1.4z" fill="{P}" {S(1.8)}/>'
           f'<circle cx="20" cy="18" r="5" fill="#fbf4e6" {S(2)}/><path d="M11 11l2 1M27 10l-1 2M30 15l-2 .6M13 15.6l1.6-1M24 7.6l1.4 1" stroke="{W}" stroke-width="1.6" stroke-linecap="round"/><path d="M9 13l1.4-1.4M28.6 12.4l1 1" stroke="{B}" stroke-width="1.6" stroke-linecap="round"/>')
I['helado']=(f'<path d="M12 19h16l-8 17z" fill="#e8b97a" {S(2.2)}/><path d="M14 23l9 0M15.6 27h7M13 19l9 13M27 19l-9 13" stroke="#c48a4a" stroke-width="1.2"/>'
             f'<path d="M11 20c-3 0-4.6-3-3-5.4C6 9 10 5 14 6.6 15.6 3.4 19 2.6 22 3.6c3-.6 6 1 7 4 4 .4 5.6 4 4 7 1.4 2.6-.6 5.4-3 5.4z" fill="{P}" {S(2.2)}/><path d="M13 9.5a4 4 0 0 1 3-2" {HL}/><circle cx="24" cy="5" r="2" fill="{R}" {S(1.4)}/>')
I['taza']=(f'<path d="M28 17h3a5 5 0 0 1 0 10h-3.4" fill="none" stroke="{O}" stroke-width="5.4"/><path d="M28 17h3a5 5 0 0 1 0 10h-3.4" fill="none" stroke="{R}" stroke-width="2.4"/>'
           f'<path d="M6 14h23v10c0 6-4.6 10-11.5 10S6 30 6 24z" fill="{R}" {S(2.2)}/><ellipse cx="17.5" cy="14" rx="11.5" ry="2.6" fill="#7a4a2a" {S(1.8)}/>'
           f'<path d="M13 9c-1.6-2 1.6-3 0-5.4M18 9c-1.6-2 1.6-3 0-5.4M23 9c-1.6-2 1.6-3 0-5.4" fill="none" stroke="{GR}" stroke-width="1.8" stroke-linecap="round"/>')
I['cubiertos']=(f'<path d="M12 4v9.6a3 3 0 0 0 6 0V4M15 4v9M15 16.6V36" fill="none" stroke="{O}" stroke-width="5" stroke-linecap="round"/><path d="M12 4v9.6a3 3 0 0 0 6 0V4M15 4v9M15 16.6V36" fill="none" stroke="{GR}" stroke-width="2.2" stroke-linecap="round"/>'
                f'<path d="M27 36V22c-3.6-1-4-5-4-9.4C23 7 25 4 27 4s3 2 3 7v25" fill="{GR}" {S(2.2)}/>')
# ---------- colores (pinta el piso) ----------
I['circazul']=circ(B); I['circamarillo']=circ(Y); I['circmorado']=circ(V); I['circnaranja']=circ(N); I['circcafe']=circ(BR); I['circrojo']=circ(R)
I['corazonrosa']=heart('#f59ac0'); I['corazonceleste']=heart('#8fd6f2'); I['corazonverde']=heart(G)
I['corazonbrillo']=heart('#f2508e',f'<path d="M33 3.5l1 2.6 2.6 1-2.6 1-1 2.6-1-2.6-2.6-1 2.6-1z" fill="{Y}" {S(1.2)}/>')
I['rombo']=f'<path d="M20 3.5 35 20 20 36.5 5 20z" fill="{DB}" {S(2.2)}/><path d="M14 16l5-5.6" {HL}/>'
I['corazon']=heart(R)
# ---------- trofeos, medallas y premios ----------
I['trofeo']=(f'<path d="M13 5h14v9a7 7 0 0 1-14 0z" fill="{Y}" {S(2.2)}/><path d="M13 8H8a4 4 0 0 0 5 6.6M27 8h5a4 4 0 0 1-5 6.6" fill="none" stroke="{O}" stroke-width="5"/><path d="M13 8H8a4 4 0 0 0 5 6.6M27 8h5a4 4 0 0 1-5 6.6" fill="none" stroke="{Y}" stroke-width="2.2"/>'
             f'<path d="M18 21h4v6h-4z" fill="{Y}" {S(1.8)}/><rect x="12" y="27" width="16" height="7" rx="2" fill="{M}" {S(2.2)}/><path d="M16 8v5" {HL}/>')
def medalla(c,n):
    return (f'<path d="M12 3.5h6l4 12h-6zM28 3.5h-6l-4 12h6z" fill="{B}" {S(1.8)}/><path d="M22 3.5h6l-4 12h-6z" fill="{R}" {S(1.8)}/>'
            f'<circle cx="20" cy="25" r="11" fill="{c}" {S(2.2)}/><circle cx="20" cy="25" r="7.6" fill="none" stroke="{O}" stroke-width="1.2" opacity=".45"/>'
            f'<text x="20" y="29.6" text-anchor="middle" font-family="sans-serif" font-weight="900" font-size="12" fill="{O}">{n}</text>')
I['oro']=medalla('#f5cd4a','1'); I['plata']=medalla('#d6dbe2','2'); I['bronce']=medalla('#d8955a','3')
I['regalo']=(f'<rect x="5" y="16" width="30" height="20" rx="2" fill="{R}" {S(2.2)}/><rect x="3.5" y="11" width="33" height="7" rx="2" fill="#f2665e" {S(2.2)}/>'
             f'<path d="M17 11h6v25h-6z" fill="{Y}" {S(1.8)}/><path d="M20 11c-3-6-10-7-10-2.6 0 2.6 4 2.6 10 2.6zM20 11c3-6 10-7 10-2.6 0 2.6-4 2.6-10 2.6z" fill="{Y}" {S(2)}/>')
I['confeti']=(f'<path d="M4 36 11 13l16 16z" fill="{Y}" {S(2.2)}/><path d="M8.5 23.5l8 8M6.6 30l3.6 3.6" stroke="{R}" stroke-width="2.2"/><path d="M4 36 11 13l16 16z" fill="none" {S(2.2)}/>'
              f'<path d="M17 10c1-4 4-6 7-5M24 16c3-2 7-2 9 0M28 24c2-1 5 0 6 2" fill="none" stroke="{B}" stroke-width="2.2" stroke-linecap="round"/>'
              f'<circle cx="31" cy="8" r="1.8" fill="{P}"/><circle cx="21" cy="3.6" r="1.4" fill="{G}"/><circle cx="35" cy="16" r="1.4" fill="{R}"/><rect x="25" y="10" width="3" height="3" fill="{V}" transform="rotate(20 26.5 11.5)"/>')
I['nota']=(f'<path d="M15 29V8l17-4v20" fill="none" stroke="{O}" stroke-width="5" stroke-linejoin="round"/><path d="M15 29V8l17-4v20" fill="none" stroke="{V}" stroke-width="2.4" stroke-linejoin="round"/>'
           f'<path d="M15 8l17-4v5l-17 4z" fill="{V}" {S(1.8)}/><ellipse cx="10.5" cy="29.5" rx="5.4" ry="4.2" fill="{V}" {S(2.2)}/><ellipse cx="27.5" cy="24.5" rx="5.4" ry="4.2" fill="{V}" {S(2.2)}/>')
# ---------- vehículos y taller ----------
I['lancha']=(f'<path d="M3 21h34l-4.6 9.6c-.6 1.4-2 2.4-3.6 2.4H11c-1.6 0-3-.8-3.8-2.2z" fill="{W}" {S(2.2)}/><path d="M5 25h31" stroke="{R}" stroke-width="2.4"/>'
             f'<path d="M12 21l4-8h11l4 8" fill="#dff1fb" {S(2)}/><path d="M2 35c3 0 4-1.6 6.6-1.6S12 35 15 35s4-1.6 6.6-1.6S25 35 28 35s4-1.6 6.6-1.6S37 35 38 35" fill="none" stroke="{B}" stroke-width="2.2" stroke-linecap="round"/>')
I['avion']=(f'<path d="M20 3c1.6 0 2.6 2 2.6 5v8.6L36 24v3.6l-13.4-4.4V31l4 3v2.6L20 35l-6.6 1.6V34l4-3v-7.8L4 27.6V24l13.4-7.4V8c0-3 1-5 2.6-5z" fill="{W}" {S(2.2)}/>'
            f'<path d="M20 3c1.6 0 2.6 2 2.6 5v2h-5.2V8c0-3 1-5 2.6-5z" fill="{B}"/><path d="M8 25l5-2.6M32 25l-5-2.6" stroke="{R}" stroke-width="2" stroke-linecap="round"/>')
I['asiento']=(f'<path d="M12 5h12c2 0 3 1 3 3v15H10V8c0-2 1-3 2-3z" fill="{B}" {S(2.2)}/><path d="M8 23h22c1.6 0 2.6 1 2.6 2.6v2.4H7.4v-2.4C7.4 24 6.6 23 8 23z" fill="{DB}" {S(2.2)}/>'
              f'<path d="M12 28v8M27 28v8M12 32h15" stroke="{O}" stroke-width="2.4" stroke-linecap="round"/><path d="M14 9v9" {HL}/>')
I['camioneta']=(f'<path d="M3.5 28v-7c0-1.6 1-2.6 2.6-3l2.4-.6L12 9h17c1.6 0 2.6.6 3.2 2L35 17.6c1 .6 1.5 1.6 1.5 2.6V28z" fill="{G}" {S(2.2)}/>'
                f'<path d="M14 17.4l2.4-6h5v6zM24 17.4v-6h4.6l2.4 6z" fill="#dff1fb" {S(1.6)}/><circle cx="11" cy="28.5" r="4.6" fill="#3d3f47" {S(2)}/><circle cx="29" cy="28.5" r="4.6" fill="#3d3f47" {S(2)}/><circle cx="11" cy="28.5" r="1.6" fill="{GR}"/><circle cx="29" cy="28.5" r="1.6" fill="{GR}"/><path d="M12 7.5h16" stroke="{O}" stroke-width="2.2" stroke-linecap="round"/>')
I['kart']=(f'<path d="M5 26l3-7h15l4-4h6l2 4v7z" fill="{N}" {S(2.2)}/><path d="M16 19c0-4 2-6 5-6" fill="none" stroke="{O}" stroke-width="2.4" stroke-linecap="round"/><circle cx="21" cy="11" r="3.4" fill="{R}" {S(1.8)}/>'
           f'<circle cx="10" cy="28" r="5" fill="#3d3f47" {S(2)}/><circle cx="30" cy="28" r="5" fill="#3d3f47" {S(2)}/><circle cx="10" cy="28" r="1.8" fill="{GR}"/><circle cx="30" cy="28" r="1.8" fill="{GR}"/>')
I['tele']=(f'<rect x="3.5" y="9" width="33" height="23" rx="3.4" fill="{GR}" {S(2.2)}/><rect x="7" y="12.5" width="21" height="16" rx="2" fill="{B}" {S(1.8)}/><path d="M15.5 16.5v8l6-4z" fill="{W}"/>'
           f'<circle cx="32" cy="15" r="1.6" fill="{O}"/><circle cx="32" cy="20.5" r="1.6" fill="{O}"/><path d="M14 9 9 3.5M26 9l5-5.5" stroke="{O}" stroke-width="2.2" stroke-linecap="round"/><path d="M11 33v3M29 33v3" stroke="{O}" stroke-width="2.4" stroke-linecap="round"/>')
I['repetir']=(f'<path d="M7 18a11 11 0 0 1 19-7.4M33 22a11 11 0 0 1-19 7.4" fill="none" stroke="{O}" stroke-width="6.4" stroke-linecap="round"/><path d="M7 18a11 11 0 0 1 19-7.4M33 22a11 11 0 0 1-19 7.4" fill="none" stroke="{G}" stroke-width="3" stroke-linecap="round"/>'
              f'<path d="M23.5 4.5l7.6 1.4-2.4 7.4zM16.5 35.5l-7.6-1.4 2.4-7.4z" fill="{G}" {S(1.8)}/>')
I['dado']=(f'<rect x="5" y="5" width="30" height="30" rx="7" fill="{W}" {S(2.2)}/><g fill="{R}"><circle cx="13" cy="13" r="2.6"/><circle cx="27" cy="13" r="2.6"/><circle cx="20" cy="20" r="2.6"/><circle cx="13" cy="27" r="2.6"/><circle cx="27" cy="27" r="2.6"/></g>')
I['escoba']=(f'<path d="M30 4 19 21" stroke="{O}" stroke-width="5.6" stroke-linecap="round"/><path d="M30 4 19 21" stroke="{M}" stroke-width="2.6" stroke-linecap="round"/>'
             f'<path d="M15.5 18.5l8 5-1.6 2.6-8-5z" fill="{R}" {S(1.8)}/><path d="M13.9 21.1l8 5L15 37c-4-.4-9-3.6-11-7.4z" fill="{Y}" {S(2.2)}/><path d="M10 28l-3 4M14 30.4l-3 4.6M18 31.6l-2.6 4" stroke="#d9a52a" stroke-width="1.4" stroke-linecap="round"/>')
I['pulgar']=(f'<path d="M13.5 18h4.1l3.4-8c.6-1.6 1.4-4.6 1.4-6 2.6 0 5 1.6 5 5.4 0 2.6-.6 4.6-1.4 6.6h6.6c2.4 0 3.8 2 3.4 4.4l-2 11c-.4 2-2 3.6-4 3.6H13.5c-2 0-3.5-1.6-3.5-3.6V21.6c0-2 1.5-3.6 3.5-3.6z" fill="{SK}" {S(2.2)}/>'
             f'<path d="M28 21h7M27.6 26h6.4M27 31h6" stroke="{O}" stroke-width="1.4" opacity=".4" stroke-linecap="round"/><path d="M13.5 22v9" {HL} opacity=".5"/>')
I['sirena']=(f'<path d="M10 28V18a10 10 0 0 1 20 0v10" fill="{R}" {S(2.2)}/><path d="M15 18a5 5 0 0 1 5-5" {HL}/><rect x="6" y="28" width="28" height="7" rx="2" fill="{GR}" {S(2.2)}/>'
             f'<path d="M20 2.5v3.6M7 7l2.6 2.6M33 7l-2.6 2.6M2.5 18h3.6M34 18h3.6" stroke="{Y}" stroke-width="2.6" stroke-linecap="round"/>')
I['fantasma']=(f'<path d="M8 35V17C8 10 13.4 5 20 5s12 5 12 12v18l-4-3-4 3-4-3-4 3-4-3z" fill="{W}" {S(2.2)}/><ellipse cx="15.5" cy="17" rx="2" ry="3" fill="{O}"/><ellipse cx="24.5" cy="17" rx="2" ry="3" fill="{O}"/>'
               f'<ellipse cx="20" cy="24" rx="2.4" ry="2" fill="{O}"/><ellipse cx="11.5" cy="22" rx="2" ry="1.2" fill="#f59ab0"/><ellipse cx="28.5" cy="22" rx="2" ry="1.2" fill="#f59ab0"/>')
I['iman']=(f'<path d="M8 6h8v14a4 4 0 0 0 8 0V6h8v14a12 12 0 0 1-24 0z" fill="{R}" {S(2.2)}/><path d="M8 6h8v6H8zM24 6h8v6h-8z" fill="{GR}" {S(2)}/>'
           f'<path d="M3 4.5l3 3M5 2l1.6 3.6M37 4.5l-3 3M35 2l-1.6 3.6" stroke="{B}" stroke-width="1.8" stroke-linecap="round"/>')
I['carrusel']=(f'<path d="M4 13 20 4l16 9z" fill="{P}" {S(2.2)}/><path d="M4 13h32v3H4z" fill="{Y}" {S(1.8)}/><path d="M9 16v16M20 16v16M31 16v16" stroke="{O}" stroke-width="2"/>'
               f'<path d="M14 24c0-2 1.4-3 3-3h4c1.6 0 2.4-1.4 3-2.6l1 1.6-1 2.4v3.6h-1.6l-.4-2h-5.6l-.6 2H14z" fill="{W}" {S(1.6)}/><path d="M4 32h32v4H4z" fill="{M}" {S(2)}/>')
I['bandera']=(f'<path d="M9 36V4" stroke="{O}" stroke-width="2.6" stroke-linecap="round"/><path d="M9 5h22l-5 7 5 7H9z" fill="{R}" {S(2.2)}/><path d="M12 8v6" {HL}/>')
I['telescopio']=(f'<path d="M4 18l24-11 3 7-24 11z" fill="{B}" {S(2.2)}/><path d="M27 7.5l4-1.6 3 7-4 1.6z" fill="{DB}" {S(2)}/><path d="M17 20l-7 16M19 20l3 16M18 20l-1 16" stroke="{O}" stroke-width="2.4" stroke-linecap="round"/>'
                 f'<circle cx="18" cy="20" r="2.4" fill="{GR}" {S(1.6)}/>')
I['fuego']=(f'<path d="M20 36c-7.6 0-12.6-5-12.6-11.6 0-6 4-9 6-14 1.6 2.6 2 4.6 2 7 2-4 4-9 3-14.4 6 3.6 12 10 12 19.4C30.4 30 27 36 20 36z" fill="{N}" {S(2.2)}/>'
            f'<path d="M20 34c-3.6 0-6-2.4-6-5.6 0-3.4 2.4-5 4-8 1 2 1.4 3 1.4 4.6 1.4-1.6 3.4-3.6 3.6-6.6 2.4 2 3 5.4 3 8.4 0 4.6-2.4 7.2-6 7.2z" fill="{Y}"/>')
I['cuerda']=(f'<path d="M3 7 37 19" stroke="{O}" stroke-width="2.4" stroke-linecap="round"/><circle cx="20" cy="13" r="4" fill="{GR}" {S(2)}/><circle cx="20" cy="13" r="1.4" fill="{O}"/>'
             f'<path d="M20 17v8" stroke="{O}" stroke-width="2.4"/><path d="M11 26h18" stroke="{O}" stroke-width="6" stroke-linecap="round"/><path d="M11 26h18" stroke="{R}" stroke-width="3" stroke-linecap="round"/><path d="M14 32l4-3M26 32l-4-3" stroke="{O}" stroke-width="1.8" stroke-linecap="round" opacity=".5"/>')
I['palmera']=(f'<path d="M20 36c0-9 .6-16 3-22" fill="none" stroke="{O}" stroke-width="5" stroke-linecap="round"/><path d="M20 36c0-9 .6-16 3-22" fill="none" stroke="{M}" stroke-width="2.4" stroke-linecap="round"/>'
              f'<path d="M23 14c-5-4-12-3.6-15 .6 5-.4 9 .6 15-.6zM23 14c4-5 11-5 14.4-1-5 .4-9 2-14.4 1zM23 14c-3 3.6-7.6 5.6-11.6 5.6 2-4.6 6.6-6.6 11.6-5.6zM23 14c4.6 1.4 8 5 9 9.6-4.6-1.4-7.6-5-9-9.6zM23 14c0-4 1.6-8 5-10-.4 4-2 7.6-5 10z" fill="{G}" {S(1.8)}/>'
              f'<circle cx="21.5" cy="16" r="1.8" fill="{BR}"/><circle cx="24.5" cy="16.5" r="1.8" fill="{BR}"/><path d="M8 36h24" stroke="{O}" stroke-width="2" stroke-linecap="round"/>')
I['obra']=(f'<path d="M7 34V14M33 34V14" stroke="{O}" stroke-width="2.6" stroke-linecap="round"/><rect x="3" y="12" width="34" height="11" rx="1.6" fill="{W}" {S(2.2)}/>'
           f'<path d="M7 12l-4 5.6M14 12 7 23M22 12l-7 11M30 12l-7 11M37 14.6 31 23" stroke="{N}" stroke-width="3.4"/><rect x="3" y="12" width="34" height="11" rx="1.6" fill="none" {S(2.2)}/><circle cx="7" cy="9" r="2.4" fill="{N}" {S(1.4)}/><circle cx="33" cy="9" r="2.4" fill="{N}" {S(1.4)}/>')
I['corre']=(f'<circle cx="24" cy="7" r="4" fill="{SK}" {S(2)}/><path d="M23 13l-5 9 6 5-2 9M18 22l-7 2M21 15l-6-1-4 4M23 13l5 5 6-1" fill="none" stroke="{O}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M23 13l-5 9 6 5-2 9M18 22l-7 2M21 15l-6-1-4 4M23 13l5 5 6-1" fill="none" stroke="{B}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/><path d="M3 26h5M5 31h5" stroke="{O}" stroke-width="2" stroke-linecap="round" opacity=".6"/>')
I['cama']=(f'<path d="M4 34V12M36 34V22" stroke="{O}" stroke-width="2.8" stroke-linecap="round"/><rect x="4" y="22" width="32" height="8" rx="2" fill="{B}" {S(2.2)}/><rect x="6" y="17" width="10" height="6" rx="3" fill="{W}" {S(2)}/>'
           f'<path d="M15 22c0-3 2-4 5-4h12c2.4 0 4 1.6 4 4z" fill="{P}" {S(2)}/>')
I['puerta']=(f'<path d="M9 36V6a2 2 0 0 1 2-2h18a2 2 0 0 1 2 2v30" fill="{M}" {S(2.2)}/><rect x="13" y="9" width="14" height="10" rx="1.4" fill="#e8b97a" {S(1.6)}/><rect x="13" y="22" width="14" height="10" rx="1.4" fill="#e8b97a" {S(1.6)}/>'
             f'<circle cx="25" cy="21" r="1.8" fill="{Y}" {S(1.2)}/><path d="M5 36h30" stroke="{O}" stroke-width="2.4" stroke-linecap="round"/>')
I['piso']=(f'<path d="M3 24 20 14l17 10-17 10z" fill="{M}" {S(2.2)}/><path d="M11.5 19l17 10M20 14v0M28.5 19l-17 10M7.3 21.5l17 10M15.8 16.5l17 10" stroke="{O}" stroke-width="1.2" opacity=".45"/>'
           f'<path d="M3 24v3l17 10 17-10v-3l-17 10z" fill="#a8743f" {S(2)}/>')
# manos que señalan y saludan
MANO='M8 22V18a3 3 0 0 1 3-3h13V12a3 3 0 0 1 6 0v3.6c3.6.6 6 3.4 6 7v4c0 5-4 9-9 9H17c-5 0-9-4-9-9z'
# manita que señala (como 👉): solo la mano, con el dedo del mismo grueso que las otras manitas, el pulgar arriba y los dedos doblados
I['manoder']=(f'<path d="M12.5 16H33.6a2.6 2.6 0 0 1 0 5.2H25a2.2 2.2 0 0 1 0 4.4a2.2 2.2 0 0 1 0 4.4a2.2 2.2 0 0 1 -1 4.4H13.4c-3.4 0-6.2-2.8-6.2-6.2V21.3c0-2.9 2.4-5.3 5.3-5.3z" fill="{SK}" {S(2)}/>'
              f'<path d="M15 16.2c0-2.8 1.8-4.4 4.2-4.4h2.4c1.4 0 2.2 1.4 1.4 2.6l-1.2 1.8" fill="{SK}" {S(1.8)}/>'
              f'<path d="M17 21.2h8M19.4 25.6h5.6M19.6 30h5.4" stroke="{O}" stroke-width="1.5" stroke-linecap="round" opacity=".7"/>')
I['manoizq']=f'<g transform="translate(40 0) scale(-1 1)">{I["manoder"]}</g>'
I['manoabajo']=f'<g transform="rotate(90 20 20)">{I["manoder"]}</g>'
I['saludo']=(f'<path d="M12 21V11a2.6 2.6 0 0 1 5.2 0V19V8.5a2.6 2.6 0 0 1 5.2 0V19V10a2.6 2.6 0 0 1 5.2 0v10.5V15a2.5 2.5 0 0 1 5 0v8.5c0 7.5-5 12-11.4 12-4.6 0-7.4-2.4-9.8-6l-4.2-6.3c-1.4-2.1 1-4.4 3-3l2.6 1.8z" fill="{SK}" {S(2)}/>'
             f'<path d="M3.5 9c.6-2.4 2-4 4-5M5 14c-.4-1.6 0-3 1-4.4M34 3.5c2 .6 3.4 2 4 4" fill="none" stroke="{O}" stroke-width="2" stroke-linecap="round"/>')

I['chispa']=f'<path d="M20 3c1.4 9 3.4 12 14 17-10.6 5-12.6 8-14 17-1.4-9-3.4-12-14-17 10.6-5 12.6-8 14-17z" fill="{Y}" {S(2.2)}/><path d="M17.5 14l1.4-4" {HL}/>'
I['girar']=(f'<path d="M30.5 23A11 11 0 1 1 26 11" fill="none" stroke="{O}" stroke-width="6.4" stroke-linecap="round"/><path d="M30.5 23A11 11 0 1 1 26 11" fill="none" stroke="{B}" stroke-width="3" stroke-linecap="round"/>'
            f'<path d="M22.5 4.5l9.5 2-3.4 9z" fill="{B}" {S(2)}/>')
E={'🪸':'coral','🌿':'hojas','🪨':'roca','⚓':'ancla','🐋':'ballena','🥔':'papa','🏐':'voleibol','🏁':'meta','🚗':'coche','🍎':'manzana','🦪':'ostra','🪑':'silla','🙈':'escondidas',
   '🪙':'moneda','🥕':'zanahoria','🥬':'lechuga','🍅':'tomate','🌽':'maiz','🍓':'fresa','🎃':'calabaza','🍉':'sandia','🍊':'naranja','🥥':'coco','🥭':'mango','🍌':'platano',
   '🍫':'chocolate','🍩':'dona','🍦':'helado','☕':'taza','🍴':'cubiertos',
   '🩷':'corazonrosa','🔵':'circazul','🟡':'circamarillo','🟣':'circmorado','🟠':'circnaranja','🩵':'corazonceleste','💗':'corazonbrillo','🟤':'circcafe','🔷':'rombo','💚':'corazonverde','🔴':'circrojo','❤':'corazon',
   '🏆':'trofeo','🥇':'oro','🥈':'plata','🥉':'bronce','🎁':'regalo','🎉':'confeti','🎵':'nota','✅':'check',
   '🚤':'lancha','✈':'avion','💺':'asiento','🚙':'camioneta','🏎':'kart','📺':'tele','🔁':'repetir','🎲':'dado','🔎':'lupa','🧹':'escoba','👍':'pulgar','🚨':'sirena','👻':'fantasma',
   '🧲':'iman','🎠':'carrusel','🚩':'bandera','🔭':'telescopio','🔥':'fuego','🪢':'cuerda','🌴':'palmera','🚧':'obra','🏃':'corre','🛏':'cama','🚪':'puerta','🟫':'piso',
   '👉':'manoder','👈':'manoizq','👇':'manoabajo','👋':'saludo','♥':'corazon','♪':'nota','♫':'nota','✦':'chispa','✗':'cerrar','↻':'girar','⇄':'repetir'}
NOM={'coral':'Arrecife','hojas':'Algas / hojas','roca':'Cuevas','ancla':'Barco hundido','ballena':'Mar abierto','papa':'Papa caliente','voleibol':'Bola','meta':'Carrera / meta','coche':'Coche',
     'manzana':'Frutas','ostra':'Perlas','silla':'Cojines','escondidas':'Escondidas','moneda':'Monedas','zanahoria':'Zanahoria','lechuga':'Lechuga','tomate':'Tomate','maiz':'Maíz','fresa':'Fresa',
     'calabaza':'Calabaza','sandia':'Sandía','naranja':'Naranja','coco':'Coco','mango':'Mango','platano':'Plátano','chocolate':'Chocolate','dona':'Dona','helado':'Helado','taza':'Chocolate caliente',
     'cubiertos':'Se come','circazul':'Azul','circamarillo':'Amarillo','circmorado':'Morado','circnaranja':'Naranja','circcafe':'Café','circrojo':'Rojo','corazonrosa':'Rosa','corazonceleste':'Turquesa',
     'corazonbrillo':'Fucsia','rombo':'Azul marino','corazonverde':'Lima','corazon':'Me gusta','trofeo':'Trofeo','oro':'1er lugar','plata':'2º lugar','bronce':'3er lugar','regalo':'Regalo',
     'confeti':'¡Bien!','nota':'Música','lancha':'Agua (lancha)','avion':'Aire (avión)','asiento':'Asientos','camioneta':'Carrocería','kart':'Go-kart','tele':'Anuncio','repetir':'En par',
     'dado':'Color original','escoba':'Vaciar','pulgar':'¡Bien!','sirena':'Sirena','fantasma':'Fantasma / invisible','iman':'Imán','carrusel':'Carrusel','bandera':'Bandera','telescopio':'Descubierto',
     'fuego':'Lava','cuerda':'Tirolesa','palmera':'Selva','obra':'Ocupado','corre':'¡Escóndete!','cama':'Almohadita','puerta':'Puertas','piso':'Piso','manoder':'Mira a la derecha',
     'manoizq':'Mira a la izquierda','manoabajo':'Mira abajo','saludo':'¡Hola!','chispa':'Chispa','girar':'Girar'}
