# Failure Visibility

Use this reference whenever the design touches error handling, fallbacks, truncation,
compaction, capability probing, version compatibility, or completion claims.

A silent failure is any state whose observable output is indistinguishable from success
while the intended effect did not occur, or occurred at reduced capability. A silent
degradation is the same thing spread over time: the system still returns answers, and
only their quality moves.

## Why this is the dominant failure class here

Ordinary software fails loudly because runtimes and type systems stop it. A model
produces fluent, confident output whether or not the effect landed, so nothing stops it.

Measurements on tool-agent benchmarks with text-independent ground truth put false
success at roughly 45-48% of all failures in single-control settings, and about 3% in a
comparable setting where an independent simulator can verify state. The single most
effective control against this class is an independent check of the environment, not a
better prompt and not a stronger reviewer model: model graders asked to detect false
success perform near chance, because they key on confident closing language and action
volume rather than verified state.

Treat "the agent said it was done" as the weakest evidence in the system.

## Mechanism taxonomy

Each of these produces output shaped like success. Look for them by mechanism, not by
whether the code looks careless — most instances are deliberate and well-intentioned.

| Mechanism | What it looks like |
|---|---|
| Success-shaped fallback | A failed operation returns a generic string the model reads as an ordinary result |
| Broad catch and continue | One `except`/`catch` around a block with several distinct failure meanings |
| Default substitution | A missing or invalid semantic field silently becomes a default |
| Unmarked truncation | Output, context, or history is cut with nothing in-band saying so |
| Paired-item severing | A tail slice or window drops a tool call away from its result |
| Capability probe to a lesser path | An unsupported feature routes to a weaker mechanism without announcement |
| Compatibility shim | An old option is still accepted but no longer does what its name says |
| Best-effort partial result | A timed-out or cancelled operation returns what it has, typed as success |
| Transport success as business success | A 200, a zero exit code, or a completion event is read as the outcome |
| Model or tool fallback chain | A cheaper model, older protocol, or narrower tool is substituted on error |
| Reasoning or budget downgrade | Effort, thinking, or output budget is lowered for latency or cost |
| Omission | A tool, permission, or context source is simply absent, with no error and no prompt |
| Concealment instruction | The model is told a state change occurred and told not to mention it |
| Inert governor | A limiter exists, is tested, and is constructed or configured so it never fires |

Two field observations worth internalizing. A guard that ships disabled by default is
indistinguishable from no guard, and reads as protection in review. A threshold set at
its maximum can mean the feature never runs, so users get the crude fallback path while
believing they have the sophisticated one.

## Backward compatibility

This is the most dangerous category because the justification is legitimate.

**Compatibility may preserve an interface. It must not preserve a capability claim.**

When a new path cannot do what the old one did, the correct move is a typed hard error
naming the replacement, at the earliest boundary that can detect it — configuration
parse time is better than request time, which is better than mid-run. Removing a
transport, a protocol, or a feature outright and refusing the old value with a migration
message is a better outcome than accepting the old value and quietly losing the
capability behind it.

An inert legacy field is acceptable when it is documented as removed and provably does
nothing. The defect is never that a field was kept; it is that the field still appears
to work.

Apply the same rule to serialized state and resumption: a checkpoint outside the
supported window should refuse to resume rather than resume degraded.

## What "loud" means

Degradation must be visible on three surfaces. Any one alone is insufficient.

1. **In band, to the model.** It must appear in the transcript the model reasons over,
   so the model can adapt: re-plan, re-fetch, checkpoint, hand back, or narrow scope. A
   budget hit, a truncation, a cleared tool result, and a denial are all facts the model
   needs. Placing them only in metadata leaves the model reasoning over a history it
   believes is complete.
2. **In the delivered artifact.** The person receiving the result must be able to see
   that it was produced under reduced capability, without reading logs.
3. **In the trace.** An operator must be able to locate and count occurrences later.

A log line satisfies none of the first two. Logging is not loudness.

Good in-band forms carry a handle back: a truncation notice that names the file holding
the full output and where the cut began; a cleared result replaced by a placeholder that
says it was removed, alongside structured counts in the response; a timeout that reports
the operation moved to the background with an identifier to retrieve it.

Never instruct the model to conceal that its context or capability changed.

## Distinguish unknown effects from unclassified errors

An effect can legitimately be unknown after a lost connection: preserve its identity
and reconcile with the environment before retrying. An unclassified exception instead
indicates a diagnostic gap to investigate. Neither state is success. A useful minimum taxonomy distinguishes denied, failed,
timed out, cancelled, blocked by policy, unavailable, retryable, and unknown, with
timeout carried as its own field rather than inferred from an exit code.

Baseline error rates per tool and per model. A rate that differs across models warrants checking adapter fields, tool descriptions,
schemas, model behavior and task mix; it does not identify a cause by itself.

Give distinct consequences distinct wording. A generic denial can lead a model to
believe a mutation landed; state explicitly what did not happen and what the current
state is.

## Completion must close on the environment

Do not let progress be recorded from an actor's self-report. Derive completion from the
environment: the final state, a deterministic check, or an independent reader that did
not perform the work.

When a failure counter, retry counter, or budget exists, the trip must reach the model
as a typed event, and the terminal state must be readable before the result is. A run
that stops for budget, for denial, and for an execution error are three different
outcomes and must not share a shape.

## Audit checklist

Run this over a harness under review:

1. Which code paths can return normally after an operation did not occur?
2. For every catch, what distinct failure meanings does it merge?
3. Does every truncation, eviction, compaction, and clearing emit an in-band marker?
4. Can a tool call be separated from its result by any window, slice, or cap?
5. Which options are accepted for compatibility, and which still imply a capability?
6. What happens when the preferred model, protocol, tool, or feature is unavailable?
7. Which limiters exist but cannot fire under shipped defaults?
8. Does any flag's behavior contradict its name?
9. Is any completion state written from a self-report rather than the environment?
10. Is any degradation visible only in a log?

## Harness bugs that look like model bugs

Several classic complaints about model behavior are harness defects. Check the harness
first when you see: premature termination (a protocol field dropped on resend, or a
budget the model was never told about), forgetfulness and repetition (context cleared
more often than intended, or history evicted without a marker), degraded edit quality
after a provider change (an edit format the model was not trained on), and inconsistent
tool use (a tool silently absent from one session's surface).
