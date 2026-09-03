# State and Orchestration

Use this reference for context assembly, memory, compaction, recovery, concurrency,
and multi-agent topology.

## Context is working material

Assemble the smallest context that preserves task correctness, not the smallest token
count in isolation. Typical ordering is stable instructions and tool definitions first,
then scoped project/domain knowledge, current task state, recent observations, and the
immediate request. Provider caching can favor stable prefixes, but relevance outranks a
cache optimization that floods the model with stale material.

Progressively disclose Skills, references, and tool schemas. Make names and
descriptions specific enough for discovery, then load the full material only when the
task needs it.

## Context degrades with length

Effective context is a fraction of advertised context, and the loss is not uniform.
Across model families, accuracy on realistic retrieval and reasoning declines well before
the stated limit, degrades faster when the target shares little vocabulary with the
query, and drops further with each distractor present. Measured effective lengths have
been reported at a small fraction of advertised windows, and rankings between models
reorder substantially as length grows. Recent frontier models still miss relevant events
several times more often late in very long transcripts, partially recoverable with
periodic restatement.

Two consequences:

- Treat attention as a budget. Aim for the smallest set of high-signal tokens that
  supports the task, not the largest set that fits.
- Measure effective context on your own task shape. Do not derive budgets from the
  advertised window, and do not assume a longer window removes the need for retrieval.

Retrieval usually beats stuffing. Reported reductions from retrieving tools and results
on demand rather than preloading them run to an order of magnitude in tokens with equal
or better accuracy, and tool-selection accuracy improves substantially when the tool
space is retrieved rather than fully enumerated. The size of the tool surface is a
harness variable, not a free parameter.

A dissenting result is worth keeping in view: agentic scaffolds that re-retrieve rather
than rely on recall have shown strong robustness across very long horizons. That is
consistent with the rule above rather than against it.

## Truncation is a correctness decision

Truncation and cache strategy are usually discussed as cost optimizations. They change
behavior.

- Opening tokens absorb disproportionate attention regardless of content. Evicting them
  degrades the model badly. A naive oldest-first policy hits this directly.
- Cached attention state is reusable only at the same position. Inserting or reordering
  content inside a stable prefix forfeits the cache and changes cost sharply. Keep the
  system prompt and tool definitions in a fixed prefix and put per-turn variability after
  it.
- Do not add or remove tool definitions mid-run. Prior actions still reference them, and
  the mismatch produces schema violations and invented calls. Restrict availability
  without changing the definitions when possible.
- Never sever a tool call from its result. Snap any cut to a turn boundary.

The settled practice for oversized output is to truncate, persist, and point: store the
full artifact, return a bounded preview, and hand back a retrievable reference and the
position where the cut began. Independent implementations have converged on this.
Compression should be designed to be restorable — dropping page content is safe while
the URL survives.

## Durable state and memory

Persist state when it has a consumer after the current context ends:

- resumable work or process restart;
- coordination across sessions or actors;
- audit and evidence retention;
- user preferences or domain facts with an explicit scope and lifecycle;
- recovery from compaction or partial execution.

Keep bounded tasks in context when persistence adds no benefit. A state store is not a
completion oracle or an authorization source merely because it is durable.

Distinguish:

- working state: objective, accepted decisions, current artifacts, blockers, next step;
- event evidence: observed operations and results;
- long-term memory: scoped facts or experience reused later;
- derived indexes and summaries: disposable projections of canonical sources.

Store exact values that must survive. Summaries should preserve uncertainty and point
to canonical artifacts rather than silently rewriting facts.

## Compaction and recovery

Compact when context pressure or cost justifies it. Preserve the objective, authority
and approvals, accepted decisions, changed artifacts, verified evidence, active
failures, and one next action. Reconcile recovered state with the live environment;
written intent may be stale and never authorizes automatic continuation.

Prefer host-native lifecycle support when it reliably reaches the next model request.
A custom recovery adapter is justified when a real lifecycle gap exists and the
adapter can remain bounded, inspectable, and non-blocking.

## Long-horizon liveness

A long task must remain able to make honest progress across context, process, and
provider boundaries:

- use a task-sized budget or pause with a typed reason before work becomes unreliable;
- preserve full artifacts or truthful recovery references before trimming inline data;
- keep the objective, authority, decisions, failures, and next action recoverable;
- apply user steering to the active state without discarding unrelated valid work;
- treat a denied effect as one state transition, not global task failure;
- update durable progress from environment evidence, not an actor's self-report.

Never hide model, context, tool, or budget reduction behind a normal completion state.
If the preferred path is temporarily unavailable, preserve evidence and expose the
safe actions that remain.

## Long-horizon pathologies

Name these; they are distinct and have different fixes.

- **Self-conditioning.** Per-step accuracy falls as a run lengthens, and the model's own
  visible errors raise its subsequent error rate further. Scale does not remove this,
  though reasoning modes reduce it in some models.
- **Multi-turn reliability collapse.** Moving the same work from one turn to many costs
  far more in reliability than in ability. Models commit early to a wrong reading and
  rarely recover on their own. Restating a consolidated specification can beat continuing
  the thread.
