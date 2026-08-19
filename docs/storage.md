# Voyage Storage

## 1. Overview

Voyage requires persistent storage for projects, goals, tasks, books, schedules, recurring tasks, daily context, and history.

The storage layer is responsible for preserving Voyage's state across sessions and days.

It must support the distinction between:

> **Persistent entities represent ongoing work, while daily context represents what the user is actively working on today.**

Storage must therefore preserve both the long-term identity of work and the day-to-day history of how that work was handled.

---

# 2. Storage Principles

Voyage storage follows several principles.

### 2.1 Persistent entities are not daily context

A task should exist independently of a particular day.

For example:

```text
Task
────
"Write commands documentation"
```

may participate in several daily contexts:

```text
Aug 19 → active
Aug 20 → carried forward
Aug 21 → completed
```

The task is stored once.

Daily participation is stored separately.

---

### 2.2 History is append-oriented

Voyage should preserve meaningful events rather than reconstructing them from current state.

For example:

```text
09:32  BOARDED   Wash gate
11:04  DOCKED    Wash gate
```

The current task state might simply be:

```text
completed
```

but the history tells us **how it got there**.

---

### 2.3 State and history are separate

Current state answers:

> What is true now?

History answers:

> What happened?

These should not be conflated.

---

### 2.4 Daily context references persistent entities

The daily layer should not contain duplicate copies of tasks.

Instead:

```text
Daily Context
      │
      ▼
   Task ID
      │
      ▼
Persistent Task
```

---

# 3. Storage Technology

The initial implementation should use **SQLite**.

SQLite is appropriate for Voyage because:

* Voyage is primarily terminal-native.
* The initial system is single-user.
* No database server is required.
* The database is stored locally.
* Transactions provide reliable state changes.
* SQLite is mature and well supported by Python.
* The database can later be migrated if Voyage requires a different storage backend.

The application should interact with SQLite through a dedicated storage layer rather than allowing commands to execute SQL directly.

```text
CLI
 │
 ▼
Commands
 │
 ▼
Workflows
 │
 ▼
Storage Layer
 │
 ▼
SQLite
```

The command layer should never need to know SQL details.

---

# 4. Database Location

Voyage should maintain its persistent data separately from the source code.

The exact location may be configurable, but the default should follow the operating system's standard application-data conventions.

Conceptually:

```text
Voyage configuration
        │
        ├── database
        └── other persistent data
```

The database should not be stored inside the project's source directory by default.

---

# 5. Core Entities

The storage model consists of the following major entities:

```text
Project
Goal
Task
Book
Recurring Task
Schedule
Daily Context
History Event
```

Their relationships can be represented as:

```text
                 ┌─────────┐
                 │ Project │
                 └────┬────┘
                      │
              ┌───────┴────────┐
              ▼                ▼
          ┌──────┐          ┌──────┐
          │ Goal │          │ Task │
          └──┬───┘          └──┬───┘
             │                 │
             └────────┬────────┘
                      │
                      ▼
               Daily Context
                      │
                      ▼
                 History Event


Book ────────────────→ Tasks

Recurring Task ──────→ Tasks

Schedule ─────────────→ Tasks
```

Not every relationship must be implemented in the first version.

The storage model should be designed so that these relationships can be introduced without restructuring the entire system.

---

# 6. Project Storage

Projects represent persistent bodies of work.

A project should contain at minimum:

```text
Project
───────
id
name
description
status
created_at
updated_at
```

Possible project states include:

```text
active
archived
```

Projects are not subject to the 24-hour task lifecycle.

A project can exist for months or years while individual tasks move through daily contexts.

---

# 7. Goal Storage

Goals represent desired outcomes.

A goal should contain:

```text
Goal
────
id
name
description
status
created_at
updated_at
```

Goals are persistent.

They are not automatically carried forward every day.

Tasks may be associated with goals.

Conceptually:

```text
Goal
 │
 ├── Task
 ├── Task
 └── Task
```

The completion of individual tasks does not automatically imply completion of the goal.

Goal completion is an explicit state change.

---

# 8. Task Storage

Tasks are persistent units of work.

A task should contain:

```text
Task
────
id
title
description
status
project_id
goal_id
created_at
updated_at
completed_at
```

Possible persistent task states include:

