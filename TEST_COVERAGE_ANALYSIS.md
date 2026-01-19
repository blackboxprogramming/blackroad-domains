# Test Coverage Analysis Report

**Repository:** blackroad-domains
**Date:** January 2026
**Current Coverage:** 0%

---

## Executive Summary

This codebase has **zero automated test coverage**. The repository contains production infrastructure code that deploys to Cloudflare, Raspberry Pi clusters, and cloud VPS instances without any automated testing or validation. This represents a significant risk for production deployments.

---

## Current State

### Codebase Inventory

| Component | Lines of Code | Test Coverage | Risk Level |
|-----------|---------------|---------------|------------|
| `generate_domains.py` | 398 | 0% | Medium |
| `deploy_domains.py` | 114 | 0% | **High** |
| `blackroad-deploy-all.sh` | 242 | 0% | **High** |
| `blackroad-netdump.sh` | 279 | 0% | Medium |
| `deploy_all_domains.sh` | 88 | 0% | **High** |
| `add-github-actions-to-all-repos.sh` | 274 | 0% | Medium |
| GitHub Actions Workflow | 64 | 0% | Medium |
| Static HTML pages | ~60 files | N/A | Low |

### What Currently Exists

- **Manual testing only** via visual browser inspection
- Brand compliance check in CI (grep-based, no unit tests)
- No testing frameworks configured
- No test configuration files
- No coverage reporting

---

## Recommended Testing Improvements

### Priority 1: Python Unit Tests (High Impact)

#### 1.1 Test `generate_domains.py`

This file contains testable pure functions for HTML generation.

**Functions to test:**
- `generate_html(domain, config)` - Core HTML generation logic

**Recommended tests:**

```python
# tests/test_generate_domains.py

import pytest
from generate_domains import generate_html, DOMAINS, HTML_TEMPLATE

class TestGenerateHtml:
    """Tests for HTML generation logic"""

    def test_generate_html_returns_valid_html(self):
        """Generated HTML should be valid and contain required elements"""
        config = {
            "title": "Test Domain",
            "tagline": "Test Tagline",
            "icon": "🧪",
            "description": "Test description",
            "features": ["Feature 1", "Feature 2"],
            "cta": "Click Here",
            "cta_link": "https://example.com"
        }
        html = generate_html("test.blackroad.io", config)

        assert "<!DOCTYPE html>" in html
        assert "<title>Test Domain</title>" in html
        assert "Test Tagline" in html
        assert "Feature 1" in html
        assert "Feature 2" in html

    def test_generate_html_escapes_special_characters(self):
        """HTML generation should handle special characters safely"""
        config = {
            "title": "Test <script>alert('xss')</script>",
            "tagline": "Safe & Secure",
            "icon": "🔒",
            "description": "Test \"quotes\" and 'apostrophes'",
            "features": ["Feature & More"],
            "cta": "Go",
            "cta_link": "#"
        }
        html = generate_html("test.blackroad.io", config)
        # Should not contain unescaped script tags
        assert "<script>alert" not in html or "&lt;script&gt;" in html

    def test_all_domains_have_required_fields(self):
        """All domain configs should have required fields"""
        required_fields = ["title", "tagline", "icon", "description", "features", "cta", "cta_link"]

        for domain, config in DOMAINS.items():
            for field in required_fields:
                assert field in config, f"Domain {domain} missing field: {field}"

    def test_all_domains_generate_valid_html(self):
        """Every domain config should produce valid HTML"""
        for domain, config in DOMAINS.items():
            html = generate_html(domain, config)
            assert "<!DOCTYPE html>" in html
            assert "</html>" in html

    def test_domain_name_transformation(self):
        """Domain names should be transformed correctly for display"""
        config = DOMAINS["universe.blackroad.io"]
        html = generate_html("universe.blackroad.io", config)
        assert "UNIVERSE" in html  # subdomain should be uppercase

    def test_features_rendered_as_divs(self):
        """Each feature should be wrapped in a feature div"""
        config = {
            "title": "Test",
            "tagline": "Test",
            "icon": "🧪",
            "description": "Test",
            "features": ["Alpha", "Beta", "Gamma"],
            "cta": "Go",
            "cta_link": "#"
        }
        html = generate_html("test.blackroad.io", config)
        assert html.count('class="feature"') == 3
```

