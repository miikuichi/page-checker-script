# Content checklist: customised corporate training page template

A skeleton of what the customised corporate training page must contain, on any Knowles country domain. Each domain has one of these pages, and course and lunch talk pages link to it. Based on the Customized Corporate Training in UAE page (ae.knowlesti.com, page 89428).

## How to use this checklist

- **Placeholders:**
  - **[Country]**: the country of the domain.
  - **[City]**: a main city in that country.
- **Content is required; design is flexible.** Each section must contain the content listed. Layout, shapes, card styles and colours follow the UI design of that country's page, within the **design rules** below.
- **Images are described, not fixed.** Each image line says what the photo should show. Every photo is set in [Country] (local people, offices, landmarks), has alt text, and is uploaded as WebP.
- **Optional items** are marked *(optional)*. They can be kept if the country's template design includes them, or removed completely:
  - handwritten taglines
  - bottom bars and banners
  - decorative illustrations
- **Tags:**
  - **Fixed**: the same text on every domain (only the country name changes).
  - **Per country**: set for each domain (locations, links, reviews, contact inbox, spelling).
- **Spelling:** the page name always uses the US spelling "Customized" (e.g. "Customized Corporate Training in [Country]"). Use one spelling consistently in the body text.


## Design rules (all pages)

These apply to every section unless the domain's own page template says otherwise.

- [ ] **No section numbers.** Sections don't show big "01, 02 …" markers. Numbers inside a section's own list (steps, modules, FAQs) are fine.
- [ ] **Section spacing:** 24px at the top and bottom of every section by default. It can follow the domain's own section padding instead.
- [ ] **Boxes and cards stand out** from their section's background colour (e.g. no pale green card on a pale green section).
- [ ] **Cards lift slightly with a shadow on hover.** Keep it quiet (about 3px, no other change). On cards with an icon, the shadow takes the colour of the icon.
- [ ] **Links and cards that go to other pages open in a new tab.**
- [ ] **Buttons that jump to a section on the same page scroll smoothly**, in every browser.
- [ ] **FAQs: exactly 10 questions on every page**, all closed when the page loads, one open at a time.
- [ ] **Buttons outside the Hero and the closing CTA section sit in a card band**, never on their own. A card band is a card across the section with an icon, a short heading, one line of text and the button(s). Its content matches the section it sits in (a good example is the card band "Not sure this is the right course?" in the "Is this the right fit?" section). The enquiry form's submit button is part of the form, so it needs no band.
- [ ] **At least one section between the closing CTA and the enquiry form.** The CTA section must be at least 2 sections away from the form, so they never sit directly next to each other (e.g. CTA, then "From enquiry to delivery", then the enquiry form).
- [ ] **Page width 100%.** The page content always spans the full width (no theme padding, sidebar or title bar). The site's side navigation menu (older domains) or top navigation bar (newer domains) adjusts the space around it.
- [ ] **Hero photo** shows without faces or key parts being cut off or covered by the hero text, at every desktop width.
- [ ] **Hiding photos on smaller screens:** the hero photo and the text over it hide at 1279px wide and below; decorations hide at 1279px and below; other big photo panels (e.g. beside a form or behind a card) hide at 1024px and below. Hidden photos must not download (lazy-load them).


## Build rules (all pages)

### Page setup
- [ ] The WordPress page title matches the H1 exactly (it feeds the breadcrumb and the enquiry email).
- [ ] One H1 per page, and no duplicate IDs.
- [ ] The theme's page title bar doesn't show above the hero. Re-check after every publish, as the template setting can switch back.
- [ ] No menu bar and no footer inside the page (the site has its own).
- [ ] Don't copy the mock-up's logo icon or big section numbers.
- [ ] One look per site: later pages use the same colours and fonts as the first page built on that site.

### Cards and grids
- [ ] Card grids fill complete rows, with no lonely card on the last row (6 cards = 3×2 or 2×3; 8 cards = 4×2 or 2×4).
- [ ] Cards in a row are the same height, and their titles and text start at the same height.
- [ ] A title beside an icon stays on one line at every width. If it wraps, put the icon above the title, change the number of columns, or use a slightly smaller title on the smallest phones.
- [ ] Fact and stat cards: the value sits directly under its label, at the same height in every card.
- [ ] Two list cards side by side: their rows line up.
- [ ] Hover lift goes on important cards only: features, benefits, audience, resources, prices, modules, formats, outcomes, linked course and talk cards. Not on plain lists, FAQ items, agenda rows, forms or tables.
- [ ] Visitors who turn off motion get the shadow only, with no lift.
- [ ] Don't repeat the same button on every card; use one button for the section (e.g. a single "Request a Quote" for the fees).

