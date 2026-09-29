# Native delegation

Use the host's native agent tools and current schemas. Brief each delegate with
the role, objective, relevant context, scope and authorization, constraints, ownership,
expected result, and decisions reserved to the parent. The delegate chooses tools
and operational steps within that mission. An information request does not
authorize edits. Assign writing workers distinct files and preserve concurrent
changes; keep exploration and review read-only.

Do independent work while a delegate runs; wait when its result is the next
dependency. Message delivery and interruption semantics depend on the host. Sending
or queueing a message is not evidence that active work stopped. Use exposed controls
and confirm active work has stopped before transferring ownership; preserve any
completed or in-flight side effects.

Leave `model` and `reasoning_effort` absent unless explicitly pinned. An
optional separately installed router may handle unpinned native spawns; explicit
settings and native roles remain authoritative. A selected model is distinct
from runtime confirmation. Report an unmet explicit requirement, observed
mismatch, or material capability limit; missing metadata means the actual setting
is unknown.

Reuse the [squire](squire.md) only for related simple support and follow-ups. Assign
substantive research, diagnosis, implementation, and technical validation to workers
directly; retained context does not change the squire's role. A squire returns an
engineering question to the parent instead of taking it on or delegating it.
The parent launches required independent acceptance review directly under [review](review.md).
Delegation does not complete a task: the parent interprets returned evidence and
decides integration and acceptance without rerunning worker work. If nested
delegation is unavailable, a delegate returns a ready brief for parent coordination.

## Advice when useful

Use an advisor to help choose an approach before committing to it. Seek a bounded
opinion when plausible alternatives have meaningful tradeoffs, evidence leaves the
diagnosis uncertain, or an assumption could invalidate planned work. Advice is
useful for ordinary engineering decisions too; do not wait for a high-risk decision
or the final review. Skip consultation when the next step is straightforward or
already settled and no new evidence challenges it.

Advice is bounded, read-only delegation. Ask the parent about product intent,
history, scope, ownership, or permissions. For an isolated technical question, a
worker may consult an advisor when its assignment permits it and native tools
support it; a squire returns the question to the parent.

For a critical decision, name the concrete consequences of being wrong and the cost
of changing course: for example, an interface or data shape that dependent work will
build on. Consult before that commitment. A delegate encountering a critical decision
mid-assignment returns it to the parent if it exceeds its mandate or advice is not
authorized. Many affected files or high confidence alone do not establish or remove
criticality. Respect choices settled by the user; reuse a prior challenge
while its assumptions and scope remain valid. A powerful executor or a planned
final review alone does not supply that prior challenge.

For critical decisions, request the most capable suitable advisor allowed by user
and repository requirements and exposed by the host; explicitly pin the model when
supported and authorized. Follow the routing rules above for unavailable or
unconfirmed settings.

Send a compact question, source evidence, assumptions, options, recommendation,
constraints, and downstream consequences. Ask for material objections and a way to
check them; an advisor may conclude that no change is needed. Keep one consultation
per decision unless new evidence, assumptions, or consequences warrant another.
The advisor cannot edit, take over execution, or delegate again; the parent decides.
Advice does not replace acceptance review. Check deferred native tools before
declaring advice unavailable; delegates return the question to the parent if needed.
Include useful advice, uncertainty, and the resulting decision in the mission result.

## Separately requested app tasks

Create an app task only on explicit user request. Use capabilities actually exposed
by the host and preserve the user's scope, model, effort, and permission requirements.
Report any setting that cannot be confirmed or required capability that is missing.
