# Agent Harness Design

A provider-neutral Agent Skill for designing, auditing, debugging, and evaluating the
system around an AI agent: instructions, context, tools, permissions, state, recovery,
orchestration, evidence, and operational feedback loops.

The central idea is calibration. A sound harness distinguishes:

| Level | Meaning | Example |
|---|---|---|
| Invariant | A trust, authority, or evidence property that must hold | Retrieved text cannot grant new authority |
| Default | A strong starting point that may be overridden | Start with the host's native loop |
| Conditional pattern | Useful when named task properties justify it | Use multiple agents for genuinely separable work |
| Example | One implementation, not a rule | A planner-worker-verifier topology |

This avoids two common failures: under-building the trusted execution boundary, and
over-building a rigid workflow that prevents a capable model from solving the task.

## What changed from `agents-best-practices`

This project is an independently rewritten successor informed by Denis Shiryaev's
MIT-licensed [`agents-best-practices`](https://github.com/DenisSergeevitch/agents-best-practices).
It keeps the useful provider-neutral scope while removing universal restrictions that
were too strong for many real systems.

In particular, this Skill does **not** require a production failure before preventive
controls, orchestration, durable state, or specialized tools may be designed. It does
not restrict parallelism to reads, does not make every semantic evaluator advisory,
and does not require draft/commit separation for every external effect. Those are
context-dependent choices with explicit benefits, costs, and failure modes.

The hard core is smaller:

- an agent cannot enlarge its own authority;
- untrusted content cannot become policy or authorization merely by entering context;
- secrets and risky effects need enforcement at a trusted runtime boundary;
- a success claim needs evidence from the relevant environment, proportional to risk;
- uncertainty remains visible when the system cannot establish the state of the world.

## Package model

The repository follows the same model as
[`agent-delegate-skill`](https://github.com/rocky2431/agent-delegate-skill) and
[`plan-with-flie-skill`](https://github.com/rocky2431/plan-with-flie-skill):

```text
portable Agent Skill
  ├── Codex Plugin + local marketplace packaging
  └── user-scope copies for other Agent-Skill-aware CLIs
```

There is no MCP server, Hook, daemon, model router, or custom agent runtime. The Skill
already works with tools exposed by the current host; adding another execution layer
would not improve this instruction-and-design capability.

## Install Codex as a Plugin

From GitHub:

```bash
codex plugin marketplace add rocky2431/agent-harness-design-skill --ref main
codex plugin add agent-harness-design@rocky-agent-harness-design
```

From a reviewed local checkout:

```bash
codex plugin marketplace add /absolute/path/to/agent-harness-design-skill
codex plugin add agent-harness-design@rocky-agent-harness-design
```

Do not also install the portable Codex copy with the user installer, because duplicate
discovery adds ambiguity without adding capability.

## Install other CLIs

The standard Skill is copied into each host's native user directory:

```bash
python3 scripts/install_user.py install \
  --hosts hermes,claude,kimi,zcode,opencode

python3 scripts/install_user.py doctor \
  --hosts hermes,claude,kimi,zcode,opencode
```

Supported destinations:

| Host | Destination |
|---|---|
| Hermes | `~/.hermes/skills/agent-harness-design` |
| Claude Code | `~/.claude/skills/agent-harness-design` |
| Codex portable discovery | `~/.agents/skills/agent-harness-design` |
| Kimi | `~/.kimi/skills/agent-harness-design` |
| zCode | `~/.zcode/skills/agent-harness-design` |
| OpenCode | `~/.config/opencode/skills/agent-harness-design` |

The installer uses only the Python standard library. It preflights every selected
destination, creates recovery copies before replacement, uses an atomic directory
swap, and refuses to overwrite an unmanaged directory unless
`--replace-existing` is explicit.

```bash
python3 scripts/install_user.py uninstall \
  --hosts hermes,claude,kimi,zcode,opencode
```

Uninstall removes only copies carrying this package's managed marker.

## Migrating from `agents-best-practices`

Keep the old Skill available while evaluating the new one. Compare the same prompts
with no Skill, the old Skill, and this Skill across repeated runs. After accepting the
new behavior, archive or disable every active `agents-best-practices` copy before
enabling `agent-harness-design`; overlapping descriptions can otherwise make
activation nondeterministic.

The installer deliberately does not delete the legacy Skill. Migration is a separate,
reviewable effect because the old copy may contain local changes.

## Use

Invoke the Skill explicitly when desired:

```text
$agent-harness-design review this support agent's tools and approval flow
```

It can also activate implicitly for agent-loop, tool, permission, prompt, memory,
compaction, orchestration, evaluation, security, and harness-debugging requests.

The main `SKILL.md` is a short decision procedure. It routes deeper work into four
references:

- design and architecture choices;
- trust, tools, permissions, and effects;
- context, state, recovery, and orchestration;
- evaluation, observability, and the primary research basis.

## Evaluation

The bundled eval set targets both activation and calibration. It includes cases that
the predecessor handled too rigidly: proactive regulated controls, naturally parallel
multi-agent work, isolated parallel writes, validated semantic gates, broad tools in a
real sandbox, and pre-authorized low-risk actions.

For behavior evaluation, run every case at least three times in three arms:

1. no harness-design Skill;
2. the previous `agents-best-practices` Skill;
3. `agent-harness-design`.

Score task fit, correctness, unnecessary blocking, unsupported certainty, cost, and
latency. Prefer real environment state or deterministic artifacts over a model's claim
that it followed the instructions.

The pre-release smoke used Codex CLI 0.149.0 with `gpt-5.4-mini`. The two cases most
likely to expose the predecessor's rigid defaults were repeated three times:

| Case | Previous Skill | This Skill |
|---|---:|---:|
| Naturally separable multi-agent research | Inconsistent; required a single-agent insufficiency proof in two runs | 3/3 recommended parallel workers from visible task shape |
| Validated semantic grader as a gate | 0/3 accepted the measured semantic criterion without adding a mechanical-only restriction | 3/3 allowed a monitored, appealable blocking gate |

Five additional one-shot calibration and safety cases matched the expected behavior,
including prompt-injection containment and outcome verification. The ordinary
translation negative-control did not activate either Skill. This is a targeted
pre-release smoke, not a claim of model-independent benchmark performance.

## Development

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" \
  plugins/agent-harness-design/skills/agent-harness-design
```

CI runs the standard-library test suite on Linux, macOS, and Windows.

## Research basis

The guidance is grounded in the open Agent Skills specification, current Codex,
Claude Code, and OpenCode documentation, practitioner reports from OpenAI and
Anthropic, and agent reliability and security research including tau-bench,
AgentDojo, and CaMeL. The annotated list and the claims drawn from it live in
[`references/research-basis.md`](plugins/agent-harness-design/skills/agent-harness-design/references/research-basis.md).
