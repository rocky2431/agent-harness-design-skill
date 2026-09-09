# Google: Gemini 3

Status: documented, checked 2026-09-09. Target: Gemini 3 family on Gemini API; the
guide includes `gemini-3-flash-preview` and `gemini-3.1-pro-preview`. Resolve the actual
ID and SDK version. Source publication: dynamic guide. Local target trials: unverified.

## Interface contract — state and tool continuation

Stateful Interactions using `previous_interaction_id` lets the server manage history
and thought signatures. When managing history manually, carry the required thought
blocks/signatures into subsequent requests. Do not replace them with a prose summary,
guess their content, or assume a stateful SDK and a manual adapter do identical work.

Source: [Gemini 3 guide](https://ai.google.dev/gemini-api/docs/gemini-3).

## Behavioral recommendation — sampling

The guide recommends default temperature `1.0` for Gemini 3 and warns that lower values
can cause loops or worse reasoning. This is a family-specific recommendation, not a
universal low-temperature reliability rule or proof of benefit on your workload.
Detailed training causes for this behavior are unknown in this profile.

## Checks and retirement

Proposed protocol check: complete a function-call round trip separately through the
chosen stateful or manual path and inspect retained state. Proposed behavior check:
compare the documented default with another legal setting on representative tasks,
including looping, correctness, latency and cost. Do not confound that comparison by
dropping signatures from one arm. Neither check was run for this profile.

Recheck preview IDs, API modes and SDK history handling on migration. Keep temperature
guidance conditional until target evidence supports it; do not project it onto earlier
or future Gemini families. See [adaptation method](../model-adaptation.md).
