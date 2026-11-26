# How I used AI tools

The full record is in [ai-log/](../ai-log/): every prompt, what the AI did, my decision, and every edit it made to my documents. Commit timestamps are the timetable.

- **Tool:** Claude Code (Claude Opus 5.5), working directly in this repository.
- **I did:** the testing approach and pillars (see [00-initial-prompt.md](../ai-log/00-initial-prompt.md)), the assumptions for the open questions, the Summarize feature definition and test ideas, and the regression approach for the incidents, the log and the scale-up ([notes/](../notes/)). I set the order of work, cut the scope where the AI over-produced (8 Summarize cases → 2), and corrected it where it misread (Summarize cases first looked like Q&A tests).
- **The AI did:** the repo structure and templates from the brief; open questions I validated; a first-pass verdict on the 20 log lines, which I reviewed; proofreading with a change log; the mocked Summarize cases and test code; and drafting the deliverables from my notes plus defaults I approved (deliverables/PLAN.md).
- **How I checked it:** reviewed each verdict against the policy file (the AI got L11 wrong at first and corrected it); every AI edit to my text is listed in [ai-log/edits.md](../ai-log/edits.md); the harness runs and its verdicts match my labels on 9 of 9.
- **Time:** about 3 h of my own work. Not counted: a recruiter call (~10 min), a break (20 min), and defining the invented Summarize feature (~30 min, done to have something concrete to test).
