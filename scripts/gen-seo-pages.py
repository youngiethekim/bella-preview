#!/usr/bin/env python3
"""Generate Bella's new SEO pages from the shared service-page template.
Run from repo root: python3 scripts/gen-seo-pages.py
Keeps chrome (CSS/header/footer) identical to bella-service-virtual-staging.html
so the new pages are visually consistent; per-page copy is keyword-targeted.
"""
import html, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

CSS = """
  :root{--bg:#FDFCFA;--ink:#232120;--soft:#6E6A66;--faint:#9C978F;--line:#E8E4DE;--line-2:#F0EDE8;--dark:#1C1A18;--green:#3E6B4C;--gold:#3E6B4C;--pad:44px}
  *{box-sizing:border-box;margin:0;padding:0}
  html{scroll-behavior:smooth}
  body{background:var(--bg);color:var(--ink);font-family:"Jost",system-ui,sans-serif;font-weight:300;font-size:16px;line-height:1.6;-webkit-font-smoothing:antialiased}
  img{display:block;max-width:100%}a{text-decoration:none;color:inherit}
  h1,h2,h3{font-weight:300;letter-spacing:-.012em;line-height:1.1}
  .micro{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--faint)}
  .wrap{max-width:1200px;margin:0 auto;padding:0 var(--pad)}
  .btn{display:inline-block;background:var(--ink);color:#fff;font-size:12.5px;letter-spacing:.14em;text-transform:uppercase;padding:14px 24px;cursor:pointer;border:0;font-family:inherit;transition:background .2s,color .2s}
  .btn:hover{background:var(--green);color:#fff}
  .btn-ghost{background:transparent;border:1px solid var(--ink);color:var(--ink)}.btn-ghost:hover{background:var(--ink);color:#fff}
  .btn-wht{background:#fff;color:var(--ink)}.btn-wht:hover{background:var(--green);color:#fff}
  header{position:sticky;top:0;z-index:70;background:rgba(253,252,250,.9);backdrop-filter:blur(10px);border-bottom:1px solid var(--line-2)}
  .nav{display:flex;align-items:center;gap:36px;height:68px;padding:0 var(--pad);max-width:1200px;margin:0 auto}
  .mark{font-size:15px;letter-spacing:.5em;font-weight:400}.nav .sp{margin-left:auto}
  .nav a.lnk{font-size:12.5px;letter-spacing:.13em;text-transform:uppercase;color:var(--soft)}.nav a.lnk:hover{color:var(--ink)}
  @media(max-width:760px){.nav a.lnk{display:none}}
  .crumb{max-width:1200px;margin:0 auto;padding:16px var(--pad) 0;font-size:12px;letter-spacing:.06em;color:var(--faint)}
  .crumb a{color:var(--soft)}.crumb a:hover{color:var(--ink)}
  .hero-in{display:grid;grid-template-columns:1.05fr 1fr;gap:0;align-items:stretch;max-width:1400px;margin:0 auto}
  @media(max-width:900px){.hero-in{grid-template-columns:1fr}}
  .hero .copy{padding:56px var(--pad) 60px}
  .hero h1{font-size:clamp(32px,4.2vw,54px);max-width:15ch;margin-top:12px}
  .hero h1 em{font-style:normal;color:var(--green)}
  .hero .copy>p{color:var(--soft);margin-top:18px;font-size:17px;max-width:46ch}
  .hero .row{display:flex;gap:12px;margin-top:28px;flex-wrap:wrap}
  .hero .cred{display:flex;align-items:center;gap:8px;margin-top:20px;font-size:12.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--soft)}
  .hero .cred svg{width:15px;height:15px;fill:var(--gold)}.hero .cred b{color:var(--ink);font-weight:400}
  .hero .shot{position:relative;background:#EFECE8;min-height:360px}
  .hero .shot img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
  .hero .shot .lbl{position:absolute;left:16px;bottom:16px;font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:#fff;background:rgba(20,18,16,.6);padding:6px 12px;backdrop-filter:blur(3px)}
  .strip{display:flex;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
  .strip div{flex:1;padding:20px 16px;text-align:center;font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--soft);border-right:1px solid var(--line)}
  .strip div:last-child{border-right:0}.strip b{color:var(--ink);font-weight:400}
  @media(max-width:760px){.strip{flex-wrap:wrap}.strip div{flex:1 1 50%}}
  section{padding:72px 0}
  .head{max-width:760px}.head h2{font-size:clamp(25px,2.9vw,38px);margin-top:10px}.head p{margin-top:14px;font-size:16px;color:var(--soft)}
  .def{max-width:820px}.def p{font-size:18px;color:var(--ink);line-height:1.6;font-weight:300}.def p+p{margin-top:18px;font-size:16px;color:var(--soft)}
  .steps{display:grid;grid-template-columns:repeat(3,1fr);gap:0;margin-top:40px}
  @media(max-width:820px){.steps{grid-template-columns:1fr}}
  .step{padding:24px 26px 0;border-left:1px solid var(--line)}.step:first-child{border-left:0;padding-left:0}
  .step .n{font-size:12px;letter-spacing:.14em;color:var(--green)}
  .step h3{font-size:18px;margin:8px 0 6px}.step p{font-size:14px;color:var(--soft)}
  @media(max-width:820px){.step{border-left:0;border-top:1px solid var(--line);padding:22px 0 0;margin-top:20px}.step:first-child{border-top:0;margin-top:0}}
  .proof{background:var(--bg);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
  .ba{display:grid;grid-template-columns:1fr 1fr;gap:5px;margin-top:36px}
  @media(max-width:700px){.ba{grid-template-columns:1fr}}
  .ba figure{position:relative;margin:0;background:#EFECE8}
  .ba img{width:100%;aspect-ratio:1.5;object-fit:cover;display:block}
  .ba figcaption{position:absolute;left:14px;top:14px;font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:#fff;background:rgba(20,18,16,.62);padding:5px 11px}
  .price-wrap{display:grid;grid-template-columns:1fr 1fr;gap:5px;margin-top:40px;align-items:stretch}
  @media(max-width:820px){.price-wrap{grid-template-columns:1fr}}
  .price-card{background:#fff;border:1px solid var(--line);padding:34px 32px;display:flex;flex-direction:column}
  .price-card.feat{background:var(--dark);color:#fff;border-color:var(--dark)}
  .price-card h3{font-size:19px}.price-card .amt{font-size:40px;font-weight:300;margin:12px 0 4px}.price-card .amt small{font-size:15px;color:var(--faint)}
  .price-card.feat .amt small{color:#A9A49A}
  .price-card ul{list-style:none;margin:18px 0 0;display:grid;gap:11px}
  .price-card li{font-size:14.5px;color:var(--soft);padding-left:22px;position:relative}
  .price-card.feat li{color:#CFC9C0}
  .price-card li::before{content:"\\2713";position:absolute;left:0;color:var(--green)}
  .price-card .btn{margin-top:24px;text-align:center}
  .related{background:var(--bg);border-top:1px solid var(--line)}
  .related-row{display:flex;gap:8px 26px;flex-wrap:wrap;margin-top:20px}
  .related-row a{font-size:14px;color:var(--soft);border-bottom:1px solid var(--line);padding-bottom:2px}
  .related-row a:hover{color:var(--ink);border-color:var(--ink)}
  .faq{max-width:820px}
  details{border-bottom:1px solid var(--line)}
  summary{padding:22px 0;cursor:pointer;font-size:17px;font-weight:400;list-style:none;display:flex;justify-content:space-between;gap:20px;align-items:center}
  summary::-webkit-details-marker{display:none}
  summary::after{content:"+";font-size:20px;color:var(--green);transition:transform .2s}
  details[open] summary::after{transform:rotate(45deg)}
  details p{padding:0 0 22px;color:var(--soft);font-size:15px;max-width:70ch}
  .cta{background:var(--dark);color:#fff;text-align:center}
  .cta-in{padding:70px var(--pad);max-width:820px;margin:0 auto}
  .cta h2{color:#fff;font-size:clamp(28px,3.4vw,44px)}.cta p{color:#A9A49A;margin:16px auto 0}
  .cta .row{display:flex;gap:12px;justify-content:center;margin-top:28px;flex-wrap:wrap}.cta .fine{margin-top:18px;font-size:13px;color:#807A72}
  /* prose (guide) */
  .prose{max-width:760px;margin:0 auto}
  .prose h2{font-size:clamp(23px,2.6vw,32px);margin:44px 0 14px}
  .prose h3{font-size:20px;margin:30px 0 10px}
  .prose p{color:var(--soft);margin-top:14px;font-size:16.5px}
  .prose ul{margin:14px 0 0 22px;color:var(--soft)}.prose li{margin-top:8px}
  .prose .lead{font-size:19px;color:var(--ink)}
  .toc{background:#fff;border:1px solid var(--line);padding:22px 26px;margin:30px 0}
  .toc .micro{margin-bottom:12px}.toc a{display:block;color:var(--soft);font-size:14.5px;padding:5px 0;border-bottom:1px solid var(--line-2)}
  .toc a:last-child{border-bottom:0}.toc a:hover{color:var(--green)}
  /* comparison table */
  .cmp{width:100%;border-collapse:collapse;margin-top:36px;font-size:14.5px}
  .cmp th,.cmp td{text-align:left;padding:16px 18px;border-bottom:1px solid var(--line);vertical-align:top}
  .cmp thead th{font-weight:400;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--faint)}
  .cmp .col-pro{background:#fff;border-left:1px solid var(--line);border-right:1px solid var(--line)}
  .cmp thead .col-pro{color:var(--green);font-weight:500}
  .cmp td:first-child{color:var(--ink)}
  .cmp-wrap{overflow-x:auto}
  footer{background:var(--dark);color:#8a857d;padding:40px var(--pad);font-size:12.5px}
  .foot{max-width:1200px;margin:0 auto}
  .foot .seg{display:flex;flex-wrap:wrap;gap:8px 22px;padding-bottom:22px;border-bottom:1px solid #2E2B28;margin-bottom:20px}
  .foot .seg .micro{width:100%;color:#6F6A63;margin-bottom:10px}
  .foot .seg a{font-size:13px;color:#A8A29A}.foot .seg a:hover{color:#fff}
  .foot .base{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
  .foot .base a{color:#A8A29A;text-decoration:underline}
"""

