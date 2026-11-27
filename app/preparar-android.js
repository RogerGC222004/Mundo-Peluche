// Ajusta el proyecto Android que crea Capacitor (npx cap add android) para Mundo Peluche:
// nombre, versión, AdMob (modo niños, sin identificador de publicidad), pantalla completa, pantalla siempre encendida,
// orientación, íconos, pantalla de carga y la firma con la llave de subida.
const fs=require('fs'), path=require('path');
const D=__dirname, A=path.join(D,'android'), APP=path.join(A,'app'), MAIN=path.join(APP,'src','main'), RES=path.join(MAIN,'res');
const cfg=JSON.parse(fs.readFileSync(path.join(D,'config.json'),'utf8'));
const cap=JSON.parse(fs.readFileSync(path.join(D,'capacitor.config.json'),'utf8'));
const game=fs.readFileSync(path.join(D,'..','fuente','mundo-peluche.html'),'utf8');
const ver=(/const GAME_VERSION='(\d+)'/.exec(game)||[])[1]; if(!ver) throw new Error('No encontré GAME_VERSION');
const read=f=>fs.readFileSync(f,'utf8'), write=(f,s)=>fs.writeFileSync(f,s);
const must=(s,re,what)=>{ if(!re.test(s)) throw new Error('No encontré '+what); };

// ---- AndroidManifest ----
const MF=path.join(MAIN,'AndroidManifest.xml'); let m=read(MF);
if(!m.includes('xmlns:tools=')) m=m.replace('<manifest ','<manifest xmlns:tools="http://schemas.android.com/tools" ');
must(m,/<application[\s\S]*?>/,'<application>');
m=m.replace(/(<application[\s\S]*?>)/, `$1\n        <meta-data android:name="com.google.android.gms.ads.APPLICATION_ID" android:value="@string/admob_app_id"/>`);
// juego para niños y familias: sin identificador de publicidad
// v246: tampoco «servicio en primer plano» (lo trae WorkManager por AdMob, pero el juego no lo usa; así Play no pide declararlo)
m=m.replace('</manifest>',['com.google.android.gms.permission.AD_ID','android.permission.ACCESS_ADSERVICES_AD_ID','android.permission.ACCESS_ADSERVICES_TOPICS','android.permission.ACCESS_ADSERVICES_ATTRIBUTION','android.permission.FOREGROUND_SERVICE']
  .map(p=>`    <uses-permission android:name="${p}" tools:node="remove"/>\n`).join('')
  // v248: el juego se ve en horizontal, pero no es un requisito del aparato (Play avisaba que eso esconde la app en algunos)
  +['android.hardware.screen.landscape','android.hardware.screen.portrait']
  .map(f=>`    <uses-feature android:name="${f}" android:required="false"/>\n`).join('')+'</manifest>');
must(m,/<activity[\s\S]*?android:name="[^"]*MainActivity"/,'MainActivity en el manifest');
m=m.replace(/(<activity\b)/, `$1\n            android:screenOrientation="${cfg.orientacion||'unspecified'}"`);
write(MF,m);

// ---- textos ----
const SF=path.join(RES,'values','strings.xml'); let s=read(SF);
// v255: el nombre de la app según el idioma del teléfono: en español «Mundo Peluche»; en cualquier otro idioma «Plush'N'Play»
s=s.replace(/<string name="app_name">[^<]*<\/string>/,'<string name="app_name">Plush\\\'N\\\'Play</string>')
   .replace(/<string name="title_activity_main">[^<]*<\/string>/,'<string name="title_activity_main">Plush\\\'N\\\'Play</string>')
   .replace('</resources>',`    <string name="admob_app_id">${cfg.admobAppId}</string>\n</resources>`);
write(SF,s);
{ const ES=path.join(RES,'values-es'); fs.mkdirSync(ES,{recursive:true});
  write(path.join(ES,'strings.xml'),'<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <string name="app_name">Mundo Peluche</string>\n    <string name="title_activity_main">Mundo Peluche</string>\n</resources>\n'); }

