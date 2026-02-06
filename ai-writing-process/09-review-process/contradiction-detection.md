# Contradiction Detection

> **Context:** Cross-chapter consistency checking for a 12-chapter, 81,000-word manuscript. Found and resolved 26 contradictions between main text and companion materials in a single pass. Most were stat conflicts or terminology drift -- the kind of problems that compound silently across months of writing.

---

Chapter 1 says Harvey reached $100M ARR. Chapter 9 says $75M. Both were written with citations. Both were accurate *at the time of writing* -- the number changed between research sessions. Without cross-chapter detection, both numbers ship. A careful reader catches the conflict. Your credibility takes the hit.

In a 12-chapter book with 81 sections written across multiple agent sessions over weeks, contradictions aren't a risk. They're a certainty. The question is whether you catch them before your readers do.

## Types of Contradictions

Not all contradictions are equal. Some destroy credibility. Others just create confusion. The detection system categorizes five types:

| Type | Example | Risk Level |
|------|---------|-----------|
| Stat conflicts | Harvey valuation: "$5B" in Ch9, "$8B" in Ch1 | High -- readers notice numbers |
| Terminology drift | "AI gateway" in Ch4, "AI router" in Ch5 for the same concept | Medium -- creates confusion over time |
| Advice contradictions | "Start with pilots" in Ch2, "Go all-in" in Ch8 | High -- undermines trust in recommendations |
| Example inconsistency | Air Canada damages: "$650.88" in one section, "$812.02" in another | High -- suggests sloppy fact-checking |
| Framework conflicts | Different step counts or ordering for similar frameworks | Medium -- weakens structural clarity |

Every high-severity contradiction in the actual book had a legitimate explanation -- a funding round happened mid-writing, or different sources reported different components of a ruling. None of those explanations matter to a reader who notices two different numbers for the same fact.

## Detection Methods

Three approaches, from cheapest to most thorough:

### 1. Grep-Based Scanning

Search for key terms, company names, and numbers across all chapter files:

```bash
# All mentions of a company with context
grep -rn "Harvey" Book/drafts/Draft\ 3/ --include="*.md" -C 2

# All dollar amounts to check for conflicts
grep -rn "\$[0-9]" Book/drafts/Draft\ 3/ --include="*.md"
```

Catches obvious conflicts -- same company, different numbers. Misses terminology drift and advice contradictions that require semantic understanding.

### 2. Pre-Scan Deduplication

The publish-review skill's deduplication scan runs before editorial work begins on any chapter. It checks for:

- **Stat repetition** -- the same statistic appearing in multiple chapters (even if consistent, over-repetition weakens impact)
- **Stat conflicts** -- the same metric with different values across chapters
- **Company over-reliance** -- the same company example appearing too frequently (Harvey in 8 chapters was a flag)
- **Verbal tics** -- the same transition phrase or opening pattern appearing across multiple sections

This catches more than grep because it understands context. It knows that "$100M ARR" in Chapter 1 and "$75M ARR" in Chapter 9 refer to the same company's revenue, even if the sentences are structured differently.

### 3. Full Manuscript Review

The most thorough approach: a reviewer agent with the complete manuscript loaded, specifically tasked with finding cross-chapter inconsistencies. This catches advice contradictions ("start with pilots" vs. "go all-in") and framework conflicts that require understanding intent, not just matching strings.

This is the approach that found the GitHub Copilot discrepancy -- Chapter 2 cited "78% suggestion acceptance rate" while Chapter 5 cited "30% suggestion acceptance rate." Both numbers were from legitimate sources. But they measured different things: 78% was the *task completion* rate, 30% was the actual *suggestion acceptance* rate. The fix wasn't changing a number -- it was clarifying what each number measured.

## Resolution Process

Finding contradictions is step one. Resolving them without introducing new problems is the real work.

**Step 1: Identify.** Note every location where the conflicting information appears -- including companion materials, not just the main text.

**Step 2: Verify.** Go back to the source. Don't guess, don't average, don't pick the more impressive number. The Air Canada damages were standardized to $812.02 (total tribunal order) because the $650.88 figure was only the fare difference.

**Step 3: Standardize everywhere.** Every location gets the same number, same terminology, same framing. Miss one and you've created a new contradiction while fixing the old one. The Harvey valuation fix touched Chapter 9's intro, data moats section, companion case studies, and exported book copies.

**Step 4: Use "primary mention + back-reference."** The chapter where a fact is introduced gets the full explanation. Later chapters reference back: "Harvey, which reached $100M ARR (Chapter 1), demonstrates..." One authoritative source per fact. Later chapters point to it, not restate it.

## Scale and Results

The full contradiction scan across the book and its companion materials found 26 contradictions:

| Severity | Count | Examples |
|----------|-------|---------|
| HIGH | 4 | Harvey valuation ($5B vs $8B), Harvey ARR ($75M vs $100M), Air Canada damages ($650 vs $812), cost metric misattributed as latency |
| MEDIUM | 12 | Copilot acceptance rates (different metrics conflated), ROI timeframes, terminology inconsistencies |
| LOW | 10 | Missing nuance in statistics, ordering differences, attribution details |

All 26 resolved in a single pass. HIGH issues required updating book text, companion materials, and exported copies. MEDIUM and LOW were mostly companion updates to match the book as source of truth.

## Prevention

Catching contradictions is the safety net. Preventing them is better.

**Handoff protocols** help. Each new agent session receives a summary of what previous chapters established -- key statistics, terminology choices, framework structures. This reduces the chance of an agent inventing a different number for the same metric.

**Centralized research** helps more. When every chapter pulls statistics from the same research files, conflicts are less likely. The Harvey ARR contradiction happened because research was updated mid-writing and earlier chapters weren't refreshed -- a process gap, not a data gap.

**Regular cross-chapter scans** are the real prevention. Run them every 3-4 chapters, not just at the end. Catching a conflict between Chapter 3 and Chapter 5 while writing Chapter 6 is far cheaper than catching it during final verification.

The contradictions will still emerge. Months of writing, evolving data, multiple agent sessions -- structurally inevitable. The question isn't whether you'll have contradictions. It's whether you have a system for finding them.

---

**Related:** [Review Philosophy](review-philosophy.md) | [Quality Skills](../04-agent-system/quality-skills.md) | [Research Architecture](../05-research-pipeline/research-architecture.md)
