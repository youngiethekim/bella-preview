# Bella for Teams & Brokerages — Partner Program Spec

_One-page working spec. Numbers are illustrative defaults to react to, not final. Legal items flagged with ⚠ need counsel before launch._

## 1. The idea in one line
Brokerages partner with Bella and promote it to their agents. Agents order at **pooled volume pricing**; the brokerage **earns a share** of everything its agents spend. It spreads because everyone wins: the brokerage earns + looks good, the agents save.

## 2. Why it works (the double win)
The brokerage promotes it hard because they get two things, not one:
- **They earn** — a % of their agents' net spend.
- **Their agents save & look good** — pooled volume pricing every agent enjoys, plus a done-for-you marketing perk the brokerage can use to recruit.

The agent's ordering experience is unchanged; the partnership sits above it.

## 3. How it flows (end to end)
1. Brokerage signs a **partner agreement** and gets a branded **signup link + invite code**.
2. Brokerage promotes Bella to its agents.
3. Agents sign up and are **auto-attached to the brokerage** (attribution — see §6).
4. Agents order and pay as normal, at **pooled brokerage pricing**.
5. Bella pays the brokerage its **cut**, monthly, as credits (or cash for approved partners).

## 4. The cut structure (defaults to approve)
| Decision | Default | Notes |
|---|---|---|
| **Basis** | 10% of **net** agent spend (ex. tax, ex. discounts already given) | "Net" so we don't pay a cut on money we discounted away |
| **Structure** | **Tiered** by trailing-90-day team volume | Motivates the brokerage to keep pushing |
| **Payout form** | **Bella credits** by default; **cash** for approved partners ⚠ | Credits sidestep most legal/tax friction |
| **Frequency** | Monthly | Statement of agent orders + cut earned |
| **Attribution window** | Agent stays attributed to the brokerage while active on the team | Handle agent moving brokerages (re-attribute or detach) |

### Reward tiers (illustrative)
| Tier | Trailing-90-day team spend | Brokerage cut | Agent pricing |
|---|---|---|---|
| Starter | $0–2.5k | 5% | Standard volume discounts |
| Growth | $2.5k–10k | 8% | Pooled team discount |
| Partner | $10k–25k | 10% | Pooled team discount |
| Elite | $25k+ | 12% | Best pooled discount + priority turnaround |

## 5. Billing / team modes (offer 1–2 at launch)
- **Agent-pays + pooled pricing (launch default).** Each agent pays on their own card; all orders roll to one volume tier so every agent gets the team discount. Lowest ops.
- **Central billing (upgrade).** Orders bill to a brokerage house account / monthly invoice. For brokerages that fund staging as a perk.
- **Split at checkout (later).** Brokerage covers a set share (e.g. staging base), agent covers the rest.
- **Prepaid wallet/credits (later).** Brokerage buys a discounted bundle; agents draw down.

## 6. Attribution (the technical backbone)
- Every agent account carries a `brokerage_id`, set at signup via invite code / branded link, or by admin invite.
- Every order is tagged with the agent's `brokerage_id` at time of order (store it on the order, don't just join live — so a later move doesn't rewrite history).
- Brokerage cut = sum of net order value for that `brokerage_id` in the period × tier rate.
- Edge cases: agent with no brokerage (direct), agent changing brokerages, agent on two teams (pick primary).

## 7. Roles & dashboards
- **Brokerage admin:** invite/remove agents, see all listings + spend, see cut earned + credit balance, download monthly statement, manage billing mode.
- **Agent (seat):** normal ordering; sees "your brokerage rate applied."
- **Bella ops:** approve partners, set custom tiers, toggle cash payout, run monthly payouts.

## 8. Build notes
Standard multi-tenant SaaS: org + roles + org-level pricing + attributed orders + monthly rollup. On the planned **Next.js + Supabase + Stripe + Payload** stack:
- **Supabase:** `brokerages`, `memberships (agent↔brokerage, role)`, `brokerage_id` + `partner_rate_snapshot` on `orders`.
- **Stripe:** customer **credit balances** for the co-op model; **Invoicing** for central billing; **Connect** only if/when you pay cash rev-share (handles payouts + tax forms).
- **Pricing engine:** resolve an order's price from the agent's brokerage tier (pooled volume), not just their own count.
- **Payouts job:** monthly cron → per-brokerage statement + credit grant (or Connect transfer for cash).

## 9. ⚠ Legal / finance questions for counsel (before promising cash %)
1. Do real-estate **referral-fee / rebate / "thing of value"** rules (state boards in the US; RECO/BCFSA/provincial regulators in Canada) restrict paying a **brokerage** a % of its agents' vendor spend? (RESPA likely N/A — staging is marketing, not a settlement service — but confirm.)
2. **Disclosure** requirements to agents/consumers if the brokerage earns on a mandated/recommended vendor?
3. **Tax reporting** — 1099-NEC (US) / T4A (CA) on cash payouts; credits vs cash treatment.
4. Partner agreement terms: term, termination, clawback on refunds/chargebacks, non-exclusivity, brand use.
5. Sales-tax handling on discounted/credited orders.

**Recommendation:** launch with **credits-only** (§4) to avoid most of the above, add **cash tier** once counsel signs off.

## 10. Open decisions for you
- Confirm the **tier %s** and thresholds against margin.
- Credits-only at launch, or push for cash from day one (pending legal)?
- Which **billing modes** ship first (rec: agent-pays + pooled pricing).
- What's the **agent-facing** discount story (do agents see "brokerage rate," or just a lower price)?
