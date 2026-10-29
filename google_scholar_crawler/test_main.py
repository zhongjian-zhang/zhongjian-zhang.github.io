import unittest
import copy
import os
from unittest.mock import patch
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread

from main import (
    ScholarFetchError,
    ScholarParseError,
    build_shields_data,
    fetch_profile,
    parse_author_profile,
)
import main as crawler


PROFILE_HTML = """
<!doctype html>
<html>
  <body>
    <div id="gsc_prf_in">Zhongjian Zhang</div>
    <table id="gsc_rsb_st">
      <tr>
        <td class="gsc_rsb_std">163</td>
        <td class="gsc_rsb_std">120</td>
      </tr>
      <tr>
        <td class="gsc_rsb_std">8</td>
        <td class="gsc_rsb_std">6</td>
      </tr>
    </table>
    <table>
      <tr class="gsc_a_tr">
        <td class="gsc_a_t">
          <a class="gsc_a_at" href="/citations?view_op=view_citation&amp;hl=en&amp;user=XkeONm0AAAAJ&amp;citation_for_view=XkeONm0AAAAJ:abc123">Paper One</a>
          <div class="gs_gray">Zhongjian Zhang, Coauthor One</div>
          <div class="gs_gray">NeurIPS, 2026</div>
        </td>
        <td class="gsc_a_c"><a>7</a></td>
        <td class="gsc_a_y"><span>2026</span></td>
      </tr>
      <tr class="gsc_a_tr">
        <td class="gsc_a_t">
          <a class="gsc_a_at" href="/citations?view_op=view_citation&amp;hl=en&amp;user=XkeONm0AAAAJ&amp;citation_for_view=XkeONm0AAAAJ:def456">Paper Two</a>
          <div class="gs_gray">Coauthor Two, Zhongjian Zhang</div>
          <div class="gs_gray">WWW, 2025</div>
        </td>
        <td class="gsc_a_c"></td>
        <td class="gsc_a_y"><span>2025</span></td>
      </tr>
    </table>
  </body>
</html>
"""

API_PROFILE = {
    'search_metadata': {'status': 'Success'},
    'search_parameters': {'author_id': 'XkeONm0AAAAJ'},
    'author': {'name': 'Zhongjian Zhang'},
    'cited_by': {'table': [{'citations': {'all': 163, 'since_2021': 120}}]},
    'articles': [
        {'citation_id': 'XkeONm0AAAAJ:abc123', 'title': 'Paper One',
         'authors': 'Zhongjian Zhang, Coauthor One', 'publication': 'NeurIPS, 2026',
         'year': '2026', 'cited_by': {'value': 7}},
        {'citation_id': 'XkeONm0AAAAJ:def456', 'title': 'Paper Two',
         'authors': 'Coauthor Two, Zhongjian Zhang', 'publication': 'WWW, 2025',
         'year': '2025', 'cited_by': {'value': None}},
    ],
}


