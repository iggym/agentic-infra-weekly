# Improvement Tasks — Agentic Infra Weekly

This list comes from an audit of the repo on 2026-10-06. It covered `index.html`, `metadata.json`, and all 23 files in `articles/`. Tasks are grouped by priority. Each one says what was found and what "done" means.

Legend: **P0** = broken for readers now · **P1** = quality/consistency · **P2** = growth/nice-to-have

---

## P0 — Broken right now

### ✅ T1. Fix the two metadata entries whose article file doesn't exist
- `articles/golden-paths-global-craters.html` (week 30): the file is missing. The card links to a 404.
- `articles/watching-the-wrong-dial.html` (week 21.1): the file is missing. The card links to a 404.
- **Done when:** each entry either has its article committed or is removed from `metadata.json`.

### T2. Week numbers never show, and "Sort by week" does nothing
- In `index.html`, `validateArticle()` runs `cleanText(raw.week, '')`. `cleanText` only accepts strings, but `week` is a number in `metadata.json`, so every article ends up with `week = ''`. As a result, the "Week N" label never renders on cards or the hero, the `week` sort compares `0` with `0`, and you can't search by week.
- **Fix:** `var week = (typeof raw.week === 'number' || typeof raw.week === 'string') ? String(raw.week).trim() : '';`
- **Done when:** cards show "Week 31" and so on, and sorting by week reorders the grid.

### ✅ T3. Remove the duplicate article entry
- `articles/paved-with-good-intentions.html` appears twice: week 12 (2026-03-16) and week 18.2 (2026-04-27).
- **Done when:** each file appears in `metadata.json` exactly once, and the correct week/date is kept.

### T4. Correct the wrong dates
- Week 21.1 `watching-the-wrong-dial` is dated `2024-05-22`, and week 21.3 `automating-the-outage` is dated `2024-05-21`. They should be 2026, so right now they sort to the bottom.
- `harness-over-horsepower` has `research_window: 2025-03-10 to 2025-03-16` for a 2026-07-29 issue, and its byline says "July 2025".
- **Done when:** all dates fit the 2026 publishing timeline, and each article's byline matches its metadata.

### T5. Fix the broken home link in "The Drift You Can't See"
- `articles/2026-07-06-the-drift-you-cant-see.html` uses `href="/"`. On GitHub Pages that goes to `iggym.github.io/`, not to the site.
- **Done when:** it links to `../index.html`, the same as the other articles (see T9).

---

## P1 — Content quality & consistency

