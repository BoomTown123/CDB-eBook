# Book Vault Structure Template

A fill-in-the-blank starting point for organizing an Obsidian vault around a book manuscript.

---

## Top-Level Structure

```
[your-book-vault]/
├── Book/
│   └── drafts/
│       └── Draft 1/
│           ├── 01-[Part-1-Name]/
│           │   ├── 00-Part-Intro.md
│           │   ├── 01-[Chapter-1-Name]/
│           │   │   ├── 00-Chapter-Intro.md
│           │   │   ├── 01-[Section-1].md
│           │   │   ├── 02-[Section-2].md
│           │   │   └── 99-Chapter-Summary.md
│           │   └── 02-[Chapter-2-Name]/
│           │       └── ...
│           ├── 02-[Part-2-Name]/
│           │   └── ...
│           └── [NN]-[Part-N-Name]/
│               └── ...
├── concepts/              # Atomic concept notes (one per idea)
├── mocs/                  # Maps of Content (navigation hubs)
├── notes/
│   ├── research/          # Research notes per chapter
│   │   ├── Chapter_01/
│   │   │   └── answers/   # Research answers by section
│   │   └── Chapter_02/
│   │       └── ...
│   └── case-studies/      # Case study notes
├── planning/              # Writing reference documents
├── templates/             # Templater templates
├── _author/               # Voice system files
├── _prompts/              # AI prompt library
├── Dashboard.md           # Progress tracking dashboard
└── .obsidian/             # Obsidian settings and plugins
```

## Naming Conventions

| Content Type | Pattern | Example |
|--------------|---------|---------|
| Part folder | `XX-Part-Name/` | `01-Foundations/` |
| Chapter folder | `XX-Chapter-Name/` | `03-Market-Analysis/` |
| Part intro | `00-Part-Intro.md` | Always `00-` prefix |
| Chapter intro | `00-Chapter-Intro.md` | Always `00-` prefix |
| Section file | `XX-Section-Name.md` | `02-Competitive-Landscape.md` |
| Chapter summary | `99-Chapter-Summary.md` | Always `99-` prefix |

Use kebab-case for folder and file names. Numbers are zero-padded to two digits.

## Your Book Structure

Fill in your book's breakdown:

| Part | Name | Chapters | Sections/Chapter |
|------|------|----------|-----------------|
| 1 | [Part 1 Name] | Ch [X]-[Y] | ~[N] sections |
| 2 | [Part 2 Name] | Ch [X]-[Y] | ~[N] sections |
| 3 | [Part 3 Name] | Ch [X]-[Y] | ~[N] sections |
| 4 | [Part 4 Name] | Ch [X]-[Y] | ~[N] sections |

**Totals:** [X] parts, [Y] chapters, ~[Z] sections
**Word targets:** [TOTAL] words (~[PER CHAPTER] per chapter, ~[PER SECTION] per section)

## Recommended Plugins

| Plugin | Purpose |
|--------|---------|
| Dataview | Dynamic queries on frontmatter fields |
| Templater | Auto-fill templates when creating notes |
| Novel Word Count | In-editor word counts per file/folder |
| Kanban | Visual chapter status tracking |
| Writing Goals | Per-file word count targets |

---

## Customization Checklist

- [ ] Replace all `[PLACEHOLDERS]` with your book's values
- [ ] Decide on number of parts and chapters
- [ ] Set word targets per chapter and section
- [ ] Install recommended plugins
- [ ] Create the folder structure before writing