HEADER = """
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
"""

FOOTER = """
<footer>
  <div class="foot">
    <div class="seg">
      <span class="micro">Bella Virtual</span>
      <a href="bella-services.html">Services</a>
      <a href="bella-service-virtual-staging.html">Virtual staging</a>
      <a href="bella-service-virtual-land-staging.html">Virtual land staging</a>
      <a href="bella-service-3d-rendering.html">3D rendering</a>
      <a href="bella-service-floor-plans.html">Floor plans</a>
      <a href="bella-service-photo-editing.html">Photo editing</a>
      <a href="bella-service-3d-tour.html">3D tours</a>
      <a href="bella-pricing.html">Pricing</a>
      <a href="bella-lookbook.html">Lookbook</a>
      <a href="bella-resources.html">Resources</a>
      <a href="bella-order-page.html">Get started</a>
    </div>
    <div class="base">
      <span>&copy; Bella Virtual Staging &middot; <a href="bella-homepage-redesign.html">Back to the studio</a></span>
      <span>Real estate virtual staging &amp; visualization &middot; Redesign mockup, not the live site</span>
    </div>
  </div>
</footer>
"""

def doc(title, desc, slug, schema, body):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="https://www.bellavirtual.com/{slug}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="https://www.bellavirtual.com/{slug}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500&display=swap" rel="stylesheet">
<script type="application/ld+json">
{json.dumps(schema, indent=None)}
</script>
<style>{CSS}</style>
</head>
<body>
{HEADER}
{body}
{FOOTER}
</body>
</html>
"""

def faq_schema(pairs):
    return {"@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in pairs]}

def crumb_schema(items):
    return {"@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":i+1,"name":n,"item":u} for i,(n,u) in enumerate(items)]}

def faq_html(pairs):
    out=['<div class="faq" style="margin-top:24px">']
    for i,(q,a) in enumerate(pairs):
        op=" open" if i==0 else ""
        out.append(f'<details{op}><summary>{html.escape(q)}</summary><p>{a}</p></details>')
    out.append('</div>')
    return "\n".join(out)

# ---------- generic service page ----------
def service_page(*, slug, fname, title, desc, service_type, price, micro, h1, sub,
                 hero_img, hero_alt, hero_lbl, strip, def_h2, def_paras, steps,
                 ba_before, ba_after, ba_before_alt, ba_after_alt, pricing_cards,
                 faq, related_label, related_links, cta_h2, cta_p, cta_fine):
    schema={"@context":"https://schema.org","@graph":[
        {"@type":"Service","@id":f"https://www.bellavirtual.com/{slug}#service","serviceType":service_type,
         "name":title.split(" | ")[0],"description":desc,
         "provider":{"@type":"Organization","name":"Bella Virtual Staging","url":"https://www.bellavirtual.com/"},
         "areaServed":["US","CA"],
         **({"offers":{"@type":"Offer","priceCurrency":"USD","price":str(price),"availability":"https://schema.org/InStock"}} if price else {})},
        crumb_schema([("Bella Virtual","https://www.bellavirtual.com/"),
                      ("Services","https://www.bellavirtual.com/services"),
                      (service_type,f"https://www.bellavirtual.com/{slug}")]),
        faq_schema(faq)]}
    strip_html="".join(f"<div>{s}</div>" for s in strip)
    steps_html="".join(
        f'<div class="step"><div class="n">Step {i+1}</div><h3>{h}</h3><p>{p}</p></div>'
        for i,(h,p) in enumerate(steps))
    def_html="".join(f"<p>{p}</p>" for p in def_paras)
    cards=[]
    for c in pricing_cards:
        feat=" feat" if c.get("feat") else ""
        wht=" btn-wht" if c.get("feat") else " btn-ghost"
        lis="".join(f"<li>{l}</li>" for l in c["li"])
        note=f'<span style="font-size:13px;color:{"#A9A49A" if c.get("feat") else "var(--faint)"}">{c["note"]}</span>' if c.get("note") else ""
        cards.append(f'<div class="price-card{feat}"><h3>{c["h"]}</h3><div class="amt">{c["amt"]}</div>{note}<ul>{lis}</ul><a class="btn{wht}" href="{c["href"]}">{c["cta"]}</a></div>')
    rel="".join(f'<a href="{u}">{n}</a>' for n,u in related_links)
    body=f"""
<nav class="crumb"><a href="bella-homepage-redesign.html">Home</a> · <a href="bella-services.html">Services</a> · {service_type}</nav>

