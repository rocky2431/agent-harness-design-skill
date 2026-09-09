# Historical Cases and Updating Guidance

Read when a past architecture is proposed as a current rule or when reconsidering a
component after a model upgrade. These are primary-source accounts checked 2026-09-09;
reported outcomes are not local replications or universal causal findings.

## Architecture changes with the task and model

| Period / configuration | Problem and mechanism | Reported result and limit | Current design consequence |
|---|---|---|---|
| ReAct, 2022 | Interleave reasoning, actions and observations to ground the next step | Demonstrated feedback-driven behavior in the authors' environments; older models and prompting | Teach the causal loop; do not demand visible chain-of-thought from modern APIs |
| SWE-agent, 2024 ACI | Raw computer interaction made navigation/editing difficult; design commands and feedback for agent use | Task performance changed with the interface; evidence is tied to the tested coding setting | Evaluate actual tool usability; do not mandate the old editor or shell for business agents |
| Anthropic, 2024-12 workflow patterns | Stable tasks and open-ended tasks need different control flow | Chaining, routing, workers and evaluators are composable patterns, not a maturity ladder | Choose by task dependencies and observable benefit |
| Manus, 2025 context practice | Cache churn and historical tool references made changing prompt/tool prefixes costly | Stable definitions, selective availability and recoverable context supported its deployed agent | Preserve history semantics; native deferred tool discovery is not the same operation as rewriting definitions |
| Anthropic, 2025-11 long-running coding | A new session lost project state or marked incomplete features done | Initialization, feature evidence and incremental work aided cross-session continuation | Persist what the next session needs; initializer/sprint machinery remains conditional |
| Anthropic, 2026-03 long-running apps | Model changes altered premature stopping and useful evaluation frequency | Sonnet 4.5 context resets, Opus 4.5 adjustments, and Opus 4.6 removal of sprint structure illustrate different needs; planner/evaluator still helped in some settings | Re-test each compensation; newer models justify neither automatic deletion nor permanent scaffolding |

Sources: [ReAct](https://react-lm.github.io/),
[SWE-agent historical ACI](https://swe-agent.com/0.7/background/),
[Building effective agents](https://www.anthropic.com/engineering/building-effective-agents),
[Manus context engineering](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus),
[long-running harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents),
[long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps).

## Corrections made in the 0.5.0 organization

- **Budget diagnosis:** the older universal “raise budget first” instruction came from
  a particular task-budget feature. Check actual exhaustion and visible settings,
  instruction/approval conflicts, protocol errors and host stopping before choosing a
  fix. Provider-specific countdown rules belong to that feature, not every governor.
- **Tool availability:** keep used definitions and historical prefixes consistent;
  allow native deferred loading and supported configuration updates. Compare the Manus
  practice above with [Claude tool search](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool).
- **Migration baseline:** retain task semantics but make each model's API protocol
  valid first. An unchanged unsupported parameter or invalid message history cannot
  serve as a fair behavioral baseline.
- **Unknown result:** uncertainty after a lost connection is a legitimate operation
  state requiring reconciliation. Unknown exceptions indicate missing diagnostics;
  neither should be mislabeled success or justify blind resubmission.
- **Concurrency and restoration:** isolate writes that can run independently;
  serialize shared dependencies. A URL alone does not guarantee recoverable evidence
  if its contents can change or disappear.

See [model-adaptation.md](model-adaptation.md) for current profile selection and
[research-basis.md](research-basis.md) for the larger source index.

## Maintain a living recommendation

Update when a model/host release, protocol change, reproduced failure or credible new
study changes a relevant assumption. This is a maintenance practice, not a scheduled
monitor or a requirement to browse every source on every Skill invocation.

1. Locate the affected component/profile; record exact configuration, source date,
   checked date and whether the claim is documentation, observation or inference.
2. Compare with the current recommendation and material counterevidence. Explain which
   conditions changed; do not infer a training cause from the outcome alone.
3. Update the active rule and its evidence together. Retain the superseded condition,
   reason and useful result in a historical case rather than a competing active default.
4. Run the smallest affected protocol/behavior cases. Repeated comparisons support
   stochastic benefit claims; one failed request can establish a protocol incompatibility.
5. Release the source and regenerate distribution through the repository's existing
   tooling. Distinguish published packages, installed copies and newly tested sessions.

Do not add a new database, routing registry or workflow engine just to maintain these
Markdown records. Model/API requirements need current verification when adopted;
durable concepts need revision when their supporting evidence changes.
