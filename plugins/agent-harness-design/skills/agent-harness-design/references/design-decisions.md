# Design Decisions

Use this reference to choose the harness shape and place model/tool responsibilities.

## Harness layers

Keep the conceptual layers separate even when one library implements several:

```text
owner intent and authority
  -> instructions and relevant context
  -> model reasoning and action proposals
  -> tool/policy boundary
  -> environment effects and observations
  -> evidence, state, and recovery
```

A provider SDK, CLI, workflow engine, or MCP server is an implementation choice, not a
mandatory layer. Start from the host's real capabilities and add only what owns a
named responsibility.

## Agent or workflow

Use a coded workflow when the path is stable and the organization values predictable
transitions more than adaptive strategy. Use an agent-directed loop when the model
must decide what information to gather, which tool to use, or how to recover from an
unexpected observation. Hybrid systems are normal: code may own policy transitions
while the model owns work inside each state.

Do not infer that “semantic” means “never enforceable.” An authoritative and testable
business definition—eligible jurisdiction, supported file type, approved account,
required evidence fields—can be a hard rule. A vague quality judgment—helpful,
complete, persuasive—usually needs a model or accountable human and explicit
uncertainty.

## Complexity is a trade, not a ladder gate

A simple native loop is a useful default because it is easy to inspect and benefits
from host improvements. Move to another shape when any of these are already evident:

- a regulation or credible threat requires preventive enforcement;
- a long task must survive process or context loss;
- throughput or latency benefits from independent concurrency;
- specialized tools or context should be isolated by role;
- a stable business process requires auditable transitions;
- measured failures identify a missing control or feedback surface.

Past failure is strong evidence, but not the only admissible evidence. Record the
expected benefit and what would cause the added layer to be removed.

## Control admission and retirement

Before turning guidance into a hard control, answer:

1. Which protected property or authoritative obligation requires it?
2. Which trusted fact source can decide the outcome?
3. Can the same property be enforced closer to data ingress or the external effect?
4. Which authorized strategies, tools, context, latency, or reliability will it cost?
5. What happens after a false block or infrastructure failure?
6. Which evaluation result, model improvement, or platform capability would retire it?

A control with no protected property is ceremony. A useful compensating mechanism can
also become harmful when the model or host improves; keep its evidence and exit
condition reviewable instead of promoting it to permanent doctrine.

## Loop design

For a custom loop, make the protocol explicit:

```text
assemble relevant context
  -> call model
  -> validate proposed operation
  -> authorize and execute, or return a denial/approval request
  -> append a structured observation
  -> finish, recover, or continue within a real budget
```

Choose bounds from provider limits, cost, latency, task deadlines, or observed loop
behavior. An arbitrary small step cap can prevent legitimate recovery; an unbounded
loop can consume resources indefinitely. A budget should terminate predictably and
preserve useful state.

Every accepted tool call needs a corresponding observation. If execution is canceled,
times out, or is denied, return that fact in the host's expected protocol so the model
does not reason over a missing result.

## Tool granularity

Prefer tools that map to meaningful agent actions and return enough context to choose
the next step. Avoid both extremes:

- dozens of tiny API-shaped tools that force the model to reconstruct internal
  implementation details;
- an opaque “do everything” tool that hides authorization, errors, and outcomes.

Broader code or shell execution may be the most ergonomic tool for coding, data, or
research work when a disposable sandbox, resource bounds, network policy, and secret
isolation contain its effects. The trust boundary—not the tool name—determines safety.

Tool descriptions should explain purpose, important constraints, inputs, outputs,
failure modes, and relationships to adjacent tools. Use local schema validation for
machine constraints. Let actionable error results help the model repair a call.

## Provider and host choices

Keep domain policy and workflow intent provider-neutral where practical. Neutrality
means preserving the product contract, not forcing every model through identical
prompts, tool formats, or lowest-common-denominator features. Put native features
behind the narrowest useful seam:

- hosted tools and computer use;
- prompt caching and compaction;
- background or durable execution;
- native approvals, hooks, plugins, or tracing;
- structured output and tool-call protocols.

Do not emulate a strong native feature solely for portability. Document the semantic
contract and allow model- or host-specific adapters when their prompting, edit format,
tool protocol, compaction, or lifecycle is materially better. Keep the chosen model and
adapter visible; never gain apparent portability through a hidden downgrade. Verify
behavior on the exact model/host/version instead of assuming similarly named features
are equivalent.

## Recommendation record

For a material component, capture:

| Field | Question |
|---|---|
| Level | Invariant, default, conditional pattern, or example? |
| Consumer | What task or operator uses it? |
| Evidence | Incident, eval, threat, regulation, scale, or host constraint? |
| Boundary | Is this the narrowest authoritative place to enforce it? |
| Benefit | Which observable measure should improve? |
| Capability cost | Authorized success, tools, context, latency, coordination, false blocks? |
| Recovery | How does the agent or operator continue after denial or failure? |
| Exit | Which evidence or capability change removes or replaces it? |
