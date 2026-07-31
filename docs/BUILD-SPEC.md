# Bella Virtual — Build Specification (Developer Hand-off)

**Purpose:** replatform `bellavirtual.com` off Shopify onto a custom stack, using the finished
design mockups in this repo as the visual + UX spec. This doc tells a developer exactly what to
build, in what order, with which stack.

**Building it?** Follow [DEV-RUNBOOK.md](DEV-RUNBOOK.md) — the ordered, step-by-step build & launch playbook (Phase 0 scaffold → Phase 1 marketing site + Payload CMS → Phase 2 app). This spec is the reference it points into.

**How to use this:** the mockups are static, self-contained HTML/CSS/vanilla-JS files — they are the
**design + interaction spec**, not the production code. Treat every screen below as "build this, wired
to a real backend." The design, copy, flows, and edge cases are already resolved, which is where these
projects normally bleed time and money.

---

## 0. Assets you're getting

| Asset | Location |
|---|---|
| Mockups (all pages) | this repo — GitHub `youngiethekim/bella-preview`, live at `https://youngiethekim.github.io/bella-preview/` |
| 301 redirect map (Shopify → new) | `migration/bella-redirect-map.csv` (198 rows) + `migration/README-redirects.md` |
| Furniture catalog (styled room sets) | `assets/lookbook/` — 298 SKU-named tiles; parsed by `scripts/catalog_data.py`, which drives both `bella-lookbook.html` (client) and `bella-catalog-db.html` (ops) |
| Furniture catalog (individual items) | `bella-catalog/` — 219 items + `manifest.json` (`{f,r,s}` = furniture/room/style) |
| Image/asset library | `assets/` (hero before/after, exterior renders, project before/after pairs, hero transform video) |
| This spec | `docs/BUILD-SPEC.md` |

---

## 1. What Bella is (context)

Bella Virtual Staging is a real-estate **visualization & marketing studio**: real interior designers
digitally stage listing photos (and offer 3D renders, floor plans, virtually-staged 3D tours, day-to-dusk
& photo edits, plus a free marketing kit). Core promise: MLS-ready in 24–48h, unlimited revisions for 2
weeks, at a fraction of physical-staging cost. Customers are real-estate agents, home builders/developers,
brokerages, and real-estate photographers. Work is fulfilled by an **external studio/contractor network**,
relayed by Bella.

---

## 2. Scope — three products, not one "website"

1. **Marketing site** (public, content/SEO) — easy 80%. Static pages + blog.
2. **The app** (authenticated) — order → fulfillment → delivery → revision → download workflow. The hard 20% that's 80% of the work.
3. **AI concierge** — a non-intrusive chat agent (RAG + live-pricing tools) embedded on the marketing site.

Build them in that order. The marketing site can launch first and take orders via Stripe while the app is built.

---

## 3. Recommended stack

| Layer | Recommendation | Notes |
|---|---|---|
| Marketing site | Static (astro/11ty or the existing HTML) on **Cloudflare Pages**, **or** WordPress if non-devs must edit the blog | Redirect map assumes clean WP-style URLs |
| App front end | **Next.js** (React) | Reuse the mockups' HTML/CSS as components |
| Auth + DB + storage | **Supabase** (Postgres + Auth + Storage + Row-Level Security) | Or Postgres + Auth0 + S3/R2 |
| Payments | **Stripe** (Checkout / Payment Links / Customer Portal; webhooks) | NOT Shopify's product/cart model — this is a service |
| Transactional email | **Resend** or **Postmark** | Order confirmations, revision notifications, secure upload links |
| File uploads (large) | Supabase Storage / S3 / Cloudflare R2 + direct/presigned uploads | Client photos, blueprints (PDF/CAD), deliverables |
| Hosting (app) | **Vercel** (Next.js), subdomain `app.bellavirtual.com` | |
| AI concierge | **Claude API** (Messages + tool use) + vector store (Supabase pgvector) | See §9 |

Environments: `production`, `staging`, `preview` (per-PR). Secrets in env vars, never in the repo.

---

## 4. Design system (match exactly — it's deliberate)

- **Font:** single family **Jost** (300/400/500) everywhere. This is an intentional choice — do NOT add a second font.
- **Tokens (CSS variables):**
  `--bg:#FDFCFA` · `--ink:#232120` · `--soft:#6E6A66` · `--faint:#9C978F` · `--line:#E8E4DE` · `--line-2:#F0EDE8` · `--dark:#1C1A18` · `--green:#3E6B4C` · `--gold:#E7C36A` (marketing) / `#B8985A` (some app UI) · `--red:#C4553F` · `--amber:#B5892F`
