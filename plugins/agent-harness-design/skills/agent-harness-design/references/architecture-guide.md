# Architecture Guide

Use this map to design an agent from the basic feedback loop or locate one component.
Read the relevant section and its linked reference; these are design choices, not a
mandatory twelve-step process. Coding, research, and business-service agents share
responsibilities, not necessarily filesystems, shells, planners, or vector databases.

## Start with one model and one tool

Example: answer a question from an approved document collection using `search_docs`.
The user supplies the question and read scope. The runtime supplies the model with
the applicable instructions, tool description, and current conversation.

```text
question + authority + relevant context
  -> model proposes search_docs(query), with a call identity
  -> runtime validates arguments and read scope, then executes the search
  -> environment returns passages with source identifiers, or a typed failure
  -> adapter returns the observation linked to the original call
  -> model answers with supported citations, or searches again
  -> check the requested answer and evidence, then deliver or report what is missing
```

The model proposes; the runtime authorizes and executes; the environment supplies
facts. A model turn ending, a tool finishing, and the user's task being complete are
different events. An empty search is a valid observation, not proof that no answer
exists. A timeout is not an empty search. No private reasoning transcript is required.

For this bounded task, conversation state and a source-aware search tool may suffice.
Add persistence only if a later session needs to resume; add a workflow for stable
business transitions; add agents when independent work justifies integration cost.

This synchronous walkthrough explains causality, not required scheduling. Streaming
arguments must be assembled and validated before execution. Several independent calls
may run concurrently; async tools may remain pending while the model does useful work.
Associate each result with its original call and retain pending work across interruption.
Use the target adapter's protocol, including provider-native async and steering support.

## Component map

| Component | Responsibility and input → output | Choice and adoption condition | Failure and smallest useful check |
|---|---|---|---|
| Goal and outcome contract | Request, corrections, authority → current goal, permitted effects, acceptance evidence | A short explicit goal for bounded work; durable decisions when work outlives a context | Tool completion mistaken for task completion; compare delivered answer/artifact with the request |
| Agent loop | Context and pending events → model proposal, observed result, next action or stop | One call without feedback; native loop for adaptive work; coded transitions for fixed policy | Lost or duplicate result; trace one call identity through execution and continuation |
| Model adapter | Product intent and conversation → valid provider request, response events and typed errors | Native API/SDK when it preserves needed features; custom adapter only for a concrete gap | HTTP success while effort or state is discarded; inspect a complete two-call protocol round trip |
| Tools / ACI | Model action and trusted scope → environment result with usable feedback | Domain actions for discoverability; shell/code for flexible work in a real sandbox | Valid schema but unusable interaction; complete one representative task using the actual interface |
| Instructions and Skills | Trusted policy, project context, task → scoped instructions at the right priority | Brief stable core plus on-demand detail; specialized Skills only when their purpose applies | Conflicting rules or unrelated activation; run one intended request and a nearby negative |
| Context and retrieval | Sources, current state, recent observations → sufficient working context | Inline small evidence; retrieve large/selective material; cache stable prefixes when compatible | Missing decisive fact; test short and long contexts with evidence in different positions |
| Memory and durable state | Progress and observations → scoped working state, event evidence, reusable knowledge | Persist for recovery, coordination or a later consumer; do not build a store for a single answer | Stale authority or competing status copies; resume and reconcile with live artifacts |
| Execution environment and permissions | Validated proposal, scoped identity → contained effect or explicit denial | Use host files/processes/browser/network only as needed; isolate tenants and privileged credentials | Broad access or false block; try an authorized operation and an out-of-scope counterexample |
| Planning and orchestration | Goal, dependencies and resource ownership → work units, schedule and integrated result | Model-led plan for open work; workflow for stable transitions; agents for useful separation | Merge conflict or lost requirement; compare integrated outcome with a simpler matched baseline |
| Reliability and recovery | Errors, pending operations, checkpoints → retry, reconcile, resume or truthful pause | Idempotency and operation records for effects that may be repeated; native resume where reliable | Timeout retried after effect landed; query original identity before submitting again |
| Budget and interaction | Limits, consumption, user steering → pace, checkpoint, correction or typed stop | Measured cost/time limits; early warning when possible; preserve hard emergency stops | Premature stop or runaway loop; inspect actual consumption, termination events and correction handling |
| Evaluation and observability | Configuration, events, artifacts → outcome judgment with limits | Protocol checks for exact requirements; realistic tasks and repeated comparisons for behavior | Fluent self-report scored as success; inspect the relevant environment/artifact and false blocks |

