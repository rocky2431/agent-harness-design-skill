# Evaluation and Observability

Use this reference to design behavioral evals, evidence checks, graders, tracing, and
launch decisions for the complete model-harness system.

## Start from a decision

An eval should decide whether a proposed change is better for a defined task
distribution. Specify:

- realistic inputs and environment state;
- observable task outcome;
- policies and forbidden outcomes;
- baseline and candidate configurations;
- repetition count and uncertainty;
- acceptable utility, safety, cost, latency, and operator burden.

Avoid optimizing a metric with no decision attached.

## Evaluation arms

For a Skill or harness change, compare at least the candidate against the current
baseline. A no-skill or simpler native-loop arm helps show whether the added layer
contributes anything. Keep model, tools, task state, and budgets matched where the
architecture permits.

Run multiple trials because agent behavior is stochastic. Report per-task outcomes,
mean performance, variance or confidence, and reliability across repeated attempts.
Metrics such as `pass^k` can reveal inconsistency hidden by one successful sample.

## Capability tax and control ablation

Measure the whole model-harness configuration. A control's capability tax includes the
authorized task success it removes, false denials, extra clarification or approval,
lost context or tool access, latency, and recovery burden. Efficiency metrics alone do
not show whether the agent remained useful.

Where safe to test, compare matched arms with the proposed control enabled, disabled,
and enforced at a narrower boundary. Include ordinary authorized tasks as well as
adversarial cases; a defense that blocks attacks by making benign work impossible is
not a successful harness. Report per model and adapter because a compensating rule can
help one configuration and become dead weight on a more capable one.

Give model- or host-compensating controls a retirement trigger. Re-run held-out cases
after material upgrades, and delete the control when it no longer improves the
protected outcome enough to justify its capability tax.

## Evidence hierarchy

Prefer evidence closest to the requested outcome:

1. final environment or database state;
2. deterministic artifact or protocol validation;
3. tool receipts and execution traces;
4. independent semantic review;
5. the acting model's self-report.

This is a preference, not a rule that every task needs all five. For writing or design,
human/model review may be the relevant outcome. For payments, deployments, or data
mutations, inspect the authoritative external state.

## Graders and gates

Use deterministic checks for exact properties. Use model graders for semantic criteria
when their rubric, reference context, and error behavior are tested against human or
environmental ground truth.

A semantic grader may be:

- advisory when false blocks are costly or the rubric is exploratory;
- a routing signal for additional review;
- a blocking gate when the accountable owner accepts the criterion, measured error is
  within tolerance, distribution shift is monitored, and a repair/appeal path exists.

Do not declare all semantic graders authoritative or all of them advisory. Evaluate the
specific grader in the role it will play. Prevent an evaluator from rewriting its own
evidence or creating an irreparable loop.

## Audit the grader before trusting the score

A benchmark result is a claim about the grading function as much as about the agent.
Reviews of widely used agent benchmarks have found insufficient test cases, empty
responses scored as successes, and reward-design defects large enough to shift reported
performance by up to its own magnitude. Patches that pass a suite have been found to fail
developer tests and to differ behaviorally from the reference at meaningful rates.

Check three things before acting on any eval number:

- **Grading validity.** What exactly does a pass require, and can it be satisfied without
  the outcome you care about?
- **Artifact isolation.** Can the agent reach solutions, reference outputs, or eval
  infrastructure? Audits of agent traces have found reward hacking and answer exposure in
  a majority of trajectories on some suites, and capability estimates have been halved by
  removing hacked successes.
- **Judge independence.** Do not use the same model family as agent and grader.
  Self-preference is causally linked to self-recognition, and verdicts can flip on
  candidate ordering alone.

Report uncertainty. A benchmark difference without a standard error is not actionable,
and small leaderboard gaps can be produced by execution environment alone: resourcing
differences have moved agent scores by several points, often because runs fail before the
agent writes anything. Match and document the configuration, or treat small differences
as noise.

Remember that a mitigation that reduces a detected behavior and a mitigation that teaches
the model to hide it look identical from outside. Prefer controls that change what is
possible over controls that change what is observed.

## Launch signals beyond the eval suite

An eval suite is necessary and not sufficient. Regressions have shipped with offline
evals looking healthy, because no deployment-time measurement existed for the behavior
that changed and qualitative reports of "something feels off" were overruled by aggregate
metrics. Commit in advance to blocking on qualitative and proxy signals, and to how fast
you can roll back.

Harness quality has no unit test. Where volume permits, compare variants online and score
outcomes the user actually produces — whether the work survived, whether the next message
was a continuation or a stack trace — rather than only offline pass rates.

## Failure taxonomy

Trace enough to distinguish:

- wrong or ambiguous owner intent;
- missing, stale, or excessive context;
- poor tool discoverability or schema;
- incorrect authority/policy decision;
- model planning or reasoning error;
- tool/runtime failure or ambiguous effect;
- integration and concurrency conflict;
- evaluator false positive or false negative;
- recovery or compaction loss.

Fix the smallest shared cause. Do not add a validator to compensate for a tool that
returns misleading data, or rewrite a prompt to compensate for an unenforced secret
boundary.

## Trace without hidden reasoning

Useful operational events include request/run ID, configuration and model versions,
tool proposals, policy decisions, approvals, execution status, bounded observations,
state transitions, retries, costs, latency, and verification results. Redact secrets
and sensitive user data; use retention and access controls appropriate to the domain.

Do not require private chain-of-thought. Action summaries, tool records, explicit
assumptions, citations, and environment evidence are more stable debugging surfaces.

## Regression and launch

Keep held-out cases so iteration does not merely memorize the initial failures. Include
activation negatives, ordinary cases, boundary cases, adversarial inputs, and recovery
paths. Test the package and the live host lifecycle separately: a valid manifest does
not prove discovery, invocation, execution, or cleanup.

Promote a change when it improves the accepted task distribution without violating
hard invariants or exceeding agreed trade-offs. Record known exclusions and the signal
that would trigger another architecture review.
