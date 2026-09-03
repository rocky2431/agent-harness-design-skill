---
name: agent-harness-design
description: "Design, audit, or evaluate an AI agent's execution layer: model/tool loops, authority and effects, context/state/recovery, orchestration, provider-native adapters, and model-harness safety, utility, or capability tax. Use only when the agent system is the subject; not for ordinary coding, writing, app state, task tracking, or delegation alone."
license: MIT
metadata:
  author: rocky2431
  version: "0.4.0"
---

# Agent Harness Design

Treat the harness as a capability amplifier and trusted execution frame around a capable
but fallible model. Preserve the model's effective capability envelope—authorized
evidence, task-sized context and output budget, real tools, environmental feedback—while
grounding authority, secrets, resources, effects, and success claims in trusted
boundaries.

## Keep activation scoped

Use this Skill when the system around an agent is the design or review target. Do not
turn ordinary coding, prose, application state, task-progress bookkeeping, or delegation
into a harness exercise. If one appears inside a genuine harness request, cover only the
harness-facing decision and let the adjacent workflow or Skill own the rest.

## Calibrate every rule

Distinguish these levels; do not silently promote one into another:

- **Invariant**: a trust, authority, or evidence property that must hold.
- **Default**: a good starting point, replaceable when task evidence favors another.
- **Conditional pattern**: appropriate only when named task, risk, scale, or host
  properties apply.
- **Example**: illustrative implementation, never a universal architecture.

Use the labels where they clarify a disputed constraint, not on every sentence.

## Optimize for capability inside the frame

Design for capability and task utility first. This is not permission to run without a
security boundary: establish the trusted frame before inference, then constrain the
narrowest external effect rather than weakening reasoning upstream.

```text
authorized evidence and capabilities
  -> model-led interpretation, strategy, and repair
  -> narrow authority and effect enforcement
  -> typed evidence, denial, and recovery
```

Read [harness-vs-software.md](references/harness-vs-software.md) when ordinary software
intuitions are applied here, or when asked why a control that is free in normal code is
expensive in a harness.

Call this **capability-preserving determinism**: make authority, effects, state,
evidence, and recovery predictable without making model behavior easier for the platform
to predict. Starving context or output, silently changing models, deleting unrelated
tools, or rewriting model-authored semantics does not gain determinism.

## Start from the real task

Before recommending architecture, establish what changes the design:

1. Desired outcome and observable completion evidence.
2. Environment and state the agent may read or change.
3. Authority already granted, approval boundaries, and forbidden effects.
4. Consequence and reversibility of a wrong action or a missed action.
5. Task shape: predictable or open-ended; atomic, sequential, or decomposable.
6. Duration, context pressure, concurrency, throughput, latency, and cost constraints.
7. Current host capabilities and concrete failures or credible threat obligations.

Resolve cheap facts from the live system, traces, code, or primary docs before asking
the owner. Keep facts, inference, preferences, and unknowns distinct.

## Preserve this hard core

These are invariants unless a stronger enclosing policy supersedes them:

- The model, a worker, retrieved content, and tool output cannot create or enlarge
  authority. They may propose actions only inside authority supplied by a trusted
  owner or policy boundary.
- Untrusted data remains data. Repetition, storage, retrieval, or another model's
  endorsement does not turn it into trusted instructions.
- Credentials and privileged effects are exposed and executed through a trusted runtime
  boundary with least necessary scope; prompt wording is not an access control.
- Do not report an action or outcome as successful without evidence from the relevant
  environment. Match verification depth to impact and say when the outcome is unknown.
- Preserve a reachable stop, deny, error, and recovery path for non-terminal work.
  Do not convert a failed or ambiguous operation into silent success.
- Keep a denial local to the disallowed effect: it must not remove unrelated
  capabilities, end useful reasoning, or block analysis, drafting, or a narrower proposal.
- Do not silently downgrade the selected model, reasoning mode, authorized evidence
  coverage, output budget, or tool surface, and never trade capability for backward
  compatibility without a typed error naming the replacement. When a real boundary
  forces a reduction, make it visible in band, in the artifact, and in the trace, and
  preserve the useful work.

Read [failure-visibility.md](references/failure-visibility.md) whenever the design
touches error handling, fallbacks, truncation, compaction, or completion claims.

Everything else in this Skill is a default or conditional pattern.

## Choose the smallest sufficient shape

Default to capabilities already provided by the host, but do not require a past failure
before addressing a credible threat, regulation, scale, or task shape visible at design
time.

Choose among these shapes by fit:

| Shape | Use when | Main cost |
|---|---|---|
| One model call | The output is bounded and no iterative environment feedback is needed | Limited recovery |
| Native tool loop | The model must inspect, act, observe, and adapt | Variable turns and cost |
| Coded workflow | Steps and transitions are stable, auditable, or policy-defined | Less flexibility |
| Durable agent loop | Work spans sessions or needs recovery from process/context loss | State consistency |
| Multiple agents | Work is separable, specialized, independently verifiable, or latency-sensitive | Coordination and merge errors |

