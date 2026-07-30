# Bella Virtual — Developer Runbook (build & launch, step by step)

This is the **ordered execution plan**. It turns the design mockups + [BUILD-SPEC.md](BUILD-SPEC.md) into a build.
- **Mockups** (live): https://youngiethekim.github.io/bella-preview/ — the design/UX/copy spec. Each page is a target to rebuild wired to a real backend.
- **Reference architecture, data model, page map:** [BUILD-SPEC.md](BUILD-SPEC.md). This runbook points into it; don't duplicate it.
- **Stack (decided):** Next.js (App Router) + **Payload CMS** (self-hosted, in the same app) + **Supabase** (Postgres + Storage) + **Stripe** + **Resend** (email), hosted on **Vercel**.
- **Golden rule:** ship in two phases. **Phase 1** = marketing site + CMS live while the existing Shopify checkout keeps taking orders (revenue never stops). **Phase 2** = the authenticated app, then retire Shopify.

> **Auth note (reconciles BUILD-SPEC §6.1):** use **Payload's built-in auth** as the single users/auth system (one `users` collection with a `role` field). Use **Supabase for Postgres + Storage only** — do **not** also run Supabase Auth. One auth system, one admin.

---

## Phase 0 — Foundations (get a skeleton deployed)

**Goal:** an empty Next.js + Payload app, connected to Supabase Postgres, deployed to Vercel, with the design system ported. No content yet.

### 0.1 Accounts & access (do first)
- [ ] GitHub repo created (private), team access granted. Trunk = `main`; branch per feature; PR previews on.
- [ ] **Vercel** project (hosting) — connect the repo.
- [ ] **Supabase** project (Postgres DB + Storage bucket `media`). Copy the **connection string** and the **S3-compatible Storage keys**.
- [ ] **Stripe** account (test mode first). Get test API keys.
- [ ] **Resend** (or Postmark) account for transactional email + a verified sending domain.
- [ ] **Cloudflare** (DNS for `bellavirtual.com`) — access to the DNS zone. Do NOT change DNS yet.
- [ ] Secrets live in Vercel env vars / `.env` (gitignored), never in the repo.

### 0.2 Scaffold the app
- [ ] `npx create-payload-app@latest bella` — choose the **Next.js + Postgres** template (Payload 3.x is Next-native and runs inside the App Router). Verify exact flags against current Payload docs.
- [ ] Set `DATABASE_URI` to the Supabase Postgres connection string. Configure the Postgres adapter (`@payloadcms/db-postgres`).
- [ ] Configure media storage: `@payloadcms/storage-s3` pointed at the Supabase Storage bucket (S3-compatible). (Cloudflare R2 also works.)
- [ ] Confirm `pnpm dev` boots the app **and** the Payload admin at `/admin`; create the first admin user.
- [ ] Deploy the skeleton to Vercel; confirm `/admin` loads on the Vercel URL and DB migrations run.

### 0.3 Port the design system (once, shared)
- [ ] Copy the CSS tokens verbatim from any mockup (BUILD-SPEC §4): `--bg #FDFCFA`, `--ink #232120`, `--soft`, `--faint`, `--line`, `--dark`, `--green #3E6B4C`, `--gold`. Put them in a global stylesheet / Tailwind theme.
- [ ] Load **Jost** (300/400/500) — the single brand font. Do not add a second font.
- [ ] Build shared `<Header>` and `<Footer>` React components from the mockup markup (nav: `Services · Pricing · Lookbook · Resources · [Get started]`; the standard dark footer). Add a **real mobile menu** (mockups just hide links under 760px).
- [ ] Respect `prefers-reduced-motion`.

**✅ Phase 0 done when:** the empty app + Payload admin are deployed to Vercel on the Supabase DB, and a test page renders with the brand header/footer, tokens, and Jost.

---

## Phase 1 — Marketing site + CMS live (revenue stays on Shopify)

**Goal:** every marketing page rebuilt, editable in Payload, reading prices from one source, live on the real domain, taking orders via a Stripe Payment Link — while Shopify checkout still works as fallback.

### 1.1 Build the Payload content model (collections & globals)

Create these in Payload. **`services` is the single source of truth for pricing.**

