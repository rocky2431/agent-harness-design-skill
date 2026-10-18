# Historical Cases and Updating Guidance

Read when revisiting a past architecture or model compensation. Historical primary
sources checked 2026-09-09; 0.6.0 retirements recorded 2026-10-18. Reported results
are neither local replications nor universal causal findings.

## Architecture changes with task and model

| Period / configuration | Problem and reported mechanism | Limit and current consequence |
|---|---|---|
| ReAct, 2022 | Interleaved reasoning, actions and observations grounded later steps; demonstrated feedback-driven behavior | Older models and authors' environments; teach the feedback loop without demanding visible chain-of-thought |
| SWE-agent, 2024 ACI | Navigation/editing commands changed coding performance | Evaluate tool usability; the old editor/shell is not mandatory for business agents |
| Anthropic, 2024-12 workflows | Stable and open-ended tasks used different control flow | Chaining, routing, workers and evaluators are patterns, not a maturity ladder |
| Manus, 2025 context | Changing prompt/tool prefixes was costly; stable definitions, selective availability and recoverable context supported its deployed agent | Preserve history semantics; native deferred discovery differs from rewriting definitions |
| Anthropic, 2025-11 coding | Initialization, feature evidence and incremental work addressed lost cross-session state and false completion | Persist handoff evidence; initializer/sprint machinery remains conditional |
| Anthropic, 2026-03 apps | Sonnet 4.5 resets, Opus 4.5 adjustments and Opus 4.6 sprint removal reflected changed stopping/evaluation needs | Planner/evaluator helped some settings; re-test, then retire unneeded compensations |

Sources: [ReAct](https://react-lm.github.io/),
[SWE-agent ACI](https://swe-agent.com/0.7/background/),
[effective agents](https://www.anthropic.com/engineering/building-effective-agents),
[Manus context](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus),
[long-running harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents),
[long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps).

## Corrections in 0.5.0

- **Budget diagnosis:** universal “raise budget first” came from a particular task-budget
  feature. Check exhaustion, visible settings, instruction/approval conflicts, protocol
  errors and host stops before choosing a fix; countdown rules stay feature-specific.
- **Tool availability:** preserve historical prefixes and references while allowing native
  deferred loading and supported updates; compare Manus with
  [Claude tool search](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool).
- **Migration baseline:** preserve semantics and make each API valid first. Unsupported
  parameters or invalid history cannot establish a fair behavioral comparison.
- **Unknown result:** reconcile effects after connection loss. Unknown exceptions need
  diagnosis; neither state is success or grounds for blind resubmission.
- **Concurrency/restoration:** isolate independent writes, serialize dependencies. A
  mutable or disappearing URL alone does not guarantee recoverable evidence.

## Retirements in 0.6.0

The 0.5.2 rule “Re-test on upgrade; do not remove on upgrade” discouraged retiring
obsolete instructions. Re-test, then retire unneeded compensations and record why here.
Authority, trust boundaries and environment evidence remain invariants. The
[Opus 5 guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5)
recommends removing redundant verification prompts; benefit here is unverified, and task checks remain applicable.

The former four statement kinds, four strengths, five evidence labels and eleven-field record
helped untangle claims but became a formatting tax. Use distinctions on demand and a four-field core.
The former universal three-surface rule now requires model/recipient visibility plus traces where
operators monitor runs. Typed replacement errors remain one honest compatibility path, not the only one.

## Maintain guidance

When a release, protocol change, real failure or credible study changes an assumption:

1. Identify the affected configuration, source/date and evidence limits.
2. Check current guidance and counterevidence; avoid inferring training causes.
3. Update guidance and evidence together; retain superseded conditions and reasons here.
4. Run affected checks. Repeat trials for stochastic benefits; one failure can establish
   protocol incompatibility.
5. Release through existing tooling; distinguish source, installed copies and new sessions.

[Model adaptation](model-adaptation.md) routes profiles;
[research basis](research-basis.md) indexes sources. Re-check changing contracts before
adoption; these Markdown records need no runtime, registry or scheduled monitor.
