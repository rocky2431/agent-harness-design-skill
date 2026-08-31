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
codex plugin marketplace add rocky2431/agent-harness-design-skill --ref v0.3.0
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

The standard-library runner creates a fresh temporary `HOME`, `CODEX_HOME`, workspace,
and ephemeral Codex session for every run. It never builds a shell command. Behavior
mode records final outputs, wall-clock duration, configuration, and Codex-reported
tokens for no-Skill, legacy, and candidate arms; optional blind grading records its
semantic judgments separately from those measurements.

```bash
python3 scripts/run_evals.py behavior \
  --arm no_skill \
  --arm agents-best-practices=/absolute/path/to/legacy-skill \
  --arm agent-harness-design=plugins/agent-harness-design/skills/agent-harness-design \
  --trials 2 --workers 4 --grade \
  --output eval-results/v0.3.0-behavior.json
```

Trigger mode tests the host's real implicit discovery. It installs marker-only probe
Skills into each clean temporary home and observes which bodies were actually loaded;
the corpus includes positive, negative, ambiguous, and adjacent-Skill coexistence
cases.

```bash
python3 scripts/run_evals.py trigger \
  --trials 2 --workers 4 \
  --output eval-results/v0.3.0-trigger.json
```

The corpus remains inside the Skill package so every installed copy carries the cases;
the runner and retained release evidence remain at repository level so portable Skill
installs do not acquire an execution dependency. Results are configuration-specific,
not claims about every model or host.

The v0.3.0 run completed 114/114 behavior answers and 38/38 blind grades. The candidate
scored 3.684/4 with a 97.4% graded pass rate, versus 3.526/94.7% for the predecessor and
3.395/92.1% without a Skill. Implicit discovery made 20/24 exact accepted selections,
including 8/8 negative or ambiguous non-activations; positive recall was 7/10 and is a
known stochastic limitation. See the
[`v0.3.0 evaluation report`](reports/v0.3.0-evaluation.md) and retained raw evidence.

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
