# Contradictions Report: Companion Materials vs Book

**Generated:** 2026-02-04
**Scope:** 43 companion files across checklists/, frameworks/, guides/, resources/, workflows/
**Source of truth:** book/ (124 files)
**Last updated:** 2026-02-04 — All 26 contradictions resolved.

---

## Summary

| Severity | Count | Resolved |
|----------|-------|----------|
| HIGH | 4 | 4 |
| MEDIUM | 12 | 12 |
| LOW | 10 | 10 |
| **Total** | **26** | **26** |

**Status:** All contradictions resolved. Book-internal inconsistencies fixed in Draft 3 and cascaded to companion files and exported book copies.

---

## HIGH Severity

### 1. Harvey valuation: $5B vs $8B (book inconsistency) — RESOLVED

- **File:** `resources/case-studies.md`
- **Resolution:** Updated Ch9 `00-Chapter-Intro.md` from "$5 billion" to "$8 billion" (Dec 2025 a16z round). Updated Ch9 `03-Data-Moats.md` from "$5 billion" to "$8 billion". Updated companion `case-studies.md` to "$8B valuation". Updated exported book copies. Citation updated to TechCrunch Dec 2025 article.

### 2. Harvey ARR: $75M vs $100M (book inconsistency) — RESOLVED

- **File:** `resources/case-studies.md`
- **Resolution:** Updated Ch9 `00-Chapter-Intro.md` from "$75 million ARR" to "$100 million ARR" (crossed $100M by Aug 2025, consistent with Ch1 and Ch2). Updated companion `case-studies.md` to "$100M ARR". Updated exported book copies.

### 3. Air Canada damages: $650.88 vs $812.02 (book inconsistency) — RESOLVED

- **Files:** `resources/case-studies.md`, `frameworks/19-seven-ai-risks-and-mitigations.md`, `frameworks/10-seven-failure-modes-of-agents.md`
- **Resolution:** Standardized to $812.02 (total tribunal order including fare difference + interest + fees). Updated Ch6 `04-The-7-Failure-Modes-of-Agents.md`, `00-Chapter-Intro.md`, `99-Chapter-Summary.md`. Updated companion `10-seven-failure-modes-of-agents.md`. Case-studies and 7-ai-risks already used $812.02. Updated exported book copies.

### 4. 200x figure misattributed: cost vs latency — RESOLVED

- **File:** `workflows/model-evaluation-workflow.md`
- **Resolution:** Changed "Time-to-first-token varies by 200x across models" to "Cost per million tokens varies by 200x across models."

---

## MEDIUM Severity

### 5. GPT failure mode: "confident hallucination" vs "chaotic people-pleaser" — RESOLVED

- **File:** `checklists/model-selection-checklist.md`
- **Resolution:** Changed "confident hallucination (GPT)" to "chaotic people-pleaser (GPT)" to match book's characterization.

### 6. 40-60% statistic scope narrowed — RESOLVED

- **File:** `checklists/gtm-ai-readiness.md`
- **Resolution:** Changed to "technical integration issues account for 40-60% of sales intelligence failures; HubSpot-Salesforce sync is a common culprit."

### 7. "Risk 8" reference (nonexistent) — RESOLVED

- **File:** `frameworks/19-seven-ai-risks-and-mitigations.md`
- **Resolution:** Changed "Risk 1, 2, and 8" to "Risk 1, Risk 2, and GTM Mistake 8."

### 8. pgvector threshold mismatch — RESOLVED

- **File:** `guides/polyglot-persistence-setup.md`
- **Resolution:** Changed "under 1--2 million" to "under 2--3 million" to match book.

### 9. ROI timeframe inconsistency — RESOLVED

- **Files:** `guides/team-ai-fluency-rollout.md`, `workflows/90-day-fluency-implementation.md`
- **Resolution:** Changed "3.4x ROI in the first year" and "500%+" figures to "300%+ ROI over three years (conservative)" to match book. All ROI tiers in 90-day-fluency-implementation.md standardized to "300%+ over 3 years."

### 10. Unverified stats in 90-day fluency program — RESOLVED

- **File:** `frameworks/11-ninety-day-ai-fluency-program.md`
- **Resolution:** Removed unsourced "25% better knowledge retention." Changed "500%+ returns" to "300%+ ROI over three years." Changed break-even "3.4x ROI in the first year" to "300%+ ROI over three years."

### 11. "Five Implications of Probabilistic Outputs" not in book — RESOLVED

- **File:** `frameworks/03-probabilistic-ai.md`
- **Resolution:** Added label: "**Companion framework** --- extends the book's discussion of probabilistic AI with a practical checklist."

### 12. METR study prediction: 20% vs 24% — RESOLVED