```text
active
completed
anchored
marooned
```

The exact implementation may use a more normalized state model, but the conceptual states must remain explicit.

### Important

A task's persistent state is not the same thing as its daily context.

For example:

```text
Task
────
id: 42
title: Write commands documentation
status: active
```

Daily records determine whether task 42 is active for a particular date.

---

# 9. Daily Context Storage

Daily context represents what the user is actively working on for a particular day.

This is the storage mechanism that gives `board` its meaning.

A daily context record should contain at minimum:

```text
Daily Context
──────────────
id
task_id
date
state
boarded_at
updated_at
```

The `task_id` references a persistent task.

The `date` identifies the working day.

Possible daily states include:

```text
active
completed
anchored
marooned
carried
```

The exact implementation may simplify these states, but the storage layer must be capable of distinguishing intentional actions from automatic rollover.

---

# 10. Why Daily Context Is Separate

Consider:

```bash
voy board "Wash gate"
```

The task:

```text
Wash gate
```

should not be duplicated every day.

Instead:

```text
TASK
id = 42
title = "Wash gate"
```

Daily context:

```text
date        task_id    state
2026-08-19  42         active
```

If it remains unfinished:

```text
date        task_id    state
2026-08-19  42         carried
2026-08-20  42         active
```

The task remains:

```text
id = 42
```

throughout.

This preserves task identity while allowing Voyage to maintain a daily history.

---

# 11. History Event Storage

History is one of Voyage's core storage requirements.

A history event should contain:

```text
History Event
──────────────
id
event_type
task_id
timestamp
date
metadata
```

Possible event types include:

```text
BOARDED
DOCKED
ANCHORED
MAROONED
CARRIED
```

System-generated events such as `CARRIED` are valid even though they do not correspond to a user command.

---

# 12. History Is Append-Only

History should be treated as an append-oriented event stream.

For example:

```text
id   event       task       timestamp
1    BOARDED     Wash gate  09:32
2    DOCKED      Wash gate  11:04
```

If the task's current state later changes, the original events remain.

The system should not rewrite:

```text
BOARDED
```

into:

```text
DOCKED
```

Instead:

```text
BOARDED
DOCKED
```

remain separate events.

This provides the foundation for `voy log`.

---

# 13. Relationship Between State and History

The current state and event history work together.

Example:

```text
Task
────
title: Wash gate
status: completed
```

History:

```text
09:32  BOARDED  Wash gate
11:04  DOCKED   Wash gate
```

The task state provides efficient access to the current condition.

The history provides the historical explanation.

Voyage should not need to reconstruct the current state by replaying the entire history on every command.

---

# 14. Recurring Task Storage

Recurring tasks represent work that should generate or suggest tasks repeatedly.

A recurring task should contain information such as:

```text
Recurring Task
───────────────
id
title
description
project_id
goal_id
schedule
active
created_at
updated_at
```

A recurring task is not itself a daily task.

Instead, it acts as a persistent definition from which daily work can be produced.

Conceptually:

```text
Recurring Task
      │
      │ occurrence
      ▼
Daily Task
      │
      ├── board
      ├── dock
      ├── anchor
      └── maroon
```

The recurring definition remains persistent even when an individual occurrence is completed.

---

# 15. Schedule Storage

Schedules represent time-based events or planned work.

A schedule should contain:

```text
Schedule
────────
id
title
task_id
start_time
end_time
created_at
updated_at
```

Schedules are separate from tasks because:

> A task describes **what** needs to be done, while a schedule describes **when** something is expected to happen.

A task may exist without a schedule.

A schedule may reference a task.

---

# 16. Book Storage

Books are persistent learning resources.

A book should contain:

```text
Book
────
id
title
author
description
status
created_at
updated_at
```

Possible states might include:

```text
unread
reading
completed
abandoned
```

Book progress should be stored independently from daily tasks.

For example:

```text
Book
────
Designing Data-Intensive Applications
status: reading
progress: chapter 5
```

A task such as:

```text
Read chapter 5
```

can exist independently and participate in today's context.

---

# 17. Entity Relationships

The initial relationship model is:

```text
PROJECT
   │
   ├──────────────┐
   ▼              ▼
 GOALS           TASKS
   │              │
   │              ├──────────→ DAILY CONTEXT
   │              │
   │              └──────────→ HISTORY
   │
   └──────────────→ TASKS


BOOKS
   │
   └──────────────→ TASKS


RECURRING TASKS
   │
   └──────────────→ TASK OCCURRENCES


SCHEDULES
   │
   └──────────────→ TASKS
```

The exact relational structure may evolve during implementation, but these conceptual relationships should remain intact.

---

# 18. Identifiers

Every persistent entity should have a unique identifier.

Identifiers should be stable throughout the lifetime of an entity.

For example:

```text
Task ID: 42
```

should continue identifying the same task even if its title changes.

User-facing commands may primarily resolve entities by name or title:

```bash
voy dock "Wash gate"
```

while the storage layer uses stable IDs:

```text
task_id = 42
```

This prevents names from becoming the primary identity of entities.

---

# 19. Timestamps

Persistent records should maintain timestamps where relevant.

At minimum, entities that can change should have:

```text
created_at
updated_at
```

Events should have:

```text
timestamp
```

Daily context should have:

```text
date
```

Dates and timestamps should be stored consistently and should not depend on formatted human-readable strings.

---

# 20. Transactions

Operations that modify multiple pieces of state should be atomic.

For example:

```bash
voy board "Wash gate"
```

may require:

1. creating the task
2. creating today's daily context
3. creating a history event

These operations should succeed or fail together.

Conceptually:

```text
BEGIN TRANSACTION

Create task
Create daily context
Create BOARDED event

COMMIT
```

If any operation fails:

```text
ROLLBACK
```

This prevents partially created state.

---

# 21. Example: Boarding

After:

```bash
voy board "Wash gate"
```

the storage layer should conceptually contain:

### Task

```text
id: 42
title: Wash gate
status: active
```

### Daily Context

```text
task_id: 42
date: 2026-08-19
state: active
```

### History

```text
event: BOARDED
task_id: 42
timestamp: 2026-08-19 09:32
```

All three changes should occur within one transaction.

---

# 22. Example: Docking

After:

```bash
voy dock "Wash gate"
```

the storage layer becomes conceptually:

### Task

```text
id: 42
title: Wash gate
status: completed
```

### Daily Context

```text
task_id: 42
date: 2026-08-19
state: completed
```

### History

```text
BOARDED  → 09:32
DOCKED   → 11:04
```

The original `BOARDED` event remains unchanged.

---

# 23. Example: Daily Rollover

Suppose:

```text
Task ID: 42
Title: Write commands documentation
```

is active on August 19.

At the daily boundary, Voyage creates the next day's context:

```text
2026-08-19 → active
2026-08-20 → carried/active
```

A history event can record:

```text
CARRIED
task_id: 42
timestamp: 2026-08-20 00:00
```

No new task is created.

---

# 24. Data Integrity

The storage layer must enforce important relationships.

Examples:

* A daily context must reference an existing task.
* A history event referencing a task must reference an existing task.
* A task's project must reference an existing project.
* A task's goal must reference an existing goal.
* Duplicate daily contexts for the same task and date should be prevented.
* Entity IDs must be unique.

The database should enforce constraints wherever practical rather than relying entirely on application code.

---

# 25. Deletion and Historical Preservation

Voyage should be conservative about deletion.

Because history is a core feature, deleting an entity can potentially destroy useful context.

For example, permanently deleting:

```text
Wash gate
```

could make historical events meaningless:

```text
09:32  BOARDED  ?
11:04  DOCKED   ?
```

Therefore, normal lifecycle actions should generally be represented through state:

```text
completed
anchored
marooned
archived
```

rather than physical deletion.

Permanent deletion should be treated as a separate, deliberate operation if it is introduced.

---

# 26. Storage and Command Separation

Commands must not directly manipulate the database.

The architecture should be:

```text
User
 │
 ▼
CLI
 │
 ▼
Command Handler
 │
 ▼
Workflow
 │
 ▼
Domain Model
 │
 ▼
Storage Interface
 │
 ▼
SQLite
```

For example:

```bash
voy board "Wash gate"
```

should not execute SQL directly from the CLI handler.

Instead:

```text
board command
     │
     ▼
board workflow
     │
     ▼
task/context operations
     │
     ▼
storage
```