| Type | Name | Key fields | Drives |
|---|---|---|---|
| Global | `siteSettings` | brandName, logo, nav[], footer[], googleRating, phone, socialLinks, defaultOG image | Header/footer/site-wide |
| Global | `pricingRules` | currency, volume-discount tiers (count→%), rush options | Order calculator math |
| Collection | `services` | name, slug, unit (`photo`/`floor`/`project`), **basePrice**, **stripePriceId**, active, + page copy (hero H1, definition, steps[], FAQ[], images) | Service pages **and** order calculator options |
| Collection | `pages` | title, slug, SEO (title/desc/OG), **`layout` = Blocks field** | Homepage, resources, any composed page |
| Collection | `testimonials` | quote, author, role, city, photo, rating, featured | Proof sections |
| Collection | `faqs` | question, answer (rich text), category, order | FAQ sections + FAQPage JSON-LD |
| Collection | `posts` | title, slug, excerpt, body (rich text), hero, author, publishedAt, SEO, draft flag | Blog (`/blog/<slug>`) |
| Collection | `locations` | city, slug, marketData, neighborhoods[], localCaseStudies[], SEO | City pages (must be differentiated — BUILD-SPEC §5.2) |
| Collection | `media` | (Payload uploads) alt text required | All images |
| Collection | `users` | email, name, **role** (`admin`/`pm`/`studio`/`client`/`guest`), + auth | Auth for everyone (Phase 2 uses this too) |
| Collection | `leads` | name, email, phone, source (`free-stage`/`open-house`/`popup`), photo, createdAt | Lead funnel capture (BUILD-SPEC free-stage) |

- [ ] **Blocks library** for the `pages.layout` field (this is the "page-builder feel within guardrails"): `Hero`, `FeatureGrid`, `BeforeAfter`, `TestimonialBand`, `PriceStrip`, `StepList`, `CTA`, `ImageText`, `FAQAccordion`, `RichText`. Each block = the corresponding mockup section, rebuilt as a React component. Enable **Live Preview** so editors see changes rendered.
- [ ] Set Payload **access control** by `role` (public read for content collections; write for admin/pm only). Add friendly field labels + help text (non-technical editors).

**✅ Acceptance:** an editor can log into `/admin`, change a `services.basePrice`, add a testimonial, and reorder blocks on a `page` — and see it in Live Preview.

### 1.2 Single pricing source + Stripe sync (the important one)
- [ ] Every price on the site reads from `services.basePrice` + `pricingRules` tiers. **Nothing hardcoded.** Marketing pages read at build/ISR; the order calculator reads live.
- [ ] Each `services` row stores its **`stripePriceId`**. When an editor changes a price, sync to Stripe (a Payload `afterChange` hook that creates a new Stripe Price and updates the ID — Stripe prices are immutable, so create-new-and-swap).
- [ ] Drive the pricing-page numbers, the FAQ "how much…" answers, and the JSON-LD `Offer` price from the same source so displayed price, schema, and checkout never drift.
- [ ] Current values to seed (⚠️ client to confirm — BUILD-SPEC §10): staging **$45**/photo, floor plans **$24**/floor, photo editing **$6**/photo, day-to-dusk **$7**/photo, volume discounts to 20%.

**✅ Acceptance:** change staging to $49 in Payload → homepage, `/virtual-staging`, `/pricing`, the order calculator, JSON-LD, and the Stripe price all reflect $49.

### 1.3 Rebuild the marketing pages (from CMS)
Rebuild each mockup as a Next.js route reading from Payload. Page→mockup→URL map is in **BUILD-SPEC §5.1**. Includes the **new SEO pages we just built** — see [SEO-KEYWORD-MAP.md](SEO-KEYWORD-MAP.md):
- [ ] `/` homepage, `/services`, `/pricing`, `/lookbook`, `/resources`, `/style-quiz`
- [ ] Service pages: `/virtual-staging`, `/3d-rendering`, `/floor-plans`, `/photo-editing`, `/3d-tour`
- [ ] Content pages: `/what-is-virtual-staging` (guide), `/ai-vs-professional-virtual-staging` (comparison), `/resources/photo-guide`, `/free-virtual-staging` (lead funnel)
- [ ] Segment pages `/for-agents|builders|brokerages|photographers`; location pages `/virtual-staging-<city>`
- [ ] Blog `/blog` + `/blog/<slug>` (migrate 140 Shopify posts into `posts`)
- [ ] Lookbook: import `bella-catalog/manifest.json` (219 items) into `media`/a `catalogItems` collection.

### 1.4 SEO carry-over (do not skip — BUILD-SPEC §5.2)
- [ ] Preserve every `<title>`, meta description, H1, and **JSON-LD** (`Service`/`Article`/`FAQPage`/`BreadcrumbList`) already in the mockups.
- [ ] **Do NOT add `AggregateRating` schema** until real on-site reviews exist (Google penalty risk — SEO doc §placeholders).
- [ ] Generate `sitemap.xml` + `robots.txt`; canonical tags on every page.
- [ ] Trim meta descriptions to ~155 chars (the new pages run ~170; DataForSEO audit flagged truncation).

### 1.5 Redirects (BUILD-SPEC §5.2)
- [ ] Import `migration/bella-redirect-map.csv` (198 rows) as **301s** (Next.js `redirects()` / middleware / Cloudflare rules). One hop, no chains. See `migration/README-redirects.md`.
- [ ] Cross-check against **Google Search Console + Ahrefs** for ranking/backlinked URLs not in the sitemap-derived map.

### 1.6 Interim checkout (so you can launch before the app exists)
- [ ] Create a **Stripe Payment Link** (or a simple intake form → Stripe) for orders. Point the "Get started" CTAs at it **for Phase 1 only**.
- [ ] Order intake emails the client + Bella (Resend). Fulfillment stays manual this phase.
- [ ] Keep the current Shopify store **live and reachable** as a fallback during cutover.