// ---- MainActivity: pantalla completa y pantalla encendida mientras juegas ----
const pkg=cap.appId, JD=path.join(MAIN,'java',...pkg.split('.')); fs.mkdirSync(JD,{recursive:true});
for(const f of fs.readdirSync(JD)) if(/^MainActivity\.(java|kt)$/.test(f)) fs.rmSync(path.join(JD,f));
write(path.join(JD,'MainActivity.java'),`package ${pkg};

import android.graphics.Color;
import android.graphics.drawable.ColorDrawable;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.view.WindowManager;
import android.webkit.WebView;
import androidx.activity.EdgeToEdge;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.core.view.WindowInsetsControllerCompat;
import com.getcapacitor.BridgeActivity;
import com.getcapacitor.WebViewListener;

public class MainActivity extends BridgeActivity {
    // v271: lo que tapan la cámara (el hoyito o la muesca) y las barras del teléfono, en píxeles del juego
    private float iTop = 0, iRight = 0, iBottom = 0, iLeft = 0;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        // v271: el tema de la pantalla de carga le ponía su imagen de fondo a TODAS las vistas: en algunos teléfonos se
        // veía el logo repetido en la franja de arriba. Al abrir el juego se cambia al tema normal (sin esa imagen).
        int t = getResources().getIdentifier("AppTheme.NoActionBar", "style", getPackageName());
        if (t != 0) setTheme(t);
        EdgeToEdge.enable(this);   // v256: Android 15 dibuja la app de borde a borde; así también se ve igual en versiones anteriores
        super.onCreate(savedInstanceState);
        getWindow().setBackgroundDrawable(new ColorDrawable(Color.rgb(0xcf, 0xe7, 0xf2)));   // v271: si algo se asoma, azul cielo liso
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        if (Build.VERSION.SDK_INT >= 28) {   // v271: el juego usa también el lado de la cámara (el juego deja ese espacio libre)
            WindowManager.LayoutParams lp = getWindow().getAttributes();
            lp.layoutInDisplayCutoutMode = Build.VERSION.SDK_INT >= 30
                ? WindowManager.LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_ALWAYS
                : WindowManager.LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES;
            getWindow().setAttributes(lp);
        }
        final WebView wv = bridge.getWebView();
        // v271: la letra grande del teléfono no agranda el juego (se salía de los menús y había que deslizar)
        wv.getSettings().setTextZoom(100);
        // v271: el juego ocupa toda la pantalla, sin márgenes; lo que tapan las barras y la cámara se le avisa al juego
        ViewCompat.setOnApplyWindowInsetsListener(wv, (v, ins) -> {
            fill(v);
            Insets c = ins.getInsets(WindowInsetsCompat.Type.displayCutout() | WindowInsetsCompat.Type.systemBars());
            float d = getResources().getDisplayMetrics().density;
            iTop = c.top / d; iRight = c.right / d; iBottom = c.bottom / d; iLeft = c.left / d;
            sendInsets();
            return WindowInsetsCompat.CONSUMED;
        });
        if (wv.getParent() instanceof View) {
            View p = (View) wv.getParent();
            ViewCompat.setOnApplyWindowInsetsListener(p, (v, ins) -> {
                fill(v);
                ViewCompat.dispatchApplyWindowInsets(wv, ins);
                return WindowInsetsCompat.CONSUMED;
            });
        }
        bridge.addWebViewListener(new WebViewListener() {
            @Override
            public void onPageLoaded(WebView w) { sendInsets(); }
        });
        hideBars();
        ViewCompat.requestApplyInsets(getWindow().getDecorView());
    }

    private void fill(View v) {
        v.setPadding(0, 0, 0, 0);
        ViewGroup.LayoutParams lp = v.getLayoutParams();
        if (lp instanceof ViewGroup.MarginLayoutParams) {
            ViewGroup.MarginLayoutParams m = (ViewGroup.MarginLayoutParams) lp;
            if (m.leftMargin != 0 || m.topMargin != 0 || m.rightMargin != 0 || m.bottomMargin != 0) { m.setMargins(0, 0, 0, 0); v.setLayoutParams(m); }
        }
    }

    private void sendInsets() {
        try {
            String js = "(function(){var s=document.documentElement.style;"
                + "s.setProperty('--sa-top','" + iTop + "px');s.setProperty('--sa-right','" + iRight + "px');"
                + "s.setProperty('--sa-bottom','" + iBottom + "px');s.setProperty('--sa-left','" + iLeft + "px');"
                + "window.dispatchEvent(new Event('resize'));})()";
            bridge.getWebView().post(() -> bridge.getWebView().evaluateJavascript(js, null));
        } catch (Exception e) { }
    }

    @Override
    public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus);
        if (hasFocus) { hideBars(); ViewCompat.requestApplyInsets(getWindow().getDecorView()); }
    }

    private void hideBars() {
        WindowInsetsControllerCompat c = WindowCompat.getInsetsController(getWindow(), getWindow().getDecorView());
        c.hide(WindowInsetsCompat.Type.systemBars());
        c.setSystemBarsBehavior(WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE);
    }
}
`);

