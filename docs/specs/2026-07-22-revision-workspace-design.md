# Bella Revision & Annotation Workspace — design

**Date:** 2026-07-22
**Status:** Approved (design), building v1
**Part of:** the Bella client-portal system (client dashboard + revision workspace + internal CMS). This spec covers **piece 1 — the revision/collaboration workspace**, chosen as the first build because on-image revision requests are the core pain point and the hub the other surfaces wrap around.

## Problem

Clients receive delivered staged photos and need to request changes. The reference tool (delivery.bellavirtualstaging.com) only offers a plain per-photo text box ("Anything you'd like changed…") plus an optional image attachment. Requests are **disconnected from where on the image** the client means, there is no pointing/drawing, no per-spot threading, no roles/status, and no clean way to relay the request to the design studio. Result: ambiguous instructions and scattered back-and-forth.

## Goal

A workspace where a client can **point at the exact spot, sketch what they mean, and explain it**, thread the discussion, and let Bella relay a clean brief to the external studio and push the revised photo back — all with visible status.

## Scope (v1)

In: single project's revision round; pin + draw + note annotations; threaded requests; role-switcher (Agent / Realtor guest / Bella PM); statuses; studio relay packet (export); mock "push revised version"; entry point from `bella-project.html`.

Out (later pieces / not now): real auth & multi-user sync; the multi-project client dashboard; the internal CMS queue; the studio as a live in-thread participant (v1 relays to studio **externally** via an exported packet); email/SMS notifications (simulated).

## Surface

New self-contained page `bella-review.html` (static HTML + vanilla JS, single Jost font per project convention). `bella-project.html` "Photos" tab gains a **Request revisions** button that opens it.

## Roles (mock "View as…" switcher)

- **Agent** — owns the project. Creates pins + sketches + notes; replies; approves photos/project; invites a realtor guest (simulated).
- **Realtor guest** — invited by the agent. View + add pins/comments/replies. Cannot approve or change status.
- **Bella PM** — sees all requests across photos; sets per-request status; bundles a round; **Send to studio** (generate packet); **push revised version** back; marks "Ready to review."

Switching role changes which actions are visible/enabled and relabels the primary button. No real permissions — it is a demo lens.

## Layout — three panes

1. **Top bar** — project name + address, order #, project status badge, round counter, and the **View as** role switcher. Primary action button varies by role (Agent: "Submit requests"; PM: "Send to studio" / "Push revised version").
2. **Left rail** — list of delivered photos. Each item badges open-request count and per-photo status (e.g. "2 requests", "revised ✓", "approved").
3. **Center stage** — the selected photo:
   - **Original ↔ Current** before/after slider; **version selector** (v1, v2…) when rounds exist.
   - **Annotation layer** (canvas over the image): click drops a numbered pin. Toolbar: **Pin · Draw (arrow / circle / freehand) · color · undo · clear**. A sketch belongs to the active pin. Coordinates stored in **percent** so marks scale with the image.
   - Zoom.
4. **Right rail — thread** — one card per numbered request: note, author + role, timestamp, sketch thumbnail, replies, **status chip**. Click card ↔ highlights pin; click pin ↔ scrolls to card. Add-comment / reply box.

## Workflow / statuses

- **Per request:** Open → Sent to studio → Revised → Approved (or Reopened).
- **Per project:** Delivered → Revisions requested → With studio → Ready to review → Approved.
- **Round counter** (Round 1, 2…) tied to the "unlimited revisions / 2 weeks" the project page advertises.

## Studio relay packet

Bella PM action **Send to studio** compiles one downloadable/printable brief:
- Project + address + order #, round #.
- Each photo **with annotations baked in** (pins + sketches rendered onto the image via canvas export).
- A **numbered instruction list** of the written notes (photo → pin # → note text, author).
- Original + current file references.

Same export pattern as the brochure/QR features. This is the "easy way to relay" — one artifact, not scattered email.

## Push revised version

Bella PM **uploads a revised photo** (mock, FileReader) as a new version; the before/after slider then compares Original / v1 / v2; affected requests flip to "Revised"; project → "Ready to review"; client is prompted to Approve or Reopen.

## Data model (in-JS, persisted to localStorage)

```
project { id, address, order, status, round, collaborators[], photos[] }
photo   { id, label, originalURL, versions:[{v, url}], pins[] }
pin     { id, n, xPct, yPct, drawing:[strokes], note, author, role, ts, status, replies:[{author,role,text,ts}] }
```

State persisted under a `localStorage` key so a live demo survives refresh; a **Reset demo** control clears it and reseeds sample data (2–3 sample pins pre-placed to show the concept).

## Connections to later pieces

- Client **dashboard** (piece 2): project tiles open this workspace.
- Bella **CMS** (piece 3): PM's multi-project revision queue opens this same workspace.
- Existing `bella-project.html`: "Photos" tab → **Request revisions** entry point.

## Fidelity / limits

Static mockup: no backend, no real auth or multi-user sync; role-switcher and invites are simulated; drawings are canvas paths in % coords; uses the existing delivered photo set. Deployed to the `bella-preview` GitHub Pages repo alongside the other mockups (noindex).
