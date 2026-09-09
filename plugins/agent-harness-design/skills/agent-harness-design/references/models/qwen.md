# Qwen: historical training/interface evidence and current limits

Status: historical/documented, checked 2026-09-09. This is not a current Qwen-family
configuration preset. Local target-model trials: unverified.

## Qwen3-Coder — 2025 historical coding interface

[Qwen3-Coder](https://qwenlm.github.io/blog/qwen3-coder/) (2025-07-22) describes agent RL
with tool/environment feedback and a Qwen Code prompt/function-calling protocol adapted
to the model. It supports testing the interface the target model was trained to use;
it does not prove that every later Qwen release should use that exact scaffold.

Adapter decision: resolve the actual checkpoint, serving engine, chat template and
tool-call parser together. An OpenAI-compatible URL alone does not establish that the
server renders the expected template or parses tool calls correctly. The particular
deployment's contract must be verified before recommending parameter values.

## Qwen3 — training background

[Qwen3](https://qwenlm.github.io/blog/qwen3/#post-training) (2025-04-29) describes long
CoT cold start, reasoning RL, thinking-mode fusion and general RL. These published
stages explain different training objectives, not the causal value of a planner,
memory database or evaluator on a user's task. Pretraining and deployment differences
can also matter; do not turn a family name into a behavioral diagnosis.

## Qwen3.8 — current boundary

The [Qwen3.8-Max announcement](https://qwen.ai/blog?id=qwen3.8) (2026-08-02) provides
current release context. The material checked here does not establish a deployable
template, parser, sampling and state-preservation profile. Those details remain
unverified, rather than inherited from Qwen3-Coder.

## Checks and retirement

Proposed check: resolve a supported checkpoint/template/parser, complete a real tool
round trip, then compare legal interface choices on the same task/environment. Inspect
parsed calls and environment outcomes separately from model-grader scores. Recheck on
checkpoint, quantization, server or parser changes; keep 2025 recommendations historical
unless the exact target evidence supports reuse. No optimization benefit is claimed.
