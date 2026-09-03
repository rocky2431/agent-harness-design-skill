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

## Gates, governors, and prescriptions

"Control" is not one thing. Three kinds are routinely conflated, and they have opposite
admission logic and opposite failure modes.

| Kind | Protects | Shape | Failure mode when wrong |
|---|---|---|---|
| Authority gate | An authorization or trust property | Binary, enforced at the effect | Breach if absent; a blocked primary path if too broad |
| Resource governor | Cost, latency, and termination | Quantitative, on a physical quantity | Capability starvation and invalid measurement |
| Semantic prescription | Nothing enforceable | A number applied to a judgment | Silent quality loss with no error anywhere |

The admission questions above are written for authority gates. Governors need their own
discipline, and prescriptions usually need deleting.

**Hard-cap only externally verifiable physical quantities**: tokens, wall-clock, bytes,
money, concurrency, process count. How deeply to think, how long an answer should be,
how many turns a task needs, and how many words belong between tool calls are judgments
the model makes from the task. A uniform number applied to them is a prescription, and
it costs measurable task success. Reported effects include a small percentage drop from
a prompt-level word cap, and a substantial drop from raising reasoning effort uniformly
rather than per task.

**Give every governor two tiers.** A soft, in-band signal the model can pace against,
and a hard ceiling that prevents runaway consumption. Independent implementations have
converged on this: a soft countdown visible only to the model alongside an enforced
output ceiling, and a token budget with reminder thresholds alongside an abort limit. A
hard ceiling with no warning tier turns a budget into an amputation, because the model
cannot checkpoint, summarize, or hand off before it lands.

**Do not mirror the soft signal client-side.** If the harness recomputes and re-sends a
budget the model is already tracking, a mismatch makes the model wrap up early. Set a
generous budget and let the model self-regulate against it.

**Size governors from measurement**, not intuition: run the task distribution without a
budget and take a high percentile of observed spend. Re-derive after model changes.

**Count the quantity whose failure you fear.** A step cap does not catch a broken tool
burning every step. That needs a consecutive-failure or stall counter, which is a
different governor. Guidance to escalate on failure thresholds is common; implementing
it is not, because turn counters get mistaken for failure counters.

**Make exhaustion a typed terminal state** distinct from interruption, replacement, and
execution error, delivered in band so the model can close out honestly, and readable
before any result field is read.

**Suspect the budget first.** Unexpected refusals, aggressive scope reduction, and
premature stops are the documented symptoms of a budget too small for the task. Raise it
before debugging anything else. Note also that the governor's *visible* value changes
behavior: a model that believes it is near its limit behaves differently from one that
believes it has room, even at identical real capacity.

Where the harness must stop, stopping loudly beats degrading quietly. Failing a request
that cannot fit is a better default than silently dropping the oldest context, and
refusing to compact in a loop is better than compacting forever.

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

## Model portability and boundary probing

Keep domain policy and workflow intent provider-neutral where practical. Neutrality
means preserving the product contract, not forcing every model through identical
prompts, tool formats, or lowest-common-denominator features.

| Hold identical across models | Free to differ per model or host |
|---|---|
| Authority and approval boundaries | Prompt wording and structure |
| Which effects are gated and how they are enforced | Edit format and tool-call protocol |
| Evidence required before a success claim | Reasoning, verbosity, and effort settings |
| Typed result and failure semantics | Compaction and context-management strategy |
| The product contract owed to the user | Hosted tools, caching, and lifecycle features |

The same harness change can help one model and hurt another. In a controlled comparison
of one scaffold change across three models, two gained roughly 6 and 11 points while a
third lost about 5. Edit format alone moved one fixed model from 20% to 61%, and the
best format is not globally rankable — for other models the ordering reverses. A model
performs better with the interface it was trained on; an unfamiliar one costs reasoning
tokens and produces more errors. Do not emulate a strong native feature solely for
portability, and never gain apparent portability through a hidden downgrade.

Scaffolding matters most for weaker models. Stronger backends tend to score higher and
show lower variance across harnesses, which means compensating machinery has a shrinking
benefit and a growing cost as models improve.

**Migration protocol.** Change one thing at a time:

1. Switch the model without touching the prompt.
2. Pin reasoning or effort settings explicitly; provider defaults differ by model and
   are not portable. The same applies to any per-model default in context management.
3. Run evals for a baseline. Compare on cost per successful task, not accuracy alone.
4. Only then adjust the prompt, if there is a regression to fix.
5. Re-run after each change.

**Boundary probing on upgrade.** Every harness component encodes an assumption about
what the model cannot do alone. Those assumptions may have been wrong, and they go stale
as models improve. On a material upgrade, remove one compensating component at a time
and measure. Reported retirements include context resets for premature stopping,
separate evaluator passes, decomposition scaffolds, and forced status-update prompting.

Two cautions keep this honest. Removal is a measurement, not a free win: the same task
run without a harness can be an order of magnitude cheaper and still produce broken
output. And drift is not monotone — successive models have moved in opposite directions
on delegation frequency and on how literally they read instructions. The rule is re-test
on upgrade, not remove on upgrade.

**Name the regime.** A harness tuned against premature stopping is actively wrong for a
model that persists past its sandbox instead of returning. Earlier practice removed stop
affordances to keep agents working; later models required trajectory-level pause instead.
State which regime the target model is in, and re-check it every upgrade.

Avoid switching model families mid-run. Beyond prompt sensitivity, a family switch can
discard cached or encrypted reasoning state the next call would have reused. Verify
behavior on the exact model, host, and version rather than assuming that similarly named
features are equivalent.

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
