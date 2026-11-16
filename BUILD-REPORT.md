# Platinum Painting Gold Coast – Homepage Build Report

Site: https://platinum-painting-gold-coast.wsdfy.com (Atarim workspace: VentraIP)
Source design: `design/original/Home v2.dc.html` (approved). Build tooling: `build/`.

## Status legend
✅ completed & verified · ⚠️ completed with notes · ❌ failed · ⏸ not tested · 🚫 unavailable

## Summary
| Area | Status | Notes |
|---|---|---|
| Theme | ✅ | Hello Elementor parent + `platinum-painting` child theme (active). Twenty Twenty-Five left installed. |
| Header / footer | ✅ | Ultimate Addons for Elementor 2.9.7 templates "Site Header" (46) / "Site Footer" (48), display: entire site. UAE Navigation Menu + Search widgets. |
| Homepage | ✅ | Page "Home" (ID 44), set as static front page, template Elementor Full Width. 10 sections in design order. |
| Contact Form 7 | ✅ (built) / ⏸ (submission) | "Homepage Quote Form" (ID 43), recipient test@gmail.com, embedded in the Free Quote section. Submissions not tested by design. |
| Yoast SEO | ⚠️ | Title + meta description set and verified in HTML. One H1, logical H2/H3. Site is set to **Discourage search engines** (`noindex, nofollow`) – left unchanged (staging). |
| Media / performance | ⚠️ | See below. |
| Responsive | ✅ (Chromium only) | 9 viewports checked. |
| Browsers | 🚫 | Only Chromium-based rendering was available. Firefox, Safari, Edge **not tested**. |

## Sections built (design order)
Hero (H1 word reveal, quarter-circle image grid, rings, pulse hub, floating cans/card) · Offer cards (spinning badges) · Rainbow marquee · About (hover-open features, colour fan, parallax images) · Before/After drag slider · Services (6) · Why It Matters (scroll word-fill + animated Sun/Salt/Storm scenes) · Recent Projects gallery (6) · Testimonials carousel (autoplay 5.5 s, arrows, dots) · Free Quote + CF7 form.

## Elementor editability
- Home: 131 containers, 78 Heading, 23 Text Editor, 15 Button, 35 Image, 8 Icon, 5 Star Rating, 1 Icon List, **8 HTML**, **1 Shortcode**.
- All text, buttons, links, photos, icons, stars and testimonial content are native widgets and editable.
- **HTML widgets (decorative only, aria-hidden):** hero rings, hero hub/twinkle/scribble, colour fan, 3 animated weather scenes, 2 brush-stroke swooshes. Reason: animated SVG/shape artwork with no native Elementor equivalent.
- **Shortcode widget:** the CF7 form (required by CF7).
- **Custom code (child theme):** `assets/pp.css` (overlapping compositions, decorative shapes, hover effects, marquee/slider mechanics, CF7 styling, responsive tweaks); `assets/pp.js` (scroll reveals, float/spin/scene animations, marquee loop, word fill, parallax, header shadow, about hover rows, before/after slider, testimonial carousel); `functions.php` (enqueues, hero preload, CF7 autop off). Behaviour is attached via CSS classes visible in each element's Advanced › CSS Classes. Absolute positions of decorations and overlapping images are in CSS, not Elementor controls.

## Media & performance
- Supplied ZIP assets: 6.24 MB originals → 0.66 MB optimised WebP (resized to display size @2x). Hero background 1.94 MB → 314 KB.
- Pexels photos referenced by the design (not in ZIP) imported at display size (1.32 MB JPG); EWWW generated WebP copies (0.83 MB) served via `<picture>` (verified, 11 picture tags).
- Plugins: **WP Super Cache** (Apache server, so LiteSpeed Cache not suitable; simple mode; cached page verified) + **EWWW Image Optimizer** (free; exec() disabled on host so only GD/Imagick WebP conversion works, no lossless JPEG/PNG compression). No overlapping plugins.
- Lighthouse (mobile, simulated throttling): Performance 56, Accessibility 96, Best Practices 100, SEO 66 (noindex). LCP 6.7 s, CLS 0.24. Desktop Performance 83 (LCP 2.0 s). No pre-build baseline existed, so no improvement is claimed.
- Remaining: render-blocking Elementor/Google Fonts CSS (~1.4 s), CLS from font swap/late layout, ~440 KB image-delivery savings (gallery sources 900 px), WordPress core lazy-loads the hero paint-cans and bottom-right hero tile (above the fold on desktop).

