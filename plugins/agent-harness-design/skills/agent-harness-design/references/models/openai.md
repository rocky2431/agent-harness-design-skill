# OpenAI: GPT-6 Astra

Status: documented, checked 2026-09-09. Target: `gpt-6-astra` via OpenAI API;
not a claim about every GPT model or every Codex host. Source publication: dynamic
guide, September 2026 changelog. Local target-system optimization trials: unverified.

## Interface contract — model adapter and pending tools

- Tool calling requires Responses; Chat Completions support does not include tools.
- Remove unsupported `temperature`, `top_p` and `top_logprobs`. `none` reasoning is
  unsupported; the migration guide recommends starting at `low` from `none`/`minimal`.
- Async function/custom tools use `async: true`; return results under the original
  `call_id`. The application still owns execution and pending work.

Sources: [Astra guide](https://developers.openai.com/api/docs/guides/latest-model),
[async tools](https://developers.openai.com/api/docs/guides/async-tool-calling),
[changelog](https://developers.openai.com/api/docs/changelog#september-2026).

## Behavioral recommendations — instructions and orchestration

The guide recommends resolving instruction/Skill conflicts, stating when independent
work should be delegated, preserving follow-through, and keeping testing proportional.
Adopt only guidance matching an observed issue and authorized workflow. A delegation
prompt does not require every system to have subagents.

Training: the guide describes delegation training; detailed pretraining/SFT/RL recipes
and a causal explanation for a particular stop remain unknown here.

## Checks and retirement

Proposed adapter check: exercise a read-only tool and its continuation, then inspect
effective settings and pending identities after interruption. Proposed behavior check:
compare task completion, unnecessary questions and test cost with/without the relevant
instruction. Neither has been run as a target-system experiment for this profile.
Recheck API/model/host upgrades; remove a compensation only when the matched result
supports removal. See [adaptation method](../model-adaptation.md).
