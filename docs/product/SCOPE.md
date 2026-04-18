# Kusse Folio — Product Scope

**Locked:** 2026-04-18

---

## Required core pages

These five pages define the **minimum valid Kusse Folio product**. Every build
ships with them. They must pass all functional and readiness checks.

| Page | Route pattern | App |
|---|---|---|
| Home | `/` | `pages` |
| About | `/about/` | `pages` |
| Projects | `/projects/` | `projects` |
| Contact | `/contact/` | `contact` |
| Privacy | `/privacy/` | `pages` |

---

## Optional modules

These are **not part of the core product**. A buyer may enable them post-purchase.
They are off by default and must not appear in nav, readiness checks, or buyer
onboarding as if they are required.

| Module | Notes |
|---|---|
| Blog | Posts / writing surface |
| Resume / CV | Structured credentials page |
| Research / Publications | Academic or professional publications |
| Services | Service offering page |

---

## Nav rule

Optional module links **must not appear in the primary or footer navigation
unless that module is explicitly enabled** for the build.

The nav should reflect only what is live and intentional. A buyer who has not
enabled Blog should see no Blog link.

---

## Readiness rule

`check_content_readiness` (and the corresponding admin Launch Readiness panel)
must only surface checks for optional modules when those modules are enabled.

A build with Blog disabled should pass readiness with zero Blog-related
warnings or blockers. Readiness is scoped to core pages only by default.

---

## Naming

In all product language, docs, and buyer-facing copy:

- Use **Blog**, not Writing
- This applies to nav labels, admin labels, docs, spec pages, and buyer guides
- The internal URL namespace (`blog`) and app name can stay as-is pending an
  explicit renaming decision; this is a product-language lock, not a code rename

---

## Current implementation state (as of v1.1.0)

Blog is implemented as an optional module with the following properties:

| Property | Value |
|---|---|
| `SiteSettings.blog_enabled` | `BooleanField(default=False)` — off for all new builds |
| Nav/footer guard | Blog link only renders when `blog_enabled=True` |
| Nav/footer label | **Blog** (not Writing) |
| URL route | `/writing/` (internal URL namespace: `blog`) |
| Demo seed | `blog_enabled=True` — Blog is shown in demo mode |

The route path (`/writing/`) does not yet match the product label (`Blog`). This
is intentional for this release. Renaming the URL is deferred to a future release
to keep route changes isolated and backwards-compatible.

---

## Previous mismatch notes (resolved in v1.1.0)

The following mismatches existed before v1.1.0 and were corrected during the
v1.1.0 scope alignment pass.

### 1. Blog was hardcoded as always-on in nav — **resolved**

`header.html` and `footer.html` now wrap the Blog link in
`{% if site_settings.blog_enabled %}`. Blog is hidden by default on all new builds.

### 2. Nav label said "Writing", not "Blog" — **resolved**

Both header and footer now display **Blog** as the visible label.

### 3. No enable/disable mechanism existed — **resolved**

`SiteSettings.blog_enabled` (`BooleanField(default=False)`) was added in
migration `core.0016`. Demo seed sets it to `True` so demo builds show Blog.

### 4. `check_content_readiness` does not check Blog content — **intentionally aligned**

The readiness command has never included Blog-specific checks. Now that Blog is
optional and gated, this omission is intentional and correct. If Blog checks are
added in future, they must be guarded by `blog_enabled`.


### 5. No scope documentation existed before this note

There was no formal product-scope document in the repo. `docs/product/DOCTRINE.md`
covers values, not surface area. This file (`SCOPE.md`) is the first explicit
statement of what is required vs optional.

---

## Remaining next adjustments

Items 1–3 from the original list were completed in v1.1.0. What remains:

**1. Align the Blog URL route from `/writing/` to `/blog/`**  
Deferred deliberately. The URL path does not match the product label. A future
release should rename the route and update any hardcoded references or redirects.
No code change is requested here.

**2. Add Blog checks to `check_content_readiness` when Blog is enabled**  
If future releases add Blog-specific readiness checks (e.g. "no published posts"),
guard them behind `{% if site_settings.blog_enabled %}` / `if site.blog_enabled`.
Currently there are no Blog checks to add.

**3. Update buyer docs to distinguish required core from optional modules**  
`docs/admin/` and any buyer-facing README sections should explicitly call out
which pages are always present and which require an enable step in admin.

