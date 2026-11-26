# Summarize case file (new in v2)

The brief only says v2 "adds a new Summarize case file feature". Everything below is **assumed**. Fill it in, mark each item as an assumption, and link it to notes/OpenQuestions.md.

## Definition (assumed)

| Aspect | Assumption |
|---|---|
| Input | _(case file: documents, notes, emails? formats? size limit?)_ |
| Output | _(length, structure: facts, timeline, open actions, applicable policies)_ |
| Who uses it, and when | |
| Does it cite policies or case documents? | Can't show detail on other cases but it should cite policies |
| Language(s) | Only one |
| Latency target (does the 8 s apply?) | Different one |
| Where the case file and summary are stored and logged | TBD |

## Risks

Ask yourself:
- **Privacy (P-107):** can a summary pull in content from another case? (Retrieval scoped by case, cache leakage between users.)
- **Faithfulness:** does every fact in the summary appear in the source? Are amounts, dates and names copied exactly?
- **Omission:** is a critical fact dropped (deadline, appeal window, decision)?
- **Invented policy links:** if it maps a case to policies, are they current (Incident 1)?
- **Size:** what happens when a case file exceeds the context window? Is it truncated silently?
- **Load:** long prompts at peak cost GPU time shared with 4 other apps.
- **Anonymisation:** case files contain names and personal data. They must be stored for audit logging, so how that data is stored needs close scrutiny.
- **Memory:** does Summarize need to know the earlier messages in the conversation? For example: "Summarize this case, taking into account the policies we discussed earlier."
- **Usage:** if we expect heavy use, should Summarize have a GPU quota? How is it prioritised against Fråga's other use cases?
- **Cost:** it is likely more expensive (time, GPU usage, policy lookups). Monitor the cost per summary so we can optimise it, but remember the tenet: avoid embarrassing answers.