- **File:** `resources/research-papers.md`
- **Resolution:** Changed "believed they were 20% faster" to "predicted they'd be 24% faster." Also fixed in `guides/ai-coding-workflow.md` for consistency.

### 13. 95% failure rate: McKinsey vs MIT — RESOLVED

- **File:** `resources/research-papers.md`
- **Resolution:** Removed 95% figure from McKinsey row (already had its own MIT Nanda Study row with 95%). McKinsey row now shows only "88% of companies fail with AI implementation."

### 14. GitHub Copilot acceptance rate: 78% vs 30% (book inconsistency) — RESOLVED

- **File:** `resources/tools.md`
- **Resolution:** Book Ch2 Section 6 updated from "78% suggestion acceptance rate" to "78% task completion rate (versus 70% without)." Ch5 Section 1's "30%" is the actual suggestion acceptance rate — no change needed. Companion `tools.md` updated to "78% task completion rate; ~30% suggestion acceptance rate." Exported book copies updated.

### 15. "post-modern-AI founding" ambiguous shorthand — RESOLVED

- **File:** `checklists/ai-readiness-assessment.md`
- **Resolution:** Changed "post-modern-AI founding" to "founded after modern AI."

### 16. Build-vs-Buy example ordering — RESOLVED

- **File:** `frameworks/04-build-vs-buy-calculus.md`
- **Resolution:** Reordered from Buy/Boost/Build to Buy/Build/Boost to match book.

---

## LOW Severity

### 17. Trust statistic without nuance — RESOLVED

- **File:** `guides/ai-coding-workflow.md`
- **Resolution:** Changed "dropped to 33%" to "dropped to 29-33%" to match book's range.

### 18. Perplexity query growth detail omitted — RESOLVED

- **File:** `resources/case-studies.md`
- **Resolution:** Added intermediate figure: "312M (May 2024), 780M (May 2025), 1.4B (June 2025)."

### 19. Clearview AI missing Ch9 reference — RESOLVED

- **File:** `resources/case-studies.md`
- **Resolution:** Added "Ch 9 (Data Strategy)" alongside existing Ch 10 reference.

### 20. Claude "97.8% security" attributed generically — RESOLVED

- **File:** `resources/tools.md`
- **Resolution:** Changed "Creator of Claude models" to "Creator of Claude 4.5 Sonnet" with "(97.8% security compliance on Claude 4.5 Sonnet)."

### 21. BCG Buy/Boost/Build attribution — RESOLVED

- **File:** `resources/research-papers.md`
- **Resolution:** Changed "BCG / MIT Sloan" to "MIT Sloan" for framework attribution.

### 22. New dollar thresholds not in book — RESOLVED

- **File:** `workflows/model-evaluation-workflow.md`
- **Resolution:** Added note: "*[Supplementary guidance --- specific thresholds not from the book]*"

### 23. New ROI tiers not in book — RESOLVED

- **File:** `workflows/90-day-fluency-implementation.md`
- **Resolution:** Standardized all tiers to "300%+ over 3 years" (removed unsourced "500%+" and "3.4x" figures). Overlaps with #9.

### 24. 7-mental-models drops "different" — RESOLVED

- **File:** `frameworks/02-seven-mental-models-of-ai-first.md`
- **Resolution:** Changed "a way of building" to "a *different* way of building" to match book.

### 25. Personal voice markers stripped (systemic) — RESOLVED (no change)

- **Decision:** Keep companion materials impersonal/third-person. External-facing reference docs benefit from neutral, authoritative voice. No changes applied.

### 26. Contraction avoidance (systemic) — RESOLVED

- **Files:** All framework files
- **Resolution:** Applied contraction replacements across all companion files. 5 replacements made (most files were already using contractions or didn't have the formal patterns).

---

## Book-Internal Inconsistencies — ALL RESOLVED

| Issue | Resolution | Files Changed |
|-------|-----------|---------------|
| Harvey valuation: $5B → $8B | Standardized to $8B (Dec 2025 valuation) | Ch9 `00-Chapter-Intro.md`, Ch9 `03-Data-Moats.md`, exported book copies |
| Harvey ARR: $75M → $100M | Standardized to $100M (crossed by Aug 2025) | Ch9 `00-Chapter-Intro.md`, exported book copies |
| Air Canada: $650.88 → $812.02 | Standardized to $812.02 (total tribunal order) | Ch6 `04-The-7-Failure-Modes.md`, `00-Chapter-Intro.md`, `99-Chapter-Summary.md`, exported book copies |
| Copilot: 78% clarified | Changed to "78% task completion rate" (not "suggestion acceptance rate") | Ch2 `06-Human-AI-Collaboration.md`, exported book copies |
