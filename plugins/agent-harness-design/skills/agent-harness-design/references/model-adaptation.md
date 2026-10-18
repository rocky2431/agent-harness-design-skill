# Model Adaptation

Use for named targets, provider/API issues, migrations or suspected model compensations.
General responsibilities live in [architecture-guide.md](architecture-guide.md); adapt their realization here.

## Select the target configuration

The consulting model and the target system's model may differ. Resolve what matters
from code, configuration, request traces and primary documentation:

- exact model ID or snapshot, provider, endpoint and region where relevant;
- API surface, SDK/adapter and host version, including local serving template/parser;
- reasoning/thinking mode, effective effort and sampling settings;
- tool surface, multimodal inputs, context/recovery method and task distribution;
- observation date and whether the identity is pinned or a moving alias.

Do not invent missing values. Give general guidance and name only missing facts that
block parameter advice. A family match is a navigation hint, not verified compatibility.
Verify aliases and current contracts live before deployment. Profiles are dated
snapshots, not a router or exhaustive support matrix.

| Profile | Documented coverage and reason to read |
|---|---|
| [OpenAI](models/openai.md) | GPT-6.1 Sol and Astra, Responses, Codex effort/fan-out and approval review |
| [Anthropic](models/anthropic.md) | Opus/Sonnet/Haiku 5.5 and Fable 5.1, prompting, Claude Code, history and advisors |
| [xAI](models/xai.md) | Grok 4.7, Grok Build permissions, sandbox, headless sessions and subagents |
| [Google](models/google.md) | Gemini 3, temperature recommendation, stateful vs manual thought-state handling |
| [DeepSeek](models/deepseek.md) | V4 Pro/Flash thinking, effective effort mapping, history with/without tools; historical R1 |
| [Moonshot](models/moonshot.md) | K3, K2.7 Code and K2.6 differences in thinking controls and preservation |
| [Z.ai](models/z-ai.md) | GLM-5.3/5.2 and endpoint-specific Preserved Thinking |
| [Qwen](models/qwen.md) | Historical Qwen3/Coder training and protocol; limits of current Qwen3.8 evidence |

Read only the matching profile and relevant common component. If none matches, inspect
the target's current primary documentation rather than borrowing a nearby model's rules.

## Untangle claims when needed

| Kind | What it establishes | Useful evidence and validation |
|---|---|---|
| Interface contract | What a specific API accepts, requires, ignores, or maps | Current provider contract plus a targeted request/response or adapter check |
| Behavioral recommendation | A prompt, tool format or orchestration choice that may improve a task | Named model/task conditions; compare legal baseline and candidate on real tasks |
| Training background | Published pretraining, SFT, RL, distillation or agent-environment exposure | Original model report; distinguish disclosed facts from missing details |
| Historical case / hypothesis | Why a mechanism was tried, retained or replaced | Dated conditions and counterevidence; no automatic current recommendation |

Use these distinctions when claims are conflated, not as an output template. They are
independent of invariant, default, conditional pattern and example.
A protocol requirement may be mandatory in one adapter but irrelevant elsewhere.
A general architectural capability such as persistence may be optional for a short task.

Training suggests hypotheses, not scaffold benefits. Hosting, quantization, parsers,
tools, prompts and task selection may explain results. Keep undisclosed recipes unknown.

## Record a usable recommendation

Use a short paragraph or table: **configuration, proposed change, evidence label,
smallest check**. Include source/date for changing model claims; add cost, risk,
counterevidence or retirement conditions only when they change the decision. Label
evidence where it matters, rather than every sentence. Vendor performance claims remain
vendor-reported until reproduced.

Before behavioral changes, re-check the vendor prompting guide linked in the profile;
keep contracts and dated measurements separate.

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
5. Re-test on upgrade, then retire compensations the new model no longer needs. Record
   the reason in [historical-cases.md](historical-cases.md); adjust or retain those still
   supported by the result.

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
