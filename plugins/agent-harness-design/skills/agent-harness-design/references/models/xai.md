# xAI: Grok 4.7 and Grok Build

Status: official documentation checked 2026-10-18 except owner-researched items
explicitly marked below. Target: `grok-4.7`, xAI API at `https://api.x.ai/v1` or
Grok Build CLI/ACP. Resolve host version, endpoint, effort, permission mode and OS.
Local target-system compatibility and optimization trials: unverified.

## Model contract and dated vendor claims

[Released 2026-09-21](https://x.ai/news/grok-4-7), Grok 4.7 has a
[500,000-token context](https://docs.x.ai/developers/models/grok-4.7), standard API
prices of $2 input/$6 output per million tokens, and effort levels `low`, `medium`,
`high` (default), `xhigh`. Long-context pricing differs above 200K; check the rate
for the actual request. Coding benchmark scores are vendor claims, not local evidence.

The [developer guide](https://docs.x.ai/developers/grok-4-7) should be re-checked before
behavioral advice, together with the current [best practices](https://docs.x.ai/developers/model-capabilities/text/best-practices).
Training descriptions do not establish the benefit of a scaffold for your workload.

The developer guide confirms Grok 4.7 Fast is the same model on faster infrastructure,
at 2x token rates and 1.5x for long context, only in Cursor and Grok Build, outside
the public API and Build free tier. The exact ID `grok-4.7-build-fast` is checked by
the owner's 2026-10-18 research, not independently re-confirmed on that page. Verify
the selectable ID before adoption.

## Grok Build — host contracts

- [Headless/ACP](https://docs.x.ai/build/cli/headless-scripting): `grok -p`, `-m`,
  `--output-format plain|json|streaming-json`; `grok agent stdio` uses ACP over
  stdin/stdout. Assistant text arrives via `session/update`, while `session/prompt`
  returns completion metadata. The [CLI reference](https://docs.x.ai/build/cli/reference)
  documents `--effort` and `--no-subagents`.
- [Permissions](https://docs.x.ai/build/features/permissions): Ask, Auto and
  Always-approve modes; `--allow`/`--deny`, with deny winning. Permission mode gates
  execution; it does not replace sandbox containment or supply owner authority.
- [Headless permissions](https://docs.x.ai/build/enterprise):
  `--permission-mode dontAsk` silently denies calls without an explicit allow rule.
  Inspect denied operations and expose limitations to the model and recipient;
  process completion alone does not prove the requested work happened.
- [Sandbox](https://docs.x.ai/build/features/sandbox): `off` (default), `workspace`,
  `devbox`, `read-only`, `strict`. Child-network blocking is enforced only on Linux;
  it is a no-op on macOS. In-process API/web traffic is separate. Built-in profiles
  do not permanently protect credential paths; verify the actual filesystem boundary.
- [Subagents](https://docs.x.ai/build/features/subagents): `general-purpose`,
  `explore`, `plan`; custom definitions in `.grok/agents/`. Official sources conflict:
  that page says explore/plan have no shell or edits, while the
  [Grok Build user guide](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-pager/docs/user-guide/16-subagents.md#capability-modes)
  says both can run shell commands but cannot edit files. Treat both as possibly
  shell-capable, with no edits; verify the deployed build's tools and enforce shell
  effects through permissions and sandbox boundaries. Use `--no-subagents` when
  the authorized workflow calls for no fan-out. No local runtime probe resolved this.
- [Worktrees](https://docs.x.ai/build/features/worktrees): `grok -w` isolates files
  in a Git checkout. It does not isolate external effects or grant authority.

## Smallest checks and retirement

Exercise a read-only headless result and ACP continuation, then a denied call under
`dontAsk`; confirm the failure is visible. Probe child-network restrictions on the
deployment OS rather than assuming cross-platform parity. Compare effort and delegation
on representative authorized work before adopting behavior prompts. These checks have
not run here. Re-test on upgrade, retire unneeded compensations, and record why in
[historical cases](../historical-cases.md).
