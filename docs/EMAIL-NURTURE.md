# Bella Virtual — "Free Room Stage" lead funnel + nurture sequence

Companion to the `bella-free-stage.html` landing page and the homepage exit-intent popup.
Audience: **real estate agents / brokers** with a live or upcoming listing.

---

## The funnel at a glance

```
Traffic ──► Trigger ─────────────► Capture ──► Deliver ──► Nurture ──► Paid order
(ads,       exit-intent popup       email +     free       3-email     $45/photo
 organic,   OR 55% scroll           1 photo     staged     sequence    full listing
 email,     OR 30s on homepage;                 room in
 socials)   OR /bella-free-stage    (2 fields)  24h
            landing page
```

**Why "stage one room free" is the magnet:** it *is* the product, it self-qualifies the lead (anyone who uploads a photo has a live listing right now), and it costs one render to win a client worth hundreds. Softer top-of-funnel entry points already built: the **style quiz** and the **phone-photo PDF guide**.

## Capture form fields (keep it to 2–3)
- Email (required)
- Name (optional)
- One room photo (optional — they can reply with it later; don't block signup on the upload)

Everything else (brokerage, listing address, phone) is asked *after* they're a lead, in the confirmation email or the order flow. More fields = fewer leads.

## Backend wiring (for the dev)
The popup and landing page currently store state locally and show a success screen. To make them real:
1. On submit, `POST { name, email, photo }` to a lead endpoint (serverless function) or straight to the email tool's subscriber API.
2. Add the subscriber to a **"Free stage leads"** group/segment, with a custom field `source = popup | landing`.
3. Trigger the automation below on "added to group."
4. Route the uploaded photo to the studio queue (or send an auto-reply asking them to reply with a photo if none was attached).
5. Tag the lead `converted` when they place a paid order, and **exit them from the nurture** so they stop getting sales emails.

Suppress the popup for anyone already subscribed or logged in (the homepage popup already uses a `localStorage` guard; the real version should also check the known-lead cookie/session).

---

## The 3-email nurture sequence

Tone: warm, concrete, agent-to-agent. Short. One clear CTA per email. Times are from signup.

### Email 1 — Deliver the value (send immediately)
**Subject:** Your free staged room is on the way 🏠
**Preview:** Send us the photo (if you haven't) and we'll have it back within 24 hours.

> Hi {{name|there}},
>
> Thanks for claiming your free staged room. Here's what happens next:
>
> **1.** Reply to this email with **one photo** of an empty or dated room (a phone photo is fine). *[If they already uploaded: "We've got your photo and our designers are on it."]*
> **2.** A real interior designer stages it to match your buyer and market.
> **3.** You get it back within **24 hours**, watermark-free and MLS-ready.
>
> No card, no catch. This is just how we show you the quality.
>
> — The Bella Virtual team
>
> *[Button: Reply with my photo]*

### Email 2 — Proof + the offer (send ~48h after Email 1)
**Subject:** What your whole listing could look like
**Preview:** A few before-and-afters, and what a full listing runs.

> Hi {{name|there}},
>
> Hope you loved your free room. Here's what a full listing looks like when every photo is staged:
>
> *[3 before/after pairs — living room, primary bedroom, kitchen]*
>
> Staged listings help buyers picture the home, and most home searches start online, so the first photo does a lot of the selling. A full listing with Bella is **$45 a photo**, paid once, with volume discounts up to 20% (a typical 8-photo listing is about **$324** — thousands less than physical staging).
>
> - 24–48 hour turnaround
> - Free unlimited revisions for two weeks
> - You approve every photo before it's final
>
> *[Button: Stage my whole listing]*

### Email 3 — Urgency + easy yes (send ~4 days after Email 2, only if not converted)
**Subject:** A little something to get your listing live
**Preview:** Your first order, on us a bit.

> Hi {{name|there}},
>
> Quick nudge, in case your listing is ready to go. Order your full listing this week and we'll take **{{OFFER — e.g. 15% off / a free day-to-dusk edit}}** off your first order.
>
> It takes about two minutes to start, and you'll have MLS-ready photos back in a day or two.
>
> *[Button: Start my order]*
>
> Not selling yet? No problem — keep your free room, and we'll be here when you are.

*After Email 3, move non-converters to a low-frequency general list (monthly tips / seasonal offers) rather than deleting them.*

---

## Metrics to watch
- **Popup:** view → submit rate (benchmark ~2–5% exit-intent; higher for scroll/landing).
- **Landing page** (`/bella-free-stage`): visit → submit rate (aim 15–30% for a warm, single-offer page).
- **Email:** open + click per email; **lead → paid-order conversion** is the number that matters.
- **Photo-upload rate** on signup (if low, lean harder on the "reply with your photo" auto-response).

## Things to confirm before launch
- The first-order incentive in Email 3 (percentage vs a free add-on).
- Whether "one free room per agent" is enforced (by email) or generous.
- Real testimonials / star rating to replace the placeholders in the trust strip.
- CAN-SPAM/CASL footer (physical address + unsubscribe) on every email.
