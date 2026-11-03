# Content checklist: lunch talk page template

A skeleton of what every individual lunch talk page must contain, on any Knowles country domain. Based on the Active Listening Lunch Talk in the UAE page (ae.knowlesti.com, page 89533).

## How to use this checklist

- **Placeholders:**
  - **[Topic]**: the lunch talk topic (e.g. Active Listening).
  - **[Country]**: the country of the domain.
  - **[City]**: a main city in that country.
- **Content is required; design is flexible.** Each section must contain the content listed. Layout, shapes, card styles and colours follow the UI design of that country's page, within the **design rules** below.
- **Images are described, not fixed.** Each image line says what the photo should show. Every photo is set in [Country] (local people, offices, landmarks), has alt text, and is uploaded as WebP.
- **Optional items** are marked *(optional)*. They can be kept if the country's template design includes them, or removed completely:
  - handwritten taglines
  - bottom bars and banners
  - decorative illustrations (skylines, patterns)
- **Tags:**
  - **Per topic**: written for each new lunch talk.
  - **Fixed**: the same text on every lunch talk page (only the country name changes).
  - **Per country**: set once for each domain (locations, contact details, links).
- Every section has a **small label**, a **heading** and a **short intro** (1–2 sentences), unless noted otherwise.


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
- [ ] Small label "Lunch Talk" (fixed)
- [ ] **Talk title** as the page's only H1: "[Topic] Lunch Talk in [Country]" (per topic)
- [ ] **Tagline:** 3 short phrases on the benefit (e.g. "Better listening. Clearer conversations. Stronger teams.") (per topic)
- [ ] **Short description:** 1 sentence on what the talk helps professionals do (per topic)
- [ ] **Hero image:** professionals in [Country] in a workplace moment that shows the topic (e.g. colleagues listening to each other in a meeting) (per topic + per country)
- [ ] **2 buttons:** request this lunch talk (goes to the enquiry form) and browse lunch talk topics (goes to the lunch talks hub) (fixed)
- [ ] **5 quick facts:** duration (30–120 minutes), formats (onsite, virtual, hybrid), audience (all employee levels), customisable, delivered across [Country] (fixed / per country)

## 2. What is this lunch talk about?
- [ ] Heading describing the topic at work (e.g. "What Better Listening Looks Like at Work") (per topic)
- [ ] **Definition paragraph:** what [Topic] means and why it matters in [Country]'s workplaces (per topic + per country)
- [ ] **"Commonly known as"** line: 3–5 other names for the topic (per topic)
- [ ] **3 cards with 3–4 points each:** Why it matters, Problems it addresses, Participants leave able to (per topic)

## 3. Framework
- [ ] Small label, e.g. "Our framework" (fixed)
- [ ] Heading naming the framework (e.g. "The 10 Habits of an Active Listener") and intro (per topic)
- [ ] **Framework content, clearly set out:** about 10 numbered habits, steps or principles with short names, in a logical order. Shown in any visual form (path, steps, grid, circle) (per topic)

## 4. Session formats
- [ ] Small label, e.g. "Flexible agenda. Practical learning." (fixed)
- [ ] Heading (e.g. "One Topic. Five Ways to Run the Session.") and intro listing the durations (fixed)
- [ ] **5 duration options**, each with the length, a format name, 1 line on what it covers and who it suits (fixed, adapted to the topic):
  - 30 minutes: Awareness Boost
  - 45 minutes: Explore and Discuss
  - 60 minutes: Apply and Practise (most popular)
  - 90 minutes: Deepen and Develop
  - 120 minutes: Custom and Comprehensive
- [ ] **Learning flow in 5 steps:** Open, Understand, Practise, Discuss, Commit, each with 1 line (fixed)

## 5. Who should attend?
- [ ] Heading (e.g. "Designed for People Who Need to Understand People.") and intro on who benefits (per topic)
- [ ] **5 audience groups**, each with 1 line on what they gain (e.g. team members, people managers, project and cross-functional teams, customer-facing professionals, leaders and supervisors) (per topic)
- [ ] *(optional)* Central message, e.g. "A more connected, collaborative workplace starts with better listeners."

