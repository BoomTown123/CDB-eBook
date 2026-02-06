# Perplexity Automation

180+ research prompts across 12 chapters. Each one needs to be submitted to Perplexity Pro, waited on, and the response saved to the right folder. Doing that manually would take days of copy-paste tedium. So we automated it.

Playwright -- the same browser automation framework used for testing web apps -- drives a real browser session against Perplexity. It reads prompt files, submits them one at a time, waits for the response, copies it, and saves to the matching `answers/` folder. The whole thing runs in a visible browser window so you can watch it work and catch problems.

---

## How It Works

The automation script (`perplexity_automated.py`) follows this sequence:

1. **Opens Perplexity** in a headed Chromium browser using cached Google OAuth credentials (you log in once, then the script reuses your session)
2. **Reads prompt files** from the chapter's `research/Chapter_XX/prompts/` folder
3. **Submits each prompt** by typing into Perplexity's search input and hitting submit
4. **Waits for the response** to fully generate (watches for the copy button to appear, plus a buffer for streaming to complete)
5. **Copies the response** via the clipboard (with a fallback to direct DOM extraction if clipboard access fails)
6. **Saves to the matching `answers/` folder** -- same subfolder name, same file name, so `prompts/s_1.2_ai_first/01_comparison.md` becomes `answers/s_1.2_ai_first/01_comparison.md`
7. **Deletes the conversation** every N prompts to prevent context bleed (Perplexity builds on previous answers in a thread, which contaminates unrelated prompts)
8. **Pauses between prompts** with a configurable delay to avoid rate limiting

---

## Key Parameters

| Parameter | Default | Purpose |
|-----------|---------|---------|
| Query or `--batch` | Required | Single query string or path to prompts folder |
| `--headed` | On | Visible browser window for monitoring |
| `--keep-thread` | Off | Don't delete thread after search (useful for follow-up queries) |
| Delay between prompts | ~12s | Pause to prevent rate limiting |
| Thread deletion | Every 4 prompts | Clear conversation to prevent context contamination |

The `perplexity_search.py` script handles credential management separately -- run it once with `--login` to open a browser, complete Google OAuth manually, and save the session state. After that, the automation script picks up the cached credentials automatically.

---

## Running a Research Batch

A typical research run for one chapter:

```bash
# First time only: log in and cache credentials
python scripts/playwright_automation/perplexity_search.py --login

# Run all prompts for Chapter 7
python scripts/playwright_automation/perplexity_automated.py \
    --batch book-ai-first-company/research/Chapter_07/prompts/
```

The script processes prompts sequentially -- submitting one, waiting for the response, saving it, then moving to the next. For a chapter with 15 prompts, expect 15-20 minutes of runtime. You can continue other work while it runs.

---

## Context Bleed Prevention

This was a non-obvious problem. Perplexity maintains conversation context within a thread. If you ask about Harvey's ARR and then ask about Stripe's payment processing, the second answer might reference Harvey unnecessarily -- because Perplexity thinks you're building on the first question.

The fix: delete the thread every 4 prompts. The script clicks into thread actions and removes the conversation, forcing a clean slate. Four prompts is the sweet spot -- enough to batch related questions (like two prompts about the same section) but frequent enough to prevent contamination between sections.

---

## Failure Handling

Some prompts fail. Rate limits, timeouts, Perplexity's own errors. The script handles this in a few ways:

- **Timeout detection**: If no response appears within 60 seconds, the script logs the failure and moves on
- **Copy fallback**: If clipboard access fails, it falls back to extracting text directly from the page DOM
- **Skip existing**: By default, prompts with existing answer files are skipped -- so re-running the same batch only processes missing answers
- **Manual verification**: Running in headed mode means you can visually spot issues -- stuck pages, CAPTCHA challenges, authentication problems

For a typical 15-prompt batch, 1-2 failures is normal. You can re-run the batch with skip-existing to pick up just the gaps.

---

## Model Selection

The script runs against whatever model you've selected in your Perplexity Pro session. For this book, I used Claude Sonnet within Perplexity's interface -- it produced longer, more detailed responses with better source attribution than the default model. The model choice within Perplexity matters for research quality: some models return surface-level summaries while others dig into primary sources and include methodology details.

---

## Practical Tips

**Run per-chapter, not the whole book at once.** 15 prompts is a clean batch. 180 prompts in one session invites rate limits and session timeouts.

**Use headed mode.** Always. The 30 seconds it takes to spot a stuck page saves you from discovering 10 empty answer files after the batch completes.

**12-second delays work.** Faster and you hit rate limits. Slower and you're wasting time. Twelve seconds consistently avoids throttling without padding the runtime.

**Delete every 4 prompts.** Not every prompt, not every 10. Four keeps related prompts together while preventing cross-topic contamination.

**Check results before writing.** A quick scan of the `answers/` folder catches low-quality responses that need re-running before synthesis begins. Better to re-run one prompt than to write a section and discover the research was thin.

---

**Related:** [Research Architecture](research-architecture.md) | [Synthesis and Extraction](synthesis-and-extraction.md) | [Script Ecosystem](../07-automation/script-ecosystem.md)
