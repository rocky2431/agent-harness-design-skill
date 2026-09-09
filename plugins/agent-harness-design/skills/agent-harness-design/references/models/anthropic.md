# Anthropic: Claude Fable 5.1

Status: documented, checked 2026-09-09. Target: Claude Fable 5.1 on the Claude API;
resolve exact model ID, account and API options before applying. Local target-system
optimization trials: unverified. Source publication: dynamic model guide.

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

## Checks and retirement

Proposed protocol test: a valid tool continuation plus an incompatible-prefix
counterexample under applicable account settings; inspect explicit rejection or
recorded transformation. Proposed behavior test: matched search and multi-tool tasks,
recording correctness, unnecessary serialization, latency and cost. Unverified here.
Recheck account/API/model changes before reuse. Compare later compaction points only
with valid history. See [historical cases](../historical-cases.md).
