# Content checklist: course page template

A skeleton of what every individual course page must contain, on any Knowles country domain. Based on the 21st Century Skills in the Workplace page (ae.knowlesti.com, page 89481).

## How to use this checklist

- **Placeholders:**
  - **[Course]**: the course name.
  - **[Country]**: the country of the domain (e.g. UAE, Singapore, Hong Kong).
  - **[City]**: a main city in that country.
- **Content is required; design is flexible.** Each section must contain the content listed. Layout, shapes, card styles and colours follow the UI design of that country's page, within the **design rules** below.
- **Images are described, not fixed.** Each image line says what the photo should show. Every photo is set in [Country] (local people, offices, landmarks), has alt text, and is uploaded as WebP.
- **Optional items** are marked *(optional)*. They can be kept if the country's template design includes them, or removed completely:
  - handwritten taglines
  - bottom bars and banners
  - decorative illustrations (skylines, dunes, patterns)
- **Tags:**
  - **Per course**: written for each new course.
  - **Fixed**: the same text on every course page (only the country name changes).
  - **Per country**: set once for each domain (locations, currency, prices, contact details, links, national goals).
- Every section has a **small label**, a **heading** and a **short intro** (1–2 sentences), unless noted otherwise.
- Under each section title, the line in *italics* says in one sentence what that section is for. The checkboxes below it list the content it must contain.


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
*The first screen. It names the course, sums up what it delivers and gives the two main next steps.*

- [ ] Small label, e.g. "Corporate training course" (fixed)
- [ ] **Course title** as the page's only H1: "[Course] Training Course in [Country]" (per course)
- [ ] **One-line subtitle** (per course)
- [ ] **Short course description**, 1–2 sentences (per course)
- [ ] **Hero image:** professionals from [Country] in a training workshop, in a recognisably local setting (per country)
- [ ] **2 buttons:** enquire about this course (goes to the enquiry form) and explore corporate training courses (goes to the course hub) (fixed)
- [ ] **4 quick facts:** duration and format (2 days, in-person or virtual), group size (1–25 participants), practical results, delivered across [Country] (fixed / per country)

## 2. Course snapshot ("Course at a glance")
*A plain-language summary: what the course is, what it helps people do, and its focus, audience and outcomes.*

- [ ] Heading "What is the [Course] Training Course?" (per course), or "Course at a Glance" with the small label "Course at a glance" (fixed). The Nigeria pages use "Course at a Glance".
- [ ] Intro: 1 sentence saying it is a practical two-day course and what it equips people with (per course)
- [ ] **Direct answer:** 1–2 plain-language sentences on what the course helps people do (per course)
- [ ] **3 facts:** Focus, Designed for, Outcomes (per course)

## 3. Why it matters in [Country]
*Links the course to [Country]'s economy, workforce and national goals, so the training feels locally relevant.*

- [ ] Small label "Why it matters in [Country]" (per country)
- [ ] Heading and intro linking the course to [Country]'s economy and goals (per course + per country)
- [ ] **4 points**, each with an icon, a heading and 1 line. One point names a national goal or vision (e.g. "Supporting UAE Vision 2031"; use the equivalent for each country) (per course + per country)
- [ ] *(optional)* Decorative illustration

## 4. From challenges to business outcomes
*Shows the problems the course solves: common workplace challenges, the skills that bridge them and the results for the organisation.*

- [ ] Heading and intro (per course)
- [ ] **Challenges → skills → outcomes**, shown as a flow:
  - Common workplace challenges in [Country]: about 5 items (per course + per country)
  - The [Course] skills that bridge them: about 6 items (per course)
  - Business outcomes for the organisation: about 5 items (per course)
- [ ] *(optional)* **Image:** a recognisable [Country] city view or landmark (per country)

## 5. What participants will be better able to do
*What participants can do differently after the course.*

- [ ] Heading (e.g. "Practical skills for immediate impact") and intro (per course)
- [ ] **6 learning outcomes**, each with an icon, a short action-word heading and 1 line (e.g. "Think critically: analyse situations, solve problems …") (per course)

