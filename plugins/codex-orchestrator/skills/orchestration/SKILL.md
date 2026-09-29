---
name: orchestration
description: "Guide when to work directly or delegate software tasks through native Codex agents while the parent owns decisions and acceptance."
---

# Codex Orchestrator

The parent frames the objective, constraints, ownership, and expected result, then
interprets evidence and owns decisions and acceptance. Keep short lookups and
sequential critical-path work with the parent when briefing and waiting would cost
more than doing the work.
Delegate when separate context or parallel progress adds value, accounting for
briefing and integration. Choose the role before reusing an agent:

- The [retained squire](references/squire.md) handles simple operational support:
  finding facts, checking status, running existing commands, and reporting results.
  It does not implement changes or coordinate other agents.
- Workers own substantive research, diagnosis, code and test changes, and technical
  validation. Assign them directly; a familiar squire is not a substitute.
- An [advisor](references/operations.md#advice-when-useful) gives a bounded,
  read-only opinion on an open decision before implementation. Seek advice when
  competing approaches or uncertain assumptions could materially change the plan,
  not only when the decision is critical. Straightforward, settled work needs none.

Give each delegate a complete authorized mission within its role. Do not repeat
its work in the parent. Loading required instructions and native agent coordination
remain parent actions.

Assess decision criticality separately from task difficulty. Before committing work
to an open decision whose failure would cause substantial harm or costly downstream
rework, obtain bounded [advice](references/operations.md#advice-when-useful), even
when the choice seems easy. Reuse still-applicable evidence that already challenges
the same decision.

Follow user instructions, applicable `AGENTS.md`, and actual host permissions.
Use [native delegation](references/operations.md) for assignments and capabilities.
Leave `model` and `reasoning_effort` unset unless intentionally pinned.
An optional separately installed router can select settings for unpinned native
spawns; explicit settings and roles remain authoritative. Do not infer the model
actually run from the requested or selected model.

Obtain an independent read-only acceptance review of the stable integrated artifact
when work changes behavior, a supported contract, or an authority boundary, or
acceptance needs independent evidence under [review](references/review.md).
The parent decides acceptance from the diff, checks, and review evidence. After
bounded corrections, use affected checks and targeted confirmation; renew full
review when earlier review no longer covers the changed behavior, contract,
authority, or ownership. Wording or presentation-only edits need parent assessment.

Continue authorized work through validation, blocking corrections, and requested
delivery. Ask only for essential missing information, a material scope decision,
or additional authorization. Report checks and limitations actually observed.
Separate app tasks require an explicit user request; see
[operations](references/operations.md#separately-requested-app-tasks).
