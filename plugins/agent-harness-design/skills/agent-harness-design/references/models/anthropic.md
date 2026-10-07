# Anthropic: Claude Fable 5.1

Status: documented, checked 2026-09-09; second-model section checked 2026-10-06.
Target: Claude Fable 5.1 on the Claude API; resolve exact model ID, account and API
options before applying. Local target-system optimization trials: unverified.
Source publication: dynamic model guide.

## Interface contract — history and recovery

For accounts created on/after 2026-08-31, the guide binds thinking blocks to their exact
conversation prefix. Editing system/tools/earlier messages before replay can return
400. The beta `thinking-binding-controls-2026-08-01` supports
`thinking.block_binding.prefix_mismatch_behavior: "drop_block"`; this discards state
and must not become a hidden success-shaped fallback.

Preserve returned assistant history. Use supported mid-conversation updates or native
compaction; for a fresh client summary, do not replay old bound thinking blocks.
These conditions must not be shortened to “all Claude history is always immutable.”

Source: [Fable 5.1 guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1).

## Behavioral recommendations — tools, effort and persistence

That guide separately recommends batching independent tool work, explicit retrieval
criteria at low effort, completing requested work, and bounded changes/testing. These
are conditional prompt candidates, not protocol rules. Training recipes explaining
these behaviors are not established by this source.

Native [tool search](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool)
supports deferred tools. Discovering a preregistered tool is different from rewriting
a signed history prefix; verify the exact API mechanism and compatibility.

## Second-model strategies — advisor and orchestrator

Interface contract ([advisor tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool),
beta `advisor_20260301`): the executor decides when to call; the server runs a separate
advisor inference over the full transcript, without tools, inside the same request.
Opus 5.5, Sonnet 5.5, Fable 5.1 and Mythos 5.1 executors reject a forced `tool_choice`,
and Opus 5/5.5, Sonnet 5.5, Fable 5/5.1 and Mythos 5/5.1 advisors return an encrypted
result the client cannot read. Advisor tokens are
reported only in `usage.iterations`. Claude Code's [advisor](https://code.claude.com/docs/en/advisor)
offers no setting to force or cap calls, and subagents inherit the configured advisor.

Vendor measurements, [checked 2026-10-06](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence),
one internal benchmark each, not locally reproduced:

- Opus 5.5 at its default (`medium`) matched Fable 5.1 at its default on an SWE-bench Pro
  subset for about a fifth of the cost per solved task.
- An Opus 5.5 executor at `high` with a Fable 5.1 advisor gained 1.7 points over Opus 5.5
  alone at `high`, at the edge of run-to-run noise, for about 2.1x the cost — roughly what
  more effort buys on the same curve.
- The consult rate is fragile: an Opus 5.5 executor at `low` consulted on 1 of 300 chart
  tasks and scored 7 points below Opus 5.5 alone. A turn-2 prompt nudge helped Haiku,
  had no measured effect on Sonnet, and slightly lowered Opus pass rates.
- Delegating to cheaper workers paid only for independent bulk work or input larger than
  one context; otherwise the coordinator's model alone at lower effort won.

Behavioral recommendation (conditional): price the advisor's model alone at low effort
before adding an advisor, and expect gains mainly where the executor is well below the
advisor and actually consults. An advisor sees the author's whole transcript, so it is
not a blind reviewer; keep required independent review separate.

## Checks and retirement

Proposed protocol test: a valid tool continuation plus an incompatible-prefix
counterexample under applicable account settings; inspect explicit rejection or
recorded transformation. Proposed behavior test: matched search and multi-tool tasks,
recording correctness, unnecessary serialization, latency and cost. Unverified here.
Recheck account/API/model changes before reuse. Compare later compaction points only
with valid history. See [historical cases](../historical-cases.md).