<section class="hero">
  <div class="hero-in">
    <div class="copy">
      <p class="micro">{micro}</p>
      <h1>{h1}</h1>
      <p>{sub}</p>
      <div class="row">
        <a class="btn" href="bella-order-page.html">Get started</a>
        <a class="btn btn-ghost" href="bella-lookbook.html">See the lookbook</a>
      </div>
      <div class="cred">
        <svg viewBox="0 0 24 24"><path d="M12 3.5l2.6 5.3 5.9.9-4.3 4.1 1 5.8-5.2-2.7-5.2 2.7 1-5.8-4.3-4.1 5.9-.9z"/></svg>
        <span><b>4.9</b> on Google · by real designers, never one-click AI</span>
      </div>
    </div>
    <div class="shot">
      <img src="{hero_img}" alt="{hero_alt}" fetchpriority="high">
      <span class="lbl">{hero_lbl}</span>
    </div>
  </div>
</section>

<div class="strip">{strip_html}</div>

<section class="wrap">
  <div class="def">
    <p class="micro">What it is</p>
    <h2 style="font-size:clamp(25px,2.9vw,38px);margin:10px 0 18px">{def_h2}</h2>
    {def_html}
  </div>
</section>

<section class="wrap" style="padding-top:0">
  <div class="head"><p class="micro">How it works</p><h2>Three steps, MLS-ready in days.</h2></div>
  <div class="steps">{steps_html}</div>
</section>

<section class="proof">
  <div class="wrap">
    <div class="head"><p class="micro">The difference it makes</p><h2>Before &amp; after.</h2></div>
    <div class="ba">
      <figure><img src="{ba_before}" alt="{ba_before_alt}"><figcaption>Before</figcaption></figure>
      <figure><img src="{ba_after}" alt="{ba_after_alt}"><figcaption>After · by Bella</figcaption></figure>
    </div>
  </div>
</section>

<section class="wrap">
  <div class="head"><p class="micro">Pricing</p><h2>Straightforward pricing. No subscription.</h2></div>
  <div class="price-wrap">{"".join(cards)}</div>
</section>

<section class="related">
  <div class="wrap">
    <p class="micro">{related_label}</p>
    <h2 style="font-size:clamp(24px,2.7vw,34px);margin-top:10px;max-width:24ch">One studio for the whole listing.</h2>
    <div class="related-row">{rel}</div>
  </div>
</section>

<section class="wrap">
  <div class="head"><p class="micro">Questions</p><h2>{service_type} FAQ</h2></div>
  {faq_html(faq)}
</section>

<section class="cta">
  <div class="cta-in">
    <h2>{cta_h2}</h2>
    <p>{cta_p}</p>
    <div class="row">
      <a class="btn btn-wht" href="bella-order-page.html">Get started</a>
      <a class="btn btn-ghost" style="border-color:#4a4640;color:#fff" href="bella-lookbook.html">Browse the lookbook</a>
    </div>
    <p class="fine">{cta_fine}</p>
  </div>
