# Knowles page checker

Check a live Knowles Training Institute page or a saved HTML draft against the supplied course, lunch talk, or customized corporate training checklist. The script produces a Markdown report and optional CSV. It only reads pages: it never publishes, edits WordPress, or submits enquiry forms.

## Requirements and installation

Use **Python 3.12 or newer**. The main mode uses only the Python standard library; no `pip install` is needed.

Download or clone this whole repository. Keep these files together (run commands below from the repository folder):

```text
page-checker-script/
├── knowles_page_checker.py
├── README.md
├── CHECKLIST_COVERAGE.md
├── checklists/
│   ├── Content Checklist - Course Page Template.md
│   ├── Content Checklist - Lunch Talk Page Template.md
│   └── Content Checklist - Customised Corporate Training Page Template.md
└── tests/
    └── test_checker.py
```

Check your Python version with `python --version`. Use `python3` instead of `python` if that is how Python 3.12+ is installed on your machine. Checklist paths are resolved beside the script, so you can also run it from another working directory.

## Run an audit

```sh
# Detect the page type and country; write report.md in the working directory.
python knowles_page_checker.py https://ae.knowlesti.com/21st-century-skills-in-the-workplace/

# Specify the type and output name.
python knowles_page_checker.py https://ae.knowlesti.com/active-listening-lunch-talk-in-the-uae/ --type lunchtalk --out lunchtalk-report.md

# Audit a saved draft without logging in or contacting its internal links.
python knowles_page_checker.py saved-draft.html --type customized --country Nigeria --no-link-check

# Write both Markdown and CSV; --csv without a path uses the report basename.
python knowles_page_checker.py saved-draft.html --type course --country UAE --out course-report.md --csv
python knowles_page_checker.py saved-draft.html --type course --country UAE --out course-report.md --csv course-rows.csv

# Skip slow internal-link requests, or verify downloaded WebP signatures.
python knowles_page_checker.py https://ae.knowlesti.com/customized-corporate-training-in-uae/ --no-link-check --check-images --timeout 20

# Astra-theme example.
python knowles_page_checker.py https://nigeria.knowlesti.com/customized-corporate-training-in-nigeria/ --type customized
```

For drafts, save the page HTML as a UTF-8 file from your browser and pass its path. A source save captures server HTML; if a form or accordion is built by JavaScript, its markup may be missing. Use a rendered DOM export or review that portion manually. Local files cannot provide a reliable origin for relative URLs, so internal HTTP checks are marked Manual; absolute images can still be fetched with `--check-images`. The program does not use browser login cookies or bypass authentication.

| Option | Purpose |
| --- | --- |
| `source` | Live HTTP/HTTPS URL or saved UTF-8 HTML path |
| `--type course\|lunchtalk\|customized` | Override detection from the H1 and URL |
| `--country "Hong Kong"` | Override domain/H1 country detection |
| `--out PATH` | Markdown output; default `report.md` |
| `--csv [PATH]` | Also write the same rows as CSV; default report basename with `.csv` |
| `--no-link-check` | Skip GET requests to internal links |
| `--check-images` | Download image files and verify `RIFF....WEBP` bytes; SVG icons are exempt |
| `--timeout SECONDS` | Timeout for each network request; default 15 |
| `--browser` | Add optional Playwright rendering checks |
| `--coverage PATH` | Write a complete checklist handling table, then exit; no source needed |

Internal links are HTTP(S) links on the exact same hostname and port as the final page URL. The script deduplicates URLs, ignores fragment-only, email and telephone links, decodes Cloudflare-protected email addresses, and uses GET requests. HTTP errors fail; network errors and redirects require Review. It follows redirects using Python's normal URL handling and TLS verification. It honours configured proxy settings. Each fetched document/image is limited to 10 MB. Many links can still make a run slow; use `--no-link-check` for a quick offline audit. Treat saved HTML and report contents as potentially private.

Existing report files at the selected output paths are overwritten. Input HTML, script and bundled checklists are protected from report-path collisions. Parent output folders must already exist.

## Read the report

The header records the source, detected type, country, UTC timestamp and status counts. **Problems to fix** lists Fail items first, followed by Review items. The full table preserves every checkbox in the selected checklist, including nested explanations, optional flags and tags. Additional diagnostics cover section presence/order, links, images, forms, text, counts and other static checks.

| Status | Meaning |
| --- | --- |
| ✅ Pass | The particular static check has supporting evidence |
| ❌ Fail | A clear HTML/content problem was found; see its evidence |
| ⚠️ Review | Candidate evidence, ambiguous markup, or a partially checked compound rule needs confirmation |
| 👁 Manual | Requires browser interaction, editorial comparison, WordPress settings or human inspection |
| N/A | An optional image is absent in an identified section, or a diagnostic does not apply to this page type |

A Pass does not certify the whole page. For example, ten closed FAQ controls still need a browser check for “one open at a time”; the combined FAQ checklist row remains Review. Review candidates can appear more than once because both the original checklist row and an additional diagnostic refer to the same issue. Counts include those diagnostics.

Exit codes: **0** = report completed with no definite Fail (Review/Manual may remain); **1** = report completed with at least one Fail; **2** = invalid input, inaccessible source/checklist, or output error. Capture the exit code before running another shell command if using this in CI. No failures are fixed automatically.

