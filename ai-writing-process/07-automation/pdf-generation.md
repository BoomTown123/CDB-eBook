# PDF Generation

> **Context:** The book needs two PDF outputs: an internal draft for author review and a clean reader version for publication. `generate_pdf.py` handles both, with Mermaid diagram rendering and persistent caching.

---

Generating a PDF from an Obsidian vault sounds simple until you actually try it. Wiki-links need resolving. YAML frontmatter needs stripping. Mermaid diagrams need rendering to SVG. Internal comment blocks need hiding in reader mode but showing in author mode. And the whole thing needs to look like a book, not a web page.

## Two Modes, Two Audiences

| Mode | Flag | Who It's For | What It Shows |
|------|------|-------------|---------------|
| Internal | `--mode internal` (default) | Author, reviewers | Everything: research source blocks, internal notes, draft metadata |
| Reader | `--mode reader` | Publication, distribution | Clean text only: no `<!-- INTERNAL: ... -->` blocks, formatted citations, professional layout |

The internal mode is your working copy. It includes the `<!-- INTERNAL: Research Sources -->` blocks that track which research files informed each section. When you're reviewing chapter 8 and wondering "did I use the McKinsey study here?", the internal PDF answers that without switching to Obsidian.

The reader mode strips all of that. What remains is the book as your audience will see it.

## How the Pipeline Works

The PDF generator is a multi-module package (`pdf_generator/`) with 11 files handling discovery, parsing, rendering, Mermaid caching, table of contents, and styling. The pipeline:

1. **File discovery.** Reads all markdown files from the draft folder in order: part intros, then chapter folders, then sections within each chapter. The ordering is deterministic -- files sort by their numeric prefixes (`01-`, `02-`, etc.).

2. **Frontmatter stripping.** Every file starts with YAML frontmatter (`---` delimited). The parser removes it. In reader mode, it also removes Obsidian comments (`%%...%%`) and HTML comment blocks (`<!-- INTERNAL: ... -->`).

3. **Link resolution.** Wiki-links like `[[concepts/Data Flywheel|Data Flywheel]]` become plain text in the PDF. The display text is preserved; the link syntax is stripped.

4. **Mermaid rendering.** Diagrams in ` ```mermaid ` code blocks are rendered to SVG, then embedded inline. This uses `mmdc` (Mermaid CLI) locally when available, with an API fallback. Rendering happens in parallel -- 4 workers by default.

5. **Markdown to HTML.** The Python `markdown` library converts the processed markdown to HTML.

6. **HTML to PDF.** WeasyPrint renders HTML to PDF with CSS-based styling. This gives full control over typography, margins, page breaks, and layout -- more flexible than Pandoc for book-specific formatting.

## Mermaid Caching

This is the performance-critical piece. The book has dozens of Mermaid diagrams -- architecture flows, decision trees, sequence diagrams. Rendering each one through `mmdc` takes 2-5 seconds. Without caching, a full book PDF takes 10+ minutes.

The caching system (`pdf_generator/cache.py`) hashes the diagram source text and stores the rendered SVG in `output/cache/`. On subsequent runs, only modified diagrams re-render. A full book PDF with warm cache takes under 60 seconds.

```bash
# Show what's cached
python scripts/generate_pdf.py --cache-stats

# Force fresh rendering
python scripts/generate_pdf.py --clear-cache

# Disable caching entirely (slow, useful for debugging)
python scripts/generate_pdf.py --no-cache

# More parallel workers for faster rendering
python scripts/generate_pdf.py --parallel 8
```

## Commands

```bash
# Default: internal mode, Draft 3
python scripts/generate_pdf.py

# Reader-ready PDF from specific draft
python scripts/generate_pdf.py --draft "Draft 3" --mode reader

# Custom output filename
python scripts/generate_pdf.py --output my_book.pdf

# Include removed/archived content (excluded by default)
python scripts/generate_pdf.py --include-removed
```

The output lands in `output/` with a timestamped filename: `Building_AI_First_Companies_Draft_3_reader_20250205_1430.pdf`. Timestamps prevent overwriting previous versions -- useful when comparing drafts.

## Why WeasyPrint

We tried Pandoc first. It works for straightforward documents, but book layout demands CSS-level control. WeasyPrint renders HTML with CSS, which means:

- **Page breaks.** CSS `break-before: page` on chapter headers. No manual page break markers in the markdown.
- **Typography.** Font families, sizes, line heights, and margins controlled in one stylesheet. Change the body font across the entire book in one line.
- **Headers/footers.** Running headers with chapter titles, page numbers, consistent formatting.
- **Print optimization.** Widows, orphans, column balancing -- CSS properties that Pandoc's intermediate LaTeX can handle but with more friction.

The trade-off: WeasyPrint requires `pango` on macOS (`brew install pango`) and the `weasyprint` Python package. The dependency is heavier than Pandoc. Worth it for the layout control.

## Dependencies

```bash
pip install markdown weasyprint pyyaml
brew install pango  # macOS only
npm install -g @mermaid-js/mermaid-cli  # Optional, for local Mermaid rendering
```

Without `mermaid-cli` installed, the generator falls back to an API-based renderer. Slower, but works without Node.js.

---

**Related:** [Script Ecosystem](script-ecosystem.md)
