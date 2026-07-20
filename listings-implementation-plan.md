# Listings Feature — Implementation Plan (MVP)

## Context

`site/listings.html` is currently a static "Coming Soon" placeholder. The site is a plain static HTML/CSS/JS build assembled by `site/build.py`, hosted on GitHub Pages — no server, no database.

Decision reached: use **Sanity** as a headless CMS, fetched **client-side** (browser calls Sanity's public read-only CDN API directly — no rebuild step, no server). Admin maintenance happens in **Sanity Studio** (Sanity's free, open-source admin UI), deployed under a branded custom subdomain (e.g. `admin.amberconsultants.in`) via DNS CNAME. No custom dashboard code, no write-token backend — this keeps the public site 100% static.

This is a small enough feature that MVP and near-final product are almost the same thing — the plan below ships a complete, usable listings page in one pass, but keeps the schema and code structured so filters, detail pages, and pagination can be added later without a rewrite (see "Deferred / Not in MVP").

## Status

**Done — fully live:**
- `site/js/listings.js` — fetches listings from Sanity's public CDN API and renders cards, with loading/empty/error states.
- `site/pages/listings.html` — fragment updated with a toggleable grid + loading + empty-state markup (this is the *source* fragment; `site/listings.html` is generated from it by `build.py`, not hand-edited).
- `site/css/styles.css` — `.listings-grid` / `.listing-card` styles added, matching the existing `.service-card` visual language (same radius/shadow/hover tokens).
- `site/build.py` — small addition: `render_shell()` now accepts an `extra_scripts` list so `js/listings.js` only loads on `listings.html`, not every page. (Plan originally assumed zero `build.py` changes; this one-line extension was needed.)
- `site/listings.html` regenerated via `python3 build.py` — verified the script tag and new markup landed only on the listings page, and that all files serve correctly from a local static server.
- `studio/` — a Sanity Studio v3 project: `schemas/listing.js` (full schema per below), `schemas/index.js`, `sanity.config.js`, `sanity.cli.js`, `package.json`.
- **Sanity project created and linked**: project ID `ortbv0xn`, dataset `production` (public visibility — confirmed the CDN API is anonymously readable via a live `curl` check). Logged in as `zoloinnovations@gmail.com`.
- **`projectId` filled in** in both `site/js/listings.js` and `studio/sanity.config.js`/`sanity.cli.js` (no more `REPLACE_WITH_PROJECT_ID` placeholders).
- **Studio deployed**: live at **https://amber-consultants.sanity.studio/** — confirmed reachable and schema list shows the `listing` type deployed under project `ortbv0xn`.

- **CORS origins configured** (`npx sanity cors add`) so browsers can actually call the CDN API — `http://localhost:3333` (Studio dev server, added automatically), `http://localhost:8000`, `http://localhost:5500` (common local static-server ports), and `null` (for `file://` access). Verified via direct header checks that all four now get a proper `access-control-allow-origin` response. This was the reason the sample listings weren't showing up in the browser earlier — `curl` isn't subject to CORS so my earlier tests missed it, but browser `fetch()` was being silently rejected and falling back to the empty state.

**Decided: Studio stays on the free `*.sanity.studio` URL, no custom domain.**
Turns out Sanity's built-in Studio hosting doesn't support custom domains on *any* plan — that requires self-hosting the static Studio build elsewhere (Vercel/Netlify/GitHub Pages) instead. You opted to keep the free hosted URL rather than take on that extra infra, so:
- **No CNAME needed** — don't add the `admin.amberconsultants.in` DNS record we discussed earlier, it wouldn't have worked against `*.sanity.studio` anyway.
- Studio stays at **https://amber-consultants.sanity.studio/**.

**CORS origins for production added**: `https://new.amberconsultants.in`, `https://amberconsultants.in`, and `https://www.amberconsultants.in` (bonus, in case that variant gets used) are all registered — `listings.html` will work once deployed to either domain.

**Business details centralized (`site/business.json`)**
Single source of truth for name, tagline, address, phone/landline, WhatsApp number + message, email, hours, social links, Sanity Studio URL, and the footer's "designed by" credit. `build.py` loads it at build time and:
- Injects it into the shared header/footer (`render_shell`) directly.
- Replaces `{{TOKEN}}` placeholders (`{{WHATSAPP_URL}}`, `{{PHONE}}`, `{{LANDLINE}}`, `{{EMAIL}}`, `{{ADDRESS}}`, `{{HOURS}}`, `{{MAPS_QUERY}}`) inside page fragments (`pages/contact.html`'s info cards + map embed, `pages/home.html`'s mid-page CTA) that used to hardcode these values.
- Generates `site/js/business-config.js` (a plain `window.AMBER_BUSINESS = {...}` script, not a runtime JSON fetch — works identically on `file://`, a local server, and GitHub Pages) so `listings.js` (WhatsApp number) and `main.js` (contact-form mailto) read the same values instead of their own hardcoded copies.
- **To update business details later**: edit `site/business.json`, re-run `python3 build.py`, done — everywhere it's used updates automatically.

**"Admin" link added to the header**
A small, low-key text link (`.admin-link`, styled subtly — muted color, underline, not a button) pointing at `business.json`'s `sanityStudioUrl`, in both the desktop nav-cta row and the mobile sheet.

**Pushed to GitHub**: https://github.com/karan51290/Amber-Consultants (public repo).
- Note: a repo with this name already existed from an earlier, unrelated Vite/TypeScript attempt at the site. Rather than delete it, it's archived at https://github.com/karan51290/Amber-Consultants-archived-2026-07-14 so nothing was lost, and the new static-site + Sanity codebase now lives at the `Amber-Consultants` name instead.
- `.gitignore` at the project root excludes `node_modules/`, the Obsidian vault symlink, `backup/`, `.claude/`, and Studio's build/cache dirs.

