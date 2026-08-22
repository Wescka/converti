from pathlib import Path
import ast
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]

class StaticQualityTests(unittest.TestCase):
    def test_python_sources_compile(self):
        for name in ("app.py", "capabilities.py", "config.py", "converters.py", "cv_exports.py", "security_utils.py"):
            ast.parse((ROOT / name).read_text(encoding="utf-8"), filename=name)

    def test_main_navigation_uses_real_routes(self):
        offenders = []
        pattern = re.compile(r'href=["\'][^"\']*#(?:convertir|formatos|ayuda|crear-cv)')
        for path in (ROOT / "templates").glob("*.html"):
            if pattern.search(path.read_text(encoding="utf-8")):
                offenders.append(path.name)
        self.assertEqual(offenders, [], f"Hash navigation remains in: {offenders}")

    def test_production_does_not_force_debug(self):
        source = (ROOT / "app.py").read_text(encoding="utf-8")
        self.assertNotIn("debug=True", source)

    def test_clean_routes_exist(self):
        source = (ROOT / "app.py").read_text(encoding="utf-8")
        for route in ("/convertir", "/formatos", "/ayuda", "/crear-cv"):
            self.assertIn(route, source)

    def test_no_secret_in_example(self):
        env = (ROOT / ".env.example").read_text(encoding="utf-8")
        key = next(line for line in env.splitlines() if line.startswith("GEMINI_API_KEY="))
        self.assertEqual(key, "GEMINI_API_KEY=")

    def test_cv_render_passes_navigation_context(self):
        source = (ROOT / "app.py").read_text(encoding="utf-8")
        self.assertIn("nav_paths=SECTION_PATHS[locale]", source)

    def test_cv_seo_render_passes_locale(self):
        source = (ROOT / "app.py").read_text(encoding="utf-8")
        self.assertRegex(source, r'render_template\("cv_seo_page\.html"[^\n]*locale=locale')

    def test_shared_mobile_navigation_assets_exist(self):
        self.assertTrue((ROOT / "static" / "js" / "site_ui.js").is_file())
        css = (ROOT / "static" / "css" / "site_ui.css").read_text(encoding="utf-8")
        self.assertIn("site-mobile-menu-toggle", css)
        for name in ("index.html", "section_page.html", "tool_page.html", "cv_seo_page.html"):
            html = (ROOT / "templates" / name).read_text(encoding="utf-8")
            self.assertIn("site-mobile-menu-toggle", html, name)
            self.assertIn("site_ui.js", html, name)

    def test_repo_root_has_no_duplicate_frontend_files_or_bytecode(self):
        forbidden = {"index.html","create_cv.html","create_cv.js","create_cv.css","site_ui.css","logo_converti.png","icon1.png","download","env.example"}
        present = sorted(x.name for x in ROOT.iterdir() if x.name in forbidden)
        self.assertEqual(present, [])
        pyc = [str(p.relative_to(ROOT)) for p in ROOT.rglob("*.pyc")]
        self.assertEqual(pyc, [])

    def test_section_pages_have_rich_localized_context(self):
        app_text = (ROOT / "app.py").read_text(encoding="utf-8")
        template = (ROOT / "templates" / "section_page.html").read_text(encoding="utf-8")
        self.assertIn("SECTION_DETAIL_UI", app_text)
        self.assertIn("detail=SECTION_DETAIL_UI[locale]", app_text)
        for token in ("detail.categories", "detail.faq", "detail.help_blocks", "detail.help_faq"):
            self.assertIn(token, template)


if __name__ == "__main__":
    unittest.main()
