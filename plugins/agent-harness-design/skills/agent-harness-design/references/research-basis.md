# Research Basis

Accessed 2026-08-31. These sources support the Skill's distinctions; they are not a
checklist to copy wholesale. Provider behavior and plugin surfaces are versioned facts,
so verify them again when implementing against a newer host.

## Skill format and distribution

- [Agent Skills specification](https://agentskills.io/specification): standard
  `SKILL.md` structure, metadata constraints, and optional resources.
- [Agent Skills creator best practices](https://agentskills.io/skill-creation/best-practices):
  ground Skills in real expertise and execution traces; remove content that does not
  improve real use.
- [Agent Skills evaluation guide](https://agentskills.io/skill-creation/evaluating-skills):
  compare Skill and baseline arms across realistic repeated cases.
- [OpenAI Codex Skills](https://developers.openai.com/codex/skills): progressive
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

## Harness and tool practice

- [Anthropic, Building effective agents](https://www.anthropic.com/research/building-effective-agents):
  simple composable patterns are a useful default; workflows and agents fit different
  task shapes.
- [Anthropic, Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents):
  tool ergonomics must be evaluated with agents; descriptions, response context, and
  token efficiency affect outcomes.
- [Anthropic, Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents):
  compaction alone can lose progress; external artifacts and verified incremental work
  help long-horizon recovery.
- [Anthropic, Scaling Managed Agents](https://www.anthropic.com/engineering/managed-agents):
  harness assumptions can become stale as models improve; keep stable interfaces and
  question compensating mechanisms.
- [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/):
  agent-legible repositories, tools, documentation, tests, and feedback loops can be
  higher leverage than prompt expansion; a short root map outperforms a monolithic
  always-on instruction manual.
- [OpenAI, Unrolling the Codex agent loop](https://openai.com/index/unrolling-the-codex-agent-loop/):
  context, tools, sandbox policy, compaction, and stable prompt structure jointly shape
  the capability and efficiency of the running agent.
- [OpenAI, Run long horizon tasks with Codex](https://developers.openai.com/blog/run-long-horizon-tasks-with-codex):
  real feedback, externalized state, steerability, and milestone verification sustain
  useful work over long runs.
- [Anthropic, Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents):
  context is a finite attention budget; start from a capable model and add instructions
  against observed failure modes instead of hard-coding brittle behavior.
- [Cursor, Continually improving our agent harness](https://cursor.com/blog/continually-improving-agent-harness):
  old static context and guardrails can become harmful as models improve, while
  model-native prompts and edit tools can preserve more capability.
- [Cursor, Cloud agent lessons](https://cursor.com/blog/cloud-agent-lessons):
  full environments, durable execution, and knowing when to remove deterministic
  harness logic are central to long-running agent quality.
- [Manus, Context engineering for AI agents](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus):
  stable context, recoverable filesystem artifacts, and deliberate tool exposure can
  preserve both agent coherence and production efficiency.
- [Cognition, Multi-agents: what's actually working](https://cognition.com/blog/multi-agents-working):
  increased model capability changed an earlier broad warning into a narrower pattern:
  shared intelligence can help while conflicting parallel writes remain costly.
- [Model Context Protocol 2026-07-28](https://blog.modelcontextprotocol.io/posts/2026-07-28/):
  the current protocol release adds a stateless core, extensions, Tasks, and
  authorization hardening. MCP remains an optional integration surface and does not
  replace domain authorization or evidence design.

## Reliability, security, and architecture evidence

- [tau-bench](https://arxiv.org/abs/2406.12045): evaluate realistic tool-agent-user
  interaction using final database state and repeated-trial reliability (`pass^k`).
- [AgentDojo](https://arxiv.org/abs/2406.13352): dynamic tool environments show both
  utility failures and prompt-injection risk when untrusted tool data enters context.
- [CaMeL](https://arxiv.org/abs/2503.18813): separate trusted control/data flow and
  enforce capability policies outside the model; stronger security can trade utility.
- [Harness-Bench](https://arxiv.org/abs/2605.27922): agent performance varies by
  model-harness pairing; evaluate execution alignment, evidence, cost, and failure
  behavior rather than attributing results to the base model alone.
- [AgentVisor](https://arxiv.org/abs/2604.24118): recent evidence that effect mediation
  plus recoverable correction can preserve more benign utility than terminal blocking.
  Treat its reported results as a preprint, not a universal architecture.
- [OWASP GenAI Security Project](https://genai.owasp.org/): current threat and control
  guidance for LLM and agentic applications, including prompt injection and excessive
  agency.
- [Capable language models can outgrow the benefits of multi-agent systems](https://www.nature.com/articles/s42256-026-01268-y):
  multi-agent gains depend on task, coordination, and single-agent capability; parallel
  structure can help while sequential or tool-heavy work can degrade.

## Emerging evidence, not hard rules

- [LongHorizon-Harness](https://arxiv.org/abs/2608.01964): reports gains from external,
  environment-verified task state and independent audit on several long-horizon
  benchmarks. Treat as a recent preprint requiring reproduction before adoption.
- [AutoSaddler](https://arxiv.org/abs/2608.23041): reports that targeted harness changes
  selected on held-out evaluation outperform unconstrained trace-specific edits. Treat
  as an emerging optimization result, not authority for automatic self-modification.

## What the sources do not justify

They do not establish that every system needs a custom loop, multiple agents, a state
machine, MCP, persistent memory, human approval, a semantic grader, or draft/commit.
They also do not justify removing preventive controls until a failure occurs. Those
choices require task-specific evidence, risk, and lifecycle validation.
