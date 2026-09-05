# Agent Harness Design

A provider-neutral Agent Skill for designing, auditing, debugging, and evaluating the
system around an AI agent: instructions, context, tools, permissions, state, recovery,
orchestration, evidence, and operational feedback loops.

The central idea is capability-preserving calibration: expose the selected model's
full authorized capability envelope, then enforce authority and external effects at
the narrowest trusted boundary. A sound harness distinguishes:

| Level | Meaning | Example |
|---|---|---|
| Invariant | A trust, authority, or evidence property that must hold | Retrieved text cannot grant new authority |
| Default | A strong starting point that may be overridden | Start with the host's native loop |
| Conditional pattern | Useful when named task properties justify it | Use multiple agents for genuinely separable work |
| Example | One implementation, not a rule | A planner-worker-verifier topology |

This avoids two common failures: under-building the trusted execution boundary, and
over-building a rigid workflow that prevents a capable model from solving the task.
It also makes every compensating constraint removable when a stronger model or host
feature makes that constraint obsolete.

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
- uncertainty remains visible when the system cannot establish the state of the world;
- denial of one effect does not cripple unrelated reasoning or safe alternatives;
- model, context, output, or tool capability is never reduced silently.

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

Use `--ref main` only when intentionally testing the moving development snapshot.
Release tags are the reproducible install boundary.

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
| Kimi | `~/.kimi-code/skills/agent-harness-design` |
| zCode | `~/.zcode/skills/agent-harness-design` |
| OpenCode | `~/.config/opencode/skills/agent-harness-design` |

Kimi Code user installs honor `KIMI_CODE_HOME` (default `~/.kimi-code`),
including the `skills` subdirectory. The legacy Python CLI directory `~/.kimi`
is not migrated or deleted. See [Kimi Skill discovery](https://www.kimi.com/code/docs/kimi-code-cli/customization/skills.html).

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

The main `SKILL.md` is a short decision procedure. It routes deeper work into six
references:

- how harness engineering differs from ordinary software;
- silent failure and silent degradation;
- design and architecture choices, including budgets and model portability;
- trust, tools, permissions, and effects;
- context, state, recovery, and orchestration;
- evaluation, observability, and the primary research basis.

## Evaluation

The standard-library runner is host-pluggable. `--host` selects an adapter that owns
every host-specific fact: binary and argv, per-run isolation, config injection, the user
skills directory, how the final message and token usage are captured, how structured
output is requested, and how a rate-limit error is recognized. `codex` and `zcode` are
implemented; `claude`, `hermes`, `kimi`, and `opencode` are named extension points. An
adapter refuses rather than degrades: a flag the host would silently ignore raises
instead, and the result file records the real host, CLI version, observed model, and
structured-output mechanism.

Every run uses a fresh temporary home and workspace, and never builds a shell command.
Behavior mode records final outputs, wall-clock duration, configuration, and
host-reported tokens per arm; optional blind grading records its semantic judgments
separately from those measurements, with arm identity hidden behind labels whose order
rotates per case.

```bash
python3 scripts/run_evals.py behavior \
  --host zcode --host-binary /path/to/zcode \
  --arm no_skill \
  --arm agent-harness-design-v030=/path/to/previous-release/skill \
  --arm agent-harness-design=plugins/agent-harness-design/skills/agent-harness-design \
  --trials 2 --workers 4 --grade \
  --output eval-results/v0.4.0-behavior.json
```

Trigger mode tests the host's real implicit discovery. It installs marker-only probe
Skills into each clean temporary home and observes which bodies were actually loaded;
the corpus includes positive, negative, ambiguous, and adjacent-Skill coexistence
cases.

```bash
python3 scripts/run_evals.py trigger \
  --host zcode --host-binary /path/to/zcode \
  --trials 2 --workers 4 \
  --output eval-results/v0.4.0-trigger.json
```

The corpus remains inside the Skill package so every installed copy carries the cases;
the runner and retained release evidence remain at repository level so portable Skill
installs do not acquire an execution dependency. Results are configuration-specific,
not claims about every model or host.

The v0.4.0 run completed 162/162 behavior answers and 54/54 blind grades on ZCode with
GLM-5.2. The candidate scored 3.796/4 against 3.685 for the previous release and 3.296
without a Skill. Paired against the previous release the difference is +0.111 with a 95%
interval of [-0.058, +0.280], so **v0.4.0 is not distinguishable from v0.3.0 on this
task distribution**; both Skill arms beat no Skill with intervals clear of zero.
Implicit discovery made 24/24 accepted selections, which measures ZCode and is not
comparable to the v0.3.0 figure measured on Codex. See the
[`v0.4.0 evaluation report`](reports/v0.4.0-evaluation.md) for the full deviation list
and retained raw evidence.

## Development

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/run_evals.py --help
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" \
  plugins/agent-harness-design/skills/agent-harness-design
```

CI runs the standard-library test suite on Linux, macOS, and Windows.

## Research basis

The guidance is grounded in the open Agent Skills specification, current Codex,
Claude Code, and OpenCode documentation, practitioner reports from OpenAI and
Anthropic, and agent reliability and security research including tau-bench,
AgentDojo, CaMeL, Harness-Bench, and recent capability-preserving defense work. The
annotated list and the claims drawn from it live in
[`references/research-basis.md`](plugins/agent-harness-design/skills/agent-harness-design/references/research-basis.md).
