#!/usr/bin/env python3
"""Generate the ops catalog database (bella-catalog-db.html) from the same
tiles that drive the lookbook. Every number on the page is counted from
assets/lookbook/ — nothing is hardcoded, so adding tiles and re-running this
keeps the lookbook and the database in lockstep.

Re-run alongside scripts/gen-lookbook.py after adding or replacing tiles.
"""
import json, sys, pathlib, collections
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from catalog_data import ROOT, ROOM_ORDER, BRAND_ORDER, STYLE_ORDER, load_items

items = load_items()

# ---- roll the flat set list up into collections -------------------------------
# A "collection" is either a furniture brand (branded sets) or a design style
# (the unbranded style catalogue). Both are counted the same way.
def rollup(records, key, order):
    out = []
    for name in order:
        mine = [r for r in records if r[key] == name]
        if not mine:
            continue
        out.append({
            "name": name,
            "count": len(mine),
            "rooms": {r: sum(1 for x in mine if x["room"] == r) for r in ROOM_ORDER
                      if any(x["room"] == r for x in mine)},
            "styles": sorted({x["style"] for x in mine}),
            "skus": [x["sku"] for x in mine],
        })
    return out

branded = [i for i in items if i["type"] == "brand"]
styled = [i for i in items if i["type"] == "style"]

COLLECTIONS = ([dict(c, kind="brand") for c in rollup(branded, "brand", BRAND_ORDER)] +
               [dict(c, kind="style") for c in rollup(styled, "style", STYLE_ORDER)])

SETS = {i["sku"]: {"sku": i["sku"], "img": i["img"], "room": i["room"],
                   "style": i["style"], "brand": i.get("brand"), "label": i["label"]}
        for i in items}

room_totals = collections.Counter(i["room"] for i in items)
STATS = {
    "sets": len(items),
    "branded": len(branded),
    "styled": len(styled),
    "brands": len({i["brand"] for i in branded}),
    "styles": len({i["style"] for i in styled}),
    "rooms": [{"name": r, "count": room_totals[r]} for r in ROOM_ORDER if room_totals[r]],
}

HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Catalog database — Bella Ops</title>
<meta name="description" content="Bella Virtual internal catalog database: how many furniture sets exist per brand and per style, and the sets behind each number.">
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500&display=swap" rel="stylesheet">
<style>
  :root{--bg:#FBFAF8;--ink:#232120;--soft:#5E5A56;--faint:#9C978F;--line:#E8E4DE;--line-2:#F0EDE8;--dark:#1C1A18;--green:#3E6B4C;--gold:#B8985A;--blue:#3E6076;--amber:#B5892F;--purple:#6B4E86;--red:#C4553F;--pad:34px}
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:var(--bg);color:var(--ink);font-family:"Jost",system-ui,sans-serif;font-weight:300;font-size:15px;line-height:1.5;-webkit-font-smoothing:antialiased}
  a{text-decoration:none;color:inherit}
  .micro{font-size:11px;letter-spacing:.13em;text-transform:uppercase;color:var(--faint)}
  button{font-family:inherit;cursor:pointer}
  .btn-line{background:transparent;color:var(--ink);border:1px solid var(--line);border-radius:6px;padding:8px 13px;font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;transition:.15s}
  .btn-line:hover{border-color:var(--ink)}

  header{position:sticky;top:0;z-index:40;background:#fff;border-bottom:1px solid var(--line)}
  .nav{display:flex;align-items:center;gap:22px;height:60px;padding:0 var(--pad);max-width:1440px;margin:0 auto}
  .mark{font-size:15px;letter-spacing:.42em;font-weight:400}
  .pill{font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--green);border:1px solid rgba(62,107,76,.4);border-radius:999px;padding:5px 11px}
  .nav .lk{font-size:13px;color:var(--soft)}
  .nav .lk.on{color:var(--ink)}
  .nav .lk:hover{color:var(--ink)}
  .nav .sp{margin-left:auto}
  .search{display:flex;align-items:center;gap:8px;background:var(--bg);border:1px solid var(--line);border-radius:7px;padding:7px 11px;min-width:240px}
  .search input{border:0;background:transparent;font-family:inherit;font-size:13px;outline:0;width:100%}
  .search svg{width:15px;height:15px;stroke:var(--faint);fill:none;stroke-width:1.6;flex:none}
  .acct{display:flex;align-items:center;gap:8px;font-size:13px;color:var(--soft)}
  .acct .av{width:28px;height:28px;border-radius:50%;background:var(--green);color:#fff;font-size:11px;display:grid;place-items:center}

  .wrap{max-width:1440px;margin:0 auto;padding:26px var(--pad) 70px}
  .h1row{display:flex;align-items:flex-end;justify-content:space-between;gap:20px;flex-wrap:wrap;margin-bottom:20px}
  .h1row h1{font-size:26px;font-weight:300;letter-spacing:-.01em}
  .h1row .sub{font-size:13px;color:var(--soft);margin-top:3px}

  .kpis{display:grid;grid-template-columns:repeat(5,1fr);gap:6px;margin-bottom:10px}
  @media(max-width:1080px){.kpis{grid-template-columns:repeat(3,1fr)}}
  @media(max-width:620px){.kpis{grid-template-columns:1fr 1fr}}
  .kpi{background:#fff;border:1px solid var(--line);border-radius:9px;padding:15px 16px;text-align:left}
  .kpi b{display:block;font-size:26px;font-weight:300;line-height:1}
  .kpi .lb{font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--faint);margin-top:8px}

  .roomstrip{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:24px}
  .roomstrip .rm{background:#fff;border:1px solid var(--line);border-radius:8px;padding:8px 13px;font-size:12.5px;color:var(--soft);display:flex;align-items:center;gap:8px}
  .roomstrip .rm b{font-weight:400;color:var(--ink)}

  .board{display:grid;grid-template-columns:1fr 1fr;gap:22px;align-items:start}
  @media(max-width:1080px){.board{grid-template-columns:1fr}}
  .panel{background:#fff;border:1px solid var(--line);border-radius:11px;overflow:hidden}
  .panel-h{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:15px 18px;border-bottom:1px solid var(--line-2);flex-wrap:wrap}
  .panel-h h2{font-size:15px;font-weight:400}
  table{width:100%;border-collapse:collapse}
  thead th{font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--faint);text-align:left;font-weight:400;padding:11px 16px;border-bottom:1px solid var(--line-2);white-space:nowrap}
  thead th.num{text-align:right}
  tbody td{padding:12px 16px;border-bottom:1px solid var(--line-2);font-size:13.5px;vertical-align:middle}
  tbody tr:last-child td{border-bottom:0}
  tbody tr{transition:background .12s;cursor:pointer}
  tbody tr:hover{background:var(--bg)}
  tbody tr.on{background:#F4F1EC}
  tbody tr.on td:first-child{box-shadow:inset 3px 0 0 var(--ink)}
  td.num{text-align:right;font-size:15px}
  .cname{display:flex;align-items:center;gap:9px}
  .tag{font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;border-radius:999px;padding:3px 8px;border:1px solid}
  .tag.brand{color:var(--green);border-color:rgba(62,107,76,.35)}
  .tag.style{color:var(--blue);border-color:rgba(62,96,118,.32)}
  .bar{height:5px;border-radius:99px;background:var(--line-2);overflow:hidden;margin-top:6px;max-width:190px}
  .bar i{display:block;height:100%;border-radius:99px;background:var(--ink)}
  tr.k-style .bar i{background:var(--blue)}
  .rooms{font-size:11.5px;color:var(--faint);margin-top:3px}

  /* drill-in */
  .detail{position:sticky;top:86px}
  .dhead{padding:16px 18px;border-bottom:1px solid var(--line-2)}
  .dhead h2{font-size:17px;font-weight:400}
  .dhead .dsub{font-size:12.5px;color:var(--soft);margin-top:3px}
  .dfilter{display:flex;gap:5px;flex-wrap:wrap;padding:12px 18px;border-bottom:1px solid var(--line-2)}
  .dfilter button{font-size:11.5px;color:var(--soft);background:transparent;border:1px solid var(--line);border-radius:99px;padding:5px 11px;transition:.14s}
  .dfilter button:hover{border-color:var(--ink);color:var(--ink)}
  .dfilter button.on{background:var(--ink);color:#fff;border-color:var(--ink)}
  .sets{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;padding:16px 18px;max-height:620px;overflow-y:auto}
  @media(max-width:620px){.sets{grid-template-columns:repeat(2,1fr)}}
  .set{border:1px solid var(--line);border-radius:9px;overflow:hidden;background:var(--bg)}
  .set img{width:100%;height:auto;display:block}
  .set .sm{padding:7px 9px 8px}
  .set .ssku{font-size:11px;letter-spacing:.05em;color:var(--soft);background:#fff;border:1px solid var(--line);border-radius:5px;padding:2px 6px;cursor:copy;display:inline-block;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;transition:.15s}
  .set .ssku:hover{color:var(--ink);border-color:var(--soft)}
  .set .ssku.copied{color:var(--green);border-color:var(--green)}
  .set .srm{font-size:11px;color:var(--faint);margin-top:4px}
  .empty{padding:40px 18px;text-align:center;color:var(--faint);font-size:13px}

  .toast{position:fixed;left:50%;bottom:26px;transform:translateX(-50%) translateY(14px);background:var(--dark);color:#fff;font-size:13px;padding:10px 17px;border-radius:7px;opacity:0;pointer-events:none;transition:.22s;z-index:80}
  .toast.on{opacity:1;transform:translateX(-50%) translateY(0)}
  @media(prefers-reduced-motion:reduce){*{transition:none!important}}
</style>
</head>
<body>
<header>
  <div class="nav">
    <a class="mark" href="bella-homepage-redesign.html">BELLA</a>
    <span class="pill">Control Center</span>
    <a class="lk" href="bella-cms.html">Queue</a>
    <a class="lk" href="bella-dashboard.html">Clients</a>
    <a class="lk" href="bella-studio.html">Studio portal</a>
    <a class="lk on" href="bella-catalog-db.html">Catalog</a>
    <span class="sp"></span>
    <div class="search"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3-3"/></svg><input id="search" placeholder="Search a SKU, brand, style or room…"></div>
    <div class="acct"><span class="av">BV</span>Bella Ops</div>
  </div>
</header>

<div class="wrap">
  <div class="h1row">
    <div>
      <h1>Catalog database</h1>
      <div class="sub">Every furniture set we hold, counted by brand and by style. Pick a collection to see the sets behind the number.</div>
    </div>
    <a class="btn-line" href="bella-lookbook.html">Open client lookbook →</a>
  </div>

  <div class="kpis" id="kpis"></div>
  <div class="roomstrip" id="roomstrip"></div>

  <div class="board">
    <div class="panel">
      <div class="panel-h">
        <h2>Collections</h2>
        <span class="micro" id="collCount"></span>
      </div>
      <div style="overflow-x:auto">
        <table>
          <thead><tr><th>Collection</th><th class="num">Sets</th><th class="num">Share</th></tr></thead>
          <tbody id="rows"></tbody>
        </table>
      </div>
    </div>

    <div class="panel detail">
      <div class="dhead">
        <h2 id="dTitle">Select a collection</h2>
        <div class="dsub" id="dSub">Click any row to browse its sets.</div>
      </div>
      <div class="dfilter" id="dFilter"></div>
      <div class="sets" id="sets"></div>
    </div>
  </div>
</div>

<div class="toast" id="toast"></div>

<script>
const COLLECTIONS=__COLLECTIONS__;
const SETS=__SETS__;
const STATS=__STATS__;

const $=id=>document.getElementById(id);
let sel=null, roomFilter='All', q='';

function toast(m){const t=$('toast');t.textContent=m;t.classList.add('on');clearTimeout(t._t);t._t=setTimeout(()=>t.classList.remove('on'),1500);}
function copy(sku,el){
  navigator.clipboard&&navigator.clipboard.writeText(sku).then(()=>toast('Copied '+sku)).catch(()=>toast(sku));
  if(el){el.classList.add('copied');setTimeout(()=>el.classList.remove('copied'),900);}
}

// ---- header stats -----------------------------------------------------------
$('kpis').innerHTML=[
  ['Total sets',STATS.sets],['Branded sets',STATS.branded],['Brands',STATS.brands],
  ['Style sets',STATS.styled],['Styles',STATS.styles]
].map(([l,v])=>`<div class="kpi"><b>${v}</b><div class="lb">${l}</div></div>`).join('');
$('roomstrip').innerHTML=STATS.rooms.map(r=>`<span class="rm">${r.name} <b>${r.count}</b></span>`).join('');

// ---- collections table ------------------------------------------------------
function matches(c){
  if(!q) return true;
  const s=q.toLowerCase();
  if(c.name.toLowerCase().includes(s)) return true;
  if(Object.keys(c.rooms).some(r=>r.toLowerCase().includes(s))) return true;
  if(c.styles.some(x=>x.toLowerCase().includes(s))) return true;
  return c.skus.some(k=>k.toLowerCase().includes(s));
}
function renderRows(){
  const list=COLLECTIONS.filter(matches);
  const max=Math.max(...COLLECTIONS.map(c=>c.count),1);
  $('collCount').textContent=list.length+' of '+COLLECTIONS.length;
  if(!list.length){$('rows').innerHTML='<tr><td colspan="3" class="empty">No collection matches that search.</td></tr>';return;}
  $('rows').innerHTML=list.map(c=>{
    const rooms=Object.entries(c.rooms).map(([r,n])=>r+' '+n).join(' · ');
    const share=(c.count/STATS.sets*100).toFixed(1);
    return `<tr class="k-${c.kind}${sel===c.name?' on':''}" data-name="${c.name}">
      <td><div class="cname"><span>${c.name}</span><span class="tag ${c.kind}">${c.kind}</span></div>
          <div class="rooms">${rooms}</div>
          <div class="bar"><i style="width:${c.count/max*100}%"></i></div></td>
      <td class="num">${c.count}</td>
      <td class="num">${share}%</td></tr>`;
  }).join('');
}
$('rows').addEventListener('click',e=>{
  const tr=e.target.closest('tr[data-name]'); if(!tr) return;
  select(tr.dataset.name);
});

// ---- drill-in ---------------------------------------------------------------
function select(name){
  sel=name; roomFilter='All';
  renderRows(); renderDetail();
  document.querySelector('.detail').scrollIntoView({block:'nearest',behavior:'smooth'});
}
function renderDetail(){
  const c=COLLECTIONS.find(x=>x.name===sel);
  if(!c){$('dTitle').textContent='Select a collection';$('dSub').textContent='Click any row to browse its sets.';
    $('dFilter').innerHTML='';$('sets').innerHTML='<div class="empty">No collection selected.</div>';return;}
  $('dTitle').textContent=c.name;
  const styleNote=c.kind==='brand'?' · '+c.styles.join(', '):'';
  $('dSub').textContent=c.count+' set'+(c.count===1?'':'s')+styleNote;
  const rooms=['All',...Object.keys(c.rooms)];
  $('dFilter').innerHTML=rooms.map(r=>{
    const n=r==='All'?c.count:c.rooms[r];
    return `<button class="${roomFilter===r?'on':''}" data-room="${r}">${r} ${n}</button>`;
  }).join('');
  const skus=c.skus.filter(k=>roomFilter==='All'||SETS[k].room===roomFilter);
  $('sets').innerHTML=skus.map(k=>{const s=SETS[k];
    return `<div class="set"><img loading="lazy" src="${s.img}" alt="${s.room} styled ${s.style} (${s.sku})">
      <div class="sm"><button class="ssku" data-sku="${s.sku}" title="Click to copy ${s.sku}">${s.sku}</button>
      <div class="srm">${s.room} · ${s.style}</div></div></div>`;
  }).join('');
}
$('dFilter').addEventListener('click',e=>{
  const b=e.target.closest('button[data-room]'); if(!b) return;
  roomFilter=b.dataset.room; renderDetail();
});
$('sets').addEventListener('click',e=>{
  const b=e.target.closest('.ssku'); if(b) copy(b.dataset.sku,b);
});

$('search').addEventListener('input',e=>{q=e.target.value.trim();renderRows();});

renderRows(); renderDetail();
})();
</script>
</body>
</html>
'''

# the IIFE wrapper the other ops pages use, applied after template substitution
HTML = HTML.replace("<script>\nconst COLLECTIONS", "<script>\n(function(){\nconst COLLECTIONS")

HTML = (HTML.replace("__COLLECTIONS__", json.dumps(COLLECTIONS, separators=(",", ":")))
            .replace("__SETS__", json.dumps(SETS, separators=(",", ":")))
            .replace("__STATS__", json.dumps(STATS, separators=(",", ":"))))

(ROOT / "bella-catalog-db.html").write_text(HTML)
print(f"wrote bella-catalog-db.html | {STATS['sets']} sets | "
      f"{STATS['brands']} brands ({STATS['branded']} sets) | "
      f"{STATS['styles']} styles ({STATS['styled']} sets)")
for c in COLLECTIONS:
    print(f"  {c['kind']:6s} {c['name']:20s} {c['count']:3d}")
