# Research Basis

Accessed 2026-09-04. These sources support the Skill's distinctions; they are not a
checklist to copy wholesale. Provider behavior and plugin surfaces are versioned facts,
so verify them again when implementing against a newer host.

## How to use this file

Weigh sources by tier, and say which tier you are relying on.

- **Robust**: peer-reviewed or widely replicated; safe to reason from.
- **Preprint**: single-lab, sound method, not independently reproduced; cite as evidence,
  not as settled.
- **Vendor**: lab or company reporting on its own system, usually without a released
  dataset; strongest as existence proof of a mechanism, weakest as a general claim.

Numbers from a benchmark are claims about a grading function too. See
[evaluation-and-observability.md](evaluation-and-observability.md) before acting on one.

## Skill format and distribution

- [Agent Skills specification](https://agentskills.io/specification): standard
  `SKILL.md` structure, metadata constraints, and optional resources.
- [Agent Skills creator best practices](https://agentskills.io/skill-creation/best-practices):
  ground Skills in real expertise and execution traces; remove content that does not
  improve real use.
- [Agent Skills evaluation guide](https://agentskills.io/skill-creation/evaluating-skills):
  compare Skill and baseline arms across realistic repeated cases.
- [OpenAI Codex Skills](https://learn.chatgpt.com/docs/build-skills): progressive
  disclosure, discovery, explicit/implicit invocation, and Plugin distribution.
- [OpenAI Plugin architecture](https://developers.openai.com/plugins/concepts/plugins):
  Skills are sufficient when existing tools can execute the workflow; MCP is optional.
- [OpenAI Plugin packaging](https://developers.openai.com/plugins/build/plugins):
  `.codex-plugin/plugin.json` and installable package structure.
- [Claude Agent Skills best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices):
  concise core instructions, task-appropriate degrees of freedom, progressive
  disclosure, and eval-first iteration.
- [Claude Code Plugins](https://code.claude.com/docs/en/plugins): standalone Skills for
  local/project use and Plugins for versioned sharing.
- [OpenCode Agent Skills](https://opencode.ai/docs/skills): on-demand Skill loading and
  discovery from `.agents`, `.claude`, and OpenCode-native locations.

## The harness as a capability lever

- [SWE-agent](https://arxiv.org/abs/2405.15793) (robust): with the language model held
  fixed, a designed agent-computer interface more than doubled resolve rate over a raw
  shell. Interface design is a first-order lever.
- [Holistic Agent Leaderboard](https://arxiv.org/abs/2510.11977) (robust): scaffold and
  model interact; cost can differ ninefold for a two-point accuracy difference, and
  different model families rank differently under different scaffolds.
- [Stop Comparing LLM Agents Without Disclosing the Harness](https://arxiv.org/abs/2605.23950)
  (preprint): harness-induced variance can exceed model-induced variance, including
  reversals of model ranking.
- [Harness-Bench](https://arxiv.org/abs/2605.27922) (preprint): report capability at the
  model-harness configuration level; stronger backends show higher means and lower
  cross-harness variance, so scaffolding matters most for weaker models.
- [OpenAI, Introducing SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/)
  (vendor): the same model moved from 2.7% to 28.3% on one suite purely by scaffold, and
  most original samples were filtered as underspecified or unfairly tested.
- [OpenAI, MLE-bench](https://openai.com/index/mle-bench/) (vendor): one model, three
  scaffolds, an order-of-magnitude spread in medal rate; changing scaffold outperformed
  quadrupling wall-clock. Agents also ended runs far early.
- [Aider, unified diffs](https://aider.chat/docs/unified-diffs.html) and
  [edit-format leaderboard](https://aider.chat/docs/leaderboards/edit.html) (vendor):
  one fixed model moved from 20% to 61% on edit format alone, with laziness markers
  falling threefold. For other models the ordering between formats reverses.
- [ETH SRI, Evaluating AGENTS.md](https://www.sri.inf.ethz.ch/publications/gloaguen2026agentsmd)
  (robust): across several agents and benchmarks, repository context files produced no
  improvement in task success while adding over 20% inference cost, and model-generated
  ones reduced success in most settings. The counterweight to over-building.
- [LangChain, anatomy of an agent harness](https://www.langchain.com/blog/the-anatomy-of-an-agent-harness)
  and [improving deep agents](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering)
  (vendor): definition of harness as everything that is not the model; with the model
  fixed, harness changes moved a terminal benchmark by roughly fourteen points. Uniformly
  raising reasoning effort scored worse than a moderate setting.
- [Inside the Scaffold](https://arxiv.org/abs/2604.03515) (preprint): source-level
  taxonomy of coding-agent architectures; useful vocabulary for loop primitives.

## Harness practice from operators

- [Anthropic, Building effective agents](https://www.anthropic.com/engineering/building-effective-agents):
  simple composable patterns are a useful default; workflows and agents fit different
  task shapes.
- [Anthropic, Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents):
  tool ergonomics must be evaluated with agents; descriptions and response context
  affect outcomes.
- [Anthropic, Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents):
  compaction alone is not sufficient; external artifacts and verified incremental work
  support long-horizon recovery. Agents mark work done without testing it.
- [Anthropic, Harness design for long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps):
  every harness component encodes an assumption about what the model cannot do alone;
  stress-test those assumptions and remove one component at a time. Also records the
  counterweight — an unharnessed run was far cheaper and produced broken output.
- [Anthropic, Scaling Managed Agents](https://www.anthropic.com/engineering/managed-agents):
  harness assumptions go stale as models improve; a context-reset mechanism added for one
  model became dead weight on the next.
- [Anthropic, April 23 postmortem](https://www.anthropic.com/engineering/april-23-postmortem):
  three harness-layer changes with no model change. A prompt-level word cap cost a few
  percent of quality; a default reasoning-effort downgrade shipped for latency; and a
  context-clearing bug repeatedly cleared thinking, presenting as forgetfulness rather
  than as an error. Internal evals did not initially reproduce any of it.
- [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/):
  agent-legible repositories, tools, documentation, tests, and feedback loops can be
  higher leverage than prompt expansion; a short root map outperforms a monolithic
  always-on instruction manual.
- [OpenAI, Unrolling the Codex agent loop](https://openai.com/index/unrolling-the-codex-agent-loop/):
  context, tools, sandbox policy, compaction, and stable prompt structure jointly shape
  capability and efficiency, including prefix stability for caching.
- [OpenAI, Run long horizon tasks with Codex](https://developers.openai.com/blog/run-long-horizon-tasks-with-codex):
  real feedback, externalized state, steerability, and milestone verification sustain
  useful work over long runs.
- [OpenAI, Codex prompting guide](https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide):
  ships an explicit prohibition on broad catches, silent defaults, success-shaped
  fallbacks, and silent early returns. Also documents removing preamble and status-update
  scaffolding for newer models because it caused premature stopping.
- [Cursor, Continually improving our agent harness](https://cursor.com/blog/continually-improving-agent-harness):
  guardrails added for weaker models were largely removed as capability grew; models
  perform worse with an edit format they were not trained on; an exhaustive typed error
  taxonomy where any unknown error is treated as a harness bug.
- [Cursor, Cloud agent lessons](https://cursor.com/blog/cloud-agent-lessons):
  an incomplete environment shows up as a subtle drop in output quality rather than an
  error — the clearest statement of why degradation must be made visible deliberately.
- [Manus, Context engineering for AI agents](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus):
  stable prefixes for cache economics, masking rather than removing tools mid-run,
  restorable compression through the filesystem, and recitation of objectives.
- [Factory, Evaluating compression](https://factory.ai/news/evaluating-compression)
  (vendor): probe-based comparison over production sessions; artifact tracking is the
  weakest dimension for every implementation tested, and regenerating summaries from
  scratch each cycle is named as a source of silent drift.
- [Factory, Large software tasks](https://factory.ai/news/what-it-takes-for-coding-agents-to-complete-large-software-tasks)
  (vendor): agents stop with much of the outcome absent because they never established
  what remained; additional compute does not help an agent that will not spend it.
- [Factory, Model routing belongs in the harness](https://factory.ai/news/model-routing-belongs-in-the-harness)
  (vendor): switching model families can discard reusable reasoning state; per-model edit
  tooling and instructions.
- [Amp, Handoff](https://ampcode.com/news/handoff) (vendor): the dissenting position on
  compaction — what a summary retains is the agent's choice, and stacking summaries
  encourages unbounded threads. Replaces it with an explicit user-reviewable handoff.
- [Building Effective AI Coding Agents for the Terminal](https://arxiv.org/abs/2603.05344)
  (preprint): names agent-aware truncation hints, instruction fade-out in long sessions,
  doom-loop detection, and stale-read detection.
- [Magentic-One](https://arxiv.org/abs/2411.04468) (robust): a stall counter that forces
  outer-loop re-planning, plus an empirical failure taxonomy naming persistent
  inefficient actions and insufficient verification.

## Budgets, limits, and liveness

- [Anthropic, task budgets](https://platform.claude.com/docs/en/build-with-claude/task-budgets):
  the reference two-tier design. A soft countdown visible only to the model, alongside a
  hard output ceiling. Documents the failure mode of an undersized budget as
  refusal-like behavior and premature stopping, prescribes raising the budget before
  debugging anything else, warns against mirroring the countdown client-side, and sizes
  budgets from a high percentile of unbudgeted spend.
- [Claude Agent SDK agent loop](https://code.claude.com/docs/en/agent-sdk/agent-loop):
  typed terminal subtypes distinguishing success, turn limit, budget limit, execution
  error, and retry exhaustion, with the result field present only on success.
- [Claude Code tools reference](https://code.claude.com/docs/en/tools-reference):
  oversized command output is persisted and replaced by a preview and a path; timeouts
  are reported with an identifier rather than swallowed.
- [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works):
  refuses to auto-compact in a loop, surfacing an error instead.
- [OpenAI, trustworthy third-party evaluations](https://openai.com/index/trustworthy-third-party-evaluations-foundations/):
  avoidable under-elicitation is a measurement failure — a harness or budget that
  prevents behavior the system could produce means the score does not measure the claimed
  capability. Reports large continued gains from an order-of-magnitude budget increase,
  and a capability estimate halved after removing reward-hacked successes.
- [Cognition, Devin and Sonnet 4.5](https://cognition.com/blog/devin-sonnet-4-5-lessons-and-challenges)
  (vendor): a model that believed it was near its limit took shortcuts; the fix was to
  raise the apparent headroom. The visible value of a governor changes behavior.

## Context, compaction, and long horizon

- [Anthropic, Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents):
  context is a finite attention budget; find the smallest set of high-signal tokens.
- [Anthropic, context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing):
  a worked example of loud degradation — cleared results are replaced by placeholder text
  telling the model they were removed, with structured counts in the response. Also warns
  that per-model defaults differ and should be set explicitly.
- [Anthropic, compaction](https://platform.claude.com/docs/en/build-with-claude/compaction)
  and [memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool):
  content before a compaction block is ignored, so the summary is all the model has;
  persistent rules belong in a re-injected instruction file rather than in history; mark
  work complete only after end-to-end verification.
- [OpenAI, compaction guide](https://platform.openai.com/docs/guides/compaction):
  the returned window is canonical and must not be pruned; compact after milestones
  rather than every turn; keep prompts functionally identical when resuming to avoid
  behavior drift.
- [Chroma, Context Rot](https://www.trychroma.com/research/context-rot) (vendor):
  performance grows increasingly unreliable as input length grows, non-uniformly; even a
  single distractor hurts. Note its own findings carefully — see miscitations below.
- [NoLiMa](https://arxiv.org/abs/2502.05167) (robust) and
  [RULER](https://arxiv.org/abs/2404.06654) (robust): effective context is a fraction of
  advertised context once lexical overlap is removed or tasks get harder.
- [ATLAS](https://arxiv.org/abs/2605.28079) (preprint): model rankings reorder
  substantially between shorter and longer context regimes.
- [Lost in the Middle](https://arxiv.org/abs/2307.03172) (robust): position within the
  window matters; control where critical material lands.
- [LLMs Get Lost in Multi-Turn Conversation](https://arxiv.org/abs/2505.06120) (robust):
  a large average drop from single-turn to multi-turn, dominated by unreliability rather
  than ability; models commit early to a wrong reading and do not recover.
- [The Illusion of Diminishing Returns](https://arxiv.org/abs/2509.09677) (preprint):
  self-conditioning — per-step accuracy falls with step count, and visible prior errors
  raise later error rates. Reasoning modes reduce it in some models.
- [Vending-Bench](https://arxiv.org/abs/2502.15840) (preprint): long runs derail into
  unrecoverable loops without correlating with context exhaustion. A bigger window is not
  a coherence fix.
- [Classifier Context Rot](https://arxiv.org/abs/2605.12366) (preprint): monitors and
  classifiers themselves degrade with context length, missing relevant actions far more
  often late in long transcripts, partially mitigated by periodic reminders. Relevant to
  trajectory-level review, not a general agent-capability claim.
- [LoCoBench-Agent](https://arxiv.org/abs/2511.13998) (preprint): the dissenting result —
  agentic scaffolds that re-retrieve show strong long-context robustness.
- [Large Language Models Can Be Easily Distracted by Irrelevant Context](https://arxiv.org/abs/2302.00093)
  (robust): removing stale material beats deprioritizing it.
- [Recursive summarization](https://arxiv.org/abs/2308.15022) (preprint): summary errors
  compound across rounds.
- [StreamingLLM](https://arxiv.org/abs/2309.17453) and
  [Prompt Cache](https://arxiv.org/abs/2311.04934) (both robust): opening tokens are
  structurally load-bearing and must not be evicted; cached state is valid only at the
  same position, so prefix stability is a correctness and cost property.
- [RAG-MCP](https://arxiv.org/abs/2505.03275) (preprint): retrieving the tool space
  rather than enumerating it substantially improves selection accuracy and cuts tokens.
- [Anthropic, code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)
  (vendor): order-of-magnitude token reductions from on-demand retrieval of tool surfaces.
- [Large Language Models Cannot Self-Correct Reasoning Yet](https://arxiv.org/abs/2310.01798)
  (robust) with [Reflexion](https://arxiv.org/abs/2303.11366) (robust): self-critique
  without an external signal is unreliable; the positive results depend on environment
  feedback.
- [Truth Decay](https://arxiv.org/abs/2503.11656) (preprint): sycophancy compounds across
  turns; anchor decisions in durable state.
- [METR, long software tasks](https://arxiv.org/abs/2503.14499) (preprint): time-horizon
  framing for how long autonomous work can run before reliability falls.

## Silent failure and degradation

- [From Confident Closing to Silent Failure](https://arxiv.org/abs/2606.09863) (preprint,
  large-N, clean design): false success accounts for roughly 45-48% of failures in
  single-control tool-agent settings, and about 3% where an independent simulator can
  verify state. Model graders detect it near chance because they key on confident closing
  language; a cheap non-model detector performs far better. The single strongest argument
  for closing completion on the environment.
- [OpenAI, Codex prompting guide](https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide):
  the explicit no-silent-failures and no-success-shaped-fallback rules.
- [AI Incident Database, incident 1152](https://incidentdatabase.ai/cite/1152/): an agent
  executed destructive commands during a declared freeze, fabricated records, and
  incorrectly reported that rollback was impossible. Every layer that failed was soft: the
  freeze was an instruction rather than a gate, the destructive command had no
  execution-layer approval, and the agent's self-report about recovery was believed.
- [Anthropic, how we contain Claude](https://www.anthropic.com/engineering/how-we-contain-claude):
  supervise what the agent is able to do rather than what it does; model-layer protection
  cannot stand alone.
- [Claude Agent SDK subagents](https://code.claude.com/docs/en/agent-sdk/subagents):
  documents a silent capability loss directly — a tool left out is simply absent, with no
  prompt and no error — alongside loud, typed limit messages delivered as tool results.

## Trust, authority, and effects

- [tau-bench](https://arxiv.org/abs/2406.12045) (robust): evaluate realistic
  tool-agent-user interaction using final database state and repeated-trial reliability.
- [AgentDojo](https://arxiv.org/abs/2406.13352) (robust): dynamic tool environments show
  both utility failures and prompt-injection risk when untrusted tool data enters context.
- [Defeating Prompt Injections by Design](https://arxiv.org/abs/2503.18813) (preprint;
  the CaMeL system): separate trusted control and data flow and enforce capabilities
  outside the model. Supplies the field's clearest utility-tax number, roughly seven
  points of task completion for provable resistance.
- [Adaptive Attacks Break Defenses Against Indirect Prompt Injection](https://arxiv.org/abs/2503.00061)
  (robust): every evaluated defense exceeded half of attacks succeeding once the attacker
  optimized against it. Any defense number not measured adaptively is an upper bound.
- [Design Patterns for Securing LLM Agents against Prompt Injections](https://arxiv.org/abs/2506.08837)
  (preprint, multi-institution): six patterns whose guarantees hold only when followed
  exactly; falling back to a general loop for hard cases discards the property.
- [BIPIA](https://arxiv.org/abs/2312.14197) (robust): more capable models have been more
  susceptible to indirect injection, so a stronger model is not itself a mitigation.
- [AgentHarm](https://arxiv.org/abs/2410.09024) (robust): refusal training alone is
  insufficient; authority and effect gating must be independent of model judgment.
- [OpenAI, guardrails and approvals](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals.md):
  put validation next to the tool that creates the side effect; chain-level guardrails do
  not cover intermediate tool calls, and concurrent checks can land after effects.
- [OpenAI, sandboxing and auto-review](https://learn.chatgpt.com/docs/sandboxing):
  the sandbox defines technical boundaries and the approval policy decides when to stop
  and ask; changing who reviews must not enlarge what is permitted.
- [OpenAI, safety alignment for long-horizon models](https://openai.com/index/safety-alignment-long-horizon-models/):
  the regime inversion. Earlier models stopped at sandbox boundaries; a later one
  persisted and sought ways around them. Per-action monitoring no longer tracks the intent
  of a trajectory, since each step can look acceptable while the sequence produces an
  unapproved outcome.
- [OpenAI, model evaluation security incident](https://openai.com/index/hugging-face-model-evaluation-security-incident/):
  models under evaluation escaped the eval sandbox to obtain answers. Isolating eval
  artifacts from agent access is load-bearing harness design.
- [Model Context Protocol 2026-07-28](https://blog.modelcontextprotocol.io/posts/2026-07-28/):
  the current protocol release adds a stateless core, extensions, Tasks, and
  authorization hardening. MCP remains an optional integration surface and does not
  replace domain authorization or evidence design.
- [OWASP GenAI Security Project](https://genai.owasp.org/): current threat and control
  taxonomies for LLM and agentic applications. Taxonomy, not empirical evidence.

## Multi-agent

- [Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) (preprint,
  strong method): high failure rates across frameworks with an annotated taxonomy;
  targeted prompt fixes recovered little, indicating structural rather than prompt causes.
- [Capable language models can outgrow the benefits of collaboration](https://www.nature.com/articles/s42256-026-01268-y)
  (robust): single-agent baseline capability is the most robust predictor of whether
  coordination helps; parallel-decomposable tasks gain and sequential ones degrade.
- [Single-Agent LLMs Outperform Multi-Agent Systems Under Equal Thinking Token Budgets](https://arxiv.org/abs/2604.02460)
  (preprint): match budgets before attributing gains to architecture.
- [Anthropic, multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
  (vendor): reports a large gain over a single agent, and in the same post attributes most
  performance variance to token spend, with multi-agent runs using far more tokens. Quote
  both together or neither.
- [Cognition, Don't Build Multi-Agents](https://cognition.com/blog/dont-build-multi-agents)
  and [Multi-Agents: What's Actually Working](https://cognition.com/blog/multi-agents-working)
  (vendor): the reversal is partial. Writes stay single-threaded; other agents contribute
  analysis. A reviewer with no shared prior context is the case where isolation clearly
  helps.
- [Prompt Infection](https://arxiv.org/abs/2410.07283) (robust): malicious instructions
  can self-replicate across agents — a failure class single-agent systems lack by
  construction.

## Evaluation methodology

- [Establishing Best Practices for Building Rigorous Agentic Benchmarks](https://arxiv.org/abs/2507.02825)
  (robust, multi-institution): named grading defects in widely used suites, including
  insufficient tests and empty responses counted as successes, with reward-design bugs
  shifting reported performance by up to its own magnitude.
- [Are "Solved Issues" in SWE-bench Really Solved Correctly?](https://arxiv.org/abs/2503.15223)
  (preprint): a meaningful share of passing patches fail developer tests or differ
  behaviorally from the reference.
- [Do Agent Benchmarks Measure Capability?](https://arxiv.org/abs/2607.22368) (preprint):
  audits found reward hacking and answer exposure in a majority of traces on some suites.
- [Adding Error Bars to Evals](https://arxiv.org/abs/2411.00640) (robust): never act on a
  benchmark delta without a standard error.
- [Anthropic, infrastructure noise](https://www.anthropic.com/engineering/infrastructure-noise)
  (vendor): execution environment alone moved agent scores by several points; small
  leaderboard differences deserve skepticism until configuration is documented and matched.
- [LLM Evaluators Recognize and Favor Their Own Generations](https://arxiv.org/abs/2404.13076)
  (robust) and [Large Language Models are not Fair Evaluators](https://arxiv.org/abs/2305.17926)
  (robust): self-preference is causally tied to self-recognition, and verdicts can flip on
  candidate ordering. Do not use the same family as agent and judge.
- [AI Agents That Matter](https://arxiv.org/abs/2407.01502) (robust): report
  cost-accuracy frontiers and hold out cases; accuracy-only optimization produces costly
  agents.
- [OpenAI, expanding on sycophancy](https://openai.com/index/expanding-on-sycophancy/)
  (vendor): a regression shipped while offline evals looked healthy and qualitative
  reports were overruled; the committed remedy is to block launches on qualitative and
  proxy signals.
- [OpenAI, detecting and reducing scheming](https://openai.com/index/detecting-and-reducing-scheming-in-ai-models/)
  (vendor): a mitigation that removes a behavior and one that teaches concealment look
  identical from outside.
- [AutoSaddler](https://arxiv.org/abs/2608.23041) (preprint): targeted harness changes
  selected on held-out evaluation outperform unconstrained trace-specific edits. Not
  authority for automatic self-modification.
- [LongHorizon-Harness](https://arxiv.org/abs/2608.01964) (preprint): reports gains from
  external, environment-verified task state and independent audit.
- [AgentVisor](https://arxiv.org/abs/2604.24118) (preprint): effect mediation plus
  recoverable correction preserved more benign utility than terminal blocking.

## Commonly miscited

Check these before repeating a widely circulated claim.

- The multi-agent failure taxonomy at [arXiv:2503.13657](https://arxiv.org/abs/2503.13657)
  contains **no** "errors amplify 17x" statistic. That figure circulates in secondary
  write-ups and is not in the paper.
- [Chroma's Context Rot report](https://www.trychroma.com/research/context-rot) reports
  **no** position effect across the needle positions it tested, so it does not support
  lost-in-the-middle claims, and it states no overall degradation percentage in prose.
  Any "Chroma found X% degradation" figure is invented.
- [arXiv:2503.14499](https://arxiv.org/abs/2503.14499) was retitled in a later version to
  "Measuring AI Ability to Complete Long **Software** Tasks".
- [arXiv:2503.18813](https://arxiv.org/abs/2503.18813) is titled "Defeating Prompt
  Injections by Design"; CaMeL is the system, not the paper title.
- [arXiv:2605.12366](https://arxiv.org/abs/2605.12366) is about **classifier and monitor**
  degradation with context length, not general agent capability.
- The Nature Machine Intelligence article on coordination is titled "Capable language
  models can outgrow the benefits of **collaboration**".

## What the sources do not justify

They do not establish that every system needs a custom loop, multiple agents, a state
machine, MCP, persistent memory, human approval, a semantic grader, or draft/commit.
They also do not justify removing preventive controls until a failure occurs, nor
removing scaffolding merely because a newer model shipped. Those choices require
task-specific evidence, risk, and lifecycle validation.