**Not done yet — needs a decision/access only you have:**
- **Inviting the client as a Studio editor** — needs their email address. Once you give me it, I can invite them via the Sanity management API, or you can do it yourself at sanity.io/manage → Project → Members → Invite.
- Replace the 3 test listings with real ones once the client is onboarded (or leave them as a working demo in the meantime).

## MVP Scope

**In scope:**
- Sanity project + `listing` schema (rich enough that Studio doesn't need a re-migration later)
- Sanity Studio deployed and reachable (at the free `*.sanity.studio` URL — see Status), client invited as an editor
- `listings.html` renders a live grid of available listings (image, title, price, address, key facts, WhatsApp CTA) fetched client-side
- Loading / empty / error states (falls back to today's "Coming Soon" messaging on fetch failure or zero listings)

**Deferred / not in MVP** (schema and code are structured to support these without rework):
- Individual listing detail pages (schema already has a `slug` field reserved for this)
- Filtering/search (by locality, price range, bedrooms) and pagination/infinite scroll
- Featured/carousel treatment on the homepage
- Map view
- Build-time pre-rendering for SEO (if listings ever need to be individually indexable by Google, this is the "approach B" rebuild we discussed and rejected for MVP — revisit later if SEO on individual listings becomes a priority)

## Schema (`studio/schemas/listing.js`)

- `title` (string, required)
- `slug` (slug, auto-generated from title) — unused by MVP UI, reserved for future detail pages
- `price` (number, required)
- `priceLabel` (string, optional — e.g. "₹85L" or "₹25,000/mo" for display flexibility vs. raw formatting)
- `locality` (string, required)
- `propertyType` (string enum: apartment / house / commercial / land)
- `bedrooms`, `bathrooms`, `areaSqft` (numbers, optional)
- `description` (text)
- `images` (array of image, required, at least 1)
- `status` (string enum: available / sold / rented — required, default "available")
- `featured` (boolean, default false) — reserved for future homepage carousel
- `publishedAt` (datetime, default now) — used for sort order

## Front-end integration (implemented)

- **`site/js/listings.js`**
  - Constants `SANITY_PROJECT_ID` / `SANITY_DATASET` (currently placeholders — see Status above).
  - `fetchListings()` — GROQ query via the CDN API endpoint, filtering `status == "available"`, ordered by `featured desc, publishedAt desc`.
  - `imageUrl(assetRef, width)` — builds a Sanity image CDN URL directly from the asset `_ref` string (no extra dereferencing query needed, since Sanity image refs already encode id/dimensions/format).
  - `renderListings(listings)` — builds card markup (image, title, priceLabel, locality, bed/bath/area, WhatsApp CTA with a pre-filled message referencing the listing title) and injects into `#listings-grid`.
  - Loading state shown immediately; on success it's replaced with cards; on empty result or fetch error, the existing "Coming Soon" empty-state markup is shown as a fallback.
- **`site/pages/listings.html`** (source fragment, regenerate with `python3 build.py`):
  - `#listings-loading`, `#listings-grid`, `#listings-empty-state` — toggled by the script above.
- **`site/build.py`**: `extra_scripts` param on `render_shell()`, wired so only `listings.html` loads `js/listings.js`.
- **`site/css/styles.css`**: `.listings-grid` / `.listing-card` rules added.

## Verification

Done so far:
- `node --check` passed on `listings.js` and all `studio/` JS files.
- `python3 build.py` regenerates `site/listings.html` cleanly; confirmed via grep that `js/listings.js` and the new markup appear only on the listings page, not the others.
- Served `site/` locally (`python3 -m http.server`) and confirmed `listings.html`, `js/listings.js`, and `css/styles.css` all return 200.

- **Test listings added** via `studio/scripts/seed-test-listings.js` (run once with `npx sanity exec scripts/seed-test-listings.js --with-user-token`), using existing photos from `site/assets/images/` as stand-in images: 2 `available` (one `featured`) + 1 `sold`.
- Confirmed end-to-end against the live dataset:
  - CDN query `*[_type == "listing" && status == "available"] | order(featured desc, publishedAt desc)` returns exactly the 2 available listings, featured one first — the sold listing is correctly excluded.
  - A card's image `_ref` correctly resolves to a working `cdn.sanity.io` image URL (200 response) via `imageUrl()` in `listings.js`.

Still to do (visual/browser checks — no browser tool available in this session):
- Open `listings.html` in an actual browser and confirm the 2 cards render visually as expected (image, title, locality, facts, price, WhatsApp CTA).
- Confirm the empty-state fallback shows correctly against a dataset with zero `available` listings.
- Throttle network in devtools to confirm the loading state displays and the page doesn't break on a slow connection.
- Check the image grid on mobile viewport widths (real estate traffic skews mobile).
- Confirm the WhatsApp CTA per card opens with the correct pre-filled listing reference.

## Future Extensions (not built now, but unblocked by this schema/structure)

- Detail pages per listing using the existing `slug` field.
- Filters/search UI reading the same `fetchListings()` data, refined with query params.
- Pagination or infinite scroll once listing volume grows.
- Homepage "featured listings" section reusing `imageUrl()`/`renderListings()` with `featured == true`.
- Revisit build-time rebuild (GitHub Actions + Sanity webhook) if individual listings need to be SEO-indexable.