### T6. Remove invented tools and unsourced claims from published issues
- Several "action step" sections recommend tools that don't seem to exist (for example, `RouteLens`, `CostScope`, and `HarnessBuilder` in *Harness Over Horsepower*, and `RouteOptimus` and `LatencyBudget` in *The Routing Robin Hood*).
- Some specific claims about named companies have no citation (for example, Cursor "downgrading the model mid-flight", or GitLab's "40% budget waste").
- **Done when:** every article has been reviewed. Each invented tool is replaced with a real one or a plain technique. Each unsourced number is either cited or removed. Each article ends with a numbered citations list that has links.

### T7. Adopt the master prompt for all new issues
- Use `docs/master-prompt-v1.md` for issue 32 onward, and run its pre-publish checklist on each PR.
- **Done when:** the next issue is produced with the prompt, and its checklist is pasted into the PR description.

### T8. Normalize week numbering
- Decimal weeks (`27.1`, `21.3`, `18.2`) are a workaround for having several issues in one week. They look odd and `21.3 > 21.2` doesn't mean anything to readers.
- **Fix:** make `week` an integer everywhere, and order same-week issues by `date` and then array position. Optionally add an `issue` field (a running issue number) to show instead.
- **Done when:** there are no decimal weeks, and the index has a stable tiebreak.

### T9. Unify the article template
- Articles use at least three different templates. They differ in title format (`Title — Agentic Infra Weekly` vs `Title`), header (`.hero-title` vs `.article-title` vs a plain `h1`), nav, and theme support. Only one article has a light theme.
- **Fix:** extract a shared `assets/article.css` (and optionally `assets/article.js` for recall cards, the diagram, the concept map, and the theme toggle) built on the same design tokens as `index.html`. Move the articles onto it step by step.
- **Done when:** every article shares the header/footer markup, home link, theme toggle (`aiw:theme`), and title format.

### T10. Add SEO and social metadata to every article
- None of the 23 articles has OG tags or a canonical URL, and 22 of 23 have no `<meta name="description">`. The index page has no OG tags either.
- **Done when:** every page has `description`, `canonical`, `og:title`, `og:description`, `og:url`, `og:type`, and `twitter:card`. Ideally it also has a default `og:image` (a 1200×630 site card).

### T11. Accessibility pass on article interactives
- Check that recall cards, hoverable architecture layers, and concept-map nodes work with the keyboard (focusable, Enter/Space, `aria-expanded`). Several say "Hover or tap", which leaves keyboard users out.
- Check contrast for muted text in both themes, and check that `prefers-reduced-motion` is respected.
- **Done when:** each article passes an axe/Lighthouse accessibility audit with a score of at least 95.

### T12. Normalize topic taxonomy
- There are 7 topics in use, and *Harness Over Horsepower* is tagged `Observability` in metadata but shows `AI Platform Architecture` on the page.
- **Done when:** the canonical list lives in one place (the master prompt plus validation, see T14), and every article's on-page topic matches its metadata.

### T13. Write a real README
- `README.md` contains only the repo name.
- **Done when:** the README covers what the publication is, the site URL, the repo layout (`index.html`, `metadata.json`, `articles/`, `docs/`, `tasks/`), the `metadata.json` schema, how to publish an issue (link the master prompt), and how to preview locally (`python3 -m http.server`).

---

## P1 — Automation & guardrails

### T14. Add a metadata/article validation check in CI
- Add a GitHub Action (and a local script, e.g. `scripts/validate.py`) that fails when any of these is true:
  - `metadata.json` is not valid JSON, or an entry is missing a required field
  - a `filename` doesn't exist, or a file in `articles/` isn't listed (orphan)
  - there are duplicate filenames or duplicate titles
  - a `date` isn't ISO `YYYY-MM-DD`, or falls outside a sane range
  - `topic` isn't in the canonical list, or `week` isn't an integer
  - an article has no `<title>`, no `meta description`, or uses `href="/"`
- **Done when:** the check runs on every PR, and the current repo passes after T1–T5.

### T15. Add a link checker
- Run `lychee` (or similar) on a weekly schedule and on PRs to catch dead citation links and broken internal anchors.
- **Done when:** a scheduled workflow reports broken links as an issue or a failing check.

### T16. Write meaningful commit messages and use PRs for new issues
- The history includes misleading messages (for example, "Update print statement from 'Hello' to 'Goodbye'", which actually added `now-you-dont.html`) and many bare "Update metadata.json" commits.
- **Done when:** a new issue lands as one PR titled `Issue NN: <Title>` that contains both the article and its metadata entry.

---

## P2 — Site features & growth

### T17. RSS/Atom feed
- Generate `feed.xml` from `metadata.json` (with a script in CI, or by hand per issue), and link it from `<head>` with `<link rel="alternate" type="application/rss+xml">`.

### T18. Sitemap and robots.txt
- Generate `sitemap.xml` from `metadata.json`, and add `robots.txt` pointing to it.

### T19. Favicon and site card
- Add an SVG favicon and a default `og:image`. The site has neither right now.

### T20. Previous/next and related-issue links
- At the bottom of each article, link the previous and next issue and up to 3 issues on the same topic. This could be built at render time from `metadata.json` with a small shared script (depends on T9).

### T21. Newsletter / subscribe call to action
- Add an email subscribe option (Buttondown, Substack embed, or a link to the RSS feed) on the index page and at the end of each article.

### T22. Privacy-friendly analytics (optional)
- If you want readership numbers, add a cookieless analytics option (Plausible or GoatCounter). Document it in the README.

### T23. Series / themes view
- Several issues form arcs: paved paths ×5, blind spots ×3, wolves/alerting ×2. Add an optional `series` field in metadata and a series filter on the index, so the repetition becomes a deliberate series instead of looking like duplication.

### T24. Make `index.html` easier to maintain
- `index.html` is a single 43 KB file. Consider splitting CSS and JS into `assets/` (shared with articles via T9), adding a `<noscript>` fallback list of issues, and preloading `metadata.json`.

---

## Suggested order

1. T1–T5 (quick fixes, one PR)
2. T14 (lock in the fixes with CI)
3. T13 and T7 (README and the master prompt workflow)
4. T9 → T10 → T11 (template unification unlocks SEO and accessibility at scale)
5. T6 (content audit, which can run in parallel)
6. P2 items as capacity allows
