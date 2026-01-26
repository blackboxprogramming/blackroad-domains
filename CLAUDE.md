# CLAUDE.md - AI Assistant Guide for BlackRoad Domains

This file provides guidance for AI assistants (Claude, etc.) working with the BlackRoad Domains repository.

## Project Overview

**BlackRoad Domains** is an infrastructure management repository for BlackRoad OS, Inc. - a proprietary operating system designed to manage AI agents and enterprise operations at scale.

**Key Stats:**
- 19+ registered GoDaddy domains
- 58 Cloudflare Pages projects
- 15 GitHub organizations
- 40+ repositories
- Static HTML landing pages with deployment automation

**Owner:** Alexa Louise Amundson (CEO)
**License:** Proprietary (BlackRoad OS, Inc.)

## Repository Structure

```
blackroad-domains/
├── .github/workflows/       # CI/CD pipeline definitions
│   ├── core-ci.yml          # Core CI pipeline (lint, guard)
│   ├── deploy.yml           # Production deployment to Cloudflare
│   ├── project-sync.yml     # GitHub Project integration
│   ├── failure-issue.yml    # CI failure tracking
│   └── auto-label.yml       # Automatic PR labeling
├── pages/                   # Generated HTML landing pages (49 files)
├── [domain-dirs]/           # 38 domain directories (e.g., blackroad-io/, lucidia-earth/)
│   └── index.html           # Landing page for each domain
├── *.md                     # Documentation files (12 total)
├── *.sh                     # Deployment scripts
├── *.py                     # Python automation scripts
└── *.html                   # Root-level HTML files
```

### Key Documentation Files

| File | Purpose |
|------|---------|
| `BLACKROAD_CANONICAL_TRUTH.md` | Master source of truth for all infrastructure |
| `COMPLETE_DOMAIN_MASTER_LIST.md` | Complete inventory of all 58 Cloudflare Pages projects |
| `LUCIDIA_EARTH_INFRASTRUCTURE.md` | Metaverse platform architecture |
| `QUICK_DEPLOY.md` | Fast deployment reference and health checks |
| `CONTRIBUTING.md` | Contribution guidelines with brand compliance |
| `PI_DEPLOYMENT_REAL.md` | Raspberry Pi deployment system |

### Key Scripts

| Script | Purpose |
|--------|---------|
| `blackroad-deploy-all.sh` | Master deployment across all infrastructure |
| `deploy_all_domains.sh` | Deploy all domain HTML to Cloudflare Pages |
| `generate_domains.py` | Generate unique HTML landing pages |
| `deploy_domains.py` | Deploy generated HTML via wrangler |
| `blackroad-netdump.sh` | Network inventory collection |
| `add-github-actions-to-all-repos.sh` | Automate GitHub Actions setup |

## Development Workflows

### CI/CD Pipeline

1. **Pull Requests** trigger `core-ci.yml`:
   - Guard check for core repo
   - Lint placeholder (extensible)

2. **Push to main** triggers `deploy.yml`:
   - Uses external workflow from `blackboxprogramming/blackroad-deploy`
   - Deploys to Cloudflare Pages project `blackroad-io`

3. **Automation Bots**:
   - `project-sync.yml` - Adds PRs to GitHub Project
   - `failure-issue.yml` - Creates issues on CI failures
   - `auto-label.yml` - Labels PRs as "labs" or "core"

### Deployment Commands

```bash
# Deploy everything
./blackroad-deploy-all.sh

# Deploy specific project with wrangler
wrangler pages deploy dist --project-name=lucidia-earth

# Generate HTML pages
python3 generate_domains.py

# Deploy domains
python3 deploy_domains.py
```

## Brand System (MUST FOLLOW)

### Required Colors

```css
--amber: #F5A623
--hot-pink: #FF1D6C      /* PRIMARY - Use this most */
--electric-blue: #2979FF
--violet: #9C27B0
--black: #000000
--white: #FFFFFF
```

### Forbidden Colors (NEVER USE)

```
#FF9D00, #FF6B00, #FF0066, #FF006B, #D600AA, #7700FF, #0066FF
```

### Spacing System (Golden Ratio φ = 1.618)

