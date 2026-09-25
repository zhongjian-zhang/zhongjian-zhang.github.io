import unittest

from main import ScholarParseError, build_shields_data, parse_author_profile


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


if __name__ == "__main__":
    unittest.main()
