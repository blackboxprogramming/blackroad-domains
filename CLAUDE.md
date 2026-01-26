# CLAUDE.md - AI Assistant Guide for BlackRoad Domains

## Repository Overview

This repository manages the **BlackRoad Domains** infrastructure - a collection of static HTML landing pages and deployment automation for the BlackRoad OS ecosystem. It contains 19 GoDaddy-registered domains deployed across 58+ Cloudflare Pages projects.

**Owner:** Alexa Louise Amundson
**Organization:** BlackRoad OS, Inc.
**License:** Proprietary (testing/evaluation only - see LICENSE)

---

## Directory Structure

```
blackroad-domains/
├── .github/workflows/      # CI/CD - Cloudflare Pages deployment
│   └── deploy.yml          # Brand compliance check + auto-deploy
├── pages/                  # Generated subdomain HTML pages
│   ├── blackroad-io.html
│   ├── home-blackroad-io.html
│   ├── demo-blackroad-io.html
│   └── ...                 # 12+ subdomain landing pages
├── {domain-name}/          # Per-domain folders (e.g., blackroad-io/, lucidia-earth/)
│   └── index.html          # Landing page for that domain
├── deploy_domains.py       # Python deployment script (wrangler-based)
├── generate_domains.py     # HTML page generator
├── blackroad-deploy-all.sh # Master deployment orchestrator
├── blackroad-netdump.sh    # Network inventory collector
├── dashboard.html          # Domain overview dashboard
├── BLACKROAD_CANONICAL_TRUTH.md  # Infrastructure source of truth
├── COMPLETE_DOMAIN_MASTER_LIST.md
├── CONTRIBUTING.md         # Contribution guidelines with brand rules
└── LICENSE                 # Proprietary license
```

---

## Quick Reference

### Key Domains

| Domain | Purpose |
|--------|---------|
| `blackroad.io` | Main website |
| `lucidia.earth` | Metaverse flagship |
| `blackroadai.com` | AI platform |
| `blackroadqi.com` | Quantum intelligence |
| `blackroad.systems` | Systems dashboard |
| `blackroad.network` | Network infrastructure |

### Infrastructure

- **DNS/CDN:** All domains use Cloudflare (nameservers: jade/chad.ns.cloudflare.com)
- **Hosting:** Cloudflare Pages
- **CI/CD:** GitHub Actions → Cloudflare Pages
- **Backend:** Raspberry Pi cluster + DigitalOcean VPS

---

## Development Workflow

### Adding a New Domain Page

1. Create directory: `mkdir {domain-name}/`
2. Add `index.html` following brand guidelines (see below)
3. Commit and push to `main` branch
4. GitHub Actions auto-deploys to Cloudflare Pages

### Manual Deployment

```bash
# Deploy specific project via wrangler
wrangler pages deploy . --project-name={project-name}

# Run Python deployment script
python3 deploy_domains.py

# Run master deployment (includes Pis and VPS)
./blackroad-deploy-all.sh
```

### Testing Changes Locally

Simply open HTML files in a browser - all pages are static HTML with embedded CSS.

---

## Brand Guidelines (Enforced by CI)

The GitHub Actions workflow enforces brand compliance. **Violations will fail the build.**

### Official Colors (MUST USE)

```css
--amber: #F5A623
--hot-pink: #FF1D6C      /* Primary Brand Color */
--electric-blue: #2979FF
--violet: #9C27B0
--black: #000000
--white: #FFFFFF
```

### Forbidden Colors (DO NOT USE)

These will **fail CI/CD checks**:
- `#FF9D00`, `#FF6B00`, `#FF0066`, `#FF006B`
- `#D600AA`, `#7700FF`, `#0066FF`

### Spacing (Golden Ratio)

```css
--space-xs: 8px      /* Base */
--space-sm: 13px     /* 8 × 1.618 */
--space-md: 21px     /* 13 × 1.618 */
--space-lg: 34px     /* 21 × 1.618 */
--space-xl: 55px     /* 34 × 1.618 */
```

### Typography

```css
font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', sans-serif;
line-height: 1.618; /* Golden Ratio */
```

### Gradient Pattern

```css
background: linear-gradient(135deg,
  var(--amber) 0%,
  var(--hot-pink) 38.2%,    /* Golden Ratio */
  var(--violet) 61.8%,      /* Golden Ratio */
  var(--electric-blue) 100%);
```

---

## Commit Message Convention

Use emoji-prefixed conventional commits:

```
✨ feat: Add new feature
🐛 fix: Fix bug in component
📝 docs: Update documentation
🎨 style: Improve styling
♻️ refactor: Refactor code
✅ test: Add tests
🔧 chore: Update config
🌌 enhance: BlackRoad proprietary enhancement
🔒 security: Security-related changes
```

---

## Key Files Reference

| File | Purpose |
|------|---------|
| `BLACKROAD_CANONICAL_TRUTH.md` | Master infrastructure source of truth |
| `COMPLETE_DOMAIN_MASTER_LIST.md` | All 58 Pages projects and 19 domains |
| `CONTRIBUTING.md` | Contribution guidelines and brand rules |
| `.github/workflows/deploy.yml` | CI/CD pipeline with brand checks |
| `deploy_domains.py` | Python-based wrangler deployment |
| `blackroad-deploy-all.sh` | Full infrastructure deployment script |

---

## AI Assistant Guidelines

### When Working on This Repository

1. **Always check brand compliance** before modifying HTML/CSS files
2. **Never use forbidden colors** - they will fail the CI pipeline
3. **Preserve Golden Ratio spacing** (1.618) in layouts
4. **Keep pages static** - no build system required for landing pages
5. **Follow commit conventions** with emoji prefixes

### Common Tasks

**Adding a new subdomain page:**
```bash
# 1. Create the folder structure
mkdir newdomain-name/
touch newdomain-name/index.html

# 2. Use existing pages as templates
# Copy structure from blackroad-io/index.html

# 3. Ensure brand compliance before committing
```

**Checking brand compliance manually:**
```bash
# Look for forbidden colors
grep -r "#FF9D00\|#FF6B00\|#FF0066\|#FF006B\|#D600AA\|#7700FF\|#0066FF" . --include="*.html" --include="*.css"

# Should return no results for compliant code
```

**Deploying changes:**
```bash
git add .
git commit -m "✨ feat: Add new domain landing page"
git push origin main
# GitHub Actions handles deployment automatically
```

### Infrastructure Context

- This repo contains **landing pages only**, not application code
- Backend services run on Raspberry Pis (see `BLACKROAD_CANONICAL_TRUTH.md`)
- All DNS managed via Cloudflare
- Deployment is automatic on push to `main`

### Important Conventions

1. **All HTML files must be self-contained** - embed CSS in `<style>` tags
2. **Use semantic HTML5** elements
3. **Mobile-first responsive design** is expected
4. **Line height should be 1.618** (Golden Ratio)
5. **Dark theme by default** (black backgrounds, light text)

---

## Related Documentation

- `BLACKROAD_CANONICAL_TRUTH.md` - Complete infrastructure reference
- `CONTRIBUTING.md` - Detailed contribution guidelines
- `LUCIDIA_EARTH_INFRASTRUCTURE.md` - Infrastructure deep-dive
- `QUICK_DEPLOY.md` - Fast deployment reference

---

## Contact

**Email:** blackroad.systems@gmail.com
**Organization:** BlackRoad OS, Inc.

---

*"The road remembers everything. So do we."* 🛣️
