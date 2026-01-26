# CLAUDE.md - AI Assistant Guidelines for BlackRoad Domains

This file provides guidance for AI assistants (including Claude) working with this repository.

## Repository Overview

**BlackRoad Domains** is a domain management and infrastructure coordination repository for BlackRoad OS, Inc. It serves as the central source of truth for managing:

- **19 registered domains** (GoDaddy → Cloudflare DNS)
- **58+ Cloudflare Pages projects**
- **15 GitHub organizations**
- **40+ GitHub repositories**
- **Physical infrastructure** (Raspberry Pi cluster + DigitalOcean VPS)

**Organization:** BlackRoad OS, Inc.
**Owner:** Alexa Louise Amundson (CEO)
**Contact:** amundsonalexa@gmail.com | blackroad.systems@gmail.com

## Codebase Structure

```
blackroad-domains/
├── .github/workflows/       # CI/CD automation (5 workflows)
├── pages/                   # Generated HTML landing pages
├── [domain-directories]/    # Per-domain storage (35 directories)
│   ├── blackroad-io/
│   ├── lucidia-earth/
│   ├── blackroadquantum-com/
│   └── ... (with hyphen suffixes for URL variations)
├── *.md                     # Documentation files
├── *.sh                     # Deployment scripts
├── *.py                     # Python automation scripts
└── *.html                   # Generated HTML files
```

### Key Documentation Files

| File | Purpose |
|------|---------|
| `BLACKROAD_CANONICAL_TRUTH.md` | **Master source of truth** - Complete infrastructure details |
| `COMPLETE_DOMAIN_MASTER_LIST.md` | All 58 Pages projects with routing |
| `LUCIDIA_EARTH_INFRASTRUCTURE.md` | Lucidia metaverse platform setup |
| `GITHUB_CLOUDFLARE_AUTOMATION.md` | Deployment automation guide |
| `PI_DEPLOYMENT_REAL.md` | Raspberry Pi deployment guide |
| `QUICK_DEPLOY.md` | Fast reference for deployments |
| `CONTRIBUTING.md` | Contribution guidelines & brand compliance |

## Development Workflows

### Deployment Methods

**1. Cloudflare Pages (Primary)**
```bash
# Deploy specific project
wrangler pages deploy dist --project-name=<project>

# Deploy all domains
~/blackroad-deploy-all.sh
```

**2. GitHub Actions CI/CD**
- Pushes to `main` trigger `deploy.yml` → calls external workflow in `blackroad-deploy`
- PRs are auto-labeled (`labs` or `core`) and synced to Project #8
- CI failures automatically create GitHub issues

**3. Raspberry Pi Deployment**
```bash
# Manual deployment via SSH/SCP
# Docker containers on available ports
# Caddy reverse proxy + Cloudflare Tunnel
```

### GitHub Workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `core-ci.yml` | PR/Push to main | Guard rail + lint placeholder |
| `deploy.yml` | Push to main | Trigger Cloudflare deployment |
| `auto-label.yml` | PR opened | Auto-label PRs |
| `project-sync.yml` | PR opened | Sync to GitHub Project #8 |
| `failure-issue.yml` | Workflow failure | Create issues on CI failure |

### Useful Commands

```bash
# Deploy everything
~/blackroad-deploy-all.sh

# Network inventory
~/blackroad-netdump.sh

# Generate domain pages
python3 generate_domains.py

# Deploy with Python
python3 deploy_domains.py
```

## Code Conventions

### Commit Message Format

Use conventional commits with emojis:

```
✨ feat: Add new feature
🐛 fix: Fix bug
📝 docs: Update documentation
🎨 style: Improve styling
♻️ refactor: Refactor code
✅ test: Add tests
🔧 chore: Update config
```

### Brand Compliance (IMPORTANT)

**Required Colors:**
```css
--amber: #F5A623
--hot-pink: #FF1D6C      /* Primary Brand Color */
--electric-blue: #2979FF
--violet: #9C27B0
--black: #000000
--white: #FFFFFF
```