## Goal, loop, and adapter

Keep the product contract independent of transport: the same read-only question must
remain read-only after a model migration. Represent completion, needed user input,
denial, execution error, resource exhaustion and unknown effect distinctly. The names
may follow the host; a custom state machine is not required.

At the adapter boundary preserve tool identities, partial-stream assembly, protocol
state, stop reasons and effective settings. Do not flatten reasoning blocks, signatures,
tool events and visible text into one string. Choose the **target system's** profile in
[model-adaptation.md](model-adaptation.md), not the model answering this design question.

See [design-decisions.md](design-decisions.md) for shape, ACI and budget choices, and
[failure-visibility.md](failure-visibility.md) for truthful observations and stopping.

## Tools and instruction loading

A useful tool exposes an action the model can select and repair: purpose, arguments,
scope, output, failure and next available action. A document search should return source
identity and enough passage context to cite; a ticket update should return the actual
updated ticket or a retrievable receipt. Schema validity alone proves neither.

Keep tool definitions already referenced by history stable. Native tool search and
deferred loading can expand discoverability without rewriting that history. Check the
adapter's supported mechanism before deciding whether to preload or discover tools.

Separate stable system constraints, scoped project guidance, user intent and untrusted
retrieved content. Skill descriptions enable selection; detailed bodies and references
load only when needed. Test both discovery and whether the loaded guidance improves
the task. See [trust-tools-and-effects.md](trust-tools-and-effects.md).

## Context, memory, and a recoverable long task

Extend the document agent to a two-day review with many sources. Preserve the goal,
accepted corrections, source IDs, judgments and uncertainty, changed artifacts, pending
search IDs, verified results and next action. One owner maintains the current work
record; raw evidence and disposable indexes can be separate. Choose a file or existing
database for its consumer, not because agents must have one.

Recovery has three different shapes:

1. Continue a valid native conversation with its supported state and pending calls.
2. Use the provider's compaction result according to its protocol.
3. Start a fresh conversation from a consolidated, evidence-linked handoff, without
   replaying reasoning state bound to a different history.

They are not interchangeable. A text summary does not recreate encrypted state or
prove an interrupted write failed. Reconcile pending operations and changed artifacts
with the environment, then resume the original objective within current authority.
Keep obsolete directions as history, not active instructions. See
[state-and-orchestration.md](state-and-orchestration.md).

## Environment, scheduling, and user interaction

A research agent may need network search and a document store; a support agent may need
scoped business APIs; a coding agent may need a filesystem, terminal and browser. Make
the relevant environment legible and enforce permissions where effects occur.

Parallelize independent work with explicit ownership and an integration consumer.
Serialize actual dependencies. A planner/evaluator split is conditional; testing a
finished result against the environment remains useful even without a separate agent.
For slow tools, keep operation identity and cancellation semantics rather than blocking
all useful work. Apply user corrections to active work without losing valid progress.

Inspect premature stopping before adding a controller: actual limits, conflicting
instructions, approval interpretation, missing results, model stop reasons, transport
errors and host cancellation distinguish different causes. See
[design-decisions.md](design-decisions.md) and
[evaluation-and-observability.md](evaluation-and-observability.md).

## Why these parts exist

[ReAct](https://react-lm.github.io/) (2022) illustrates action/observation feedback;
[SWE-agent ACI](https://swe-agent.com/0.7/background/) (2024, historical interface)
shows why tools are part of the agent design. Anthropic's
[composable patterns](https://www.anthropic.com/engineering/building-effective-agents)
(2024-12) distinguish workflows and agents;
[context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
(2025-09-29) connects tools, retrieval and working context. These are dated primary
examples, checked 2026-09-09, not proof that every agent needs every part. Continue to
[historical-cases.md](historical-cases.md) for conditions under which parts changed.