</section>
"""
    (ROOT/fname).write_text(doc(title,desc,slug,schema,body))
    print("wrote",fname)


SIBLINGS=[("Virtual staging","bella-service-virtual-staging.html"),
          ("Virtual land staging","bella-service-virtual-land-staging.html"),
          ("3D rendering","bella-service-3d-rendering.html"),
          ("Floor plans","bella-service-floor-plans.html"),
          ("Photo editing","bella-service-photo-editing.html"),
          ("3D tours","bella-service-3d-tour.html")]

# ===== 1. 3D RENDERING =====
service_page(
  slug="3d-rendering", fname="bella-service-3d-rendering.html",
  title="3D Rendering for Real Estate | Architectural Rendering Services | Bella Virtual",
  desc="Photoreal 3D rendering for real estate — interior and exterior architectural renders that sell pre-construction, renovations and new developments before they're built.",
  service_type="3D rendering", price="", micro="3D rendering",
  h1="Sell the home <em>before it's built.</em>",
  sub="Photoreal real estate 3D rendering of interiors and exteriors, so buyers can walk a home that doesn't physically exist yet. From a floor plan or a set of architectural drawings, our artists build a render buyers believe.",
  hero_img="assets/render/ext-villa-1.jpg",
  hero_alt="A photorealistic 3D exterior rendering of a modern home at dusk",
  hero_lbl="3D exterior render by Bella",
  strip=["<b>Interior</b> &amp; exterior","<b>Photoreal</b> quality","From <b>drawings</b> or floor plans","<b>Unlimited revisions</b>"],
  def_h2="What is real estate 3D rendering?",
  def_paras=[
    "Real estate 3D rendering turns architectural drawings, floor plans or design ideas into photorealistic images of a finished home — inside and out — long before ground is broken. It's the difference between asking a buyer to imagine, and showing them.",
    "Architectural rendering services let builders and developers pre-sell units, help agents market new construction, and let renovators show buyers the after. Every render is built by a 3D artist to match your materials, finishes and light."],
  steps=[("Send your drawings","Upload floor plans, elevations, CAD files or architectural drawings — plus any finishes or references you have in mind."),
         ("We build the render","A 3D artist models the space, applies your materials and lighting, and produces a photoreal interior or exterior render."),
         ("Approve &amp; download","Review, request changes, and download high-resolution renders ready for the MLS, brochures and investor decks.")],
  ba_before="assets/floorplan/fp-2d.jpg", ba_after="assets/render/ext-villa-2.jpg",
  ba_before_alt="A 2D architectural floor plan before 3D rendering",
  ba_after_alt="A photorealistic 3D exterior render produced from the plan",
  pricing_cards=[
    {"feat":True,"h":"3D rendering","amt":"Quoted<small> per project</small>","note":"Interior &amp; exterior · priced by scope","li":["Photoreal interior or exterior renders","Built from your plans or drawings","Your exact materials, finishes &amp; light","Unlimited revisions until it's right"],"href":"bella-order-page.html","cta":"Get a quote"},
    {"h":"Also available","amt":"Add-ons","note":"Round out the listing","li":["3D virtual tours &amp; 360° panoramas","2D &amp; 3D floor plans","Virtual staging for the interiors","Day-to-dusk exterior edits"],"href":"bella-services.html","cta":"See all services"}],
  faq=[("What is 3D rendering in real estate?","Real estate 3D rendering is the creation of photorealistic images of a property — interior or exterior — from architectural drawings, floor plans or design concepts, so buyers can see a finished home before it's built or renovated."),
       ("How much do 3D rendering services cost?","3D rendering is quoted per project because scope varies widely — a single exterior render is very different from a full development. Send us your drawings and we'll return a fixed quote, with no subscription."),
       ("What do you need to start a render?","Floor plans, elevations or CAD/architectural drawings, plus any material and finish selections or reference images. The more detail you provide, the closer the first render lands."),
       ("Can you do both interior and exterior renders?","Yes. We produce interior renders (rooms, kitchens, amenities) and exterior renders (facades, streetscapes, dusk shots) for pre-construction, new developments and renovations."),
       ("How long does a 3D render take?","Most single renders come back within a few business days; larger developments are scheduled by scope. You'll get a timeline with your quote, and revisions are unlimited.")],
  related_label="More visualization services",
  related_links=[(n,u) for n,u in SIBLINGS if u!="bella-service-3d-rendering.html"],
  cta_h2="Ready to render your project?",
  cta_p="Send your drawings and we'll return a fixed quote — photoreal interior and exterior renders buyers believe.",
  cta_fine="Interior &amp; exterior · photoreal · unlimited revisions")

# ===== 2. FLOOR PLANS =====
service_page(
  slug="floor-plans", fname="bella-service-floor-plans.html",
  title="Real Estate Floor Plans | 2D & 3D Floor Plan Services | Bella Virtual",
  desc="Clean 2D floor plans and dimensional 3D floor plans for real estate listings, from $24 a floor. Labelled, MLS-ready in 24–48 hours, drawn from your sketch or measurements.",
  service_type="Floor plans", price="24", micro="Floor plans",
  h1="Floor plans that <em>keep buyers on your listing.</em>",
  sub="A clear, labelled floor plan is one of the most-requested things buyers look for — and listings that have one hold attention longer. We turn your sketch or measurements into clean 2D floor plans and dimensional 3D floor plans, MLS-ready.",
  hero_img="assets/floorplan/fp-3d.jpg",
  hero_alt="A labelled 3D floor plan of a home produced by Bella",
  hero_lbl="3D floor plan by Bella",
  strip=["From <b>$24</b> / floor","<b>2D</b> &amp; <b>3D</b> options","Back in <b>24–48 hrs</b>","<b>Labelled</b> &amp; to scale"],
  def_h2="2D and 3D floor plans, done for you.",
  def_paras=[
    "A real estate floor plan is a scaled, top-down drawing of a home's layout — rooms, dimensions and flow — that helps a buyer understand a property before they ever step inside. Listings with a floor plan answer the \"how does it flow?\" question that photos alone can't.",
    "We produce clean black-and-white 2D floor plans for a fast, professional look, and dimensional 3D floor plans that show furniture and depth. Send a rough sketch, a Matterport scan or on-site measurements and we'll draft it labelled and to scale."],
  steps=[("Send a sketch or measurements","Upload a rough sketch, existing plan, Matterport scan or room measurements — whatever you have."),
         ("We draft the plan","A drafter produces a clean 2D or 3D floor plan, labelled with rooms and dimensions, matched to MLS standards."),
         ("Approve &amp; download","Review, request tweaks, and download print- and MLS-ready files. Revisions are free.")],
  ba_before="assets/floorplan/fp-2d.jpg", ba_after="assets/floorplan/fp-3d-studio.jpg",
  ba_before_alt="A clean 2D real estate floor plan",
  ba_after_alt="A dimensional 3D floor plan of the same layout",
  pricing_cards=[
    {"feat":True,"h":"2D floor plan","amt":"$24<small> / floor</small>","note":"Clean, labelled, to scale","li":["Black-and-white or light-color styling","Room labels and dimensions","Drawn from your sketch or scan","MLS-ready in 24–48 hours"],"href":"bella-order-page.html","cta":"Get started"},
    {"h":"3D floor plan","amt":"Quoted<small> / floor</small>","note":"Dimensional, furnished look","li":["Furniture and depth for realism","Great for brochures and web","Same fast turnaround","Free revisions"],"href":"bella-pricing.html","cta":"See full pricing"}],
  faq=[("How much does a floor plan cost?","Bella's 2D floor plans start at $24 per floor. Dimensional 3D floor plans are quoted per floor by complexity. There's no subscription and no minimum."),
       ("What's the difference between a 2D and 3D floor plan?","A 2D floor plan is a clean, top-down, to-scale drawing with room labels and dimensions — fast and professional. A 3D floor plan adds furniture, depth and perspective, which helps buyers feel the space in brochures and on the web."),
       ("What do you need to draw a floor plan?","A rough sketch, an existing plan, a Matterport scan, or on-site measurements. We convert any of these into a clean, labelled, to-scale floor plan."),
       ("Are your floor plans MLS-ready?","Yes. We build floor plans to standard MLS and listing specifications, labelled with rooms and dimensions, in the file formats portals accept."),
       ("How fast can I get a floor plan?","Most 2D floor plans are back within 24 to 48 hours of receiving your sketch or measurements.")],
  related_label="More listing services",
  related_links=[(n,u) for n,u in SIBLINGS if u!="bella-service-floor-plans.html"],
  cta_h2="Add a floor plan to your listing.",
  cta_p="Send a sketch or measurements and get a clean, labelled 2D or 3D floor plan back in 24 to 48 hours.",
  cta_fine="From $24 a floor · labelled &amp; to scale · MLS-ready")

# ===== 3. PHOTO EDITING =====
service_page(
  slug="photo-editing", fname="bella-service-photo-editing.html",
  title="Real Estate Photo Editing Services | Day-to-Dusk & Sky Replacement | Bella Virtual",
  desc="Real estate photo editing services by hand — day-to-dusk (virtual twilight), sky replacement, brightening and blemish removal. MLS-ready hero shots from $6 a photo.",
  service_type="Photo editing", price="6", micro="Photo editing",
  h1="The polish that <em>stops the scroll.</em>",
  sub="Photo editing for real estate is what turns a good listing photo into a hero shot: day-to-dusk skies, sky replacement, brightening, lens and line correction, and blemish clean-up — edited by hand, not a filter.",
  hero_img="assets/scene/dusk-home.jpg",
  hero_alt="A real estate exterior photo edited to a golden dusk sky",
  hero_lbl="Day-to-dusk edit by Bella",
  strip=["From <b>$6</b> / photo","<b>Day-to-dusk</b> &amp; sky swaps","Edited <b>by hand</b>","Back in <b>24 hrs</b>"],
  def_h2="Real estate photo editing, done by hand.",
  def_paras=[
    "Real estate photo editing is the retouching that makes a listing photo look its best without misrepresenting the home — correcting exposure and color, straightening verticals, replacing a flat sky, and removing distractions like bins or cords.",
    "Our most-requested edit is day-to-dusk (also called virtual twilight): we turn a daytime exterior into a warm, golden-hour shot that consistently earns more clicks as the listing thumbnail. Every edit is done by a retoucher, so it looks real."],
  steps=[("Upload your photos","Send the raw listing photos and flag which ones you want as day-to-dusk, sky swaps, or general clean-up."),
         ("We edit by hand","A retoucher corrects light and color, replaces skies, straightens lines and clears distractions — never an auto-filter."),
         ("Approve &amp; download","Review, request tweaks, and download MLS-ready images. Turnaround is typically 24 hours.")],
  ba_before="assets/hero/hero-before.jpg", ba_after="assets/hero/hero-after.jpg",
  ba_before_alt="A flat daytime real estate exterior photo before editing",
  ba_after_alt="The same exterior after a day-to-dusk photo edit",
  pricing_cards=[
    {"feat":True,"h":"Photo editing","amt":"From $6<small> / photo</small>","note":"Brightening, color &amp; clean-up","li":["Exposure, color &amp; white-balance","Line and lens correction","Blemish and distraction removal","Back in about 24 hours"],"href":"bella-order-page.html","cta":"Get started"},
    {"h":"Day-to-dusk","amt":"From $7<small> / photo</small>","note":"Virtual twilight / sky replacement","li":["Daytime exterior to golden-hour dusk","Sky replacement on flat-sky shots","Window and lighting glow","Higher click-through as the thumbnail"],"href":"bella-pricing.html","cta":"See full pricing"}],
  faq=[("What does real estate photo editing include?","It covers exposure and color correction, white balance, line and perspective straightening, sky replacement, day-to-dusk conversions, and removing distractions like bins, cords or reflections — all done by hand so the home still looks true to life."),
       ("What is a day-to-dusk (virtual twilight) edit?","Day-to-dusk, or virtual twilight, converts a daytime exterior photo into a warm golden-hour or twilight scene with a glowing sky and lit windows. It's one of the highest-performing listing thumbnails because it stands out in search results."),
       ("How much does real estate photo editing cost?","General editing starts at about $6 per photo and day-to-dusk edits from about $7 per photo, with volume pricing. There's no subscription."),
       ("Is edited photography allowed on the MLS?","Yes, as long as edits don't misrepresent the property. We enhance light, color and skies and remove minor distractions, but we don't alter the structure of the home. Confirm any local disclosure rules with your board."),
       ("How fast is turnaround?","Most photo edits are returned within about 24 hours of upload.")],
  related_label="More listing services",
  related_links=[(n,u) for n,u in SIBLINGS if u!="bella-service-photo-editing.html"],
  cta_h2="Give your photos the hero treatment.",
  cta_p="Upload your listing photos and get hand-edited, MLS-ready images — including day-to-dusk — back in about a day.",
  cta_fine="From $6 a photo · day-to-dusk from $7 · edited by hand")

print("service pages done")

# ===== 4. WHAT IS VIRTUAL STAGING (guide) =====
def guide_what_is():
    slug="what-is-virtual-staging"; fname="bella-what-is-virtual-staging.html"
    title="What Is Virtual Staging? A Complete Guide for Real Estate | Bella Virtual"
    desc="What is virtual staging? A plain-English guide: how it works, what it costs, whether it's allowed on the MLS, and how it compares to physical staging for real estate."
    faq=[("What is virtual staging in real estate?","Virtual staging in real estate is the practice of digitally adding furniture and decor to a photo of an empty or dated room, so buyers browsing online can picture themselves living in the home. It's done in editing software by a designer, and the result is a realistic, MLS-ready listing photo."),
         ("How much does virtual staging cost?","Professional virtual staging typically costs $30–$75 per photo. Bella starts at $45 per photo with volume discounts, versus $2,000–$5,000+ to physically stage a home."),
         ("Is virtual staging legal / allowed on the MLS?","Yes. Virtually staged photos are allowed on the MLS in most markets as long as they're clearly disclosed as virtually staged. You should not digitally alter permanent features to hide defects. Confirm exact disclosure wording with your local real estate board."),
         ("Is virtual staging worth it?","For empty, dated or hard-to-picture rooms, yes — staging helps buyers visualize the space, and most buyers' agents report it makes a home easier to sell. At a fraction of physical staging's cost, the return on a single stronger listing photo is high."),
         ("What's the difference between virtual staging and physical staging?","Physical staging places real rented furniture in the home; virtual staging adds designer furniture to the photo digitally. Virtual is far cheaper and faster and can be restyled per buyer, but it only appears in photos — the home is still empty in person.")]
    schema={"@context":"https://schema.org","@graph":[
        {"@type":"Article","headline":"What Is Virtual Staging? A Complete Guide for Real Estate",
         "description":desc,"author":{"@type":"Organization","name":"Bella Virtual Staging"},
         "publisher":{"@type":"Organization","name":"Bella Virtual Staging","url":"https://www.bellavirtual.com/"},
         "mainEntityOfPage":f"https://www.bellavirtual.com/{slug}"},
        crumb_schema([("Bella Virtual","https://www.bellavirtual.com/"),
                      ("Resources","https://www.bellavirtual.com/resources"),
                      ("What is virtual staging",f"https://www.bellavirtual.com/{slug}")]),
        faq_schema(faq)]}
    body=f"""
