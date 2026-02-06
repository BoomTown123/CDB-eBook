# Word Count Tracker Template

Pseudocode and logic for building a word count script tailored to a book manuscript in Obsidian.

---

## Purpose

Count words in your manuscript, excluding metadata, diagrams, and reference sections that inflate the count.

## What to Exclude

| Content | Why |
|---------|-----|
| YAML frontmatter (`---` to `---`) | Metadata, not prose |
| Mermaid diagram blocks | Generated visuals |
| References sections (`## References` to end) | Citation listings |
| HTML comments (`<!-- ... -->`) | Internal tracking notes |
| Empty lines | Not words |

## Core Logic (Pseudocode)

```python
def count_words(file_path):
    content = read_file(file_path)

    # Strip YAML frontmatter (first block only)
    content = remove_between("---", "---", content, first_only=True)

    # Strip Mermaid blocks
    content = remove_between("```mermaid", "```", content)

    # Strip references section (## References to end of file)
    content = remove_after("## References", content)

    # Strip HTML comments
    content = remove_between("<!--", "-->", content)

    # Count remaining words
    return len(content.split())
```

## Output Formats

### Per-Section (verbose mode)

```
Chapter 6: [CHAPTER TITLE]
  6.1 [Section Title]              1,187 words  (target: 1,200)  [OK]
  6.2 [Section Title]              1,243 words  (target: 1,200)  [+4%]
  6.3 [Section Title]                892 words  (target: 1,200)  [-26%]
  ...
  Chapter total:                   6,412 words  (target: 6,500)
```

### Per-Chapter Summary (default)

```
Chapter  Title                        Words    Target   %      Status
1        [Chapter Title]              6,234    6,500    96%    [OK]
2        [Chapter Title]              6,891    6,500    106%   [OVER]
3        [Chapter Title]              4,102    6,500    63%    [SHORT]
...
TOTAL                                78,122   78,000   100%
```

## CLI Interface

```bash
# Default: all chapters, summary view
python scripts/word_count.py

# Specific chapter with section breakdown
python scripts/word_count.py --chapter 6 --verbose

# Specific draft
python scripts/word_count.py --draft "Draft 2"

# JSON output for tooling
python scripts/word_count.py --json

# Combined
python scripts/word_count.py --draft "Draft 3" --chapter 12 --verbose
```

## Color Coding

| Status | Condition | Color |
|--------|-----------|-------|
| OK | Within 10% of target | Green |
| OVER | More than 10% above target | Yellow |
| SHORT | More than 10% below target | Red |

## Key Features to Build

- [ ] Exclude frontmatter, diagrams, references, and comments
- [ ] Per-section breakdown with `--verbose` flag
- [ ] Per-chapter summary as default view
- [ ] JSON output with `--json` flag
- [ ] Filter to specific chapter with `--chapter N`
- [ ] Draft selection with `--draft "Draft N"`
- [ ] Color-coded output for at-a-glance status
- [ ] Read word targets from each file's frontmatter `target_words` field

## Dependencies

- Python 3.8+
- `pyyaml` -- frontmatter parsing
- `rich` (optional) -- colored terminal output
