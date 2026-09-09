# DeepSeek: V4 thinking and historical R1

Status: documented, checked 2026-09-09. Current coverage: `deepseek-v4-pro` and
`deepseek-v4-flash`, thinking mode, OpenAI-format Chat Completions. Other API formats
need their own mapping. Source publication: dynamic guide. Local target trials: unverified.

## Interface contract — effective settings and history

Thinking defaults to enabled with effort `high`. Requested `medium`, `high`, and
`xhigh` all map to actual `high`; `low` and `max` retain their values.
Thinking ignores `temperature`, `top_p`, `presence_penalty`, and `frequency_penalty`
without rejecting them. Accepted parameters therefore do not prove effective settings.

With `tools` in the request, preserve all prior `reasoning_content`, including turns
without a tool call; missing required content can produce 400. Without `tools`, prior
reasoning is not required and is ignored if supplied. Do not apply old R1 history rules
to V4 thinking tools.

Source: [Thinking Mode](https://api-docs.deepseek.com/guides/thinking_mode/).

## Historical training and recommendations

[DeepSeek-R1](https://github.com/deepseek-ai/DeepSeek-R1) (2025) distinguishes R1-Zero's
RL without preliminary SFT from R1's SFT/RL stages. Its historical usage guidance
suggests temperature 0.5–0.7 and user-message prompt placement. It does not establish
V4 defaults, serving templates or a need for a particular planner. V4 training causes
for the adapter behavior above are not established here.

## Checks and retirement

Proposed checks: exercise a tool-bearing continuation and a no-tools conversation;
inspect full history and effective effort. Use a missing-state counterexample to test
compatibility separately from quality. An “xhigh vs high” benchmark cannot establish
an effort benefit when both map to `high`. Recheck model/mode/API upgrades; compare
behavioral changes only between legal configurations. No such target trial is claimed.
