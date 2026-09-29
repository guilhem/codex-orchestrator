<div align="center">

# Codex Orchestrator

**Keep the decisions. Delegate autonomous work.**

A Codex plugin for coordinating native agents around a clear division of responsibilities.

Native agents · Model-agnostic orchestration · MIT licensed

[Quick start](#quick-start) · [How it works](#how-it-works) · [Model routing](#optional-model-routing) · [Migration](#migrating-from-astra-advisor)

</div>

Your selected model stays in charge of scope, decisions, and acceptance. A
**retained squire (écuyer)** handles simple operational support across related
assignments. **Workers** handle substantive research, diagnosis, and implementation;
an **advisor** helps the parent assess open choices before implementation. The parent
keeps short lookups and sequential critical-path work when briefing and waiting
would cost more. Independent reviewers assess changes when the work calls for it.

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

Support follow-ups can reuse the same squire while its context remains useful. The parent
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

```mermaid
flowchart TB
    User["You · goal and constraints"] --> Parent["Parent · decisions and acceptance"]
    Parent -->|simple support| Squire["Squire / écuyer · facts, status, existing commands"]
    Parent -->|technical assignments| Workers["Workers · research, diagnose, build, verify"]
    Parent -->|open choices| Advisor["Advisor · read-only advice before implementation"]
    Parent -->|when needed| Reviewer["Independent reviewer · read-only assessment"]
    Parent -->|accepted result| User
```

| Responsibility | How the skill assigns it |
| --- | --- |
| **Frame and decide** | The parent sets the objective, scope, ownership, and expected result; interprets evidence; and accepts the work. It keeps work direct when delegation would cost more. |
| **Support the parent** | The squire finds facts, extracts logs, checks status, and runs existing commands or tests. It reports evidence; it does not change code, diagnose failures, or coordinate agents. |
| **Research and execute** | Workers receive technical assignments directly: substantive research, diagnosis, implementation, tests, and validation. |
| **Advise before acting** | An advisor challenges assumptions and compares approaches when uncertainty or tradeoffs could change the plan, including ordinary engineering choices. It stays read-only; the parent decides. |
| **Review independently** | The parent requests a read-only acceptance review for changes to behavior, supported contracts, or authority boundaries, or when acceptance needs independent evidence. |
| **Report honestly** | Delegates return sources, completed actions and checks, uncertainty, and unresolved decisions. The parent reports observed results and material limitations. |

Assignments carry explicit scope and permissions. A research request does not
authorize edits. Give each delegate the complete authorized outcome and stopping
condition within its role. Reuse the squire for related support; if that work reveals
a bug or needs technical judgment, the parent assigns a worker or consults an advisor.
Split the initial assignment only for a
verified host routing constraint. Message delivery and interruption are host-specific:
use exposed controls and check active work before reassignment. After a bounded
correction, use affected checks and targeted review confirmation; wording-only
changes need parent assessment.

Advice helps before implementation; independent review assesses the resulting work.
Consult when competing approaches or uncertain assumptions could change the plan;
straightforward or already settled work needs no consultation. A simple choice can
still be critical when other work depends on it and changing
course later would be costly. Before committing to such an open decision, the
parent seeks a bounded advisor opinion and reuses an existing challenge while its
evidence remains applicable. Critical advice requests the most capable suitable
model permitted by the user's settings and the host; the parent keeps the decision,
and the final acceptance review still checks the resulting work.

## What's included

| Component | Purpose |
| --- | --- |
| [Orchestration skill](plugins/codex-orchestrator/skills/orchestration/SKILL.md) | Instructions for delegation, squire reuse, review, and acceptance. |
| [Hooks](plugins/codex-orchestrator/hooks/hooks.json) | Once trusted, add a brief delegation reminder to each parent prompt and copy missing bundled profiles into the separate router's configuration directory. |

The orchestration skill needs no additional SDK or API key. Automatic model
selection is an optional integration described below.

## Optional model routing

Install and configure [codex-subagent-router](https://github.com/guilhem/codex-subagent-router)
separately to use Jev for model and effort selection on eligible native agent
spawns. That plugin owns the routing hook, SDK, and `TYPESAFE_API_KEY` setup.

Codex Orchestrator supplies three editable profiles:

| Profile | Assigned work | Model | Effort |
| --- | --- | --- | --- |
| [Routine](plugins/codex-orchestrator/routing/codex-orchestrator-routine.json) | Evidence collection, status checks, and bounded execution of existing commands. | `gpt-6.1-sol` | `low` |
| [Implementation](plugins/codex-orchestrator/routing/codex-orchestrator-implementation.json) | Ordinary code changes, tests, technical analysis, and review under a clear contract. | `gpt-6.1-sol` | `high` |
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
| [Native delegation](plugins/codex-orchestrator/skills/orchestration/references/operations.md) | Assignment boundaries, advice before decisions, and separately requested app tasks. |
| [Retained squire](plugins/codex-orchestrator/skills/orchestration/references/squire.md) | Simple support, reuse, reporting, and handoffs. |
| [Independent review](plugins/codex-orchestrator/skills/orchestration/references/review.md) | Acceptance criteria and correction follow-ups. |

---

Maintained by [Guilhem Lettron](https://github.com/guilhem). Derived from
[Astra Advisor](https://github.com/DannyMac180/astra-advisor) by Daniel McAteer.
[MIT licensed](LICENSE), with the original copyright attribution preserved.
