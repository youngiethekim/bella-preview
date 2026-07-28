# Bella Virtual — Shopify → WordPress 301 redirect map

`bella-redirect-map.csv` — 198 redirects generated from the live Shopify sitemaps
(`www.bellavirtual.com`) on 2026-07-28. Import this into your WordPress redirect
plugin **after** the destination pages are published.

## Columns
`source, target, regex, code` — the format the **Redirection** plugin (redirection.me) reads directly.

- `source` — the old Shopify path
- `target` — the new WordPress path
- `regex` — `0` for an exact match, `1` for a pattern (only the `/zh/` row uses `1`)
- `code` — `301` (permanent) for every row

## How to import
- **Redirection plugin:** Tools → Redirection → **Import/Export** → upload the CSV. Done.
- **Rank Math:** Rank Math → Redirections → Import/Export → Import CSV. Rank Math expects
  columns `sources`/`url_to`; rename the header row to match, or map on import.
- **Server-level (.htaccess/nginx):** hand this file to your dev — it's the source of truth.

## What's mapped (198 rows)
| Type | Rule |
|---|---|
| Pages (34) | `/pages/<slug>` → `/<slug>` — slug kept **verbatim** (no "improvements" — slug changes reset rankings) |
| Collections (7) | mapped to the new clean service URLs (see below) |
| Blog (141) | `/blogs/news` → `/blog`; `/blogs[/news]/<slug>` → `/blog/<slug>` |
| Products (14) | routed to the closest service page by keyword |
| Case studies (2) | `/pages/case-study/<slug>` → `/case-study/<slug>` |
| `/zh/` locale (1 wildcard) | `/zh/(.*)` → `/$1` |

Service collections → new pages:
- `/collections/virtual-staging-services` (+ `-copy`) → `/virtual-staging`
- `/collections/3d-rendering-services` → `/3d-rendering`
- `/collections/floor-plan-services` → `/floor-plans`
- `/collections/photo-editing-services` → `/photo-editing`
- `/collections/our-services` → `/services`
- `/collections/frontpage` → `/`

## ⚠️ Decisions to confirm BEFORE importing
1. **`/zh/` Chinese locale** — the wildcard row strips `/zh/` and forwards to the English page.
   That's correct **only if you're dropping the Chinese version.** If you're keeping it,
   delete that row and set up `hreflang` + real `/zh` pages instead.
2. **Product routing** — the 14 SKUs are routed to the nearest service page by keyword.
   Skim the `/products/...` rows and adjust any you'd send elsewhere.
3. **Slug preservation** — city pages keep their exact slugs (e.g. `/virtual-home-staging-san-diego`
   stays as-is). Don't rename them during the move; do it later with its own redirect if ever.
4. **Blog duplicates** — a few posts exist at both `/blogs/<slug>` and `/blogs/news/<slug>`;
   both forward to the same `/blog/<slug>`. Publish one canonical post.

## ⚠️ Not in this file — add manually
- **Cross-check against Google Search Console + Ahrefs.** The sitemap only lists *current* URLs.
  Any old/orphaned URL that still ranks or has backlinks won't be here — export those and add them.
  This is the #1 source of migration SEO loss.
- Shopify system URLs: `/cart`, `/account`, `/checkout`, `/collections/all`, `/policies/*`.
- Paginated / tag / filtered collection URLs (`?page=`, `/collections/x/tag`).
- Image/CDN URLs (`/cdn/shop/...`) — usually left alone.

## Golden rules
- **Publish the WP destination page first, then activate its redirect** (a 301 to a missing page = 404).
- **301, one hop, no chains.** Run the finished map through a redirect checker.
- After launch: crawl for 404s, resubmit the new sitemap in GSC, watch Coverage + Performance for 2–4 weeks.
