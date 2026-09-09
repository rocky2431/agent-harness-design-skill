# Harness Engineering and Ordinary Software

Use this reference when someone applies ordinary software intuitions to a harness, or
asks why a control that would be free in normal code is expensive here.

A harness is every piece of code, configuration, and execution logic around the model:
task framing, context, tools, sandbox and approval policy, progress reporting, failure
handling, and the return of a useful result. It is not a wrapper around a library call.

## The harness is a first-order capability lever

With the model held fixed, harness changes move task success by amounts comparable to
changing models. This is why the harness deserves design attention, and equally why a
bad harness is expensive.

| Evidence | Effect with the model fixed |
|---|---|
| SWE-agent | A designed agent-computer interface more than doubled resolve rate over a raw shell |
| SWE-bench Verified | Same GPT-4: 2.7% with an early RAG scaffold, 28.3% with CodeR |
| MLE-bench | Same gpt-4o: 0.8% / 4.4% / 8.7% across three scaffolds; changing scaffold beat quadrupling wall-clock |
| Aider edit formats | Same `gpt-4-1106-preview`: 20% with search/replace blocks, 61% with unified diffs |
| Harness-Bench | Same task set and model pool: 76.2% versus 52.4% across harnesses |

The same literature reports harness-induced variance that can exceed model-induced
variance, including reversals of model ranking. Report capability for a model-harness
pair, never for a model alone.

The counterweight matters as much: a controlled study of repository context files found
no improvement in task success and over 20% higher inference cost, with model-generated
context files reducing success in most settings. A harness component is a hypothesis
about capability, and many popular ones are net negative. Measure rather than assume in
either direction.

## Where the intuitions break

| Axis | Ordinary software | Harness | Consequence |
|---|---|---|---|
| Specification | Complete and mechanically decidable | Partly natural language, interpreted by a general reasoner | Branches cannot be enumerated; over-specification is itself a failure mode |
| Determinism | Same input, same output | Output is a distribution | Unit tests become evals with repetition and reported uncertainty |
| Failure signature | Crash, exception, type error | Well-formed, confident, wrong | Silent failure is the default failure mode, not an edge case |
| Component trajectory | Dependencies are stable or decay slowly | The wrapped model keeps improving | Harness code has a shelf life; today's fix becomes tomorrow's ceiling |
| Cost of a control | Near zero | Consumes the same scarce attention that produces capability | Controls are subtractive and must be measured |
| Data and instruction channel | Separated by parser and type system | Merged in one token stream | Injection is a type confusion no parser fixes; enforce at the effect |
| State | Variables with defined lifetime | A lossy, finite window that degrades with length and also holds the program | Context is working memory and program text at once |
| Error text | Consumed by code | Consumed by reasoning | Error message quality is a functional interface |
| Refactoring | Behavior-preserving transformations exist | Reordering or rewording changes behavior | There is no safe refactor without an eval |
| System boundary | The code is the system | The environment is part of the system | Making the environment legible often beats changing the loop |
| Visibility of degradation | A crash or an error | Often only a subtle drop in output quality | Visibility must be built; it does not appear on its own |

## What follows from those differences

**Correctness is statistical.** Report reliability across repeated trials, not the best
run. A single success does not establish that the configuration works.

**Silent failure needs active defense.** Ordinary software fails loudly by default
because type systems and runtimes stop it. Here a failed operation still produces
fluent, plausible output. See [failure-visibility.md](failure-visibility.md).

**Every compensating component encodes an assumption about model or host limits.**
Those assumptions can go stale or be wrong; business authority and environment contracts
may remain necessary independently of model capability.
Re-test them on upgrade; remove one at a time and measure.

**A control is not free.** It consumes context, latency, and authorized strategies. The
question is never "is this control good practice" but "does this control buy more than
its capability tax on this model-harness pair."

**The environment can be a high-leverage surface.** Fast tests, readable errors,
reproducible setup, and a working development environment change agent outcomes more
than most loop logic. A cloud agent lacking a full environment degrades in output
quality rather than failing visibly, which makes the cause hard to find.

## What does not change

Non-determinism is not an excuse to abandon engineering discipline. Authority, effects,
identity, schemas, quotas, and evidence remain exactly representable and belong in code.
The difference is where the line falls, not whether a line exists. See
[design-decisions.md](design-decisions.md) for placing that line.
