# Held-out question set v1 (pre-registered)

24 questions, 8 categories, 3 each. The held-out set the benchmark measures against. None of
them reference any rule in `output-styles/*.md`, so the styled arm can't be scored for
following instructions it was handed.

The set deliberately spans expected verbosity: `analysis` / `research` questions invite long
answers (where the style should help most), while `writing` / `lookup` are already terse
(where the style should get out of the way). That lets the benchmark test the "gains scale
with verbosity" claim instead of assuming it.

| id | category | question |
|---|---|---|
| debug-01 | dev-debug | Python memory leak, finding held references |
| debug-02 | dev-debug | Postgres query suddenly slow |
| debug-03 | dev-debug | React prod build shows blank white page |
| decision-01 | dev-decision | REST vs GraphQL, small team |
| decision-02 | dev-decision | Message queue vs cron for background jobs |
| decision-03 | dev-decision | Monorepo vs separate repos |
| explain-01 | concept-explain | What is a database index, when it hurts |
| explain-02 | concept-explain | Race condition for a single-threaded dev |
| explain-03 | concept-explain | Eventual consistency, in user terms |
| research-01 | research | Switch from Jira to Linear? |
| research-02 | research | Annual billing at a discount, tradeoffs |
| research-03 | research | Contractor vs full-time for a 4-month project |
| analysis-01 | analysis | Onboarding funnel drops 60% |
| analysis-02 | analysis | Churn rose 3% to 5%, investigation plan |
| analysis-03 | analysis | Two features competing for one sprint |
| kwork-01 | knowledge-work | Back-to-back meetings, no real work |
| kwork-02 | knowledge-work | 400 unread emails, sane triage |
| kwork-03 | knowledge-work | Critical feedback without demoralizing |
| writing-01 | writing | Two-sentence Slack: deploy delayed |
| writing-02 | writing | Launch email subject + preview line |
| writing-03 | writing | One-paragraph out-of-office reply |
| lookup-01 | lookup | 'i.e.' vs 'e.g.' |
| lookup-02 | lookup | 'fewer' vs 'less' |
| lookup-03 | lookup | HTTP 502 meaning |
