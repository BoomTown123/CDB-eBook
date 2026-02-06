# Editorial Workflow

> **Context:** A 4-phase editorial process that took *Blueprint for An AI-First Company* from drafted to publishable. Results: 240 line editing issues resolved, 188 copyediting issues resolved, 15 critical verification issues caught, zero remaining.

---

This is the longest phase of the review pipeline and the one where the quality gap between "AI-written" and "published" actually closes. Automated audits take minutes. The big themes review takes an hour or two. Editorial review takes 4-8 hours per chapter -- and it's worth every minute.

The 4 phases run sequentially. Each catches problems the previous one doesn't. Skipping a phase or collapsing them into one "edit everything" pass reliably produces worse results, because the editorial mindset for evaluating structure is different from the mindset for evaluating grammar.

## The 4 Phases

| Phase | Focus | Issues Found | Mindset |
|-------|-------|-------------|---------|
| Developmental Editing | Structure, argument flow, chapter organization | Structural recommendations per chapter | Architect |
| Line Editing | Prose quality, sentence-level craft, voice | 240 issues across 12 chapters | Craftsperson |
| Copyediting | Grammar, consistency, formatting | 188 issues across 12 chapters | Perfectionist |
| Final Verification | Citations, links, frontmatter, word counts | 15 critical issues | Auditor |

## Phase 1: Developmental Editing

The structural pass. You're not reading sentences -- you're reading architecture.

**What it evaluates:**
- Does the chapter's argument build across sections? Or do sections feel like disconnected blog posts stapled together?
- Does each section lead naturally to the next? Could you rearrange them without noticing?
- Is anything missing from the argument? Where does the reader's "but what about..." go unanswered?
- Does the opening hook earn the reader's attention? Does the closing bridge point to what comes next?
- Are the frameworks placed where they're most useful, or are they buried in the wrong section?

**What it produces:** Structural recommendations. "Move Section 3 before Section 2 -- the framework needs to be established before the case study." "Section 5 has no supporting evidence -- add a case study or cut the claim."

This is where chapters get reorganized. Better to rearrange now than to polish sentences in the wrong section.

## Phase 2: Line Editing

The sentence-level pass. Every sentence gets scrutinized for craft.

**What it evaluates:**
- Voice consistency against the author's authenticity markers. Does this sound like the author or like a capable AI?
- Kill list enforcement. "It's important to note that" and "let's delve into" are automatic flags -- no exceptions, no context that makes them acceptable.
- Sentence rhythm and variation. Three long sentences in a row? The third one needs to be short. Punchy.
- Specificity. "A large company" becomes "Walmart." "A significant improvement" becomes "40% reduction in processing time." Numbers beat adjectives.
- Hedging detection. "It could be argued that" means you're not confident in the claim. Either commit to it or cut it.

**What it produces:** Line-level edit suggestions with original text and proposed replacement. 240 issues across 12 chapters -- kill-list violations, hedging patterns, rhythm problems, vague language.

This phase catches the difference between prose that reads like a human wrote it and prose that reads like an AI trying very hard. Readers feel the difference, even when they can't articulate it.

## Phase 3: Copyediting

The consistency pass. Grammar, punctuation, and the unglamorous work of making sure the manuscript doesn't contradict itself on formatting.

**What it evaluates:**
- Grammar and punctuation errors
- Consistent terminology across chapters. Is it "AI-first" with a hyphen or "AI first" without? (Hyphen. Always.) Is it "microservices" or "micro-services"?
- Number formatting. "12 chapters" or "twelve chapters"? "81,000 words" or "81000 words"?
- Capitalization conventions. Is "Agent Hub" always capitalized the same way?
- Citation format consistency. Named footnote keys, references section at the end, internal research blocks present.
- List formatting. Consistent use of periods, parallel construction across bullet points.

**What it produces:** Copyedit corrections -- 188 across 12 chapters. Most were minor individually. Collectively, they're the difference between a manuscript that feels professional and one that feels like a draft someone forgot to finalize.

The copyediting phase is thankless work. Nobody notices when it's done well. Everyone notices when it's done poorly.

## Phase 4: Final Verification

The pre-publication audit. Binary questions, binary answers.

**The checklist:**
- Do all citation URLs still resolve? (URLs break. They break constantly. A citation audit run 3 weeks after writing caught 15 dead links.)
- Are there orphaned footnotes -- footnote definitions with no reference in the text, or references with no definition?
- Is the frontmatter updated? Status fields should read "editing" or "done," not "drafting."
- Are word counts within 10% of targets? A section targeting 1,200 words that came in at 1,800 needs tightening. One that came in at 600 needs expansion.
- Are internal research blocks present and accurate? These are hidden in the reader-facing PDF but essential for tracking which research informed which section.

**What it produces:** A sign-off checklist. 15 critical issues were caught in this phase -- mostly broken citation URLs and orphaned footnotes that slipped through earlier passes. All 15 were resolved before publication.

This phase exists because the editorial passes before it focus on prose quality and can miss metadata problems. A beautifully written chapter with a broken frontmatter field and 3 dead citation links isn't publishable.

## The Publish-Review Skill

The 4-phase workflow is automated through the `publish-review` skill, which orchestrates the entire process with a consistent reviewer persona.

**Pre-scan deduplication** runs before any editing begins. It checks for:
- Company over-reliance (same company appearing too frequently across sections)
- Stat conflicts (same metric reported differently in different sections)
- Verbal tics (the same transition phrase appearing 8 times in one chapter)

**Phase-by-phase editing** runs each phase with its own checklist and evaluation criteria. The skill doesn't combine phases -- it runs them sequentially, producing distinct outputs for each.

**Fact verification protocol** requires WebSearch confirmation before adding any new information during editing. The skill can suggest an improved example, but it must verify the example is accurate before inserting it. This prevents the common AI editing failure mode: making the prose better while making the facts worse.

**Phrase kill list** with replacement suggestions. Not just flagging "it's important to note that" -- providing the specific replacement: just state the thing directly. The kill list has 30+ patterns, each with a concrete fix.

**Post-review verification** generates grep commands that the reviewer can run to confirm issues were actually resolved. "Search for 'important to note' across all files" -- if the grep returns results, the editing pass missed something.

## The Human in the Loop

The AI scans 81 sections, flags 428 issues, proposes corrections. The human makes every final call.

The AI flags "arguably" as hedging. The human decides whether the uncertainty is genuine (keep it) or timidity (cut it). The AI suggests a shorter sentence. The human decides whether the longer version has rhythm worth preserving. These judgment calls are the irreplaceable contribution.

4-8 hours per chapter, 48-96 hours for a 12-chapter book. Not fast. But those hours go to judgment, not hunting for typos. The system found the problems. The human decided what to do about them.

---

**Related:** [Review Philosophy](review-philosophy.md) | [Editing and Review Prompts](../03-prompt-engineering/editing-and-review-prompts.md) | [Quality Skills](../04-agent-system/quality-skills.md)
