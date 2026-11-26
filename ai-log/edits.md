# Changes AI made to my documents

Every change Claude made to a file I started, so I can review it. Content added by AI is marked "(AI-added)" or "AI first pass" inside the files.

| File | Change | Why |
|---|---|---|
| `InitialPrompt.md` | Moved to `ai-log/00-initial-prompt.md`. **Text unchanged.** | It is the first prompt in the audit trail. |
| `SummarizeFeafutre.md` | Renamed to `features/Summarize.md` (typo); replaced the one-line placeholder with a definition/risks/tests template. | The prompt called it SummaryFeature.md; it now sits in a features folder. |
| `fraga-*.csv` | Moved to `data/`. Content unchanged. | Separate data from notes. |
| `HowToTest.md` | Moved to `notes/`. Converted ". " bullets to Markdown lists; gave each bullet a bold lead-in; tightened grammar (e.g. "priority policies" → "use … policies first", "couldn't found" → "no … rule was found"). **No idea removed or added.** | Readability. |
| `OpenQuestions.md` | Moved to `notes/`. Your 5 questions reworded for clarity (meaning kept) and numbered Q1–Q3, Q9, Q10. Each now has Assumption / Impact / Status fields. Added Q4–Q8 and Q11–Q19, marked "(AI-added)". Grouped by theme. | Template for recording assumptions; cover gaps in the brief. |
| `TestForIncidents.md` | Moved to `notes/`. Kept your one-line purpose; added a per-incident template and guiding questions for each incident. | You asked for questions and a skeleton. |
| `TestForUpscaling.md` | Moved to `notes/`. Kept your purpose line; added the v1→v2 numbers table, question areas and a test plan skeleton. **Flagged:** documents grow ~13x (40,000 / 3,000), not 15x. | Correctness of a number you used in the pillars. |
| `TestForCurrentLog.md` | Moved to `notes/`. Kept your purpose line; added an **AI first-pass verdict** for all 20 log lines (to be verified by you) and a failure-type table. | Gives you a starting point to verify rather than derive from scratch. |
| `README.md` | Replaced the placeholder with a repo guide. | Navigation for reviewers. |