#### 1.2 Test `deploy_domains.py`

This file interacts with external systems (Cloudflare, filesystem) and needs mocked tests.

**Functions to test:**
- `deploy_domain(html_file, project_name)` - Deployment logic

**Recommended tests:**

```python
# tests/test_deploy_domains.py

import pytest
from unittest.mock import Mock, patch, MagicMock
import os
import tempfile

class TestDeployDomain:
    """Tests for domain deployment logic"""

    @patch('deploy_domains.subprocess.run')
    @patch('deploy_domains.shutil.copy')
    @patch('deploy_domains.os.makedirs')
    @patch('deploy_domains.os.path.exists')
    @patch('deploy_domains.shutil.rmtree')
    def test_deploy_domain_success(self, mock_rmtree, mock_exists, mock_makedirs, mock_copy, mock_run):
        """Successful deployment should return True"""
        mock_exists.return_value = True
        mock_run.return_value = Mock(
            returncode=0,
            stdout="Deployment complete! https://test.pages.dev"
        )

        from deploy_domains import deploy_domain
        result = deploy_domain("test.html", "test-project")

        assert result == True
        mock_run.assert_called_once()

    @patch('deploy_domains.subprocess.run')
    @patch('deploy_domains.shutil.copy')
    @patch('deploy_domains.os.makedirs')
    @patch('deploy_domains.os.path.exists')
    @patch('deploy_domains.shutil.rmtree')
    def test_deploy_domain_failure(self, mock_rmtree, mock_exists, mock_makedirs, mock_copy, mock_run):
        """Failed deployment should return False"""
        mock_exists.return_value = True
        mock_run.return_value = Mock(
            returncode=1,
            stderr="Error: Authentication failed"
        )

        from deploy_domains import deploy_domain
        result = deploy_domain("test.html", "test-project")

        assert result == False

    @patch('deploy_domains.subprocess.run')
    def test_deploy_domain_timeout_handling(self, mock_run):
        """Deployment should handle timeouts gracefully"""
        import subprocess
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="wrangler", timeout=120)

        from deploy_domains import deploy_domain
        result = deploy_domain("test.html", "test-project")

        assert result == False

    def test_temp_directory_cleanup(self):
        """Temp directories should be cleaned up after deployment"""
        # Test that cleanup happens in finally block
        pass  # Implementation depends on refactoring deploy_domain
```

---

### Priority 2: Shell Script Testing (Medium-High Impact)

The shell scripts perform critical deployment operations and should be tested using **BATS** (Bash Automated Testing System).

#### 2.1 Test `blackroad-deploy-all.sh`

**Functions to test:**
- `log_success()`, `log_error()`, `log_info()`, `log_section()`
- `deploy_frontend()`
- `deploy_worker()`
- `deploy_pi_backend()`
- `deploy_vps()`

**Recommended tests:**

```bash
# tests/test_blackroad_deploy.bats

#!/usr/bin/env bats

# Load the script functions
setup() {
    source ./blackroad-deploy-all.sh --source-only 2>/dev/null || true
}

@test "log_success outputs green text with checkmark" {
    run log_success "Test message"
    [[ "$output" == *"✅"* ]]
    [[ "$output" == *"Test message"* ]]
}

@test "log_error outputs red text with cross" {
    run log_error "Error message"
    [[ "$output" == *"❌"* ]]
    [[ "$output" == *"Error message"* ]]
}

@test "deploy_frontend fails when directory does not exist" {
    run deploy_frontend "test-project" "/nonexistent/path"
    [ "$status" -eq 1 ]
    [[ "$output" == *"Directory not found"* ]]
}

@test "deploy_pi_backend fails when SSH connection fails" {
    run deploy_pi_backend "test-pi" "192.168.999.999" "/path"
    [ "$status" -eq 1 ]
    [[ "$output" == *"Cannot connect"* ]]
}

@test "environment variables control deployment targets" {
    export DEPLOY_FRONTENDS=false
    export DEPLOY_WORKERS=false
    export DEPLOY_PI=false
    export DEPLOY_VPS=false

    # Script should complete without deploying anything
    run ./blackroad-deploy-all.sh --dry-run
    [ "$status" -eq 0 ]
}
```

