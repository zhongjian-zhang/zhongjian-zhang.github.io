import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread

from main import (
    ScholarFetchError,
    ScholarParseError,
    build_shields_data,
    fetch_profile,
    parse_author_profile,
)


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


class CrawlerTests(unittest.TestCase):
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