- **Status colors** (project board): Client review = red, In revision = amber/yellow, Complete = green.
- **Buttons:** dark ink pill, uppercase, hover → green. Primary CTA label is **"Get started"** sitewide → order flow.
- **Header (all marketing pages):** `BELLA · Services · Pricing · Lookbook · Resources · [Get started]`. Logo → home.
- **Footer (all marketing pages):** identical — Services · Virtual staging · 3D tours · Pricing · Lookbook · Resources · Get started + copyright.
- Respect `prefers-reduced-motion`; theme-agnostic; mobile-responsive (nav links collapse < 760px — **add a real mobile menu**, current mockups just hide them).

---

## 5. Part A — Marketing site

### 5.1 Pages (each mockup = one page)
| Page | Mockup | URL |
|---|---|---|
| Homepage | `bella-homepage-redesign.html` (=`index.html`) | `/` |
| Services hub | `bella-services.html` | `/services` |
| Virtual staging | `bella-service-virtual-staging.html` | `/virtual-staging` |
| Virtual land staging (vacant-lot overlay) | `bella-service-virtual-land-staging.html` | `/virtual-land-staging` |
| How to sell vacant land (guide) | `bella-how-to-sell-vacant-land.html` | `/how-to-sell-vacant-land` |
| Virtually staged 3D tours | `bella-service-3d-tour.html` | `/3d-tour` |
| 3D rendering, Floor plans, Photo editing | **TO BUILD** (clone the service template) | `/3d-rendering`, `/floor-plans`, `/photo-editing` |
| Pricing | `bella-pricing.html` | `/pricing` |
| Lookbook (298-set furniture catalog) | `bella-lookbook.html` + `assets/lookbook/` | `/lookbook` |
| Catalog database (internal — sets per brand/style) | `bella-catalog-db.html` | `/admin` view, not public |
| Resources hub (+ real-estate-marketing SEO section) | `bella-resources.html` | `/resources` |
| Phone photo guide | `bella-guide-photos.html` | `/resources/photo-guide` |
| Style quiz | `bella-style-quiz.html` | `/style-quiz` |
| Location pages (~18) | `bella-virtual-staging-los-angeles.html` (template) | `/virtual-staging-<city>` |
| Segment pages | `bella-for-{agents,builders,brokerages,photographers}.html` | `/for-agents` etc. |
| Blog (140 posts) | migrate from Shopify | `/blog`, `/blog/<slug>` |

### 5.2 SEO / migration requirements (do not skip)
- Preserve titles, meta descriptions, H1s, and **JSON-LD schema** already present in the mockups (`Service`, `FAQPage`, `BreadcrumbList`, `CollectionPage`).
- Import `migration/bella-redirect-map.csv` as **301s** (one hop, no chains). See `migration/README-redirects.md`.
- **Cross-check the redirect map against Google Search Console + Ahrefs** for orphaned URLs that still rank/have backlinks — the sitemap-derived map won't include those.
- Decide the `/zh/` Chinese locale: keep (hreflang) or 301 to English (map has a wildcard for the latter).
- Location pages must be **substantively differentiated** from service pages (local market data, neighborhoods, local case studies) to avoid duplicate-content penalties.
- Generate a fresh XML sitemap; resubmit in GSC; keep Shopify live ~30 days as fallback.

### 5.3 Blog / CMS
140 posts to migrate. If non-technical staff must publish → WordPress (or a headless CMS: Sanity/Contentful/Payload). Keep clean `/blog/<slug>` URLs.

---

## 6. Part B — The app (the real build)

