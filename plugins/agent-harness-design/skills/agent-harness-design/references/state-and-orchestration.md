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
