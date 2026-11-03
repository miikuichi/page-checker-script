#!/usr/bin/env python3
"""Read-only Knowles checklist auditor. Python 3.12+, no main-mode dependencies."""
from __future__ import annotations

import argparse
from collections import Counter
import csv
from dataclasses import dataclass, field
from datetime import datetime, timezone
from difflib import SequenceMatcher
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urldefrag, urljoin, urlsplit
from urllib.request import Request, urlopen

CHECKLIST_FILES = {
    'course': 'Content Checklist - Course Page Template.md',
    'lunchtalk': 'Content Checklist - Lunch Talk Page Template.md',
    'customized': 'Content Checklist - Customised Corporate Training Page Template.md',
}
COUNTRIES = {'ae.knowlesti.com': 'UAE', 'knowlesti.sg': 'Singapore',
             'hongkong.knowlesti.com': 'Hong Kong', 'nigeria.knowlesti.com': 'Nigeria',
             'seychelles.knowlesti.com': 'Seychelles', 'vietnam.knowlesti.com': 'Vietnam'}
PAGE_PATTERNS = {'course': r'.+ Training Course in (?:the )?{country}',
                 'lunchtalk': r'.+ Lunch Talk in (?:the )?{country}',
                 'customized': r'Customized Corporate Training in (?:the )?{country}'}
SECTION_KEYWORDS = {
    'hero': ['hero'], 'course snapshot': ['course at a glance', 'what is the'],
    'why it matters': ['why it matters'],
    'from challenges': ['challenges', 'business outcomes'],
    'what participants will': ['practical skills for immediate impact', 'learning outcomes'],
    'where these skills': ['real-world application', 'application areas'],
    'course framework': ['framework'], 'framework': ['framework', 'habits'],
    'course curriculum': ['curriculum', 'modules'],
    'real workplace scenarios': ['situations that feel familiar', 'scenarios'],
    'why organisations': ['built for', 'why organisations'],
    'who should attend': ['right course for your team', 'who should attend', 'designed for people'],
    'prerequisites': ['open to diverse learners', 'prerequisites'],
    'assessment': ['understand starting points', 'assessment', 'diagnostic'],
    'adapting': ['local relevance', 'global best practice'],
    'customisation': ['shaped around your goals', 'customisation'],
    'choose your training': ['flexible formats', 'training format'],
    'how participants learn': ['hands-on and engaging', 'how participants learn'],
    'two-day': ['agenda', 'insight to impact'],
    'participant resources': ['continued growth', 'resources'],
    'pricing': ['pricing', 'investment', 'high-value training'],
    'corporate evidence': ['trusted by organisations', 'corporate evidence'],
    'reviews': ['reviews', 'in their own words', 'participants tell us'],
    'what clients say': ['what clients say', 'testimonials'],
    'frequently asked': ['frequently asked', 'questions answered', 'questions we are asked', 'questions'],
    'top 6': ['top 6', 'popular courses'],
    'training across': ['local delivery across', 'training across', 'lunch talks across'],
    'take the next step': ['ready to', 'build future-ready', 'take the next step'],
    'from enquiry': ['conversation to impact', 'from enquiry'],
    'get in touch': ['get in touch', 'discuss your training needs', 'tell us what your team needs'],
    'what is this lunch': ['what', 'looks like at work'],
    'session formats': ['session formats', 'five ways', 'flexible agenda'],
    'workplace application': ['workplace application', 'changes the conversation'],
    'delivery options': ['delivery options', 'works best'],
    'customisable': ['your team. your context', 'customis'],
    'related topics': ['related', 'continue building'],
    'training formats strip': ['training formats'],
    'start with': ['start with what you see at work'],
    'enquiry form': ['what would you like your team to achieve', 'enquiry'],
    'three ways': ['three ways', 'right programme'],
    'what we can fit': ['what we can fit', 'fit to your team'],
    'a clear next': ['clear next step'],
    'what does your team': ['need to strengthen'],
    'planning across': ['planning across', 'teams and locations'],
    'shape the right': ['shape the right programme'],
}
REQUIRED_COUNTS = {'learning outcomes': 6, 'numbered modules': 10, 'price options': 4,
                   'duration options': 5, 'real reviews': 3, 'related lunch talks': 6,
                   'course cards': 6, 'audience groups': 5, 'workplace situations': 6,
                   'application areas': 8, 'scenario cards': 4}
BANNED_WORDS = [r'\bLorem\b', r'\bundefined\b', r'\bTBD\b', r'\[insert', r'\{\{',
                r'\[(?:Country|Course|Topic|City)\]']
THEME_CLASSES = {'avada-page-titlebar-wrapper', 'fusion-page-title-bar',
                 'entry-header', 'ast-archive-description'}
WIDTHS = (320, 390, 768, 1024, 1280, 1366, 1920)
DURATION_OPTIONS = {30, 45, 60, 90, 120}
STATUSES = {'pass': '✅ Pass', 'fail': '❌ Fail', 'review': '⚠️ Review',
            'manual': '👁 Manual', 'na': 'N/A'}
VOID = set('area base br col embed hr img input link meta param source track wbr'.split())
SKIP_TEXT = {'script', 'style', 'svg', 'template', 'noscript'}
USER_AGENT = 'Mozilla/5.0 (compatible; KnowlesPageChecker/1.0; read-only audit)'


def clean(text):
    return re.sub(r'\s+', ' ', text).strip()


def plain(text):
    return clean(re.sub(r'[*`_]', '', text))


def required_count(text):
    """REQUIRED_COUNTS value for a phrase stated as a count ("6 learning outcomes"), not a passing mention."""
    return next((v for k, v in REQUIRED_COUNTS.items() if re.search(rf'\b\d+\s+{re.escape(k)}\b', text)), None)


@dataclass(eq=False)
class Node:
    tag: str
    attrs: dict = field(default_factory=dict)
    parent: Node | None = None
    children: list = field(default_factory=list)
    line: int = 0

    def find(self, tag=None, cls=None, id=None, text=None):
        """Find descendants by tag, class, ID, or visible text."""
        return [n for n in self.walk() if (tag is None or n.tag == tag)
                and (cls is None or cls in n.attrs.get('class', '').split())
                and (id is None or n.attrs.get('id') == id)
                and (text is None or text.casefold() in n.text().casefold())]

    def walk(self):
        for child in self.children:
            if isinstance(child, Node):
                yield child
                yield from child.walk()

    def text(self):
        if self.tag in SKIP_TEXT or 'hidden' in self.attrs or self.attrs.get('aria-hidden') == 'true':
            return ''
        return clean(' '.join(c.text() if isinstance(c, Node) else c for c in self.children))

    def location(self):
        return f'<{self.tag}{"#" + self.attrs["id"] if self.attrs.get("id") else ""}> line {self.line}'


