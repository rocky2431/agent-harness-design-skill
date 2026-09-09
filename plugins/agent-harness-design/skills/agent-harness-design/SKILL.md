---
name: agent-harness-design
description: "Design, audit, or evaluate an AI agent's execution layer: model/tool loops, authority and effects, context/state/recovery, orchestration, provider-native adapters, and model-harness safety, utility, or capability tax. Use only when the agent system is the subject; not for ordinary coding, writing, app state, task tracking, or delegation alone."
license: MIT
metadata:
  author: rocky2431
  version: "0.5.0"
---

# Agent Harness Design

Design the execution layer around an agent as a capability amplifier and trusted
execution frame. Preserve authorized evidence, tools, feedback and task-sized resources
while grounding authority, effects and success claims in the relevant environment.

## Keep activation scoped

Use this Skill when the agent system itself is the subject: new design, review,
diagnosis or model migration. Ordinary coding, writing, application state, task tracking
and delegation alone do not need a harness exercise. Cover only the harness-facing
part of a mixed request. A short component question deserves a short component answer.

## Choose the useful entry

| Request | Start here | Deliver |
|---|---|---|
| Design from scratch | [Architecture guide](references/architecture-guide.md): one model, one tool, then relevant components | Smallest sufficient shape, component contracts and a concrete verification path |
| Review an existing system | Trace its actual loop; read the affected component references below | Specific defects or trade-offs, evidence, narrow fix and recovery implications |
| Diagnose a failure | Actual request, tool result and stop events; [failure visibility](references/failure-visibility.md) | Distinguish instruction, context, protocol, resource, model and host causes before prescribing a fix |
| Adapt or migrate a model | [Model adaptation](references/model-adaptation.md), then only the matching profile | Valid target configuration, protocol differences, conditional optimizations and unverified checks |

Establish the outcome, evidence, environment, existing authority, task shape and material
resource constraints from available artifacts. Ask only for missing facts that change
the answer. The model using this Skill is not necessarily the target system's model.
Resolve the target model/version, provider endpoint, API/host, mode and task conditions
before giving specific settings; do not silently substitute a nearby family or alias.

## Keep scope and rule strength separate

General component responsibilities, provider/host interface contracts, behavioral
recommendations and historical examples answer different questions. Read
[model-adaptation.md](references/model-adaptation.md) when those are being conflated.

Independently distinguish:

- **Invariant**: a trust, authority or evidence property that must hold.
- **Default**: a starting point replaceable by task evidence.
- **Conditional pattern**: useful under named task, model, risk or host conditions.
- **Example**: an illustration, not a mandatory architecture.

General does not mean mandatory: short tasks may need no persistent store. Model-specific
can still be required: a provider may require a particular tool/history protocol.
Published pretraining, SFT and RL details can motivate adaptation hypotheses; they do not
prove the cause of a failure or the benefit of a scaffold. Mark undisclosed facts unknown.

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

Architectural choices are defaults or conditional patterns; provider interface contracts
remain binding within their documented configuration.

## Make the smallest sufficient design

Start with one model call for bounded work or a native tool loop for inspect/act/observe.
Use durable state for recovery, a coded workflow for stable transitions, and multiple
agents for useful decomposition, isolation or latency. None is a mandatory upgrade path.
A preventive control is justified without an incident when a credible threat, obligation
or task shape supports it. Name its consumer, protected property, capability tax, recovery
path and retirement condition.

Use **capability-preserving determinism**: make authority, effects, evidence and recovery
predictable while leaving room for interpretation, strategy and repair. Enforce at the
narrowest trusted boundary. Broad sandboxed tools and parallel isolated writes can be
appropriate; serialize real dependencies. A validated semantic evaluator can advise,
route or gate according to its errors, stakes and repair path.

Separate authority gates from resource governors and semantic prescriptions. Default to
a soft in-band tier before a hard resource ceiling when the runtime can provide warning;
retain immediate emergency stops. Measure token/time/cost needs rather than prescribing
arbitrary reasoning depth or answer length. Diagnose premature stopping from traces;
absence of completion does not by itself prove budget exhaustion.

## Read only the affected components

- [Architecture guide](references/architecture-guide.md): basic loop, twelve component
  contracts, design choices, normal paths, recovery and minimum checks.
- [Design decisions](references/design-decisions.md): shape, tools/ACI, budgets and
  control admission. [Harness vs software](references/harness-vs-software.md): why
  familiar software controls can cost agent capability.
- [Trust, tools and effects](references/trust-tools-and-effects.md): permissions,
  external content, secrets, execution environment and mutation boundaries.
- [State and orchestration](references/state-and-orchestration.md): instruction/context
  loading, retrieval, memory, compaction, pending work, ownership and parallelism.
- [Failure visibility](references/failure-visibility.md): errors, unknown effects,
  truncation, fallbacks, typed stops and evidence-based completion.
- [Model adaptation](references/model-adaptation.md): target selection and seven linked
  provider profiles. Read the matching profile, not every provider.
- [Evaluation and observability](references/evaluation-and-observability.md): real
  outcomes, protocol checks, behavioral comparisons, costs and false blocks.
- [Historical cases](references/historical-cases.md): why architectures changed and how
  to update/retire recommendations. [Research basis](references/research-basis.md): sources.

## Verify and deliver at the requested depth

For a direct question, give the decision, reason and relevant qualification. For a full
design, explain outcome/evidence, component responsibilities and interfaces, authority,
failure/recovery, alternatives and a verification plan. For an audit, lead with findings;
for diagnosis, distinguish verified causes from hypotheses. Avoid forcing a full template.

Separate documented protocol requirements, locally observed behavior, vendor-reported
benefits, inference and unknowns. For specific model/API claims, cite the primary source
and its checked date in the answer; a local profile read is not a user-visible citation.
State when target-system behavior remains untested. Verify changing interface facts
before adoption.
Compare the candidate with the current or simpler legal baseline at comparable resources;
never score an invalid protocol baseline as a behavioral improvement. Repeat stochastic
trials, inspect outcomes and costs, and report which model-harness configuration ran.
Skill-answer quality does not prove the target system's runtime behavior.

Each compensation encodes an assumption: Re-test on upgrade; do not remove on upgrade.
Drift is not monotone: the same change may help one model and hurt another.
Change the smallest implicated surface, test relevant regressions and retain useful
historical evidence. No hidden chain-of-thought is required for evaluation.