**Forbidden Colors (DO NOT USE):**
```
#FF9D00, #FF6B00, #FF0066, #FF006B, #D600AA, #7700FF, #0066FF
```

**Spacing System (Golden Ratio φ = 1.618):**
```css
--space-xs: 8px
--space-sm: 13px
--space-md: 21px
--space-lg: 34px
--space-xl: 55px
--space-2xl: 89px
--space-3xl: 144px
```

**Typography:**
- Font family: `-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', sans-serif`
- Line height: `1.618` (Golden Ratio)

### File Naming Conventions

- Domain directories use hyphens: `blackroad-io/`, `lucidia-earth/`
- Mirror directories have hyphen suffix: `blackroadio-/`, `lucidiaearth-/`
- HTML pages: `{domain-name}.html`
- Shell scripts: `{descriptive-name}.sh`

## Infrastructure Details

### Domain Groups

| Group | Domains |
|-------|---------|
| **Lucidia** | lucidia.earth (metaverse), lucidia.studio, lucidiaqi.com |
| **BlackRoad Core** | blackroad.io, blackroad.me, blackroad.company, blackroad.systems, blackroad.network |
| **Quantum** | blackroadquantum.com/info/net/shop/store, blackroadqi.com |
| **Blockchain** | roadchain.io, roadcoin.io |
| **AI** | blackroadai.com |
| **Other** | blackboxprogramming.io, blackroadinc.us |

### Physical Infrastructure

| Device | IP | Purpose |
|--------|-----|---------|
| Main Pi (Aria) | 192.168.4.64 | Primary server, 26+ Docker containers |
| Lucidia Pi | 192.168.4.38 | Backend API (3000), WebSocket (8080) |
| DigitalOcean VPS | 159.65.43.12 | Cloud compute |

### Cloudflare Configuration

- **Nameservers:** jade.ns.cloudflare.com, chad.ns.cloudflare.com
- **Account ID:** `463024cf9efed5e7b40c5fbe7938e256`
- **Zone ID (lucidia.earth):** `848cf0b18d51e0170e0d1537aec3505a`

## AI Assistant Guidelines

### When Modifying This Repository

1. **Read before writing** - Always understand existing code/docs before changes
2. **Preserve brand compliance** - Use only approved colors and spacing
3. **Update canonical docs** - Keep `BLACKROAD_CANONICAL_TRUTH.md` in sync
4. **Follow commit conventions** - Use emoji prefixes consistently
5. **Don't expose secrets** - Never commit API tokens or credentials

### Common Tasks

**Adding a new domain:**
1. Create directory: `mkdir {domain-name}/`
2. Add to `COMPLETE_DOMAIN_MASTER_LIST.md`
3. Update `BLACKROAD_CANONICAL_TRUTH.md`
4. Generate landing page via `generate_domains.py`
5. Deploy via `wrangler pages deploy`

**Updating documentation:**
1. Edit the relevant `.md` file
2. Keep `BLACKROAD_CANONICAL_TRUTH.md` as master reference
3. Ensure consistency across all docs
4. Use proper markdown formatting

**Troubleshooting deployments:**
1. Check `blackroad-deploy-all.sh` for deployment logic
2. Review workflow runs in GitHub Actions
3. Verify Cloudflare Pages project configuration
4. Check Raspberry Pi logs if Pi-hosted

### What NOT to Do

- Do not modify `.github/workflows/` without understanding impacts
- Do not use forbidden brand colors
- Do not commit sensitive credentials or API tokens
- Do not create new documentation files unnecessarily - update existing ones
- Do not change deployment scripts without testing

## Testing Checklist

Before submitting changes:

- [ ] Visual verification in browser
- [ ] Brand compliance (colors, spacing, typography)
- [ ] Documentation consistency
- [ ] No hardcoded secrets or credentials
- [ ] Commit messages follow conventions

## License

**Proprietary - BlackRoad OS, Inc.**

- ✅ Permitted: Testing, evaluation, educational purposes
- ❌ Prohibited: Commercial use, resale, redistribution without permission

For licensing inquiries: blackroad.systems@gmail.com
