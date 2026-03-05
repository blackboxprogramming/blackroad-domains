# BlackRoad Domains

**Owner:** Alexa Louise Amundson
**Organization:** BlackRoad OS, Inc.
**Email:** amundsonalexa@gmail.com | blackroad.systems@gmail.com
**Last Updated:** 2026-03-05

---

## Status

| System | Status |
|--------|--------|
| CI / Guard | `CORE CI` validates repo structure, HTML, YAML |
| Auto Deploy | Static site deploy to Cloudflare Pages on push to main |
| Security Scan | CodeQL + dependency review on PRs and weekly schedule |
| Self-Healing | Health checks every 6 hours with auto-rollback |
| Automerge | Dependabot PRs auto-approved and squash-merged |
| Domain Router | Cloudflare Worker routes all 19 domains to Pages projects |
| Dependabot | GitHub Actions updates weekly (Mondays) |

---

## Infrastructure

- **19 GoDaddy Registered Domains** (all on Cloudflare DNS)
- **58 Cloudflare Pages Projects**
- **15 GitHub Organizations**
- **40+ GitHub Repositories**
- **7 Physical Devices**
- **4 AI Platform Integrations**

---

## All 19 Registered Domains

### Lucidia
- lucidia.earth (Metaverse)
- lucidia.studio
- lucidiaqi.com

### BlackRoad Core
- blackroad.io (Main site)
- blackroad.me
- blackroad.company
- blackroad.systems
- blackroad.network

### AI & Quantum
- blackroadai.com
- blackroadqi.com
- blackroadquantum.com / .info / .net / .shop / .store

### Blockchain
- roadchain.io
- roadcoin.io

### Other
- blackboxprogramming.io
- blackroadinc.us

**Nameservers:** jade.ns.cloudflare.com, chad.ns.cloudflare.com

---

## Workflows

All GitHub Actions are **pinned to specific commit hashes** for supply-chain security.

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `auto-deploy.yml` | Push to main/master | Auto-detect project type, deploy to Cloudflare Pages or Railway |
| `automerge.yml` | PR events | Auto-approve and merge Dependabot minor/patch PRs |
| `core-ci.yml` | PRs and pushes | Validate repo structure, HTML files, YAML syntax |
| `deploy.yml` | Push to main/master | Direct static site deploy to Cloudflare Pages |
| `deploy-worker.yml` | Push to `workers/**` | Deploy domain router Cloudflare Worker |
| `auto-label.yml` | PR opened | Auto-label PRs as "labs" or "core" |
| `failure-issue.yml` | CI failure | Auto-create GitHub issues on CI failures |
| `project-sync.yml` | PR opened | Add PRs to project board |
| `security-scan.yml` | PRs, pushes, weekly | CodeQL analysis and dependency scanning |
| `self-healing.yml` | Every 6 hours | Health checks with auto-rollback |

---

## Cloudflare Worker

The domain router worker (`workers/domain-router/worker.js`) handles:
- Routing all 19 domains to their Cloudflare Pages projects
- `/api/health` endpoint for monitoring
- Security headers (HSTS, X-Frame-Options, Referrer-Policy)
- www subdomain support for all domains

Deploy manually:
```bash
cd workers/domain-router
wrangler deploy
```

---

## Quick Start

```bash
# Deploy static sites to Cloudflare Pages
wrangler pages deploy . --project-name=blackroad-domains

# Deploy domain router worker
cd workers/domain-router && wrangler deploy

# Deploy specific domain project
wrangler pages deploy blackroad-io/ --project-name=blackroad-io

# List all Cloudflare Pages projects
wrangler pages project list

# Run network inventory
./blackroad-netdump.sh
```

---

## Documentation

| File | Purpose |
|------|---------|
| `BLACKROAD_CANONICAL_TRUTH.md` | Master source of truth |
| `COMPLETE_DOMAIN_MASTER_LIST.md` | All domains and projects |
| `LUCIDIA_EARTH_INFRASTRUCTURE.md` | Infrastructure guide |
| `QUICK_DEPLOY.md` | Fast deployment reference |
| `ALL_DOMAINS_REFERENCE.md` | Domain routing details |
| `CONTRIBUTING.md` | Contribution guidelines |

---

## License & Copyright

**Copyright 2024-2026 BlackRoad OS, Inc. All Rights Reserved.**

**CEO:** Alexa Louise Amundson (Sole Stockholder)
**Incorporation:** Delaware C-Corporation

**PROPRIETARY AND CONFIDENTIAL** - This software is NOT open source.

### Usage Restrictions
- **Permitted:** Testing, evaluation, and educational purposes
- **Prohibited:** Commercial use, resale, or redistribution without written permission

### Enterprise Scale
- 30,000 AI Agents
- 30,000 Human Employees
- One Operator: Alexa Amundson (CEO)

### Stripe Products & Assets
All Stripe products, payment integrations, and digital assets are proprietary to BlackRoad OS, Inc.

### Contact
For commercial licensing inquiries: blackroad.systems@gmail.com

See [LICENSE](LICENSE) for complete terms.
