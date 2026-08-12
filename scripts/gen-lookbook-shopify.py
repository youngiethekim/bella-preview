#!/usr/bin/env python3
"""Generate a SELF-CONTAINED, Shopify-paste-ready 2026 lookbook block from the
SKU tiles in assets/lookbook/. Output = bella-lookbook-2026-shopify.html — one block
(scoped <style> + <div class="blb"> + <script>) you paste into a Shopify page (code view)
or a theme section. All CSS is namespaced under .blb so it never fights the theme;
image URLs are absolute so they resolve on Shopify."""
import os, re, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
LB = ROOT/"assets"/"lookbook"
# absolute base so images resolve from any host (swap for your own CDN / Shopify files if you rehost)
IMG_BASE = "https://youngiethekim.github.io/bella-preview/assets/lookbook/"

ROOM = {"LR":"Living Room","DR":"Dining Room","BDR":"Bedroom","BR":"Bedroom","BD":"Bedroom",
        "KI":"Kitchen","KT":"Kitchen","OF":"Office","EX":"Exterior","SA":"Living Room","LIB":"Office"}
ROOM_ORDER = ["Living Room","Dining Room","Bedroom","Kitchen","Office","Exterior"]
BRAND = {"ROVE":"Rove Concepts","SUNDAYS":"Sundays","MOB":"Mobital","GUS":"Gus*","EM":"Eternity Modern","ROC":"Roche Bobois"}
BRAND_ORDER = ["Rove Concepts","Sundays","Mobital","Gus*","Eternity Modern","Roche Bobois"]
SIG_STYLE = {"ROVE":"Modern","SUNDAYS":"Coastal","MOB":"Modern","GUS":"Mid-Century","EM":"Contemporary","ROC":"Bold Luxe"}
STYLE_CODES = {"MDRN":"Modern","CONT":"Contemporary","COAS":"Coastal","HAMP":"Hamptons Coastal","MCM":"Mid-Century",
               "SCND":"Scandinavian","TRNS":"Transitional","FARM":"Farmhouse","MFRM":"Modern Farmhouse",
               "NDBH":"Nordic Boho","TRAD":"Traditional","PTIO":"Patio","SKY":"Sky"}
STYLE_ORDER = ["Modern","Contemporary","Coastal","Hamptons Coastal","Mid-Century","Scandinavian","Transitional",
               "Farmhouse","Modern Farmhouse","Nordic Boho","Bold Luxe","Traditional","Patio","Sky"]

items=[]
for f in sorted(os.listdir(LB)):
    if not f.lower().endswith(".jpg"): continue
    sku=f[:-4]
    m=re.match(r'^(LR|DR|BDR|BD|BR|KI|KT|OF|EX|SA|LIB)-([A-Z]+)-([A-Z]?)(\d{2,4})$', sku)
    if not m: continue
    room,mid,_pfx,num=m.group(1),m.group(2),m.group(3),int(m.group(4))
    it={"sku":sku,"img":IMG_BASE+f,"room":ROOM.get(room,room),"num":num}
    if mid in BRAND: it.update(type="brand",brand=BRAND[mid],label=BRAND[mid],style=SIG_STYLE[mid])
    elif mid in STYLE_CODES: it.update(type="style",brand="",label=STYLE_CODES[mid],style=STYLE_CODES[mid])
    else: continue
    items.append(it)

def sortkey(it):
    tr=0 if it["type"]=="brand" else 1
    cr=(BRAND_ORDER.index(it["label"]) if it["type"]=="brand" and it["label"] in BRAND_ORDER
        else (STYLE_ORDER.index(it["style"]) if it["style"] in STYLE_ORDER else 99))
    rr=ROOM_ORDER.index(it["room"]) if it["room"] in ROOM_ORDER else 99
    return (tr,cr,rr,it["num"])
items.sort(key=sortkey)

rooms=[r for r in ROOM_ORDER if any(i["room"]==r for i in items)]
brands=[b for b in BRAND_ORDER if any(i.get("brand")==b for i in items)]
styles=[s for s in STYLE_ORDER if any(i["style"]==s for i in items)]
DATA=json.dumps(items, separators=(",",":"))

