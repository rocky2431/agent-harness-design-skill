# Trust, Tools, and Effects

Use this reference for authorization, prompt injection, tool boundaries, approvals,
mutations, and sandboxing.

## Separate capability, authority, and evidence

- **Capability**: what the environment technically allows.
- **Authority**: what the owner or trusted policy permits for this task.
- **Evidence**: what shows an operation or outcome occurred.

Possessing a capability is not authority to use it. A model proposal, worker message,
webpage, email, ticket, file, tool description, or stored memory does not grant new
authority. Tool output may provide facts needed to fill an authorized operation, but
it does not expand the operation's purpose or scope.

## Trusted enforcement boundary

Enforce high-impact constraints where the real effect is executed. Depending on the
system, that may be an API gateway, database policy, OS sandbox, cloud IAM role,
transaction layer, or tool wrapper. Prompt instructions remain useful behavioral
guidance, but they cannot substitute for an enforcement point an attacker cannot edit.

Keep secrets outside model-visible context when possible. Supply scoped credentials at
execution time; prevent one tool's data from being copied into an unrelated sink; and
log identifiers or hashes rather than secret values.

## Untrusted content and prompt injection

Mark provenance and keep control intent separate from data. When an agent reads
external content:

1. retain the owner's goal and authorized effect boundary in trusted state;
2. treat embedded instructions as data unless a trusted policy explicitly delegates
   authority to that source;
3. authorize each real operation against the trusted goal and available evidence;
4. restrict information flows when sensitive data and untrusted sinks coexist;
5. test both benign utility and adversarial outcomes.

Prompt reminders and injection classifiers can reduce risk, but they are probabilistic.
For material effects, combine them with runtime authorization and information-flow or
capability controls appropriate to the threat.

## Approval is conditional

Require human approval when an action exceeds existing authority, contains a material
ambiguity the owner must resolve, or has impact that policy assigns to a human. Scope
approval to the meaningful operation rather than every low-level tool call.

Do not re-ask merely because execution moved to another agent or tool. Conversely,
approval of a plan is not blanket authority for materially different arguments,
recipients, amounts, environments, or side effects.

Useful patterns include:

- pre-authorized bounded operations for routine, reversible work;
- approve-once scopes with expiry or quantitative limits;
- preview/draft followed by commit for high-impact or hard-to-reverse effects;
- direct commit for explicit, low-risk, repeatable operations;
- break-glass paths with stronger identity and audit.

Draft/commit is a risk-control option, not a universal requirement.

## Mutation, retry, and concurrency

Make a mutation idempotent when the transport or workflow may retry it. Use an
idempotency key, compare-and-swap version, transaction, natural unique key, or explicit
operation record when appropriate. Purely local one-shot work does not need ceremonial
idempotency machinery.

Parallel writes are safe when ownership is disjoint or the environment supplies real
conflict control, for example:

- separate Git worktrees or files with an explicit integration owner;
- independent records protected by unique keys;
- database transactions and isolation;
- optimistic concurrency with a surfaced conflict;
- append-only event partitions with deterministic merge rules.

Sequentialize operations with shared mutable dependencies. Never rely on “the agents
probably will not touch the same thing.”

## Tool results and error semantics

Return structured facts the model can act on:

- operation status: succeeded, denied, failed, timed out, canceled, or unknown;
- stable identifiers for changed resources;
- concise outputs and bounded diagnostic detail;
- whether a retry is safe and what must change first;
- evidence needed to verify a consequential outcome.

Do not turn transport success into business success. A `200`, zero exit code, or tool
completion event may prove only that a request was accepted. Verify the relevant state
when the consequence warrants it.

## Sandbox selection

Use a sandbox when the model can execute arbitrary or attacker-influenced code, access
untrusted dependencies, or make changes whose blast radius should be contained. A real
sandbox controls filesystem, process, network, resource, and secret access. A `cwd`,
prompt, Docker label, or tool allowlist alone is not equivalent.

The sandbox may intentionally expose a broad shell because isolation makes that broad
interface more useful and safer than a long bespoke tool list. Validate the actual
lifecycle: creation, policy, execution, output capture, cleanup, and escape resistance
relevant to the use case.
