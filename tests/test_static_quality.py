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

    def test_home_seo_prioritizes_converter_and_ai_cv(self):
        html = (ROOT / "templates" / "index.html").read_text(encoding="utf-8")
        self.assertIn("Convertidor de archivos y CV con IA gratis", html)
        self.assertIn("Crea un CV profesional con IA totalmente gratis", html)
        self.assertIn('/cv/crear-cv-con-ia', html)
        self.assertIn('/convertir/pdf-a-word', html)

    def test_converter_route_has_distinct_search_intent(self):
        html = (ROOT / "templates" / "index.html").read_text(encoding="utf-8")
        self.assertIn("canonical_override is defined", html)
        self.assertIn("Convertidor de archivos online gratis", html)

    def test_sitemap_contains_hreflang_markup(self):
        source = (ROOT / "app.py").read_text(encoding="utf-8")
        self.assertIn('xmlns:xhtml=', source)
        self.assertIn('hreflang=\"x-default\"', source)

    def test_tool_pages_use_search_focused_titles(self):
        source = (ROOT / "app.py").read_text(encoding="utf-8")
        template = (ROOT / "templates" / "tool_page.html").read_text(encoding="utf-8")
        self.assertIn('seo_page_title', source)
        self.assertIn('{{ seo_page_title }}', template)


    def test_document_ai_tab_is_integrated_without_replacing_existing_nav(self):
        source = (ROOT / "app.py").read_text(encoding="utf-8")
        self.assertIn('"fixdocs":"/corregir-documentos-ia"', source)
        self.assertIn('@app.get("/corregir-documentos-ia")', source)
        for name in ("index.html", "section_page.html", "tool_page.html", "create_cv.html", "cv_seo_page.html"):
            html = (ROOT / "templates" / name).read_text(encoding="utf-8")
            self.assertIn("nav-doc-ai", html, name)
            self.assertRegex(html, r'(crear-cv|cv_path|nav_create|paths\.create)', name)

    def test_document_ai_placeholder_is_not_indexed_before_functionality_exists(self):
        html = (ROOT / "templates" / "document_ai_page.html").read_text(encoding="utf-8")
        self.assertIn('name="robots" content="noindex,follow"', html)
        source = (ROOT / "app.py").read_text(encoding="utf-8")
        core = re.search(r'core_keys\s*=\s*\(([^)]*)\)', source)
        self.assertIsNotNone(core)
        self.assertNotIn("fixdocs", core.group(1))


    def test_section_pages_use_shared_header_without_local_override(self):
        html = (ROOT / "templates" / "section_page.html").read_text(encoding="utf-8")
        self.assertNotIn("Header local:", html)
        self.assertNotRegex(html, r"\.header\{[^}]*!important")
        self.assertIn("site_ui.css", html)
        self.assertIn("width:min(1240px,calc(100% - 32px))", html)


    def test_image_conversion_exposes_document_outputs(self):
        capabilities = (ROOT / "capabilities.py").read_text(encoding="utf-8")
        converters = (ROOT / "converters.py").read_text(encoding="utf-8")
        app = (ROOT / "app.py").read_text(encoding="utf-8")
        for target in ("docx", "pptx", "html", "pdf"):
            self.assertIn(f'"{target}"', capabilities)
        self.assertIn("def images_to_document", converters)
        self.assertIn("validate_image_source", converters)
        self.assertIn("images_to_document(sources, target, tools, options)", app)

    def test_imagemagick_supports_magick_or_convert_binary(self):
        source = (ROOT / "security_utils.py").read_text(encoding="utf-8")
        self.assertRegex(source, r'magick=find_tool\(\s*"magick",\s*"convert",')


    def test_priority_conversion_pages_have_people_first_content(self):
        seo = (ROOT / "seo_content.py").read_text(encoding="utf-8")
        template = (ROOT / "templates" / "tool_page.html").read_text(encoding="utf-8")
        for slug in ("pdf-a-word","word-a-pdf","jpg-a-pdf","pdf-a-jpg","pdf-a-png","png-a-jpg","jpg-a-png","png-a-webp","csv-a-xlsx","xlsx-a-csv"):
            self.assertIn(f'"{slug}"', seo)
        for token in ("seo.use_cases", "seo.compatibility", "seo.issues", "seo.privacy", "seo.expectation"):
            self.assertIn(token, template)

    def test_tool_pages_use_current_structured_data_without_faq_rich_result(self):
        template = (ROOT / "templates" / "tool_page.html").read_text(encoding="utf-8")
        self.assertIn('"@type": "WebApplication"', template)
        self.assertIn('"@type": "BreadcrumbList"', template)
        self.assertNotIn('"@type": "FAQPage"', template)

    def test_ai_guard_preserves_factual_fields_and_retries(self):
        source = (ROOT / "app.py").read_text(encoding="utf-8")
        self.assertIn("def _cv_guard_ai_facts", source)
        self.assertIn('retryable_http = {429, 500, 502, 503, 504}', source)
        self.assertIn('"temperature":0.2', source)
        self.assertIn("result = _cv_guard_ai_facts(original_current, result, action, source_text)", source)

    def test_seo_module_is_python_valid_and_imported(self):
        ast.parse((ROOT / "seo_content.py").read_text(encoding="utf-8"), filename="seo_content.py")
        source = (ROOT / "app.py").read_text(encoding="utf-8")
        self.assertIn("from seo_content import enrich_tool_seo", source)

    def test_mid_width_header_keeps_buttons_visible_without_logo_collision(self):
        css = (ROOT / "static" / "css" / "site_ui.css").read_text(encoding="utf-8")
        js = (ROOT / "static" / "js" / "site_ui.js").read_text(encoding="utf-8")
        self.assertIn("@media (min-width:721px) and (max-width:1280px)", css)
        self.assertIn("grid-template-rows:58px auto", css)
        self.assertIn("max-height:none!important;opacity:1!important;pointer-events:auto!important", css)
        self.assertIn("window.innerWidth > 720", js)

    def test_convert_root_has_people_first_seo_content_without_blocking_converter(self):
        for name in ("index.html", "index_en.html", "index_fr.html", "index_ptbr.html"):
            html = (ROOT / "templates" / name).read_text(encoding="utf-8")
            self.assertIn("convert-seo-guide", html, name)
            self.assertIn("canonical_override is defined", html, name)
            self.assertLess(html.index('id="convertir"'), html.index("convert-seo-guide"), name)

    def test_site_ui_cache_version_is_bumped_for_layout_release(self):
        for name in ("index.html", "index_en.html", "index_fr.html", "index_ptbr.html", "section_page.html", "tool_page.html"):
            html = (ROOT / "templates" / name).read_text(encoding="utf-8")
            self.assertIn("20260822-header-stable-7", html, name)



class HeaderResponsiveRegressionTests(unittest.TestCase):
    def test_mid_width_keeps_navigation_visible(self):
        css = (ROOT / 'static/css/site_ui.css').read_text(encoding='utf-8')
        self.assertIn('@media (min-width:721px) and (max-width:1280px)', css)
        self.assertIn('grid-template-rows:58px auto', css)
        self.assertIn('max-height:none!important;opacity:1!important;pointer-events:auto!important', css)
        self.assertIn('.site-mobile-menu-toggle,.cvb-mobile-menu-toggle{display:none!important}', css)

    def test_only_mobile_collapses_navigation(self):
        css = (ROOT / 'static/css/site_ui.css').read_text(encoding='utf-8')
        self.assertIn('@media (max-width:720px)', css)
        self.assertNotIn('@media (max-width:1280px) and (min-width:721px)', css)

    def test_header_css_has_single_mid_width_strategy(self):
        css = (ROOT / 'static/css/site_ui.css').read_text(encoding='utf-8')
        self.assertEqual(css.count('@media (min-width:721px) and (max-width:1280px)'), 1)

if __name__ == "__main__":
    unittest.main()
