# Voice Drift Prevention

Voice consistency across a 12-chapter, 81,000-word book is the hardest quality metric to maintain. Early sections sound like you -- you're fresh, the voice files are top of mind, every paragraph gets attention. By chapter 8, AI patterns creep in. Familiar phrases feel natural. Hedging stacks up. Openings get formulaic. Without active prevention, your voice erodes so gradually you don't notice until a full read-through reveals the damage.

---

## The Drift Problem

Drift isn't a sudden failure. It's entropy. Each writing session introduces small deviations that compound. The AI generates "It's important to note that..." once and you let it slide because you're focused on the argument. Next session, two more slip through. By the end of the chapter, your manuscript reads like a McKinsey report with pop culture references stapled on.

Three factors accelerate drift:

1. **Session fatigue.** The longer a writing session runs, the less carefully you edit AI output. Chapter 3 at 9am gets tighter review than Chapter 3 at 11pm.
2. **Context window pressure.** Longer chapters push voice files further from the model's attention. By section 6, the authenticity markers are distant memory.
3. **Familiarity blindness.** After reading "comprehensive" and "robust" fifty times, they stop registering as problems.

---

## Kill Lists

Maintain a specific list of phrases that AI defaults to. Not general guidelines -- exact strings to search for and eliminate.

**Corporate speak (delete on sight):**

| Phrase | Replacement |
|--------|-------------|
| "It's important to note that..." | Just say it |
| "Let's delve into..." | "Here's how..." or delete |
| "In today's rapidly evolving landscape..." | Be specific about what's changing |
| "Organizations should endeavor to..." | "You should..." |
| "In conclusion..." | Just end |
| "Going forward..." | Delete |
| "Leveraging" / "Utilizing" | "Using" |

**Decorative adjectives (delete or replace with specifics):**
- comprehensive, robust, transformative, holistic, synergistic, scalable (without context), innovative (without evidence)

**Hedge stacking (take a position):**
- "might potentially perhaps consider" -- pick one hedge or commit to the claim
- "It could be argued that..." -- argue it or don't
- "Some might say..." -- who? Be specific or cut it

**AI structural tells:**
- Three examples in every list (vary lengths)
- Perfect parallel structure everywhere (allow asymmetry)
- Every point weighted equally (some points matter more -- show it)
- Smooth transitions everywhere (abrupt shifts are human)

---

## De-AI Prompts

A dedicated editing prompt that strips AI patterns. Run it on every section after writing. This isn't the same as the writing prompt -- it's adversarial. Its job is to find and fix the patterns the writing prompt missed.

The de-AI prompt references the kill list directly and checks for:

- Kill list violations (exact string matching)
- Throat-clearing introductions (sentences that describe what you're about to say instead of saying it)
- Trailing conclusions (paragraphs that summarize what was just said)
- Uniformity of sentence length (a hallmark of AI prose)
- Missing practitioner voice (no "I've seen..." or "In my experience...")
- Generic examples that could appear in any business book

The key insight: run this as a *separate pass*, not as part of writing. The writing agent and the editing agent need different objectives. One generates. The other interrogates.

---

## Periodic Voice Audits

An automated `check-voice` skill that scores each section (0-100) against defined voice patterns. Not subjective -- rule-based, with specific deductions and bonuses:

**Deductions:**
- Kill list violation: -3 points each
- Hedging pattern ("I think," "maybe," "sort of"): -2 points each
- AI structural signal (uniform lists, perfect parallelism): -2 points each
- Throat-clearing opener: -5 points
- No practitioner perspective in entire section: -5 points

**Bonuses:**
- Approved voice marker used naturally: +1 each
- Sustained metaphor: +3
- Specific opening (named person, place, number): +3
- Balanced take (opportunity + risk): +2

**Target: 85+ across all sections.** Below 75 triggers a rewrite flag. The score isn't perfect -- no automated metric captures everything -- but it catches the mechanical problems that compound into voice drift.

Run audits after every chapter, not just at the end. Drift caught at chapter 4 is a quick fix. Drift discovered at chapter 11 means rewriting 60,000 words of context.

---

## The 10 Learnings

Real mistakes discovered while writing this book. Each one came from producing something wrong, analyzing why it felt off, and encoding the fix into the system.

### 1. The Over-Specification Trap
Seven specific details in one paragraph reads like you're proving you were there. One vivid anchor earns trust. The gold standard uses ONE: "Russ rapping through my AirPods on a plane to Toronto."

### 2. The Mixed Metaphor Problem
Five images fighting for attention in one paragraph -- hockey sticks, Ferraris, Mad Max, sandstorms, garages. Pick one metaphor. Commit to it. The gold standard sustains one basketball metaphor across 385 words.

### 3. Throat-Clearing Detection
"Before diving into specific technology choices, let's establish grounding truths that will save you from expensive mistakes." That sentence adds nothing. If it describes what you're about to say instead of saying it, cut it.

### 4. Generic vs Visceral
"Sees AI as a threat rather than a tool" is how a consultant would say it. "Thinks AI is coming for their jobs" is what people actually fear. Find the darker, truer version.

### 5. Trailing Off vs Landing
Ellipses at the end of an analogy mean you didn't know how to finish. Every sentence needs to land somewhere. If you're trailing off, you don't have an ending yet.

### 6. The Fake Precision Problem
"$4.2 million budget" from someone else's board presentation. Suspiciously precise. Real specifics are messy -- "about 18 months," "a few million." Fake specifics are exact. Readers sense the difference.

### 7. Redundancy Blindness
"The potential is genuinely massive. The timing is genuinely now." Same word, consecutive sentences. Read aloud to catch it. The fix is usually better than just removing the repetition -- it forces a new angle.

### 8. Density Comes From Cutting
Every revision got shorter. 142 words became 118 became 89. Same meaning, 37% fewer words. If you're chasing density by adding insight, you're doing it wrong. Chase it by removing everything that isn't insight.

### 9. Examples Teach Themselves
If you need a paragraph explaining why the example was good, the example isn't good enough. Rewrite the example until it teaches without commentary.

### 10. One Anchor, Then Universal
The gold standard pattern: one specific detail that grounds you, immediate move to universal insight, land with something quotable. Specific, then universal, then memorable. In that order. One of each.

---

## Putting It Together

Voice drift prevention isn't one technique. It's a layered defense:

1. **Kill lists** catch the obvious AI patterns
2. **De-AI prompts** strip what kill lists miss
3. **Voice audits** score consistency across the full manuscript
4. **The 10 learnings** prevent known mistakes from recurring

No single layer is sufficient. The kill list catches "delve into" but not a trailing conclusion. The de-AI prompt catches trailing conclusions but not a section that scores 72 overall. The voice audit catches the 72 but not *why* it's a 72. The learnings explain the why.

Run all four. Every chapter. The investment is small -- maybe 30 minutes per chapter for the full cycle. The alternative is discovering at chapter 12 that your voice wandered off somewhere around chapter 6.

---

## Next Steps

- [Building a Voice System](building-a-voice-system.md) -- The full 6-file foundation that drift prevention protects
- [De-AI Editing Prompt](../03-prompt-engineering/editing-and-review-prompts.md) -- The specific prompt for stripping AI patterns
