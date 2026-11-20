import unittest
from src.detector import analyze_url
from src.url_parser import parse_url
class URLParserTests(unittest.TestCase):
    def test_adds_default_scheme(self): self.assertEqual(parse_url("example.com")["scheme"],"http")
    def test_rejects_empty(self):
        with self.assertRaises(ValueError): parse_url(" ")
    def test_rejects_missing_host(self):
        with self.assertRaises(ValueError): parse_url("https:///path")
class DetectorTests(unittest.TestCase):
    def test_plain_https_domain_low(self):
        r=analyze_url("https://www.google.com"); self.assertEqual(r["risk"]["level"],"low"); self.assertEqual(r["risk"]["score"],0)
    def test_ip_and_http_raise_risk(self): self.assertGreaterEqual(analyze_url("http://192.0.2.10/account/reset")["risk"]["score"],30)
    def test_brand_lookalike(self):
        codes={x["code"] for x in analyze_url("http://paypa1-login.example.xyz/verify")["risk"]["reasons"]}; self.assertIn("lookalike_domain",codes)
    def test_detector_does_not_fetch_target(self): self.assertIn("disclaimer",analyze_url("https://example.com"))
if __name__=="__main__": unittest.main()
