from pathlib import Path
import py_compile
import re
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

class StaticQualityTests(unittest.TestCase):
    def test_python_sources_compile(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name in ("app.py", "capabilities.py", "config.py", "converters.py", "cv_exports.py", "security_utils.py"):
                target = Path(tmp) / f"{name}.pyc"
                py_compile.compile(str(ROOT / name), cfile=str(target), doraise=True)

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

    def test_repo_has_no_duplicate_runtime_files_at_root(self):
        forbidden = {
            "index.html", "index_en.html", "index_fr.html", "index_ptbr.html",
            "create_cv.html", "tool_page.html", "section_page.html", "cv_seo_page.html",
            "create_cv.css", "site_ui.css", "create_cv.js", "download", "env.example"
        }
        present = sorted(name for name in forbidden if (ROOT / name).exists())
        self.assertEqual(present, [], f"Duplicate/mixed files in repository root: {present}")

    def test_no_compiled_python_is_committed(self):
        pyc = [str(x.relative_to(ROOT)) for x in ROOT.rglob("*.pyc")]
        caches = [str(x.relative_to(ROOT)) for x in ROOT.rglob("__pycache__") if x.is_dir()]
        self.assertEqual(pyc, [], f"Compiled Python files remain: {pyc}")
        self.assertEqual(caches, [], f"__pycache__ remains: {caches}")

    def test_shared_mobile_header_is_present_on_generic_pages(self):
        for path in (ROOT / "templates").glob("*.html"):
            text = path.read_text(encoding="utf-8")
            if '<header class="header">' in text:
                self.assertIn('converti-mobile-menu-toggle', text, path.name)
                self.assertIn('/static/js/site_ui.js', text, path.name)

    def test_shared_assets_exist(self):
        for rel in (
            "static/css/site_ui.css", "static/css/create_cv.css",
            "static/js/site_ui.js", "static/js/create_cv.js",
            "static/images/logo_converti.png", "static/images/icon1.png",
            "templates/cv_seo_page.html", "templates/section_page.html"
        ):
            self.assertTrue((ROOT / rel).is_file(), rel)

    def test_cv_seo_has_five_intents_per_locale(self):
        source = (ROOT / "app.py").read_text(encoding="utf-8")
        for slug in (
            "crear-cv-con-ia", "mejorar-cv-con-ia", "optimizar-cv-computrabajo",
            "cv-ats", "convertir-cv-computrabajo"
        ):
            self.assertIn(slug, source)
        self.assertIn('locale=locale', source)


    def test_create_cv_receives_navigation_paths(self):
        source = (ROOT / "app.py").read_text(encoding="utf-8")
        self.assertIn('nav_paths=SECTION_PATHS[locale]', source)
        template = (ROOT / "templates/create_cv.html").read_text(encoding="utf-8")
        self.assertIn('{{ nav_paths.convert }}', template)
        self.assertIn('{{ nav_paths.formats }}', template)
        self.assertIn('{{ nav_paths.help }}', template)

    def test_mobile_cv_flow_and_export_labels_remain(self):
        js = (ROOT / "static/js/create_cv.js").read_text(encoding="utf-8")
        css = (ROOT / "static/css/create_cv.css").read_text(encoding="utf-8")
        self.assertIn("revealGeneratedCvOnMobile", js)
        self.assertIn("setMobileView('preview')", js)
        self.assertIn("min-width:92px", css)

if __name__ == "__main__":
    unittest.main()