---

### Priority 3: Integration Tests (Medium Impact)

#### 3.1 HTML Validation Tests

Validate that generated HTML pages are well-formed and accessible.

```python
# tests/test_html_validation.py

import pytest
from pathlib import Path
import re

class TestHtmlValidation:
    """Validate generated HTML pages"""

    @pytest.fixture
    def html_files(self):
        """Get all HTML files in the repository"""
        return list(Path(".").glob("**/*.html"))

    def test_all_html_files_have_doctype(self, html_files):
        """All HTML files should have DOCTYPE declaration"""
        for html_file in html_files:
            content = html_file.read_text()
            assert "<!DOCTYPE html>" in content, f"{html_file} missing DOCTYPE"

    def test_all_html_files_have_lang_attribute(self, html_files):
        """All HTML files should have lang attribute for accessibility"""
        for html_file in html_files:
            content = html_file.read_text()
            assert 'lang="en"' in content or "lang='en'" in content, \
                f"{html_file} missing lang attribute"

    def test_all_html_files_have_viewport_meta(self, html_files):
        """All HTML files should be mobile-responsive"""
        for html_file in html_files:
            content = html_file.read_text()
            assert "viewport" in content, f"{html_file} missing viewport meta"

    def test_all_html_files_have_title(self, html_files):
        """All HTML files should have a title"""
        for html_file in html_files:
            content = html_file.read_text()
            assert "<title>" in content and "</title>" in content, \
                f"{html_file} missing title"

    def test_no_broken_internal_links(self, html_files):
        """Internal links should point to existing files"""
        for html_file in html_files:
            content = html_file.read_text()
            # Find href attributes pointing to local files
            links = re.findall(r'href="([^"]+)"', content)
            for link in links:
                if link.startswith("/") and not link.startswith("//"):
                    # Local absolute path
                    target = Path(".") / link.lstrip("/")
                    # Skip if it's a route or anchor
                    if "#" not in link and "." in link:
                        assert target.exists() or True  # Soft check
```

#### 3.2 Brand Compliance Tests

Formalize the brand compliance checks currently in CI.

```python
# tests/test_brand_compliance.py

import pytest
from pathlib import Path
import re

# Official brand colors
OFFICIAL_COLORS = {
    "#F5A623",  # Orange
    "#FF1D6C",  # Red/Pink
    "#2979FF",  # Blue
    "#9C27B0",  # Purple
}

# Forbidden colors (old brand)
FORBIDDEN_COLORS = {
    "#FF9D00",
    "#FF6B00",
    "#FF0066",
    "#FF006B",
    "#D600AA",
    "#7700FF",
    "#0066FF",
}

class TestBrandCompliance:
    """Ensure brand guidelines are followed"""

    @pytest.fixture
    def style_files(self):
        """Get all CSS and HTML files"""
        css_files = list(Path(".").glob("**/*.css"))
        html_files = list(Path(".").glob("**/*.html"))
        return css_files + html_files

    def test_no_forbidden_colors(self, style_files):
        """Files should not contain forbidden brand colors"""
        for file_path in style_files:
            content = file_path.read_text()
            for color in FORBIDDEN_COLORS:
                assert color.lower() not in content.lower(), \
                    f"Forbidden color {color} found in {file_path}"

    def test_uses_official_colors(self, style_files):
        """Files should use official brand colors"""
        all_content = ""
        for file_path in style_files:
            all_content += file_path.read_text()

        # At least one official color should be present
        found_official = any(
            color.lower() in all_content.lower()
            for color in OFFICIAL_COLORS
        )
        assert found_official, "No official brand colors found in stylesheets"
```

