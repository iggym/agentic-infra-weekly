# Agentic Infra Weekly

A weekly publication on infrastructure and platform engineering for agentic AI systems. The site is published at https://iggym.github.io/agentic-infra-weekly/.

## What This Is

*Agentic Infra Weekly* covers the operational and architectural patterns that emerge when building systems where AI agents call tools, run code, or orchestrate infrastructure. Each issue explores one problem: a real incident, a design decision, or a technical pattern. Every claim is cited, every tool is real, and every architecture diagram is mapped to a production system.

Issues are published weekly and focus on:
- **Security & Governance**: Prompt injection, confused deputies, authorization at scale
- **AI Systems Engineering**: Model integration patterns, fallbacks, cost control
- **Kubernetes & DevOps**: Configuration management, canary deployments, validation
- **AI Platform Architecture**: Caching, inference optimization, batch processing
- **Developer Enablement**: Tooling workflows, AI-assisted coding, measurement
- **Observability**: Telemetry for agents, sampling strategies, cost attribution

## Repo Layout

```
├── index.html           # Card grid, search, sort, theme toggle
├── metadata.json        # Source of truth: issue index, bylines, topics
├── articles/            # Individual HTML issue pages (1 per week)
├── assets/              # Shared CSS/JS for articles (future)
├── docs/                # Master prompt and editorial guidelines
│   └── master-prompt-v1.md
├── scripts/             # Validation and generation tools
│   └── validate.py      # Checks metadata, article files, schema compliance
├── tasks/               # Improvement backlog with priority levels
│   └── improvements.md
└── .github/workflows/   # CI/CD
    └── validate.yml     # Runs metadata validator on PRs and pushes to main
```

## metadata.json Schema

Each entry describes one published issue:

```json
{
  "slug": "string",               // URL-safe identifier, used in filename
  "title": "string",              // Article headline
  "date": "YYYY-MM-DD",           // ISO 8601 publication date (2026 only)
  "week": "integer",              // ISO 8601 week number (1–53)
  "topic": "string",              // One of 7 canonical topics (see below)
  "description": "string",        // One-sentence summary for SEO/cards
  "filename": "string"            // File in articles/ directory
}
```

**Canonical topics:**
- Security & Governance
- AI Systems Engineering
- Kubernetes & DevOps
- AI Platform Architecture
- Developer Enablement
- Observability
- Platform Engineering

**Validation rules:**
- `filename` must exist in `articles/`
- `date` must be ISO 8601 and in 2026–2027
- `week` must be an integer 1–53
- `topic` must be in the canonical list
- Filenames and titles must be unique
- No orphan articles in `articles/` directory

## How to Publish an Issue

1. **Use the master prompt.** The editorial specification lives in `docs/master-prompt-v1.md`. It defines:
   - Structure: 11 sections (problem, bold reframe, evidence, grain of salt, action steps, first 24 hours)
   - Research rules: every claim must be cited, no invented tools or numbers
   - HTML contract: head tags (OG, Twitter, canonical), theme support, interactive components
   - Recall cards, architecture layers (6-layer model), concept maps, and citations
   
   Copy the prompt and use it to write your issue with an AI model.

2. **Generate the HTML.** The prompt defines an HTML contract. Either:
   - Use `scripts/template.py` (if updated) to render from a data structure, or
   - Write the HTML by hand following the contract
   
   Every article must have:
   - `<!DOCTYPE html>`, viewport meta, theme support (light/dark via CSS custom properties)
   - Skip link and sticky header with home link (`../index.html`) and theme toggle
   - Sections with H2 headings, prose, and optional interactives
   - Numbered citations list with links
   - No external CSS or JS files (inline or reference shared `assets/` when available)

3. **Add metadata.** Create an entry in `metadata.json` with:
   - Unique slug and filename
   - Publication date (ISO 8601)
   - Week number and canonical topic
   - One-sentence description

4. **Open a PR.** Title it `Issue NN: <Title>`. Include both the article HTML and the metadata entry.

5. **Run the validator locally:**
   ```bash
   python3 scripts/validate.py
   ```
   The CI workflow runs the same check on PRs.

6. **Merge to main.** GitHub Actions publishes to https://iggym.github.io/agentic-infra-weekly/ automatically.

## Preview Locally

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000 in a browser.

The index page loads `metadata.json` from the same origin and builds the card grid dynamically. All articles are self-contained HTML files.

## Improvements Backlog

See `tasks/improvements.md` for a detailed list of pending work, prioritized by:
- **P0**: Broken for readers right now
- **P1**: Content quality, consistency, and guardrails
- **P2**: Growth and nice-to-have features (RSS, sitemap, newsletter CTA)

Run the validator to check the current state:
```bash
python3 scripts/validate.py
```

## License

Content: Copyright 2026. License TBD.  
Code: MIT.
