# Building Custom Skills

> **Context:** The book writing system uses 14 Claude Code skills. This document explains how to design and build your own skills for book projects -- the anatomy, the design principles, and the process from identifying a repeating task to shipping a working skill.

---

A skill should be something you can explain to a competent colleague in 2 minutes. If it takes longer, break it into multiple skills. If it takes less than 30 seconds, it's probably a script, not a skill.

That's the design bar. Everything in this document works backward from it.

## Skill Anatomy

Every Claude Code skill has three layers:

```
.claude/skills/skill-name/
  SKILL.md          # The instruction file
  scripts/          # Python scripts the skill invokes
  references/       # YAML configs, pattern files, examples
```

**`SKILL.md`** is the brain. It contains the skill's purpose, inputs, outputs, step-by-step process, and definition of done. This is what Claude reads when the skill is invoked. It's the only file that *must* exist.

**`scripts/`** handles the mechanical work. File scanning, pattern matching, counting, searching, formatting -- anything that's deterministic and repeatable goes here. Python is the default because it handles file I/O and text processing well, but any language works.

**`references/`** stores configuration. Pattern lists, approved phrases, scoring weights, templates. These files change when your standards evolve but the process stays the same.

Not every skill needs all three layers. The `publish-review` skill is just a SKILL.md with a detailed checklist -- no scripts, no references. The `research-reader` skill has 9 scripts and no reference files. The `check-voice` skill uses all three: instructions, a scanning script, and a `voice_patterns.yaml` reference file.

## Skill vs Agent (One More Time)

This distinction matters enough to repeat.

**Skills = procedures.** They define steps, tools, and outputs. "Run these 5 scripts in this order, compile results into this format, output to this location." A skill is a recipe.

**Agents = personas.** They define voice, priorities, and judgment. "You are a reviewer. Check for these patterns. Use this scoring rubric. Report in this format." An agent is a role.

Skills can invoke agents. The `book-chapter-writer` skill invokes three agents at different steps. Agents execute within skills -- they do work, they don't orchestrate.

When you're building something new, ask: "Is this about *what to do* or *who does it*?" If it's a process with defined steps, build a skill. If it's a perspective with judgment calls, configure an agent.

## Design Principles

### 1. Concise Context

Claude is already smart. You don't need to explain what markdown is or how footnotes work. Write the SKILL.md like you're briefing a senior colleague: state the goal, define the process, specify the edge cases, stop.

Bad: "Markdown footnotes are a way to add references to your text. They use the syntax [^tag] inline and [^tag]: at the bottom..."

Good: "Use named footnote keys: `[^harvey-arr]`. One tag per unique source URL."

### 2. Appropriate Degrees of Freedom

Rigid for fragile tasks. Flexible for creative tasks. Citation format is fragile -- one inconsistency breaks the reference system. Voice tone is creative -- overly rigid rules produce stilted prose.

| Task | Freedom Level | Why |
|------|--------------|-----|
| Citation format | Rigid | One wrong format breaks the system |
| File naming | Rigid | Scripts depend on consistent naming |
| Voice and tone | Flexible | Creativity needs room |
| Section structure | Semi-rigid | Patterns help, but every section is different |
| Diagram style | Flexible | Context determines the right visualization |

### 3. Progressive Disclosure

Don't load everything upfront. The skill metadata (name, description) gives Claude enough to know *when* to use the skill. The SKILL.md gives the full process. Reference files provide patterns and configurations only when a specific step needs them.

The `book-chapter-writer` SKILL.md is 800+ lines. But Claude doesn't read all 800 lines when invoked -- it reads the plan display template first, checks research status, then reads only the steps it needs to execute. Information is available when it's needed, not before.

### 4. Scripts for Repeatability

If you do it twice, script it. The research-reader skill has 9 Python scripts not because the work is hard but because it's *repetitive*. Searching research files, extracting statistics, formatting citations -- these are the same operations run hundreds of times across 12 chapters. Manual execution introduces inconsistency. Scripts eliminate it.

The threshold: if a task involves file I/O and you'll run it more than 5 times, write a script. If it's purely cognitive (voice judgment, argument quality), keep it in the SKILL.md instructions.

## 6-Step Creation Process

### 1. Identify the Repeating Task

Look for tasks you do more than 3 times per chapter. For us, these included: checking voice patterns, counting citations, finding unused research, auditing cross-chapter links, and classifying section openings. Each became a skill.

### 2. Document the Manual Steps

Before automating, write down exactly what you do when performing the task manually. Not what you *think* you do -- what you *actually* do. This captures edge cases that muscle memory handles but instruction documents miss.

### 3. Write the SKILL.md

Define: purpose (one sentence), inputs (what triggers the skill), outputs (what it produces), process (numbered steps), and definition of done (checklist). Keep it under 200 lines for single-purpose skills. The chapter-writer is an exception because it orchestrates multiple agents and steps.

### 4. Script the Mechanical Parts

File scanning, pattern matching, counting, formatting -- anything deterministic. Leave judgment calls to the agent executing the skill. The voice-check script counts kill list violations. The *decision* about whether a specific use of "leverage" is actually problematic stays with the reviewer agent.

### 5. Add Reference Files

Pattern lists, approved phrases, scoring weights, templates. Store them as YAML for easy parsing or markdown for human readability. These files are the configuration knobs you'll tune over time.

### 6. Test with Real Content

Run the skill against actual chapter content, not test files. A voice-check skill that works on a 500-word test document might fail on a 1,200-word section with code blocks, footnotes, and Mermaid diagrams. Real content has edges that test content doesn't.

## Example: Creating the Voice Check Skill

**The problem:** Manual voice review was inconsistent. Reviewers caught different issues on different passes. No baseline score. No way to track improvement across drafts.

**Manual steps documented:**
1. Scan for kill list phrases ("important to note," "let's delve," "robust")
2. Check for hedging language ("somewhat," "arguably," "it could be said")
3. Look for AI-signal patterns ("leverage," "comprehensive framework")
4. Count approved voice markers ("Here's the thing," "I've seen this fail when")
5. Assess overall voice match (subjective)

**What got scripted:** Steps 1-4. Pattern matching against defined lists. Counting. Scoring.

**What stayed in instructions:** Step 5 -- overall voice judgment. The script produces a score. The reviewer interprets whether that score matches the *feel* of the prose.

**Reference file:** `voice_patterns.yaml` with four lists: kill_phrases, hedging_patterns, ai_signals, approved_markers. Adding a new pattern to any list takes one line of YAML.

**Result:** Consistent, repeatable, runs in seconds. Base score of 70, adjustments per pattern type, target of 85+. The scoring rubric was calibrated across Draft 2 -- we ran it on sections we knew were good, sections we knew were bad, and tuned the weights until the scores matched our editorial judgment.

## What Makes a Good Skill

A few heuristics from building 14 of them:

- **Single responsibility.** `check-voice` checks voice. It doesn't also check citations. When you're tempted to add "and also check X," make a separate skill.
- **Clear inputs and outputs.** The skill should declare what it needs (chapter number, draft path, section ID) and what it produces (report file, score, issue list).
- **Fail gracefully.** If a research file is missing or a section file has unexpected formatting, the skill should report the problem, not crash silently.
- **Iterate in production.** Don't over-design the first version. Ship something that handles the 80% case, then add edge case handling as you hit real problems. The voice-check skill went through 4 iterations. Each one was triggered by a real chapter that exposed a gap.

---

**Deep dives:** [Agent Architecture](agent-architecture.md) | [Quality Skills](quality-skills.md)
