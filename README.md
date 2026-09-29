<div align="center">

# Codex Orchestrator

**Keep the decisions. Delegate autonomous work.**

A Codex plugin for coordinating native agents around a clear division of responsibilities.

Native agents · Model-agnostic orchestration · MIT licensed

[Quick start](#quick-start) · [How it works](#how-it-works) · [Model routing](#optional-model-routing) · [Migration](#migrating-from-astra-advisor)

</div>

Your selected model stays in charge of scope, decisions, and acceptance. A
**retained squire** — a delegate reused across related assignments — handles a
coherent autonomous task or independent workstream when delegation adds value. The
parent keeps short lookups and sequential critical-path work when briefing and
waiting would cost more. Independent reviewers assess changes when the work calls
for it.

The plugin packages this workflow as an [orchestration skill](plugins/codex-orchestrator/skills/orchestration/SKILL.md).
These are instructions for agents using the host's native tools; available
capabilities, your instructions, and repository permissions govern what can run.

## Quick start

**Requires:** Codex with plugin support and native agent delegation tools, plus
the `codex` CLI for the installation commands below. Codex **0.157.1** is the
minimum verified version for filtering subagent prompt hooks. The optional
prompt reminder also requires **Python 3** on macOS/Linux; Windows uses its
built-in PowerShell.

1. Register this repository as a marketplace and install the plugin (no checkout
   needed):

   ```sh
   codex plugin marketplace add guilhem/codex-orchestrator
   codex plugin add codex-orchestrator@codex-orchestrator
   ```

2. Review the bundled hooks in Codex's hook settings. Codex skips plugin hooks
   until you trust their current definitions:

   | Hook shown in Codex | Event | When to trust it |
   | --- | --- | --- |
   | **Add Codex Orchestrator reminder** | `UserPromptSubmit` | For a delegation reminder on every parent prompt. Subagent prompts receive no reminder. Optional when you invoke the skill explicitly. |
   | **Install Codex Orchestrator routing profiles** | `SessionStart` | Only for [optional model routing](#optional-model-routing). |

3. Confirm that the plugin is installed and enabled:

   ```sh
   codex plugin list --marketplace codex-orchestrator
   ```

   Expect `codex-orchestrator@codex-orchestrator` with status
   `installed, enabled`. Then start a fresh task or CLI session, select your
   preferred parent model, and give it a concrete goal:

   ```text
   Use $codex-orchestrator:orchestration to fix the empty-search bug.
   Reproduce it, make the smallest fix, run the affected tests, and review the diff.
   ```

Follow-ups can reuse the same squire while its context remains useful. The parent
keeps the user conversation and decides what to do with the returned evidence.

If the newly installed plugin does not appear in Codex, restart the app and
check again. If a hook does not run, review its trust state in Codex's hook
settings.

The prompt hook reads the event JSON and emits no reminder when a top-level
`agent_id` or `agent_type` field is present, even if its value is empty. Invalid
input also produces no reminder and does not block the prompt. This prevents
new injections; existing history, including history copied with
`fork_context: true`, can still contain earlier reminders. Use a fresh subagent
context to avoid copying them.

## How it works

**The orchestrator decides; the squire carries out the mission.** The
orchestrator is the parent agent you talk to. The **squire (écuyer)** is its
delegate, reused across related work so it keeps useful context.

Squires, workers, advisors, and reviewers are all **sub-agents**. These names
describe their jobs. For eligible new agents,
[model routing](#optional-model-routing) selects the requested model and effort.

```mermaid
flowchart TB
    accTitle: Orchestrator, routing, and agent roles
    accDescr: The orchestrator assigns the work. Optional routing selects model and effort when each sub-agent is created. The squire executes missions, workers handle specific tasks, the advisor challenges decisions, and the reviewer checks finished work.
    Orchestrator["Orchestrator<br/>Decides and accepts the result"]
    Routing["Routing · optional<br/>Mission → model + effort"]
    Squire["Squire / écuyer<br/>Researches, builds, verifies"]
    Workers["Workers<br/>Handle specific tasks"]
    Advisor["Advisor<br/>Challenges a decision, read-only"]
    Reviewer["Reviewer<br/>Checks finished work, read-only"]

    Orchestrator --> Routing
    Routing -->|mission| Squire
    Routing -->|advice| Advisor
    Routing -->|review| Reviewer
    Squire -->|assigns tasks if authorized| Workers
```

The orchestrator assigns the work. The routing block selects model and effort
when a sub-agent is created, including workers launched by the squire. Results,
checks, and open questions return to the caller; **the orchestrator makes the
final decision**. It keeps short tasks direct when delegation would cost more.

The parent can also launch workers directly. A squire can consult an advisor for a
technical question when its mission permits it. Both depend on the host's native
tools; if the squire cannot delegate, it gives the parent a ready task brief.

**Advice comes before a decision; review checks the resulting work.** Before a
critical commitment, the parent consults an advisor using the most capable
suitable model allowed by the user and host, reusing still-applicable advice.
The advisor cannot edit or delegate. The parent separately requests independent
review for changes to behavior, supported contracts, or authority boundaries, or
when acceptance needs independent evidence.

Each assignment defines scope, permissions, and a stopping condition. A research
request does not authorize edits. The squire carries its complete mission through
to a result; the parent reuses it for follow-ups while its context remains useful.
See [native delegation](plugins/codex-orchestrator/skills/orchestration/references/operations.md)
and [squire reuse](plugins/codex-orchestrator/skills/orchestration/references/squire.md)
for handoff and ownership rules.

## What's included

| Component | Purpose |
| --- | --- |
| [Orchestration skill](plugins/codex-orchestrator/skills/orchestration/SKILL.md) | Instructions for delegation, squire reuse, review, and acceptance. |
| [Hooks](plugins/codex-orchestrator/hooks/hooks.json) | Once trusted, add a brief delegation reminder to each parent prompt and copy missing bundled profiles into the separate router's configuration directory. |

The orchestration skill needs no additional SDK or API key. Automatic model
selection is an optional integration described below.

## Optional model routing

**The orchestrator chooses the job; the router chooses the model and effort.**
Routing applies when a new squire, worker, advisor, or reviewer is created. Your
selected parent model stays unchanged.

Install and configure [codex-subagent-router](https://github.com/guilhem/codex-subagent-router)
separately to use Jev for model and effort selection on eligible native agent
spawns. That plugin owns the routing hook, SDK, and `TYPESAFE_API_KEY` setup.

Explicit settings are `model`, `reasoning_effort`, or a native role (`agent_type`):
any one of them bypasses routing. Without a routing selection, the host keeps
explicit choices and uses its defaults for the rest. Reusing an existing squire
does not create a new agent or trigger a new routing selection.

Codex Orchestrator supplies three editable profiles:

| Profile | Assigned work | Model | Effort |
| --- | --- | --- | --- |
| [Routine](plugins/codex-orchestrator/routing/codex-orchestrator-routine.json) | Evidence collection, status checks, and bounded execution of existing commands. | `gpt-6-luna` | `max` |
| [Implementation](plugins/codex-orchestrator/routing/codex-orchestrator-implementation.json) | Ordinary code changes, tests, technical analysis, and review under a clear contract. | `gpt-6-sol` | `high` |
| [Complex](plugins/codex-orchestrator/routing/codex-orchestrator-complex.json) | Difficult diagnosis, architectural tradeoffs, and work with material security or data integrity risk. | `anthropic/claude-opus-5-5` | `high` |

To install them, trust **Install Codex Orchestrator routing profiles**
(`SessionStart`) in Codex's hook settings, then start a new session. The hook
copies missing `codex-orchestrator-*.json` files to
`$CODEX_HOME/subagent-router/`, falling back to `~/.codex/subagent-router/`
when `CODEX_HOME` is unset. It provides shell and
PowerShell commands for macOS/Linux and Windows respectively.

Edit the installed profiles to customize routing. Existing files are preserved.
To restore a bundled profile, delete its installed copy and start a new session;
disable the hook before removing the profiles permanently.

The skill leaves model and effort unset unless intentionally pinned. User and
repository requirements still apply. A routing choice records selection;
confirming which model actually ran requires runtime evidence.

## Migrating from Astra Advisor

The plugin and marketplace are now named `codex-orchestrator`. Existing
installations are not renamed automatically. Remove the old registration, then
follow [Quick start](#quick-start):

```sh
codex plugin remove astra-advisor@astra-advisor
codex plugin marketplace remove astra-advisor
```

- Update `$astra-advisor:orchestration` references in your instructions to `$codex-orchestrator:orchestration`.
- Move customizations from installed `astra-*.json` profiles to the new profiles, then remove obsolete copies to avoid duplicate routing choices.
- Update external settings that reference old profile IDs; those IDs are the filenames without `.json`.

The project is maintained at [`guilhem/codex-orchestrator`](https://github.com/guilhem/codex-orchestrator).

## Development and reference

From a local checkout of this repository, run the existing package validator
and tests:

```sh
sh plugins/codex-orchestrator/scripts/verify.sh
```

The verifier checks packaging, references, README links, and the bundled tests.
CI also runs the hook tests on Windows. These checks cover the packaged command,
not live host injection or agent behavior; host discovery, trust, and model routing
need host validation.

| Read more | Covers |
| --- | --- |
| [Native delegation](plugins/codex-orchestrator/skills/orchestration/references/operations.md) | Assignment boundaries, optional advice, and separately requested app tasks. |
| [Retained squire](plugins/codex-orchestrator/skills/orchestration/references/squire.md) | Reuse, reporting, and handoffs. |
| [Independent review](plugins/codex-orchestrator/skills/orchestration/references/review.md) | Acceptance criteria and correction follow-ups. |

---

Maintained by [Guilhem Lettron](https://github.com/guilhem). Derived from
[Astra Advisor](https://github.com/DannyMac180/astra-advisor) by Daniel McAteer.
[MIT licensed](LICENSE), with the original copyright attribution preserved.
