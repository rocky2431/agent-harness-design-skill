# Z.ai: GLM thinking and endpoint differences

Status: documented, checked 2026-09-09. Target: GLM API with explicit model and
endpoint. Source publication: dynamic guide. A Skill evaluated inside ZCode is not
proof of the target adapter's protocol or optimization benefit.

## Interface contract — thinking and preservation

The guide lists thinking enabled by default for GLM-5.3, 5.3-FLASH, 5.2, 5.1, 5 and
4.7. GLM-5.3 and 5.3-FLASH force thinking and cannot disable it; do not apply the
older toggle to those models.

Preserved Thinking defaults **on at the Coding Plan endpoint**, **off at the standard
API endpoint**. Enabling it uses `thinking.clear_thinking: false` and requires returning
complete, unmodified `reasoning_content` in its original sequence. Model identity alone
does not determine endpoint defaults. Interleaved thinking and preserved thinking are
different features.

Source: [Thinking Mode](https://docs.z.ai/guides/capabilities/thinking-mode).

## Behavioral recommendations and limits

The provider recommends preservation particularly for coding/agent scenarios. Treat
any continuity or cache benefit as vendor-reported until measured. Do not infer
training recipes or transfer results from GLM-5.2 on ZCode to GLM-5.3 via another API.
Detailed pretraining/SFT/RL causes remain unknown in this profile.

## Checks and retirement

Proposed protocol test: inspect the endpoint, explicit settings and complete returned
history over a tool continuation; validate the disallowed thinking toggle on a forced
thinking model. Proposed optimization test: matched legal preserved/non-preserved
configurations only where supported, measuring completion, token use and latency.
These target experiments are unverified here. Recheck host translations, endpoint
defaults and model upgrades before copying configuration; preserve the evidence that
justified a choice and retire it only after a relevant comparison.
