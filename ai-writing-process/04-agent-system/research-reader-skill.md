# The Research Reader Skill

> **Context:** Research files are raw Perplexity output -- long, unstructured, mixed quality. The research-reader skill provides 9 extraction tools that turn those files into writer-ready and reviewer-ready content. It's the bridge between the research pipeline and the writing agents.

---

Here's the problem with research at scale: 180+ Perplexity responses across 12 chapters produce thousands of pages of raw output. Stats are buried in paragraphs. Quotes lack attribution confidence. Company examples repeat across files. No writer -- human or AI -- can efficiently process a 2,000-word research dump while maintaining creative flow.

The research-reader skill solves this with 9 targeted extraction tools. Each one answers a specific question a writer or reviewer has at a specific moment in their workflow.

## 9 Tools

| Tool | Purpose | Key Flag |
|------|---------|----------|
| `research_snapshot` | One-stop section overview | Start here always |
| `format_citations` | Citation-ready with footnote keys | `--section X.X` |
| `find_support` | Evidence for/against a thesis | `--counter` |
| `find_unused` | Compare draft vs available research | `--draft "path"` |
| `extract_stats` | Statistics with credibility scoring | `--min-credibility HIGH` |
| `extract_quotes` | Quotes with confidence scoring | `--min-confidence HIGH` |
| `list_research` | All available research files | -- |
| `search_research` | Keyword search across research | `--context 3` |
| `get_section_research` | All files for a section | -- |

The tools are Python scripts in `.claude/skills/research-reader/scripts/`. Every agent call runs them from the project root.

## The Starting Point: research_snapshot

Every writing and reviewing session starts here. One command returns a ranked overview of everything available for a section:

```bash
python .claude/skills/research-reader/scripts/research_snapshot.py 7 7.3
```

The output includes: ranked research files by relevance, top statistics with semantic labels, best quotes with attribution, key companies mentioned, and a suggested starting point. It's the table of contents for your research -- read this, then decide which deeper tools to use.

Without this, the writer agent would need to read every research file for every section. With 3-5 files per section and 7 sections per chapter, that's 20-35 file reads before writing starts. The snapshot compresses that to one call per section.

## Credibility and Confidence Scoring

Not all research is equal. A specific revenue figure from a company's annual report is more reliable than a round number from a blog post. A direct quote with full attribution (name, title, source) is more trustworthy than an unattributed fragment.

**Credibility scoring for statistics:**

| Level | Criteria | Example |
|-------|----------|---------|
| HIGH | Specific numbers, named sources, from answer files | "Harvey reached $100M ARR" from company review |
| MEDIUM | Context present, partial sourcing | "Estimated $50M revenue in 2024" |
| LOW | Round numbers, estimated, unverified | "Roughly 80% of companies" |

**Confidence scoring for quotes:**

| Level | Criteria | Example |
|-------|----------|---------|
| HIGH | Full attribution (name + title), complete sentence, structured source | Winston Weinberg, CEO Harvey |
| MEDIUM | Partial attribution, inline quote with context | "An engineering lead at Linear" |
| LOW | Unknown attribution or fragment | "One founder described it as..." |

Both the writer and reviewer use these filters. The writer uses `--min-credibility HIGH` to ensure every cited stat is solid. The reviewer uses the same filters to check whether high-value evidence was missed.

## Writer Workflow

Before writing ANY section, the writer agent runs these scripts in order:

1. **`research_snapshot`** -- get the overview, understand what's available
2. **`format_citations`** -- get citation-ready content with footnote keys already formatted for copy-paste
3. **`find_support`** -- find evidence for the section's key arguments (always use `--counter` for balanced writing)
4. **`extract_stats`** -- pull HIGH credibility statistics only
5. **`extract_quotes`** -- pull HIGH confidence quotes only

The first two are mandatory. The last three depend on the section -- some sections are argument-heavy and need `find_support`, others are example-heavy and need more stats and quotes.

The output from `format_citations` is designed for direct integration. Statistics come pre-formatted:

```markdown
Harvey reached $100M ARR in three years[^harvey-review]
```

References come pre-formatted:

```markdown
[^harvey-review]: Harvey Year in Review 2024 -- [harvey.ai](https://www.harvey.ai/year-in-review/2024)
```

The writer copies these into the section. No manual footnote creation, no hunting for URLs. This is why the book hit 775 citations -- making citation easy makes citation ubiquitous.

## Reviewer Workflow

The reviewer agent uses the same tools but in a different order with a different goal. The reviewer isn't looking for content to add. It's looking for content the writer *missed*.

1. **`find_unused`** -- priority: what HIGH credibility research was available but not used? This is the most actionable output for review
2. **`research_snapshot`** -- compare what's available vs. what was used
3. **`extract_stats` / `extract_quotes`** -- check if the strongest evidence made it into the draft

The `find_unused` tool compares the draft file against all research for that section and reports:

- Stats in research but not in draft (with count)
- Quotes in research but not in draft
- Companies mentioned in research but absent from draft
- A summary with total unused research pieces

When the reviewer finds a HIGH credibility stat that the writer missed, it flags the specific stat, the source file, and suggests where in the section it should be integrated. This is actionable review output -- not "needs more research" but "add $2,000+ monthly cost stat from `answers/s_4.3/01_tiered.md` after paragraph 3."

## What Makes This Work

The key design decision: the scripts are *extractors*, not *readers*. They don't dump entire research files into the agent's context. They parse, filter, rank, and return only what's relevant. This keeps the context window clean for the actual writing or reviewing work.

A research snapshot for one section might reference 5 files totaling 8,000 words but return a 400-word summary with the 3 most relevant stats, 2 best quotes, and a ranked file list. The agent gets what it needs without drowning in raw research.

The other key decision: credibility and confidence scoring happens at extraction time, not at write time. The writer doesn't need to evaluate whether a stat is trustworthy -- the extraction script has already made that judgment. This offloads a cognitive task from the creative process, keeping the writer focused on voice and argument rather than source evaluation.

---

**Deep dives:** [Chapter Writer Skill](chapter-writer-skill.md) | [Research Architecture](../05-research-pipeline/research-architecture.md) | [Synthesis and Extraction](../05-research-pipeline/synthesis-and-extraction.md)
