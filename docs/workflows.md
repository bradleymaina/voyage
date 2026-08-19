# Voyage Workflows

## 1. Overview

Workflows define how Voyage behaves when the user interacts with the system.

The command documentation defines **what commands mean**.

The data model defines **what information Voyage stores**.

This document defines:

> **What happens between the user's command and the resulting state.**

Voyage workflows are designed around a central distinction:

> **Persistent entities represent the user's ongoing work, while daily context represents what the user is actively working on today.**

Tasks are the bridge between these two layers.

---

# 2. Core Concepts

Voyage operates across three related layers:

```text
Persistent State
────────────────
Projects
Goals
Books
Tasks
Schedules
Recurring Tasks

        │
        │ daily context
        ▼

Daily State
───────────
Today's active tasks
Today's priorities
Today's scheduled work

        │
        │ actions
        ▼

History
───────
Boarded
Docked
Anchored
Marooned
Carried forward
```

Persistent entities survive across days.

Daily context changes from day to day.

History records meaningful changes to the user's state.

---

# 3. Task Lifecycle

Tasks have a persistent identity, but their active daily context has a 24-hour lifespan.

The normal lifecycle is:

```text
                 ┌─────────────┐
                 │             │
                 ▼             │
              ┌────────┐      │
              │ ACTIVE │──────┤
              └────────┘      │
                 │             │
          ┌──────┼──────┐      │
          ▼      ▼      ▼      │
        DOCK   ANCHOR MAROON   │
          │      │      │       │
          ▼      ▼      ▼       │
      COMPLETE PAUSED ABANDONED│
                                │
                 24h expires ──┘
                         │
                         ▼
                      NEXT DAY
```

The four task actions are:

```text
board
dock
anchor
maroon
```

---

# 4. Workflow: Boarding a New Task

Command:

```bash
voy board "Wash gate"
```

### Purpose

Create a new task and immediately place it into today's active context.

### Process

```text
User
 │
 │ voy board "Wash gate"
 ▼
Parse command
 │
 ▼
Validate task information
 │
 ▼
Create persistent task
 │
 ▼
Create today's task context
 │
 ▼
Record BOARDED event
 │
 ▼
Return success
```

### Result

Persistent state:

```text
Task
────
Title: Wash gate
Status: active
```

Daily state:

```text
Today
─────
[ ] Wash gate
```

History:

```text
09:32  BOARDED  Wash gate
```

`board` therefore combines:

1. task creation
2. activation for today
3. history recording

The user does not need separate commands for these operations.

---

# 5. Workflow: Boarding an Existing Task

A task may already exist but not currently be part of today's active context.

Command:

```bash
voy board "Study SQL"
```

### Process

```text
Find existing task
        │
        ▼
Does it already exist?
        │
       YES
        │
        ▼
Create today's active context
        │
        ▼
Record BOARDED event
```

Voyage must not create duplicate tasks simply because the user boards an existing task.

The persistent task remains the same task.

Only its daily context changes.

---

# 6. Workflow: Docking a Task

Command:

```bash
voy dock "Wash gate"
```

### Purpose

Mark active work as completed.

### Process

```text
Find task
   │
   ▼
Verify task is active
   │
   ▼
Mark task completed
   │
   ▼
Remove from active daily context
   │
   ▼
Record DOCKED event
   │
   ▼
Return success
```

Result:

```text
Today
─────
No active "Wash gate"
```

Persistent state:

```text
Wash gate
Status: completed
```

History:

```text
09:32  BOARDED  Wash gate
11:04  DOCKED   Wash gate
```

A docked task does not roll forward into the next day.

---

# 7. Workflow: Anchoring a Task

Command:

```bash
voy anchor "Study SQL"
```

### Purpose

Explicitly pause work.

### Process

```text
Find task
   │
   ▼
Verify task is active
   │
   ▼
Change daily task state → anchored
   │
   ▼
Record ANCHORED event
   │
   ▼
Return success
```

Anchoring is different from leaving a task unfinished.

An unfinished task is eligible for rollover.

An anchored task represents an explicit decision:

> **Do not actively work on this right now.**

The task itself remains persistent.

---

# 8. Workflow: Marooning a Task

Command:

```bash
voy maroon "Build mobile app"
```

### Purpose

