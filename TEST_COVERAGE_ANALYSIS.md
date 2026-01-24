# Test Coverage Analysis for BlackRoad Domains

**Date:** 2026-01-24
**Repository:** blackroad-domains
**Analysis Status:** Complete

---

## Executive Summary

This repository currently has **zero automated test coverage**. The codebase contains significant deployment and infrastructure logic that would benefit substantially from testing. This document identifies key areas where tests should be added to improve reliability, catch regressions, and enable safe refactoring.

---

## Current State

| Metric | Value |
|--------|-------|
| **Test Files** | 0 |
| **Test Coverage** | 0% |
| **Testing Frameworks** | None configured |
| **CI Testing** | Brand compliance check only |

### What Exists Today

1. **Brand Compliance Check** (`.github/workflows/deploy.yml:20-35`) - A grep-based check for color codes
2. **Manual Testing** - Deployment verification is done manually

---

## Recommended Testing Areas

### 1. Python Unit Tests (High Priority)

#### 1.1 `generate_domains.py` - Domain HTML Generator

**Testable Functions:**

| Function | Lines | Test Priority | Description |
|----------|-------|---------------|-------------|
| `generate_html()` | 350-368 | **Critical** | Core HTML generation logic |
| `main()` | 371-398 | High | File generation orchestration |

**Recommended Test Cases:**

```python
# tests/test_generate_domains.py

class TestGenerateHtml:
    def test_generates_valid_html_structure(self):
        """Ensure output is valid HTML with DOCTYPE, html, head, body tags"""

    def test_domain_name_formatting(self):
        """Test that 'universe.blackroad.io' becomes 'UNIVERSE' in output"""

    def test_features_rendered_correctly(self):
        """Verify all features from config appear in HTML output"""

    def test_cta_link_included(self):
        """Ensure call-to-action links are properly rendered"""

    def test_handles_missing_optional_fields(self):
        """Gracefully handle configs with missing optional fields"""

    def test_special_characters_escaped(self):
        """Ensure XSS-safe output for user-provided content"""

class TestDomainConfigs:
    def test_all_domains_have_required_fields(self):
        """Validate DOMAINS dict has title, tagline, icon, description, features, cta, cta_link"""

    def test_cta_links_are_valid_urls_or_anchors(self):
        """Verify cta_link values are valid URLs or # anchors"""

    def test_icons_are_single_emojis(self):
        """Validate icons are valid emoji characters"""
```

#### 1.2 `deploy_domains.py` - Deployment Script

**Testable Functions:**

| Function | Lines | Test Priority | Description |
|----------|-------|---------------|-------------|
| `deploy_domain()` | 23-69 | High | Single domain deployment |
| `main()` | 72-114 | Medium | Deployment orchestration |

**Recommended Test Cases:**

```python
# tests/test_deploy_domains.py

class TestDeployDomain:
    def test_creates_temp_directory(self):
        """Verify temp directory is created for deployment"""

    def test_copies_html_as_index(self):
        """Ensure HTML file is copied as index.html"""

    def test_cleans_up_temp_directory_on_success(self):
        """Verify temp directory is removed after successful deployment"""

    def test_cleans_up_temp_directory_on_failure(self):
        """Verify temp directory is removed even on deployment failure"""

    def test_handles_missing_source_file(self):
        """Graceful handling when HTML file doesn't exist"""

    def test_handles_wrangler_timeout(self):
        """Proper error handling for deployment timeouts"""

    def test_extracts_deployment_url_from_output(self):
        """Correctly parse deployment URL from wrangler output"""

class TestDeploymentMapping:
    def test_all_html_files_exist(self):
        """Verify all files in DEPLOYMENTS dict exist in pages directory"""

    def test_project_names_are_valid(self):
        """Validate Cloudflare project names follow naming conventions"""
```

---

### 2. Bash Script Tests (Medium Priority)

