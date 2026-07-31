# Bella Virtual — SEO keyword map & page plan

Source: DataForSEO (Google, United States, en), pulled 2026-07. Metrics per keyword: **Vol** = monthly US searches · **KD** = keyword difficulty 0–100 (lower = easier) · **CPC** = advertiser cost-per-click (a proxy for commercial value) · **Intent** = dominant search intent.

## How keywords were chosen
Bella is a **done-for-you service**, so the money is in **commercial-intent** terms ("services", "company", "for realtors", "real estate 3d rendering") rather than DIY terms ("software", "app", "free" — those are people trying to do it themselves). We target commercial terms on service pages, and use one comparison page to *convert* the large DIY/AI audience into done-for-you buyers.

---

## The virtual-staging cluster (core money)

| Keyword | Vol | KD | CPC | Intent | Target page |
|---|---|---|---|---|---|
| virtual staging | 4,400 | 45 | $12.05 | info | Homepage + staging page (long game) |
| virtual staging real estate / for realtors / real estate virtual staging | 1,900 | 32–35 | $17.42 | info→comm | **Staging service page** (primary) |
| virtual staging ai | 3,600 | 30 | $10.05 | commercial | **AI-vs-professional page** (convert) |
| best virtual staging software | 1,000 | 32 | $14.13 | commercial | AI-vs-professional page |
| virtual staging software | 880 | 22 | $17.58 | commercial | AI-vs-professional page |
| free virtual staging | 720 | 19 | $4.88 | info | **Free-stage funnel page** |
| **virtual staging services** | 720 | 29 | $17.71 | **commercial** | **Staging service page** (best value: LOW comp) |
| ai virtual staging | 480 | 47 | $10.47 | commercial | AI-vs-professional page |
| virtual staging company / companies | 390 | 32–34 | $15.79 | **commercial** | Staging page + homepage |
| virtual staging app | 260 | 26 | $9.90 | info | AI-vs-professional page |
| best virtual staging for real estate | 210 | 25 | $24.27 | commercial | AI-vs-professional page |
| virtual staging bedroom | 170 | 19 | $5.25 | info | Guide / lookbook (room-type) |
| virtual staging photos | 110 | 23 | $13.37 | info | Staging page |
| what is virtual staging | 110 | **6** | $3.91 | info | **What-is guide** (easy win) |
| virtual staging furniture | 110 | 49 | $10.10 | info | Staging page (hard, skip pushing) |
| virtual staging cost | 70 | low | $7.88 | info | **Pricing page** |
| how much does virtual staging cost | 50 | low | $7.65 | info | Pricing page |
| what is virtual staging in real estate | 50 | **1** | $4.21 | info | What-is guide (trivial win) |
| virtual staging near me | 50 | 26 | $9.92 | commercial | Location pages |
| 3d / 360 virtual staging | 50 each | **3** | — | info | Staging page (niche) |

## Adjacent services (net-new capture — pages didn't exist)

| Keyword | Vol | KD | CPC | Intent | Target page |
|---|---|---|---|---|---|
| 3d rendering services | 1,300 | 43 | $34.81 | commercial | **3D rendering page** |
| architectural rendering services | 590 | **9** | $32.48 | commercial | 3D rendering page (easy + high value) |
| 3d architectural rendering | 880 | 38 | $23.70 | info | 3D rendering page |
| real estate 3d rendering / 3d rendering real estate / for real estate | 140 | **0** | $36.09 | commercial | 3D rendering page (easy + highest CPC) |
| exterior rendering | 170 | **0** | $18.29 | info | 3D rendering page |
| 2d floor plan | 1,300 | **7** | $6.22 | info | **Floor plans page** (easy win) |
| 3d floor plan | 1,300 | 34 | $4.91 | info | Floor plans page |
| real estate floor plans | 320 | 31 | $9.16 | info | Floor plans page |
| floor plan services | 70 | **0** | $13.37 | commercial | Floor plans page |
| photo editing for real estate | 720 | 19 | $11.86 | commercial | **Photo editing page** |
| real estate photo editing | 720 | 43 | $11.86 | info | Photo editing page |
| real estate photo editing services | 260 | 16 | $13.84 | commercial | Photo editing page (easy) |
| virtual twilight | 110 | **0** | $6.72 | info | Photo editing page |
| day to dusk / day to dusk photo editing | 60 | low | — | info | Photo editing page |
| virtual tour real estate | 480 | 18 | $13.12 | commercial | **3D-tour page** (exists) |
| 3d virtual tour | 390 | 39 | $6.70 | info | 3D-tour page |
| 360 virtual tour real estate | 140 | 36 | $6.05 | info | 3D-tour page |
| matterport virtual staging | 50 | — | $18.52 | navig | 3D-tour page |
| virtual renovation / remodel | 90 each | 22–25 | $6.95 | mixed | (optional renovation page / order flow) |
| commercial virtual staging | 10 | **0** | $36.09 | commercial | Staging page section (high CPC, low vol) |