<nav class="crumb"><a href="bella-homepage-redesign.html">Home</a> · <a href="bella-resources.html">Resources</a> · What is virtual staging</nav>

<section class="wrap" style="padding-bottom:0">
  <div class="prose">
    <p class="micro">Guide</p>
    <h1 style="font-size:clamp(30px,4vw,48px);margin-top:12px">What is virtual staging?</h1>
    <p class="lead">Virtual staging is the digital furnishing of a listing photo — adding realistic designer furniture and decor to an empty or dated room so buyers scrolling online can instantly picture themselves living there. This guide covers how it works, what it costs, whether it's allowed on the MLS, and how it stacks up against physical staging.</p>
  </div>
</section>

<section class="wrap" style="padding-top:24px">
  <div class="prose">
    <div class="ba" style="grid-template-columns:1fr 1fr">
      <figure style="position:relative;margin:0"><img src="assets/projects/living-before.jpg" alt="An empty living room before virtual staging" style="width:100%;aspect-ratio:1.5;object-fit:cover"><figcaption style="position:absolute;left:14px;top:14px;font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:#fff;background:rgba(20,18,16,.62);padding:5px 11px">Before · empty</figcaption></figure>
      <figure style="position:relative;margin:0"><img src="assets/projects/living-after.jpg" alt="The same living room after virtual staging" style="width:100%;aspect-ratio:1.5;object-fit:cover"><figcaption style="position:absolute;left:14px;top:14px;font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:#fff;background:rgba(20,18,16,.62);padding:5px 11px">After · virtually staged</figcaption></figure>
    </div>

    <div class="toc">
      <p class="micro">In this guide</p>
      <a href="#how">How virtual staging works</a>
      <a href="#cost">How much virtual staging costs</a>
      <a href="#mls">Is virtual staging allowed on the MLS?</a>
      <a href="#vs">Virtual vs. physical staging</a>
      <a href="#worth">Is virtual staging worth it?</a>
    </div>

    <h2 id="how">How virtual staging works</h2>
    <p>Virtual staging happens in photo-editing software, not in the home. You send photos of the empty or dated rooms, a designer selects and places furniture, rugs, art and lighting to match the space and the buyer, and you get back a realistic, high-resolution image ready for the MLS. Good virtual staging is done by a real interior designer — not a one-click AI filter — which is why the furniture sits correctly in the perspective and light of the actual room.</p>
    <p>Typical turnaround is 24 to 48 hours, and because it's digital, the same room can be restaged in a completely different style for a different buyer without any extra shoots.</p>

    <h2 id="cost">How much does virtual staging cost?</h2>
    <p>Professional virtual staging generally runs <strong>$30 to $75 per photo</strong>. Bella starts at $45 a photo with volume discounts, so a typical eight-photo listing is around $324 to $360. Compare that to physical staging, which commonly costs $2,000 to $5,000 or more for a whole home over a couple of months — virtual staging delivers the same "buyers can picture it" effect for a tiny fraction of the cost.</p>

    <h2 id="mls">Is virtual staging allowed on the MLS?</h2>
    <p>Yes. Virtually staged photos are permitted on the MLS in most markets, on one condition: they must be <strong>clearly disclosed as virtually staged</strong>. You can add furniture and decor, but you shouldn't digitally hide or alter permanent defects. Rules vary by board and state (for example, some require specific disclosure language), so confirm the exact wording with your local real estate board. Bella builds every image to MLS specifications and tells you what to note.</p>

    <h2 id="vs">Virtual staging vs. physical staging</h2>
    <p>Physical staging brings real rented furniture into the home; virtual staging adds it to the photo. Physical staging is experienced in person at showings, but it's expensive, slow to set up, and locked to one style. Virtual staging is dramatically cheaper and faster, can be restyled per buyer, and works everywhere the listing appears online — but the home is still empty when a buyer walks through. Many sellers use virtual staging for the online listing (where most buyers form their first impression) and reserve physical staging, if any, for key in-person showings.</p>

    <h2 id="worth">Is virtual staging worth it?</h2>
    <p>For empty, dated or awkward rooms, it's one of the highest-return marketing moves on a listing. The vast majority of buyers start their search online, where the photos <em>are</em> the property, and most buyers' agents say staging makes a home easier to visualize and sell. When a single stronger set of photos can mean faster showings and better offers, the per-photo cost pays for itself quickly.</p>
  </div>
