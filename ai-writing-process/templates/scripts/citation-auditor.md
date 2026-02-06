# Citation Auditor Template

Pseudocode and logic for building a citation audit script that checks density, finds uncited claims, and detects common footnote problems.

---

## Purpose

Audit citation density across your manuscript and flag statistical claims that lack footnotes.

## What to Detect

### Citation References

Two patterns to match:

| Pattern | Location | Example |
|---------|----------|---------|
| `[^tag-name]` | Body text (inline reference) | `reached $100M ARR[^harvey-arr]` |
| `[^tag-name]: ...` | References section (definition) | `[^harvey-arr]: Harvey 2024...` |

### Uncited Statistical Claims

Regex patterns that should typically have a citation nearby:

```
Percentages:        \d+(\.\d+)?%
Dollar amounts:     \$[\d.,]+\s*(million|billion|M|B|K)?
Large numbers:      \d{1,3}(,\d{3})+
Multipliers:        \d+x\s+(faster|slower|more|better|cheaper)
Ratios:             \d+\s+out of\s+\d+
Growth phrases:     doubled|tripled|grew by
Time specifics:     in\s+\d{4}|since\s+\d{4}
```

## Core Logic (Pseudocode)

```python
def audit_citations(section_path):
    content = read_file(section_path)
    body_text = extract_body(content)  # exclude frontmatter, code blocks

    # Count citation references in body
    inline_refs = find_all(r'\[\^[\w-]+\]', body_text)

    # Count citation definitions in references
    definitions = find_all(r'^\[\^[\w-]+\]:', content)

    # Count words (excluding metadata)
    word_count = count_words(section_path)

    # Calculate density
    density = len(inline_refs) / (word_count / 1000)

    # Find uncited stats
    stats = find_all(STAT_PATTERNS, body_text)
    uncited = [s for s in stats if no_citation_within(s, radius=50_chars)]

    # Find orphaned footnotes
    orphaned_refs = [r for r in inline_refs if r not in definitions]
    orphaned_defs = [d for d in definitions if d not in inline_refs]

    # Find duplicate URLs
    urls = extract_urls_from_definitions(content)
    duplicates = find_duplicate_urls(urls)

    return {
        'citations': len(inline_refs),
        'words': word_count,
        'density_per_1k': density,
        'benchmark': word_count / [YOUR WORDS PER CITATION],
        'uncited_claims': uncited,
        'orphaned_refs': orphaned_refs,
        'orphaned_defs': orphaned_defs,
        'duplicate_urls': duplicates
    }
```

## Output Format

```
Section 6.1: [Section Title]
  Citations: 8
  Words: 1,187
  Density: 6.7 per 1,000 words
  Benchmark: 7.9 (1 per 150 words)
  Status: BELOW BENCHMARK

  Uncited claims:
    Line 45: "85% of enterprises..." -- needs citation
    Line 78: "$4.2 billion market..." -- needs citation

  Orphaned references:
    [^missing-def] -- referenced but never defined

  Duplicate URLs:
    https://example.com/report -- used by [^tag-a] and [^tag-b]
```

## Benchmark Targets

Fill in based on your citation density goals:

| Section Length | Target Citations | Density |
|---------------|-----------------|---------|
| 800 words | [N] | [N] per 1K |
| 1,200 words | [N] | [N] per 1K |
| 1,800 words | [N] | [N] per 1K |

## Key Features to Build

- [ ] Citation counting per section
- [ ] Density calculation against your benchmark
- [ ] Uncited statistical claim detection with line numbers
- [ ] Duplicate URL detection (same URL, different footnote tags)
- [ ] Orphaned footnote detection (both directions)
- [ ] Per-chapter summary view
- [ ] `--fix` mode for auto-standardization of duplicates
- [ ] `--dry-run` for previewing fixes before applying

## Dependencies

- Python 3.8+
- `re` (standard library) -- regex matching
- `pyyaml` -- frontmatter parsing
- `rich` (optional) -- colored terminal output
