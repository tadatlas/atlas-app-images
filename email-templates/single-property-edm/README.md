# Single Property EDM

**Purpose:** One-listing campaign email — open inspection, new listing, price revision or last chance to inspect — with an optional "Recently Sold" proof block. Sent from the listing agent to a targeted buyer segment.
**Cadence:** On request from Agent Services or the listing agent, usually 1–2 days before the inspection.
**Source file:** Built from `data/<slug>.json` by `build.py`. Chrome (head/CSS, header, OFF-MARKET ACCESS, footer) is lifted verbatim from the Weekly OFI Stripo export into `partials/`.
**Build script:** `python build.py data/<slug>.json --check` → `output/<slug>.html`
**ActiveCampaign:** paste `output/<slug>.html` into a campaign using ActiveCampaign's HTML (code) editor — the same route as the Weekly OFI. Do not use the AI/API import (`generate_campaign` / `import_campaign_design`): it rebuilds the email in designer markup and drops the mobile CSS (confirmed on the 34 Jeffreys build, campaign 717).

To make this part of the `atlas-email` skill, copy this file to `references/templates/single-property.md` and add a row to the skill's reference index.

## Structure

Top to bottom. Sections are separate `es-content` tables; nothing opens or closes across them.

| # | Block | Band | Source |
|---|---|---|---|
| 1 | Header — logo, two-line date/label block | dark `#1e1e1e` | `partials/header.html` (`{{HEADER_LINE_1}}`, `{{HEADER_LINE_2}}`) |
| 2 | Intro — eyebrow, serif headline | white | `intro()` |
| 3 | Hero — lead photo, 540px, linked | white | `hero()` |
| 4 | Details — street, suburb, specs, body copy | white | `details()` |
| 5 | Inspection panel — label, day, time · dark CTA | sand `#ebe4df` panel inside white | `inspection()` |
| 6 | Gallery — two photos, 263 / 262px | white | `gallery()` (omitted if < 2 photos) |
| 7 | Enquiries — agent name, phone, email (1 or 2 agents) | white, 60px bottom | `agents()` |
| 8 | Recently Sold — heading + one card per sale | sand `#ebe4df` | `sold()` (omitted if no items) |
| 9 | OFF-MARKET ACCESS — register CTA | navy `#283b48` | `partials/offmarket.html` |
| 10 | Footer — locations, socials, legal, ActiveCampaign footer | dark `#1e1e1e` | `partials/footer.html` |

Band order is white → sand → navy → dark. Dropping the Sold block leaves white → navy, which still reads cleanly.

## Content rules

- **Facts only from the data source.** Notion Property Marketing Database (Properties) is the source for ID, beds/baths/cars, land size, headline, agents and photos. Body copy may only state what the listing confirms — no invented views, proximity claims or features (NSW advertising rules; see `atlas-listing-descriptions` §11–12).
- **Never call a listing "new" unless it is.** Check `Listed date`.
- **"Exclusive" only for genuinely off-market or pre-market access.** A publicly listed home with a public open is "rare" or "rarely offered", not exclusive.
- Eyebrow: 1–3 words, uppercase (`FOR SALE`, `PRICE REVISION`, `LAST CHANCE TO INSPECT`, `NEW TO MARKET`).
- Headline: one idea, sentence case, no full stop, ≤ 45 characters so it holds two lines on mobile.
- Body: 2–3 short paragraphs, ≤ 70 words total. Australian English, no exclamation marks, no stacked adjectives.
- Price: shown only where the agent supplies it. Sold price line uses the agent's wording (e.g. `Contact Peter Kakos or Alicia Chen`).
- Sold block: same street or suburb, sold by the same team, within the last ~3 months. It is proof of demand, not a second listing.

## Typography and format conventions — locked to the OFI design system

| Field | Convention |
|---|---|
| Eyebrow / labels | Helvetica 11px, `letter-spacing:2px`, uppercase; labels bold |
| Headline | Times New Roman 28/34px `#1e1e1e`; mobile 26px (`es-text-mobile-size-26 es-m-lh-12`) |
| Street | Times New Roman 22px (hero listing), 18px (sold card), title case, street only |
| Suburb | Helvetica 11px uppercase + ` NSW` |
| Specs | `X BED &nbsp;Y BATH &nbsp;Z CAR`, uppercase; CAR dropped when 0/blank |
| Body | Helvetica 13/20px `#333333` |
| Day / time | `Saturday 31 October` then `9:15am – 9:45am` — en dash, lowercase am/pm, no leading zero |
| Agent | name Times 18px; phone and email Helvetica 12px, `tel:+61…` and `mailto:` links |
| CTA | `es-button-3401`: `#1e1e1e` fill, white 10px text, `letter-spacing:1.5px`, `padding:12px 28px`, nowrap. Mobile override `padding:12px 14px` in `EXTRA_CSS` |

## Links and tracking

- Listing: `https://www.atlas.com.au/property/<slug>-<id lowercase>3` — use the `Listing link` from Notion, never rebuild it.
- UTM on every Atlas link: `?utm_source=property_edm&utm_medium=email&utm_campaign=property_<street>_<suburb>_<ddmmmyyyy>&utm_content=<PropertyID>`; the off-market CTA uses `utm_content=offmarket_access`.
- Hero, gallery and CTA all point to the listing; each Sold card points to its own listing with its own ID.
- Images: Reapit URLs (`images.sales.reapit.com.au/...`) are used as supplied. AgentBox originals (`agentboxcdn.com.au/...-rsd.jpg`) are routed through the Asteroid resizer, `?nf_fm=jpg&nf_q=70&nf_w=800` (hero `nf_w=1080`) — the same conversion the Weekly OFI uses. `build.py` does this and warns if an image is outside the listing's own ID folder.

## Sending (ActiveCampaign)

- From: lead listing agent (name + `@atlas.com.au` address); reply-to the same.
- Subject ≤ ~40 characters; preview text carries the address and inspection time.
- Audience: a buyer-requirements segment matched to the price bracket, or the lead agent's primary-owner segment. Confirm with the requester every time — it is not inferable from the listing.
- Load: create the campaign with the HTML (code) editor and paste the built file. Set subject, preheader, sender and audience, send a test to yourself, check it on a phone, then send or schedule after sign-off.
- Do not load it through the AI/API import — it rebuilds the layout and strips the mobile CSS (see Known faults).

## Known faults

| Fault | Fix |
|---|---|
| Footer `PRIVACY POLICY` / `UNSUBSCRIBE` are plain text, not links (inherited from OFI chrome) | ActiveCampaign footer carries `%UNSUBSCRIBELINK%`; fix at source in Stripo |
| Header logo is white-on-transparent PNG — invisible in previews that drop images | None needed; flag only if a client blocks images |
| Inspection panel and cards stay two-up on mobile (50% columns, as in the OFI) | Keep CTA label ≤ 14 characters or it wraps |
| ActiveCampaign AI/API import (`generate_campaign` html import) rebuilds the email in designer markup: button classes, most `@media` rules and some copy blocks change (74 diff hunks on the 34 Jeffreys build) | Paste the HTML into the HTML/code editor instead |
| Image hosts (`asteroidcdn`, `reapit`, `stripocdn`) and atlas.com.au are not reachable from Claude's cloud sandbox | Links and images can't be HTTP-checked there; run `scripts/verify_email.py` without `--no-net` locally, and send a test before the live send |