Testing bash scripts requires a framework like [Bats](https://github.com/bats-core/bats-core) (Bash Automated Testing System).

#### 2.1 `blackroad-deploy-all.sh`

**Testable Functions:**

| Function | Lines | Test Priority | Description |
|----------|-------|---------------|-------------|
| `log_success()` | 36-38 | Low | Output formatting |
| `log_error()` | 40-42 | Low | Error output formatting |
| `deploy_frontend()` | 59-95 | **Critical** | Frontend deployment logic |
| `deploy_worker()` | 101-120 | High | Worker deployment logic |
| `deploy_pi_backend()` | 126-153 | High | Raspberry Pi deployment |
| `deploy_vps()` | 159-185 | High | VPS deployment |

**Recommended Test Cases:**

```bash
# tests/blackroad-deploy-all.bats

@test "deploy_frontend fails gracefully for missing directory" {
  run deploy_frontend "test-project" "/nonexistent/path"
  [ "$status" -eq 1 ]
  [[ "$output" == *"Directory not found"* ]]
}

@test "deploy_frontend skips npm install when no package.json" {
  # Test behavior for static HTML projects
}

@test "deploy_pi_backend handles SSH connection failure" {
  run deploy_pi_backend "test-pi" "192.168.0.999" "/path"
  [ "$status" -eq 1 ]
  [[ "$output" == *"Cannot connect"* ]]
}

@test "environment flags control deployment scope" {
  DEPLOY_FRONTENDS=false DEPLOY_WORKERS=false DEPLOY_PI=false DEPLOY_VPS=false \
    run ./blackroad-deploy-all.sh
  # Verify no deployments attempted
}
```

#### 2.2 `blackroad-netdump.sh`

**Testable Functions:**

| Function | Lines | Test Priority | Description |
|----------|-------|---------------|-------------|
| `section()` | 15-20 | Low | Output formatting |
| `subsection()` | 22-25 | Low | Output formatting |
| System checks | 45-268 | Medium | Various system queries |

**Recommended Test Cases:**

```bash
# tests/blackroad-netdump.bats

@test "handles missing commands gracefully" {
  # Mock missing 'docker' command
  run ./blackroad-netdump.sh
  [[ "$output" == *"Docker not installed"* ]]
}

@test "outputs valid timestamp format" {
  run ./blackroad-netdump.sh
  [[ "$output" =~ [0-9]{4}-[0-9]{2}-[0-9]{2} ]]
}
```

---

### 3. GitHub Actions Workflow Tests (Medium Priority)

#### 3.1 Brand Compliance Check

The current brand check in `.github/workflows/deploy.yml` has a **logical flaw**:

```yaml
# Current implementation (BUGGY):
if grep -r "#FF9D00\|#FF006B" . --include="*.html" --include="*.css"; then
  exit 1  # Fails if colors ARE found
fi
```

**Issue:** The check exits with failure when forbidden colors are found, but `generate_domains.py` line 187-191 explicitly uses these "forbidden" colors:
```python
--orange: #FF9D00;
--red: #FF006B;
--purple: #7700FF;
--blue: #0066FF;
```

**Recommended Tests:**

```yaml
# Test the brand compliance logic separately
- name: Test brand compliance checker
  run: |
    # Create test file with forbidden colors
    echo "<div style='color: #FF9D00'>" > /tmp/test.html

    # Should fail
    if ./scripts/check_brand_compliance.sh /tmp/test.html; then
      echo "FAIL: Should have detected forbidden color"
      exit 1
    fi

    # Create compliant file
    echo "<div style='color: #F5A623'>" > /tmp/test.html

    # Should pass
    ./scripts/check_brand_compliance.sh /tmp/test.html
```

---

### 4. Integration Tests (Lower Priority)

#### 4.1 End-to-End HTML Generation

```python
# tests/integration/test_full_generation.py

class TestFullGeneration:
    def test_generates_all_domain_pages(self):
        """Run full generation and verify all files created"""

    def test_generated_html_is_valid(self):
        """Parse generated HTML with BeautifulSoup/lxml"""

    def test_generated_html_matches_domain_config(self):
        """Cross-validate generated content with DOMAINS dict"""
```

#### 4.2 Deployment Dry Run

```python
# tests/integration/test_deployment_dry_run.py

class TestDeploymentDryRun:
    def test_deployment_would_succeed(self):
        """Mock wrangler and verify deployment commands are correct"""
```

---

## Recommended Test Infrastructure

### 1. Python Testing Setup

```
# requirements-dev.txt
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-mock>=3.10.0
beautifulsoup4>=4.12.0  # HTML validation
responses>=0.23.0       # HTTP mocking
```

```python
# pytest.ini or pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "--cov=. --cov-report=term-missing --cov-fail-under=80"
```

### 2. Bash Testing Setup

```bash
# Install bats
git clone https://github.com/bats-core/bats-core.git
cd bats-core && ./install.sh /usr/local
```

### 3. CI Integration

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  python-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements-dev.txt
      - run: pytest --cov --cov-report=xml
      - uses: codecov/codecov-action@v4

  bash-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: sudo apt-get install -y bats
      - run: bats tests/*.bats
```

---

## Priority Ranking

| Priority | Area | Effort | Impact |
|----------|------|--------|--------|
| 1 | Python unit tests for `generate_html()` | Low | High |
| 2 | Domain configuration validation | Low | Medium |
| 3 | Deployment function tests (mocked) | Medium | High |
| 4 | Fix brand compliance bug | Low | Medium |
| 5 | Bash script tests | Medium | Medium |
| 6 | Integration tests | High | Medium |

---

## Critical Bugs Found During Analysis

### Bug 1: Brand Compliance Check Contradiction

**Location:** `.github/workflows/deploy.yml:25` vs `generate_domains.py:187-191`

The workflow forbids colors (`#FF9D00`, `#FF006B`, `#7700FF`, `#0066FF`) that are explicitly used in the HTML template. This means:
- Either the brand compliance check is wrong
- Or all generated HTML is non-compliant

**Recommendation:** Clarify which colors are official, update either the check or the template.

### Bug 2: Hardcoded Path

**Location:** `generate_domains.py:375` and `deploy_domains.py:12`

```python
output_dir = "/Users/alexa/blackroad-domains/pages"  # macOS path
PAGES_DIR = "/Users/alexa/blackroad-domains/pages"
```

These paths are hardcoded to a specific user's machine and will fail on other systems.

**Recommendation:** Use relative paths or environment variables.

---

## Next Steps

1. **Set up pytest** with the recommended configuration
2. **Write tests for `generate_html()`** - highest value, lowest effort
3. **Add domain configuration validation tests** - catches typos in config
4. **Fix the brand compliance contradiction** - currently broken
5. **Replace hardcoded paths** with portable alternatives
6. **Add CI workflow for tests** - prevent regressions

---

## Summary

This infrastructure codebase manages 19 domains, 58 Cloudflare projects, and deployments to 7+ Raspberry Pis. Despite this critical role, it has **zero test coverage**. Adding tests to the areas identified above would:

- Prevent deployment failures caused by configuration errors
- Enable safe refactoring of deployment scripts
- Catch regressions before they reach production
- Document expected behavior for future maintainers

The highest-value starting point is **unit tests for `generate_html()`** and **validation of the DOMAINS configuration**, as these are the most frequently modified and have clear testable outputs.
