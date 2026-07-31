#!/usr/bin/env python3
"""Generate the modern Bella furniture catalog (bella-lookbook.html) from the
SKU-named tiles in assets/lookbook/. SKU = {ROOM}-{BRAND}-{###}.
Re-run after adding/replacing tiles (e.g. hi-res originals, or the style catalogue)."""
import os, re, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
LB = ROOT/"assets"/"lookbook"

ROOM = {"LR":"Living Room","DR":"Dining Room","BDR":"Bedroom","BR":"Bedroom",
        "KI":"Kitchen","OF":"Office","EX":"Exterior"}
BRAND = {"ROVE":"Rove Concepts","SUNDAYS":"Sundays","MOB":"Mobital","GUS":"Gus*",
         "EM":"Eternity Modern","ROC":"Roche Bobois"}
# each brand carries a signature style (used for the Style filter; becomes richer
# once the style catalogue is ingested)
STYLE = {"ROVE":"Warm Modern","SUNDAYS":"Coastal","MOB":"Modern Minimal",
         "GUS":"Mid-Century","EM":"Contemporary","ROC":"Bold Luxe"}
BRAND_ORDER = ["ROVE","SUNDAYS","MOB","GUS","EM","ROC"]
ROOM_ORDER = ["LR","DR","BDR"]

items=[]
for f in sorted(os.listdir(LB)):
    if not f.lower().endswith(".jpg"): continue
    sku=f[:-4]
    m=re.match(r'^(LR|DR|BDR|BR|KI|OF|EX)-([A-Z]+)-(\d+)$', sku)
    if not m:
        print("SKIP (unparsed):",sku); continue
    room,brand,num=m.group(1),m.group(2),int(m.group(3))
    items.append({"sku":sku,"img":f"assets/lookbook/{f}",
                  "room":ROOM.get(room,room),"roomCode":room,
                  "brand":BRAND.get(brand,brand),"brandCode":brand,
                  "style":STYLE.get(brand,"Modern"),"num":num})

def sortkey(it):
    return (BRAND_ORDER.index(it["brandCode"]) if it["brandCode"] in BRAND_ORDER else 99,
            ROOM_ORDER.index(it["roomCode"]) if it["roomCode"] in ROOM_ORDER else 99, it["num"])
items.sort(key=sortkey)

# filter option lists (preserve intended order)
brands=[BRAND[b] for b in BRAND_ORDER if any(i["brandCode"]==b for i in items)]
rooms=[ROOM[r] for r in ROOM_ORDER if any(i["roomCode"]==r for i in items)]
styles_order=["Warm Modern","Coastal","Modern Minimal","Mid-Century","Contemporary","Bold Luxe"]
styles=[s for s in styles_order if any(i["style"]==s for i in items)]

DATA=json.dumps(items, separators=(",",":"))

HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Furniture Catalog | Lookbook 2025 by Room, Style &amp; Brand | Bella Virtual</title>
<meta name="description" content="Browse Bella's 2025 furniture catalog of designer-staged room sets by room, style and brand — Rove Concepts, Sundays, Mobital, Gus*, Eternity Modern and Roche Bobois. Copy a SKU and send it with your order.">
<link rel="canonical" href="https://www.bellavirtual.com/lookbook">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500&display=swap" rel="stylesheet">
<style>
  :root{--bg:#FDFCFA;--ink:#232120;--soft:#6E6A66;--faint:#9C978F;--line:#E8E4DE;--line-2:#F0EDE8;--dark:#1C1A18;--green:#3E6B4C;--gold:#B8985A;--wash:#FAF8F5;--pad:40px}
  *{box-sizing:border-box;margin:0;padding:0}
  html{scroll-behavior:smooth}
  body{background:var(--bg);color:var(--ink);font-family:"Jost",system-ui,sans-serif;font-weight:300;font-size:16px;line-height:1.6;-webkit-font-smoothing:antialiased}
  img{display:block;max-width:100%}a{text-decoration:none;color:inherit}
  h1,h2,h3{font-weight:300;letter-spacing:-.012em;line-height:1.1}
  .micro{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--faint)}
  .wrap{max-width:1400px;margin:0 auto;padding:0 var(--pad)}
  .btn{display:inline-block;background:var(--ink);color:#fff;font-size:12.5px;letter-spacing:.14em;text-transform:uppercase;padding:13px 22px;cursor:pointer;border:0;font-family:inherit;transition:background .2s}
  .btn:hover{background:var(--green)}
  header{position:sticky;top:0;z-index:70;background:rgba(253,252,250,.9);backdrop-filter:blur(10px);border-bottom:1px solid var(--line-2)}
  .nav{display:flex;align-items:center;gap:34px;height:64px;padding:0 var(--pad);max-width:1400px;margin:0 auto}
  .mark{font-size:15px;letter-spacing:.5em;font-weight:400}.nav .sp{margin-left:auto}
  .nav a.lnk{font-size:12.5px;letter-spacing:.13em;text-transform:uppercase;color:var(--soft)}.nav a.lnk:hover{color:var(--ink)}
  @media(max-width:820px){.nav a.lnk{display:none}}
  /* hero */
  .hero{padding:52px 0 30px;border-bottom:1px solid var(--line)}
  .hero .eyebrow{color:var(--green);font-weight:600}
  .hero h1{font-size:clamp(30px,4vw,50px);margin:12px 0 0;max-width:20ch}
  .hero p{color:var(--soft);margin-top:16px;max-width:60ch;font-size:16.5px}
  .hero .tip{margin-top:16px;font-size:14px;color:var(--ink);background:var(--wash);border:1px solid var(--line);border-radius:10px;padding:12px 16px;display:inline-flex;gap:9px;align-items:flex-start;max-width:60ch}
  .hero .tip b{font-weight:500}
  /* toolbar */
  .bar{position:sticky;top:64px;z-index:60;background:rgba(253,252,250,.94);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
  .bar-in{max-width:1400px;margin:0 auto;padding:14px var(--pad)}
  .search{display:flex;align-items:center;gap:10px;border:1px solid var(--line);border-radius:10px;padding:10px 14px;background:#fff;max-width:420px}
  .search svg{width:16px;height:16px;stroke:var(--faint);fill:none;stroke-width:1.6}
  .search input{border:0;outline:0;font-family:inherit;font-size:14.5px;width:100%;color:var(--ink);background:transparent}
  .frow{display:flex;gap:8px;align-items:center;flex-wrap:nowrap;overflow-x:auto;margin-top:12px;padding-bottom:2px;scrollbar-width:thin}
  .frow::-webkit-scrollbar{height:5px}.frow::-webkit-scrollbar-thumb{background:var(--line);border-radius:9px}
  .flabel{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--faint);flex:0 0 auto;margin-right:2px}
  .chip{flex:0 0 auto;font-family:inherit;font-size:13px;border:1px solid var(--line);background:#fff;color:var(--soft);padding:7px 14px;border-radius:99px;cursor:pointer;white-space:nowrap;transition:all .15s}
  .chip:hover{border-color:var(--ink);color:var(--ink)}
  .chip.on{background:var(--ink);color:#fff;border-color:var(--ink)}
  .chip .c{opacity:.55;font-size:11.5px;margin-left:5px}
  .barfoot{display:flex;justify-content:space-between;align-items:center;margin-top:12px;gap:16px;flex-wrap:wrap}
  .count{font-size:13px;color:var(--soft)}.count b{color:var(--ink);font-weight:500}
  .clear{font-size:12.5px;letter-spacing:.06em;color:var(--green);background:0;border:0;cursor:pointer;font-family:inherit}
  .clear:hover{color:var(--ink)}
  /* grid */
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:22px;padding:34px 0 70px}
  .card{background:#fff;border:1px solid var(--line);border-radius:12px;overflow:hidden;display:flex;flex-direction:column;transition:box-shadow .2s,transform .2s;animation:fade .3s ease both}
  @keyframes fade{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
  .card:hover{box-shadow:0 18px 40px -22px rgba(20,18,16,.32);transform:translateY(-2px)}
  .card .ph{position:relative;aspect-ratio:16/10;background:#EFECE8;overflow:hidden;cursor:zoom-in}
  .card .ph img{width:100%;height:100%;object-fit:cover;transition:transform .5s ease}
  .card:hover .ph img{transform:scale(1.04)}
  .card .sku{position:absolute;left:10px;top:10px;font-size:11px;letter-spacing:.08em;background:rgba(20,18,16,.72);color:#fff;padding:5px 9px;border-radius:6px;backdrop-filter:blur(3px)}
  .card .body{padding:14px 16px 16px;display:flex;flex-direction:column;gap:9px;flex:1}
  .card .meta{display:flex;align-items:baseline;justify-content:space-between;gap:10px}
  .card .brand{font-size:15.5px;color:var(--ink)}
  .card .room{font-size:12.5px;color:var(--faint)}
  .card .tags{display:flex;gap:6px;flex-wrap:wrap}
  .pill{font-size:11px;letter-spacing:.04em;color:var(--green);background:#EDF4EE;padding:4px 9px;border-radius:99px}
  .copy{margin-top:auto;display:flex;align-items:center;justify-content:center;gap:8px;font-family:inherit;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink);background:var(--wash);border:1px solid var(--line);border-radius:8px;padding:10px;cursor:pointer;transition:all .15s}
  .copy:hover{background:var(--ink);color:#fff;border-color:var(--ink)}
  .copy svg{width:13px;height:13px;stroke:currentColor;fill:none;stroke-width:1.6}
  .empty{text-align:center;padding:80px 20px;color:var(--soft)}
  .empty h3{font-size:22px;color:var(--ink);margin-bottom:8px}
  /* lightbox */
  .lb{position:fixed;inset:0;z-index:200;background:rgba(18,16,14,.9);display:none;align-items:center;justify-content:center;padding:30px}
  .lb.on{display:flex}
  .lb figure{margin:0;max-width:1100px;width:100%}
  .lb img{width:100%;height:auto;max-height:78vh;object-fit:contain;border-radius:8px}
  .lb .cap{display:flex;justify-content:space-between;align-items:center;gap:16px;color:#EDE9E3;margin-top:14px;flex-wrap:wrap}
  .lb .cap .l b{color:#fff;font-weight:500;font-size:17px}
  .lb .cap .l span{color:#B7B0A8;font-size:13px}
  .lb .cap .r{display:flex;gap:10px}
  .lb .cap button{font-family:inherit;font-size:12px;letter-spacing:.1em;text-transform:uppercase;padding:10px 16px;border-radius:8px;cursor:pointer;border:1px solid #4a4640;background:transparent;color:#fff}
  .lb .cap button.pri{background:#fff;color:var(--ink);border-color:#fff}
  .lb .x{position:absolute;top:18px;right:22px;width:40px;height:40px;border-radius:99px;border:0;background:rgba(255,255,255,.12);color:#fff;font-size:22px;cursor:pointer}
  .lb .arrow{position:absolute;top:50%;transform:translateY(-50%);width:46px;height:46px;border-radius:99px;border:0;background:rgba(255,255,255,.12);color:#fff;font-size:22px;cursor:pointer}
  .lb .arrow.prev{left:20px}.lb .arrow.next{right:20px}
  .lb .arrow:hover,.lb .x:hover{background:rgba(255,255,255,.24)}
  /* toast */
  .toast{position:fixed;bottom:26px;left:50%;transform:translateX(-50%) translateY(20px);background:var(--ink);color:#fff;font-size:13.5px;padding:12px 20px;border-radius:99px;opacity:0;transition:all .25s;z-index:300;pointer-events:none}
  .toast.on{opacity:1;transform:translateX(-50%) translateY(0)}
  footer{background:var(--dark);color:#8a857d;padding:40px var(--pad);font-size:12.5px;margin-top:20px}
  .foot{max-width:1400px;margin:0 auto}
  .foot .seg{display:flex;flex-wrap:wrap;gap:8px 22px;padding-bottom:22px;border-bottom:1px solid #2E2B28;margin-bottom:20px}
  .foot .seg .micro{width:100%;color:#6F6A63;margin-bottom:10px}
  .foot .seg a{font-size:13px;color:#A8A29A}.foot .seg a:hover{color:#fff}
  .foot .base{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
  .foot .base a{color:#A8A29A;text-decoration:underline}
  @media(prefers-reduced-motion:reduce){.card{animation:none}.card .ph img{transition:none}}
</style>
</head>
<body>
<header>
  <div class="nav">
    <a class="mark" href="bella-homepage-redesign.html">BELLA</a>
    <span class="sp"></span>
    <a class="lnk" href="bella-services.html">Services</a>
    <a class="lnk" href="bella-pricing.html">Pricing</a>
    <a class="lnk" href="bella-lookbook.html">Lookbook</a>
    <a class="lnk" href="bella-resources.html">Resources</a>
    <a class="btn" href="bella-order-page.html">Get started</a>
  </div>
</header>

<section class="hero"><div class="wrap">
  <p class="micro eyebrow">Lookbook 2025 · Brand furniture</p>
  <h1>The Bella furniture catalog.</h1>
  <p>Every set below is a real room styled by our designers with furniture from a leading brand. Browse by room, style or brand — then, when a look feels right for your listing, copy its SKU and send it with your order.</p>
  <div class="tip"><span>🔖</span><span><b>How to order a look:</b> hover a set, hit <b>Copy SKU</b>, and paste it into your order notes. We'll stage your photos in that exact style.</span></div>
</div></section>

<div class="bar"><div class="bar-in">
  <div class="search">
    <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>
    <input id="q" type="text" placeholder="Search a SKU or keyword (e.g. LR-ROVE, bedroom, coastal)" autocomplete="off">
  </div>
  <div class="frow" id="fRoom"><span class="flabel">Room</span></div>
  <div class="frow" id="fBrand"><span class="flabel">Brand</span></div>
  <div class="frow" id="fStyle"><span class="flabel">Style</span></div>
  <div class="barfoot"><span class="count" id="count"></span><button class="clear" id="clear">Clear filters</button></div>
</div></div>

<main class="wrap"><div class="grid" id="grid"></div><div class="empty" id="empty" style="display:none"><h3>No sets match those filters.</h3><p>Try clearing a filter or searching a different room or brand.</p></div></main>

<div class="lb" id="lb">
  <button class="x" id="lbX" aria-label="Close">&times;</button>
  <button class="arrow prev" id="lbPrev" aria-label="Previous">&#8249;</button>
  <button class="arrow next" id="lbNext" aria-label="Next">&#8250;</button>
  <figure>
    <img id="lbImg" src="" alt="">
    <div class="cap"><div class="l"><b id="lbBrand"></b> &nbsp;<span id="lbMeta"></span></div>
      <div class="r"><button class="pri" id="lbCopy">Copy SKU</button><a class="pri" style="text-decoration:none" href="bella-order-page.html">Order this look</a></div></div>
  </figure>
</div>

<div class="toast" id="toast"></div>

<footer><div class="foot">
  <div class="seg"><span class="micro">Bella Virtual</span>
    <a href="bella-services.html">Services</a><a href="bella-service-virtual-staging.html">Virtual staging</a>
    <a href="bella-service-virtual-land-staging.html">Virtual land staging</a><a href="bella-service-3d-rendering.html">3D rendering</a>
    <a href="bella-service-floor-plans.html">Floor plans</a><a href="bella-service-photo-editing.html">Photo editing</a>
    <a href="bella-service-3d-tour.html">3D tours</a><a href="bella-pricing.html">Pricing</a>
    <a href="bella-lookbook.html">Lookbook</a><a href="bella-resources.html">Resources</a><a href="bella-order-page.html">Get started</a></div>
  <div class="base"><span>&copy; Bella Virtual Staging &middot; <a href="bella-homepage-redesign.html">Back to the studio</a></span>
    <span>Furniture catalog · Lookbook 2025 · Redesign mockup, not the live site</span></div>
</div></footer>

<script>
const DATA=__DATA__;
const ROOMS=__ROOMS__, BRANDS=__BRANDS__, STYLES=__STYLES__;
const state={room:"All",brand:"All",style:"All",q:""};
const grid=document.getElementById('grid'), empty=document.getElementById('empty');
function count(field,val){return DATA.filter(d=>val==="All"||d[field]===val).length;}
function buildChips(id,field,vals){
  const row=document.getElementById(id);
  ["All",...vals].forEach(v=>{
    const b=document.createElement('button'); b.className='chip'+(state[field]===v?' on':'');
    b.innerHTML=v+(v!=="All"?'<span class="c">'+DATA.filter(d=>d[field]===v).length+'</span>':'');
    b.onclick=()=>{state[field]=v;[...row.querySelectorAll('.chip')].forEach(c=>c.classList.remove('on'));b.classList.add('on');render();};
    row.appendChild(b);
  });
}
function match(d){
  if(state.room!=="All"&&d.room!==state.room)return false;
  if(state.brand!=="All"&&d.brand!==state.brand)return false;
  if(state.style!=="All"&&d.style!==state.style)return false;
  if(state.q){const s=(d.sku+" "+d.brand+" "+d.room+" "+d.style).toLowerCase();if(!s.includes(state.q.toLowerCase()))return false;}
  return true;
}
let view=[];
function render(){
  view=DATA.filter(match);
  grid.innerHTML="";
  empty.style.display=view.length?"none":"block";
  document.getElementById('count').innerHTML="<b>"+view.length+"</b> "+(view.length===1?"set":"sets");
  view.forEach((d,i)=>{
    const c=document.createElement('div'); c.className='card'; c.style.animationDelay=Math.min(i*12,240)+'ms';
    c.innerHTML=`<div class="ph" data-i="${i}"><span class="sku">${d.sku}</span><img loading="lazy" src="${d.img}" alt="${d.room} staged with ${d.brand} furniture (${d.sku})"></div>
      <div class="body"><div class="meta"><span class="brand">${d.brand}</span><span class="room">${d.room}</span></div>
      <div class="tags"><span class="pill">${d.style}</span></div>
      <button class="copy" data-sku="${d.sku}"><svg viewBox="0 0 24 24"><rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/></svg>Copy SKU · ${d.sku}</button></div>`;
    grid.appendChild(c);
  });
}
// events
document.getElementById('q').addEventListener('input',e=>{state.q=e.target.value;render();});
document.getElementById('clear').onclick=()=>{state.room="All";state.brand="All";state.style="All";state.q="";document.getElementById('q').value="";
  document.querySelectorAll('.frow').forEach(r=>r.querySelectorAll('.chip').forEach((c,idx)=>c.classList.toggle('on',idx===0)));render();};
let toastT;
function toast(m){const t=document.getElementById('toast');t.textContent=m;t.classList.add('on');clearTimeout(toastT);toastT=setTimeout(()=>t.classList.remove('on'),1600);}
function copy(sku){navigator.clipboard&&navigator.clipboard.writeText(sku).then(()=>toast("Copied "+sku)).catch(()=>toast(sku));}
grid.addEventListener('click',e=>{
  const cp=e.target.closest('.copy'); if(cp){copy(cp.dataset.sku);return;}
  const ph=e.target.closest('.ph'); if(ph){openLB(parseInt(ph.dataset.i));}
});
// lightbox
let lbi=0;
const lb=document.getElementById('lb');
function openLB(i){lbi=i;const d=view[i];document.getElementById('lbImg').src=d.img;document.getElementById('lbImg').alt=d.sku;
  document.getElementById('lbBrand').textContent=d.brand;document.getElementById('lbMeta').textContent=d.room+" · "+d.style+" · "+d.sku;
  document.getElementById('lbCopy').onclick=()=>copy(d.sku);lb.classList.add('on');}
function step(n){lbi=(lbi+n+view.length)%view.length;openLB(lbi);}
document.getElementById('lbX').onclick=()=>lb.classList.remove('on');
document.getElementById('lbPrev').onclick=()=>step(-1);
document.getElementById('lbNext').onclick=()=>step(1);
lb.addEventListener('click',e=>{if(e.target===lb)lb.classList.remove('on');});
document.addEventListener('keydown',e=>{if(!lb.classList.contains('on'))return;if(e.key==="Escape")lb.classList.remove('on');if(e.key==="ArrowLeft")step(-1);if(e.key==="ArrowRight")step(1);});
// init
buildChips('fRoom','room',ROOMS);buildChips('fBrand','brand',BRANDS);buildChips('fStyle','style',STYLES);render();
</script>
</body>
</html>
'''

HTML = (HTML.replace("__DATA__", DATA)
            .replace("__ROOMS__", json.dumps(rooms))
            .replace("__BRANDS__", json.dumps(brands))
            .replace("__STYLES__", json.dumps(styles)))
(ROOT/"bella-lookbook.html").write_text(HTML)
print(f"wrote bella-lookbook.html with {len(items)} sets | brands={brands} | rooms={rooms} | styles={styles}")
