# Agent Harness Design maintenance

This repository owns the independent Skill under
`plugins/agent-harness-design/skills/agent-harness-design/`. Keep the entrypoint short;
general component design belongs in `references/architecture-guide.md` and existing
component references. Target-model selection belongs in `references/model-adaptation.md`
with dated profiles under `references/models/`. Do not build a runtime or mandatory
dependency chain to maintain this knowledge.

Treat scope and rule strength independently. Preserve authority/evidence invariants;
distinguish general responsibilities, provider contracts, behavioral recommendations
and historical cases. The consulting model need not be the target model. Record exact
model, mode, endpoint, host, date and evidence limits. Published pretraining/SFT/RL
facts do not by themselves establish causal benefits from a particular scaffold.

Update affected guidance and evidence together when releases, protocol changes, real
failures or credible research change an assumption. Keep useful superseded conditions
and retirement reasons in `references/historical-cases.md`; do not leave conflicting
active defaults. Read only relevant sources and references.

Use existing stdlib installers, eval runner and tests. Structural checks establish
package integrity; new-session trials establish Skill behavior; target-system trials
establish runtime compatibility or optimization benefits. Keep those claims separate.
Record raw failures and unverified configurations; never turn a protocol-invalid
baseline into a behavioral improvement claim. Freeze the Skill tree during an eval:
the runner copies it per run. After edits, retain prior evidence and rerun the affected
cases against the final source.

For an authorized release, align plugin/Skill/installer versions, retain matching
evaluation evidence, run `python3 -m unittest discover -s tests -v` and the available
Skill validator. Publish this source before refreshing its Marketplace pin. Preserve
older evidence and package URLs. Publishing does not update installed user copies.