## Responsive / browser checks (Chromium screenshots via Atarim)
1920, 1440, 1366, 1024, 768, 430, 390, 375, 360: layouts render without broken sections; screenshot widths matched viewports (no overflow observed). Fixed during QA: closing-tag bug, grid breakpoints, header hamburger overlap (tablet/mobile), testimonial widths/dots. Hover states and live animations were **not** interactively tested (static screenshots only).

## Deviations / outstanding
1. Mobile header: phone button and logo slightly smaller than design so the hamburger fits (design overflowed off-screen).
2. Menu/footer links use sitemap URLs (/about/, /services/, /gallery/, /testimonials/, /contact/) – these pages do not exist yet (404). "More About Us", "View Full Gallery", "Learn More", social and Privacy/Terms links are `#` as in the design.
3. Placeholder details kept as supplied (0400 000 000, email, QBCC 0000000, "Customer Name / Suburb").
4. Before/after uses one photo twice with a CSS "weathered" filter (as in the design); both images share one alt text.
5. Colour-contrast flag: the word-fill text starts light grey by design; Hello theme skip link flagged as not focusable.
6. Search engine visibility is off (staging) – switch on before launch.

## Post-build updates
- Site title set to **Platinum Painting Gold Coast** and tagline to **The Platinum Standard In Painting** (Settings › General).
- Site icon (favicon): a white Cinzel "P" monogram on brand blue #1359AC (`design/favicon/pp-site-icon-512.png`, media ID 54). The brand kit had no square icon, so you picked this new mark, derived from the brand. Verified icon + apple-touch-icon tags on the live homepage.
- Responsive round 5 (tablet/mobile): hero card/gradient on mobile, decorations hidden where they overlapped headings, no orphan cards on tablet (offers, weather cards), 2-column gallery on tablet, contact cards keep icon beside text, tighter mobile service cards, 4-column footer at 1024px. Verified live at 360px and previewed at 390/768/1024px (Chromium only).
- Animation audit vs design (Home v2): every animation hook used in the design markup is implemented, with matching counts. Reveals: 63 in the design markup; 73 in the build, because the design's repeating templates (6 hero words, 6 gallery cards) are counted once in markup but appear as separate elements in Elementor. Floats 13, parallax 3, badge spin 3, marquee, word-fill, sun/salt/storm scene loops, fan, twinkle, pulse, scribble draw, header shadow, about hover rows, before/after drag, testimonial autoplay. The design's `drip`/`rock` handlers have no elements in Home v2, so there is nothing to add. Motion verified live by diffing timed screenshots. Hover parity: the glow is limited to the hero CTA, as in the design. Not tested interactively: hover states, drag, and the desktop parallax feel (static screenshots only).
- Responsive sweep (2026-11-16, Chromium via Atarim screenshots) at 320, 360, 375, 390, 430, 768, 1024, 1366, 1440 and 1920px: no horizontal scrolling. Every full-page capture is exactly the viewport width. An overflow probe with the page clip removed shows the only overhang is the rainbow marquee band, which is intentional and clipped. No layout breakdown found. Fixed: email breaking mid-word at 320px, and the "Why It Matters" and Before/After paint cans overlapping text at 1366px. Not tested: Firefox, Safari, Edge.
- Header search removed (2026-11-16): the UAE search button and its divider were deleted from the Site Header template. Verified at 10 widths: phone/tablet header pixel-identical (search was already hidden there); desktop header changed only by the removed search (menu re-centred about 30px right); page heights and widths unchanged; no horizontal scrolling.
