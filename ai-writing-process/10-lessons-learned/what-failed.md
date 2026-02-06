# What Failed

Dead ends, mistakes, and things that cost time without delivering value. Every failure here taught something -- but I'd rather you skip the tuition.

---

## 1. Starting Without Voice Encoding

Draft 1 was written without the voice system. The output was grammatically correct, well-structured, and completely generic. It read like every AI-generated business book you've skimmed and forgotten.

The entire first draft was essentially a very expensive outline. The structure survived. The prose didn't.

The temptation to "just start writing" is strong when AI produces fluent prose on the first try. Fluent isn't the same as distinctive. You won't notice the difference until you read 20 pages and realize nothing sticks.

---

## 2. Monolithic "Write a Chapter" Prompts

Early attempts used single prompts: "Write Chapter 5 about Building with AI. Here's the outline, the research, the voice guide." Everything in one instruction.

The output: strong openings that trailed off by section 3. Mixed metaphors -- basketball, cooking, and construction in the same paragraph. No sustained argument. The prompt was doing too much, and the AI was dropping context like a juggler with too many balls.

Breaking into 27 modular prompts fixed this. When openings were formulaic, one prompt changed. When citations were inconsistent, a different prompt changed. No cascading side effects.

The monolithic approach wasted several weeks. The lesson: composition beats compression. Multiple focused instructions outperform one giant one.

---

## 3. Write-Then-Research

Writing sections first and adding citations later is backwards. The prose locks in an argument structure, then citations get wedged into existing sentences like afterthoughts. Evidence decorates an opinion instead of shaping it.

Research-first means the evidence shapes the argument from the start. When you know Harvey reached $100M ARR in three years *before* you write about legal AI, that stat becomes the anchor, not a footnote bolted on during editing.

The quality difference between early chapters (written then researched) and later chapters (researched then written) is visible. Later chapters are tighter, better evidenced, and more surprising -- because research surfaced facts that changed what I would have argued otherwise.

---

## 4. Trusting AI Self-Review

"Review what you just wrote" produces agreement, not critique. The same context window that produced the writing can't objectively evaluate it.

We wasted multiple review cycles on self-review before accepting this. The fix -- separate reviewer agent with its own system prompt, tools, and success criteria -- should have been built from the start. Double the prompt engineering, but the reviewer caught problems the writer never would have found.

---

## 5. Over-Engineering the Intelligence App Early

The Flask + PostgreSQL app was built too early. Scripts would have sufficed through Draft 2. The app became valuable in Draft 3 when skills needed persistent state and semantic search across 81 sections. Before that, it was infrastructure waiting for a use case.

The lesson: scripts first, app when scripts hit limits. You'll know the moment -- it's when increasingly baroque shell pipelines are trying to answer questions that a database query handles in one line. For this project, that moment came around 50,000 words. Under 30,000 words, you probably never need the app.

---

## 6. Inconsistent Frontmatter

Early sections had incomplete YAML frontmatter. Missing `research_sources`. Wrong status values. Inconsistent tags. This broke Dataview queries, confused AI agents, and made progress tracking unreliable.

Batch enrichment scripts fixed it retroactively across 81 sections. But retroactive fixes are always more expensive than upfront standards.

The fix for your project: create a section template with every required field pre-populated. Use Templater so new sections always start complete. Validate with a lint script after every session. Ten minutes of prevention saves hours of cleanup.

---

## 7. Mixed Metaphor Blindness

Multiple chapters contained paragraphs with 3-4 competing images -- sports, construction, and cooking metaphors colliding in the same paragraph. Each individual metaphor was fine. Together they created noise.

The problem: metaphors are invisible to the writer mid-flow. Each feels like it's adding clarity. Only a reader (or a reviewer agent with specific instructions) sees the collision.

Related failures: over-specification (7 details competing in one paragraph) and trailing off (building to a point that never arrives). Each cost a full section rewrite when caught. Encoding these as rules in the master system prompt reduced their frequency, but the first occurrence of each was always expensive.

---

## 8. No Cross-Chapter Consistency Checking Until Late

Contradictions accumulated silently. The same metric with different numbers in Chapter 4 and Chapter 9. Terminology drift -- "AI-first" vs "AI first" vs "AI-First." A company described as a startup in one chapter and mid-market in another.

By the final editorial pass, 26 contradictions had accumulated. Each required reading both sections, determining which was correct, and fixing the other without breaking the surrounding argument.

A simple grep for key company names and statistics after every 3-4 chapters would have caught these incrementally, when they were cheap to fix. Instead they compounded into a multi-day editorial cleanup.

---

## The Meta-Lesson

Every failure shares a root cause: optimizing for speed over system quality. Skipping voice files to start faster. One prompt to avoid engineering. Writing before researching. Trusting self-review.

Each shortcut created debt that came due with interest. The system rewarded doing things right the first time, every single time.

---

See also: [What Worked](what-worked.md) | [If Starting Over](if-starting-over.md) | [Architecture Decisions](../01-overview/architecture-decisions.md)
