Open questions.

. We define that answers should be under 8s 95% of the time. Is it acceptable that during peak hours we don't hit the 8s? Or is it only acceptable on the cases that the question touches many files? 
. Can the user specify the effort / certainty of the answer? Depending on how long it takes for a simple query, 8s might be unrealistic in the scenarios when the user wants to triple check the answer and references.
. Does the solution need to support other languages, or only Swedish? Swedish and English? Translation might add to the computing time.
. Is the 8s only counting from the moment we get the API call? Can the user upload files (or only ask in plain text)? In case we have an SLA on uploading the file (which depends on their setup) or processing the files.
. Do we have a commitment in the fail rate of the answers (how often they can thumb down)? We need a process to collect that data on production and during development. And hopefully identify the error (wrong policy, wrong amount, times it answers "I don't know"). No embarrassing answers for me it means asking for confirmation instead of hallucinating.