(() => {
  const rows = [
    ['Language','Langue','Idioma'],['Site language','Langue du site','Idioma del sitio'],
    ['Skip to content','Aller au contenu','Saltar al contenido'],['Main navigation','Navigation principale','Navegación principal'],['Footer','Pied de page','Pie de página'],['NOON Tech home','Accueil NOON Tech','Inicio de NOON Tech'],
    ['Our apps','Nos apps','Nuestras apps'],['Say hello','Contact','Contacto'],['Say hello.','Parlons-en.','Hablemos.'],['About','À propos','Quiénes somos'],['Contact','Contact','Contacto'],['Privacy','Confidentialité','Privacidad'],['Privacy.','Confidentialité.','Privacidad.'],
    ['INDEPENDENT LANGUAGE APP STUDIO','STUDIO INDÉPENDANT D’APPS LINGUISTIQUES','ESTUDIO INDEPENDIENTE DE APPS DE IDIOMAS'],
    ['Real language.','La langue vivante.','El idioma real.'],['Real character.','Du caractère.','Con carácter.'],
    ['We build language apps for the language','Des apps pour apprendre la langue','Creamos apps para aprender el idioma'],['people actually speak.','telle qu’on la parle vraiment.','que de verdad se habla.'],
    ['We build language apps for the language people actually speak.','Des apps pour apprendre la langue telle qu’on la parle vraiment.','Creamos apps para aprender el idioma que de verdad se habla.'],
    ['A little attitude. In every app.','Du caractère. Dans chaque app.','Un poco de actitud. En cada app.'],['THE NOON COLLECTION / 01—04','LA COLLECTION NOON / 01—04','LA COLECCIÓN NOON / 01—04'],
    ['Spanish · Real talk','Espagnol · La vraie vie','Español · Como se habla'],['Spanish · Conjugation','Espagnol · Conjugaison','Español · Conjugación'],['Yiddish · Coming soon','Yiddish · Bientôt disponible','Yidis · Próximamente'],['Spanish · False friends','Espagnol · Faux amis','Español · Falsos amigos'],
    ['Español que no te enseñan en clase.','L’espagnol qu’on ne t’apprend pas en cours.','Español que no te enseñan en clase.'],
    ['The words, expressions and attitude you won’t find in a textbook.','Les mots, les expressions et le ton que tu ne trouveras pas dans un manuel.','Las palabras, las expresiones y la actitud que no encontrarás en un libro de texto.'],
    ['Spanish conjugation, without the bullshit.','La conjugaison espagnole, sans le baratin.','La conjugación española, sin rollos.'],
    ['Make Spanish verbs part of your everyday life. One conjugation at a time.','Fais une place aux verbes espagnols dans ton quotidien. Une conjugaison à la fois.','Haz que los verbos españoles formen parte de tu día a día. Una conjugación cada vez.'],
    ['Yiddish. The useful words first.','Le yiddish. Les mots utiles d’abord.','Yidis. Primero, las palabras útiles.'],
    ['A little language. A lot of character. Discover the words that say it best.','Quelques mots. Beaucoup de caractère. Découvre ceux qui disent tout.','Pocas palabras. Mucho carácter. Descubre las que lo dicen todo.'],
    ['Las trampas del español.','Les pièges de l’espagnol.','Las trampas del español.'],
    ['Spot false friends, confusing sounds and regional meanings. Learn what Spanish really means, before it catches you out.','Repère les faux amis, les sons trompeurs et les sens qui changent selon les pays. Comprends vraiment l’espagnol avant de tomber dans le piège.','Detecta falsos amigos, sonidos engañosos y significados regionales. Entiende lo que realmente dice el español antes de caer en la trampa.'],
    ['Coming soon','Bientôt disponible','Próximamente'],['The download link will appear here when available.','Le lien de téléchargement apparaîtra ici dès qu’il sera disponible.','El enlace de descarga aparecerá aquí cuando esté disponible.'],
    ['Language has personality.','Les langues ont du caractère.','Los idiomas tienen personalidad.'],['Your apps should too.','Tes apps aussi.','Tus apps también.'],['Meet NOON Tech','Découvrir NOON Tech','Conoce NOON Tech'],['Small apps. Real language.','Petites apps. Langue vivante.','Pequeñas apps. Idioma real.'],
    ['Small studio.','Petit studio.','Pequeño estudio.'],['About NOON Tech','À propos de NOON Tech','Acerca de NOON Tech'],
    ['NOON Tech is an independent app studio exploring language with curiosity, practical tools and a little attitude. From everyday Spanish to expressive Yiddish, each app has its own personality.','NOON Tech est un studio indépendant qui explore les langues avec curiosité, des outils pratiques et du caractère. De l’espagnol du quotidien au yiddish expressif, chaque app a sa personnalité.','NOON Tech es un estudio independiente que explora los idiomas con curiosidad, herramientas prácticas y un poco de actitud. Del español cotidiano al expresivo yidis, cada app tiene su propia personalidad.'],
    ['Explore our apps ↗','Découvrir nos apps ↗','Explora nuestras apps ↗'],['Discover our apps','Découvrir nos apps','Descubre nuestras apps'],
    ['A question, an idea or something we should fix?','Une question, une idée ou quelque chose à corriger ?','¿Una pregunta, una idea o algo que debamos corregir?'],
    ['Write to NOON Tech. For app support, include the app name, your device model and a short description of what happened.','Écris à NOON Tech. Pour une demande d’assistance, précise le nom de l’app, le modèle de ton appareil et une courte description du problème.','Escribe a NOON Tech. Para solicitar ayuda, indica el nombre de la app, el modelo de tu dispositivo y una breve descripción del problema.'],
    ['Privacy information','Informations de confidentialité','Información de privacidad'],['Contact & support','Contact et assistance','Contacto y ayuda'],
    ['6 interface languages','6 langues d’interface','6 idiomas de interfaz'],['6 interface languages · prototype','6 langues d’interface · prototype','6 idiomas de interfaz · prototipo'],['2 languages · French & Spanish','2 langues · français et espagnol','2 idiomas · francés y español'],
    ['French, English, Spanish, German, Italian and Dutch. The language studied is Spanish.','Français, anglais, espagnol, allemand, italien et néerlandais. La langue étudiée est l’espagnol.','Francés, inglés, español, alemán, italiano y neerlandés. El idioma que se aprende es el español.'],
    ['French, English, Spanish, German, Italian and Dutch. Interface languages in the current prototype; the language studied is Yiddish.','Français, anglais, espagnol, allemand, italien et néerlandais. Langues d’interface du prototype actuel ; la langue étudiée est le yiddish.','Francés, inglés, español, alemán, italiano y neerlandés. Idiomas de interfaz del prototipo actual; el idioma que se aprende es el yidis.'],
    ['French and Spanish.','Français et espagnol.','Francés y español.'],
    ['About this website','À propos de ce site','Acerca de este sitio'],
    ['This static website does not use analytics scripts, advertising trackers, cookies or local storage. It has no account system or contact form.','Ce site statique n’utilise ni scripts d’analyse, ni traceurs publicitaires, ni cookies, ni stockage local. Il ne propose ni compte utilisateur ni formulaire de contact.','Este sitio estático no utiliza scripts de análisis, rastreadores publicitarios, cookies ni almacenamiento local. No dispone de cuentas de usuario ni de formulario de contacto.'],
    ['When hosted on GitHub Pages, GitHub processes technical request information, including IP addresses, to provide and secure hosting. See','Lors de l’hébergement sur GitHub Pages, GitHub traite des informations techniques de connexion, notamment les adresses IP, pour fournir et sécuriser l’hébergement. Consulte','Al alojar el sitio en GitHub Pages, GitHub trata información técnica de las solicitudes, incluidas las direcciones IP, para prestar y proteger el servicio. Consulta'],
    ['GitHub’s privacy statement','la déclaration de confidentialité de GitHub','la declaración de privacidad de GitHub'],['Contact by email','Contact par e-mail','Contacto por correo electrónico'],
    ['If you email NOON Tech, your email address and message are used to respond to your request. Please do not send passwords or sensitive personal information.','Si tu écris à NOON Tech, ton adresse e-mail et ton message servent à répondre à ta demande. N’envoie pas de mot de passe ni de données personnelles sensibles.','Si escribes a NOON Tech, tu dirección de correo y tu mensaje se utilizan para responder a tu solicitud. No envíes contraseñas ni información personal sensible.'],
    ['Our applications','Nos applications','Nuestras aplicaciones'],
    ['This notice covers the website only. App-specific privacy information will be published here when available. For questions about ¡JODER!, VOSOTROS, DREK! or TRAMPA,','Cette notice concerne uniquement le site. Les informations de confidentialité propres aux apps seront publiées ici dès qu’elles seront disponibles. Pour toute question sur ¡JODER!, VOSOTROS, DREK! ou TRAMPA,','Este aviso solo se aplica al sitio web. La información de privacidad de cada app se publicará aquí cuando esté disponible. Si tienes preguntas sobre ¡JODER!, VOSOTROS, DREK! o TRAMPA,'],
    ['contact NOON Tech','contacte NOON Tech','contacta con NOON Tech'],['Updated 6 September 2026','Mis à jour le 6 septembre 2026','Actualizado el 6 de septiembre de 2026'],
    ['App-specific privacy information is being prepared.','Les informations de confidentialité de cette app sont en préparation.','La información de privacidad de esta app está en preparación.'],
    ['for information about the app’s data practices.','pour en savoir plus sur le traitement des données par l’app.','para conocer cómo trata los datos la app.'],['Website privacy notice','Confidentialité du site','Privacidad del sitio web'],
    ['Lost in translation?','Perdu en chemin ?','¿Te has perdido?'],['This page could not be found.','Cette page est introuvable.','No se ha encontrado esta página.'],['Back to NOON Tech','Retour à NOON Tech','Volver a NOON Tech'],
    ['Get it on Google Play ↗','Disponible sur Google Play ↗','Disponible en Google Play ↗'],['Download on the App Store ↗','Télécharger sur l’App Store ↗','Descargar en App Store ↗'],
    ['Page not found · NOON Tech','Page introuvable · NOON Tech','Página no encontrada · NOON Tech'],['Say hello. · NOON Tech','Contact · NOON Tech','Contacto · NOON Tech'],['Privacy. · NOON Tech','Confidentialité · NOON Tech','Privacidad · NOON Tech'],['Language, with a little attitude · NOON Tech','Les langues ont du caractère · NOON Tech','Idiomas con carácter · NOON Tech']
  ];
  for (const name of ['¡JODER!','VOSOTROS','DREK!','TRAMPA']) {
    rows.push([`Discover ${name}`,`Découvrir ${name}`,`Descubre ${name}`]);
    rows.push([`${name} privacy`,`${name} : confidentialité`,`${name}: privacidad`]);
    rows.push([`${name} privacy · NOON Tech`,`${name} : confidentialité · NOON Tech`,`${name}: privacidad · NOON Tech`]);
    rows.push([`${name} privacy information`,`${name} : confidentialité`,`${name}: privacidad`]);
    rows.push([`The policy for ${name} is not yet published. Please`,`La politique de ${name} n’est pas encore publiée. Merci de`,`La política de ${name} todavía no está publicada. Puedes`]);
  }
  const dictionary = new Map(rows.map(r=>[r[0],{en:r[0],fr:r[1],es:r[2]}]));
  for(const r of window.NOON_EXTRA || []) dictionary.set(r[0], {...dictionary.get(r[0]),en:r[0],it:r[1],nl:r[2],de:r[3]});
  for(const r of window.NOON_JODER || []) dictionary.set(r[0], {en:r[0],fr:r[1],es:r[2],it:r[3],nl:r[4],de:r[5]});
  dictionary.get('Español que no te enseñan en clase.').en = 'Spanish they don’t teach you in class.';
  dictionary.get('Las trampas del español.').en = 'The traps of Spanish.';
  const nodes = [];
  const walker = document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
  while(walker.nextNode()) { const n=walker.currentNode; if(!n.parentElement.closest('script,style,option')) nodes.push([n,n.textContent]); }
  const attrs=[...document.querySelectorAll('[aria-label]')].map(e=>[e,e.getAttribute('aria-label')]);
  const title=document.title;
  const links=[...document.querySelectorAll('a[href]')].map(e=>[e,e.getAttribute('href')]);
  const select=document.querySelector('#site-language');
  function translate(s,lang){const k=s.trim();return dictionary.has(k)?s.replace(k,dictionary.get(k)[lang] || dictionary.get(k).en):s;}
  function apply(lang){
    document.documentElement.lang=lang;select.value=lang;
    for(const [n,s] of nodes)n.textContent=translate(s,lang);
    for(const [e,s] of attrs)e.setAttribute('aria-label',translate(s,lang));
    document.title=translate(title,lang);
    for(const e of document.querySelectorAll('[lang]:not(html)'))e.lang=lang;
    for(const [a,href] of links){const u=new URL(href,location.href);if(u.origin===location.origin&&u.pathname.startsWith('/noon-tech-site/')||u.origin===location.origin&&location.hostname==='127.0.0.1'){u.searchParams.set('lang',lang);a.href=u.href;}}
    document.querySelectorAll('.store a').forEach(a=>{const key=a.href.includes('play.google.com')?'Get it on Google Play ↗':'Download on the App Store ↗';a.textContent=translate(key,lang)});
  }
  const requested=new URL(location.href).searchParams.get('lang');
  let language=['fr','es','en','it','nl','de'].includes(requested)?requested:'fr';apply(language);
  select.addEventListener('change',()=>{language=select.value;const u=new URL(location.href);u.searchParams.set('lang',language);history.replaceState(null,'',u);apply(language)});
  document.addEventListener('store-ready',()=>apply(language));
})();