Intentionally abandon work.

### Process

```text
Find task
   │
   ▼
Verify task exists
   │
   ▼
Mark task abandoned
   │
   ▼
Remove from active daily context
   │
   ▼
Record MAROONED event
   │
   ▼
Return success
```

A task that has been marooned is **not deleted**.

Its existence and history are preserved.

An optional reason may be supplied:

```bash
voy maroon "Build mobile app" --reason "Scope became too large"
```

The reason becomes part of the historical event.

---

# 9. Workflow: Daily Rollover

Daily rollover is one of the most important workflows in Voyage.

At the end of a 24-hour period, active unfinished tasks are evaluated.

For example:

```text
August 19

[ ] Write commands documentation
[x] Wash gate
```

At rollover:

```text
Write commands documentation → carried forward
Wash gate → completed
```

The next day becomes:

```text
August 20

[ ] Write commands documentation
```

### Rollover process

```text
End of day
    │
    ▼
Find today's active tasks
    │
    ▼
For each task
    │
    ├── completed ──→ leave completed
    │
    ├── anchored ───→ remain paused
    │
    ├── marooned ───→ remain abandoned
    │
    └── unfinished ─→ carry forward
                            │
                            ▼
                         tomorrow
```

The task is **not recreated**.

Its persistent identity remains unchanged.

Only the daily context moves forward.

---

# 10. Carrying a Task Forward

When an unfinished task crosses midnight, Voyage creates the next day's context for that task.

Example:

```text
Task ID: 42
Title: Write commands documentation
```

August 19:

```text
Task 42
Daily context:
August 19 → active
```

After rollover:

```text
Task 42
Daily context:
August 19 → active
August 20 → active
```

This allows Voyage to answer historical questions such as:

> How many days has this task been carried forward?

or:

> When did I first start working on this?

without changing the identity of the task.

---

# 11. Anchored Tasks and Rollover

Anchored tasks require special treatment.

If a task is explicitly anchored:

```bash
voy anchor "Study SQL"
```

it should **not automatically behave like an unfinished active task**.

The anchor represents an intentional pause.

Therefore:

```text
ACTIVE
  │
  └── anchor
        ↓
     ANCHORED
```

An anchored task remains outside the active working context until explicitly brought back.

If the user wants to work on it again, they can board it:

```bash
voy board "Study SQL"
```

This returns it to today's active context.

---

# 12. Reboarding a Task

`board` can therefore reactivate an existing task.

Example:

```text
Study SQL
Status: anchored
```

The user decides to resume:

```bash
voy board "Study SQL"
```

Result:

```text
Study SQL
Status: active
Today's context: active
```

History:

```text
12:10  ANCHORED  Study SQL
15:30  BOARDED   Study SQL
```

This makes `board` both:

* the creation mechanism for new work
* the reactivation mechanism for existing work

---

# 13. Daily Context

Today's context is a projection of persistent state.

It should not become a second independent copy of the task.

Conceptually:

```text
Persistent Task
      │
      ▼
Daily Context
```

For example:

```text
Persistent
──────────
Task: Wash gate
Status: active

Daily
─────
August 19 → active
```

The daily context tells Voyage:

> This task is part of today's work.

The persistent task tells Voyage:

> This piece of work exists.

---

# 14. Workflow: Logging

Command:

```bash
voy log
```

The log reads historical events rather than reconstructing history from the current state.

Example:

```text
VOYAGE LOG

19 AUG

09:32  BOARDED   Wash gate
10:15  BOARDED   Write commands documentation
11:04  DOCKED    Wash gate
12:10  ANCHORED  Study SQL
13:40  MAROONED  Old mobile app
```

Every meaningful state-changing action should produce a history event.

The history system should therefore be append-oriented.

Existing events should not normally be modified or deleted.

---

# 15. Workflow: Project-Associated Tasks

Projects represent persistent bodies of related work.

A task can be boarded directly into a project:

```bash
voy board "Fix contact normalization" --project Sherlock
```

The workflow is:

```text
Create task
    │
    ├── Associate with Sherlock
    │
    ├── Add to today's context
    │
    └── Record BOARDED event
```

The project itself remains persistent.

The task participates in the project's work while still following the normal daily lifecycle.

---

# 16. Workflow: Goal-Associated Tasks

