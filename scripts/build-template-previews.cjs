const fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..'),page=path.join(root,'apps/kardash/templates/index.html');
const esc=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('"','&quot;');
const examples={
 recette:['','4','15','25','180','Tomates · 500 g\nPâtes · 400 g','1. Préparer les ingrédients\n2. Cuire puis servir','https://example.com/recette','Une idée pour le dîner.'],
 courses:['☐ Tomates · 500 g\n☐ Pain · 1\n☐ Pommes · 6','','Épicerie du quartier','Prévoir un sac.'],
 tache:['Préparer le sac de voyage','28/09/2026 · 18:00','Aucune','À faire','Chargeur, livre et écouteurs.'],
 'rendez-vous':['28/09/2026 · 14:30','12 rue Exemple, Ville Exemple','Camille Exemple','+33 …','','Arriver dix minutes avant.'],
 colis:['Transporteur exemple','EXEMPLE-001','https://example.com/suivi','30/09/2026','En attente',''],
 entretien:['Vélo de ville','01/09/2026','01/12/2026','Réglage des freins et des vitesses.','+33 …',''],
 'pret-objet':['Perceuse','Prêté','Camille Exemple','+33 …','27/09/2026','04/10/2026','En cours',''],
 'pret-argent':['Camille Exemple','Prêté','120','EUR','0','3','40','01/10/2026',''],
 note:['Idées pour le week-end\n• Balade au parc\n• Préparer un pique-nique','',''],
 mesures:['Étagère du salon','Format compact','—','80 cm','120 cm','30 cm',''],
 'etat-des-lieux':['12 rue Exemple, Ville Exemple','27/09/2026','Salon','Bon état','Petite marque sur le mur près de la fenêtre.','',''],
 piscine:['27/09/2026','—','—','—','Nettoyage du panier et relevés à compléter.','04/10/2026',''],
 inventaire:['Perceuse','OUTIL-001','1','Garage · étagère 2','','']
};
const icons={recipe:'◈',shopping:'☑',loan:'⇄',custom:'▤'};
let html=fs.readFileSync(page,'utf8'),count=0;
html=html.replace(/<article class="template-card">[\s\S]*?<\/article>/g,card=>{
 const id=card.match(/files\/([a-z-]+)\.json/)[1];const m=JSON.parse(fs.readFileSync(path.join(root,'apps/kardash/templates/files',id+'.json')));
 if(!examples[id]||examples[id].length!==m.fields.length)throw Error('Example/field mismatch '+id);
 const fields=m.fields.map((f,i)=>{let value;if(f.type==='photo')value='<div class="mock-photo"><span aria-hidden="true">▧</span><span>Emplacement photo</span></div>';else if(f.type==='file'||f.type==='scan')value='<div class="mock-file"><span aria-hidden="true">▤</span> Document exemple.pdf</div>';else value='<div class="mock-value">'+esc(examples[id][i])+'</div>';return '<div class="mock-field" data-field-id="'+esc(f.id)+'"><dt>'+esc(f.label)+'</dt><dd>'+value+'</dd></div>'}).join('');
 const mock='<figure class="kard-preview" data-template="'+id+'"><figcaption>Simulated preview · fictional examples</figcaption><div class="mock-kard" lang="fr" translate="no" style="--kard-color:'+esc(m.color)+'"><div class="mock-top"><span>KARD°ASH</span><span aria-hidden="true">•••</span></div><div class="mock-title"><span aria-hidden="true">'+icons[m.baseType]+'</span><strong>'+esc(m.name)+'</strong></div><dl tabindex="0" aria-label="Champs du modèle">'+fields+'</dl></div></figure>';
 count++;if(card.includes('<figure'))return card.replace(/<figure[\s\S]*?<\/figure>/,mock);return card.replace(/<details>[\s\S]*?<\/details>/,mock);
});
if(count!==13)throw Error('Unexpected template count '+count);
fs.writeFileSync(page,html);console.log(count+' previews generated from JSON with every field, in original order');