### Phones and tablets
- [ ] No sideways scrolling at any width from 320px up.
- [ ] Nothing cut off, and no text smaller than 12px.
- [ ] Grids change columns cleanly (desktop, tablet, phone) and still fill complete rows.
- [ ] Hero buttons stay on one line down to 320px (smaller text on small phones if needed).
- [ ] If the site's form uses reCAPTCHA: scale it to 88% on phones and 80% at 360px and below, so it fits.

### Photos and decorations
- [ ] Photos are real images (`<img>`) with alt text, not CSS backgrounds (search engines can't see backgrounds).
- [ ] Alt text describes what is in the photo, without keyword stuffing. Set it in the Media Library and on the page.
- [ ] To fade a photo into a coloured band, fade the photo itself with a mask. Don't lay a colour gradient over it (it leaves thin lines at the edges).
- [ ] Handwritten notes or cards over a photo don't cover faces or words in it (whiteboards, flip charts). Re-check whenever the photo changes.
- [ ] No photo is used twice on one page.
- [ ] Use Media Library images first. Never delete media; the user does that.
- [ ] Image prompts for ChatGPT follow the earlier prompt files (one file per image, with the file name, size, alt text and a description of the scene).
- [ ] Decorations (line art, watercolour) go in empty corners only, never over text; check every desktop width.
- [ ] Anchor a flower or plant by its stem at the section edge so it doesn't look like it's floating.
- [ ] Use decorations on a few sections only.

### Enquiry form settings
- [ ] Each page type has its own form, named with the country: "Customized Corporate Training in [Country]", "Corporate Training Course Enquiry in [Country]", "Lunch Talks Enquiry in [Country]".
- [ ] Email subject "New … Enquiry in [Country]", sent to the enquiry inbox (contact@knowlesti.sg unless the country has its own).
- [ ] CAPTCHA on.
- [ ] AJAX submission on (without it, refreshing the page sends the enquiry again).
- [ ] No "0 of N max characters" counters.
- [ ] Test the form on the live page (the editor hides the CAPTCHA).

---

## 1. Hero
- [ ] **Page title** as the page's only H1: "Customized Corporate Training in [Country]" (per country)
- [ ] **Subtitle:** 1 line (e.g. "Tailored learning for high-performing [Country] organisations.") (per country)
- [ ] **Short description:** Knowles helps organisations run existing courses, customise proven programmes or build bespoke learning (fixed)
- [ ] **Hero image:** a corporate team in a training workshop with a facilitator, in a recognisably [Country] setting (per country)
- [ ] **2 buttons:** start your enquiry (goes to the enquiry form) and browse corporate courses (goes to the course hub) (fixed)

## 2. Training formats strip
- [ ] **5 quick facts:** in-house at your office, live online anywhere in [Country], blended learning, 1,500+ courses, tailored to your team and goals (fixed / per country)

## 3. Start with what you see at work
- [ ] Heading "Start with what you see at work" and intro: you don't need to diagnose the training need yourself (fixed)
- [ ] **4 example quotes:** problems a manager might describe in their own words (e.g. "Our new supervisors were promoted for technical skill, not for leading people.") (fixed)
- [ ] **3 promises:** no training brief needed, reply within one working day, ask before you commit (fixed)
- [ ] *(optional)* **Image:** a recognisable [Country] city view or workplace, large enough to fill up to half the section (per country)

## 4. Enquiry form
- [ ] Heading (e.g. "What would you like your team to achieve?") and intro (fixed)
- [ ] **Enquiry form:** name, email, contact number, enquiry and consent (with a privacy policy link), spam protection (reCAPTCHA) and a submit button. Notifications go to [Country]'s enquiry inbox (per country)
- [ ] **Form layout follows the SG enquiry form** (knowlesti.sg), recoloured in the domain's colours, including its "Training topic or course title" field (fixed)
- [ ] Privacy note: details are used only to respond to the enquiry, with a link to the privacy policy (per country link)
- [ ] *(optional)* **Image:** professionals in [Country] at work, filling up to half the section beside the form, darkened or faded so any text over it stays readable (per country)

## 5. Three ways to build the right programme
- [ ] Heading and intro (fixed)
- [ ] **3 options**, each with an icon, a name and 1–2 lines (fixed):
  - Run an existing course (from 1,500+ courses)
  - Customise a course (sector, team and objectives)
  - Develop a bespoke programme
- [ ] *(optional)* Card band with a button to the enquiry form, if the domain's layout has one here (fixed)

## 6. What we can fit to your team
- [ ] Heading and intro (fixed)
- [ ] **Image:** colleagues in [Country] planning a tailored training programme together (per country)
- [ ] **6 elements**, each with an icon, a name and 1 line (fixed, country named): objectives and content, examples and industry context ([Country] market), activities and scenarios, roles and experience levels, duration and format, sequence and pathways

## 7. A clear next step at every stage
- [ ] Heading and intro (fixed)
- [ ] **4 numbered steps**, each with a name and 1 line (fixed):
  - Tell us your priorities
  - We clarify the requirement
  - We recommend an approach
  - You review the proposal (content, format, timeline and investment)

## 8. What does your team need to strengthen?
- [ ] Heading and intro (fixed)
- [ ] **About 7 training topic tiles**, each with an SVG icon or illustration (not a photo), a name and a link to a real category page on the domain (e.g. leadership, corporate communication, interpersonal communication, sales, customer service, soft skills, personal development) (per country links)
- [ ] **"See all" link** to the course hub (fixed)

## 9. Planning across teams and locations?
- [ ] Heading and intro: training across multiple sites, with flexible delivery (fixed)
- [ ] **4 planning options:** multi-site delivery across [Country], multiple cohorts and phased rollouts, pilot sessions, in-person / virtual / blended delivery (fixed / per country)
- [ ] **Map of [Country] showing the locations where KTI delivers training.** This is the main element of the locations panel. Mark each location at its true position on the map and label it. Draw the map from real country borders so it stays sharp at every size (per country)
- [ ] **Location list:** the KTI locations named in text, with a count summary (e.g. "7 Emirates, 11 Locations"; use the country's own regions) (per country)

## 10. What clients say
- [ ] Heading (e.g. "What clients say") and intro (fixed)
- [ ] **3 real reviews**, copied word for word from [Country]'s own reviews page, each showing only the quote, the company name (in larger text) and the company logo (no border, shown large). No course name, no stars and no dates (per country)
- [ ] If [Country] has no reviews of its own, use reviews from the KTI Singapore reviews page (knowlesti.sg)
- [ ] Each logo matches the company in the review, and the reviews differ from those on the course template page where possible

## 11. Frequently asked questions
- [ ] Heading (e.g. "Questions we are asked most") and intro naming [Country] (per country)
- [ ] **10 questions** that open and close, all closed when the page loads, one open at a time. Topics (fixed): choosing the right course · where training is delivered in [Country] · live online and in-house · response time · several teams or locations at once · what can be customised · industry-specific examples · what affects the quote and lead time · how far ahead to book · certificate
- [ ] The answer on locations names the same cities as the map in section 9 (per country)
- [ ] All answers are based on KTI's published FAQ answers, not invented
- [ ] *(optional)* **Image:** a [Country] workplace or landmark, filling the section behind the content rather than sitting in a small card, as a real image (not a CSS background) (per country)

## 12. Shape the right programme for your team
- [ ] Heading (e.g. "Shape the right programme for your team") and intro (fixed)
- [ ] **Image:** a recognisable [Country] skyline or landmark filling the section behind the text, as a real image (not a CSS background) (per country)
- [ ] **Button** to explore all corporate courses (goes to the course hub) (fixed)
- [ ] **4 benefits:** tailored to your goals, practical and relevant learning, support from [Country]-based experts, results that make a difference (fixed / per country)

---

## SEO and publishing checks (after publishing)

### SEO (Yoast)
- [ ] **SEO title** = the page name (the H1), with no site name added, within Yoast's width limit (600px).
- [ ] **Focus keyphrase** set, and a **meta description** of about 120–140 characters that contains it.
- [ ] **Facebook and X image** = the hero photo.
- [ ] **Featured image** = the hero photo.
- [ ] Every image has alt text.

### Publishing
- [ ] Publish every update right away, then check the live page (reload with a cache-buster, e.g. `?v=2`).
- [ ] After each publish, check that the page template and the hidden title bar didn't switch back.
- [ ] Old page content: delete only when asked, and save a backup first.
- [ ] The site header and footer are shared by every page: report problems, and change them only with an OK.

### Final sweep on the live page (320px to 1920px)
- [ ] No sideways scroll, nothing cut off, card rows even.
- [ ] Spacing the same in every section.
- [ ] All links work (no 404s) and all images load.
- [ ] FAQs all closed when the page loads, one open at a time.
- [ ] The enquiry form shows with its CAPTCHA, and a test enquiry arrives.
- [ ] One H1, no duplicate IDs, no console errors.
- [ ] SEO title, meta description, Facebook/X image, featured image and breadcrumb all match the H1.
- [ ] Search the page text for: "Lorem", "undefined", placeholder text, wrong durations and wrong contact details.