Goals represent desired outcomes.

A goal may have multiple tasks contributing toward it.

For example:

```text
Goal
└── Launch Sherlock

Tasks
├── Fix contact normalization
├── Add lecturer search
└── Deploy to Raspberry Pi
```

A task can therefore belong to both:

```text
Project
Goal
```

while still having its own daily lifecycle.

Example:

```bash
voy board "Deploy to Raspberry Pi" \
    --project Sherlock \
    --goal "Launch Sherlock"
```

The task is then:

```text
Persistent
──────────
Project → Sherlock
Goal    → Launch Sherlock

Daily
─────
Today → active
```

---

# 17. Books and Tasks

Books are persistent learning resources.

A book itself does not enter the daily task lifecycle.

Instead, reading or studying the book can produce tasks.

For example:

```text
Book
────
Designing Data-Intensive Applications
```

Today's work:

```bash
voy board "Read chapter 5 of DDIA"
```

The relationship becomes:

```text
Book
 │
 └── Task
      │
      ├── board
      ├── dock
      ├── anchor
      └── maroon
```

This keeps the book persistent while allowing individual reading activities to participate in daily planning.

---

# 18. Command Failure

Commands must fail safely.

A failed command must not leave Voyage in a partially modified state.

For example:

```bash
voy dock "Nonexistent task"
```

should not create anything.

It should return an informative error:

```text
Task not found: "Nonexistent task"
```

Likewise:

```bash
voy maroon "Wash gate"
```

should not silently create a task.

Operations that change existing work should first resolve and validate the target.

---

# 19. Idempotency

Commands should behave predictably when repeated.

For example, attempting to dock an already docked task should not create multiple completion events.

Similarly, boarding the same task twice on the same day should not create duplicate daily contexts.

Conceptually:

```text
board + board
      ↓
one active task
```

rather than:

```text
board + board
      ↓
two copies of the task
```

This is important because users may repeat commands accidentally.

---

# 20. State Transitions

The valid task transitions are:

```text
NEW
 │
 └── board ──→ ACTIVE
                  │
        ┌─────────┼─────────┐
        │         │         │
       dock     anchor    maroon
        │         │         │
        ▼         ▼         ▼
    COMPLETED  ANCHORED  MAROONED
                  │
                  │ board
                  ▼
                ACTIVE
```

Daily rollover introduces another transition:

```text
ACTIVE
  │
  │ unfinished at end of day
  ▼
NEXT DAY ACTIVE
```

The task itself remains persistent throughout these transitions.

---

# 21. Workflow Invariants

Voyage must maintain the following invariants.

### 21.1 A task has one persistent identity

Rolling a task into another day must never create a new task.

### 21.2 A task cannot be simultaneously active and completed

A docked task is no longer active.

### 21.3 A task cannot be simultaneously active and marooned

Marooning removes the task from active work.

### 21.4 Anchoring is explicit

A task is not considered anchored merely because the user stopped working on it.

### 21.5 Unfinished active work rolls forward

If the user takes no explicit action, unfinished active work is carried into the next day.

### 21.6 History is preserved

Docking, anchoring, marooning, boarding, and rollover events should remain historically observable.

### 21.7 Daily context does not duplicate persistent entities

The daily layer references persistent tasks rather than creating independent copies.

---

# 22. Overall Workflow

The complete Voyage workflow can be represented as:

```text
                    USER INTENTION
                         │
                         ▼
                voy board "Task"
                         │
                         ▼
                  TODAY'S WORK
                         │
              ┌──────────┼──────────┐
              │          │          │
              ▼          ▼          ▼
            dock       anchor     maroon
              │          │          │
              ▼          ▼          ▼
          completed    paused    abandoned
              │          │          │
              └──────────┼──────────┘
                         │
                         ▼
                       LOG
                         │
                         ▼
                     HISTORY
```

If no explicit action is taken before the daily boundary:

```text
ACTIVE TASK
     │
     │ midnight / daily boundary
     ▼
CARRIED FORWARD
     │
     ▼
NEXT DAY
```

The fundamental interaction loop is therefore:

```text
BOARD → WORK → DOCK / ANCHOR / MAROON
                    │
                    ▼
                   LOG
```

This loop is the core behavioral model of Voyage.