// ---- versión y firma ----
const GF=path.join(APP,'build.gradle'); let g=read(GF);
must(g,/versionCode\s*=?\s*\d+/,"versionCode"); must(g,/versionName\s*=?\s*"[^"]*"/,"versionName");
g=g.replace(/versionCode\s*=?\s*\d+/,'versionCode '+ver).replace(/versionName\s*=?\s*"[^"]*"/,`versionName "${ver}"`);
must(g,/buildTypes\s*\{\s*release\s*\{/,'buildTypes.release');
g=g.replace(/android\s*\{/,`android {
    signingConfigs {
        debug {   // v148: el APK se firma con la llave privada del APK (secreto APK_LLAVE en GitHub); si no está, con la de prueba
            if (System.getenv("APK_LLAVE_ARCHIVO")) {
                storeFile file(System.getenv("APK_LLAVE_ARCHIVO"))
                storePassword System.getenv("APK_LLAVE_CLAVE")
                keyAlias "mundopelucheapk"
                keyPassword System.getenv("APK_LLAVE_CLAVE")
            } else {
                storeFile file("../../llave/prueba-debug.keystore")
                storePassword "android"
                keyAlias "androiddebugkey"
                keyPassword "android"
            }
        }
        release {
            if (System.getenv("LLAVE_ARCHIVO")) {
                storeFile file(System.getenv("LLAVE_ARCHIVO"))
                storePassword System.getenv("LLAVE_CLAVE")
                keyAlias System.getenv("LLAVE_ALIAS")
                keyPassword System.getenv("LLAVE_CLAVE")
            }
        }
    }`);
g=g.replace(/buildTypes\s*\{\s*release\s*\{/,'buildTypes {\n        release {\n            if (System.getenv("LLAVE_ARCHIVO")) signingConfig signingConfigs.release');
write(GF,g);

// ---- íconos y pantalla de carga ----
const R=path.join(D,'recursos','res');
const copyDir=(a,b)=>{ fs.mkdirSync(b,{recursive:true}); for(const f of fs.readdirSync(a)){ const p=path.join(a,f), q=path.join(b,f); if(fs.statSync(p).isDirectory()) copyDir(p,q); else fs.copyFileSync(p,q); } };
for(const dir of fs.readdirSync(RES)){ const p=path.join(RES,dir); if(!fs.statSync(p).isDirectory()) continue;
  for(const f of fs.readdirSync(p)) if(/^splash\.(png|xml|9\.png)$/.test(f) || (dir.startsWith('mipmap') && /^ic_launcher/.test(f))) fs.rmSync(path.join(p,f)); }
for(const f of ['ic_launcher_background.xml']){ const p=path.join(RES,'values',f); if(fs.existsSync(p)) fs.rmSync(p); }
copyDir(R,RES);
// Android 12 o más nuevo: color de fondo de la pantalla de carga
const ST=path.join(RES,'values','styles.xml'); if(fs.existsSync(ST)){ let t=read(ST);
  t=t.replace(/<item name="android:background">@drawable\/splash<\/item>/g,'<item name="android:windowBackground">@drawable/splash</item>');   // v271: antes se pintaba en cada vista (logo repetido)
  t=t.replace(/(<style name="AppTheme\.NoActionBar"[^>]*>)/,'$1\n        <item name="android:windowBackground">@color/mp_cielo</item>');
  write(path.join(RES,'values','mp_colores.xml'),'<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="mp_cielo">#cfe7f2</color>\n</resources>\n');
  t=t.replace(/(<style name="AppTheme\.NoActionBarLaunch"[^>]*>)/,'$1\n        <item name="windowSplashScreenBackground">#cfe7f2</item>\n        <item name="windowSplashScreenAnimatedIcon">@mipmap/ic_launcher_foreground</item>'); write(ST,t); }
console.log('Android listo ·', pkg, '· versión', ver, '· anuncios', cfg.pruebas?'de PRUEBA':'reales');
