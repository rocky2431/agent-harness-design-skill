# Moonshot: Kimi thinking models

Status: documented, checked 2026-09-09. Target: Moonshot API model IDs below, not an
unspecified Kimi Code host. Source publication: dynamic guide. Local target trials:
unverified.

## Interface contract — model-specific controls

| Model | Thinking / preserved history | Effort |
|---|---|---|
| `kimi-k3` | Always reasons and preserves thinking; omit `thinking` | `low`, `high`, `max`; default `max` |
| `kimi-k2.7-code` | Always on; do not request disabled thinking; preservation cannot be disabled | `reasoning_effort` unsupported |
| `kimi-k2.6` | Thinking enabled by default, can disable; `thinking.keep: "all"` enables preservation, default is not kept | `reasoning_effort` unsupported |

The guide gives `kimi-k2.7-code-highspeed` the same thinking behavior as K2.7 Code.
For preserved history return complete assistant messages, including returned
`reasoning_content`, without rewriting them. K3 may return that field; do not fabricate
it when absent. Family-wide parameter presets lose these distinctions.

Source: [Thinking models](https://platform.kimi.ai/docs/guide/use-thinking-models).

## Behavioral hypotheses and training limits

Preserved state may change cost and continuity, but this profile establishes documented
controls, not a locally measured performance gain. Detailed pretraining/SFT/RL causes
are unknown here. Do not infer them from a coding label or fluent tool use.

## Checks and retirement

Proposed adapter check: a multi-step read-only tool task on the selected exact model,
inspecting preserved assistant messages and supported control fields. Include a rejected
unsupported configuration where appropriate. Compare legal modes only where the model
actually offers a choice; K2.7 Code is not a valid thinking-on/off experiment.
Recheck aliases, API changes and host translation before migration. No target-system
optimization experiment was run for this profile.
