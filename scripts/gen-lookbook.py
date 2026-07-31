#!/usr/bin/env python3
"""Generate the modern Bella furniture catalog (bella-lookbook.html) from the
SKU-named tiles in assets/lookbook/. SKU = {ROOM}-{BRAND}-{###}.
Re-run after adding/replacing tiles (e.g. hi-res originals, or the style catalogue)."""
import json, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from catalog_data import ROOT, load_items, facets

items = load_items()
rooms, brands, styles = facets(items)

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
  :root{--bg:#FDFCFA;--ink:#232120;--soft:#6E6A66;--faint:#9C978F;--line:#E8E4DE;--line-2:#F0EDE8;--dark:#1C1A18;--green:#3E6B4C;--gold:#B8985A;--red:#C4553F;--wash:#FAF8F5;--pad:40px}
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
  .bar-top{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
  .search{display:flex;align-items:center;gap:10px;border:1px solid var(--line);border-radius:10px;padding:10px 14px;background:#fff;flex:1 1 240px;min-width:200px}
  .search svg{width:16px;height:16px;stroke:var(--faint);fill:none;stroke-width:1.6}
  .search input{border:0;outline:0;font-family:inherit;font-size:14.5px;width:100%;color:var(--ink);background:transparent}
  .sel{flex:0 0 auto;font-family:inherit;font-size:13.5px;color:var(--ink);background:#fff;border:1px solid var(--line);border-radius:10px;padding:10px 14px;cursor:pointer;min-width:132px;transition:border-color .15s}
  .sel:hover{border-color:var(--ink)}.sel:focus{outline:0;border-color:var(--ink)}
  .savedbtn{flex:0 0 auto;display:inline-flex;align-items:center;gap:8px;font-family:inherit;font-size:13.5px;border:1px solid var(--line);background:#fff;color:var(--soft);padding:10px 15px;border-radius:10px;cursor:pointer;transition:all .15s}
  .savedbtn svg{width:16px;height:16px;fill:none;stroke:currentColor;stroke-width:1.7}
  .savedbtn:hover{border-color:var(--ink);color:var(--ink)}
  .savedbtn .n{background:var(--line-2);color:var(--soft);border-radius:99px;padding:0 8px;font-size:12px;font-weight:500;min-width:20px;text-align:center}
  .savedbtn.on{background:var(--ink);color:#fff;border-color:var(--ink)}
  .savedbtn.on svg{fill:var(--red);stroke:var(--red)}
  .savedbtn.on .n{background:rgba(255,255,255,.2);color:#fff}
  .bar-bot{display:flex;align-items:center;gap:12px;margin-top:12px;flex-wrap:wrap}
  .rooms{display:flex;gap:8px;flex-wrap:wrap}
  .bar-bot .right{margin-left:auto;display:flex;align-items:center;gap:16px}
  .chip{flex:0 0 auto;font-family:inherit;font-size:13px;border:1px solid var(--line);background:#fff;color:var(--soft);padding:7px 15px;border-radius:99px;cursor:pointer;white-space:nowrap;transition:all .15s}
  .chip:hover{border-color:var(--ink);color:var(--ink)}
  .chip.on{background:var(--ink);color:#fff;border-color:var(--ink)}
  .chip .c{opacity:.5;font-size:11.5px;margin-left:5px}
  .count{font-size:13px;color:var(--soft)}.count b{color:var(--ink);font-weight:500}
  .clear{font-size:12.5px;letter-spacing:.06em;color:var(--green);background:0;border:0;cursor:pointer;font-family:inherit}
  .clear:hover{color:var(--ink)}
  /* saved action bar */
  .savedbar{display:flex;align-items:center;justify-content:space-between;gap:14px;background:var(--wash);border:1px solid var(--line);border-radius:12px;padding:13px 18px;margin:28px 0 -8px;flex-wrap:wrap}
  .savedbar span{font-size:14px;color:var(--soft)}.savedbar b{color:var(--ink);font-weight:500}
  .savedbar .a{display:flex;gap:8px}
  .savedbar .a button,.savedbar .a a{font-family:inherit;font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;padding:9px 15px;border-radius:8px;cursor:pointer;text-decoration:none;border:0}
  .savedbar .copyall{background:#fff;border:1px solid var(--line);color:var(--ink)}.savedbar .copyall:hover{border-color:var(--ink)}
  .savedbar .order{background:var(--ink);color:#fff}.savedbar .order:hover{background:var(--green)}
  /* grid */
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:22px;padding:34px 0 70px}
  .card{background:#fff;border:1px solid var(--line);border-radius:12px;overflow:hidden;display:flex;flex-direction:column;transition:box-shadow .2s,transform .2s;animation:fade .3s ease both}
  @keyframes fade{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
  .card:hover{box-shadow:0 18px 40px -22px rgba(20,18,16,.32);transform:translateY(-2px)}
  .card .ph{position:relative;background:#EFECE8;overflow:hidden;cursor:zoom-in;line-height:0}
  .card .ph img{width:100%;height:auto;display:block;transition:transform .5s ease}
  .card:hover .ph img{transform:scale(1.03)}
  .save{position:absolute;right:10px;bottom:10px;width:34px;height:34px;border-radius:99px;border:0;background:rgba(255,255,255,.85);backdrop-filter:blur(4px);cursor:pointer;display:flex;align-items:center;justify-content:center;transition:transform .15s,background .15s;z-index:2}
  .save:hover{transform:scale(1.09)}
  .save svg{width:17px;height:17px;stroke:var(--ink);fill:none;stroke-width:1.7;transition:all .2s}
  .save.on svg{fill:var(--red);stroke:var(--red)}
  .save.pop{animation:pop .3s ease}
  @keyframes pop{0%{transform:scale(1)}45%{transform:scale(1.3)}100%{transform:scale(1)}}
  .card .body{padding:9px 12px 10px 14px;display:flex;align-items:center;justify-content:space-between;gap:10px}
  .card .meta{display:flex;flex-direction:column;gap:1px;min-width:0}
  .card .brand{font-size:14px;color:var(--ink);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .card .room{font-size:11.5px;color:var(--faint)}
  .card .sku{align-self:flex-start;margin-top:3px;max-width:100%;font-size:11px;letter-spacing:.06em;color:var(--soft);background:var(--wash);border:1px solid var(--line);border-radius:5px;padding:2px 7px;cursor:copy;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;transition:all .15s}
  .card .sku:hover{color:var(--ink);border-color:var(--soft);background:#fff}
  .card .sku.copied{color:var(--green);border-color:var(--green)}
  .card .acts{flex:0 0 auto;display:flex;gap:6px}
  .copy,.info{width:33px;height:33px;display:flex;align-items:center;justify-content:center;background:var(--wash);border:1px solid var(--line);border-radius:8px;cursor:pointer;transition:all .15s;padding:0}
  .copy:hover,.info:hover{background:var(--ink);border-color:var(--ink)}
  .copy svg,.info svg{width:16px;height:16px;stroke:var(--soft);fill:none;stroke-width:1.6}
  .copy:hover svg,.info:hover svg{stroke:#fff}
  /* info modal */
  .imodal{position:fixed;inset:0;z-index:250;background:rgba(20,18,16,.55);backdrop-filter:blur(3px);display:none;align-items:center;justify-content:center;padding:24px}
  .imodal.on{display:flex}
  .icard{background:#fff;border-radius:14px;max-width:440px;width:100%;max-height:92vh;overflow-y:auto;box-shadow:0 30px 70px -25px rgba(20,18,16,.6);position:relative}
  .icard>img{width:100%;height:auto;display:block}
  .icard .ix{position:absolute;top:12px;right:12px;width:32px;height:32px;border:0;border-radius:99px;background:rgba(255,255,255,.9);color:var(--ink);font-size:20px;line-height:1;cursor:pointer;z-index:2}
  .icard .ic{padding:20px 22px 22px}
  .icard .ib{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--green);font-weight:600}
  .icard h3{font-size:21px;font-weight:400;margin:6px 0 14px;letter-spacing:-.01em}
  .icard .irow{display:flex;justify-content:space-between;gap:12px;font-size:13.5px;padding:9px 0;border-bottom:1px solid var(--line-2)}
  .icard .irow span:first-child{color:var(--faint)}.icard .irow span:last-child{color:var(--ink)}
  .icard .pieces{margin-top:16px}
  .icard .pieces h4{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--faint);margin-bottom:6px}
  .icard .piece{display:flex;justify-content:space-between;gap:12px;font-size:14px;padding:7px 0;border-bottom:1px solid var(--line-2)}
  .icard .piece span:last-child{color:var(--soft)}
  .icard .shop{margin-top:16px;font-size:13px;color:var(--soft);line-height:1.5;background:var(--wash);border:1px solid var(--line);border-radius:9px;padding:12px 14px}
  .icard .shop b{color:var(--ink);font-weight:500}
  .icard .ifoot{display:flex;gap:8px;margin-top:16px}
  .icard .ifoot button,.icard .ifoot a{flex:1;text-align:center;font-family:inherit;font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;padding:11px;border-radius:8px;text-decoration:none;cursor:pointer;border:0}
  .icard .ifoot .cp{background:var(--wash);border:1px solid var(--line);color:var(--ink)}.icard .ifoot .cp:hover{border-color:var(--ink)}
  .icard .ifoot .od{background:var(--ink);color:#fff}.icard .ifoot .od:hover{background:var(--green)}
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
  .lb .cap button.saveb{border-color:#4a4640}
  .lb .cap button.saveb.on{background:var(--red);border-color:var(--red);color:#fff}
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
  <div class="bar-top">
    <div class="search">
      <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>
      <input id="q" type="text" placeholder="Search a SKU, room or style" autocomplete="off">
    </div>
    <select id="fStyle" class="sel" aria-label="Filter by style"></select>
    <select id="fBrand" class="sel" aria-label="Filter by brand"></select>
    <button class="savedbtn" id="savedBtn" aria-label="Show saved sets"><svg viewBox="0 0 24 24"><path d="M12 21s-8-4.5-8-10a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 11c0 5.5-8 10-8 10z"/></svg><span>Saved</span><span class="n" id="savedN">0</span></button>
  </div>
  <div class="bar-bot">
    <div class="rooms" id="fRoom"></div>
    <div class="right"><span class="count" id="count"></span><button class="clear" id="clear">Clear</button></div>
  </div>
</div></div>

<main class="wrap">
  <div class="savedbar" id="savedBar" style="display:none">
    <span id="savedInfo"></span>
    <div class="a"><button class="copyall" id="copyAll">Copy all SKUs</button><a class="order" id="orderSaved" href="bella-order-page.html">Add to order →</a></div>
  </div>
  <div class="grid" id="grid"></div>
  <div class="empty" id="empty" style="display:none"><h3>No sets match those filters.</h3><p>Try clearing a filter or searching a different room or style.</p></div>
</main>

<div class="lb" id="lb">
  <button class="x" id="lbX" aria-label="Close">&times;</button>
  <button class="arrow prev" id="lbPrev" aria-label="Previous">&#8249;</button>
  <button class="arrow next" id="lbNext" aria-label="Next">&#8250;</button>
  <figure>
    <img id="lbImg" src="" alt="">
    <div class="cap"><div class="l"><b id="lbBrand"></b> &nbsp;<span id="lbMeta"></span></div>
      <div class="r"><button class="saveb" id="lbSave">♥ Save</button><button class="pri" id="lbCopy">Copy SKU</button><a class="pri" style="text-decoration:none" href="bella-order-page.html">Order this look</a></div></div>
  </figure>
</div>

<div class="imodal" id="imodal"><div class="icard">
  <button class="ix" id="iClose" aria-label="Close">&times;</button>
  <img id="iImg" src="" alt="">
  <div class="ic" id="iBody"></div>
</div></div>

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
const state={room:"All",brand:"All",style:"All",q:"",savedView:false};
const grid=document.getElementById('grid'), empty=document.getElementById('empty');
function buildChips(id,field,vals){          // Room pills
  const row=document.getElementById(id);
  ["All",...vals].forEach(v=>{
    const b=document.createElement('button'); b.className='chip'+(state[field]===v?' on':'');
    b.innerHTML=v+(v!=="All"?'<span class="c">'+DATA.filter(d=>d[field]===v).length+'</span>':'');
    b.onclick=()=>{state[field]=v;[...row.querySelectorAll('.chip')].forEach(c=>c.classList.remove('on'));b.classList.add('on');render();};
    row.appendChild(b);
  });
}
function buildSelect(id,field,vals){         // Style / Brand dropdowns
  const sel=document.getElementById(id);
  sel.innerHTML=['<option value="All">All '+(field==='style'?'styles':'brands')+'</option>']
    .concat(vals.map(v=>'<option value="'+v+'">'+v+' ('+DATA.filter(d=>d[field]===v).length+')</option>')).join('');
  sel.onchange=()=>{state[field]=sel.value;render();};
}
function match(d){
  if(state.savedView&&!saved.has(d.sku))return false;
  if(state.room!=="All"&&d.room!==state.room)return false;
  if(state.brand!=="All"&&d.brand!==state.brand)return false;
  if(state.style!=="All"&&d.style!==state.style)return false;
  if(state.q){const s=(d.sku+" "+d.label+" "+d.room+" "+d.style).toLowerCase();if(!s.includes(state.q.toLowerCase()))return false;}
  return true;
}
let view=[];
function render(){
  view=DATA.filter(match);
  grid.innerHTML="";
  empty.style.display=view.length?"none":"block";
  if(!view.length){
    empty.querySelector('h3').textContent=state.savedView?"No saved sets yet.":"No sets match those filters.";
    empty.querySelector('p').textContent=state.savedView?"Tap the ♥ on any set to save it here for your order.":"Try clearing a filter or searching a different room or style.";
  }
  document.getElementById('count').innerHTML="<b>"+view.length+"</b> "+(view.length===1?"set":"sets")+(state.savedView?" saved":"");
  updateBars();
  view.forEach((d,i)=>{
    const c=document.createElement('div'); c.className='card'; c.style.animationDelay=Math.min(i*12,240)+'ms';
    c.innerHTML=`<div class="ph" data-i="${i}"><button class="save${saved.has(d.sku)?' on':''}" data-sku="${d.sku}" aria-label="Save this set"><svg viewBox="0 0 24 24"><path d="M12 21s-8-4.5-8-10a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 11c0 5.5-8 10-8 10z"/></svg></button><img loading="lazy" src="${d.img}" alt="${d.room} styled ${d.style} (${d.sku})"></div>
      <div class="body"><div class="meta"><span class="brand">${d.label}</span><span class="room">${d.room}${d.brand? ' · '+d.style : ''}</span><button class="sku" data-sku="${d.sku}" title="Click to copy ${d.sku}">${d.sku}</button></div>
      <div class="acts"><button class="info" data-sku="${d.sku}" title="Set details" aria-label="Set details"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 11v5"/><circle cx="12" cy="7.6" r="0.6" fill="currentColor" stroke="none"/></svg></button><button class="copy" data-sku="${d.sku}" title="Copy ${d.sku}" aria-label="Copy ${d.sku}"><svg viewBox="0 0 24 24"><rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/></svg></button></div></div>`;
    grid.appendChild(c);
  });
}
// events
document.getElementById('q').addEventListener('input',e=>{state.q=e.target.value;render();});
document.getElementById('clear').onclick=()=>{state.room="All";state.brand="All";state.style="All";state.q="";state.savedView=false;
  document.getElementById('q').value="";document.getElementById('fStyle').value="All";document.getElementById('fBrand').value="All";
  document.querySelectorAll('#fRoom .chip').forEach((c,idx)=>c.classList.toggle('on',idx===0));render();};
let toastT;
function toast(m){const t=document.getElementById('toast');t.textContent=m;t.classList.add('on');clearTimeout(toastT);toastT=setTimeout(()=>t.classList.remove('on'),1600);}
function copy(sku){navigator.clipboard&&navigator.clipboard.writeText(sku).then(()=>toast("Copied "+sku)).catch(()=>toast(sku));}
// saved-for-order (heart on cards → "Saved" view in the toolbar, no floating box)
let saved=new Set(JSON.parse(localStorage.getItem('bella_saved')||'[]').filter(s=>DATA.some(d=>d.sku===s)));
const savedBtn=document.getElementById('savedBtn'), savedBar=document.getElementById('savedBar');
function persist(){localStorage.setItem('bella_saved',JSON.stringify([...saved]));}
function updateBars(){
  document.getElementById('savedN').textContent=saved.size;
  savedBtn.classList.toggle('on',state.savedView);
  if(state.savedView && saved.size){
    savedBar.style.display='flex';
    document.getElementById('savedInfo').innerHTML='<b>'+saved.size+'</b> saved '+(saved.size===1?'set':'sets')+' — copy the SKUs or send them straight to your order.';
    document.getElementById('orderSaved').href='bella-order-page.html?skus='+encodeURIComponent([...saved].join(','));
  } else savedBar.style.display='none';
}
function toggleSave(sku){
  const add=!saved.has(sku); add?saved.add(sku):saved.delete(sku); persist();
  document.querySelectorAll('.save[data-sku="'+sku+'"]').forEach(b=>{b.classList.toggle('on',add);if(add){b.classList.add('pop');setTimeout(()=>b.classList.remove('pop'),300);}});
  const lbs=document.getElementById('lbSave'); if(lbs&&lbs.dataset.sku===sku){lbs.classList.toggle('on',add);lbs.textContent=(add?'♥ Saved':'♥ Save');}
  toast(add?'Saved '+sku:'Removed '+sku);
  if(state.savedView) render(); else updateBars();
}
savedBtn.onclick=()=>{ if(!state.savedView && !saved.size){toast('Tap the ♥ on a set to save it');return;} state.savedView=!state.savedView; render(); };
document.getElementById('copyAll').onclick=()=>{if(!saved.size){toast('No saved sets yet');return;}copy([...saved].join(', '));};
grid.addEventListener('click',e=>{
  const sv=e.target.closest('.save'); if(sv){e.stopPropagation();toggleSave(sv.dataset.sku);return;}
  const inf=e.target.closest('.info'); if(inf){openInfo(DATA.find(x=>x.sku===inf.dataset.sku));return;}
  const cp=e.target.closest('.copy'); if(cp){copy(cp.dataset.sku);return;}
  const sk=e.target.closest('.sku'); if(sk){copy(sk.dataset.sku);sk.classList.add('copied');setTimeout(()=>sk.classList.remove('copied'),900);return;}
  const ph=e.target.closest('.ph'); if(ph){openLB(parseInt(ph.dataset.i));}
});
// per-set furniture details — populate PIECES[sku]=[{name,type,price}] when piece data exists
const PIECES={};
function openInfo(d){
  if(!d)return;
  const im=document.getElementById('iImg'); im.src=d.img; im.alt=d.sku;
  const pcs=PIECES[d.sku];
  let h='<div class="ib">'+(d.brand||'Bella studio')+'</div><h3>'+d.room+' · '+d.style+'</h3>';
  h+='<div class="irow"><span>Room</span><span>'+d.room+'</span></div>';
  h+='<div class="irow"><span>Style</span><span>'+d.style+'</span></div>';
  h+='<div class="irow"><span>'+(d.brand?'Brand':'Collection')+'</span><span>'+(d.brand||'Bella studio pick')+'</span></div>';
  h+='<div class="irow"><span>SKU</span><span>'+d.sku+'</span></div>';
  if(pcs&&pcs.length){
    h+='<div class="pieces"><h4>Furniture in this set</h4>'+pcs.map(p=>'<div class="piece"><span>'+p.name+(p.type?' · '+p.type:'')+'</span><span>'+(p.price||'')+'</span></div>').join('')+'</div>';
  }else if(d.brand){
    h+='<div class="shop"><b>Shop this look.</b> This room is staged with real '+d.brand+' furniture — Bella partners get <b>15–65% off</b> the actual pieces through the Bella Catalog. Individual piece names available on request.</div>';
  }else{
    h+='<div class="shop"><b>Curated by a Bella designer.</b> Send us this SKU and we\'ll stage your photos in this exact look.</div>';
  }
  h+='<div class="ifoot"><button class="cp" id="iCopy">Copy SKU</button><a class="od" href="bella-order-page.html?skus='+d.sku+'">Order this look →</a></div>';
  document.getElementById('iBody').innerHTML=h;
  document.getElementById('iCopy').onclick=()=>copy(d.sku);
  imodal.classList.add('on');
}
const imodal=document.getElementById('imodal');
document.getElementById('iClose').onclick=()=>imodal.classList.remove('on');
imodal.addEventListener('click',e=>{if(e.target===imodal)imodal.classList.remove('on');});
document.addEventListener('keydown',e=>{if(e.key==="Escape")imodal.classList.remove('on');});
// lightbox
let lbi=0;
const lb=document.getElementById('lb');
function openLB(i){lbi=i;const d=view[i];document.getElementById('lbImg').src=d.img;document.getElementById('lbImg').alt=d.sku;
  document.getElementById('lbBrand').textContent=d.label;document.getElementById('lbMeta').textContent=d.room+" · "+d.style+" · "+d.sku;
  document.getElementById('lbCopy').onclick=()=>copy(d.sku);
  const lbs=document.getElementById('lbSave');lbs.dataset.sku=d.sku;lbs.classList.toggle('on',saved.has(d.sku));lbs.textContent=(saved.has(d.sku)?'♥ Saved':'♥ Save');lbs.onclick=()=>toggleSave(d.sku);
  lb.classList.add('on');}
function step(n){lbi=(lbi+n+view.length)%view.length;openLB(lbi);}
document.getElementById('lbX').onclick=()=>lb.classList.remove('on');
document.getElementById('lbPrev').onclick=()=>step(-1);
document.getElementById('lbNext').onclick=()=>step(1);
lb.addEventListener('click',e=>{if(e.target===lb)lb.classList.remove('on');});
document.addEventListener('keydown',e=>{if(!lb.classList.contains('on'))return;if(e.key==="Escape")lb.classList.remove('on');if(e.key==="ArrowLeft")step(-1);if(e.key==="ArrowRight")step(1);});
// init
buildChips('fRoom','room',ROOMS);buildSelect('fStyle','style',STYLES);buildSelect('fBrand','brand',BRANDS);render();
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
