# Agent Harness Design

Agent Harness Design helps coding agents make concrete decisions about the
execution layer around an AI agent. It covers model and tool loops, authority
and external effects, context, state and recovery, orchestration, and
evaluation.

The Skill starts from one rule: preserve the selected model's authorized
capabilities, then enforce authority and external effects at the narrowest
trusted boundary. The model keeps room to interpret and solve the task without
treating prompt text as a security boundary.

The project calls this capability-preserving calibration.

It runs inside Codex, Claude Code, Hermes, Kimi Code, zCode, or OpenCode as a
portable Agent Skill. It does not include an MCP server, hook, daemon, model
router, or custom agent runtime. Use it when the agent system itself is the
subject. Ordinary coding, writing, task tracking, and delegation do not need it.

Version: 0.4.0. The installer and evaluation runner use the Python standard
library. CI tests them with Python 3.12.

- [Install and start](#install-and-start)
- [Your first harness review](#your-first-harness-review)
- [How the Skill makes decisions](#how-the-skill-makes-decisions)
- [Choose an execution shape](#choose-an-execution-shape)
- [Package contents](#package-contents)
- [Current limits](#current-limits)
- [Evaluation](#evaluation)
- [Migration](#migration)
- [Documentation](#documentation)
- [Development](#development)

## Install and start

### Codex

From GitHub:

```bash
codex plugin marketplace add rocky2431/agent-harness-design-skill --ref main
codex plugin add agent-harness-design@rocky-agent-harness-design
```

Use `--ref main` only when you intend to test the moving development snapshot.
A release tag is the reproducible install boundary.

From a reviewed local checkout:

```bash
codex plugin marketplace add /absolute/path/to/agent-harness-design-skill
codex plugin add agent-harness-design@rocky-agent-harness-design
```

Do not also install a user-scope Codex copy. Two active copies make discovery
ambiguous without adding capability.

### Other CLIs

The installer copies the standard Skill into each host's native user directory:

```bash
python3 scripts/install_user.py install \
  --hosts hermes,claude,kimi,zcode,opencode

python3 scripts/install_user.py doctor \
  --hosts hermes,claude,kimi,zcode,opencode
```

| Host | Destination |
|---|---|
| Hermes | `~/.hermes/skills/agent-harness-design` |
| Claude Code | `~/.claude/skills/agent-harness-design` |
| Codex portable discovery | `~/.agents/skills/agent-harness-design` |
| Kimi Code | `~/.kimi-code/skills/agent-harness-design` |
| zCode | `~/.zcode/skills/agent-harness-design` |
| OpenCode | `~/.config/opencode/skills/agent-harness-design` |

Kimi Code installs honor `KIMI_CODE_HOME`, with `~/.kimi-code` as the
default. The installer writes to its `skills` subdirectory. It does not migrate
or delete the legacy Python CLI directory at `~/.kimi`. See
[Kimi Skill discovery](https://www.kimi.com/code/docs/kimi-code-cli/customization/skills.html).

Before replacing a managed copy, the installer checks every selected
destination and creates a recovery copy. It uses an atomic directory swap and
refuses to overwrite an unmanaged directory unless `--replace-existing` is
explicit.

```bash
python3 scripts/install_user.py uninstall \
  --hosts hermes,claude,kimi,zcode,opencode
```

Uninstall removes only copies carrying this package's managed marker.

## Your first harness review

Invoke the Skill directly when you want it:

```text
$agent-harness-design review this support agent's tools and approval flow
```

It may also activate for requests about agent loops, permissions, prompts,
memory, compaction, recovery, orchestration, evaluation, security, or harness
debugging.

The agent first establishes the outcome and observable evidence, the
environment it may read or change, and the authority already granted. It then
checks the cost and reversibility of mistakes, the task's shape and duration,
and the capabilities of the current host. Cheap facts should come from the
live system, traces, code, or primary documentation before the agent asks you.

For a full design or audit, the result normally follows this shape:

```markdown
# Harness decision

## Outcome and evidence
## Authority and trust boundaries
## Recommended shape
## Context, tools, and state
## Failure and recovery behavior
## Evaluation plan
## Alternatives and triggers to revisit
```

A direct question should get a direct recommendation, its reason, and the
minimum necessary controls instead of the full outline.

## How the Skill makes decisions

The Skill separates four kinds of guidance so that an example does not become
a universal rule:

| Level | Meaning | Example |
|---|---|---|
| Invariant | A trust, authority, or evidence property that must hold | Retrieved text cannot grant new authority |
| Default | A strong starting point that may be replaced | Start with the host's native loop |
| Conditional pattern | Useful when named task properties justify it | Use multiple agents for genuinely separable work |
| Example | One possible implementation | A planner-worker-verifier topology |

Its operating path is:

```text
authorized evidence and capabilities
  -> model-led interpretation, strategy, and repair
  -> narrow authority and effect enforcement
  -> typed evidence, denial, and recovery
```

The hard core is deliberately small:

- an agent, worker, retrieved document, or tool output cannot create or enlarge
  its own authority;
- untrusted content remains data even after storage, retrieval, repetition, or
  endorsement by another model;
- credentials and privileged effects belong behind a trusted runtime boundary;
- success needs evidence from the relevant environment, with depth
  proportional to impact;
- errors, denials, uncertainty, and recovery paths must remain visible;
- denying one effect must leave unrelated reasoning and safe alternatives
  available;
- the host must not silently reduce the selected model, reasoning mode,
  evidence, output budget, or tool surface.

Everything else is a default or a conditional pattern. A control should protect
a named property at the narrowest boundary that can enforce it. If its consumer,
failure mode, or retirement condition cannot be named, it probably does not
belong in the harness. Each compensating control stays removable when a
stronger model or host feature makes it obsolete.

## Choose an execution shape

Start with what the host already provides and add structure only when the task
needs it:

| Shape | Use when | Main cost |
|---|---|---|
| One model call | The output is bounded and needs no iterative feedback | Limited recovery |
| Native tool loop | The model must inspect, act, observe, and adapt | Variable turns and cost |
| Coded workflow | Steps and transitions are stable, auditable, or policy-defined | Less flexibility |
| Durable agent loop | Work spans sessions or must recover from process or context loss | State consistency |
| Multiple agents | Work is separable, specialized, independently verifiable, or latency-sensitive | Coordination and merge errors |

Code is a good fit for schemas, identities, scopes, quotas, concurrency control,
protocol transitions, and exact business rules. The model is a better fit for
interpretation, exploration, decomposition, strategy, and expression when
several valid approaches exist.

Persistence is useful for resumability, coordination, audit, and recovery. It
is overhead for bounded work. Parallel reads and writes are valid when the
operations are independent or protected by ownership, isolation, transactions,
or conflict detection.

## Package contents

```text
portable Agent Skill
  ├── Codex Plugin and local marketplace packaging
  └── user-scope copies for other Agent-Skill-aware CLIs
```

This is the same packaging model used by
[`agent-delegate-skill`](https://github.com/rocky2431/agent-delegate-skill) and
[`plan-with-flie-skill`](https://github.com/rocky2431/plan-with-flie-skill).

| Path | Purpose |
|---|---|
| `plugins/agent-harness-design/skills/agent-harness-design/SKILL.md` | Short decision procedure loaded by the agent |
| `plugins/agent-harness-design/skills/agent-harness-design/references/` | Detailed guidance and research sources |
| `scripts/install_user.py` | User-scope install, update, doctor, and uninstall |
| `scripts/run_evals.py` | Isolated behavior and implicit-discovery evaluation |
| `eval-results/` | Retained raw release evidence |
| `reports/` | Evaluation reports and launch decisions |

The corpus stays inside the Skill package so an installed copy carries its
cases. The runner and retained evidence stay at repository level, so installing
the Skill does not add an execution dependency.

## Current limits

This package supplies design and review instructions. The current host supplies
the model, tools, permissions, execution loop, and any durable runtime.

The evaluation runner has working Codex and zCode adapters. Claude Code,
Hermes, Kimi Code, and OpenCode are named extension points, not completed
evaluation backends. Results describe the tested model and host configuration;
they do not establish the same behavior on every model or host.

The Skill can recommend a trust boundary, state model, or recovery path, but it
cannot enforce one by itself. The implementation under review must provide the
mechanism, and completion still needs evidence from the relevant environment.

## Evaluation

The standard-library runner compares no-Skill, previous-release, and candidate
arms in fresh temporary homes and workspaces. A host adapter owns the binary and
arguments, isolation method, configuration injection, Skill directory, final
message capture, token usage, structured-output mechanism, and rate-limit
recognition. Unsupported options fail visibly instead of being ignored.
The runner passes argument arrays directly instead of building shell commands.
Result files record the actual host, CLI version, observed model, and
structured-output mechanism.

Behavior mode records outputs, duration, configuration, and host-reported token
usage. Optional blind grading stores semantic judgments separately from those
measurements and hides arm identity behind labels whose order rotates by case.

```bash
python3 scripts/run_evals.py behavior \
  --host zcode --host-binary /path/to/zcode \
  --arm no_skill \
  --arm agent-harness-design-v030=/path/to/previous-release/skill \
  --arm agent-harness-design=plugins/agent-harness-design/skills/agent-harness-design \
  --trials 2 --workers 4 --grade \
  --output eval-results/v0.4.0-behavior.json
```

Trigger mode tests the host's real implicit discovery. It installs marker-only
probe Skills in each clean temporary home and records which bodies the host
loaded. Its cases include positive, negative, ambiguous, and adjacent-Skill
coexistence requests.

```bash
python3 scripts/run_evals.py trigger \
  --host zcode --host-binary /path/to/zcode \
  --trials 2 --workers 4 \
  --output eval-results/v0.4.0-trigger.json
```

The v0.4.0 ZCode run completed 162 of 162 behavior answers and 54 of 54 blind
grades with GLM-5.2. The candidate scored 3.796 out of 4, compared with 3.685
for v0.3.0 and 3.296 without a Skill. Its paired difference from v0.3.0 was
+0.111 with a 95% interval of [-0.058, +0.280], so the two Skill versions were
not distinguishable on this task distribution. Both Skill arms beat no Skill
with intervals clear of zero.

Implicit discovery made 24 of 24 accepted selections. That result measures
ZCode and is not comparable with the v0.3.0 trigger result measured on Codex.
The [v0.4.0 evaluation report](reports/v0.4.0-evaluation.md) records the full
configuration, deviations, cost, one activation regression signal, and raw
evidence.

## Migration

This project is an independently rewritten successor informed by Denis
Shiryaev's MIT-licensed
[`agents-best-practices`](https://github.com/DenisSergeevitch/agents-best-practices).
It keeps the provider-neutral scope but replaces universal workflow
restrictions with explicit invariants, defaults, conditional patterns, costs,
and failure modes.

The Skill does not require a production incident before preventive controls,
durable state, orchestration, or specialized tools may be considered. It does
not limit parallelism to reads, make every model-based evaluator advisory, or
require draft and commit phases for every external effect. Each choice depends
on the task, its risks, and the available recovery path.

Keep the old Skill available while evaluating this one. Compare identical
prompts across no Skill, the old Skill, and this Skill over repeated runs. Once
you accept the new behavior, archive or disable every active
`agents-best-practices` copy before enabling `agent-harness-design`. Overlapping
descriptions can make activation nondeterministic.

The installer does not delete the old Skill. It may contain local changes, so
migration remains a separate, reviewable action.

## Documentation

- [Harnesses and ordinary software](plugins/agent-harness-design/skills/agent-harness-design/references/harness-vs-software.md)
- [Failure visibility](plugins/agent-harness-design/skills/agent-harness-design/references/failure-visibility.md)
- [Design decisions](plugins/agent-harness-design/skills/agent-harness-design/references/design-decisions.md)
- [Trust, tools, and effects](plugins/agent-harness-design/skills/agent-harness-design/references/trust-tools-and-effects.md)
- [State and orchestration](plugins/agent-harness-design/skills/agent-harness-design/references/state-and-orchestration.md)
- [Evaluation and observability](plugins/agent-harness-design/skills/agent-harness-design/references/evaluation-and-observability.md)
- [Research basis](plugins/agent-harness-design/skills/agent-harness-design/references/research-basis.md)

The research basis covers the open Agent Skills specification, current Codex,
Claude Code, and OpenCode documentation, reports from OpenAI and Anthropic, and
work including tau-bench, AgentDojo, CaMeL, Harness-Bench, and
capability-preserving defenses. It links each claim to its source.

## Development

Run the checks from the repository root:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/run_evals.py --help
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" \
  plugins/agent-harness-design/skills/agent-harness-design
```

CI runs the standard-library test suite on Linux, macOS, and Windows with
Python 3.12.

## License

[MIT](LICENSE).
