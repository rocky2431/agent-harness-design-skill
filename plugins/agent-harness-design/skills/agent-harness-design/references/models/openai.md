# OpenAI: GPT-6.1 Sol and GPT-6 Astra

Status: official model, host and adapter documentation checked 2026-10-18;
no new API adapter round trip was run. Targets: `gpt-6.1-sol` and
`gpt-6-astra` via the OpenAI API or Codex CLI. Resolve endpoint, host build, mode and
effective effort separately. Local target-system optimization trials: unverified.

## Current model choice — dated vendor guidance

GPT-6.1 Sol
[launch](https://openai.com/index/introducing-gpt-6-1-sol/): release date 2026-09-29
checked by the owner's 2026-10-18 research; the retrieved launch page did not expose
that date, so it was not independently re-confirmed here.
The [GPT-6 model guide](https://openai.com/index/practical-guide-building-gpt-6/)
recommends it for complex coding, research and computer use, positioning intelligence
near Astra at one fifth the token price. Standard API USD per million tokens:

| Model | Input | Output |
|---|---:|---:|
| GPT-6.1 Sol | $2 | $10 |
| GPT-6 Astra | $10 | $50 |
| GPT-6 Luna | $0.10 | $0.50 |

These are dated list prices and vendor positioning, not local workload measurements.
Before behavioral changes, re-check the current model guide and
[prompting guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra).

## Codex — effort, fan-out and reviewer roles

[Models](https://learn.chatgpt.com/docs/models): `ultra` delegates separable work to
parallel subagents; most tasks need neither Max nor Ultra. The
[configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
defines `agents.max_concurrent_threads_per_session` (excluding the primary thread),
`agents.default_subagent_model` and `features.multi_agent` (stable, on by default;
re-confirmed on the English reference 2026-10-18). Inspect effective child
models and resource use rather than assuming effort changes only private reasoning.
[OpenAI's usage guidance](https://help.openai.com/en/articles/20001516-managing-usage-with-gpt-6-astra-in-work-and-codex)
notes that higher effort uses more allowance and need not improve the result.

[`codex-auto-review`](https://developers.openai.com/codex/concepts/sandboxing/auto-review)
reviews sandbox-boundary approval requests. It changes the reviewer, not authority or
sandbox limits. [Code review](https://learn.chatgpt.com/docs/developer-commands) documents
`/review` and `codex review`; these are different jobs from approval review.
Local CLI evidence: `codex exec --help` on Codex CLI 0.159.3, checked 2026-10-18,
lists the `review` subcommand as running a code review against the current repository.
This confirms `codex exec review` for that build; the fetched official CLI reference
did not directly document it. No review execution was tested here.

## Interface contract — Sol/Astra adapter and pending tools

- Tool calling requires Responses; Chat Completions support does not include tools.
- Remove unsupported `temperature`, `top_p` and `top_logprobs`. `none` reasoning is
  unsupported; the migration guide recommends starting at `low` from `none`/`minimal`.
- Async function/custom tools use `async: true`; return results under the original
  `call_id`. The application still owns execution and pending work.

Sources: [GPT-6 guide](https://developers.openai.com/api/docs/guides/latest-model),
[async tools](https://developers.openai.com/api/docs/guides/async-tool-calling),
[changelog](https://developers.openai.com/api/docs/changelog#september-2026).

## Behavioral recommendations — instructions and orchestration

The guide recommends resolving instruction/Skill conflicts, stating when independent
work should be delegated, preserving follow-through, and keeping testing proportional.
Adopt only guidance matching an observed issue and authorized workflow. A delegation
prompt does not require every system to have subagents.

Training: the earlier 2026-09-09 guide described delegation training; that wording is
retained as historical context, not re-confirmed in the current guide. Detailed
pretraining/SFT/RL recipes and a causal explanation for a stop remain unknown here.

## Checks and retirement

Proposed adapter check: exercise a read-only tool and its continuation, then inspect
effective settings and pending identities after interruption. Proposed behavior check:
compare task completion, unnecessary questions and test cost with/without the relevant
instruction. Neither has been run as a target-system experiment for this profile.
Re-test on upgrade, then retire compensations the new model no longer needs and
record why in [historical cases](../historical-cases.md). See [adaptation method](../model-adaptation.md).