</section>

<section class="wrap"><div class="prose"><div class="head"><p class="micro">Questions</p><h2 style="margin-top:8px">Virtual staging FAQ</h2></div>{faq_html(faq)}</div></section>

<section class="cta">
  <div class="cta-in">
    <h2>See your own room staged.</h2>
    <p>Read the theory — now see it on your listing. Get your first room virtually staged, or send one photo and see it staged free.</p>
    <div class="row">
      <a class="btn btn-wht" href="bella-service-virtual-staging.html">Virtual staging service</a>
      <a class="btn btn-ghost" style="border-color:#4a4640;color:#fff" href="bella-free-stage.html">Stage one room free</a>
    </div>
    <p class="fine">From $45 a photo · MLS-ready in 24–48 hours · by real designers</p>
  </div>
</section>
"""
    (ROOT/fname).write_text(doc(title,desc,slug,schema,body)); print("wrote",fname)

guide_what_is()

# ===== 5. AI VS PROFESSIONAL (comparison / conversion) =====
def ai_vs_pro():
    slug="ai-vs-professional-virtual-staging"; fname="bella-ai-vs-professional-virtual-staging.html"
    title="AI Virtual Staging vs. Professional: Which Is Better for Listings? | Bella Virtual"
    desc="AI virtual staging software vs. professional done-for-you staging: a side-by-side comparison of quality, cost, speed and MLS-readiness — and when free AI staging apps fall short on real listings."
    faq=[("Is AI virtual staging any good?","AI virtual staging has improved fast and is fine for a quick concept or a personal mock-up. For a live MLS listing, though, AI still commonly produces warped furniture, impossible perspectives, melted windows and lighting that doesn't match the room — details buyers and agents notice. For listings that represent a real home, professional or designer-reviewed staging is safer."),
         ("How much does AI virtual staging cost vs professional?","Free and low-cost AI staging apps run from $0 to about $15–$30 per image or a monthly subscription, but you do the work and quality-check every result. Professional done-for-you staging like Bella is about $45 a photo, includes a real designer and unlimited revisions, and returns MLS-ready files without you touching software."),
         ("Can I use free AI virtual staging for my MLS listing?","You can, but be careful: free AI staging often adds unrealistic furniture and can accidentally alter the room, which can violate MLS disclosure rules. If you use it, disclose it as virtually staged and review every image closely. A professional service removes that risk."),
         ("What's the difference between AI staging and a virtual staging service?","AI staging is software you operate yourself — you upload, prompt, and pick from generated results. A virtual staging service is done for you by interior designers who stage each photo to your market and buyer, quality-check it, and revise it until it's right. One is a tool; the other is a finished result."),
         ("Should real estate agents use AI or professional virtual staging?","For anything a client will see, most agents are better served by a professional service: the images are consistent, realistic and MLS-ready, and your name is on the listing. AI tools are useful for fast internal concepts, but the stakes on a real listing usually justify done-for-you.")]
    schema={"@context":"https://schema.org","@graph":[
        {"@type":"Article","headline":"AI Virtual Staging vs. Professional: Which Is Better for Listings?",
         "description":desc,"author":{"@type":"Organization","name":"Bella Virtual Staging"},
         "publisher":{"@type":"Organization","name":"Bella Virtual Staging","url":"https://www.bellavirtual.com/"},
         "mainEntityOfPage":f"https://www.bellavirtual.com/{slug}"},
        crumb_schema([("Bella Virtual","https://www.bellavirtual.com/"),
                      ("Resources","https://www.bellavirtual.com/resources"),
                      ("AI vs professional virtual staging",f"https://www.bellavirtual.com/{slug}")]),
        faq_schema(faq)]}
    rows=[
      ("Who does the work","You — upload, prompt, and pick from AI results","A real interior designer, done for you"),
      ("Realism on real rooms","Can warp furniture, windows &amp; perspective","Furniture sits correctly in the room's light &amp; scale"),
      ("Style match to buyer","Generic; hard to control","Matched to your market and buyer"),
      ("Revisions","Re-generate and hope","Unlimited revisions by a human, free for 2 weeks"),
      ("MLS-ready &amp; disclosure","Your responsibility to check","Built to MLS specs, with disclosure guidance"),
      ("Cost","$0–$30 / image or subscription","$45 / photo, no subscription"),
      ("Your time","You operate the software","Upload and approve — that's it"),
      ("Best for","Fast internal concepts &amp; mock-ups","Live listings a client will see")]
    rows_html="".join(f'<tr><td>{a}</td><td>{b}</td><td class="col-pro">{c}</td></tr>' for a,b,c in rows)
    body=f"""
<nav class="crumb"><a href="bella-homepage-redesign.html">Home</a> · <a href="bella-resources.html">Resources</a> · AI vs professional virtual staging</nav>

<section class="wrap" style="padding-bottom:0">
  <div class="prose">
    <p class="micro">Comparison</p>
    <h1 style="font-size:clamp(30px,4vw,48px);margin-top:12px">AI virtual staging vs. professional staging</h1>
    <p class="lead">AI virtual staging software is fast, cheap and everywhere — so is it good enough for a real listing? Here's an honest side-by-side of AI staging apps versus a professional, done-for-you virtual staging service, so you can pick the right tool for what's actually at stake.</p>
  </div>
</section>

<section class="wrap" style="padding-top:28px">
  <div class="prose">
    <div class="cmp-wrap">
      <table class="cmp">
        <thead><tr><th></th><th>Free / DIY AI staging</th><th class="col-pro">Professional service (Bella)</th></tr></thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>

    <h2>Where AI virtual staging shines</h2>
    <p>AI staging tools are genuinely useful. If you want to test a furniture layout, show a seller a rough idea, or stage a personal project in minutes for little or no money, a good AI app does the job. The technology has improved quickly, and for low-stakes, internal concepts it's often all you need.</p>

    <h2>Where AI falls short on real listings</h2>
    <p>The trouble starts when the photo represents a real home a buyer will tour. AI still routinely produces furniture that floats or warps, chairs with too many legs, windows that melt into walls, and lighting that doesn't match the actual room. On a listing thumbnail those tells are subtle; opened full-screen by a serious buyer or a sharp-eyed agent, they undermine trust — and if the AI quietly alters a permanent feature, you can run into MLS disclosure problems.</p>

    <h2>Why a professional service wins for listings</h2>
    <p>A done-for-you service replaces the software with a person. A real interior designer stages each photo to your market and buyer, checks that every piece sits correctly in the room's perspective and light, and revises it until it's right — then hands you MLS-ready files with disclosure guidance. You don't operate anything or quality-check a dozen generations; you upload, and you approve. For a listing with your name on it, that's usually worth far more than the per-photo cost.</p>
    <p>Bella's virtual staging is $45 a photo, done by real designers, with unlimited revisions — the finished result, not a tool you have to run.</p>
  </div>
</section>

<section class="wrap"><div class="prose"><div class="head"><p class="micro">Questions</p><h2 style="margin-top:8px">AI vs professional staging FAQ</h2></div>{faq_html(faq)}</div></section>

<section class="cta">
  <div class="cta-in">
    <h2>Skip the software. Get it done right.</h2>
    <p>Let a real designer stage your listing — MLS-ready in 24–48 hours. Or send one photo and see a room staged free first.</p>
    <div class="row">
      <a class="btn btn-wht" href="bella-order-page.html">Get started</a>
      <a class="btn btn-ghost" style="border-color:#4a4640;color:#fff" href="bella-free-stage.html">Stage one room free</a>
    </div>
    <p class="fine">$45 a photo · real interior designers · unlimited revisions</p>
  </div>
