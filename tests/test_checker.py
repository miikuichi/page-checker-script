import csv
import contextlib
import io
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import knowles_page_checker as k

ROOT = Path(k.__file__).parent


def html(kind='course', faq=10, opened=False):
    title = {'course': 'Listening Training Course in UAE',
             'lunchtalk': 'Listening Lunch Talk in UAE',
             'customized': 'Customized Corporate Training in UAE'}[kind]
    return f'''<!doctype html><html><head><title>{title}</title>
    <meta name="description" content="{'a'*125}">
    <meta property="og:image" content="/hero.webp"><meta name="twitter:image" content="/hero.webp">
    </head><body><header><nav>Site navigation</nav></header><main class="entry-content">
    <section class="hero"><h1>{title}</h1><img src="/hero.webp" alt="Team">
    <a class="button" href="#enquiry">Enquire</a>
    <a class="button" href="/courses" target="_blank" rel="noopener">Courses</a></section>
    <section><h2>Frequently asked questions</h2>
    {''.join('<details'+(' open' if opened and i == 0 else '')+'><summary>Question '+str(i)+'</summary><p>Answer</p></details>' for i in range(faq))}
    </section><section id="enquiry"><h2>Get in touch</h2><form data-ajax="true">
    <label for="name">Name</label><input id="name" name="name">
    <input type="email"><input type="tel"><textarea name="message"></textarea>
    <label><input type="checkbox" name="consent">I consent</label>
    <a href="/privacy" target="_blank" rel="noopener">Privacy</a><button>Send</button>
    <div class="g-recaptcha"></div></form></section></main><footer>Site footer</footer></body></html>'''