class DOM(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.root = Node('document')
        self.stack = [self.root]
        self.feed(html)
        self.close()

    def handle_starttag(self, tag, attrs):
        # Handle common optional closing tags used by WordPress fragments.
        if tag in {'li', 'p', 'tr', 'td', 'th', 'option'} and self.stack[-1].tag == tag:
            self.stack.pop()
        node = Node(tag, {k: v or '' for k, v in attrs}, self.stack[-1], line=self.getpos()[0])
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        self.stack[-1].children.append(data)


@dataclass
class Item:
    section: str
    text: str
    optional: bool = False
    tags: tuple = ()
    line: int = 0


def parse_checklist(path):
    """Preserve all checkbox rows, nested explanations, section order and source lines."""
    items, section, sub = [], '', ''
    for line_no, line in enumerate(path.read_text(encoding='utf-8-sig').splitlines(), 1):
        if line.startswith('## '):
            section, sub = line[3:].strip(), ''
        elif line.startswith('### '):
            sub = line[4:].strip()
        elif re.match(r'\s*- \[[ xX]\] ', line):
            text = re.sub(r'^\s*- \[[ xX]\]\s*', '', line)
            items.append(Item(section + (' → ' + sub if sub else ''), text,
                              'optional' in text.lower(), (), line_no))
        elif items and line.startswith('  ') and line.strip():
            items[-1].text += '\n' + line.strip()
    for item in items:
        item.tags = tuple(dict.fromkeys(re.findall(r'\b(?:per course|per topic|per country|fixed)\b',
                                                  item.text.lower())))
    return items


def fetch(url, timeout=15, limit=10_000_000):
    """GET only; retain TLS/proxy defaults, limit response size and isolate failures."""
    try:
        with urlopen(Request(url, headers={'User-Agent': USER_AGENT}), timeout=timeout) as response:
            data = response.read(limit + 1)
            if len(data) > limit:
                return None, response.status, response.url, 'Response exceeds size limit'
            return data, response.status, response.url, ''
    except HTTPError as exc:
        return None, exc.code, exc.url, f'HTTP {exc.code}'
    except (URLError, OSError, ValueError, TimeoutError) as exc:
        return None, None, url, str(exc)


def decode_cf(value):
    try:
        raw = bytes.fromhex(value)
        return bytes(b ^ raw[0] for b in raw[1:]).decode('utf-8') if len(raw) > 1 else ''
    except (ValueError, UnicodeError):
        return ''


class Audit:
    def __init__(self, html, source, kind=None, country=None, timeout=15,
                 link_check=True, check_images=False):
        self.html, self.source, self.timeout = html, source, timeout
        self.dom = DOM(html).root
        self.nodes = list(self.dom.walk())
        self.positions = {n: i for i, n in enumerate(self.nodes)}
        h1s = self.dom.find('h1')
        self.h1 = h1s[0].text() if h1s else ''
        probe = (self.h1 + ' ' + unquote(source).replace('-', ' ')).lower()
        self.kind = kind or ('lunchtalk' if 'lunch talk' in probe else
                             'customized' if re.search(r'customi[sz]ed corporate training', probe) else
                             'course' if 'training course' in probe else None)
        suffix = re.search(r'\bin (?:the )?(.+?)\.?$', self.h1, re.I)
        self.country = country or COUNTRIES.get(urlsplit(source).hostname, '') or (suffix[1] if suffix else 'Unknown')
        self.subject = re.split(r'\s+(?:Training Course|Lunch Talk)\s+in\s+', self.h1, flags=re.I)[0]
        # Scope content checks away from shared site header/footer, where identifiable.
        self.content = next((n for n in self.nodes if 'entry-content' in n.attrs.get('class', '').split()), None)
        self.content = self.content or next(iter(self.dom.find('main')), self.dom)
        self.content_nodes = list(self.content.walk())
        self.links = self.content.find('a')
        self.images = self.content.find('img')
        self.headings = [n for n in self.content_nodes if re.fullmatch(r'h[1-6]', n.tag)]
        self.link_check, self.check_images = link_check, check_images
        self.cache = {}
        self.section_matches = {}

    def get(self, url, limit=10_000_000):
        if (url, limit) not in self.cache:
            self.cache[url, limit] = fetch(url, self.timeout, limit)
        return self.cache[url, limit]

    def meta(self, key):
        return next((n.attrs.get('content', '') for n in self.dom.find('meta')
                     if n.attrs.get('name', n.attrs.get('property', '')).lower() == key), '')

    def section(self, section):
        if section in self.section_matches:
            return self.section_matches[section]
        name = re.sub(r'^\d+\.\s*', '', section)
        name = re.sub(r'\s*\(.*', '', name).lower()
        if name == 'hero':
            heading = next(iter(self.content.find('h1')), None)
        else:
            keys = [name]
            for prefix, aliases in SECTION_KEYWORDS.items():
                if name.startswith(prefix):
                    keys += aliases
            keys = [self.replace(k).lower() for k in keys]
            candidates = self.headings + [n for n in self.content_nodes
                                          if n.tag in {'p', 'span', 'div'} and len(n.text()) < 120]
            # Titles and text inside a grid of cards name items, not sections.
            candidates = [n for n in candidates if not self.in_card_grid(n)]
            scored = []
            for n in candidates:
                text = n.text().lower().strip(' .?!')
                score = max((1 if k == text else .9 if len(k) > 8 and k in text else
                             SequenceMatcher(None, k, text).ratio()) for k in keys)
                if score >= .72:
                    scored.append((score, -self.positions[n], n))
            heading = max(scored, key=lambda v: v[:2])[2] if scored else None
        self.section_matches[section] = heading
        return heading

    def in_card_grid(self, node):
        """True inside or around a grid of sibling cards (class card or *-card); a lone card can hold a section heading."""
        def is_card(n):
            return isinstance(n, Node) and any(re.search(r'(?:^|-)card$', c) for c in n.attrs.get('class', '').split())
        def grid_card(n):
            return is_card(n) and n.parent is not None and sum(map(is_card, n.parent.children)) > 1
        n = node
        while n is not None and n is not self.content:
            if grid_card(n):
                return True
            n = n.parent
        return any(map(grid_card, node.walk()))

    def replace(self, text):
        for key, value in {'Country': self.country, 'Course': self.subject, 'Topic': self.subject}.items():
            text = text.replace('[' + key + ']', value).replace('[' + key.lower() + ']', value)
        return text

    def scope(self, section):
        heading = self.section(section)
        if not heading:
            return None
        n = heading.parent
        while n and n is not self.content:
            if n.tag == 'section' or any(re.search(r'(?:^|[-_])(section|hero)(?:$|[-_])', c)
                                          for c in n.attrs.get('class', '').split()):
                return n
            n = n.parent
        # Heading-delimited fragment prevents counting the whole page as one section.
        start = self.positions[heading]
        rank = int(heading.tag[1]) if re.fullmatch(r'h[1-6]', heading.tag) else 2
        end = next((self.positions[n] for n in self.headings if self.positions[n] > start
                    and int(n.tag[1]) <= rank), len(self.nodes))
        fragment = Node('fragment')
        selected = set(self.nodes[start:end])
        fragment.children = [n for n in self.nodes[start:end] if n.parent not in selected]
        return fragment

    def check_h1(self):
        """Page setup: one H1, no duplicate IDs, correct page-name pattern."""
        problems = []
        h1s = self.dom.find('h1')
        if len(h1s) != 1:
            problems.append(f'Found {len(h1s)} H1 elements; expected 1')
        ids = Counter(n.attrs['id'] for n in self.nodes if 'id' in n.attrs)
        problems += [f'Duplicate id={key!r} ({count})' for key, count in ids.items() if count > 1]
        if self.kind and not re.fullmatch(PAGE_PATTERNS[self.kind].format(
                country=re.escape(self.country) if self.country != 'Unknown' else '.+'), self.h1):
            problems.append(f'H1 does not match page-name pattern: {self.h1!r}')
        return ('fail', '; '.join(problems)) if problems else ('pass', f'One H1: {self.h1!r}; IDs unique')

    def check_title(self):
        """SEO title equals H1; WordPress admin title and pixel width need review."""
        titles = self.dom.find('title')
        title = titles[0].text() if titles else ''
        if not title or title != self.h1:
            return 'fail', f'<title>={title!r}; H1={self.h1!r}'
        return 'review', 'HTML title equals H1. Confirm WordPress title and Yoast 600px width in admin.'

    def check_meta(self):
        """SEO description length and focus keyphrase when exposed in HTML."""
        description = self.meta('description')
        if not 120 <= len(description) <= 140:
            return 'fail', f'Meta description has {len(description)} characters; expected 120–140'
        phrase = self.meta('focus_keyphrase') or self.meta('yoast:focuskw')
        if not phrase:
            return 'review', f'Meta description: {len(description)} characters. Focus keyphrase not exposed; confirm in Yoast.'
        return ('pass', f'{len(description)} characters; contains {phrase!r}') if phrase.casefold() in description.casefold() else ('fail', f'Missing focus keyphrase {phrase!r} in meta description')

    def check_theme(self):
        """Build/page setup: possible theme title bar above the hero."""
        nodes = [n for n in self.nodes if THEME_CLASSES.intersection(n.attrs.get('class', '').split())]
        return ('review', 'Possible theme title bar (confirm CSS visibility): ' + ', '.join(n.location() for n in nodes)) if nodes else ('pass', 'No known theme title bar markup found')

    def check_embedded_navigation(self):
        """Build/page setup: navigation/footer embedded inside page content."""
        nodes = [n for n in self.content_nodes if n.tag in {'nav', 'footer'}]
        if self.content is self.dom:
            return 'review', 'Cannot isolate page content from shared site chrome; inspect navigation/footer placement.'
        return ('review', 'Confirm embedded navigation/footer: ' + ', '.join(n.location() for n in nodes)) if nodes else ('pass', 'No nav/footer within identified page content')

    def check_links(self):
        """Design/build links: new tabs, noopener, anchor targets, empty and JS links."""
        problems, notes = [], []
        ids = {n.attrs.get('id') for n in self.nodes}
        for a in self.links:
            href = a.attrs.get('href', '').strip()
            where = a.location()
            if '/cdn-cgi/l/email-protection' in href or a.attrs.get('data-cfemail'):
                decoded = decode_cf(a.attrs.get('data-cfemail') or href.partition('#')[2])
                notes.append(f'{where}: Cloudflare email {decoded or "could not decode"}')
                continue
            if not href or href == '#' or href.lower().startswith('javascript:'):
                problems.append(f'{where}: invalid href={href!r}')
            elif href.startswith('#'):
                if unquote(href[1:]) not in ids:
                    problems.append(f'{where}: missing target {href}')
                if a.attrs.get('target') == '_blank':
                    problems.append(f'{where}: in-page link opens new tab')
            elif urlsplit(href).scheme.lower() in {'mailto', 'tel'}:
                continue
            elif urlsplit(urljoin(self.source, href)).scheme in {'http', 'https'}:
                if a.attrs.get('target') != '_blank' or 'noopener' not in a.attrs.get('rel', '').lower().split():
                    problems.append(f'{where}: {href} requires target="_blank" and rel="noopener"')
        return ('fail' if problems else 'pass', '; '.join(problems + notes) or 'Page links have valid targets and tab settings')

    def check_http_links(self):
        """Final sweep: internal GET statuses, including redirects; switchable."""
        if not self.link_check:
            return 'manual', 'HTTP link checks disabled (--no-link-check).'
        base = urlsplit(self.source)
        if base.scheme not in {'http', 'https'}:
            return 'manual', 'Saved HTML: use a live URL for relative/internal HTTP checks.'
        urls = set()
        for a in self.links:
            href = a.attrs.get('href', '')
            if not href or href.startswith('#') or '/cdn-cgi/l/email-protection' in href:
                continue
            url = urldefrag(urljoin(self.source, href))[0]
            if urlsplit(url).scheme in {'http', 'https'} and urlsplit(url).netloc == base.netloc:
                urls.add(url)
        errors, redirects, uncertain = [], [], []
        for url in sorted(urls):
            _, status, final, error = self.get(url)
            if status and status >= 400:
                errors.append(f'{url}: HTTP {status}')
            elif error:
                uncertain.append(f'{url}: {error}')
            elif final != url:
                redirects.append(f'{url} → {final}')
        return ('fail' if errors else 'review' if redirects or uncertain else 'pass',
                f'GET checked {len(urls)} unique internal links. ' + '; '.join(errors + redirects + uncertain))

    def image_url(self, image):
        return image.attrs.get('data-src') or image.attrs.get('data-lazy-src') or image.attrs.get('src', '')

    def check_images_html(self):
        """Photos: alt, WebP URLs, CSS photo URLs, reuse and below-hero lazy loading."""
        problems, review = [], []
        hero = self.scope('1. Hero')
        hero_images = set(hero.find('img')) if hero else set()
        urls = Counter()
        for image in self.images:
            where, url = image.location(), self.image_url(image)
            if 'alt' not in image.attrs:
                problems.append(f'{where}: missing alt')
            elif not image.attrs['alt'].strip():
                review.append(f'{where}: empty alt; confirm decorative image')
            extension = Path(urlsplit(url).path).suffix.lower()
            if extension not in {'.webp', '.svg'}:
                review.append(f'{where}: cannot confirm WebP URL {url!r}')
            if extension in {'.jpg', '.jpeg', '.png', '.gif'}:
                problems.append(f'{where}: non-WebP raster image {url}')
            if url and extension != '.svg':
                urls[url] += 1
            if image not in hero_images and image.attrs.get('loading') != 'lazy':
                review.append(f'{where}: missing loading="lazy"; confirm location/lazy-loader')
        problems += [f'Photo reused {count} times: {url}' for url, count in urls.items() if count > 1]
        css = ' '.join(n.attrs.get('style', '') for n in self.nodes)
        css += ' '.join(''.join(c for c in n.children if isinstance(c, str)) for n in self.dom.find('style'))
        backgrounds = re.findall(r'url\(["\']?([^\s)"\']+\.(?:jpe?g|png|webp)(?:\?[^)"\']*)?)', css, re.I)
        review += [f'CSS photo URL (confirm photo vs decoration): {u}' for u in backgrounds]
        return ('fail' if problems else 'review' if review else 'pass',
                f'{len(self.images)} images inspected. ' + '; '.join(problems + review))

    def check_image_bytes(self):
        """Optional image validation: GET image bytes and check RIFF....WEBP signature."""
        if not self.check_images:
            return 'manual', 'Byte validation disabled; use --check-images to verify image files.'
        errors, uncertain, count = [], [], 0
        for url in sorted({self.image_url(i) for i in self.images}):
            if Path(urlsplit(url).path).suffix.lower() == '.svg':
                continue
            absolute = urljoin(self.source, url)
            if urlsplit(absolute).scheme not in {'http', 'https'}:
                uncertain.append(f'{url}: no absolute HTTP image URL')
                continue
            data, status, _, error = self.get(absolute)
            count += 1
            if error:
                uncertain.append(f'{absolute}: {error}')
            elif not (data[:4] == b'RIFF' and data[8:12] == b'WEBP'):
                errors.append(f'{absolute}: not a WebP RIFF signature')
        return ('fail' if errors else 'review' if uncertain else 'pass',
                f'{count} files downloaded (10 MB limit/file). ' + '; '.join(errors + uncertain))

    def check_social(self):
        """SEO: Open Graph and X images equal the hero image."""
        hero = self.scope('1. Hero')
        images = hero.find('img') if hero else []
        og, twitter = self.meta('og:image'), self.meta('twitter:image')
        if not og or not twitter:
            return 'fail', f'og:image={og!r}, twitter:image={twitter!r}; both required'
        if not images:
            return 'review', f'Social images present: {og}, {twitter}; hero image not identified'
        url = urljoin(self.source, self.image_url(images[0]))
        if any(urljoin(self.source, v) != url for v in (og, twitter)):
            return 'review', f'Hero candidate {url}; og:image={og}; twitter:image={twitter}; confirm WordPress size variants'
        return 'pass', f'Both social image URLs equal hero: {url}'

    def faq_scope(self):
        section = next((s for s in self.section_matches if 'Frequently asked' in s), 'Frequently asked questions')
        return self.scope(section)

    def check_faq(self):
        """FAQ: exactly ten questions, all closed initially; interaction requires browser."""
        scope = self.faq_scope()
        if not scope:
            return 'review', 'FAQ section not identified; inspect custom accordion markup. One-open-at-a-time needs browser testing.'
        questions = scope.find('summary')
        if not questions:
            questions = [n for n in scope.walk() if n.attrs.get('aria-expanded') is not None]
        if not questions:
            return 'review', 'No standard summary/aria-expanded question controls found; count questions manually.'
        opened = [n for n in scope.walk() if (n.tag == 'details' and 'open' in n.attrs)
                  or n.attrs.get('aria-expanded') == 'true'
                  or {'active', 'open', 'is-open'}.intersection(n.attrs.get('class', '').split())]
        if len(questions) != 10 or opened:
            return 'fail', f'Found {len(questions)} FAQ questions (expected 10); initially open: {", ".join(n.location() for n in opened) or "none"}'
        return 'review', 'Found exactly 10 questions, all closed in HTML. Confirm one open at a time in a browser.'

    def check_form(self):
        """Enquiry: expected field labels/types, consent, privacy, CAPTCHA and submit."""
        forms = self.content.find('form')
        if not forms:
            return 'review', 'No form element in HTML; check whether a plugin renders the form with JavaScript.'
        missing_by_form = []
        for form in forms:
            fields = form.find('input') + form.find('textarea') + form.find('select')
            labels = {n.attrs.get('for'): n.text() for n in form.find('label')}
            signatures = [' '.join([n.attrs.get(k, '') for k in ('name', 'type', 'placeholder', 'aria-label')] +
                                   [labels.get(n.attrs.get('id'), ''), n.parent.text() if n.parent and n.parent.tag == 'label' else '']).lower()
                          for n in fields]
            patterns = {'name': r'\bname\b', 'email': r'\bemail\b', 'contact number': r'phone|contact.number|\btel\b',
                        'enquiry/message': r'enquiry|message|textarea', 'consent': r'consent|agree|privacy'}
            missing = [key for key, pattern in patterns.items() if not any(re.search(pattern, s) for s in signatures)]
            if not any(n.attrs.get('type') == 'checkbox' for n in fields):
                missing.append('consent checkbox')
            if not any('privacy' in a.attrs.get('href', '').lower() for a in form.find('a')):
                missing.append('privacy policy link')
            if not any(n.tag == 'button' and n.attrs.get('type', 'submit') == 'submit' or n.attrs.get('type') == 'submit'
                       for n in form.walk()):
                missing.append('submit button')
            missing_by_form.append((form, missing))
        form, missing = min(missing_by_form, key=lambda pair: len(pair[1]))
        if missing:
            return 'review', f'{form.location()}: fields not identifiable: {", ".join(missing)}; confirm plugin markup.'
        return 'review', f'{form.location()}: expected field signatures, consent checkbox, privacy link and submit found. Confirm labels, required settings and notification inbox manually.'

    def check_captcha(self):
        """Enquiry settings: CAPTCHA markup or loader, without submitting the form."""
        found = any(re.search(r'recaptcha|hcaptcha|forminator.*captcha', str(n.attrs), re.I) for n in self.nodes)
        return 'review', ('CAPTCHA marker found; verify it renders and is enforced.' if found else
                          'No CAPTCHA marker found; confirm plugin/live rendering and enforcement.')

    def check_ajax(self):
        """Enquiry settings: AJAX flags where explicitly exposed by form markup."""
        forms = self.content.find('form')
        for n in forms:
            attrs = n.attrs
            if any('ajax' in k.lower() and str(v).lower() in {'false', '0', 'off'} for k, v in attrs.items()):
                return 'fail', f'{n.location()}: AJAX explicitly disabled'
            if 'wpforms-ajax-form' in attrs.get('class', '').split() or any('ajax' in k and str(v).lower() in {'true', '1', 'on'} for k, v in attrs.items()):
                return 'review', f'{n.location()}: AJAX enabled in markup; verify behaviour without duplicate submissions.'
        return 'manual', 'AJAX setting not exposed. Inspect plugin settings and test in an authorised browser session.'

    def check_counters(self):
        """Enquiry settings: no visible zero-of-max-characters counters."""
        found = re.findall(r'\b0\s+of\s+\d+\s+max\s+characters\b', self.content.text(), re.I)
        return ('fail', 'Counter found: ' + '; '.join(found)) if found else ('pass', 'No initial character counters in HTML text')

    def check_text(self):
        """Final text sweep: placeholders, lunch fees/durations, hybrid and contacts."""
        text = self.content.text()
        problems, notes = [], []
        for pattern in BANNED_WORDS:
            for match in re.finditer(pattern, text, re.I):
                problems.append(text[max(0, match.start()-35):match.end()+50])
        for match in re.finditer(r'\bhybrid\b', text, re.I):
            notes.append('Hybrid (allowed for lunch talks): ' + text[max(0, match.start()-25):match.end()+35])
        if self.kind == 'lunchtalk':
            for match in re.finditer(r'(\d+)(?:\s*[–−-]\s*(\d+))?\s*(minutes?|mins?|hours?)\b', text, re.I):
                values = [int(v) for v in match.groups()[:2] if v]
                if match[3].lower().startswith('hour'):
                    values = [v*60 for v in values]
                if any(v < 30 or v > 120 for v in values):
                    problems.append('Out-of-range lunch duration: ' + match[0])
            for match in re.finditer(r'\b(pric(?:e|es|ing)|fees?)\b|(?:SGD|AED|USD|\$)\s*\d+', text, re.I):
                notes.append('Possible lunch pricing (confirm context): ' + text[max(0, match.start()-20):match.end()+35])
        contacts = re.findall(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|\+\d[\d ()-]{6,}\d', text)
        contacts += [decode_cf(n.attrs.get('data-cfemail') or n.attrs.get('href', '').partition('#')[2])
                     for n in self.content_nodes if n.attrs.get('data-cfemail') or '/cdn-cgi/l/email-protection#' in n.attrs.get('href', '')]
        notes.append('Compare contacts with Contact Us: ' + ', '.join(sorted(set(filter(None, contacts)))))
        return ('fail' if problems else 'review', '; '.join(problems + notes))

    def check_hero_buttons(self):
        """Hero: exactly two CTA links, own enquiry form and a listing page."""
        scope = self.scope('1. Hero')
        if not scope:
            return 'review', 'Hero not identified; inspect the two CTA destinations manually.'
        links = scope.find('a')
        candidates = [a for a in links if re.search(r'btn|button', a.attrs.get('class', ''), re.I) or a.attrs.get('role') == 'button']
        if not candidates:
            candidates = links
        if len(candidates) != 2:
            return 'review', f'Found {len(candidates)} hero link/button candidates; expected 2. Confirm hero boundary.'
        form_links = [a for a in candidates if a.attrs.get('href', '').startswith('#') and a.attrs.get('href') != '#']
        targets = [self.dom.find(id=unquote(a.attrs['href'][1:])) for a in form_links]
        has_form = any(nodes and (nodes[0].tag == 'form' or nodes[0].find('form')) for nodes in targets)
        listing = [a.attrs.get('href') for a in candidates if not a.attrs.get('href', '').startswith('#')]
        return 'review', f'2 hero CTA candidates; own form target confirmed={has_form}; listing candidates={listing}. Confirm listing page purpose.'

    def check_card_bands(self):
        """Design: CTA buttons outside hero/closing CTA need a card band."""
        suspects = []
        for a in self.links:
            if not re.search(r'btn|button', a.attrs.get('class', ''), re.I):
                continue
            n, ancestry = a.parent, []
            while n and n is not self.content:
                ancestry.append(n)
                n = n.parent
            signatures = ' '.join(n.attrs.get('class', '') + ' ' + n.attrs.get('id', '') for n in ancestry)
            if not re.search(r'hero|cta|card|band|form', signatures, re.I):
                suspects.append(a.location())
        return 'review', ('Buttons without identifiable band/hero/CTA ancestor: ' + ', '.join(suspects) if suspects else
                          'No obvious unbanded buttons; confirm icon, heading, text and section placement visually.')

    def check_separation(self):
        """Design: at least one section between closing CTA and enquiry form."""
        cta_name = '12. Shape the right programme for your team' if self.kind == 'customized' else 'Take the next step'
        form_name = '4. Enquiry form' if self.kind == 'customized' else 'Get in touch'
        cta, form = self.scope(cta_name), self.scope(form_name)
        sections = [n for n in self.content_nodes if n.tag == 'section']
        if cta in sections and form in sections:
            gap = abs(sections.index(cta) - sections.index(form)) - 1
            return ('fail' if gap < 1 else 'review', f'{gap} section elements between CTA and form; confirm semantic section boundaries.')
        return 'manual', 'Identify closing CTA and enquiry form; ensure at least one content section lies between them.'

    def check_reviews(self):
        """Reviews: three quotes/logos; flag stars and dates, confirm authenticity manually."""
        name = 'What clients say' if self.kind == 'customized' else 'Reviews'
        scope = self.scope(name)
        if not scope:
            return 'review', 'Reviews region not identified; count three reviews and verify company/logo and source.'
        quotes = scope.find('blockquote')
        if not quotes:
            quotes = [n for n in scope.walk() if any(c in {'review-card', 'testimonial', 'testimonial-card'} for c in n.attrs.get('class', '').split())]
        problems = []
        if quotes and len(quotes) != 3:
            problems.append(f'Found {len(quotes)} review cards; expected 3')
        for n in scope.walk():
            if '★' in n.text() or re.search(r'star|rating', n.attrs.get('class', ''), re.I):
                problems.append(f'{n.location()}: possible star rating')
                break
        dates = re.findall(r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b|\b20\d{2}-\d{2}(?:-\d{2})?', scope.text(), re.I)
        problems += ['Review date: ' + d for d in dates]
        return ('fail' if problems else 'review', '; '.join(problems) or
                f'{len(quotes)} review candidates, {len(scope.find("img"))} logo/image candidates. Verify company names, matching logos, no course name shown, and verbatim source.')

    def check_count(self, item):
        """Content counts: scope list/card candidates to the matched numbered section."""
        scope = self.scope(item.section)
        if not scope:
            return 'review', 'Section not confidently identified; count the required items manually.'
        text = plain(item.text).lower()
        if 'duration options' in text:
            values = {int(m) for m in re.findall(r'\b(\d+)\s*(?:minutes?|mins?)\b', scope.text(), re.I)}
            return ('review' if values == DURATION_OPTIONS else 'fail' if values else 'review',
                    f'Duration values found: {sorted(values)}; expected {sorted(DURATION_OPTIONS)}. Confirm five distinct options and their descriptions.')
        required = required_count(text)
        match = re.search(r'\b(\d+)\s+(?:numbered )?(?:cards|points|steps|options|elements|benefits|reasons|formats|resources|promises|quick facts|facts|example quotes|proof points)\b', text)
        required = required or (int(match[1]) if match else None)
        if required is None:
            return 'manual', 'Count and compare the content with the checklist in the rendered section.'
        lists = [n for n in scope.walk() if n.tag in {'ul', 'ol'}]
        counts = [len([c for c in n.children if isinstance(c, Node) and c.tag == 'li']) for n in lists]
        cards = [n for n in scope.walk() if any(c in {'card', 'module-card', 'topic-card', 'price-card'} for c in n.attrs.get('class', '').split())]
        if cards:
            counts.append(len(cards))
        # One flat list or one explicit card collection provides a reliable count.
        # More than one representation can be responsive duplicates or sub-lists.
        if len(counts) == 1 and counts[0] != required:
            return 'fail', f'Found {counts[0]} items in the matched section; expected {required}. Section candidate: {self.section(item.section).text()!r}'
        return 'review', f'Expected {required}; list/card candidate counts={counts or "unknown"}. ' + ('A count matches; verify item identity and required subcontent.' if required in counts else 'Confirm custom markup and count manually before treating as a failure.')

    def check_tiles(self):
        """Top six/category tiles: SVG icons, no raster photographs."""
        section = 'What does your team need to strengthen?' if self.kind == 'customized' else 'Top 6 corporate training courses'
        scope = self.scope(section)
        if not scope:
            return 'review', 'Tile section not identified. Confirm SVG icons and no photo tiles.'
        rasters = [self.image_url(n) for n in scope.find('img') if not urlsplit(self.image_url(n)).path.lower().endswith('.svg')]
        return 'review', f'{len(scope.find("svg"))} inline SVGs; raster/image candidates={rasters}. Confirm only SVGs are used on tiles.'

    def check_agenda(self):
        """Course agenda: two days, break time consistency and curriculum session names."""
        if self.kind != 'course':
            return 'na', 'Two-day agenda applies to course pages only.'
        agenda, curriculum = self.scope('Two-day course agenda'), self.scope('Course curriculum')
        if not agenda:
            return 'review', 'Agenda not identified. Compare both day timetables, breaks and curriculum manually.'
        text = agenda.text()
        days = re.split(r'\bDay\s*([12])\b', text, flags=re.I)
        if len(days) < 5:
            return 'review', 'Cannot split Day 1 and Day 2 markup; compare 09:00–17:00 sessions and breaks manually.'
        day_text = {days[i]: days[i+1] for i in range(1, len(days)-1, 2)}
        notes = []
        for day, body in day_text.items():
            times = re.findall(r'\b\d{1,2}:\d{2}\b', body)
            notes.append(f'Day {day} times: {times}')
        breaks = []
        for body in day_text.values():
            breaks.append(re.findall(r'(\d{1,2}:\d{2}\s*[–-]\s*\d{1,2}:\d{2})\s*(?:Morning break|Lunch(?: break)?|Afternoon break)', body, re.I))
        if len(breaks) == 2 and all(len(b) == 3 for b in breaks) and breaks[0] != breaks[1]:
            return 'fail', 'Break times differ between days: ' + repr(breaks)
        modules = curriculum.find('li') if curriculum else []
        missing = [n.text() for n in modules if clean(re.sub(r'^\d+[.)\s]+', '', n.text())).casefold() not in text.casefold()]
        return 'review', '; '.join(notes) + f'; unmatched module candidates={missing}. Confirm named sessions, all three breaks, opening/closing and action planning.'

    def check_group(self):
        """Lunch/course group size: flag explicit ranges outside 1–25 participants."""
        text = self.content.text()
        ranges = re.findall(r'\b(\d+)\s*(?:[–-]|to)\s*(\d+)\s*(?:participants|people|attendees)\b', text, re.I)
        bad = [(a, b) for a, b in ranges if int(a) < 1 or int(b) > 25]
        return ('fail', f'Group ranges outside 1–25: {bad}') if bad else ('review', f'Group ranges found: {ranges}; confirm minimum 1 and maximum 25 per session.')


# Routing stays explicit and conservative: compound editorial/visual requirements never
# become a Pass merely because a keyword or a matching count exists.
ITEM_ROUTES = [
    (r'one h1|no duplicate id|only h1|only.*h1', 'check_h1'),
    (r'seo title|wordpress page title', 'check_title'),
    (r'focus keyphrase|meta description', 'check_meta'),
    (r'facebook and x image', 'check_social'),
    (r'title bar', 'check_theme'),
    (r'no menu bar', 'check_embedded_navigation'),
    (r'links and cards that go', 'check_links'),
    (r'faqs:|10 (?:numbered )?questions|faqs all closed', 'check_faq'),
    (r'buttons outside', 'check_card_bands'),
    (r'at least one section between', 'check_separation'),
    (r'photos are real images|every image has alt|no photo is used twice|alt text describes', 'check_images_html'),
    (r'^captcha on', 'check_captcha'),
    (r'^ajax submission', 'check_ajax'),
    (r'max characters', 'check_counters'),
    (r'^enquiry form:', 'check_form'),
    (r'^2 buttons:', 'check_hero_buttons'),
    (r'^3 real reviews', 'check_reviews'),
    (r'breaks on both days|session names match|modules match|day [12] timetable', 'check_agenda'),
    (r'search the page text|contact details', 'check_text'),
]


def route(item):
    text = plain(item.text).lower()
    for pattern, method in ITEM_ROUTES:
        if re.search(pattern, text):
            return method
    if required_count(text) is not None or re.match(r'\d+ (?:numbered )?(?:cards|points|steps|options|elements|benefits|reasons|formats|resources|promises|quick facts|facts|example quotes|proof points)', text):
        return 'check_count'
    return None


def manual_item(audit, item):
    """Unobservable checklist details: report evidence without claiming completion."""
    text = plain(item.text)
    if item.optional:
        scope = audit.scope(item.section) if re.match(r'\d+\.', item.section) else None
        if scope and 'image' in text.lower() and not scope.find('img'):
            return 'na', 'Optional image not present in the matched section.'
        return 'manual', 'Optional: if included, check this requirement visually; otherwise mark N/A after inspection.'
    if re.match(r'\d+\.', item.section):
        heading = audit.section(item.section)
        return 'review', (f'Candidate {heading.location()}: {heading.text()!r}. Verify: {text}' if heading else
                          'Section not identified by heading/label; inspect for alternate wording and verify this item.')
    return 'manual', 'Inspect the rendered page, WordPress settings or approved source: ' + text


def run_audit(audit, items):
    rows = []
    numbered = list(dict.fromkeys(i.section for i in items if re.match(r'\d+\.', i.section)))
    # Precompute matches before FAQ checks; never silently omit a section.
    for section in numbered:
        audit.section(section)
    for item in items:
        method = route(item)
        if method:
            function = getattr(audit, method)
            status, evidence = function(item) if method == 'check_count' else function()
            # Most checklist rows combine observable and editorial requirements.
            if status == 'pass' and method in {'check_h1', 'check_images_html'} and (
                    'only h1' in plain(item.text).lower() or 'alt text describes' in plain(item.text).lower()
                    or 'photos are real' in plain(item.text).lower() or 'console' in item.text):
                status, evidence = 'review', evidence + '; confirm remaining wording/visual/console requirements manually.'
        else:
            status, evidence = manual_item(audit, item)
        rows.append({'section': item.section, 'item': item.text, 'optional': item.optional,
                     'tags': ', '.join(item.tags), 'status': status, 'evidence': evidence,
                     'source_line': item.line})
    extra = [('HTML structure and page name', 'check_h1'), ('Title equality', 'check_title'),
             ('Meta description', 'check_meta'), ('Social images', 'check_social'),
             ('Link attributes and anchors', 'check_links'), ('Internal HTTP links', 'check_http_links'),
             ('Image markup and URLs', 'check_images_html'), ('Image file signatures', 'check_image_bytes'),
             ('FAQ structure', 'check_faq'), ('Review markup', 'check_reviews'),
             ('Enquiry fields', 'check_form'), ('CAPTCHA', 'check_captcha'), ('AJAX', 'check_ajax'),
             ('Character counters', 'check_counters'), ('Hero buttons', 'check_hero_buttons'),
             ('Button card bands', 'check_card_bands'), ('CTA/form separation', 'check_separation'),
             ('Placeholders and contact inventory', 'check_text'), ('Group size', 'check_group'),
             ('Agenda and curriculum', 'check_agenda')]
    if audit.kind != 'lunchtalk':
        extra.append(('SVG topic tiles', 'check_tiles'))
    for title, method in extra:
        status, evidence = getattr(audit, method)()
        rows.append({'section': 'Additional HTML diagnostics', 'item': title, 'optional': False,
                     'tags': '', 'status': status, 'evidence': evidence, 'source_line': ''})
    found = [(s, audit.section(s)) for s in numbered]
    positions = [audit.positions[n] for _, n in found if n]
    order = ' → '.join(f'{s}: {n.location() if n else "NOT IDENTIFIED"}' for s, n in found)
    rows.append({'section': 'Additional HTML diagnostics', 'item': 'Section presence and order',
                 'optional': False, 'tags': '', 'status': 'review', 'source_line': '',
                 'evidence': ('Candidate order matches checklist. ' if positions == sorted(positions) and len(set(positions)) == len(positions) else 'Candidate sections overlap or appear out of order. ') + order + '. Confirm headings, small labels, intros and unmatched sections manually.'})
    return rows


def browser_audit(source, timeout):
    """Optional read-only rendering checks; never submit forms or click arbitrary links."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return [('manual', 'Playwright not installed. Run python -m pip install playwright and python -m playwright install chromium.')]
    results = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
            url = source if urlsplit(source).scheme in {'http', 'https'} else Path(source).resolve().as_uri()
            for width in WIDTHS:
                page.set_viewport_size({'width': width, 'height': 1000})
                page.goto(url, wait_until='networkidle', timeout=timeout*1000)
                data = page.evaluate('''() => {
                  const visible = e => !!(e.getClientRects().length && getComputedStyle(e).visibility !== 'hidden');
                  const cards = [...document.querySelectorAll('[class~="card"], [class$="-card"]')].filter(visible);
                  const tiny = [...document.querySelectorAll('main p, main a, main span, .entry-content p')]
                    .filter(e => visible(e) && e.textContent.trim() && parseFloat(getComputedStyle(e).fontSize)<12);
                  const clipped = cards.filter(e => e.scrollHeight > e.clientHeight+2 && ['hidden','clip'].includes(getComputedStyle(e).overflowY));
                  const rows = {};
                  for (const c of cards) {const r=c.getBoundingClientRect(); const k=Math.round(r.top); (rows[k]??=[]).push(r.height);}
                  const uneven=Object.values(rows).filter(r=>r.length>1 && Math.max(...r)-Math.min(...r)>2).length;
                  const hero=document.querySelector('.hero img, [class$="-hero"] img');
                  const panels=[...document.querySelectorAll('.photo-panel img, .big-photo img')];
                  return {overflow:document.documentElement.scrollWidth>innerWidth+1,
                    tiny:tiny.length,clipped:clipped.length,uneven,
                    heroVisible:hero ? visible(hero):null,
                    visiblePanels:panels.filter(visible).length,panelCount:panels.length};
                }''')
                failed = data['overflow'] or data['tiny'] or data['clipped'] or data['uneven']
                failed = failed or (width <= 1279 and data['heroVisible'] is True) or (width <= 1024 and data['visiblePanels'])
                results.append(('fail' if failed else 'review', f'{width}px: {json.dumps(data)}. Selectors are heuristic; verify unrecognised cards/photos, hero overlay text and decorations.'))
            # Native details only. Do not click anchors, buttons or form controls.
            details = page.locator('details:has(> summary)')
            if details.count() >= 2:
                for i in range(details.count()):
                    details.nth(i).evaluate('(e) => {e.open=false}')
                details.nth(0).locator('summary').click()
                details.nth(1).locator('summary').click()
                opened = page.locator('details[open]').count()
                results.append(('pass' if opened == 1 else 'fail', f'Native details interaction: {opened} open after two clicks. Confirm these are the FAQ controls.'))
            else:
                results.append(('manual', 'Custom FAQ interaction not tested; click two questions and confirm only the second remains open.'))
            results.append(('fail' if errors else 'pass', f'Browser console/page errors: {errors}'))
            browser.close()
    except Exception as exc:
        results.append(('review', f'Browser checks incomplete: {exc}'))
    return results


def cell(text):
    return str(text).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('|', '\\|').replace('\n', '<br>')


def write_report(path, audit, rows):
    counts = Counter(r['status'] for r in rows)
    lines = ['# Knowles page checklist report', '', f'- Source: {cell(audit.source)}',
             f'- Page type: {audit.kind}', f'- Country: {cell(audit.country)}',
             f'- Generated: {datetime.now(timezone.utc).isoformat()} (UTC)',
             '- Counts: ' + ', '.join(f'{label}: {counts[key]}' for key, label in STATUSES.items()), '',
             'Static matches are evidence, not approval to publish. Checklist text is treated as data; no website changes or form submissions are made.', '',
             '## Problems to fix', '']
    problems = [r for status in ('fail', 'review') for r in rows if r['status'] == status]
    lines += [f'- {STATUSES[r["status"]]} — **{cell(r["section"])} / {cell(plain(r["item"]))}**: {cell(r["evidence"])}' for r in problems] or ['None detected automatically; complete all manual checks.']
    lines += ['', '## Full checklist (original order)', '', '| Section | Checklist item | Optional | Tags | Status | Evidence |',
              '| --- | --- | --- | --- | --- | --- |']
    lines += ['| ' + ' | '.join(cell(v) for v in [r['section'], r['item'], 'yes' if r['optional'] else 'no', r['tags'], STATUSES[r['status']], r['evidence']]) + ' |' for r in rows]
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return counts


def write_coverage(folder):
    """Generate a per-item handling table from the same routing used by the auditor."""
    lines = ['# Checklist coverage', '', 'Generated with `python knowles_page_checker.py --coverage CHECKLIST_COVERAGE.md`.', '',
             'Automatic means a static subcheck is available; compound requirements may still return Review or Manual. Additional diagnostics always run, including links, images, forms, counts, text and section order.', '',
             '| Type / source line | Section | Item | Handling |', '| --- | --- | --- | --- |']
    for kind, filename in CHECKLIST_FILES.items():
        for item in parse_checklist(folder / filename):
            method = route(item)
            handling = f'Automatic / review: {method}' if method else 'Review: section/content evidence' if re.match(r'\d+\.', item.section) else 'Manual: rendered page / admin / source'
            if item.optional:
                handling += '; optional, N/A only when absence is established'
            lines.append('| ' + ' | '.join(cell(v) for v in [f'{kind}:{item.line}', item.section, item.text, handling]) + ' |')
    return '\n'.join(lines) + '\n'


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', nargs='?', help='Live http(s) URL or UTF-8 saved HTML file')
    parser.add_argument('--type', choices=CHECKLIST_FILES)
    parser.add_argument('--country')
    parser.add_argument('--out', type=Path, default=Path('report.md'))
    parser.add_argument('--csv', nargs='?', const='', metavar='PATH', help='Also write CSV (default: report basename.csv)')
    parser.add_argument('--no-link-check', action='store_true')
    parser.add_argument('--check-images', action='store_true')
    parser.add_argument('--browser', action='store_true')
    parser.add_argument('--timeout', type=int, default=15, help='Per-request timeout in seconds (default: 15)')
    parser.add_argument('--coverage', type=Path, help='Write the per-checklist-item coverage table and exit')
    args = parser.parse_args(argv)
    if sys.version_info < (3, 12):
        parser.error('Python 3.12+ is required')
    if args.timeout < 1:
        parser.error('--timeout must be at least 1')
    folder = Path(__file__).resolve().parent / 'checklists'
    try:
        if args.coverage:
            args.coverage.write_text(write_coverage(folder), encoding='utf-8')
            print(f'Coverage table: {args.coverage}')
            return 0
        if not args.source:
            parser.error('Provide a URL or saved HTML file')
        source = args.source
        if urlsplit(source).scheme in {'http', 'https'}:
            data, _, final, error = fetch(source, args.timeout)
            if error:
                print(f'Unable to read page: {error}', file=sys.stderr)
                return 2
            source = final
            # WordPress is normally UTF-8; respect a declared HTML charset.
            charset = re.search(br'charset=["\']?([\w-]+)', data[:4096], re.I)
            html = data.decode(charset[1].decode('ascii') if charset else 'utf-8', errors='replace')
        else:
            html = Path(source).read_text(encoding='utf-8-sig')
        audit = Audit(html, source, args.type, args.country, args.timeout, not args.no_link_check, args.check_images)
        if not audit.kind:
            parser.error('Cannot detect page type from H1/URL; provide --type course|lunchtalk|customized')
        print(f'Page type: {audit.kind}; country: {audit.country}; H1: {audit.h1 or "missing"}')
        items = parse_checklist(folder / CHECKLIST_FILES[audit.kind])
        rows = run_audit(audit, items)
        if args.browser:
            for status, evidence in browser_audit(source, args.timeout):
                rows.append(dict(section='Optional browser checks', item='Rendered behaviour', optional=True,
                                 tags='', status=status, evidence=evidence, source_line=''))
        output_paths = [args.out]
        csv_path = Path(args.csv) if args.csv else args.out.with_suffix('.csv')
        if args.csv is not None:
            output_paths.append(csv_path)
        protected = [Path(__file__).resolve(), *(folder / f for f in CHECKLIST_FILES.values())]
        if urlsplit(source).scheme not in {'http', 'https'}:
            protected.append(Path(source).resolve())
        if any(p.resolve() in protected for p in output_paths) or len({p.resolve() for p in output_paths}) != len(output_paths):
            parser.error('Report paths must be distinct and must not overwrite input/script/checklists')
        counts = write_report(args.out, audit, rows)
        if args.csv is not None:
            with csv_path.open('w', newline='', encoding='utf-8-sig') as stream:
                writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows({**r, 'status': STATUSES[r['status']]} for r in rows)
            print(f'CSV: {csv_path}')
        print(f'{len(items)} checklist items; {len(rows)-len(items)} diagnostics. ' + ', '.join(f'{STATUSES[k]}: {counts[k]}' for k in STATUSES))
        print(f'Report: {args.out}')
        return 1 if counts['fail'] else 0
    except (OSError, ValueError, LookupError) as exc:
        print(f'Cannot complete audit: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    # Windows pipes default to a legacy code page that cannot print the status icons.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8', errors='replace')
    raise SystemExit(main())