This keeps the system modular and allows the storage implementation to change without rewriting the command interface.

---

# 27. Storage Responsibilities

The storage layer is responsible for:

* creating and retrieving entities
* updating persistent state
* maintaining relationships
* storing daily contexts
* storing history events
* enforcing persistence constraints
* executing transactions
* retrieving historical information
* supporting daily rollover

The storage layer is **not** responsible for deciding what a command means.

For example:

> Whether `maroon` means "abandon a task" is a workflow concern.

> How the abandoned state is persisted is a storage concern.

---

# 28. Storage Invariants

Voyage storage must maintain the following invariants.

### Persistent identity

A task retains the same ID across days.

### Daily uniqueness

A task should have at most one daily context record for a given date.

### History preservation

Historical events are not overwritten when current state changes.

### Atomic state changes

Related state changes occur within a transaction.

### Referential integrity

Relationships reference valid persistent entities.

### Daily separation

Daily context is associated with a specific date.

### No task duplication on rollover

Carrying work into tomorrow must never create a duplicate persistent task.

---

# 29. Initial Storage Model

The initial database can therefore be represented conceptually as:

```text
┌─────────────────┐
│ projects        │
├─────────────────┤
│ id              │
│ name            │
│ description     │
│ status          │
│ created_at      │
│ updated_at      │
└────────┬────────┘
         │
         │
┌────────▼────────┐
│ goals           │
├─────────────────┤
│ id              │
│ name            │
│ description     │
│ status          │
│ created_at      │
│ updated_at      │
└────────┬────────┘
         │
         │
┌────────▼────────┐
│ tasks           │
├─────────────────┤
│ id              │
│ title           │
│ description     │
│ status          │
│ project_id      │
│ goal_id         │
│ created_at      │
│ updated_at      │
│ completed_at    │
└────────┬────────┘
         │
         ├────────────────────┐
         │                    │
         ▼                    ▼
┌─────────────────┐   ┌─────────────────┐
│ daily_context   │   │ history_events  │
├─────────────────┤   ├─────────────────┤
│ id              │   │ id              │
│ task_id         │   │ event_type      │
│ date            │   │ task_id         │
│ state           │   │ timestamp       │
│ boarded_at      │   │ metadata        │
│ updated_at      │   │                 │
└─────────────────┘   └─────────────────┘


┌─────────────────┐
│ books           │
├─────────────────┤
│ id              │
│ title           │
│ author          │
│ status          │
│ created_at      │
│ updated_at      │
└─────────────────┘


┌─────────────────┐
│ recurring_tasks │
├─────────────────┤
│ id              │
│ title           │
│ description     │
│ project_id      │
│ goal_id         │
│ schedule        │
│ active          │
│ created_at      │
│ updated_at      │
└─────────────────┘


┌─────────────────┐
│ schedules       │
├─────────────────┤
│ id              │
│ title           │
│ task_id         │
│ start_time      │
│ end_time        │
│ created_at      │
│ updated_at      │
└─────────────────┘
```

---

# 30. Storage Architecture

The implementation should expose storage operations through a small abstraction rather than spreading database operations throughout Voyage.

Conceptually:

```text
voyage/
├── cli/
├── commands/
├── workflows/
├── domain/
└── storage/
    ├── database
    ├── repositories
    └── migrations
```

The exact module structure will be defined during implementation.

The important architectural boundary is:

```text
Application logic
        │
        ▼
Storage interface
        │
        ▼
SQLite implementation
```

---

# 31. Final Storage Philosophy

Voyage storage is built around three ideas:

### Persistent work

Projects, goals, books, and tasks represent things that exist over time.

### Daily context

Daily context represents what the user has chosen to work on within a 24-hour window.

### History

History preserves the sequence of meaningful decisions and actions.

Together:

```text
             PERSISTENT WORK
                   │
                   ▼
             DAILY CONTEXT
                   │
                   ▼
                ACTION
                   │
       ┌───────────┼───────────┐
       ▼           ▼           ▼
      DOCK       ANCHOR      MAROON
       │           │           │
       └───────────┼───────────┘
                   ▼
                 LOG
                   │
                   ▼
                HISTORY
```

The storage system exists to make this model durable.

> **Voyage should never lose what the user has done, what they are doing, or why their current work is in its current state.**

