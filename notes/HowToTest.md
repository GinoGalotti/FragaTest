How to test policies

Here I will try to document some ideas around what things we could treat on the actual usage of fraga. What are the edge cases I assume that would happen based on my understanding of the product and the example policies. 

. Questions should be categorised on topics, and we should check at the policies around those topics. 
. We need ways to audit that the right policies are marked on the right topics (policies might touch several topics).
. I am assuming the API has a debug mode where we can get as an answer: time it took to process (without counting the extra time for debugging), policies that were consulted, certainty score on the answer, topic that was observed, keywords marked from the response. We could use that data to improve our system. Ideally this will also be available from production data to compare with current versions (and user satisfaction), although data might need to be anonymised or follow some ISO/rules.
. If the question doesn't specify a clear topic, we should validate that we ask for clarifications instead of assuming or hallucinating (no embarrassing answers).
. Some key words should have priority. Rules about child or disabled people should priority policies specific to those groups. If not, fail to general policies about the topic (parking, housing) and specify that it couldn't found specific on the minority group.
. Amounts are important. We should make sure that amounts are validated. On answers with sources, the test should assert that the source contains the information (we can mock it on quick tests). The answers MUST contain some key things, even if the rest of the wording changes. Example: when asking for the parking permit it MUST contain 3 years if that's the case. 
. Rules for ISO / GDPR / etc must always be followed. Some policies (like P-107 on the example) affect Fraga answers, and we need to test those edges in specific. Try to force questions that will ask for sensitive data, etc.
. ((Assumption)) We should prevent users from using Fraga as a general AI and respond accordingly if the use case is not around policy questions. We should limit usage on generative AI, coding, etc. 
. ((Assumption)) If users query Fraga with cases that should be flagged for review, we should test that. Maybe we have some ruling that if someone is asking for something that is clearly illegal, it must be flagged.
