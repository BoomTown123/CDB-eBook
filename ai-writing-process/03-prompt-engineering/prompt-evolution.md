# Prompt Evolution

The 27-prompt system wasn't designed. It was grown. Across three complete drafts of a 12-chapter book, each draft exposed what the prompts were missing, and each revision closed the gap between "AI-generated content" and "content that sounds like a specific human wrote it."

Here's how the system changed -- and what drove each change.

---

## Draft 1: The Naive Phase

The first draft used basic prompts. "Write a chapter about AI infrastructure." "Write a section about data strategy." No voice encoding, no research pipeline, no quality gates.

The output was functional. It covered topics coherently, organized arguments logically, and used proper grammar. It also sounded like every other AI-generated business book -- competent, smooth, and completely forgettable. No practitioner perspective. No personality. No point of view that anyone might disagree with.

**What we had:**
- ~5 ad hoc prompts, written fresh each session
- No voice files or reference materials
- No research integration -- opinion-heavy, citation-light
- Review was manual and inconsistent (read it, fix what looks wrong)
- No systematic quality checks

**What it produced:** Chapters that read like a consultant's report. Technically sound, internally consistent, and impossible to distinguish from any other AI-written business content. Required heavy human editing to inject voice, cut generic passages, and add real examples.

**The key learning:** AI doesn't need help writing. It needs help writing *like you*. The problem was never "can it produce words?" The problem was "can it produce *your* words?"

---

## Draft 2: The System Phase

Draft 2 was a ground-up rebuild of the prompting approach, driven by one realization: voice has to be encoded as persistent context, not in-line instructions.

**What changed:**
- Built the 6-file voice system (gold standard, voice guide, blog-to-book adaptation, audience empathy profiles, authenticity markers, quick reference)
- Created the master system prompt -- first version at ~200 lines covering voice DNA, phrase tables, audience profiles, and structural requirements
- Added the research-first pipeline: Perplexity prompts run *before* writing, not after. The writer agent starts with stats, quotes, and company examples already extracted.
- Grew from 5 ad hoc prompts to 15 modular prompts (later grew to 25)
- Separated writing prompts from editing prompts -- different concerns, different prompts

**What it produced:** Voice consistency improved dramatically. Sections started sounding like a specific author with specific opinions. Citations grounded claims in evidence. Audience balance was deliberate, not accidental.

But problems remained. Quality was uneven across chapters. Some sections had voice drift where the AI slipped back into generic mode. Opening paragraphs were formulaic -- 5 of 7 in one chapter started the same way. No systematic way to detect these patterns until a human caught them on read-through.

**The key learning:** Encoding voice gets you 70% of the way. Detecting when the voice drifts gets you the rest. Writing prompts alone aren't enough -- you need editing and review prompts to catch what writing prompts miss.

---

## Draft 3: The Quality Phase

Draft 3 was about closing the gap between "usually good" and "consistently publishable."

**What changed:**
- Master system prompt grew from ~200 lines to 339 lines, adding the 10 encoded learnings, the density test scorecard, and the voice calibration check
- Added the De-AI editing prompt -- the single biggest quality improvement in the entire system. It catches 9 categories of AI tells and produces a severity-graded change log.
- Introduced automated quality audits as Claude Code skills: voice scoring, citation density analysis, opening variety checks, link integrity, term consistency
- Built the phrase kill list based on actual patterns found in earlier drafts (not theoretical concerns -- real "leverage" and "important to note" instances discovered in the manuscript)
- Added the 4-phase editorial review with dedicated prompts per phase: deduplication scan, argument strengthening, voice polish, final verification
- Total prompt count reached 27 (8 writing + master, 5 editing, 4 review, 3 linking, 5 fix)

**What it produced:** Publication-ready output. 81,000+ words, 775 citations with source URLs, consistent voice across all 12 chapters, both audiences served throughout. The quality audit pipeline caught voice drift, citation gaps, and terminology inconsistencies before they compounded across sections.

**The key learning:** Trust but verify. The writing prompts are good enough to produce strong first drafts. But "good enough" first drafts still accumulate small errors that compound across 12 chapters. The review and fix prompts are the compounding-error defense.

---

## Evolution Patterns

Five patterns showed up consistently across all three drafts:

| Pattern | Draft 1 | Draft 3 |
|---------|---------|---------|
| **Inline to Structured** | Voice instructions embedded in each prompt | 6 reference files + master system prompt composed at runtime |
| **Single to Modular** | "Write a chapter" as one prompt | 8 composable writing prompts + 14 editing/review/fix prompts |
| **Manual to Automated** | Voice review by reading and gut feeling | Automated scoring skills producing quantified dashboards |
| **Generic to Specific** | "Write well" and "sound natural" | 19 named craft techniques, 4 phrase tables, 10 encoded learnings |
| **Trust to Verify** | Assume the output is good, fix what looks wrong | Kill lists, audits, quality gates, graded reviews |

The throughline: each pattern moves from implicit to explicit. "Sound like me" becomes 339 lines of encoded voice rules. "Good quality" becomes a 6-dimension scoring rubric. "Natural writing" becomes a 9-category AI detection checklist.

---

## What Stays Constant

The core identity -- Dense, Direct, Human -- never changed across three drafts. The voice files evolved, the prompt count tripled, the quality infrastructure went from nothing to 14 automated skills. But the three-word DNA was Draft 1 and still is Draft 3.

The prompts got more specific. They didn't get different.

This matters for anyone building their own system. Nail your core identity first. Three words. Then build everything else as increasingly precise ways to enforce those three words at scale. If your identity shifts between drafts, your prompt system is solving the wrong problem.

---

## What I'd Do Differently

Two things.

**Build the De-AI prompt in Draft 1, not Draft 3.** AI tells compound. Every chapter written without the De-AI prompt needed a full cleanup pass later. If I'd built it early, the editing load in Draft 3 would have been half what it was.

**Start with the research pipeline, not the writing prompts.** Draft 1's biggest weakness wasn't voice -- it was substance. Opinion-heavy writing without evidence is easy to produce and hard to trust. The research pipeline should be the *first* thing you build, not the second. Write after research, always.

---

**Related:** [Prompt Architecture](prompt-architecture.md) | [Master System Prompt](master-system-prompt.md) | [What Worked](../10-lessons-learned/what-worked.md)
