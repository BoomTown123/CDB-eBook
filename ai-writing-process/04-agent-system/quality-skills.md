# Quality Skills

> **Context:** Six automated analysis skills audit every chapter across voice, citations, research, links, openings, and vocabulary. The `review-chapter` skill runs all six and produces a unified dashboard with a weighted health score.

---

Manual quality review doesn't scale. You can read a chapter and feel that something is off, but you can't reliably detect that the same opening pattern appears in 5 of 7 sections, or that citation density drops by 40% in the back half of the chapter, or that a concept mentioned in Chapter 4 has zero cross-references from Chapter 9. Automated skills catch the patterns humans miss.

## 6 Analysis Skills

The `review-chapter` skill orchestrates all six and produces a single dashboard:

| Skill | What It Checks | Score Weight |
|-------|---------------|-------------|
| `check-voice` | Kill list violations, hedging, AI patterns, approved markers | 25% |
| `check-citations` | Citation density, uncited stats, citation format | 20% |
| `map-research` | Research coverage gaps, orphan research, cross-chapter opportunities | 20% |
| `audit-links` | Cross-chapter links, island sections, hub sections | 15% |
| `audit-openings` | Opening pattern variety, repetitive starts | 10% |
| `analyze-terms` | Overused terms, synonym suggestions | 10% |

The weights reflect priority. Voice is 25% because if the book doesn't sound like one person wrote it, nothing else matters. Citations and research share 40% because credibility is what separates a serious book from AI-generated filler. Links, openings, and terms handle the polish layer.

## Voice Scoring (check-voice)

This skill is the most nuanced. It starts with a base score of 70 and adjusts based on what it finds:

| Pattern Type | Score Impact | Max Contribution |
|-------------|-------------|-----------------|
| Approved voice patterns ("Here's the thing," "What does X look like?") | +1 each | +15 |
| Personal markers (specific opinions, I've-seen-this moments) | +2 each | +10 |
| Kill list violations ("important to note," "let's delve") | -3 each | No limit |
| Hedging patterns ("somewhat," "arguably," "it could be said") | -2 each | No limit |
| AI signal phrases ("leverage," "comprehensive," "robust") | -2 each | No limit |

Target score: 85+. In practice, first drafts land around 72-78. After the de-AI editing pass, they reach 85-92. The scoring is intentionally punitive on kill list violations because those are the phrases that make readers think "an AI wrote this" -- and once that trust breaks, it doesn't come back.

The skill scans every section file, tallies the patterns, and reports violations with line numbers. It doesn't fix anything. It surfaces problems for the reviewer or editor to address.

## Citation Density (check-citations)

The benchmark: 1 citation per 150 words. The actual book averaged 1 per 105 words, which is higher than most business non-fiction. That density is a direct result of the research-first pipeline making citations cheap.

What the skill checks:

- **Uncited statistical claims** -- any sentence with a percentage, dollar amount, multiplier, or specific number that lacks a footnote gets flagged
- **Under-cited sections** -- fewer than 6 citations in a 1,200-word section triggers a warning
- **Over-cited sections** -- more than 25 citations suggests the section is a research dump rather than synthesized prose
- **Format compliance** -- footnotes use named keys, references section exists, internal research block is present

The uncited-stats detection isn't perfect. It catches "grew 300%" without a footnote but can't distinguish between the author's analysis ("roughly half the market") and a factual claim that needs sourcing. Human review handles the gray area.

## Research Coverage (map-research)

This skill compares what's *available* in the research files against what's *used* in the draft. It surfaces three things:

- **Coverage gaps** -- research files with HIGH credibility stats that don't appear anywhere in the chapter
- **Orphan research** -- completed research that maps to no section (usually from prompt generation that was too broad)
- **Cross-chapter opportunities** -- research from Chapter 4 that would strengthen an argument in Chapter 9

The cross-chapter detection is the most valuable output. In a 12-chapter book, arguments connect across parts. A stat about AI infrastructure costs from Chapter 4 might be exactly what Chapter 10's operations section needs. Without automated detection, these connections only happen if the author remembers they exist.

## Opening Variety (audit-openings)

This skill classifies how each section opens and flags repetition:

| Opening Type | Example |
|-------------|---------|
| Question | "What does AI-first actually mean?" |
| Statistic | "Harvey reached $100M ARR in three years." |
| Story | "When Uber hit 2,000 microservices..." |
| Definition | "An AI gateway is the control plane..." |
| Company example | "Figma didn't add AI as a feature." |
| Contrast | "Here's what most people get wrong about..." |

The rule: no pattern should appear more than twice per chapter. When Chapter 3 came back with 5 of 7 sections starting with "Here's the thing," this skill caught it in 10 seconds. A human reviewer might not -- especially after reading 40 sections across multiple chapters.

## Health Score Dashboard

The `review-chapter` skill aggregates all six scores into a weighted health score on a 0-100 scale. Reports are saved to `reports/<Draft>/chapter-reviews/` and include:

- **Overall health score** with trend tracking (shows delta from last review)
- **Metric breakdown table** with individual scores
- **Top 10 priority issues** ranked by impact
- **Quick action commands** -- which scripts to run to fix each issue

```bash
# Full review of chapter 8
python .claude/skills/review-chapter/scripts/review_chapter.py --draft "Draft 1" 8

# Quick scores only (no detailed breakdown)
python .claude/skills/review-chapter/scripts/review_chapter.py --draft "Draft 1" 8 --quick

# Compare chapter against book average
python .claude/skills/review-chapter/scripts/review_chapter.py --draft "Draft 1" 8 --compare
```

The `--compare` flag is useful for spotting outlier chapters. If 11 chapters score 82-88 and one scores 71, you know where to focus editorial time.

## What Automated Quality Can't Do

These skills catch *patterns*. They don't catch *judgment calls*. They'll flag that a section is under-cited but won't know whether the section is the author's personal analysis (where citations are inappropriate) or a factual claim that needs sourcing. They'll detect AI-pattern phrases but can't distinguish between "leverage" used as corporate jargon (bad) and "leverage" used to describe an actual mechanical lever (fine).

The quality pipeline reduces human review time by catching the mechanical stuff. It doesn't replace human review. Both are required. Neither is optional.

---

**Deep dives:** [Voice Drift Prevention](../02-author-voice/voice-drift-prevention.md) | [Review Philosophy](../09-review-process/review-philosophy.md)
