# Synthesis and Extraction

Raw Perplexity answers are useful but not usable. A typical response is 1,000-2,000 words of narrative prose -- stats buried in paragraphs, quotes mixed with analysis, company examples scattered across sections. A writer agent can't efficiently pull what it needs from that format. Neither can a human.

The synthesis layer transforms raw research into structured, writer-ready material. Statistics land in tables with credibility scores. Quotes get attributed with confidence levels. Company examples are grouped by name with context. The writer agent's job becomes *selecting and framing*, not *finding and formatting*.

---

## The Gap Between Raw and Ready

Here's what a raw Perplexity answer looks like versus what the writer actually needs:

**Raw answer (1,500 words of prose):**
> Harvey, the legal AI company, has grown rapidly since its founding. According to their year-in-review, they reached approximately $100M in annual recurring revenue within three years of launch. CEO Winston Weinberg has spoken about their approach: "We built the company from scratch because retrofitting AI into existing legal workflows was impossible." The company serves over 500 law firms...

**What the writer needs:**
- A stat: `$100M ARR in three years` -- credibility: HIGH, source: Harvey Year in Review
- A quote: `"We built the company from scratch because retrofitting AI was impossible"` -- speaker: Winston Weinberg, CEO Harvey, confidence: HIGH
- A company example: Harvey, legal AI, $100M ARR, 500+ law firms

Three different content types, each with metadata that tells the writer *how much to trust it*. That's what synthesis produces.

---

## The Synthesize-Research Skill

The `synthesize-research` skill automates extraction from raw answers. Run it per chapter or per section:

```bash
# Process all sections in a chapter
python .claude/skills/synthesize-research/scripts/synthesize_research.py --chapter 8

# Process a single section
python .claude/skills/synthesize-research/scripts/synthesize_research.py --section "8.1"

# Only sections missing synthesis files
python .claude/skills/synthesize-research/scripts/synthesize_research.py --missing

# Preview without writing files
python .claude/skills/synthesize-research/scripts/synthesize_research.py --chapter 8 --dry-run
```

The script scans answer files in `research/Chapter_XX/answers/`, runs pattern matching for each content type, and generates `synthesis.md` files alongside the answers.

### What Gets Extracted

| Content Type | Format | Example |
|------------|--------|---------|
| Statistics | Table with stat, context, credibility | "$100M ARR in three years" -- Harvey Year in Review -- HIGH |
| Quotes | Blockquote with speaker attribution | "AI is not the product, it's the foundation" -- CEO, Harvey |
| Company Examples | Grouped by company with specifics | Harvey: legal AI, $100M ARR, 500+ law firms |
| Frameworks | Numbered lists with structure | 5-step adoption model from McKinsey |

---

## Credibility Scoring

Not all stats are equal. A percentage from a McKinsey survey with 1,000 respondents is not the same as a round number from an unattributed blog post. The synthesis pipeline scores every statistic:

- **HIGH**: Specific numbers from named primary sources. "$100M ARR" from Harvey's own year-in-review. "47% of developers" from GitHub's annual survey with methodology described. These are citation-ready -- the writer agent uses them directly.
- **MEDIUM**: Contextual numbers with partial sourcing. "About 60% of enterprises" attributed to a consulting report but without methodology. Useful for directional claims, but flag if possible.
- **LOW**: Round numbers, estimates, unverified claims. "Most companies" or "over 50%" without a named source. These get filtered out by default.

**The rule:** The writer agent only uses HIGH credibility stats. The reviewer agent flags anything below HIGH that makes it into a draft. This sounds aggressive, but it's the difference between "Harvey reached $100M ARR in three years" (verifiable, impressive, citable) and "most AI companies grow fast" (meaningless).

---

## Confidence Scoring for Quotes

Quotes get a parallel scoring system:

- **HIGH**: Direct quote with named speaker, title, and clear context. `"We built from scratch because retrofitting was impossible" -- Winston Weinberg, CEO Harvey`. Full attribution, complete sentence, from a structured source.
- **MEDIUM**: Attributed but context is unclear. The person is named but the quote might be paraphrased or the context of the statement isn't clear.
- **LOW**: Unattributed, fragmented, or likely paraphrased. "Industry leaders say that AI is transforming..." -- no specific person, no specific context.

Speaker types also get categorized: CEO, CTO, Research (McKinsey, Gartner), and Other. This matters because the book targets practitioners -- a CTO quote about infrastructure tradeoffs lands harder than an analyst quote about market trends.

---

## Output Format

Each synthesis file follows a consistent structure: Key Statistics (table), Notable Quotes (blockquotes with attribution), Company Examples (grouped by company), Frameworks & Models (numbered lists), and Writing Notes (counts of what was found). The `Writing Notes` section at the bottom gives a quick signal -- if a section produced 12 stats and 5 quotes, there's plenty of evidence. If it produced 1 stat and no quotes, you might need to run additional research prompts.

---

## Research Reader Integration

The synthesis files feed into a second layer: the research-reader skill's 9 extraction scripts. These scripts operate on *both* synthesis files and raw answers, providing different views depending on what the writer needs in the moment:

| Script | What It Does |
|--------|-------------|
| `research_snapshot.py` | One-stop overview: ranked files, top stats, best quotes, key companies |
| `format_citations.py` | Copy-paste ready stats and quotes with footnote keys |
| `find_support.py` | Find evidence for a specific argument (with optional counter-arguments) |
| `extract_stats.py` | All statistics filtered by credibility and semantic category |
| `extract_quotes.py` | All quotes filtered by confidence and speaker type |
| `find_unused.py` | Compare draft against research to find unused evidence |
| `search_research.py` | Keyword search across all research files |
| `list_research.py` | Inventory of available research for a chapter |
| `get_section_research.py` | All research files relevant to a specific section |

The typical workflow before writing a section: run `research_snapshot.py` for the overview, then `format_citations.py` for citation-ready content. The writer agent does this automatically as part of the chapter-writing skill. By the time it starts composing prose, the evidence is already formatted and waiting.

---

**Related:** [Research Architecture](research-architecture.md) | [Citation Management](citation-management.md) | [Research Reader Skill](../04-agent-system/research-reader-skill.md)