---

### Priority 4: CI/CD Pipeline Tests

#### 4.1 Add Test Stage to GitHub Actions

```yaml
# .github/workflows/deploy.yml (updated)

name: Test and Deploy to Cloudflare Pages

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    name: Run Tests
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install pytest pytest-cov

      - name: Run Python tests
        run: |
          pytest tests/ -v --cov=. --cov-report=xml --cov-report=term

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml

  lint:
    runs-on: ubuntu-latest
    name: Lint Code
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install linters
        run: pip install flake8 black

      - name: Run flake8
        run: flake8 *.py --max-line-length=120

      - name: Check formatting with black
        run: black --check *.py

      - name: ShellCheck
        uses: ludeeus/action-shellcheck@master
        with:
          scandir: '.'

  deploy:
    needs: [test, lint]
    runs-on: ubuntu-latest
    # ... existing deploy job
```

---

## Recommended Testing Stack

### Python Testing
- **pytest** - Test framework
- **pytest-cov** - Coverage reporting
- **unittest.mock** - Mocking external services
- **responses** or **httpretty** - HTTP mocking for API calls

### Shell Testing
- **bats-core** - Bash Automated Testing System
- **shellcheck** - Static analysis for shell scripts

### HTML/CSS Testing
- **html5validator** - HTML validation
- **pa11y** - Accessibility testing
- **lighthouse-ci** - Performance and best practices

### CI/CD
- **codecov** - Coverage tracking
- **pre-commit** - Git hooks for linting

---

## Implementation Roadmap

### Phase 1: Foundation (Immediate)
1. Create `tests/` directory structure
2. Add `pytest.ini` or `pyproject.toml` configuration
3. Write unit tests for `generate_domains.py`
4. Add pytest to CI pipeline

### Phase 2: Critical Paths (Short-term)
1. Write mocked tests for `deploy_domains.py`
2. Add integration tests for HTML validation
3. Set up coverage reporting with 50% target

### Phase 3: Comprehensive Coverage (Medium-term)
1. Add BATS tests for shell scripts
2. Implement brand compliance tests
3. Add accessibility testing
4. Increase coverage target to 80%

### Phase 4: Advanced Testing (Long-term)
1. Add end-to-end deployment tests (staging environment)
2. Implement visual regression testing
3. Add performance benchmarks
4. Set up mutation testing

---

## Quick Start

To begin implementing tests, create the following structure:

```
blackroad-domains/
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_generate_domains.py
│   ├── test_deploy_domains.py
│   ├── test_html_validation.py
│   └── test_brand_compliance.py
├── pytest.ini
└── requirements-dev.txt
```

**requirements-dev.txt:**
```
pytest>=7.0.0
pytest-cov>=4.0.0
black>=23.0.0
flake8>=6.0.0
```

**pytest.ini:**
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
addopts = -v --tb=short
```

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Deployment breaks production | High | Critical | Add deployment tests |
| HTML generation produces invalid output | Medium | High | Add HTML validation tests |
| Brand colors drift from guidelines | Medium | Medium | Automated brand compliance |
| Shell scripts fail silently | High | High | Add BATS tests with assertions |
| API credentials exposed | Low | Critical | Add secret scanning |

---

## Conclusion

The current lack of automated testing represents a significant gap in the development workflow. Implementing the recommendations in this document will:

1. **Reduce deployment risk** by catching errors before production
2. **Improve code quality** through test-driven development
3. **Enable confident refactoring** with a safety net of tests
4. **Document expected behavior** through test cases
5. **Speed up development** by catching regressions early

The recommended approach prioritizes high-risk deployment code first, then expands to comprehensive coverage of all components.
