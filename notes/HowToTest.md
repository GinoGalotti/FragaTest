# How to test policy answers

Ideas for testing Fråga's real usage, and the edge cases I expect based on my understanding of the product and the example policies.

- **Topics.** Questions should be categorised by topic, and we check the policies for that topic.
- **Topic tagging audit.** We need a way to check that each policy is tagged with the right topics (a policy can cover several).
- **Debug mode (assumption).** The API has a debug mode that returns: processing time (excluding debug overhead), policies consulted, a certainty score, the detected topic, and keywords extracted from the response. We use this to improve the system. Ideally it is also available for production data, so we can compare versions against user satisfaction. The data may need anonymising to meet GDPR/ISO requirements.
- **Unclear questions.** If a question has no clear topic, Fråga should ask for clarification instead of assuming or hallucinating (no embarrassing answers).
- **Keyword priority.** Some keywords take priority. Questions about children or disabled people should use policies specific to those groups first. If none exist, fall back to the general policy for the topic (parking, housing) and say that no group-specific rule was found.
- **Amounts and durations.** These must be validated. For answers with sources, the test asserts that the source contains the stated value (mocked in quick tests). Answers MUST contain the key facts, even if the wording changes. Example: a parking permit answer must contain "3 years".
- **Compliance rules (GDPR, ISO, etc.).** These must always be followed. Some policies govern Fråga's own behaviour (e.g. P-107), and their edges need specific tests. Try questions that ask for sensitive data.
- **Out of scope (assumption).** Users should not be able to use Fråga as a general AI assistant. If a request is not about policy (generative writing, coding, etc.), Fråga declines.
- **Flagging (assumption).** Some requests should be flagged for review, e.g. clearly illegal requests. We test that they are flagged.
