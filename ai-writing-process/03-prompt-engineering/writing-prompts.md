# Writing Prompts

Eight prompts handle content creation. Each targets a specific content type with its own structure, word target, and quality criteria. The master system prompt (voice, audience, rules) is always present -- these prompts layer on top of it.

---

## The 8 Writing Prompts

| # | Prompt | What It Produces | Word Target |
|---|--------|------------------|-------------|
| 01 | Chapter Opening | Hook + context + chapter preview | 350-450 |
| 02 | Section | Core substantive content with subheadings, examples, action items | 1,000-1,200 |
| 03 | Framework | Numbered lists -- the author's signature style | N x 300 |
| 04 | Case Study | Real-world company narrative (setup, approach, outcome, lesson) | 400-600 |
| 05 | Analogy | Pop culture or business bridge for abstract concepts | 200-400 |
| 06 | Executive Summary | "What You'll Learn" box for chapter top | Variable |
| 07 | Chapter Closing | Synthesis + key takeaways + bridge to next chapter | 300-400 |
| 08 | Technical Deep Dive | Advanced optional sections for technical readers | Variable |

---

## The Section Prompt: The Workhorse

The section prompt (02) runs 4-6 times per chapter. It's the most engineered prompt in the system because it handles the bulk of content production.

It requires 6 elements in the input:

1. **Section context.** What the previous section covered, what this section's purpose is, and what comes next. Without this, sections feel disconnected -- like standalone blog posts stitched together.

2. **Key points.** The 3-5 arguments or topics the section must cover. Not a script -- a constraint that ensures nothing critical gets skipped.

3. **Research input.** The research-reader skill provides a snapshot of relevant stats, quotes, and company examples before the section prompt fires. This is what separates citation-heavy output from opinion-heavy output.

4. **Word target.** 1,000-1,200 words with an explicit note that "dense value matters more than word count."

5. **Structural requirements.** Opening (2-3 sentences connecting to chapter flow), core content with subheadings every 200-300 words, a complexity acknowledgment ("this is harder than it sounds"), practical application (a "What This Means For You" callout), audience balance (callouts where advice differs for enterprise vs. startup), and a closing that lands.

6. **Density requirements.** One strong example per point. Each paragraph has one job. No throat-clearing. Tightening pass after writing -- can you cut 20%?

The output includes a frontmatter block, inline footnote citations, a references section with source URLs, and an internal research tracking block. Everything the vault needs in one pass.

---

## The Framework Prompt: Signature Style

Numbered frameworks -- "5 Principles for X," "7 Signs of Y" -- are the author's signature move throughout the book. The framework prompt enforces a consistent structure for each point:

**Title** -- memorable and quotable, not generic. "Start with the Job, Not the Technology" instead of "Planning."

**Explanation** -- 2-3 paragraphs covering what the principle means in practice, why it matters, and the common mistake it prevents.

**Example** -- one real company, scenario, or analogy. Specific enough to be credible. The prompt explicitly says "one example per point -- not two proving the same thing."

**Action** -- a "What This Means For You" callout or specific "Action:" item. Something the reader can do, not just understand.

Additional constraints: points must be roughly equal length (don't front-load), the final point should feel like a capstone, at least one point gets a "this is harder than it sounds" acknowledgment, and examples should vary (not all tech companies).

The prompt also supports pop culture theming. A Star Wars framework might use Youngling through Council as stages. A sports framework might use training through championship. The key rule: if you pick a theme, sustain it through all points. Don't mix Star Wars with Marvel.

---

## The Chapter Opening Prompt: Setting the Hook

Chapter openings need to accomplish four things in 350-450 words: hook the reader, establish context, preview the chapter, and bridge into the first section.

The prompt offers four hook patterns:

- **Provocative question** that challenges assumptions
- **Brief scenario** showing the problem in action
- **Bold statement** that will be explored
- **Reality check** using "What does X actually look like?"

It enforces one sustained analogy (the mixed-metaphor learning encoded as a constraint), direct "you" address, and a specific anchor detail instead of a generic opening. The bridge to the first section must land on a question or insight -- not trail off.

The opening prompt was one of the first to need iteration. Early versions produced openings that all started with "In today's rapidly evolving..." The prompt now explicitly lists generic openers as anti-patterns and requires a specific, non-generic first sentence.

---

## The Chapter Closing Prompt: Landing, Not Trailing Off

The closing prompt produces synthesis (not summary), key takeaways (3-5 actionable items), and a bridge to the next chapter. The distinction between synthesis and summary matters: summary restates what you said; synthesis connects the themes into something the reader didn't see coming.

The hardest constraint to enforce: a memorable closing line. "Call it an MVP. Call it day one. Either way, I'm finally playing" from the gold standard is the benchmark. Not every chapter closing hits that level, but the prompt pushes for it.

---

## Sequencing

Prompts fire in a specific order because each builds on what came before:

1. **Chapter opening first.** Sets the hook, establishes the metaphor, previews themes. Everything else follows from this.
2. **Sections in order.** Each section references what the previous one covered. Writing out of order loses narrative flow.
3. **Frameworks and case studies woven in.** These aren't separate sections -- they're embedded within sections where the content calls for them.
4. **Chapter closing last.** Can only synthesize themes that actually exist in the completed sections. Writing this early produces generic closings disconnected from the actual content.

The chapter-writer skill handles this sequencing automatically. For manual use, follow this order and pass the output of each step as context to the next.

---

## Building Your Own Writing Prompts

Start with the section prompt. It's the one you'll use most and the one where quality problems surface first. Get it producing consistent, voice-accurate output, then add the opening and closing prompts. Framework and case-study prompts come last -- they solve specific structural problems you'll discover during writing.

Each prompt should include: required inputs, structural requirements, voice reminders (referencing the master prompt), density requirements, word target, and a "good output" example showing what success looks like. The example is the most important part. AI calibrates to examples more reliably than to instructions.

---

**Related:** [Prompt Architecture](prompt-architecture.md) | [Chapter Writer Skill](../04-agent-system/chapter-writer-skill.md) | [Section Writing Template](../templates/prompts/section-writing-template.md)