class CheckerTests(unittest.TestCase):
    def audit(self, source=None, **kwargs):
        return k.Audit(source or html(), 'https://ae.knowlesti.com/listening/', **kwargs)

    def test_all_checkboxes_preserved(self):
        for filename in k.CHECKLIST_FILES.values():
            path = ROOT / 'checklists' / filename
            items = k.parse_checklist(path)
            self.assertEqual(len(items), sum('- [ ] ' in line for line in path.read_text(encoding='utf-8').splitlines()))
            self.assertGreater(len(items), 100)
            self.assertTrue(any(i.optional for i in items))
            self.assertTrue(any('per country' in i.tags for i in items))
            rows = k.run_audit(self.audit(link_check=False), items)
            self.assertEqual([i.text for i in items], [r['item'] for r in rows[:len(items)]])

    def test_detection(self):
        for kind in k.CHECKLIST_FILES:
            audit = self.audit(html(kind))
            self.assertEqual(audit.kind, kind)
            self.assertEqual(audit.country, 'UAE')
            self.assertEqual(audit.check_h1()[0], 'pass')

    def test_dom_visible_text_and_parent(self):
        dom = k.DOM('<main>yes<script>bad</script><svg>bad</svg><style>bad</style><template>bad</template><b hidden>bad</b><span class="label" id="a">okay</span></main>').root
        self.assertEqual(dom.text(), 'yes okay')
        self.assertEqual(dom.find(cls='label', id='a')[0].parent.tag, 'main')

    def test_duplicate_h1_and_ids(self):
        audit = self.audit(html() + '<h1 id="a">Bad</h1><div id="a"></div>')
        status, evidence = audit.check_h1()
        self.assertEqual(status, 'fail')
        self.assertIn('Duplicate', evidence)
        self.assertIn('2 H1', evidence)

    def test_count_rule_needs_a_number(self):
        faq = k.Item('23. Frequently asked questions', 'Answers about the main focus, who it suits and learning outcomes are written for the course')
        outcomes = k.Item('5. What participants will be better able to do', '**6 learning outcomes**, each with an icon')
        self.assertNotEqual(k.route(faq), 'check_count')
        self.assertEqual(k.route(outcomes), 'check_count')

    def test_card_grid_text_is_not_a_section(self):
        cards = ('<section><h2>How Participants Learn</h2><div class="grid">'
                 '<div class="card"><h3>Learn</h3><p>Short input on the concept and why it matters.</p></div>'
                 '<div class="card"><h3>Flexible formats</h3><p>Onsite or virtual.</p></div></div></section>')
        audit = self.audit(html().replace('</main>', cards + '</main>'))
        self.assertIsNone(audit.section('3. Why it matters in [Country]'))
        self.assertIsNone(audit.section('16. Choose your training format'))
        audit = self.audit(html().replace('</main>', cards + '<section><h2>Why it matters in UAE</h2></section>'
                                          '<div class="card"><h2>Pricing and investment</h2></div></main>'))
        self.assertEqual(audit.section('3. Why it matters in [Country]').text(), 'Why it matters in UAE')
        self.assertEqual(audit.section('20. Pricing and investment').text(), 'Pricing and investment')

    def test_curriculum_count(self):
        audit = self.audit(html().replace('</main>', '<section><h2>Course curriculum</h2><ol>' + '<li>Module</li>'*9 + '</ol></section></main>'))
        item = k.Item('8. Course curriculum', '**10 numbered modules** with short titles')
        self.assertEqual(audit.check_count(item)[0], 'fail')

    def test_boolean_attributes_do_not_crash(self):
        audit = self.audit(html().replace('</main>', '<a href class>Empty</a></main>'))
        self.assertEqual(audit.check_links()[0], 'fail')

    def test_faq_count_and_open(self):
        self.assertEqual(self.audit().check_faq()[0], 'review')
        self.assertEqual(self.audit(html(faq=12)).check_faq()[0], 'fail')
        self.assertEqual(self.audit(html(opened=True)).check_faq()[0], 'fail')

    def test_link_errors(self):
        audit = self.audit(html().replace('href="#enquiry"', 'href="#missing" target="_blank"').replace('rel="noopener"', 'rel="noreferrer"'))
        result = audit.check_links()
        self.assertEqual(result[0], 'fail')
        self.assertIn('missing target', result[1])
        self.assertIn('noopener', result[1])
        self.assertIn('in-page', result[1])

    def test_shared_navigation_is_excluded(self):
        self.assertEqual(self.audit().check_embedded_navigation()[0], 'pass')

    def test_cloudflare(self):
        email, key = 'person@example.com', 23
        encoded = bytes([key] + [ord(c) ^ key for c in email]).hex()
        self.assertEqual(k.decode_cf(encoded), email)
        self.assertEqual(k.decode_cf('zz'), '')
        audit = self.audit(html().replace('</main>', f'<a href="/cdn-cgi/l/email-protection#{encoded}">email</a></main>'))
        self.assertNotEqual(audit.check_links()[0], 'fail')
        self.assertIn(email, audit.check_text()[1])

    def test_meta_and_social(self):
        self.assertEqual(self.audit().check_meta()[0], 'review')
        self.assertEqual(self.audit(html().replace('a'*125, 'too short')).check_meta()[0], 'fail')
        self.assertEqual(self.audit().check_social()[0], 'pass')
        self.assertEqual(self.audit(html().replace('property="og:image"', 'property="other"')).check_social()[0], 'fail')

    def test_image_failures(self):
        audit = self.audit(html().replace('src="/hero.webp" alt="Team"', 'src="/hero.jpg"'))
        result = audit.check_images_html()
        self.assertEqual(result[0], 'fail')
        self.assertIn('missing alt', result[1])
        self.assertIn('non-WebP', result[1])

    def test_image_signature(self):
        audit = self.audit(check_images=True)
        with patch.object(audit, 'get', return_value=(b'RIFFxxxxWEBPpayload', 200, '', '')):
            self.assertEqual(audit.check_image_bytes()[0], 'pass')
        with patch.object(audit, 'get', return_value=(b'<html>oops</html>', 200, '', '')):
            self.assertEqual(audit.check_image_bytes()[0], 'fail')

    def test_http_failures_redirects_and_dedup(self):
        audit = self.audit()
        def get(url):
            return None, 404 if url.endswith('privacy') else 200, url, ''
        with patch.object(audit, 'get', side_effect=get):
            self.assertEqual(audit.check_http_links()[0], 'fail')
        with patch.object(audit, 'get', side_effect=lambda u: (b'', 200, u+'/', '')):
            self.assertEqual(audit.check_http_links()[0], 'review')
        with patch.object(audit, 'get', return_value=(None, None, '', 'timeout')):
            self.assertEqual(audit.check_http_links()[0], 'review')

    def test_text_lunch_and_contacts(self):
        audit = self.audit(html('lunchtalk').replace('</main>', '<p>[Country] 180 minutes hybrid USD 100 +65 1234 5678</p></main>'))
        status, evidence = audit.check_text()
        self.assertEqual(status, 'fail')
        self.assertIn('180', evidence)
        self.assertIn('allowed', evidence)
        self.assertIn('pricing', evidence)
        self.assertIn('+65', evidence)

    def test_form_and_ajax(self):
        self.assertEqual(self.audit().check_form()[0], 'review')
        self.assertIn('expected field signatures', self.audit().check_form()[1])
        self.assertEqual(self.audit(html().replace('data-ajax="true"', 'data-ajax="false"')).check_ajax()[0], 'fail')

    def test_optional_image_na(self):
        item = k.Item('23. Frequently asked questions', '*(optional)* Image', True)
        self.assertEqual(k.manual_item(self.audit(), item)[0], 'na')

    def test_cli_markdown_csv_and_preservation(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, report, csv_path = [Path(tmp)/p for p in ('draft.html', 'out.md', 'out.csv')]
            source.write_text(html(faq=12), encoding='utf-8')
            original = source.read_bytes()
            with contextlib.redirect_stdout(io.StringIO()):
                code = k.main([str(source), '--no-link-check', '--out', str(report), '--csv'])
            self.assertEqual(code, 1)
            self.assertEqual(source.read_bytes(), original)
            self.assertIn('Found 12 FAQ', report.read_text(encoding='utf-8'))
            with csv_path.open(encoding='utf-8-sig') as stream:
                rows = list(csv.DictReader(stream))
            items = k.parse_checklist(ROOT/'checklists'/k.CHECKLIST_FILES['course'])
            self.assertGreater(len(rows), len(items))
            self.assertEqual(rows[0]['item'], items[0].text)

    def test_cli_failure_is_clear(self):
        result = subprocess.run([sys.executable, str(ROOT/'knowles_page_checker.py'), '/no/such/file.html'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn('Traceback', result.stderr)

    def test_cli_summary_on_legacy_code_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp)/'draft.html'
            source.write_text(html(faq=12), encoding='utf-8')
            result = subprocess.run([sys.executable, str(ROOT/'knowles_page_checker.py'), str(source), '--no-link-check',
                                     '--out', str(Path(tmp)/'out.md')], capture_output=True,
                                    env={**os.environ, 'PYTHONIOENCODING': 'cp1252'})
            self.assertEqual(result.returncode, 1, result.stderr.decode('utf-8', 'replace'))
            self.assertIn('✅ Pass', result.stdout.decode('utf-8'))

    def test_fetch_failure_isolated(self):
        with patch.object(k, 'urlopen', side_effect=TimeoutError('timed out')):
            self.assertIn('timed out', k.fetch('https://example.com')[3])

    def test_coverage_table_has_every_item(self):
        table = k.write_coverage(ROOT/'checklists')
        count = sum(len(k.parse_checklist(ROOT/'checklists'/f)) for f in k.CHECKLIST_FILES.values())
        self.assertEqual(len([l for l in table.splitlines() if l.startswith('| course:') or l.startswith('| lunchtalk:') or l.startswith('| customized:')]), count)


if __name__ == '__main__':
    unittest.main()
