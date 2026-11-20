// comprueba que los dibujos empacados se arman igual que los originales
const fs=require('fs'); const js=fs.readFileSync(process.argv[2],'utf8');
const m=js.match(/const EMI_SVG=(\{[\s\S]*?\});\nconst EMI_EMO/); const SVG=eval('('+m[1]+')'); const HL=js.match(/const EMI_HL='([^']*)'/)[1];
const exp=v=>v.replace(/~([\d.]+)~/g,'stroke="§" stroke-width="$1" stroke-linejoin="round" stroke-linecap="round"').replace(/¤/g,HL).replace(/§/g,'#5a4426');
const ref=JSON.parse(fs.readFileSync(process.argv[3],'utf8')); let bad=0; for(const k in ref){ if(exp(SVG[k])!==ref[k]){ bad++; if(bad<3) console.log('distinto',k); } } console.log('revisados',Object.keys(ref).length,'distintos',bad);