class CrawlerTests(unittest.TestCase):
    def test_api_failure_cannot_overwrite_published_snapshot(self):
        with patch.dict(os.environ, {
                'GOOGLE_SCHOLAR_ID': 'XkeONm0AAAAJ',
                'SCHOLAR_SOURCE': 'serpapi', 'SERPAPI_API_KEY': 'TEST_KEY'}), \
                patch('main.fetch_serpapi_profile', side_effect=ScholarFetchError('quota exhausted')), \
                patch('main.write_results') as write:
            with self.assertRaises(ScholarFetchError):
                crawler.main()
            write.assert_not_called()

    def test_api_does_not_retry_authentication_or_quota_errors(self):
        import requests

        for status in (401, 403, 429):
            response = requests.Response()
            response.status_code = status
            with self.subTest(status=status), patch('main.requests.Session.get',
                    return_value=response) as get:
                with self.assertRaisesRegex(ScholarFetchError, f'HTTP {status}'):
                    crawler.fetch_serpapi_profile('XkeONm0AAAAJ', 'TEST_KEY', backoff=0)
                self.assertEqual(get.call_count, 1)

    def test_api_preserves_total_and_per_paper_contract(self):
        actual = crawler.parse_serpapi_profile(API_PROFILE, 'XkeONm0AAAAJ')
        expected = parse_author_profile(PROFILE_HTML)
        for key in ('name', 'citedby', 'publications'):
            self.assertEqual(actual[key], expected[key])
        self.assertEqual(actual['source'], 'serpapi')
        self.assertTrue(actual['updated'].endswith('+00:00'))

    def test_api_rejects_errors_mismatched_authors_and_incomplete_data(self):
        variants = []
        for field, value in [('error', 'Invalid key'), ('articles', []),
                             ('cited_by', {}), ('serpapi_pagination', {'next': 'more'})]:
            variant = copy.deepcopy(API_PROFILE)
            variant[field] = value
            variants.append(variant)
        variant = copy.deepcopy(API_PROFILE)
        variant['articles'][0]['citation_id'] = 'OtherAuthor:abc123'
        variants.append(variant)
        for variant in variants:
            with self.subTest(variant=variant), self.assertRaises(ScholarParseError):
                crawler.parse_serpapi_profile(variant, 'XkeONm0AAAAJ')

    def test_api_fetch_does_not_leak_key_in_failure_traceback(self):
        import requests
        import traceback

        secret = 'SENSITIVE_TEST_KEY'
        with patch('main.requests.Session.get', side_effect=requests.ConnectionError(
                'https://serpapi.com/search.json?api_key=' + secret)):
            try:
                crawler.fetch_serpapi_profile('XkeONm0AAAAJ', secret, backoff=0)
                self.fail('Network failure must be reported')
            except ScholarFetchError:
                self.assertNotIn(secret, traceback.format_exc())

    def test_api_fetch_bounds_requests_and_uses_author_endpoint(self):
        import requests

        response = requests.Response()
        response.status_code = 200
        import json
        response._content = json.dumps(API_PROFILE).encode()
        with patch('main.requests.Session.get', side_effect=[
                requests.Timeout('temporary'), response]) as get:
            author = crawler.fetch_serpapi_profile('XkeONm0AAAAJ', 'TEST_KEY', backoff=0)
        self.assertEqual(author['citedby'], 163)
        self.assertEqual(get.call_count, 2)
        self.assertEqual(get.call_args.kwargs['params']['engine'], 'google_scholar_author')
        self.assertEqual(get.call_args.kwargs['params']['num'], 100)

    def test_parse_rejects_unreadable_total_instead_of_publishing_zero(self):
        for total in ("", "--", "unavailable"):
            with self.subTest(total=total), self.assertRaises(ScholarParseError):
                parse_author_profile(PROFILE_HTML.replace('>163<', f'>{total}<'))

    def test_parse_rejects_missing_publications(self):
        with self.assertRaises(ScholarParseError):
            parse_author_profile('<div id="gsc_prf_in">Zhongjian Zhang</div>'
                                 '<table id="gsc_rsb_st"><td class="gsc_rsb_std">163</td></table>')

    def test_fetch_uses_fallback_for_http_200_challenge(self):
        import requests

        challenge = requests.Response()
        challenge.status_code = 200
        challenge._content = b'<html>Please verify you are human</html>'
        profile = requests.Response()
        profile.status_code = 200
        profile._content = PROFILE_HTML.encode()
        with patch('main.requests.Session.get', side_effect=[challenge, profile]) as get:
            html = fetch_profile('https://example.test/direct',
                                 fallback_url='https://example.test/fallback', backoff=0)
        self.assertEqual(parse_author_profile(html)['citedby'], 163)
        self.assertEqual(get.call_count, 2)

    def test_parse_author_profile_preserves_json_contract(self):
        author = parse_author_profile(PROFILE_HTML)

        self.assertEqual(author["name"], "Zhongjian Zhang")
        self.assertEqual(author["citedby"], 163)
        self.assertEqual(
            list(author["publications"]),
            ["XkeONm0AAAAJ:abc123", "XkeONm0AAAAJ:def456"],
        )
        first = author["publications"]["XkeONm0AAAAJ:abc123"]
        self.assertEqual(first["author_pub_id"], "XkeONm0AAAAJ:abc123")
        self.assertEqual(first["bib"]["title"], "Paper One")
        self.assertEqual(first["bib"]["author"], "Zhongjian Zhang, Coauthor One")
        self.assertEqual(first["bib"]["citation"], "NeurIPS, 2026")
        self.assertEqual(first["bib"]["pub_year"], "2026")
        self.assertEqual(first["num_citations"], 7)
        self.assertEqual(
            build_shields_data(author),
            {"schemaVersion": 1, "label": "citations", "message": "163"},
        )

    def test_parse_author_profile_rejects_missing_citation_total(self):
        with self.assertRaisesRegex(ScholarParseError, "citation total"):
            parse_author_profile('<div id="gsc_prf_in">Zhongjian Zhang</div>')

    def test_fetch_retries_are_bounded(self):
        class RetryHandler(BaseHTTPRequestHandler):
            attempts = 0

            def do_GET(self):
                type(self).attempts += 1
                if type(self).attempts < 3:
                    self.send_response(503)
                    self.end_headers()
                    return
                body = PROFILE_HTML.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, format, *args):
                pass

        server = ThreadingHTTPServer(("127.0.0.1", 0), RetryHandler)
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            url = f"http://127.0.0.1:{server.server_port}/profile"
            html = fetch_profile(url, attempts=3, timeout=1, backoff=0)
        finally:
            server.shutdown()
            server.server_close()
            thread.join()

        self.assertIn("Zhongjian Zhang", html)
        self.assertEqual(RetryHandler.attempts, 3)

    def test_fetch_reports_failure_after_configured_attempts(self):
        class FailureHandler(BaseHTTPRequestHandler):
            attempts = 0

            def do_GET(self):
                type(self).attempts += 1
                self.send_response(503)
                self.end_headers()

            def log_message(self, format, *args):
                pass

        server = ThreadingHTTPServer(("127.0.0.1", 0), FailureHandler)
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            url = f"http://127.0.0.1:{server.server_port}/profile"
            with self.assertRaisesRegex(ScholarFetchError, "after 2 attempts"):
                fetch_profile(url, attempts=2, timeout=1, backoff=0)
        finally:
            server.shutdown()
            server.server_close()
            thread.join()

        self.assertEqual(FailureHandler.attempts, 2)

    def test_fetch_uses_fallback_when_direct_scholar_access_is_forbidden(self):
        class ForbiddenHandler(BaseHTTPRequestHandler):
            direct_attempts = 0
            fallback_attempts = 0

            def do_GET(self):
                if self.path == "/direct":
                    type(self).direct_attempts += 1
                    self.send_response(403)
                    self.end_headers()
                    return

                type(self).fallback_attempts += 1
                body = PROFILE_HTML.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, format, *args):
                pass

        server = ThreadingHTTPServer(("127.0.0.1", 0), ForbiddenHandler)
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            base_url = f"http://127.0.0.1:{server.server_port}"
            html = fetch_profile(
                f"{base_url}/direct",
                fallback_url=f"{base_url}/fallback",
                attempts=3,
                timeout=1,
                backoff=0,
            )
        finally:
            server.shutdown()
            server.server_close()
            thread.join()

        self.assertEqual(parse_author_profile(html)["citedby"], 163)
        self.assertEqual(ForbiddenHandler.direct_attempts, 1)
        self.assertEqual(ForbiddenHandler.fallback_attempts, 1)


if __name__ == "__main__":
    unittest.main()
