# Citation Management

775 citations across 81 sections. That number wasn't a target -- it was a side effect of making citation *cheap*. When the research pipeline pre-stages evidence with footnote keys, you cite. When you have to stop writing to hunt for a URL, you don't. The system changed the economics, and the citation density followed.

But 775 citations across 12 chapters creates its own management problem. Duplicate URLs with different tags. Inconsistent formatting. Sections with 15 citations next to sections with 2. Without tooling, citation quality degrades as the manuscript grows.

---

## Citation Format

Every citation uses markdown footnotes with named keys:

```markdown
Harvey reached $100M ARR in three years[^harvey-arr].

## References

[^harvey-arr]: Harvey Year in Review 2024 -- [harvey.ai](https://www.harvey.ai/year-in-review/2024)
```

The format has three parts: an inline reference (`[^harvey-arr]`), a definition at the bottom of the section (`[^harvey-arr]: ...`), and a URL wrapped in a markdown link. This works natively in Obsidian's reading view and converts cleanly to PDF.

Each section file maintains its own `## References` block at the end. Cross-section citation deduplication happens at the book level via automation, not manually.

---

## What to Cite vs. What Not To

This distinction matters more than it sounds. Over-citing makes prose read like an academic paper. Under-citing makes it read like opinion.

| Cite | Don't Cite |
|------|-----------|
| "Harvey reached $100M ARR in three years" | "Harvey is a legal AI company" |
| "85% of enterprises plan AI adoption by 2026" | "Enterprise AI adoption is growing" |
| Direct quotes from founders and CTOs | Author's analysis and opinions |
| Specific numbers, percentages, dollar amounts | General industry descriptions |
| Methodology details ("surveyed 1,000 enterprises") | Widely known facts |

The rule of thumb: if removing the claim would weaken the argument, cite it. If it's context-setting or common knowledge, don't. "Stripe processes billions in payments" doesn't need a citation. "Stripe's ML-based fraud detection reduces false positives by 25%" does.

---

## One Tag Per Source URL

This rule prevents the most common citation mess: the same source appearing with different footnote tags across sections.

```markdown
# Correct -- same source, same tag:
Glean's CEO described enterprise search as "a knowledge graph problem"[^glean].
The Knowledge Graph takes 12-18 months to mature[^glean].

[^glean]: Contrary Research -- [Glean Profile](https://research.contrary.com/company/glean)

# Wrong -- same source, different tags:
Glean's CEO quote[^glean-quote].
Knowledge Graph maturity[^glean-graph].

[^glean-quote]: Contrary Research -- https://research.contrary.com/company/glean
[^glean-graph]: Contrary Research -- https://research.contrary.com/company/glean  # DUPLICATE URL!
```

In Obsidian's reading view, repeated references to the same footnote render as `[3]`, `[3-1]`, `[3-2]` -- making it clear they reference the same source. Different tags pointing to the same URL create false variety and inflate the bibliography.

---

## Citation Audit Script

`standardize_citations.py` is the automated enforcer. It scans every section file and catches problems before they compound:

```bash
# Audit mode -- report issues without changing anything
python scripts/standardize_citations.py

# Fix duplicate tags (preview first)
python scripts/standardize_citations.py --fix --dry-run

# Apply fixes
python scripts/standardize_citations.py --fix

# Generate book-wide bibliography
python scripts/standardize_citations.py --bibliography
```

The script identifies duplicate URLs with different footnote tags, standardizes the citation format, and can generate a consolidated bibliography across all 12 chapters. The `--dry-run` flag is non-negotiable before any automated fix -- you preview every change before it touches a file.

---

## Citation Density

The target was roughly 1 citation per 150 words -- about 8-10 citations per 1,200-word section. The actual density came in higher: 1 citation per 105 words (775 citations across 81,122 words).

That overshoot wasn't a problem. It happened because the research-first pipeline made evidence so accessible that writers naturally used more of it. The key metric isn't density alone -- it's *appropriate* density. Stats and quotes should be cited. Analysis and opinion shouldn't. A section about the economics of AI infrastructure might have 12 citations (lots of numbers). A section about organizational culture might have 5 (more opinion, fewer stats). Both are fine.

---

## Internal Research Tracking

Every section includes a hidden block that tracks which research files informed the writing. This doesn't appear in the reader-facing PDF but shows up in internal review mode:

```markdown
<!-- INTERNAL: Research Sources
- [[research/Chapter_01/answers/s_1.2/01_ai_first_vs_enabled|AI-First Research]]
- [[research/Chapter_01/web_research/s_1.2_ai_first_vs_enabled|Web Research]]
-->
```

This serves two purposes: reviewers can trace any claim back to its research source, and the `find_unused.py` script can compare what research was available versus what actually got used -- highlighting evidence that might strengthen a section.

---

## Fact Verification Protocol

For any new fact added during editing -- not from the original research pipeline -- there's a verification sequence:

1. **Search** to confirm the claim is accurate
2. **Find the primary source** (not a secondary blog post citing someone else)
3. **Extract the exact URL** from the source
4. **Add the footnote citation** with proper formatting
5. **If verification fails, don't add the fact.** No citation, no claim.

This sounds rigid. It is. The alternative is a published book where someone Googles one of your stats and finds it's wrong. That destroys credibility on every other stat in the chapter, cited or not.

---

## The Workflow in Practice

During a typical writing session, citations flow through three stages:

**Stage 1: Pre-staged.** The research pipeline produces citation-ready content via `format_citations.py`. Stats already have footnote keys. The writer agent pastes them directly into prose.

**Stage 2: Writer-added.** The writer agent encounters a claim that needs evidence but isn't in the pre-staged research. It searches via `search_research.py` or `extract_stats.py`, finds the stat, formats the citation inline.

**Stage 3: Reviewer-caught.** The reviewer agent scans the draft for statistical claims without citations. It flags them. The writer either adds a citation or reframes the claim as opinion.

Most citations (roughly 70%) come from Stage 1 -- pre-staged by the research pipeline before writing begins. That's the point. Front-loading research makes citation a byproduct of writing, not an interruption.

---

**Related:** [Research Architecture](research-architecture.md) | [Synthesis and Extraction](synthesis-and-extraction.md) | [Quality Skills](../04-agent-system/quality-skills.md) | [Script Ecosystem](../07-automation/script-ecosystem.md)
