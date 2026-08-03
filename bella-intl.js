/* Bella intl — currency (USD/CAD) + language (EN/FR/ES/ZH). Shared across pages.
   Unified render: each managed text node -> pick language text -> convert $ prices. Edit RATE + DICT here.
   Translations keep "$N" (US format) so the currency converter still finds prices. zh = machine draft, native review before launch. */
(function(){
  var RATE={USD:1, CAD:1.37};                 // edit the CAD rate here
  var DICT={
    // --- nav / chrome / CTAs (site-wide) ---
    "Services":{fr:"Services",es:"Servicios",zh:"服务"},
    "Pricing":{fr:"Tarifs",es:"Precios",zh:"价格"},
    "Lookbook":{fr:"Portfolio",es:"Portafolio",zh:"作品集"},
    "Resources":{fr:"Ressources",es:"Recursos",zh:"资源"},
    "Get started":{fr:"Commencer",es:"Comenzar",zh:"开始"},
    "Get Started":{fr:"Commencer",es:"Comenzar",zh:"开始"},
    "See before & afters":{fr:"Voir les avant/après",es:"Ver antes y después",zh:"查看前后对比"},
    "See the lookbook":{fr:"Voir le portfolio",es:"Ver el portafolio",zh:"查看作品集"},
    "See the partner program":{fr:"Voir le programme partenaire",es:"Ver el programa de socios",zh:"查看合作计划"},
    "Set up a brokerage account":{fr:"Créer un compte agence",es:"Crear una cuenta de agencia",zh:"创建经纪公司账户"},
    "Become a partner brokerage":{fr:"Devenir agence partenaire",es:"Ser agencia asociada",zh:"成为合作经纪公司"},
    "Start my order":{fr:"Commander",es:"Hacer mi pedido",zh:"开始下单"},
    "Take the quiz":{fr:"Faire le quiz",es:"Hacer el test",zh:"开始测试"},
    "Read the guide":{fr:"Lire le guide",es:"Leer la guía",zh:"阅读指南"},
    // --- homepage: hero ---
    "Real estate visualization studio":{fr:"Studio de visualisation immobilière",es:"Estudio de visualización inmobiliaria",zh:"房地产视觉工作室"},
    "Real estate visualization that sells listings":{fr:"La visualisation immobilière qui fait vendre vos inscriptions",es:"Visualización inmobiliaria que vende propiedades",zh:"让房源更快成交的房地产视觉呈现"},
    "for more.":{fr:"pour plus.",es:"por más.",zh:"卖得更高。"},
    "Bella Virtual is a real estate visualization studio. Our specialists handle virtual staging, 3D rendering, architectural visualization and 3D floor plans, showing buyers a property's full potential so listings market better, sell faster and earn a higher return. Real designers, never AI. MLS-ready in 24 to 48 hours, from $45 a photo.":{
      fr:"Bella Virtual est un studio de visualisation immobilière. Nos spécialistes réalisent le home staging virtuel, le rendu 3D, la visualisation architecturale et les plans d'étage 3D, montrant aux acheteurs tout le potentiel d'un bien pour que les inscriptions se démarquent, se vendent plus vite et rapportent davantage. De vrais designers, jamais d'IA. Prêt pour le MLS en 24 à 48 heures, à partir de $45 la photo.",
      es:"Bella Virtual es un estudio de visualización inmobiliaria. Nuestros especialistas se encargan del home staging virtual, el renderizado 3D, la visualización arquitectónica y los planos 3D, mostrando a los compradores todo el potencial de una propiedad para que las propiedades destaquen, se vendan más rápido y generen mayor retorno. Diseñadores reales, nunca IA. Listo para el MLS en 24 a 48 horas, desde $45 por foto.",
      zh:"Bella Virtual 是一家房地产视觉工作室。我们的专家提供虚拟布置、3D 渲染、建筑可视化和 3D 平面图，向买家展示房产的全部潜力，让房源更出众、成交更快、回报更高。真实的设计师，绝不使用 AI。24 至 48 小时内交付、符合 MLS 标准，每张照片 $45 起。"},
    "Real designers, never AI":{fr:"De vrais designers, jamais d'IA",es:"Diseñadores reales, nunca IA",zh:"真实设计师，绝不用 AI"},
    "24–48 hour delivery":{fr:"Livraison en 24–48 h",es:"Entrega en 24–48 h",zh:"24–48 小时交付"},
    "MLS-ready & AB 723":{fr:"Prêt pour le MLS et conforme AB 723",es:"Listo para MLS y AB 723",zh:"符合 MLS 与 AB 723"},
    "Rework or refund":{fr:"Retouche ou remboursement",es:"Corrección o reembolso",zh:"重做或退款"},
    // --- homepage: the math ---
    "The math":{fr:"Le calcul",es:"Las cuentas",zh:"算一算"},
    "Same result. A fraction of the cost.":{fr:"Même résultat. Une fraction du coût.",es:"Mismo resultado. Una fracción del costo.",zh:"同样的效果，成本低得多。"},
    "Physical staging":{fr:"Home staging physique",es:"Home staging físico",zh:"实体布置"},
    "Bella virtual staging":{fr:"Home staging virtuel Bella",es:"Home staging virtual Bella",zh:"Bella 虚拟布置"},
    // --- homepage: services / our team ---
    "Our team":{fr:"Notre équipe",es:"Nuestro equipo",zh:"我们的团队"},
    "Real estate visualization & marketing specialists in your corner.":{fr:"Des spécialistes de la visualisation et du marketing immobilier à vos côtés.",es:"Especialistas en visualización y marketing inmobiliario de tu lado.",zh:"专业的房地产视觉与营销团队，助您一臂之力。"},
    "Virtual staging":{fr:"Home staging virtuel",es:"Home staging virtual",zh:"虚拟布置"},
    "Furniture removal":{fr:"Retrait de meubles",es:"Eliminación de muebles",zh:"家具移除"},
    "Virtual renovation":{fr:"Rénovation virtuelle",es:"Renovación virtual",zh:"虚拟翻新"},
    "3D floor plans":{fr:"Plans d'étage 3D",es:"Planos 3D",zh:"3D 平面图"},
    "Day-to-dusk edits":{fr:"Effet jour vers crépuscule",es:"Edición de día a atardecer",zh:"日转黄昏修图"},
    "Virtual tours & 360°":{fr:"Visites virtuelles et 360°",es:"Recorridos virtuales y 360°",zh:"虚拟导览与 360°"},
    "3D renders":{fr:"Rendus 3D",es:"Renders 3D",zh:"3D 渲染图"},
    "Sky swaps & photo edits":{fr:"Remplacement de ciel et retouche",es:"Cambio de cielo y edición",zh:"换天与照片修饰"},
    // --- homepage: who we are ---
    "Who we are":{fr:"Qui nous sommes",es:"Quiénes somos",zh:"关于我们"},
    "Real estate pros who make you look like one.":{fr:"Des pros de l'immobilier qui vous font briller.",es:"Profesionales inmobiliarios que te hacen quedar como uno.",zh:"让您更显专业的房地产专家。"},
    "Bella isn't a software company. We're interior designers and real estate professionals who have staged thousands of residential and commercial properties, so we know exactly what buyers in your market are looking for. We turn your listing photos and other real estate media into visuals that stand out, showing the full potential of the property and painting the picture buyers are searching for. You walk into every appointment with a property that already looks sold.":{
      fr:"Bella n'est pas une entreprise de logiciels. Nous sommes des designers d'intérieur et des professionnels de l'immobilier qui ont mis en scène des milliers de biens résidentiels et commerciaux ; nous savons donc exactement ce que recherchent les acheteurs de votre marché. Nous transformons vos photos d'inscription et vos autres médias immobiliers en visuels qui se démarquent, révélant tout le potentiel du bien et dépeignant l'image que les acheteurs recherchent. Vous arrivez à chaque rendez-vous avec un bien qui semble déjà vendu.",
      es:"Bella no es una empresa de software. Somos diseñadores de interiores y profesionales inmobiliarios que hemos ambientado miles de propiedades residenciales y comerciales, así que sabemos exactamente qué buscan los compradores de tu mercado. Convertimos las fotos de tus propiedades y otros medios inmobiliarios en imágenes que destacan, mostrando todo el potencial de la propiedad y creando la imagen que los compradores buscan. Llegas a cada cita con una propiedad que ya parece vendida.",
      zh:"Bella 不是一家软件公司。我们是室内设计师和房地产专业人士，已为数千套住宅和商业物业完成布置，因此我们非常清楚您所在市场的买家想要什么。我们把您的房源照片和其他房地产素材，打造成脱颖而出的视觉呈现，展现物业的全部潜力，描绘出买家心中理想的画面。让您每次带看，都拿着一套看起来已经售出的物业。"},
    // --- homepage: sections ---
    "Completed jobs":{fr:"Projets réalisés",es:"Trabajos realizados",zh:"已完成项目"},
    "Real listings. Real outcomes.":{fr:"De vraies inscriptions. De vrais résultats.",es:"Propiedades reales. Resultados reales.",zh:"真实房源，真实成效。"},
    "In the press":{fr:"Dans la presse",es:"En la prensa",zh:"媒体报道"},
    "Staged in 48 hours. Sold in days.":{fr:"Mis en scène en 48 heures. Vendu en quelques jours.",es:"Ambientado en 48 horas. Vendido en días.",zh:"48 小时完成布置，几天内售出。"},
    // --- brokerages page ---
    "For brokerages & real estate teams":{fr:"Pour les agences et équipes immobilières",es:"Para agencias y equipos inmobiliarios",zh:"面向经纪公司与地产团队"},
    "Bella Partner Program":{fr:"Programme partenaire Bella",es:"Programa de socios Bella",zh:"Bella 合作计划"},
    "See the partner program":{fr:"Voir le programme partenaire",es:"Ver el programa de socios",zh:"查看合作计划"},
    // --- footer (shared) ---
    "Virtual land staging":{fr:"Aménagement virtuel de terrain",es:"Ambientación virtual de terreno",zh:"虚拟土地布置"},
    "3D rendering":{fr:"Rendu 3D",es:"Renderizado 3D",zh:"3D 渲染"},
    "Floor plans":{fr:"Plans d'étage",es:"Planos",zh:"平面图"},
    "Photo editing":{fr:"Retouche photo",es:"Edición de fotos",zh:"照片编辑"},
    "3D tours":{fr:"Visites 3D",es:"Recorridos 3D",zh:"3D 导览"},
    "Back to the studio":{fr:"Retour au studio",es:"Volver al estudio",zh:"返回工作室"}
  };
  var LANGS={en:1,fr:1,es:1,zh:1};
  var RX_PRICE=/\$\s?[\d,]+(?:\.\d+)?(?:\s?[–-]\s?\$?\s?[\d,]+(?:\.\d+)?)?/;
  var managed=[];

  function skip(p){ if(!p) return true; var t=p.nodeName; if(t==='SCRIPT'||t==='STYLE'||t==='TEXTAREA'||t==='OPTION'||t==='NOSCRIPT') return true; return !!(p.closest && p.closest('#bvIntl')); }
  function collectNodes(){
    var w=document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null), n;
    while(n=w.nextNode()){
      var t=n.nodeValue; if(!t||!t.trim()) continue; if(skip(n.parentNode)) continue;
      var key=t.replace(/\s+/g,' ').trim();
      var isI18n=!!DICT[key], isPrice=RX_PRICE.test(t);
      if(isI18n||isPrice) managed.push({node:n, en:t, key:isI18n?key:null, lead:(t.match(/^\s*/)||[''])[0], trail:(t.match(/\s*$/)||[''])[0]});
    }
  }
  function convertPrices(text,cur){
    var r=RATE[cur]||1; if(r===1) return text;
    return text.replace(new RegExp(RX_PRICE.source,'g'),function(tok){
      return tok.replace(/[\d,]+(?:\.\d+)?/g,function(num){ var v=parseFloat(num.replace(/,/g,'')); return isNaN(v)?num:Math.round(v*r).toLocaleString('en-US'); });
    });
  }
  function render(lang,cur){
    managed.forEach(function(m){
      var txt=m.en;
      if(lang!=='en' && m.key && DICT[m.key][lang]) txt=m.lead+DICT[m.key][lang]+m.trail;
      m.node.nodeValue=convertPrices(txt,cur);
    });
    document.documentElement.setAttribute('lang',lang);
  }
  function buildControl(){
    var css=document.createElement('style');
    css.textContent='#bvIntl{position:fixed;left:16px;bottom:16px;z-index:150;display:flex;gap:6px;align-items:center;background:rgba(253,252,250,.94);backdrop-filter:blur(8px);border:1px solid #E8E4DE;border-radius:99px;padding:5px 6px;box-shadow:0 10px 30px -14px rgba(20,18,16,.4);font-family:inherit}#bvIntl select{font-family:inherit;font-size:12px;color:#232120;background:transparent;border:0;border-radius:99px;padding:5px 8px;cursor:pointer;letter-spacing:.02em}#bvIntl select:focus{outline:2px solid #3E6B4C;outline-offset:1px}#bvIntl .bvsep{width:1px;height:16px;background:#E8E4DE}@media print{#bvIntl{display:none}}';
    document.head.appendChild(css);
    var box=document.createElement('div'); box.id='bvIntl'; box.setAttribute('role','group'); box.setAttribute('aria-label','Language and currency');
    box.innerHTML='<select id="bvLang" aria-label="Language"><option value="en">🌐 English</option><option value="fr">Français</option><option value="es">Español</option><option value="zh">中文</option></select><span class="bvsep"></span><select id="bvCur" aria-label="Currency"><option value="USD">$ USD</option><option value="CAD">$ CAD</option></select>';
    document.body.appendChild(box);
    return box;
  }
  function init(){
    buildControl();
    collectNodes();
    var curSel=document.getElementById('bvCur'), langSel=document.getElementById('bvLang');
    var cur=localStorage.getItem('bv_cur')||'USD', lang=localStorage.getItem('bv_lang')||'en';
    if(!RATE[cur]) cur='USD'; if(!LANGS[lang]) lang='en';
    curSel.value=cur; langSel.value=lang;
    render(lang,cur);
    curSel.addEventListener('change',function(){ localStorage.setItem('bv_cur',curSel.value); render(langSel.value,curSel.value); });
    langSel.addEventListener('change',function(){ localStorage.setItem('bv_lang',langSel.value); render(langSel.value,curSel.value); });
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init); else init();
})();
