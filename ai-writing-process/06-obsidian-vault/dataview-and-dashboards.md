# Dataview and Dashboards

Here's the thing about tracking progress on an 81-section book: you stop doing it. Not because you don't care, but because manually updating a spreadsheet after every writing session is friction that accumulates until you just... don't. By chapter 5, your tracking sheet is 3 weeks stale and you're guessing what's done.

Dataview eliminates this entirely. It's an Obsidian plugin that queries frontmatter like a database -- no manual updates, no stale data. Open the Dashboard, and it reads every section's `status` field in real time. 47 done, 22 revising, 12 drafting. The frontmatter *is* the tracking system. You update the section's status while writing, and the Dashboard reflects it instantly.

---

## What Dataview Actually Does

Dataview treats your vault as a queryable database. Every Markdown file with YAML frontmatter becomes a row. Every frontmatter field becomes a column. You write queries in a SQL-like syntax, and Dataview renders live tables directly in your notes.

For a book vault with standardized frontmatter across 81 sections, 12 chapter intros, 4 part intros, 9 concept notes, and assorted research files -- that's a database with real utility.

```dataview
TABLE target_words, status
FROM "Book/drafts/Draft 1"
WHERE type = "section"
SORT chapter ASC, section ASC
```

That query produces a live table of every section in the book, sorted by chapter and section number, showing word targets and current status. No script to run. No export to update. It refreshes every time you open the note.

---

## The Dashboard

`Dashboard.md` is the nerve center. A single file that assembles everything you need to know about the manuscript's state:

**Progress overview** -- chapters and sections grouped by status, with counts. At a glance: how much is done, how much is in progress, how much hasn't started.

**Per-part breakdowns** -- each of the 4 parts shows its chapters and sections with status. You can see that Part II (Building) is fully drafted while Part IV (Sustaining) is still in revising.

**Word count targets** -- chapter-level targets (6,500 each) and the aggregate (78,000). The Novel Word Count plugin handles actual counts in the editor; Dataview tracks targets.

**Graph health** -- sections missing concept links, orphan files with low link counts, concept hub connectivity. This section surfaces structural problems before they compound.

**Currently drafting** -- live list of sections with `status: drafting`. When you sit down to write, you know exactly where to start.

The Dashboard doesn't require maintenance. Add a new section, give it frontmatter, and it appears in the relevant queries automatically. Change a status from `drafting` to `revising`, and the counts update on next open.

---

## Queries Worth Stealing

These are the queries that earned their place in the Dashboard through daily use:

### Sections Progress by Chapter

Shows how each chapter is progressing at a glance:

```dataview
TABLE WITHOUT ID
  ("Chapter " + chapter) as Chapter,
  length(filter(rows, (r) => r.status = "done")) as "Done",
  length(filter(rows, (r) => r.status = "drafting")) as "Drafting",
  length(filter(rows, (r) => r.status = "outline")) as "Outline",
  length(rows) as "Total"
FROM "Book/drafts"
WHERE type = "section"
GROUP BY chapter
SORT chapter ASC
```

### Sections Missing Concept Links

Finds sections that aren't connected to any concept note -- orphan candidates:

```dataview
TABLE WITHOUT ID
  file.link as Section,
  chapter as "Ch",
  status as Status
FROM "Book/drafts"
WHERE type = "section" AND (!key_concepts OR length(key_concepts) = 0)
SORT chapter ASC, section ASC
```

The full query library -- orphan detection, concept coverage, chapter-specific views, inline queries -- lives in the vault's `_vault-guide/08-Dataview-Queries.md`. These three are the ones you'll use daily.

---

## Writing Velocity Tracking

Dataview handles *what's done*. For *how fast* -- words per day, pace toward the 78,000-word target -- `daily_stats.py` calculates velocity from git diffs. Obsidian's Novel Word Count plugin shows live counts as you type. The Writing Goals plugin provides visual indicators when a section hits its 1,200-word target. Three layers: Dataview for status, Python for trends, plugins for right now.

---

## Plugin Stack

Six plugins together handle the full spectrum of tracking and productivity:

| Plugin | Purpose | Why It Matters |
|--------|---------|----------------|
| **Dataview** | Dynamic queries on frontmatter | Live dashboards without manual updates |
| **Templater** | Auto-fill templates with metadata | Consistent frontmatter on every new file |
| **Novel Word Count** | In-editor word counts | See progress while writing, not after |
| **Kanban** | Visual progress tracking | Move chapter cards across status columns |
| **Writing Goals** | Per-section word targets | Visual indicator when a section hits target |
| **Daily Stats** | Writing velocity tracking | Daily and weekly word count trends |

Kanban provides a simpler view -- drag chapter cards across status columns for the 30-second "where am I?" check between sessions.

---

## What This Adds Up To

Obsidian + Dataview + standardized frontmatter turns a folder of Markdown files into a live project management system. No Notion, no Jira, no spreadsheet.

The catch: it only works if frontmatter is consistent. One section with `drafitng` instead of `drafting` disappears from every query. One missing `type: section` throws the Dashboard's count off. Validate early -- run a Dataview query that counts all sections and compare it to how many you expect. If the numbers don't match, a frontmatter field is wrong somewhere.

The investment: about an hour to learn Dataview basics, 2 hours to build the Dashboard. The return: you never update a tracking spreadsheet again.

---

**Related:** [Templates and Frontmatter](templates-and-frontmatter.md) | [Writing Analytics](../07-automation/writing-analytics.md)