</section>
"""
    (ROOT/fname).write_text(doc(title,desc,slug,schema,body)); print("wrote",fname)

ai_vs_pro()

# ===== 6. VIRTUAL LAND STAGING (new service — vacant-lot overlay) =====
def land_staging_page():
    slug="virtual-land-staging"; fname="bella-service-virtual-land-staging.html"
    title="Virtual Land Staging | See the Home Your Lot Could Hold | Bella Virtual"
    desc="Virtual land staging overlays a finished home onto your vacant lot photo so buyers see the potential. Choose from a library of home designs, no blueprints needed, MLS-ready fast."
    service_type="Virtual land staging"
    faq=[("What is virtual land staging?","Virtual land staging digitally places a finished home onto a photo of a vacant lot, so buyers can picture what the land could become instead of looking at empty grass. You choose a home from a library of designs and a Bella designer composites it realistically into your listing photo."),
         ("How is it different from 3D rendering?","3D rendering builds a custom, photorealistic model of a specific home from architectural blueprints, quoted per project. Virtual land staging needs no blueprints and no custom modeling: you pick a home from our library and we overlay it onto your lot photo. It is faster and far more affordable, priced per photo like virtual staging."),
         ("Do I need blueprints or plans?","No. That is the whole point. Send a clear photo of the vacant lot, pick a home style from the library, and we handle the rest. If you do have a specific design in mind, that is a job for 3D rendering instead."),
         ("How much does virtual land staging cost?","It is priced per lot photo, like virtual staging (from $45 per photo), with volume discounts. There is no subscription and no per-project quote."),
         ("Can I use virtual land staging on the MLS?","Yes, with disclosure. The image shows a <em>possible</em> home, not an existing or approved structure, so it must be clearly labeled as a conceptual illustration of the lot's potential. We build every image to that standard and tell you exactly what to note; confirm wording with your local board.")]
    schema={"@context":"https://schema.org","@graph":[
        {"@type":"Service","@id":f"https://www.bellavirtual.com/{slug}#service","serviceType":service_type,
         "name":"Virtual Land Staging","description":desc,
         "provider":{"@type":"Organization","name":"Bella Virtual Staging","url":"https://www.bellavirtual.com/"},
         "areaServed":["US","CA"],"offers":{"@type":"Offer","priceCurrency":"USD","price":"45","availability":"https://schema.org/InStock"}},
        crumb_schema([("Bella Virtual","https://www.bellavirtual.com/"),
                      ("Services","https://www.bellavirtual.com/services"),
                      (service_type,f"https://www.bellavirtual.com/{slug}")]),
        faq_schema(faq)]}
    rel="".join(f'<a href="{u}">{n}</a>' for n,u in SIBLINGS if u!=fname)
    # HOUSE LIBRARY uses the exterior renders as stand-ins. PLACEHOLDER: swap for a real
    # vacant-lot before/after + a proper home library once those assets exist.
    homes=[("assets/render/ext-villa-2.jpg","Modern two-storey"),
           ("assets/render/ext-villa-1.jpg","Contemporary"),
           ("assets/render/ext-villa-3.jpg","Farmhouse")]
    homes_html="".join(f'<figure><img src="{i}" alt="{n} home design from the Bella library, shown on a lot"><figcaption>{n}</figcaption></figure>' for i,n in homes)
    body=f"""
<nav class="crumb"><a href="bella-homepage-redesign.html">Home</a> · <a href="bella-services.html">Services</a> · {service_type}</nav>

<section class="hero">
  <div class="hero-in">
    <div class="copy">
      <p class="micro">Virtual land staging</p>
      <h1>See the home your <em>lot could hold.</em></h1>
      <p>Vacant land is hard to sell because buyers can't picture the potential. Virtual land staging overlays a finished home onto your lot photo — pick a design from our library, no blueprints needed — so buyers see a future, not just grass.</p>
      <div class="row">
        <a class="btn" href="bella-order-page.html">Get started</a>
        <a class="btn btn-ghost" href="bella-service-3d-rendering.html">Need a custom design?</a>
      </div>
      <div class="cred">
        <svg viewBox="0 0 24 24"><path d="M12 3.5l2.6 5.3 5.9.9-4.3 4.1 1 5.8-5.2-2.7-5.2 2.7 1-5.8-4.3-4.1 5.9-.9z"/></svg>
        <span><b>4.9</b> on Google · composited by real designers, never one-click AI</span>
      </div>
    </div>
    <div class="shot">
      <img src="assets/render/ext-villa-2.jpg" alt="A home shown on a vacant lot with virtual land staging" fetchpriority="high">
      <span class="lbl">A home shown on a client's lot</span>
    </div>
  </div>
</section>

<div class="strip"><div>Pick from a <b>home library</b></div><div><b>No blueprints</b> needed</div><div>From <b>$45</b> / lot photo</div><div>Back in <b>24–48 hrs</b></div></div>

<section class="wrap">
  <div class="def">
    <p class="micro">What it is</p>
    <h2 style="font-size:clamp(25px,2.9vw,38px);margin:10px 0 18px">What is virtual land staging?</h2>
    <p>Virtual land staging digitally places a finished home onto a photo of a vacant lot, so buyers can picture what the land could become instead of staring at empty grass and trees. Land is one of the hardest things to sell precisely because buyers can't visualize the potential — this shows them.</p>
    <p>It's different from 3D rendering: there are no blueprints and no custom modelling. You choose a home from our library of designs and a designer composites it realistically into your listing photo — faster and far more affordable, priced per photo like virtual staging.</p>
  </div>
</section>

<section class="wrap" style="padding-top:0">
  <div class="head"><p class="micro">How it works</p><h2>Grass to dream home in three steps.</h2></div>
  <div class="steps">
    <div class="step"><div class="n">Step 1</div><h3>Send your lot photo</h3><p>A clear, straight-on photo of the vacant lot — a phone photo is fine. Tell us the buyer and budget if you know them.</p></div>
    <div class="step"><div class="n">Step 2</div><h3>Pick a home from the library</h3><p>Choose the style and size that fits the lot and the buyer — modern, farmhouse, craftsman and more.</p></div>
    <div class="step"><div class="n">Step 3</div><h3>We composite it</h3><p>A designer places the home into your photo with realistic scale, light and landscaping. MLS-ready in 24–48 hours.</p></div>
  </div>
</section>

<section class="proof">
  <div class="wrap">
    <div class="head"><p class="micro">The home library</p><h2>Choose a home that fits the lot.</h2><p>Dozens of styles and sizes — matched to your buyer and price point. No two lots are sold the same way.</p></div>
    <div class="ba" style="grid-template-columns:repeat(3,1fr)">{homes_html}</div>
  </div>
</section>

<section class="wrap">
  <div class="head"><p class="micro">Pricing</p><h2>Priced per lot photo. No project quote.</h2></div>
  <div class="price-wrap">
    <div class="price-card feat">
      <h3>Virtual land staging</h3>
      <div class="amt">$45<small> / lot photo</small></div>
      <span style="font-size:13px;color:#A9A49A">Volume discounts up to 20% off</span>
      <ul><li>Pick a home from our design library</li><li>Composited by a real designer</li><li>Realistic scale, light &amp; landscaping</li><li>MLS-ready in 24–48 hours, free revisions</li></ul>
      <a class="btn btn-wht" href="bella-order-page.html">Get started</a>
    </div>
    <div class="price-card">
      <h3>Have a specific design?</h3>
      <div class="amt" style="font-size:30px">3D rendering</div>
      <span style="font-size:13px;color:var(--faint)">Custom, from blueprints</span>
      <ul><li>Photoreal model of your exact home</li><li>Built from architectural drawings</li><li>Quoted per project</li><li>For pre-construction &amp; developments</li></ul>
      <a class="btn btn-ghost" href="bella-service-3d-rendering.html">See 3D rendering</a>
    </div>
  </div>