## 6. Workplace application
- [ ] Heading (e.g. "Where Better Listening Changes the Conversation.") and intro (per topic)
- [ ] **Image:** someone in a [Country] workplace using the skill in a real conversation (e.g. listening attentively as a colleague explains an idea) (per topic + per country)
- [ ] **6 workplace situations**, each with a short name and 1 line (e.g. meetings, one-to-ones, customer conversations, feedback and coaching, conflict, stakeholder communication) (per topic)
- [ ] **Card band** with a button to the customisation section, e.g. "Want Real Workplace Examples?" with the button "See How We Tailor It" (per topic)

## 7. Delivery options
- [ ] Heading (e.g. "Run It Where Your Team Works Best.") and intro (fixed)
- [ ] **Image:** a lunch talk in progress, either at a client's workplace in [Country] or with a team joining online. Not an empty room or a generic meeting (per country)
- [ ] **3 delivery modes**, each with a short description and 2–3 benefits (fixed, country named):
  - Onsite (at your premises)
  - Virtual (live online, from anywhere in [Country])
  - Hybrid (in-person and online together)

## 8. Customisable for you
- [ ] Heading (e.g. "Your Team. Your Context. Your Conversation.") and intro (fixed, topic named)
- [ ] **5 customisation options:** business objective, audience level, industry examples, real workplace scenarios, session length and interaction (fixed)
- [ ] **Link to the customised training page**, e.g. a banner "We'll Customise It for Your Team." with the button "Explore Customisation Options" (per country link)

## 9. Training across [Country]
- [ ] Heading (e.g. "[Topic] Lunch Talks Across [Country].") and intro: onsite, at an arranged venue or live online anywhere in [Country] (per country)
- [ ] **Map of [Country] showing the locations where KTI delivers.** This is the main element of the section. Mark each location at its true position on the map and label it. Draw the map from real country borders so it stays sharp at every size (per country)
- [ ] **Location list:** the KTI locations named in text (cards, columns or a list, as the design suits), grouped by region if the country has many (per country)
- [ ] *(optional)* Map legend, e.g. "Dots mark the cities where we deliver"

## 10. Related topics
- [ ] Heading (e.g. "Continue Building Better Workplace Conversations.") and intro (per topic)
- [ ] *(optional)* **Image:** colleagues in a relaxed [Country] office setting, e.g. talking over lunch (per country)
- [ ] **6 related lunch talks**, each with a name, 1 line and a link to that lunch talk's page on the domain (per topic + per country links)
- [ ] **Link to all lunch talks**, e.g. a banner "Not Sure Which Topic Is Right for Your Team?" with the button "View All Lunch Talk Topics" (goes to the lunch talks hub) (fixed)

## 11. Take the next step
- [ ] Heading (e.g. "Ready to Make Better Listening a Workplace Habit?") and intro naming [Country] organisations (per topic + per country)
- [ ] **Button** to browse all lunch talks (goes to the lunch talks hub) (fixed)

## 12. Frequently asked questions
- [ ] Heading (e.g. "Questions [Country] Organisations Ask Before Booking.") (per country)
- [ ] **10 numbered questions** that open and close, all closed when the page loads, one open at a time:
  - About the talk (per topic): what the talk is · what participants learn · who it suits
  - Practical (fixed): duration options · onsite, virtual or hybrid · customisation · ideal group size and multiple sessions · delivery outside the main cities · how far ahead to book · how to request a proposal
- [ ] Answers name the topic and [Country] where relevant; city names match the locations in section 9
- [ ] All answers are based on KTI's published FAQ answers and lunch talk information, not invented

## 13. Get in touch
- [ ] Heading (e.g. "Tell Us What Your Team Needs.") and intro (fixed)
- [ ] **3 promises:** fast response (within 1 business day), no obligation, tailored recommendation (fixed)
- [ ] **Enquiry form:** name, email, contact number, enquiry and consent (with a privacy policy link), spam protection (reCAPTCHA) and a submit button. Notifications go to [Country]'s enquiry inbox (per country)
- [ ] **Form layout follows the SG enquiry form** (knowlesti.sg), recoloured in the domain's colours, including its "Training topic or course title" field (fixed)
- [ ] **"We're here to help" panel:** delivery format, scheduling, customisation (fixed, country named)
- [ ] *(optional)* **Image:** a recognisable [Country] skyline or landmark (per country)

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
