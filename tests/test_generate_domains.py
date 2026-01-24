"""
Tests for generate_domains.py
"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generate_domains import generate_html, DOMAINS, HTML_TEMPLATE


class TestGenerateHtml:
    """Tests for the generate_html() function"""

    def test_generates_valid_html_structure(self):
        """Ensure output contains valid HTML structure"""
        config = {
            "title": "Test Title",
            "tagline": "Test Tagline",
            "icon": "🎯",
            "description": "Test description",
            "features": ["Feature 1", "Feature 2"],
            "cta": "Click Me",
            "cta_link": "https://example.com"
        }
        html = generate_html("test.blackroad.io", config)

        assert "<!DOCTYPE html>" in html
        assert "<html lang=\"en\">" in html
        assert "</html>" in html
        assert "<head>" in html
        assert "</head>" in html
        assert "<body>" in html
        assert "</body>" in html

    def test_title_included_in_output(self):
        """Test that title appears in the HTML"""
        config = {
            "title": "My Custom Title",
            "tagline": "Tagline",
            "icon": "🎯",
            "description": "Description",
            "features": ["Feature"],
            "cta": "CTA",
            "cta_link": "#"
        }
        html = generate_html("test.blackroad.io", config)

        assert "<title>My Custom Title</title>" in html

    def test_description_in_meta_tag(self):
        """Test that description appears in meta tag"""
        config = {
            "title": "Title",
            "tagline": "Tagline",
            "icon": "🎯",
            "description": "This is the meta description",
            "features": ["Feature"],
            "cta": "CTA",
            "cta_link": "#"
        }
        html = generate_html("test.blackroad.io", config)

        assert 'content="This is the meta description"' in html

    def test_icon_rendered(self):
        """Test that icon emoji appears in output"""
        config = {
            "title": "Title",
            "tagline": "Tagline",
            "icon": "🌍",
            "description": "Description",
            "features": ["Feature"],
            "cta": "CTA",
            "cta_link": "#"
        }
        html = generate_html("test.blackroad.io", config)

        assert '🌍' in html

    def test_features_rendered_as_divs(self):
        """Test that features are rendered as individual divs"""
        config = {
            "title": "Title",
            "tagline": "Tagline",
            "icon": "🎯",
            "description": "Description",
            "features": ["Alpha Feature", "Beta Feature", "Gamma Feature"],
            "cta": "CTA",
            "cta_link": "#"
        }
        html = generate_html("test.blackroad.io", config)

        assert '<div class="feature">Alpha Feature</div>' in html
        assert '<div class="feature">Beta Feature</div>' in html
        assert '<div class="feature">Gamma Feature</div>' in html

    def test_cta_link_and_text(self):
        """Test that CTA button has correct link and text"""
        config = {
            "title": "Title",
            "tagline": "Tagline",
            "icon": "🎯",
            "description": "Description",
            "features": ["Feature"],
            "cta": "Launch Now",
            "cta_link": "https://launch.example.com"
        }
        html = generate_html("test.blackroad.io", config)

        assert 'href="https://launch.example.com"' in html
        assert '>Launch Now</a>' in html

    def test_domain_name_formatting_subdomain(self):
        """Test that subdomain is extracted and uppercased"""
        config = {
            "title": "Title",
            "tagline": "Tagline",
            "icon": "🎯",
            "description": "Description",
            "features": ["Feature"],
            "cta": "CTA",
            "cta_link": "#"
        }
        html = generate_html("universe.blackroad.io", config)

        # 'universe.blackroad.io' should become 'UNIVERSE'
        assert '>UNIVERSE</h1>' in html

    def test_domain_name_formatting_root(self):
        """Test that root domain formats correctly"""
        config = {
            "title": "Title",
            "tagline": "Tagline",
            "icon": "🎯",
            "description": "Description",
            "features": ["Feature"],
            "cta": "CTA",
            "cta_link": "#"
        }
        html = generate_html("blackroad.io", config)

        # 'blackroad.io' should become 'BLACKROAD OS'
        assert '>BLACKROAD OS</h1>' in html

    def test_tagline_rendered(self):
        """Test that tagline appears in output"""
        config = {
            "title": "Title",
            "tagline": "This is the tagline text",
            "icon": "🎯",
            "description": "Description",
            "features": ["Feature"],
            "cta": "CTA",
            "cta_link": "#"
        }
        html = generate_html("test.blackroad.io", config)

        assert 'This is the tagline text' in html

    def test_empty_features_list(self):
        """Test handling of empty features list"""
        config = {
            "title": "Title",
            "tagline": "Tagline",
            "icon": "🎯",
            "description": "Description",
            "features": [],
            "cta": "CTA",
            "cta_link": "#"
        }
        html = generate_html("test.blackroad.io", config)

        # Should still generate valid HTML
        assert "<!DOCTYPE html>" in html
        assert '<div class="features">' in html

    def test_special_characters_in_description(self):
        """Test that special characters are handled"""
        config = {
            "title": "Title",
            "tagline": "Tagline",
            "icon": "🎯",
            "description": "Description with 'quotes' and \"double quotes\"",
            "features": ["Feature"],
            "cta": "CTA",
            "cta_link": "#"
        }
        html = generate_html("test.blackroad.io", config)

        # Should contain the description
        assert "Description with 'quotes'" in html


class TestDomainConfigurations:
    """Tests for the DOMAINS configuration dictionary"""

    REQUIRED_FIELDS = ['title', 'tagline', 'icon', 'description', 'features', 'cta', 'cta_link']

    def test_domains_not_empty(self):
        """Ensure DOMAINS dict is not empty"""
        assert len(DOMAINS) > 0

    def test_all_domains_have_required_fields(self):
        """Validate all domains have required configuration fields"""
        for domain, config in DOMAINS.items():
            for field in self.REQUIRED_FIELDS:
                assert field in config, f"Domain '{domain}' missing required field: {field}"

    def test_all_titles_are_non_empty_strings(self):
        """Ensure all titles are non-empty strings"""
        for domain, config in DOMAINS.items():
            assert isinstance(config['title'], str), f"Domain '{domain}' title is not a string"
            assert len(config['title']) > 0, f"Domain '{domain}' has empty title"

    def test_all_features_are_lists(self):
        """Ensure features field is always a list"""
        for domain, config in DOMAINS.items():
            assert isinstance(config['features'], list), f"Domain '{domain}' features is not a list"

    def test_all_cta_links_are_valid_format(self):
        """Validate CTA links are URLs or anchors"""
        for domain, config in DOMAINS.items():
            link = config['cta_link']
            valid = (
                link.startswith('https://') or
                link.startswith('http://') or
                link.startswith('/') or
                link.startswith('#')
            )
            assert valid, f"Domain '{domain}' has invalid cta_link: {link}"

    def test_all_icons_are_non_empty(self):
        """Ensure all icons are non-empty"""
        for domain, config in DOMAINS.items():
            assert len(config['icon']) > 0, f"Domain '{domain}' has empty icon"

    def test_no_duplicate_titles(self):
        """Ensure no two domains have the same title"""
        titles = [config['title'] for config in DOMAINS.values()]
        assert len(titles) == len(set(titles)), "Duplicate titles found in DOMAINS"

    def test_domain_count(self):
        """Verify expected number of domains"""
        # Should have at least 10 domains configured
        assert len(DOMAINS) >= 10, f"Expected at least 10 domains, found {len(DOMAINS)}"


class TestHtmlTemplate:
    """Tests for the HTML_TEMPLATE constant"""

    def test_template_has_all_placeholders(self):
        """Ensure template has all required placeholders"""
        required_placeholders = [
            '{title}',
            '{description}',
            '{icon}',
            '{domain_name}',
            '{tagline}',
            '{features_html}',
            '{cta}',
            '{cta_link}'
        ]
        for placeholder in required_placeholders:
            assert placeholder in HTML_TEMPLATE, f"Missing placeholder: {placeholder}"

    def test_template_is_valid_html_structure(self):
        """Ensure template has valid HTML structure"""
        assert '<!DOCTYPE html>' in HTML_TEMPLATE
        assert '<html' in HTML_TEMPLATE
        assert '</html>' in HTML_TEMPLATE

    def test_template_includes_viewport_meta(self):
        """Ensure template has responsive viewport meta tag"""
        assert 'viewport' in HTML_TEMPLATE
        assert 'width=device-width' in HTML_TEMPLATE

    def test_template_includes_inter_font(self):
        """Ensure Inter font is loaded"""
        assert 'fonts.googleapis.com' in HTML_TEMPLATE
        assert 'Inter' in HTML_TEMPLATE
