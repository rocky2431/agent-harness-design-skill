# Model Adaptation

Use for a named target model, a provider/API issue, model migration, or a suspected
model-specific compensation. General responsibilities live in
[architecture-guide.md](architecture-guide.md); this module changes their realization.

## Select the target configuration

The consulting model and the target system's model may differ. Resolve what matters
from code, configuration, request traces and primary documentation:

- exact model ID or snapshot, provider, endpoint and region where relevant;
- API surface, SDK/adapter and host version, including local serving template/parser;
- reasoning/thinking mode, effective effort and sampling settings;
- tool surface, multimodal inputs, context/recovery method and task distribution;
- observation date and whether the identity is pinned or a moving alias.

Do not invent missing values. Give the general design now and name only the missing
facts that block concrete parameter advice. A family match is a navigation hint, not
verified compatibility. Treat alias resolution and current protocol requirements as
facts to verify live before deployment. These profiles are dated snapshots, not an
automatic model router or an exhaustive support matrix.

| Profile | Documented coverage and reason to read |
|---|---|
| [OpenAI](models/openai.md) | GPT-6 Astra, Responses tool calls, async work, instruction calibration |
| [Anthropic](models/anthropic.md) | Claude Fable 5.1, history binding, tool batching and effort-dependent search |
| [Google](models/google.md) | Gemini 3, temperature recommendation, stateful vs manual thought-state handling |
| [DeepSeek](models/deepseek.md) | V4 Pro/Flash thinking, effective effort mapping, history with/without tools; historical R1 |
| [Moonshot](models/moonshot.md) | K3, K2.7 Code and K2.6 differences in thinking controls and preservation |
| [Z.ai](models/z-ai.md) | GLM-5.3/5.2 and endpoint-specific Preserved Thinking |
| [Qwen](models/qwen.md) | Historical Qwen3/Coder training and protocol; limits of current Qwen3.8 evidence |

Read only the matching profile and relevant common component. If none matches, inspect
the target's current primary documentation rather than borrowing a nearby model's rules.

## Separate four kinds of statement

| Kind | What it establishes | Required evidence and validation |
|---|---|---|
| Interface contract | What a specific API accepts, requires, ignores, or maps | Current provider contract plus a targeted request/response or adapter check |
| Behavioral recommendation | A prompt, tool format or orchestration choice that may improve a task | Named model/task conditions; compare legal baseline and candidate on real tasks |
| Training background | Published pretraining, SFT, RL, distillation or agent-environment exposure | Original model report; distinguish disclosed facts from missing details |
| Historical case / hypothesis | Why a mechanism was tried, retained or replaced | Dated conditions and counterevidence; no automatic current recommendation |

These kinds are independent of Invariant / Default / Conditional pattern / Example.
A protocol requirement may be mandatory in one adapter but irrelevant elsewhere.
A general architectural capability such as persistence may be optional for a short task.

Training can suggest a hypothesis, not settle an architecture. Pretraining coverage may
motivate a retrieval check; SFT examples may explain a message/template convention;
agent RL may expose a model to long tool trajectories. None proves that adding a planner
or deleting verification improves your workload. Hosting, quantization, parsers, tools,
prompts and task selection can explain the same observation. Undisclosed recipes stay
unknown; do not infer a brand's fixed personality from a few answers.

## Record a usable recommendation

Keep prose or a small table with: exact configuration, affected component, kind and rule
strength, source and date, observed issue, proposed change, smallest check, cost/risk,
counterevidence, and condition for retaining or retiring it. Explicitly label evidence:
**documented**, **locally observed**, **hypothesis**, **historical**, or **unverified**.
An official performance claim remains vendor-reported until reproduced.

Preserve opaque reasoning state as protocol material when required; do not decode it,
rewrite it as visible text or require hidden chain-of-thought for evaluation. User-facing
state, event evidence and provider reasoning state serve different consumers.

## Migrate without an invalid baseline

1. Freeze task semantics, authority, success evidence and environment. Record the old
   configuration and observable failure or migration objective. Distinguish premature
   stopping from excessive persistence; controls for one regime may harm the other.
2. Make the new target **protocol-valid first**: required API, templates, tool formats,
   history state, supported parameters and effective effort. Literal prompt preservation
   is conditional on both models accepting that representation.
3. Compare the closest legal baseline at comparable resources. Record unavoidable
   differences; identical parameter strings do not mean identical computation.
4. Change a relevant behavioral choice and run representative tasks. Repeat trials for
   stochastic quality or performance claims; include costs, false blocks and recovery.
5. Retain, adjust or retire that compensation based on the result. Re-test on upgrade;
   do not remove on upgrade. Keep useful historical evidence outside active defaults.

A missing-signature rejection followed by a valid request establishes a compatibility
fix, not an intelligence gain. Never construct a knowingly invalid baseline to make an
optimization win. Where access is unavailable, deliver documented guidance and a precise
unverified check; a Skill answer or mock test cannot prove target-model performance.

## A worked contrast: tool loop and recovery

The same read-only search goal has the same authority and completion evidence across
providers. Under the documented Astra API, tool calls use Responses and an async result
retains its `call_id`. Under DeepSeek V4 thinking with `tools`, subsequent requests
preserve prior `reasoning_content`, including turns without a tool call. Under stateful
Gemini Interactions, the server manages thought signatures through the continuation ID.
Do not normalize all three into a bare text transcript. Consult the linked profiles for
their dates, qualifications, current checks and alternative API modes.

For a long review, the goal, evidence pointers and pending operation record survive
outside the model context. Native continuation preserves valid provider state; a fresh
handoff starts from consolidated task evidence and does not pretend to restore that
state. Test this distinction at the adapter and at the final task outcome separately.