- **Context anxiety.** As the window fills, a model may hedge, scope down, or refuse work
  it could still do. Observed independently by several teams, and present on some models
  and absent on others, so it is a per-model check rather than a permanent fixture.
- **Looping without strategy change.** Repeating a failing approach with cosmetic
  variation. The productive response is a stall counter that forces re-planning, or an
  in-band message naming the repeated call, its arguments, and the identical error.
- **Declaring done without verification.** The most common single long-run failure across
  independent analyses: the model reviews its own output, judges it fine, and stops.
  Close completion on the environment, not on self-assessment.
- **Summary drift.** Errors in summaries compound when summaries are built on summaries.
  Anchor to canonical artifacts and merge newly trimmed spans into a stable structured
  summary rather than regenerating it from scratch each cycle.
- **Sycophancy accumulation.** Positions erode across turns under pushback. Anchor
  decisions in durable state rather than in conversation.

Note that context exhaustion does not explain all of this. Long runs have derailed into
unrecoverable loops without approaching the window limit, so a larger window is not a
fix for coherence.

Self-correction without an external signal is unreliable and can reduce accuracy.
Open-ended drafting can be self-reviewed; correctness must close on a ground-truth
signal such as tests, tool errors, or environment state.

What compaction loses first, empirically, is the record of which artifacts were changed.
Preserve that explicitly rather than trusting a general summary to retain it.

## Multi-agent decision

Multiple agents are a conditional architecture. They can be the first implementation
when the task already has natural parallelism, role-specific tools or context,
independent verification, or latency requirements. They can also be the wrong choice
after a single-agent failure if the work is tightly sequential or merge-heavy.

Evaluate these properties:

| Property | Favors multiple agents | Favors one agent |
|---|---|---|
| Dependencies | Wide, independent branches | Long sequential chain |
| Context | Distinct domains or large isolated corpora | Shared evolving context |
| Tools | Role-specific access | Same tool surface |
| Verification | Independent perspectives add signal | One deterministic check suffices |
| Latency | Parallel wall-time matters | Coordination dominates |
| Integration | Clear merge contract | Highly coupled edits or decisions |

Do not use a fixed “planner, researcher, builder, reviewer” team for every task. Choose
only roles with distinct work, context, tools, or acceptance responsibilities.

Isolation is also a context tool, not only a parallelism tool. A subagent can explore
widely and return a small distilled result, keeping exploration cost out of the parent's
window. The same property makes an independent reviewer valuable: a reviewer with no
prior context cannot inherit the author's assumptions and must rediscover the intent.

Two questions in this area are genuinely disputed. Do not cite one side as settled.

- **Should failed attempts stay in context?** Keeping them preserves evidence the model
  needs to adapt; removing them avoids compounding degradation. Current best reading:
  keep failures visible for near-term steering, clear them across a compaction boundary,
  and re-test per model, since some models no longer self-condition.
- **Does subagent isolation help or hurt?** Reported results point both ways within days
  of each other. The discriminator is task shape: isolation tends to win for
  parallelizable, read-mostly investigation and to lose for shared-state construction
  where implicit decisions must stay consistent. Keep writes single-threaded even when
  several agents contribute analysis.

When quoting a multi-agent improvement, quote its cost and variance decomposition with
it. A large reported gain accompanied by an order-of-magnitude token increase, and an
analysis attributing most variance to token spend, is a compute result as much as an
architecture result.

## Work packets and ownership

For each delegated unit, state:

- outcome and acceptance evidence;
- relevant context and dependencies;
- authority inherited from the parent and effects still gated;
- artifact or resource ownership;
- budget and stop condition;
- return format and integration owner.

The parent remains responsible for integration and for claims made to the owner. A
worker result is evidence to inspect, not automatic truth. Verification can be
deterministic, model-based, human, or environmental depending on the acceptance
criterion.

## Topology choices

- **Independent parallel**: several self-contained analyses or artifacts, merged once.
- **Central coordinator**: one agent routes packets and integrates results; useful when
  global consistency matters.
- **Pipeline**: each role consumes the prior result; useful for stable stage boundaries
  but sensitive to upstream errors.
- **Debate or ensemble**: several candidates are compared; useful only when diversity
  and a credible selection method outweigh cost.
- **Verifier loop**: execution followed by focused checking and repair; stop on evidence
  or budget, not on endless disagreement.

Use the least communication needed. Share compact artifacts or summaries instead of
full transcripts. Budget total model calls and integration work, not each worker in
isolation.

## Concurrency and recovery

Record task identity, ownership, and observable state when work can be retried or
resumed. Use leases, transactions, idempotency, or conflict detection only where the
environment needs them. Surface an ambiguous outcome as `unknown` and inspect before
resubmitting a potentially duplicated effect.

Every non-terminal orchestration state should have a reachable next action: continue,
revise, retry safely, reassign, cancel, or abandon. This is a liveness requirement, not
a claim that workflow position proves semantic completeness.