## Broader / top-of-funnel (support, not primary)
| Keyword | Vol | KD | Intent | Note |
|---|---|---|---|---|
| real estate photography | 14,800 | 38 | commercial | Too broad/adjacent; don't chase |
| real estate marketing | 2,400 | 19 | commercial | Resources section (built) |
| home staging near me | 2,400 | 15 | commercial | Physical-staging seekers → "virtual vs traditional" angle in guide |

---

## Page plan (what maps where)

### Optimize (already live)
1. **Staging service page** (`bella-service-virtual-staging.html`) → title/H1/copy for *virtual staging services* + *company* + *for realtors*; keep FAQ+Service schema.
2. **Homepage** → *virtual staging* + *real estate virtual staging*; add Organization + Service JSON-LD.
3. **Pricing** (`bella-pricing.html`) → *virtual staging cost* / *how much does virtual staging cost*; add cost FAQ + FAQPage schema.
4. **Free-stage funnel** (`bella-free-stage.html`) → *free virtual staging*.
5. **3D-tour** (`bella-service-3d-tour.html`) → *virtual tour real estate* / *3d virtual tour* / *matterport*.

### Build (new)
6. **3D rendering** (`bella-service-3d-rendering.html`) — fills existing broken link on the services hub.
7. **Floor plans** (`bella-service-floor-plans.html`) — fills broken link; *2d floor plan* (KD 7) is the anchor.
8. **Photo editing** (`bella-service-photo-editing.html`) — fills broken link; folds in day-to-dusk / virtual twilight.
9. **What is virtual staging** (`bella-what-is-virtual-staging.html`) — KD 1–6 guide, top-of-funnel, routes to service + order.
10. **AI vs professional virtual staging** (`bella-ai-vs-professional-virtual-staging.html`) — captures the ~6,000/mo AI/software/free audience and converts the "AI looks fake on my listing" segment to done-for-you.

## On-page rules applied to every page
- One primary keyword in `<title>` (≤60 chars), `<h1>`, first 100 words, and `<meta description>`.
- Descriptive `<canonical>`, Open Graph, breadcrumb.
- JSON-LD: Service (service pages) / Article (guides) + FAQPage + BreadcrumbList.
- Internal links: every service page links up to /services and across to sibling services; guides link down to the service + order.
- Image `alt` text describes the room/service (not "image1.jpg").

## Placeholders to confirm before go-live
- **Star rating**: pages say "4.9 on Google." We did **not** add `AggregateRating` schema — Google requires it to reflect real, on-site reviews. Add the schema only once real reviews exist, or Google may issue a manual action.
- **NAR stats** (82% / 97%): confirm against the latest NAR Profile of Home Staging / Home Buyers & Sellers before publishing.
- **Prices**: floor plans $24/floor, photo editing from $6/photo, staging $45/photo — confirm these match live backend pricing.

---

## Virtual Land Staging (new service, added 2026-07) — a naming/positioning note, not a keyword play

Overlays a home (chosen from a library) onto a vacant-lot photo. **The service term has no search demand:** "virtual land staging", "land staging", "vacant land staging", "lot staging", "land visualization" and ~a dozen variants all return **0 indexed volume** — the category isn't named in buyers' heads. So we named it for **clarity + brand halo** (it's *virtual staging* for land), not for a keyword.

Traffic comes from the **demand that does exist**, on the seller side — captured by the `bella-how-to-sell-vacant-land.html` guide, which presents land staging as the solution:

| Keyword | Vol | KD | CPC | Intent | Target |
|---|---|---|---|---|---|
| sell my land | 480 | **6** | $53.80 | transactional | Sell-vacant-land guide |
| how to sell land | 260 | — | $18.18 | info | Guide |
| vacant lot for sale | 880 | 13 | $1.30 | transactional | Guide (context) |
| selling vacant land | 90 | — | $32.81 | transactional | Guide |
| how to sell vacant land | 40 | — | $12.55 | info | Guide |

**Pages:** `bella-service-virtual-land-staging.html` (service, conversion) ← `bella-how-to-sell-vacant-land.html` (guide, ranks) → order flow.
**Distinct from 3D rendering:** library overlay + no blueprints + per-lot-photo pricing, vs custom model from blueprints + per-project quote. Cross-linked both ways.
**Build/asset needs:** a curated **home library** (exterior designs to pick from — like the furniture lookbook), a **house-picker step** in the order flow, and **disclosure** on every image as a conceptual illustration of the lot's potential (not an existing/approved structure). Price to confirm (currently mirrors staging, $45/lot photo).
