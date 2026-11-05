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
m=m.replace('</manifest>','    <uses-permission android:name="com.google.android.gms.permission.AD_ID" tools:node="remove"/>\n</manifest>');
must(m,/<activity[\s\S]*?android:name="[^"]*MainActivity"/,'MainActivity en el manifest');
m=m.replace(/(<activity\b)/, `$1\n            android:screenOrientation="${cfg.orientacion||'unspecified'}"`);
write(MF,m);

// ---- textos ----
const SF=path.join(RES,'values','strings.xml'); let s=read(SF);
s=s.replace(/<string name="app_name">[^<]*<\/string>/,'<string name="app_name">Mundo Peluche</string>')
   .replace(/<string name="title_activity_main">[^<]*<\/string>/,'<string name="title_activity_main">Mundo Peluche</string>')
   .replace('</resources>',`    <string name="admob_app_id">${cfg.admobAppId}</string>\n</resources>`);
write(SF,s);

// ---- MainActivity: pantalla completa y pantalla encendida mientras juegas ----
const pkg=cap.appId, JD=path.join(MAIN,'java',...pkg.split('.')); fs.mkdirSync(JD,{recursive:true});
for(const f of fs.readdirSync(JD)) if(/^MainActivity\.(java|kt)$/.test(f)) fs.rmSync(path.join(JD,f));
write(path.join(JD,'MainActivity.java'),`package ${pkg};

import android.os.Bundle;
import android.view.WindowManager;
import androidx.core.view.WindowCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.core.view.WindowInsetsControllerCompat;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        hideBars();
    }

    @Override
    public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus);
        if (hasFocus) hideBars();
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
  t=t.replace(/(<style name="AppTheme\.NoActionBarLaunch"[^>]*>)/,'$1\n        <item name="windowSplashScreenBackground">#cfe7f2</item>\n        <item name="windowSplashScreenAnimatedIcon">@mipmap/ic_launcher_foreground</item>'); write(ST,t); }
console.log('Android listo ·', pkg, '· versión', ver, '· anuncios', cfg.pruebas?'de PRUEBA':'reales');