### 1.7 Go-live (Phase 1 launch checklist)
- [ ] Full QA on staging: every page renders from CMS, mobile nav works, prices correct everywhere, forms send email, Lighthouse ≥ 90.
- [ ] Point `bellavirtual.com` DNS (Cloudflare) at Vercel. Lower TTL a day before for a fast rollback.
- [ ] 301s live and verified (spot-check 15–20 old URLs, including top blog posts).
- [ ] Submit new sitemap in GSC; keep Shopify reachable ~30 days as fallback.
- [ ] Monitor GSC coverage + 404s + Vercel logs for the first week.

**✅ Phase 1 done when:** the new marketing site is live on the real domain, the team edits content/prices in Payload, orders come in via the Stripe link, SEO is preserved, and Shopify is standby-only.

---

## Phase 2 — The app (order → delivery → revision → download)

**Goal:** replace the interim checkout with the real authenticated workflow, then retire Shopify. Build in this order; each is a shippable milestone. Full data model in **BUILD-SPEC §6.2**; screen map in **§6/§7**. Implement `orders`, `projects`, `photos`, `changeRequests`, `messages`, `studioJobs`, `contractors`, `credits` as **Payload collections** — that gives the internal ops "Control Center" (mockup `bella-cms.html`) largely for free via the Payload admin with custom views.

### 2.1 Auth & accounts
- [ ] Enable auth on the `users` collection: magic-link + password. Roles: client, guest, admin, pm, studio.
- [ ] Access control / row rules by role + project membership (a client sees only their projects; a studio sees only assigned jobs, no client identity/pricing).
- [ ] Build `bella-login.html` → real sign-in; `bella-dashboard.html` → client dashboard.

### 2.2 Real order flow (`bella-order-page.html`)
- [ ] Rebuild the 3-step wizard reading services/prices from Payload (§1.2). Per-photo service picker, volume discounts, requirements uploads (photos + blueprints PDF/CAD).
- [ ] Checkout via **Stripe Checkout** (not the Payment Link); **webhook** creates the `order` + `project` on successful payment.
- [ ] File uploads to Supabase Storage via presigned/direct upload.

### 2.3 Delivery + downloads
- [ ] Studio-delivered staged photos land in the project; client review flow.
- [ ] **Watermarked** preview downloads for un-approved photos; **clean** downloads once approved (the canvas/watermark logic is already worked out in the mockups — BUILD-SPEC §8).

### 2.4 Review & collaboration (`bella-review.html` + `bella-project.html`)
- [ ] Kanban project workspace (3 columns: Client review → In revision → Complete).
- [ ] Pin + draw + note annotations; threaded revision conversation; guest (agent's client) view+comment invites.

### 2.5 Internal ops + fulfillment (`bella-cms.html` + `bella-studio.html`)
- [ ] Ops Control Center: cross-client order queue, assign studio/contractor, relay revisions, SLA flags (Payload admin + custom views).
- [ ] Studio contractor portal: scoped production brief, upload deliverables, submit for QA. Contractor network (BUILD-SPEC §6).

### 2.6 Billing + notifications
- [ ] Billing model per client decision (pay-per-order / prepaid credits / plans — BUILD-SPEC §12.3); `bella-billing.html`.
- [ ] Transactional email (Resend): order confirmation, "staged photos ready", revision updates, secure upload links.

### 2.7 Cutover & retire Shopify
- [ ] Repoint "Get started" CTAs from the Stripe Payment Link to the real order flow.
- [ ] Soak test with a few real orders end-to-end.
- [ ] Decommission Shopify once a full billing cycle has passed cleanly.

**✅ Phase 2 done when:** a client can order + pay, upload, get staged photos, request revisions, and download — and Bella + studios manage it internally — with no dependency on Shopify.

---

## Cross-cutting (apply throughout)
- **Environments:** `production`, `staging`, per-PR previews. Migrations reviewed before prod.
- **Security:** RLS/access control by role; secrets in env vars; validate Stripe webhooks (signature); never expose service keys client-side; GDPR/CCPA-friendly lead handling.
- **Performance/a11y:** Lighthouse ≥ 90; images `next/image`; alt text required in `media`; keyboard-navigable; contrast per BUILD-SPEC §4.
- **Analytics:** privacy-friendly analytics + GSC + Stripe dashboard from day one.

## Open decisions to get from the client before Phase 1 (BUILD-SPEC §12)
1. Confirm real **prices**, **NAR stats** (82%/97%), and **testimonials** (no fabrication).
2. `/zh/` Chinese locale — keep (hreflang) or 301 to English?
3. Staged 3D tours — do we host the finished tour or hand back files?
4. Billing model — pay-per-order, prepaid credits, or plans?
5. Which studio contractors are in the network, and how do they receive/return work?
