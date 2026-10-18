# Anthropic: current Claude family

Status: official documentation checked 2026-10-18 unless dated otherwise below.
Targets: Claude API and Claude Code; resolve endpoint, account, exact model ID, host
build and effective effort. Local target-system optimization trials: unverified.

| Target | Current prompting guide | Claude Code default effort |
|---|---|---|
| `claude-opus-5-5` | [Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5) | `medium` |
| `claude-sonnet-5-5` | [Sonnet 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5) | `medium` |
| `claude-haiku-5-5` | [Haiku 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5) | `medium` |
| `claude-fable-5-1` | [Fable 5.1](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1) | `high` |

Before applying behavioral advice, re-check the matching guide above and
[best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices).
Request extra initiative explicitly, explain instruction motives, and prefer positive
examples. Reduce aggressive emphasis when it causes overtriggering; the documented
example concerns Opus 4.5/4.6, not a measured effect across every newer model.

## Opus prompting — behavioral recommendations

The [Opus 5 guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5)
reports unprompted verification: remove generic verification prompts and redundant
verifier scaffolds that cause over-verification. Preserve required outcome evidence
and task-specific checks. State the intended scope because the model may expand it.
It delegates readily; damp unnecessary spawning for small work. Claude Code/Agent SDK
caps `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` and
`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` require 2.1.217+.
Effort controls thinking rather than visible length; ask for concise prose directly.
Evaluate `low`/`medium` where quality holds and `xhigh` for demanding coding.
These are vendor recommendations, not locally measured benefits.

[Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5)
always has thinking on; `thinking: {"type": "disabled"}` is unsupported. Parse content
by block type. Start at `medium`, sweep effort, and reserve `xhigh`/`max` for measured
gains. Budget output for thinking plus the reply. Per-message effort changes (beta)
preserve cache; changing top-level effort invalidates it. For unattended loops, a
text-only `end_turn` can be a progress report: check remaining work and outstanding
operations before completion. Keep continuations bounded and real authorization gates.
Do not transfer these behavioral prescriptions to Sonnet or Haiku without checking
their guides and workload.

## Sonnet and Haiku 5.5 — different conditions

[Sonnet 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5)
defaults to `high` on the API, unlike Claude Code's `medium`. The guide recommends
`medium` for well-specified agentic coding and higher effort for harder work. At low
effort it can skip verification; low/medium can check in before long work finishes.

[Haiku 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5)
replaces the old thinking budget with effort, default `medium`. Thinking can be disabled
at `low`/`medium`/`high`, but not `xhigh`/`max`. Its guide suggests verification prompting
when low/medium runs report unchecked changes. Thus removing Opus over-verification
prompts is not a family-wide instruction. Test the observed failure on the exact target.

## Claude Code — host contract

[Model configuration](https://code.claude.com/docs/en/model-config): explicit env var,
`--effort` or `/effort` choices precede settings, then model defaults. Settings keys
`modelSettings`/`effortLevel` reject `max`; only `CLAUDE_CODE_EFFORT_LEVEL` persists it.
That variable also overrides Skill/subagent frontmatter effort. Opus 5.5 ignores the
legacy top-level user `effortLevel`; project/local/managed settings still apply.

[Subagents](https://code.claude.com/docs/en/sub-agents) support `model`, `effort`,
`disallowedTools` and `omitClaudeMd` (2.1.271+). Explore normally uses the conversation
model; current docs qualify Fable on subscription/Console/LLM-gateway connections with
an Opus alias. A custom `Explore` with `model: haiku` replaces the built-in definition;
check effective model overrides. The owner's 2026-10-18 research dates the inheritance
change to 2.1.198; that version attribution was not re-established here.
[Subagents inherit the advisor](https://code.claude.com/docs/en/advisor).

## Claude thinking — history and recovery

For accounts created on/after 2026-08-31 00:00 UTC, **Fable 5.1, Opus 5.5, Sonnet 5.5
and Haiku 5.5** thinking blocks are bound to their exact conversation prefix by default.
Editing system/tools/earlier messages before replay returns 400 on a prefix mismatch.
Older accounts opt into enforcement by setting the mismatch behavior. The beta
`thinking-binding-controls-2026-08-01` supports
`thinking.block_binding.prefix_mismatch_behavior: "drop_block"`; this discards state
and reports dropped blocks in `input_transformations`. Keep that loss visible; it must
not become a hidden success-shaped fallback.

Preserve returned assistant history. Use supported mid-conversation updates or native
compaction; for a fresh client summary, do not replay old bound thinking blocks.
These conditions must not be shortened to “all Claude history is always immutable.”

Sources: [preserved thinking](https://platform.claude.com/docs/en/build-with-claude/preserved-thinking#prefix-check),
[Fable 5.1 guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1).

## Fable 5.1 — tools, effort and persistence

The Fable guide separately recommends batching independent tool work, explicit retrieval
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
and Opus 5/5.5, Sonnet/Haiku 5.5, Fable 5/5.1 and Mythos 5/5.1 advisors return an encrypted
result the client cannot read. Advisor tokens are
reported in `usage.iterations`. The API supports per-request `max_uses`; Claude Code's [advisor](https://code.claude.com/docs/en/advisor)
offers no setting to force or cap calls, and subagents inherit the configured advisor.

Vendor measurements, [originally checked 2026-10-06](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence),
retained as dated evidence, not locally reproduced:

- Opus 5.5 at its default (`medium`) matched Fable 5.1 at its default on an SWE-bench Pro
  subset for about a fifth of the cost per solved task.
- An Opus 5.5 executor at `high` with a Fable 5.1 advisor gained 1.7 points over Opus 5.5
  alone at `high`, at the edge of run-to-run noise, for about 2.1x the cost — roughly what
  more effort buys on the same curve.
- The consult rate is fragile: an Opus 5.5 executor at `low` consulted on 1 of 300 chart
  tasks and scored 7 points below Opus 5.5 alone. The earlier turn-2 nudge result (helping Haiku, neutral on Sonnet, slightly hurting
  Opus) remains 2026-10-06 evidence, not re-checked on the current page.
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
Re-test on upgrade, then retire unneeded compensations and record the reason in
[historical cases](../historical-cases.md). Recheck account/API/model changes before reuse
and compare later compaction points only with valid history.
