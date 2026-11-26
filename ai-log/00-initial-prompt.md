I am doing an exercise for an interview. 

I want to deliver the answer on a pdf but also as a repo they can see. On the repo I want us to build the tests and the solutions, but also that you leave a trail on the conversations and the usage I've done of AI, and how I've worked with it. That will serve as an audit, and also as a summary on my ways of working. Also I want to use the commits as timestamps so we can track how long things take and that I did it on time the slot.

Let's structure the repo on different folders. One for the deliverables we need to prepare, but also files for the open questions that raise during the exercise (and the assumed answers we need to take to move forward), and an example of some of the features (like summarise) so we can prepare tests around it. Another one were we log the work with AI. Feel free to propose other structure if it'll add clarity.

For now the structure is: InitialPrompt.md has the prompt I started with, HowToTest.md is some ideas I have around how to test the Fraga app, OpenQuestions.md is where I am detailing questions (and we will write the assumptions if we need them to move forward), SummaryFeature.md will contain the definition of Summarize (I'm making up what it would entail). You also have advania-assessment-quality-engineering-excellence-lead.pdf as the exercise we are doing (don't commit this, add it to the ignore), fraga-log-sample.csv with questions from the users to evaluate, and fraga-policy-excetps.csv with example policies. Both CSV can be commited,

I don't have any specific skills and data premade for this. I am adding the PDF where they describe the problem, and the two data appendixes on ./ . For the tests we will use playwright if we are talking about end up end testing, and any API testing framework to mock the answers (like Pytest).

I already have some ideas on how I would address it. But I want you to start providing a set of questions and template that make sure that I think and add all the necessary details. I have a lot of experience preparing testing plans, and I want you to make sure I address everything important. 

The pillars I will follow: 
. Fråga v1 is already running, so we have example data to use for our tests, and we can extrapolate usage, load, etc. When possible, we will use test data as close as the one we have.
. For APIs, interfaces and rules are critical. We should make sure valid values are correctly handled and edge cases/wrong values are gracefully handled.
. Testing AI means checking for patterns on the non-deterministic answers. Focusing on the policies referenced, the amounts; but not on the specific wording. Ideally having some thresholds on length of the answer, language used, etc. 
. Priorities are to ship on time (keep momentum, fast turn around, improve through iteration), and not embarrassing answer (err on the side of caution, double check the answers, explicitly show doubt if certainty isn't high)
. Load, performance and fail over is critical when we have 15x the documents and many more users. We will have to extrapolate numbers and closely monitor technical aspects. 
. Incidents will happen, but we should always ensure we are regressing the issues that caused previous incidents so we don't make the same mistakes.
. Testing follows a pyramid: we get quick feedback on the areas surrounding what each commit touches, we run critical and quick areas often (with a risk/impact matrix, and taking into consideration effort and speed). We do a more complete testing approach on a lower cadence, and demanding efforts required before milestones. 
. 38 minutes is a long pipeline per-commit, but it is a healthy length for tests that round nightly. We will focus on creating different pipelines that trigger on different stages: quick test to validate changes locally (measured in seconds), integration tests before PR/merges (maximum 10-15 minutes), overnight tests covering all areas and bigger test data (maximum an hour) that report issues to be addressed, on-demand tests focusing on areas like performance/failover/compatibility/localisation on regular intervals to audit later.
. Tests have a flakiness, quality and greeness that define their cadence. If they fail often, their flakiness reduces; if it covers a critical area or regresses an incident, quality increases; if it always passes the greeness increases (and maybe we don't have to run it always). Ideally tests surround areas: if a changes touches a file, tests around that feature should be prioritised.
. We will write the questions that we need for the new cases. 15x of documents and people means there will be new use cases we need to understand and include. 
. Summarise hasn't been tested with real uses yet so it requires specific effort to validate. We will test it more exhaustingly and, if things go well, decide to turn some of the tests off when the risk lowers (or change the cadence)

At the moment they are empty, but I have made the following files. Feel free to add some questions or an skeleton on how to organize it, although I already have ideas on how to test it. 
.TestForIncidents.md: Here I will specify how could we test to regress for the known incidents
.TestForUpscaling.md: Here I will specify how to test for the challenges of upscaling we will find from V1 to V2
.TestForCurrentLog.md: Here I will detail some tests we could do to cover some of the thumbs up/down answers we can observe on the logs

Feel free to fix the wording and clarity on any of the documents I have already started, but please leave a log on what you changed so I can evaluate it. Try to keep answers short, concise and clear. 