## 6. Where these skills make a difference
*Everyday work situations where participants will use the skills.*

- [ ] Heading (e.g. "Real-world application across your organisation") and intro (per course)
- [ ] **Image:** people in [Country] applying the course's skills at work, e.g. a facilitator or team leader guiding a discussion with colleagues. Any shape or crop that fits the design (per country)
- [ ] **8 application areas**, each with an icon and a short label (e.g. sales and business development, customer service, cross-functional collaboration) (per course)

## 7. Course framework
*The course's named method: a few building blocks that take participants from understanding a challenge to acting on it.*

- [ ] Small label naming the framework (e.g. "KTI [Name] Framework") (per course)
- [ ] Heading and intro explaining what the framework achieves (per course)
- [ ] **Framework content, clearly set out:** about 5 building blocks, each with a name and 1 line, in a logical order from foundation to result. Shown in any visual form (pyramid, steps, circle, layers) (per course)
- [ ] *(optional)* Handwritten tagline

## 8. Course curriculum
*The ten modules the course covers, in order. They are also the session names in the agenda.*

- [ ] Heading and intro mentioning that it is a two-day course (per course)
- [ ] **10 numbered modules** with short titles (per course)
- [ ] **Card band** with the button "View detailed agenda" (goes to the agenda section); its heading and line match the curriculum (fixed)
- [ ] The modules match the sessions in the agenda (section 18)

## 9. Real workplace scenarios
*Realistic local work situations that participants practise on during the course.*

- [ ] Heading (e.g. "Learn through situations that feel familiar") and intro (per course)
- [ ] **Image:** a diverse team in [Country] working through a business problem together (per country)
- [ ] **4 scenario cards**, each with a title, 1 line and the skill it practises. At least one is set in a [City] (per course + per country)
- [ ] *(optional)* Tagline, e.g. "Real people. Real challenges. Real progress."

## 10. Why organisations choose this course
*The reasons organisations choose Knowles for this course.*

- [ ] Heading "Built for [Country] organisations, backed by results" (per country)
- [ ] Intro: 1 or 2 paragraphs, depending on the space in the design (fixed)
- [ ] **Image:** a recognisable [Country] landmark or business district (per country)
- [ ] **6 reasons:** [Country] relevance, practical and actionable, measurable impact, trusted by leading organisations, flexible and scalable (1 to 25 participants), a long-term partner (fixed)

## 11. Who should attend
*Who the course is for, and the goals that show it is the right fit.*

- [ ] Heading (e.g. "Is this the right course for your team?") and intro (fixed)
- [ ] **Image:** a team leader with colleagues at different career stages, in a [Country] workplace (per country)
- [ ] **"Ideal for" list:** 5 types of participant (fixed)
- [ ] **"You may also consider this course if you want to" list:** 5 goals (per course)
- [ ] **Card band** with 2 buttons, e.g. "Not sure this is the right course?" with get help (goes to the form) and explore corporate courses (goes to the course hub) (fixed)

