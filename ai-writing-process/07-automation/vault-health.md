# Vault Health

> **Context:** An Obsidian vault with 200+ files and 1,199 links needs structural monitoring. Three tools handle this: `validate_vault.py` catches broken links and missing metadata, `graph_health_report.py` analyzes connectivity and scores overall health, and `enrich_section_frontmatter.py` performs batch operations that transformed vault structure.

---

Here's what most people get wrong about Obsidian vaults for book writing: they treat linking as decoration. A wiki-link here, a backlink there, maybe a concept note when they remember. The vault works fine with 20 files. At 200+, it becomes a liability -- broken links everywhere, orphan files nobody references, sections that exist in isolation with zero cross-chapter connections.

Vault health isn't about aesthetics. It's about whether your knowledge graph actually helps you write. A section on "data flywheels" in chapter 9 should link to the concept note, which should link back to the three other chapters that discuss flywheels. Without that structure, you're maintaining 81 disconnected documents instead of one interconnected book.

## Vault Validation

`validate_vault.py` is the first line of defense. It scans every markdown file in the vault and reports four types of problems:

**Broken wiki-links.** Any `[[target]]` where the target file doesn't exist. This happens constantly -- you rename a file, restructure a chapter folder, or typo a concept name. The script normalizes links, checks against a full file index (by stem and by relative path), and tries common prefixes (`concepts/`, `notes/`, `mocs/`) before flagging a link as broken.

**Missing frontmatter.** Chapter and section files have required fields: `type`, `status`, `chapter`, `part`. The script checks files under `Book/drafts/` and flags any that are missing required metadata. Incomplete frontmatter breaks Dataview queries, which breaks your dashboards.

**Orphan files.** Files that exist but nothing links to them. The script builds a set of all link targets across the vault and identifies files that never appear as a target. These are either forgotten drafts, deprecated notes, or files that need integration.

**Invalid tags.** Tags used in content that don't match the approved tag index. This prevents tag sprawl -- without it, you end up with `#agents`, `#agent`, `#ai-agents`, and `#agent-architecture` all meaning the same thing.

```bash
# Full validation
python scripts/validate_vault.py

# Only check links (fastest)
python scripts/validate_vault.py --links

# Only check frontmatter
python scripts/validate_vault.py --frontmatter

# Errors only, no warnings
python scripts/validate_vault.py --quiet
```

The script exits with code 1 if errors exist, code 0 if clean. This makes it usable in CI pipelines or pre-commit hooks -- though for a solo writing project, running it manually after batch operations is enough.

## Graph Health Report

`graph_health_report.py` goes deeper than validation. It doesn't just find broken things -- it measures how well the vault is connected and produces a health score from 0 to 100.

The analysis runs in two passes. First pass: index every file, extract all wiki-links (from both content and frontmatter), classify each file by type (concept, chapter, section, MOC, research, case study). Second pass: calculate inlinks by checking who points to whom.

The health score penalizes four things:

| Factor | Weight | What It Measures |
|--------|--------|-----------------|
| Orphan ratio | Up to -30 points | Percentage of files with fewer than 3 connections |
| Concept coverage | Up to -30 points | Percentage of sections that link to at least one concept note |
| Average link density | Up to -20 points | Mean outlinks per file (target: 3+) |
| Bidirectional gaps | Up to -20 points | One-way links that should be reciprocated |

Each file type has a target link density: concepts should have 8+ links, chapters 10+, sections 5+, MOCs 15+. The report shows actual vs target per type, color-coded green/yellow/red.

```bash
# Full report with health score
python scripts/graph_health_report.py

# One-line summary
python scripts/graph_health_report.py --brief

# Show orphan files that need attention
python scripts/graph_health_report.py --orphans

# JSON for the book intelligence app
python scripts/graph_health_report.py --json
```

The recommendations section is actionable. It doesn't just say "improve concept coverage." It says "Add key_concepts to sections (26 sections missing)" with the exact count. You know what to fix and how much work it is.

## The Enrichment Story

Here's where the numbers get interesting. Before running `enrich_section_frontmatter.py`, the vault was structurally flat. Sections had their content but almost no metadata linking them to the broader vault. The graph view in Obsidian showed clusters of files connected to their chapter and nothing else.

The enrichment script analyzed the text of all 81 sections, matched content against concept keyword mappings (e.g., "flywheel," "feedback loop" -> Data Flywheel concept), and added three types of frontmatter links:

1. **`key_concepts`** -- Links to concept notes based on content analysis
2. **`related_sections`** -- Links to other sections in the same chapter
3. **`up`** -- Breadcrumb hierarchy links (Section -> Chapter -> Part -> Book)

It also supports `--sequence` mode for adding `next`/`prev` navigation links between consecutive sections.

One batch run. Here's what changed:

| Metric | Before | After |
|--------|--------|-------|
| Section-to-concept links | 0% | 68% |
| Average links per section | ~1 | 7.0 |
| Total vault links | ~630 | 1,199 |
| Concept notes referenced | 0 | 9 |
| Graph health score | ~45 | ~75 |

That's 555 new links from a single script execution. The graph view went from disconnected clusters to a web where you could trace a concept across chapters. Backlinks became useful -- clicking on a concept note showed every section that discusses it.

```bash
# Preview changes (always preview first)
python scripts/enrich_section_frontmatter.py

# Apply all enrichment
python scripts/enrich_section_frontmatter.py --apply

# Only add breadcrumb hierarchy
python scripts/enrich_section_frontmatter.py --hierarchy --apply

# Only add next/prev sequence links
python scripts/enrich_section_frontmatter.py --sequence --apply

# Target a single chapter
python scripts/enrich_section_frontmatter.py --chapter 6 --apply
```

## Maintenance Cadence

These tools aren't daily scripts. They're checkpoints.

| When | What to Run | Why |
|------|------------|-----|
| After any batch operation | `validate_vault.py` | Catch anything that broke |
| After adding sections or restructuring | `enrich_section_frontmatter.py --apply` | Rebuild concept links |
| Weekly | `graph_health_report.py` | Catch structural drift |
| Before PDF generation | `validate_vault.py --links` | Don't bake broken links into the PDF |
| Before publication review | `graph_health_report.py --orphans` | Find forgotten content |

The pattern: validate after changes, analyze weekly, enrich after structural changes. Running validation after every writing session is overkill -- the scripts that modify files (enrichment, citation fixing) are the ones that can introduce breakage. Run validation after those.

One thing I learned the hard way: always run enrichment with no flags first (preview mode) before `--apply`. The preview shows exactly which files will change and what will be added. I once ran `--apply` without previewing and it added concept links to every section -- including sections where the concept was mentioned in passing and the link was misleading. Preview, review, apply. In that order.

---

**Related:** [Script Ecosystem](script-ecosystem.md) | [Linking and Navigation](../06-obsidian-vault/linking-and-navigation.md) | [Quality Skills](../04-agent-system/quality-skills.md)