BLOCK = r'''<!-- ============================================================
     BELLA · Lookbook 2026 — paste-ready block for Shopify
     Paste into: Online Store > Pages > (your page) > Show HTML (</>), OR a theme section.
     Everything is scoped under .blb so it will not affect your theme.
     Images load from an absolute URL; re-host them and change IMG_BASE if you like.
     ============================================================ -->
<style>
@import url('https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500&display=swap');
.blb{--bg:#FDFCFA;--ink:#232120;--soft:#6E6A66;--faint:#9C978F;--line:#E8E4DE;--line2:#F0EDE8;--green:#3E6B4C;--wash:#FAF8F5;
  background:var(--bg);color:var(--ink);font-family:'Jost',system-ui,-apple-system,sans-serif;font-weight:300;line-height:1.6;
  -webkit-font-smoothing:antialiased;max-width:1440px;margin:0 auto;padding:0 22px 60px}
.blb, .blb *, .blb *::before, .blb *::after{box-sizing:border-box}
.blb img{display:block;max-width:100%}
.blb button{font-family:inherit;cursor:pointer;color:inherit}
.blb .blb-eye{font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--green);font-weight:600;margin:0}
.blb h2.blb-h{font-weight:300;font-size:clamp(30px,4.4vw,52px);letter-spacing:-.015em;line-height:1.08;margin:12px 0 0}
.blb .blb-sub{color:var(--soft);max-width:60ch;margin:14px 0 0;font-size:16.5px}
.blb .blb-hero{padding:46px 0 26px;border-bottom:1px solid var(--line)}
/* toolbar */
.blb .blb-bar{position:sticky;top:0;z-index:5;background:rgba(253,252,250,.95);backdrop-filter:blur(8px);
  padding:14px 0;border-bottom:1px solid var(--line);margin-bottom:22px}
.blb .blb-row{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.blb .blb-search{display:flex;align-items:center;gap:9px;border:1px solid var(--line);border-radius:10px;padding:10px 14px;background:#fff;flex:1 1 240px;min-width:190px}
.blb .blb-search input{border:0;outline:0;font-family:inherit;font-size:14.5px;width:100%;color:var(--ink);background:transparent}
.blb select.blb-sel{font-family:inherit;font-size:13.5px;color:var(--ink);background:#fff;border:1px solid var(--line);border-radius:10px;padding:10px 14px;cursor:pointer;min-width:130px}
.blb .blb-chips{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px;align-items:center}
.blb .blb-chip{font-family:inherit;font-size:13px;border:1px solid var(--line);background:#fff;color:var(--soft);border-radius:99px;padding:8px 15px;transition:all .15s}
.blb .blb-chip:hover{border-color:var(--green);color:var(--ink)}
.blb .blb-chip.on{background:var(--green);border-color:var(--green);color:#fff}
.blb .blb-chip .n{opacity:.6;font-size:11.5px;margin-left:5px}
.blb .blb-count{margin-left:auto;font-size:13px;color:var(--faint)}
.blb .blb-clear{background:0;border:0;color:var(--green);font-size:13px;text-decoration:underline;padding:6px}
/* grid */
.blb .blb-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:10px}
@media(max-width:900px){.blb .blb-grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:560px){.blb .blb-grid{grid-template-columns:1fr}}
.blb .blb-card{border:1px solid var(--line);border-radius:12px;overflow:hidden;background:#fff;cursor:pointer;transition:transform .18s,box-shadow .18s}
.blb .blb-card:hover{transform:translateY(-3px);box-shadow:0 18px 40px -20px rgba(20,18,16,.32)}
.blb .blb-ph{position:relative;aspect-ratio:4/3;background:var(--wash);overflow:hidden}
.blb .blb-ph img{width:100%;height:100%;object-fit:cover;transition:transform .5s}
.blb .blb-card:hover .blb-ph img{transform:scale(1.04)}
.blb .blb-sku{position:absolute;top:10px;left:10px;font-size:10.5px;letter-spacing:.08em;background:rgba(253,252,250,.92);color:var(--ink);padding:4px 8px;border-radius:6px}
.blb .blb-body{padding:14px 15px}
.blb .blb-body b{font-weight:400;font-size:15.5px;display:block}
.blb .blb-body span{font-size:12.5px;color:var(--faint);display:block;margin-top:2px}
.blb .blb-empty{text-align:center;color:var(--soft);padding:60px 0}
/* lightbox */
.blb-lb{position:fixed;inset:0;z-index:99999;background:rgba(18,16,14,.9);display:none;align-items:center;justify-content:center;padding:26px}
.blb-lb.on{display:flex}
.blb-lb figure{margin:0;max-width:1100px;width:100%;font-family:'Jost',system-ui,sans-serif}
.blb-lb img{width:100%;height:auto;max-height:78vh;object-fit:contain;border-radius:8px}
.blb-lb .cap{display:flex;justify-content:space-between;align-items:center;gap:16px;color:#EDE9E3;margin-top:14px;flex-wrap:wrap}
.blb-lb .cap b{color:#fff;font-weight:500;font-size:16px}.blb-lb .cap small{color:#B7B0A8;font-size:13px;display:block;margin-top:2px}
.blb-lb .cap button{font-family:inherit;font-size:12px;letter-spacing:.1em;text-transform:uppercase;padding:10px 16px;border-radius:8px;border:1px solid #4a4640;background:transparent;color:#fff}
.blb-lb .cap button.pri{background:#fff;color:#232120;border-color:#fff}
.blb-lb .x{position:absolute;top:18px;right:22px;width:40px;height:40px;border-radius:99px;border:0;background:rgba(255,255,255,.14);color:#fff;font-size:22px}
.blb-lb .arw{position:absolute;top:50%;transform:translateY(-50%);width:46px;height:46px;border-radius:99px;border:0;background:rgba(255,255,255,.14);color:#fff;font-size:22px}
.blb-lb .arw.prev{left:20px}.blb-lb .arw.next{right:20px}
.blb-toast{position:fixed;bottom:26px;left:50%;transform:translateX(-50%) translateY(20px);background:#232120;color:#fff;font-size:13.5px;padding:12px 20px;border-radius:99px;opacity:0;transition:.25s;z-index:100000;pointer-events:none;font-family:'Jost',system-ui,sans-serif}
.blb-toast.on{opacity:1;transform:translateX(-50%) translateY(0)}
</style>

<div class="blb">
  <div class="blb-hero">
    <p class="blb-eye">Lookbook 2026 · Designer-staged rooms</p>
    <h2 class="blb-h">Browse the collection.</h2>
    <p class="blb-sub">Every set is a real room styled by our designers with furniture from a leading brand. Filter by room, style or brand, then copy a look's code and send it with your order — we'll stage your photos in that exact style.</p>
  </div>

  <div class="blb-bar">
    <div class="blb-row">
      <label class="blb-search"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#9C978F" stroke-width="1.7"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/></svg><input type="text" class="blb-q" placeholder="Search a code, room or style"></label>
      <select class="blb-sel blb-style"><option value="">All styles</option>__STYLES__</select>
      <select class="blb-sel blb-brand"><option value="">All brands</option>__BRANDS__</select>
    </div>
    <div class="blb-chips">
      <button class="blb-chip blb-room on" data-room="">All</button>__ROOMS__
      <span class="blb-count"></span>
      <button class="blb-clear" type="button">Clear</button>
    </div>
  </div>

  <div class="blb-grid"></div>
  <div class="blb-empty" style="display:none">No sets match those filters. Try clearing a filter.</div>
</div>

<div class="blb-lb" aria-hidden="true">
  <button class="x" aria-label="Close">&times;</button>
  <button class="arw prev" aria-label="Previous">&#8249;</button>
  <button class="arw next" aria-label="Next">&#8250;</button>
  <figure>
    <img alt="">
    <div class="cap"><div><b class="lb-label"></b><small class="lb-meta"></small></div>
      <div style="display:flex;gap:10px"><button class="lb-copy pri">Copy code</button></div></div>
  </figure>
</div>
<div class="blb-toast"></div>

<script>
(function(){
  var DATA=__DATA__;
  var root=document.querySelector('.blb'); if(!root||root.dataset.on) return; root.dataset.on='1';
  var lb=document.querySelector('.blb-lb'), toastEl=document.querySelector('.blb-toast');
  var grid=root.querySelector('.blb-grid'), empty=root.querySelector('.blb-empty');
  var q=root.querySelector('.blb-q'), styleSel=root.querySelector('.blb-style'), brandSel=root.querySelector('.blb-brand'), countEl=root.querySelector('.blb-count');
  var state={room:'',style:'',brand:'',q:''}, view=[];
  function esc(s){return (s+'').replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  function toast(m){toastEl.textContent=m;toastEl.classList.add('on');clearTimeout(toast._t);toast._t=setTimeout(function(){toastEl.classList.remove('on');},1900);}
  function copy(t){try{navigator.clipboard.writeText(t);}catch(e){}toast('Copied '+t);}
  function match(d){
    if(state.room&&d.room!==state.room) return false;
    if(state.style&&d.style!==state.style) return false;
    if(state.brand&&d.brand!==state.brand) return false;
    if(state.q){var s=(d.sku+' '+d.room+' '+d.style+' '+(d.brand||'')+' '+d.label).toLowerCase(); if(s.indexOf(state.q)<0) return false;}
    return true;
  }
  function render(){
    view=DATA.filter(match);
    grid.innerHTML=view.map(function(d,i){
      return '<article class="blb-card" data-i="'+i+'"><div class="blb-ph"><span class="blb-sku">'+esc(d.sku)+'</span>'
        +'<img loading="lazy" src="'+esc(d.img)+'" alt="'+esc(d.label)+' — '+esc(d.room)+'"></div>'
        +'<div class="blb-body"><b>'+esc(d.label)+'</b><span>'+esc(d.room)+' · '+esc(d.style)+'</span></div></article>';
    }).join('');
    empty.style.display=view.length?'none':'block';
    countEl.textContent=view.length+' set'+(view.length!==1?'s':'');
  }
  // filters
  root.querySelectorAll('.blb-room').forEach(function(b){ b.onclick=function(){
    root.querySelectorAll('.blb-room').forEach(function(x){x.classList.remove('on');}); b.classList.add('on');
    state.room=b.getAttribute('data-room'); render();
  };});
  styleSel.onchange=function(){state.style=styleSel.value;render();};
  brandSel.onchange=function(){state.brand=brandSel.value;render();};
  q.oninput=function(){state.q=q.value.trim().toLowerCase();render();};
  root.querySelector('.blb-clear').onclick=function(){
    state={room:'',style:'',brand:'',q:''}; q.value='';styleSel.value='';brandSel.value='';
    root.querySelectorAll('.blb-room').forEach(function(x){x.classList.remove('on');});
    root.querySelector('.blb-room[data-room=""]').classList.add('on'); render();
  };
  // lightbox
  var lbi=0;
  function openLB(i){ lbi=i; var d=view[i]; if(!d) return;
    lb.querySelector('img').src=d.img; lb.querySelector('img').alt=d.label;
    lb.querySelector('.lb-label').textContent=d.label;
    lb.querySelector('.lb-meta').textContent=d.room+' · '+d.style+' · '+d.sku;
    lb.querySelector('.lb-copy').onclick=function(){copy(d.sku);};
    lb.classList.add('on');
  }
  function step(n){ if(!view.length) return; lbi=(lbi+n+view.length)%view.length; openLB(lbi); }
  function closeLB(){ lb.classList.remove('on'); }
  grid.addEventListener('click',function(e){ var c=e.target.closest('.blb-card'); if(c) openLB(+c.getAttribute('data-i')); });
  lb.querySelector('.x').onclick=closeLB;
  lb.querySelector('.prev').onclick=function(){step(-1);};
  lb.querySelector('.next').onclick=function(){step(1);};
  lb.addEventListener('click',function(e){ if(e.target===lb) closeLB(); });
  document.addEventListener('keydown',function(e){ if(!lb.classList.contains('on')) return;
    if(e.key==='Escape')closeLB(); if(e.key==='ArrowLeft')step(-1); if(e.key==='ArrowRight')step(1); });
  render();
})();
</script>
'''

def opts(vals): return "".join('<option value="%s">%s</option>'%(v,v) for v in vals)
def chips(vals): return "".join('<button class="blb-chip blb-room" data-room="%s">%s</button>'%(r,r) for r in vals)

out = (BLOCK
    .replace("__STYLES__", opts(styles))
    .replace("__BRANDS__", opts(brands))
    .replace("__ROOMS__", chips(rooms))
    .replace("__DATA__", DATA))

(ROOT/"bella-lookbook-2026-shopify.html").write_text(out)
print("wrote bella-lookbook-2026-shopify.html — %d sets, %d rooms / %d styles / %d brands" % (len(items),len(rooms),len(styles),len(brands)))
