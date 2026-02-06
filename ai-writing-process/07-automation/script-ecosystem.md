# Script Ecosystem

> **Context:** The writing system for *Blueprint for An AI-First Company* is backed by 17 Python scripts that handle everything from word counting to PDF generation to vault validation. This document maps the full ecosystem and explains when to use each script.

---

Here's the thing about book-scale writing: manual operations stop working somewhere around chapter 4.

At 81,000 words across 81 sections with 775 citations, you can't manually count words, check link integrity, or audit citation formats. The cognitive overhead eats into writing time. So we built scripts -- not as a planned architecture, but iteratively, each one solving a specific pain point as it emerged.

The 17 scripts fall into four categories: manuscript management, content validation, research enrichment, and infrastructure. Some run daily. Some ran once and changed the vault forever. All of them operate on the same Obsidian vault directory, take consistent CLI flags, and produce either rich terminal output or JSON for piping.

## Manuscript Management (4 Scripts)

These are the scripts you run every day. They answer the question: where am I?

| Script | What It Does | When to Use |
|--------|-------------|-------------|
| `word_count.py` | Counts words per section, chapter, part, and book -- excluding YAML frontmatter, Mermaid diagrams, reference sections, and HTML comments | Before and after writing sessions |
| `book_status.py` | Rich-formatted progress dashboard with color-coded status bars per chapter | Weekly check-ins, motivation |
| `daily_stats.py` | Tracks writing velocity, records daily snapshots, shows GitHub-style contribution graphs, calculates streaks | Daily -- can auto-record via git hook |
| `search_content.py` | Full-text search with regex support and context display across all manuscript files | When you need to find where you said something |

The word count script is the most used. The key design decision: what counts as "words." Raw file word counts are misleading when each file has 30 lines of YAML frontmatter, Mermaid diagrams with hundreds of words of syntax, and a references section with 20 URLs. `word_count.py` strips all of that and counts only the prose your reader will see.

```bash
# Full book count
python scripts/word_count.py --draft "Draft 3"

# Single chapter with per-section breakdown
python scripts/word_count.py --draft "Draft 3" --chapter 12 --verbose

# JSON output for tooling
python scripts/word_count.py --draft "Draft 3" --json
```

## Content Validation (4 Scripts)

These catch problems before they compound. A broken link in chapter 3 that references chapter 7 won't cause issues until someone follows it -- by which point you've published.

| Script | What It Does | When to Use |
|--------|-------------|-------------|
| `validate_vault.py` | Scans for broken wiki-links, missing frontmatter fields, orphan files, invalid tags | After batch operations, before PDF generation |
| `standardize_citations.py` | Finds duplicate URLs cited with different footnote tags, generates bibliography | After writing sessions with heavy citation work |
| `audit_citation_format.py` | Checks that citations follow the standard format: `[^key]: Source Name. [Title](URL)` | Before publication review |
| `fix_citation_format.py` | Auto-converts plain URL citations to markdown link format | When audit finds PLAIN_URL issues |

The citation scripts work as a pipeline. `audit_citation_format.py` identifies three issue types: PLAIN_URL (URL not in a markdown link), MISSING_SOURCE (no source name), and NO_URL (no URL at all). `fix_citation_format.py` auto-fixes the first type. `standardize_citations.py` handles the broader problem of the same URL appearing under different footnote tags across sections.

```bash
# Audit citations (find problems)
python scripts/standardize_citations.py

# Preview fixes without applying
python scripts/standardize_citations.py --fix --dry-run

# Apply fixes
python scripts/standardize_citations.py --fix

# Generate book-wide bibliography
python scripts/standardize_citations.py --bibliography
```

## Research & Enrichment (4 Scripts)

These scripts ran in bursts -- typically once per major phase -- and transformed the vault's structure.

| Script | What It Does | When to Use |
|--------|-------------|-------------|
| `add_research_frontmatter.py` | Batch-adds YAML frontmatter to research files with chapter links, concept detection | After importing new research |
| `enrich_research_files.py` | Adds related chapter links, index links, and concept links to research files | After research pipeline runs |
| `enrich_section_frontmatter.py` | Analyzes section content and adds concept links, related sections, breadcrumb hierarchy | Once per draft, or when sections are restructured |
| `download_blog_articles.py` | Downloads and caches blog content from RSS feeds as JSON for voice reference | Once during setup |

The enrichment scripts are the unsung heroes. `enrich_section_frontmatter.py` ran once and added 555 new links to the vault, moving section-to-concept coverage from 0% to 68%. It analyzes the text of each section, matches against concept keyword mappings, and adds `key_concepts`, `related_sections`, and breadcrumb `up` links to the frontmatter. One batch operation made the vault's graph view actually useful.

```bash
# Preview what would change
python scripts/enrich_section_frontmatter.py

# Apply concept links and hierarchy
python scripts/enrich_section_frontmatter.py --apply

# Only process one chapter
python scripts/enrich_section_frontmatter.py --chapter 6 --apply
```

## Infrastructure (5 Scripts)

These handle output generation, structural analysis, and project management.

| Script | What It Does | When to Use |
|--------|-------------|-------------|
| `generate_pdf.py` | Converts markdown to PDF via WeasyPrint, with Mermaid rendering and caching | When you need a PDF for review or distribution |
| `graph_health_report.py` | Analyzes link density, orphan nodes, concept coverage, calculates health score (0-100) | Weekly structural check |
| `book_tui.py` | Terminal UI with keyboard navigation to access 7 core scripts | When you can't remember script names |
| `backup_commit.py` | Smart git commits with auto-generated messages based on what changed | End of writing sessions |
| `convert_to_github.py` | Transforms Obsidian format (wiki-links, frontmatter, internal blocks) to GitHub-compatible markdown | When publishing to external repository |

`convert_to_github.py` deserves a note. Obsidian markdown isn't standard markdown. Wiki-links like `[[concepts/Data Flywheel|Data Flywheel]]` don't render on GitHub. Internal comment blocks like `<!-- INTERNAL: Research Sources -->` should be stripped. The converter handles link resolution, navigation generation, and content cleaning to produce a publish-ready repository.

## The TUI

`book_tui.py` wraps the 7 most-used scripts in a terminal menu built with the `pick` library. Arrow keys to navigate, Enter to select, then it prompts for parameters with sensible defaults and presets.

The TUI registers scripts with typed parameters (bool, int, string, path, choice) and named presets. For example, `daily_stats` has presets for "today" (view stats), "record" (save snapshot), "week" (7-day history), and "streak." You pick a preset or configure manually.

It's a small convenience that eliminates the friction of remembering `python scripts/daily_stats.py --history 7 --graph`. When you're in flow, that friction matters.

## Design Principles

Every script follows the same patterns:

1. **Vault-relative paths.** Scripts resolve the vault directory from their own location. No hardcoded paths. Pass `--vault /path/to/vault` to override.
2. **Dry-run modes.** Any script that modifies files supports `--dry-run` to preview changes. This isn't optional -- batch operations on 81 files with one typo in the regex can ruin an afternoon.
3. **Rich output with fallback.** Scripts use the `rich` library for colored tables and progress bars but fall back to plain text if it's not installed. The output is meant to be readable at a glance.
4. **JSON output.** Every script with data output supports `--json` for piping to other tools or for the book intelligence app to consume.
5. **Graceful dependency handling.** Missing optional libraries get helpful install messages rather than stack traces.

The scripts grew organically, but the patterns stayed consistent. That consistency means any new script plugs in without surprises.

---

**Deep dives:** [PDF Generation](pdf-generation.md) | [Writing Analytics](writing-analytics.md) | [Vault Health](vault-health.md)