### 6.1 Roles & auth
- **Client / Agent** — places orders, reviews & approves photos, requests revisions, downloads, manages brand.
- **Guest** (agent's client) — view + comment only (invited to a project).
- **Bella admin / PM** — internal ops (CMS): manage all orders, assign studios, relay revisions.
- **Studio contractor** — scoped fulfillment portal (no client identity/pricing).
Use Supabase Auth (email magic-link + password). Row-Level Security by role + project membership.

### 6.2 Data model (core entities)
- **users** (id, email, name, role, phone, headshot, brand_logo, brand_bio)
- **contractors** (id, name, specialties[]) — the studio network
- **orders** (id, user_id, project_type[empty|occupied|dated|prebuild], commercial bool, services JSON, photo_count, package, subtotal, discount, total, stripe_payment_intent, status)
- **projects** (id, order_id, user_id, address, agent_name, slug `<addr>-bella-virtual`, folder_name, status, contractor_id, revision_round)
- **photos** (id, project_id, index, original_url, staged_url, status[delivered→client-review | inrevision | approved], style_key, watermark bool)
- **change_requests** (id, photo_id, x%, y%, note, drawing JSON[strokes], sent bool, verdict[fixed|unfixed|null], unmet_reason)
- **messages** (id, project_id or photo_id, author_role[client|studio|system], author_name, text, created_at) — the revision conversation thread
- **studio_jobs** (id, project_id, contractor_id, status[assigned|in_progress|changes|qa|done], production_brief JSON)
- **files / uploads** (id, project_id, kind[listing_photo|blueprint|reference|deliverable|360], url, uploaded_by)
- **marketing_assets** (id, project_id, kind[brochure|website|flyer|before_after|furniture|lead_capture], template[modern|editorial|bold], config JSON)
- **leads** (id, project_id, name, email, phone, source[qr|nfc], created_at) — open-house lead capture
- **catalog_items** (from `bella-catalog/manifest.json`) — furniture used / shop-the-look
- **credits / transactions** (optional billing wallet) — see `bella-billing.html`
- **style_presets** (6 styles: modern, scandi, coastal, midcentury, farmhouse, contemporary)

### 6.3 Core workflow (state machine)
`Order placed + paid` → `Project created` → `Studio assigned (production brief)` → `Studio delivers` →
**Client review** → (a) `Mark as done` → **Complete** ; or (b) `Request revisions` (annotations sent) →
**In revision (with studio)** → studio re-delivers → back to **Client review** → … → **Complete** →
**Download** (clean if approved; watermarked preview otherwise) → **Marketing kit**.
Notifications fire at each hand-off (email + in-app).

### 6.4 Screen-by-screen (each maps to a mockup)
| Screen | Mockup | Key behavior to build |
|---|---|---|
| **Order flow** (3-step wizard) | `bella-order-page.html` | Project type → photo count (stepper drives numbered upload boxes) → per-photo style modal (6 styles + specific templates + room + notes) → extras (renovation/day-to-dusk/sky/floor plans/360 tour/3D renders) with **volume pricing** (3+/6+/11+/21+ = 5/10/15/20% off; renders discount as a bundle) → per-photo service targeting (pick which photos get reno/dusk/sky) → "Most popular" default = 8 photos → live cart total → Step 3 package summary + project details + requirements/upload panel + free marketing kit opt-out + furniture-sourcing opt-in → **Stripe checkout**. Style can be pre-selected via `?style=<key>` from the quiz. Not-ready path emails a secure upload link to photographer/marketing manager. |
| **Client dashboard** | `bella-dashboard.html` | Projects grid + status chips, revision round-trip loop, profile/brand onboarding (logo/headshot/bio feed the marketing kit), New order CTA, activity feed, team/guests. |
| **Project workspace** | `bella-project.html` | Editable title + slug/folder naming; **Photos = drag-and-drop kanban** (Client review → In revision → Complete) with progress summary, bounded-scroll lanes, collapsible columns, game-like FLIP/confetti motion; **inline mark-up modal** (pin/draw/note using a **Benjamin Moore paint palette**) → send changes / mark done; **revision conversation thread** (client ⇄ studio, "sent to studio", email-reply framing); **watermarked downloads** (un-approved = light "PREVIEW" watermark, approved = clean original — see §6.7); **Furniture-used** tab (real furniture photos + `<model-viewer>` 3D viewer + shop-the-look); **Marketing materials** tab (brochure / website / open-house flyer / before-after / furniture guide / lead-capture, each with **Modern/Editorial/Bold** template picker + live QR + brand). |
| **Revision workspace** (team/internal) | `bella-review.html` | Full annotation tool: pin (%-coords), SVG draw (arrow/circle/freehand, `preserveAspectRatio=none`), threaded per-request replies, roles, per-request + per-project status, PM "Studio brief" printable packet, Original↔Staged compare slider, version bar. |
| **Internal CMS / ops** | `bella-cms.html` | Cross-client order queue, KPI filters, assign-to-studio, colour-coded SLA, "revisions to relay", advance status. |
| **Studio portal** | `bella-studio.html` | Gated, scoped (no client identity/pricing). Per-job **production brief** (services, per-photo shot list w/ each room's style, buyer/direction, source files w/ "waiting" state), work pane, version board, start→in-progress→QA, contractor network (`?studio=`). |
| **Login** | `bella-login.html` | Real auth (Supabase). |
| **Billing** (optional) | `bella-billing.html` | Prepaid credit wallet, top-up packs, plan toggle, Stripe. |

### 6.5 Payments (Stripe)
- Per-order Checkout with dynamic line items from the cart (staging × qty w/ volume discount, floor plans/floor, renders, add-ons). NOT products/cart.
- Volume-discount + bundle logic must match the mockup's `lines()` pricing exactly (single source of truth = backend; the AI concierge & order flow both read it).
- Webhooks: on `payment_intent.succeeded` → create project, assign studio, email confirmation.
- Optional: credit wallet + Customer Portal.

### 6.6 File uploads & storage
- Client listing photos, blueprints/plans (PDF, DWG, DXF, JPG, PNG), 360° equirectangular, reference images, deliverables.
- Direct/presigned uploads to Storage; large files; virus scan; "send later / email a secure upload link" flow (tokenized link, no login).

### 6.7 Downloads & watermarking (specific requirement)
- **Un-approved** photos (Client review / In revision) download as a **lightly watermarked preview** (tiled diagonal "BELLA VIRTUAL · PREVIEW").
- **Approved** photos download **clean/original**.
- Mockup does this client-side via canvas (works because Bella's CDN sends permissive CORS); production should watermark **server-side** for reliability/security. Keep the separate `state.wm` "Virtually staged" **MLS-compliance label** toggle as its own feature.

### 6.8 Marketing kit generation
From delivered photos + brand: **listing brochure, one-listing website, open-house flyer, before/after "see the potential", shop-the-look furniture guide, and an open-house QR/NFC lead-capture** landing page (captures leads → `leads`). Brochure & website each have **Modern/Editorial/Bold** templates. Export brochures/flyers as **print-ready PDF**; publish the one-listing site under the agent's brand at `listings.bellavirtual.com/<slug>`.

---

## 7. Part C — AI concierge (marketing site)
Non-intrusive chat widget (mockup in the homepage footer, `#baLaunch`/`.ba-panel`). Build as:
- **Claude API** (Messages + tool use) with a system prompt = Bella brand voice + guardrails ("answer only from Bella content; never invent pricing; escalate when unsure").
- **RAG:** index FAQ/service pages/blog/policies into a vector store (Supabase pgvector); retrieve + ground answers.
- **Tools:** `get_pricing()` (live, from the same backend as checkout), `recommend_service()`, `start_order(prefill)`, `handoff_to_human()`.
- **"Gets smarter" = a feedback loop**, not auto-learning: auto-sync KB on content changes, log conversations, review gaps weekly, add answers. Live data stays current via tools.
- UI: launcher bubble, no auto-popup, no page overlay, dismissible.

---

## 8. Integrations / third-party
Stripe · Supabase (auth/db/storage) · Resend/Postmark (email) · Claude API + pgvector (concierge) ·
`<model-viewer>` (3D furniture) · Matterport/Kuula/iGuide (staged 3D tour embed/host) · QR generation ·
Google (reviews 4.9, Search Console) · optional Cloudflare (CDN/redirects/images).

---

## 9. Non-functional requirements
- **Security:** RLS on every table; presigned uploads; Stripe webhooks verified; no secrets client-side.
- **Compliance:** MLS-ready output + virtual-staging **disclosure** (e.g. AB 723) — keep the "Virtually staged" labeling feature; tell agents what to disclose.
- **Performance:** static/CDN marketing site; image optimization (WebP); lazy-load.
- **Accessibility:** keyboard/focus, `prefers-reduced-motion`, alt text, color contrast.
- **Mobile:** real nav menu (mockups only hide links < 760px).

---

## 10. Content/data the CLIENT must supply or confirm (flagged placeholders)
The mockups intentionally flag invented data — **replace before launch**:
- **Confirm real pricing** for every service (staging $45/photo, floor plans $24/$84 per floor, dusk $7, sky $6, renders $630/$840, tour, commercial rates — several are PLACEHOLDER).
- **Confirm stats:** "97% of buyers start online" & "82% staging helps visualize" (NAR — confirm current figures); "$285M+ / thousands of listings" hero stats; SOLD/days-on-market case-study numbers are SAMPLE.
- **Real testimonials/logos** only (real ones on hand: 4.9 Google; Beverly Bahm; Highland Homes/Caleigh Wells; "These are perfect, thank you!").
- **Real images** where stock/placeholder is used (some Unsplash, some AI-generated).
- Real furniture-brand data for shop-the-look; commercial before/after; the "Rove Concepts" catalog images.

---

## 11. Suggested phases & milestones
- **Phase 0 — Launch marketing site (days):** deploy static site to Cloudflare Pages, DNS, import redirects, Stripe Payment Link + intake form for orders. Business runs on new site; fulfillment manual.
- **Phase 1 — Real order + delivery (weeks):** Next.js order flow wired to Stripe + Supabase; project created on payment; client uploads; staged-photo delivery; watermarked vs clean downloads; email notifications.
- **Phase 2 — Review + dashboard:** kanban project workspace, annotation/revision workflow, conversation thread, client dashboard, guest invites.
- **Phase 3 — Internal ops:** CMS order queue + studio portal (production brief, contractor network) — removes the manual relay bottleneck.
- **Phase 4 — Marketing kit + AI concierge + billing/credits.**

---

## 12. Open decisions for the client (get answers before Phase 1)
1. `/zh/` Chinese locale — keep or drop?
2. Staged 3D tours — do we **host** the finished tour, or hand back files? (copy currently says hosted/embeddable)
3. Billing — pay-per-order, prepaid credits, or subscription plans? (mockup has a credit wallet)
4. ~~WordPress for the blog, or headless/static?~~ **DECIDED: Payload CMS (headless, inside the Next.js app). See §13.**
5. Which studio contractors are in the network, and how do they receive/return work?
6. Real pricing + stats + testimonials (see §10).

---

## 13. Content & pricing management (CMS)

**Editors are non-technical** (founder / marketing team). They must be able to change prices, service copy, testimonials, FAQs, and blog posts without a developer, and without anything falling out of sync.

### 13.1 Single source of truth for pricing (do this first)
Prices are currently **hardcoded across ~12 static pages** (staging $45/photo, floor plans $24/floor, photo editing $6/photo, day-to-dusk $7/photo, plus volume-discount tiers) and duplicated in the order calculator and FAQs. In production:

- Store every price in **one `pricing` table / CMS collection** (service, unit, base price, volume-discount tiers, active flag).
- **Everything reads from it:** the order calculator, every marketing page that prints a price, the pricing page, and FAQ answers. Marketing pages read at build/ISR time; the app reads live.
- **Map each price to a Stripe Price object** (store the Stripe price ID on the row) so a change updates the site *and* checkout together. Prefer editing in the CMS and syncing to Stripe (webhook or a small admin action), so there's one place to change a number.
- Keep the FAQ "how much does virtual staging cost?" answer and the JSON-LD `Offer`/price driven from the same source so structured data never drifts from displayed price.

Net effect: change $45 → $49 in one field → homepage, service pages, pricing page, order calculator, Stripe, and schema all update.

### 13.2 CMS — DECIDED: Payload CMS
**Client has chosen Payload CMS.** Self-host it inside the Next.js app on the same Postgres/Supabase DB — one codebase, one admin login, one database. Editors get a polished dashboard for prices, copy, testimonials, FAQs, blog, and images; the app and marketing pages read the same data. No second system to secure or keep in sync.

Editing model the client expects (set expectations with them): Payload is **structured content editing**, not a visual drag-and-drop builder like Elementor. Editors change text, prices, images, blog posts, and add/reorder testimonials/FAQs via forms — not free-form layout. To get a page-builder *feel* within brand guardrails, implement a **Payload Blocks** library of on-brand sections (hero, feature grid, testimonial band, CTA, image+text) that editors can add/remove/reorder to compose pages, and enable **Live Preview** so they see changes rendered. Layout/style changes beyond the block library stay with the developer (by design — keeps the site on-brand and unbreakable).

Rejected: WordPress/Elementor and Webflow — both are separate systems from the app, so pricing would live in two places and drift; Payload keeps one source of truth.

### 13.3 What belongs in the CMS vs the app DB
- **CMS-managed (editors touch):** prices & discount tiers, service page copy, testimonials, FAQs, blog posts, homepage hero/section copy, images, city-page content.
- **App DB (system-managed):** orders, projects, photos, revisions, messages, users, studio jobs, credits/invoices. Not editor-facing content.

### 13.4 Launch sequencing with live revenue
The current Shopify store is generating revenue; **do not risk a big-bang cutover.** Reconciles with §11:

- **Phase 1 — marketing site + CMS live, checkout untouched.** Ship the Next.js marketing pages + Payload CMS + single pricing source, import the 301 redirects (`migration/bella-redirect-map.csv`). Keep taking orders through the **existing Shopify checkout or a Stripe Payment Link + intake form**. SEO/brand/new pages go live in weeks; editors start managing prices/content immediately; revenue never stops.
- **Phase 2 — the app.** Build and prove the authenticated order → dashboard → studio → billing flow (§11 Phases 1–4). When ready, repoint the "Get started" CTAs from the interim checkout to the new order flow and retire Shopify. Pricing already lives in the CMS, so the order calculator reads the same numbers with no rework.
