# Writing Analytics

> **Context:** Three scripts track writing progress at different granularities: per-section word counts, chapter-level status dashboards, and daily velocity trends. Combined with Obsidian plugins, they create a full picture of where the book stands at any moment.

---

Writing a book without progress tracking is like driving without a speedometer. You feel like you're moving, but you have no idea if you'll arrive on time. At 78,000 words target across 12 chapters, "I wrote a lot today" doesn't cut it. You need numbers.

## Word Count: The Foundation

`word_count.py` is the most-run script in the entire system. It answers one question: how many words of actual prose exist in the manuscript?

The challenge is defining "actual prose." A raw word count of every `.md` file in the vault overstates by 15-20%. Here's what gets excluded:

| Excluded Content | Why |
|-----------------|-----|
| YAML frontmatter | Metadata, not prose |
| Mermaid diagram syntax | Code, not prose |
| References sections (`## References` onward) | URLs and citation text |
| HTML comments (`<!-- ... -->`) | Internal tracking blocks |
| Obsidian comments (`%% ... %%`) | Author notes |
| Footnote markers (`[^tag]`) | Syntax, not words |

Wiki-link syntax gets special handling. `[[concepts/Data Flywheel|Data Flywheel]]` counts as two words ("Data Flywheel"), not the full path. The link destination is metadata; the display text is what the reader sees.

```bash
# Full book with per-section breakdown
python scripts/word_count.py --draft "Draft 3" --verbose

# Verbose mode shows exclusion breakdown:
#   Frontmatter (YAML):     3,456 words
#   Mermaid diagrams:          891 words
#   References section:      2,103 words
#   Comments (HTML/Obs):       234 words
#   Footnote markers:          775 words
#   ─────────────────────────────────────
#   Total excluded:          7,459 words
#   Raw file total:         88,832 words
#   Book content:           81,373 words
```

That 7,400-word gap between raw and counted is real. Without filtering, you'd think you were 10% further ahead than you actually are.

## Book Status Dashboard

`book_status.py` is the weekly check-in. It reads the frontmatter status field from every chapter and section file, counts words per chapter, and renders a color-coded progress table.

Each chapter shows:
- **Status** (outline, drafting, revising, editing, done) -- color-coded red through green
- **Word count** vs target
- **Progress bar** -- visual fill based on percentage
- **Part grouping** -- chapters organized under their parts

```bash
# Full formatted dashboard
python scripts/book_status.py

# One-line summary for scripts or dashboards
python scripts/book_status.py --brief
# Output: 81,373/78,000 words (104%) | 10/12 done | 2 in progress

# JSON for programmatic consumption
python scripts/book_status.py --json
```

The `--brief` mode is designed for embedding. Pipe it into a Slack message, a commit description, or a daily standup note. The `--json` mode feeds the book intelligence app's dashboard.

## Daily Stats: Velocity Tracking

`daily_stats.py` is the accountability tool. It takes daily snapshots of word counts, stores them in `.writing_stats.json`, and shows you trends.

What it tracks:

| Feature | Command | What You See |
|---------|---------|-------------|
| Today's writing | `--` (default) | Words added today, daily goal progress, which chapters changed |
| Record snapshot | `--record` | Saves today's count for future comparison |
| History | `--history 7` | Table of last N days with daily changes |
| Contribution graph | `--graph` | GitHub-style heatmap of writing activity over 12 weeks |
| Chapter progress | `--progress` | Progress bars for every chapter against 6,500-word target |
| Section detail | `--sections` | Per-section word changes since last snapshot |
| Writing streak | `--streak` | Consecutive days meeting the 500-word daily goal |
| Obsidian sync | `--sync` | Writes a Dashboard-Stats.md file into the vault |

The contribution graph is surprisingly motivating. Seeing a row of green squares creates the same "don't break the chain" effect as any habit tracker. Empty squares create guilt. Both work.

```bash
# Record today's snapshot and sync to Obsidian
python scripts/daily_stats.py --record --sync

# Show last 14 days of writing history
python scripts/daily_stats.py --history 14

# See which sections changed today
python scripts/daily_stats.py --sections
```

The script also installs as a git post-commit hook (`--install-hook`). Every time you commit changes to the book drafts folder, it auto-records a snapshot. No manual `--record` needed. Writing stats accumulate passively.

## Obsidian Integration

The scripts complement two Obsidian plugins:

**Novel Word Count** shows live word counts in the file explorer sidebar. Every section file displays its current word count next to the filename. This is the real-time view -- useful during active writing when you want to see a section grow toward its 1,200-word target without leaving the editor.

**Writing Goals** sets per-section targets. A progress bar appears at the bottom of each file showing percentage toward goal. When the bar turns green, the section is long enough. This plugin catches under-writing in real time; the scripts catch it in aggregate.

The combination works like this: Obsidian plugins give you the section-level view while you're writing. Scripts give you the chapter and book-level view when you step back to assess.

## Metrics That Matter

After writing 12 chapters, here are the metrics that actually influenced decisions:

| Metric | Why It Mattered |
|--------|----------------|
| Words per section | Flagged sections that were too thin (under 800 words) or bloated (over 1,800) |
| Daily velocity | Showed that 500 words/day was sustainable; 1,000 led to burnout and quality drops |
| Chapter completion dates | Made deadline estimation possible -- 3 days per chapter in drafting phase |
| Status distribution | Revealed that chapters clustered in "drafting" too long; we needed a push to "revising" |

The metrics you don't need: total time spent (hard to measure with AI assistance), words per hour (meaningless when the AI writes and you edit), revision count (the good chapters needed more revisions, not fewer).

Track output, not effort. The scripts are built around that principle.

---

**Related:** [Script Ecosystem](script-ecosystem.md) | [Dataview and Dashboards](../06-obsidian-vault/dataview-and-dashboards.md)