## 12. Prerequisites and experience level
*What participants need (and don't need) before attending, the experience level and the group size.*

- [ ] Heading (e.g. "Open to diverse learners") and intro (fixed)
- [ ] **3 points:** Prerequisites (none required), Experience level (all levels, early career to senior leaders), Team participation (minimum 1, maximum 25 per session) (fixed)
- [ ] *(optional)* Closing banner, e.g. "A learning experience for everyone"

## 13. Assessment and learning diagnostic
*How participants' starting skills are checked, so the training can be tailored and progress measured.*

- [ ] Heading (e.g. "Understand starting points. Maximise results.") and intro (fixed)
- [ ] **Image:** a facilitator reviewing progress or results with a small team (per country)
- [ ] **4 steps:** pre-course self-assessment, identify development areas, tailored learning experience, measure progress (fixed)
- [ ] *(optional)* Handwritten tagline

## 14. Adapting the programme for [Country] organisations
*How the content is adapted to [Country]'s sectors, culture and national priorities.*

- [ ] Heading (e.g. "Local relevance. Global best practice.") and intro (per country)
- [ ] **Image:** something that represents doing business in [Country], e.g. local professionals in a recognisably local business setting, or a landmark that stands for the country's economy. Any orientation (portrait or landscape) (per country)
- [ ] **4 points:** [Country] business context (naming the country's key sectors), cultural alignment, local case studies, supporting national priorities (per country)

## 15. Customisation
*The ways an organisation can tailor the course, with a route to the customised training page.*

- [ ] Heading (e.g. "A course shaped around your goals") and intro (fixed)
- [ ] **6 options:** focus areas, industry relevance, team-specific outcomes, delivery and format, blended learning options, ongoing support (fixed)
- [ ] **Link to the customised training page**, e.g. a banner "Let's design the right solution for you" with a button (per country link)

## 16. Choose your training format
*The ways the course can be delivered, and how the facilitator is chosen.*

- [ ] Heading (e.g. "Flexible formats for your organisation") and intro (fixed)
- [ ] **Image:** training being delivered, not a meeting. For example, a facilitator leading an interactive session at a client's office in [Country], or a participant taking part in a live virtual class (per country)
- [ ] **4 formats:** in-person at your premises, virtual training, public scheduled sessions, facilitator matching (fixed)

## 17. How participants learn
*The learning approach, as five steps from first engagement to keeping the learning going.*

- [ ] Heading (e.g. "A hands-on and engaging learning experience") and intro (fixed)
- [ ] **5 steps**, each with 1 line: Engage, Practise, Apply, Reflect, Sustain (fixed)
- [ ] *(optional)* Closing element: a tagline bar, or a card banner that links to another page (e.g. the course hub or customisation page)

## 18. Two-day course agenda
*The timetable for both days: sessions, breaks, group size and venue.*

- [ ] Heading (e.g. "A practical journey from insight to impact") and intro (fixed)
- [ ] **Day 1 timetable:** day title, sessions from 09:00 to 17:00, opening welcome and course overview, closing wrap-up and reflections (per course sessions)
- [ ] **Day 2 timetable:** day title, sessions from 09:00 to 17:00, opening recap, action planning before the close, closing next steps (per course sessions)
- [ ] **Breaks on both days, at the same times:** morning break, lunch break, afternoon break (fixed times; the UAE page uses 10:30–10:45, 12:15–13:15 and 14:45–15:00)
- [ ] Session names match the curriculum modules (section 8)
- [ ] **Group size and venue:** 1–25 participants; delivered at your premises or a venue of your choice in [Country] (fixed / per country)

## 19. Participant resources and post-course application
*What participants receive to use during and after the course.*

- [ ] Heading (e.g. "Practical tools for continued growth") and intro (fixed)
- [ ] **Image:** a participant using the course materials to apply what they learned (any setting; not necessarily devices) (per country)
- [ ] **5 resources:** learner guide, course workbook, digital resources, course handouts, certificate of completion (fixed)
- [ ] *(optional)* Closing banner, e.g. "Put learning into action"

## 20. Pricing and investment
*The price of each format, and the discounts for teams.*

- [ ] Heading (e.g. "High-value training for a stronger workforce") and intro (fixed)
- [ ] **4 price options**, each with a format, a price in the country's chosen currency and 1 line: Lunch Talk (1 hour), Half Day, Full Day, 2 Day (per country)
- [ ] **Team discounts:** discounts for more than 2 participants, group discounts up to 40%, minimum 1 and maximum 25 participants (fixed)

## 21. Corporate evidence
*Proof that organisations trust Knowles: track record, relevance, impact and long-term partnership.*

- [ ] Heading (e.g. "Trusted by organisations across [Country]") and intro (per country)
- [ ] **4 proof points:** proven track record, practical and relevant, measurable impact, a long-term partner (fixed)
- [ ] **Image:** a recognisable [Country] city view (per country)
- [ ] *(optional)* Image caption and tagline

## 22. Reviews ("In their own words")
*Real feedback from past participants, quoted word for word with the company and course.*

- [ ] Heading (e.g. "What participants tell us") and intro with a link to [Country]'s reviews page (per country)
- [ ] **3 real reviews**, copied word for word from [Country]'s own reviews page, each showing only the quote, the company name (in larger text) and the company logo (no border, shown large). No course name, no stars and no dates (per country)
- [ ] If [Country] has no reviews of its own, use reviews from the KTI Singapore reviews page (knowlesti.sg)
- [ ] Each logo matches the company in the review, and reviews differ from other template pages where possible

## 23. Frequently asked questions
*Short answers to the questions buyers ask most, in dropdowns.*

- [ ] Heading (e.g. "Your questions answered") and intro naming the course (per course)
- [ ] *(optional)* **Image:** a [Country] landmark (per country)
- [ ] **10 numbered questions** that open and close, all closed when the page loads, one open at a time. Topics: main focus · who it suits · learning outcomes · where and how it is delivered in [Country] (at your office, a venue or virtual) · customisation · duration · number of participants · certificate · group discounts · how to get started
- [ ] Answers about the main focus, who it suits and learning outcomes are written for the course; the other answers are fixed (per course / fixed)
- [ ] All answers are based on KTI's published FAQ answers and course information, not invented

## 24. Top 6 corporate training courses
*Links to other popular courses on the same site.*

- [ ] Heading and intro, then a **card band** with a "Browse all courses" button (goes to the course hub) (fixed)
- [ ] **6 course cards**, each with an icon or illustration, a course area name, a short tagline and a link to a real category page on that domain (per country links)

## 25. Training across [Country]
*Where Knowles delivers training in [Country], on a map and in a list.*

- [ ] Heading (e.g. "Local delivery across [Country]") and intro saying where KTI delivers training, with in-person and virtual options (per country)
- [ ] **Map of [Country] showing the locations where KTI delivers training.** This is the main element of the section. Mark each location at its true position on the map and label it. Draw the map from real country borders so it stays sharp at every size (per country)
- [ ] **Location list:** the KTI locations named in text (cards, columns or a list, as the design suits), grouped by region if the country has many (per country)
- [ ] *(optional)* Side note and handwritten tagline

## 26. Take the next step
*The closing call to action. It invites visitors to enquire or browse all courses.*

- [ ] Heading naming the course's aim and the country (e.g. "Build future-ready teams in [Country]") and intro (per course + per country)
- [ ] **Image:** a wide, recognisable [Country] skyline or landmark filling the section behind the text, as a real image (not a CSS background) (per country)
- [ ] **Button** to view all courses (goes to the course hub) (fixed)
- [ ] **3 points:** develop your people, drive better results, a stronger [Country] (first point per course, last per country)

## 27. From enquiry to delivery
*The steps from first contact to follow-up, so buyers know what happens next.*

- [ ] Heading (e.g. "A simple process, from conversation to impact") and intro (fixed)
- [ ] **5 numbered steps:** get in touch, discuss and plan, confirm and prepare, deliver the training, follow up for lasting impact (fixed)
- [ ] *(optional)* Closing banner

## 28. Get in touch
*The enquiry form and the contact details for [Country].*

- [ ] Heading (e.g. "Let's discuss your training needs") and intro (fixed)
- [ ] **Enquiry form:** name, email, contact number, enquiry and consent (with a privacy policy link), spam protection (reCAPTCHA) and a submit button. Notifications go to [Country]'s enquiry inbox (per country)
- [ ] **Form layout follows the SG enquiry form** (knowlesti.sg), recoloured in the domain's colours, including its "Training topic or course title" field (fixed)
- [ ] **Contact details** from that domain's Contact Us page: office location, email, phone, business hours with time zone (per country)
- [ ] *(optional)* Closing note naming the country

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