</section>

<section class="related">
  <div class="wrap"><p class="micro">More visualization services</p>
    <h2 style="font-size:clamp(24px,2.7vw,34px);margin-top:10px;max-width:24ch">One studio for the whole listing.</h2>
    <div class="related-row">{rel}</div>
  </div>
</section>

<section class="wrap">
  <div class="head"><p class="micro">Questions</p><h2>Virtual land staging FAQ</h2></div>
  {faq_html(faq)}
</section>

<section class="cta">
  <div class="cta-in">
    <h2>Show buyers what your lot could become.</h2>
    <p>Send a photo of the vacant land, pick a home, and get an MLS-ready image that sells the potential — back in 24 to 48 hours.</p>
    <div class="row">
      <a class="btn btn-wht" href="bella-order-page.html">Get started</a>
      <a class="btn btn-ghost" style="border-color:#4a4640;color:#fff" href="bella-how-to-sell-vacant-land.html">How to sell vacant land</a>
    </div>
    <p class="fine">From $45 a lot photo · pick from a home library · no blueprints needed</p>
  </div>
</section>
"""
    (ROOT/fname).write_text(doc(title,desc,slug,schema,body)); print("wrote",fname)

land_staging_page()

# ===== 7. HOW TO SELL VACANT LAND (guide — captures the real demand) =====
def guide_sell_land():
    slug="how-to-sell-vacant-land"; fname="bella-how-to-sell-vacant-land.html"
    title="How to Sell Vacant Land Faster | Guide for Agents & Owners | Bella Virtual"
    desc="How to sell vacant land faster: price it right, give buyers the facts they need, and — the part most sellers miss — help them picture the home the lot could hold."
    faq=[("How do I sell vacant land faster?","Price it against real comparable land sales, give buyers the facts they can't see (zoning, utilities, access, soil/survey), use clear wide photos, and help them visualize the potential — vacant land staging that overlays a possible home on the lot consistently makes a bare parcel feel like a future address."),
         ("Why is vacant land so hard to sell?","Because there's nothing to picture. Buyers walk a home and imagine living there; on raw land they see grass and uncertainty. Removing that uncertainty — with facts and a visual of what could be built — is what moves land."),
         ("Do I need a realtor to sell land?","Not necessarily, but land has quirks (zoning, utilities, financing, disclosures) that an agent experienced in land handles well. Whether you list with an agent or by owner, strong marketing and visualization matter more for land than for houses."),
         ("How do I make vacant land more appealing to buyers?","Clean sightlines and mark the boundaries, share a survey and utility/zoning info up front, add a simple site or floor plan if you can, and use virtual land staging to show a finished home on the lot so buyers see the potential instead of a blank field.")]
    schema={"@context":"https://schema.org","@graph":[
        {"@type":"Article","headline":"How to Sell Vacant Land Faster","description":desc,
         "author":{"@type":"Organization","name":"Bella Virtual Staging"},
         "publisher":{"@type":"Organization","name":"Bella Virtual Staging","url":"https://www.bellavirtual.com/"},
         "mainEntityOfPage":f"https://www.bellavirtual.com/{slug}"},
        crumb_schema([("Bella Virtual","https://www.bellavirtual.com/"),
                      ("Resources","https://www.bellavirtual.com/resources"),
                      ("How to sell vacant land",f"https://www.bellavirtual.com/{slug}")]),
        faq_schema(faq)]}
    body=f"""
<nav class="crumb"><a href="bella-homepage-redesign.html">Home</a> · <a href="bella-resources.html">Resources</a> · How to sell vacant land</nav>

<section class="wrap" style="padding-bottom:0">
  <div class="prose">
    <p class="micro">Guide</p>
    <h1 style="font-size:clamp(30px,4vw,48px);margin-top:12px">How to sell vacant land faster</h1>
    <p class="lead">Vacant land is one of the hardest things to sell — not because it's undesirable, but because buyers can't picture it. A house sells the feeling of living there; a bare lot sells grass and uncertainty. Close that gap and land moves. Here's how.</p>
  </div>
</section>

<section class="wrap" style="padding-top:28px">
  <div class="prose">
    <h2>1. Price it against real land comps</h2>
    <p>Land is priced on comparable <em>land</em> sales — lot size, zoning, location, and what's actually buildable — not on nearby house prices. Overpricing is the number-one reason a parcel sits. Pull recent sold lots in the area and price to the market, not to hope.</p>

    <h2>2. Give buyers the facts they can't see</h2>
    <p>On a house, buyers can see what they're getting. On land, they're buying questions. Answer them up front and you remove the friction that stalls a sale:</p>
    <ul>
      <li>Zoning and permitted uses</li>
      <li>Utilities — power, water, sewer/septic, gas, internet</li>
      <li>Road access and easements</li>
      <li>A survey, plat, or boundary markers</li>
      <li>Soil / perc test if it's for building</li>
    </ul>

    <h2>3. Show the boundaries and the sightlines</h2>
    <p>Mark the corners, mow a path, and shoot wide, level photos (drone shots help). A buyer who can see exactly what they'd own is far closer to an offer than one squinting at an ambiguous field.</p>

    <h2>4. Help them picture what could be built</h2>
    <p>This is the step most land listings skip, and it's the one that changes everything. Buyers commit to a <em>vision</em>, and on raw land you have to give them one. <strong>Virtual land staging</strong> overlays a finished home onto your lot photo — you pick a design from a library, and a designer composites it in realistically — so the listing shows a future address instead of an empty lot. It's the same reason virtually staged rooms sell homes: people buy what they can imagine living in.</p>
    <p>It's fast and inexpensive (priced per photo, no blueprints required), and every image is disclosed as a conceptual illustration of the lot's potential.</p>

    <h2>5. Market it where land buyers actually look</h2>
    <p>Beyond the MLS, land sells on land-specific portals and to a local audience of builders and developers. Lead with the visual — a lot photo with a home on it stops the scroll where a photo of grass never will.</p>
  </div>
</section>

<section class="wrap"><div class="prose"><div class="head"><p class="micro">Questions</p><h2 style="margin-top:8px">Selling vacant land — FAQ</h2></div>{faq_html(faq)}</div></section>

<section class="cta">
  <div class="cta-in">
    <h2>Sell the potential, not the grass.</h2>
    <p>Show buyers the home your lot could hold. Virtual land staging, from $45 a photo, MLS-ready in 24–48 hours.</p>
    <div class="row">
      <a class="btn btn-wht" href="bella-service-virtual-land-staging.html">Virtual land staging</a>
      <a class="btn btn-ghost" style="border-color:#4a4640;color:#fff" href="bella-order-page.html">Get started</a>
    </div>
    <p class="fine">Pick from a home library · no blueprints · disclosed as a conceptual illustration</p>
  </div>
</section>
"""
    (ROOT/fname).write_text(doc(title,desc,slug,schema,body)); print("wrote",fname)

guide_sell_land()
print("ALL DONE")