```css
--space-xs: 8px       /* Base */
--space-sm: 13px      /* 8 × φ */
--space-md: 21px      /* 13 × φ */
--space-lg: 34px      /* 21 × φ */
--space-xl: 55px      /* 34 × φ */
--space-2xl: 89px     /* 55 × φ */
--space-3xl: 144px    /* 89 × φ */
```

### Typography

```css
font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', sans-serif;
line-height: 1.618; /* Golden Ratio */
```

### Gradients

```css
background: linear-gradient(135deg,
  var(--amber) 0%,
  var(--hot-pink) 38.2%,     /* Golden Ratio */
  var(--violet) 61.8%,       /* Golden Ratio */
  var(--electric-blue) 100%);
```

## Commit Message Format

Use conventional commits with emojis:

```
✨ feat: Add new feature
🐛 fix: Fix bug in component
📝 docs: Update documentation
🎨 style: Improve styling
♻️ refactor: Refactor code
✅ test: Add tests
🔧 chore: Update config
```

## Domain Naming Conventions

### Primary Domains
- Format: `[name].io`, `.earth`, `.com`, `.me`, `.systems`, `.network`, `.us`
- Examples: `blackroad.io`, `lucidia.earth`, `blackroadai.com`

### Pages Project Naming
- Format: Domain with hyphens instead of dots
- Examples: `lucidia.earth` → `lucidia-earth`, `blackroad.io` → `blackroad-io`

### Directory Naming
- Domain directories use hyphen format matching Cloudflare project names
- Trailing `-` variants exist for some domains (e.g., `blackroadio-`)

## Infrastructure Overview

### Cloudflare
- 58 Cloudflare Pages projects
- Cloudflare Workers for routing
- Cloudflare Tunnel for edge connectivity
- Nameservers: `jade.ns.cloudflare.com`, `chad.ns.cloudflare.com`

### Physical Hardware
- 3 Raspberry Pis on local network (192.168.4.x)
- 1 Cloud VPS (DigitalOcean)
- Docker containers (26+ per Pi)

### GitHub Organizations (15)
BlackRoad-OS, Blackbox-Enterprises, BlackRoad-AI, BlackRoad-Archive, BlackRoad-Cloud, BlackRoad-Education, BlackRoad-Foundation, BlackRoad-Gov, BlackRoad-Hardware, BlackRoad-Interactive, BlackRoad-Labs, BlackRoad-Media, BlackRoad-Security, BlackRoad-Studio, BlackRoad-Ventures

## Working with This Repository

### When Making Changes

1. **HTML Pages**: Edit files in domain directories or `pages/`
2. **Regenerate Pages**: Run `python3 generate_domains.py`
3. **Deploy**: Use wrangler or the deployment scripts
4. **Documentation**: Keep `.md` files in sync with changes

### Testing Checklist

- [ ] Visual test in multiple browsers
- [ ] Responsiveness on mobile/tablet/desktop
- [ ] Brand compliance (colors, spacing, typography)
- [ ] Accessibility (color contrast, keyboard navigation)

### PR Requirements

- Follow brand system guidelines
- Test on multiple browsers
- Update documentation as needed
- Use conventional commit format
- Include screenshots for UI changes

## Important Notes for AI Assistants

1. **Static Site**: This is primarily a static HTML site deployed to Cloudflare Pages. No build step required for most changes.

2. **Brand Compliance**: All UI changes MUST follow the brand system. Use only approved colors and golden ratio spacing.

3. **Documentation Heavy**: Extensive documentation exists. Reference `BLACKROAD_CANONICAL_TRUTH.md` for authoritative infrastructure details.

4. **Deployment**: Production deployments go through the external `blackroad-deploy` repository workflow.

5. **External Dependencies**: Uses `wrangler` CLI for Cloudflare, Python 3 for scripts, bash for deployment automation.

6. **No Package.json**: This is not a Node.js project. Domain directories contain static HTML files.

## Quick Reference URLs

- Main Site: https://blackroad.io
- Metaverse: https://lucidia.earth
- Dashboard: https://blackroad-io.pages.dev
- Docs: https://docs.blackroad.io

---

*Last Updated: 2026-01-26*
*Repository: blackroad-domains*
