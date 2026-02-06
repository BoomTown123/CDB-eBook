# Review Skill Template

A fill-in-the-blank starting point for building a chapter review skill that aggregates quality checks into a single dashboard.

---

```markdown
---
name: review-chapter
description: "Quality dashboard aggregating metrics from all analysis checks."
---

# Review Chapter

Generate a unified quality dashboard for a chapter.

## Analysis Dimensions

| Dimension | Weight | Script/Check |
|-----------|--------|-------------|
| Voice | [X]% | [voice check script or manual checklist] |
| Citations | [X]% | [citation audit script or method] |
| Research | [X]% | [research coverage check] |
| Links | [X]% | [internal link audit method] |
| [YOUR DIMENSION] | [X]% | [your check method] |

*Weights must total 100%.*

## Health Score Calculation

```python
health_score = sum(dimension_score * weight for each dimension)
```

**Interpretation:**
- **85+:** Publication ready
- **70-84:** Minor improvements needed
- **Below 70:** Specific fixes required

## Per-Dimension Checks

### Voice Check
- Scan for kill-list violations ([YOUR KILL LIST]) -- deduct 3 points each
- Detect hedging patterns ("it might be argued", "perhaps") -- deduct 2 each
- Find AI-generated signals ("delve", "crucial", "landscape") -- deduct 2 each
- Count approved voice markers ([YOUR SIGNATURE PHRASES]) -- add 1 each
- Base score: 70, target: 85+

### Citation Check
- Count footnote citations per section
- Calculate density: citations per 1,000 words
- Benchmark: [YOUR TARGET -- e.g., 1 citation per 150 words]
- Flag uncited statistics and direct quotes
- Flag orphaned footnotes (defined but never referenced)
- Flag duplicate URLs with different tags

### [YOUR DIMENSION]
- [What to check]
- [How to score]
- [What to flag]
- [Target threshold]

## Output Format

```markdown
## Chapter [N] Quality Dashboard

### Health Score: [X]/100

| Dimension | Score | Weight | Weighted | Issues |
|-----------|-------|--------|----------|--------|
| Voice | [X] | [X]% | [X] | [count] |
| Citations | [X] | [X]% | [X] | [count] |
| Research | [X] | [X]% | [X] | [count] |
| Links | [X] | [X]% | [X] | [count] |

### Priority Issues
1. [Highest impact issue with file and line reference]
2. [Second highest]
3. [Third]

### Recommended Actions
- [ ] [Specific action with file path]
- [ ] [Specific action with file path]
- [ ] [Specific action with file path]
```

## Tracking Over Time

Store dashboard results in [YOUR TRACKING LOCATION] to compare scores across revisions:

```
Chapter 6 — v1: 62  →  v2: 74  →  v3: 88
```
```

---

## Customization Checklist

- [ ] Set dimension weights (must total 100%)
- [ ] Define your kill list and signature phrases for voice check
- [ ] Set citation density benchmark
- [ ] Set research utilization target
- [ ] Add any book-specific dimensions
- [ ] Define where to store historical scores