## Optional browser mode

The main script works without Playwright. To enable the optional mode:

```sh
python -m pip install playwright
python -m playwright install chromium
python knowles_page_checker.py saved-draft.html --type customized --country Nigeria --browser --no-link-check
```

On minimal Linux machines Chromium may need system libraries; consult Playwright's installation instructions (`python -m playwright install --with-deps chromium` requires system package permissions).

Browser mode reloads at **320, 390, 768, 1024, 1280, 1366 and 1920px**. It inspects document overflow, small text, vertically clipped cards, uneven card rows, identified hero/photo panels, JavaScript errors and console errors. It tests one-open-at-a-time for native `<details>` elements by clicking only their summaries. It does not submit forms. Missing packages/browser binaries or failed navigation are reported without losing the static report.

Browser selectors are heuristic (`.card`, classes ending in `-card`, `.hero img`, classes ending in `-hero`, `.photo-panel img`, `.big-photo img`). Custom themes can use other markup: verify any unrecognised elements manually. Card-row detection and native-details selection need confirmation; custom JavaScript FAQ accordions remain Manual. Browser mode does not prove that hidden images avoided downloading, check all text clipping directions, or verify image content. This optional mode has not been validated against the four example live websites.

## Coverage, assumptions and limitations

[CHECKLIST_COVERAGE.md](CHECKLIST_COVERAGE.md) lists **every checkbox from all three files**, its section, source line and handling method. Regenerate it after changing checklists or routing:

```sh
python knowles_page_checker.py --coverage CHECKLIST_COVERAGE.md
```

The attached checklists are bundled unchanged. Their publishing, deletion and form-test directions are audit requirements for a person; the program does not execute them.

- **Editable rules:** `CHECKLIST_FILES`, `COUNTRIES`, `PAGE_PATTERNS`, `SECTION_KEYWORDS`, `REQUIRED_COUNTS`, `BANNED_WORDS`, `THEME_CLASSES`, `DURATION_OPTIONS` and `ITEM_ROUTES` are named near the top of the script or routing section. Add domain mappings and section aliases there. Checklist text remains the source of truth.
- **Detection:** Lunch Talk, Customized/Customised Corporate Training and Training Course determine type. Page-name validation requires “Customized” in the customized H1. Country uses `--country`, then known domains, then the H1 suffix after “in”. Unknown countries require confirmation; use an override. Course/topic is inferred from the H1; city placeholders require editorial review.
- **Content scope:** `.entry-content` is preferred, then `<main>`, then the whole document. Theme headers/footers and repeated mobile markup can affect results. `script`, `style`, `svg`, `template`, `noscript`, HTML-hidden and `aria-hidden` text are excluded from text searches. Static mode does not evaluate external CSS or execute JavaScript.
- **Sections/counts:** Heading/label aliases and close wording produce candidates, not proof that a section's content is complete. Headings and text inside, or wrapping, a grid of sibling cards (class `card` or ending in `-card`) are never section candidates; a lone card can still hold one. Count rules apply only when the checklist states the number (“6 learning outcomes”), not to a passing mention. Missing or reordered candidates require Review. Lists and known card classes supply counts; unfamiliar markup is never silently treated as a successful count. Duration values are checked against 30/45/60/90/120. Lunch durations outside 30–120 minutes and explicit participant ranges outside 1–25 are flagged. Agenda matching is conservative and reports times/module candidates for manual comparison.
- **SEO:** HTML title equality, metadata length and social images can be inspected. Focus keyphrases are normally private Yoast settings, so description/keyphrase checks remain Review if absent from HTML. WordPress page title, featured-image setting, breadcrumbs and Yoast's 600px width require admin/browser inspection. Different WordPress image-size URLs require Review.
- **Images:** SVG icons are exempt from WebP checks. Empty alt text is Review for decoration; descriptive quality, locale, faces, photo reuse through alternate crop URLs, map accuracy and Media Library settings need manual confirmation. CSS photo URLs are candidates for Review because they may be decorations. Lazy-loading plugins and invisible responsive variants need confirmation.
- **Forms/reviews:** Field signatures, CAPTCHA loaders, AJAX attributes and review/logo candidates are evidence only. Required settings, delivery inbox, actual AJAX behaviour, CAPTCHA enforcement, consent wording, logo/company identity, verbatim quotes and fallback review sources require human verification. No test enquiry is sent.
- **Visual/editorial requirements:** Hover lift/shadow, spacing, alignment, line wrapping, responsive crops, reduced motion, decoration placement, local relevance, promised outcomes, factual FAQ answers, exact fixed copy and matching the country's Contact Us page require manual review. “Hybrid” is explicitly allowed for lunch talks and is listed with context. Possible lunch pricing is flagged for Review to avoid mistaking a FAQ question about price for a displayed fee.

## Development checks

```sh
python -m unittest discover -s tests -v
```

Tests use saved/synthetic HTML and mocked network responses. They cover checklist preservation, all three types, structural failures, FAQ state/count, URL attributes, Cloudflare emails, metadata, images, duration checks, reports/CSV and command-line failures. Live sites may require network allowlist access and are separate from these offline checks.