Delete a layer whose consumer or protected property cannot be named. Treat each added
control as a removable hypothesis with a named fact source, narrowest enforcement
boundary, capability and false-block cost, recovery path, and retirement trigger. A
preventive mechanism is still justified without an incident when its threat model,
obligation, and usability cost are concrete.

Read [design-decisions.md](references/design-decisions.md) for loop, workflow, tool,
budget, and portability choices.

## Place decisions on the right boundary

- Give the model freedom over interpretation, exploration, decomposition, strategy,
  and expression when multiple valid approaches exist.
- Enforce a protected property at the narrowest boundary that can actually protect it.
  Do not remove a broad reasoning or tool capability when an ingress check, scoped
  credential, sandbox, transaction, or pre-effect gate can contain the real risk.
- Use code for schemas, identities, scopes, quotas, concurrency control, protocol
  transitions, and authoritative business rules that can be represented exactly.
- Separate authority gates from resource governors and from semantic prescriptions. Cap
  only externally verifiable physical quantities, give every governor a soft in-band
  tier before its hard ceiling, and put no fixed number on how deeply to think, how long
  an answer should be, or how many turns a task deserves.
- A semantic evaluator may advise, block, or route. Its role depends on validated error
  rates, stakes, recovery paths, and who owns the acceptance criterion; it is not
  advisory merely because it uses a model.
- Broad tools can be appropriate inside a real disposable sandbox. Narrow tools are
  preferable when they improve discoverability, policy enforcement, or auditability.
- Separate draft from commit when review materially reduces risk or the effect is hard
  to reverse. Direct execution is reasonable for explicit, scoped, low-risk authority.

Read [trust-tools-and-effects.md](references/trust-tools-and-effects.md) whenever the
design touches permissions, external content, secrets, approvals, sandboxing, mutations,
or long-horizon authority.

## Design context, state, and orchestration conditionally

Keep active context relevant and make canonical state externally inspectable when it
must survive context loss. Persistence serves resumability, coordination, audit, and
recovery; it is overhead for bounded work. Effective context is smaller than the
advertised window and degrades with length, so curate rather than accumulate.

For long-running work, preserve liveness as well as safety: task-sized budgets or a
typed pause, recoverable artifacts and evidence, user corrections that do not discard
valid progress, and completion derived from the live environment rather than the agent's
confidence. A denied effect must leave safe next actions reachable.

Parallel reads and writes are both valid when operations are independent or protected by
ownership, isolation, transactions, or conflict detection. Sequentialize work with real
dependencies or shared mutable state.

Use multiple agents when decomposition creates a measurable advantage at a matched
budget, not as a badge of sophistication and not only after a single-agent failure. State
the dependency graph, ownership, merge rule, total budget, and evidence expected from
each worker.

Read [state-and-orchestration.md](references/state-and-orchestration.md) for memory,
compaction, recovery, concurrency, and topology choices.

## Evaluate the model-harness system

Define the evaluation before polishing the architecture:

1. Use realistic tasks and relevant failure/adversarial cases.
2. Compare against no-skill, previous-version, simpler, and control-ablation baselines.
3. Repeat stochastic trials; report reliability, not only the best run.
4. Score the final environment state and required evidence where possible.
5. Measure utility, safety, false blocks, recovery, latency, token/cost, operator
   burden, and **capability tax**: the authorized task success lost to the control.
6. Report results for the model-harness configuration; the same harness can help one
   model and hinder another.
7. Inspect traces to locate whether failure came from instructions, context, tools,
   policy, model behavior, execution, or the evaluator.
8. Change the smallest implicated surface and rerun held-out cases for regressions.
   Re-test compensating controls on every model upgrade: each encodes an assumption
   about what the model cannot do alone, drift is not monotone, and one control can help
   one model and hurt another. Re-test on upgrade; do not remove on upgrade.

Read [evaluation-and-observability.md](references/evaluation-and-observability.md) for
eval design, evidence, graders, tracing, and launch decisions. Read
[research-basis.md](references/research-basis.md) when current source support matters.

## Deliver the smallest useful decision

Match the requested depth and format. For a direct or concise answer, give only the
recommendation, reason, and minimum controls. For a full design or audit, lead with the
recommended shape and adapt only the relevant parts of this outline:

```markdown
# Harness decision

## Outcome and evidence
## Authority and trust boundaries
## Recommended shape
## Context, tools, and state
## Failure and recovery behavior
## Evaluation plan
## Alternatives and triggers to revisit
```

Name assumptions and uncertainty. Separate current evidence from extrapolation. Do not
turn this Skill's defaults into a policy engine or use “best practice” in place of a
task-specific reason.
