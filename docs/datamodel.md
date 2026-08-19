# Voyage Data Model

## 1. Overview

Voyage stores persistent information about the user's projects, goals,
tasks, recurring tasks, schedules, and history.

The data model is built around an important distinction:

> Persistent entities represent the user's ongoing work, while daily
> context represents what is relevant to a particular day.

Daily context is therefore derived from persistent data rather than
being treated as a primary entity.

The core entities are:

- Projects
- Goals
- Tasks
- Recurring Tasks
- Task Schedules
- Recurring Task Occurrences
- History

---

## 2. Project

A project represents something the user is working on that requires
sustained attention over time.

A project does not require a predefined completion date or lifespan.
It may continue indefinitely.

Examples:

- Voyage
- Sherlock
- hwcheck
- Learning C
- NSE quantitative trading

### Attributes

```text
Project
-------
id
name
description
created_at
status
````

### Example

```text
id: 1
name: Voyage
description: Personal context management system
status: active
created_at: 2026-08-19
```

### Relationships

A project can have zero or more tasks.

```text
Project
   │
   └── 0..* Tasks
```

Tasks are not required to belong to a project.

---

## 3. Goal

A goal represents a desired outcome that the user wants to achieve.

A goal may have a target, deadline, or measurable outcome.

Examples:

* Read 5 books before the end of the year
* Learn about the NSE
* Become proficient in C
* Earn 100,000 KES

### Attributes

```text
Goal
----
id
title
description
target
deadline
status
created_at
```

### Relationships

A goal may be associated with zero or more tasks.

```text
Goal
 │
 └── 0..* Tasks
```

A task does not need to belong to a goal.

---

## 4. Task

A task represents an actionable unit of work.

Tasks are independent entities.

A task may:

* Belong to a project
* Support a goal
* Belong to neither
* Be scheduled for a specific day
* Be carried forward
* Be completed
* Be marooned

### Attributes

```text
Task
----
id
title
description
project_id
goal_id
status
created_at
completed_at
marooned_at
```

`project_id` is optional.

`goal_id` is optional.

### Example: Independent Task

```text
id: 42
title: Learn pytest
description: Learn the basics of pytest
project_id: NULL
goal_id: NULL
status: active
created_at: 2026-08-19
```

This task is completely independent.

### Example: Project Task

```text
id: 43
title: Implement CLI
project_id: 1
goal_id: NULL
status: active
```

This task belongs to the Voyage project.

### Example: Goal Task

```text
id: 44
title: Read DDIA
project_id: NULL
goal_id: 2
status: active
```

This task supports a goal.

A task may also be associated with both a project and a goal.

---

## 5. Task Lifecycle

Tasks are persistent and have a lifecycle.

The initial lifecycle is:

```text
                 ┌──────────────┐
                 │    ACTIVE    │
                 └──────┬───────┘
                        │
             ┌──────────┼──────────┐
             ▼          ▼          ▼
        COMPLETED    CARRIED     MAROONED
                     FORWARD
```

### Active

The task is currently active and may appear in future contexts.

### Completed

The task has been successfully completed.

Completed tasks remain in the database and history.

They are not deleted.

### Carried Forward

A task can remain active when the user does not complete it on the
day for which it was scheduled.

The task is then associated with a later date.

Carrying forward a task does not create a new task.

Example:

```text
August 19
    Learn pytest
        ↓
    Not completed
        ↓
August 20
    Learn pytest
```

The task retains the same identity.

### Marooned

A marooned task is a task the user has deliberately abandoned.

It is removed from active work and future context but remains in
history.

Example:

```text
Learn pytest
    ↓
MAROONED
```

The task is not deleted.

---

## 6. Task Scheduling

A task and its scheduled date are separate concepts.

A task represents the work itself.

A schedule represents when the task should appear in the user's
context.

For example:

```text
Task
----
title: Learn pytest
```

and:

```text
TaskSchedule
------------
task_id: 42
scheduled_date: 2026-08-20
```

This separation allows a task to be moved between days without
creating duplicate tasks.

The task represents:

> What needs to be done?

The schedule represents:

> When should it appear in my context?

---

## 7. Task Schedule

A task schedule associates an active task with a date on which it
should appear in the user's context.

### Attributes

```text
TaskSchedule
------------
id
task_id
scheduled_date
created_at
```

### Example

```text
Task:
    Learn pytest

TaskSchedule:
    task_id: 42
    scheduled_date: 2026-08-20
```

If the task is carried forward:

```text
2026-08-20
    ↓
2026-08-21
```

the task remains the same entity.

The schedule changes rather than creating a second task.

---

## 8. Recurring Tasks

A recurring task represents work that should occur according to a
recurring schedule.

Examples:

* Work out every Tuesday
* Read every Wednesday
* Work out three times per week

Recurring tasks are separate from ordinary tasks because their
appearance in daily context is determined by recurrence rules.

### Attributes

```text
RecurringTask
-------------
id
title
description
recurrence_rule
created_at
status
```

The recurrence rule determines when an occurrence is due.

Example:

```text
title:
    Work out

recurrence_rule:
    Every Tuesday
```

Another example:

```text
title:
    Work out

recurrence_rule:
    Three times per week
```

The exact recurrence syntax will be determined when the scheduling
system is implemented.

---

## 9. Recurring Task Occurrences

A recurring task represents the rule.

An occurrence represents a specific instance of that rule.

For example:

```text
Recurring Task
--------------
Work out
Every Tuesday
```

can produce:

```text
Occurrence
----------
Tuesday, August 25
```

The occurrence represents the specific instance of the recurring task
for that date.

This distinction allows the recurring definition to remain persistent
while individual occurrences can have their own completion history.

Conceptually:

```text
RecurringTask
      │
      ├── Occurrence: August 25
      ├── Occurrence: September 1
      ├── Occurrence: September 8
      └── Occurrence: September 15
```

---

## 10. Recurring Task Scheduling

Recurring-task evaluation is a Voyage responsibility.

The operating system scheduler, such as cron or a daemon, may be used
to trigger Voyage's scheduling process.

However:

> Cron is infrastructure; recurrence rules belong to Voyage.

The recurrence logic should therefore not be encoded directly into
crontab entries.

Conceptually:

```text
Operating System
       │
       │ trigger
       ▼
Voyage Scheduler
       │
       │ evaluate recurrence rules
       ▼
Recurring Tasks
       │
       ▼
Recurring Occurrences
       │
       ▼
Today's Context
```

This keeps the recurrence model independent from the operating system.

---

## 11. Miscellaneous Work

Miscellaneous work represents short-lived or unclassified work that
does not need to belong to a project or goal.

Examples:

* Learn systemd
* curl vs ping
* Investigate a Linux command
* Try a new tool

Miscellaneous work can be represented as a task without a project or
goal.

For example:

```text
Task
----
title: Learn systemd
project_id: NULL
goal_id: NULL
```

No separate database entity is required unless future requirements
justify one.

---

## 12. Daily Context

Daily context is the collection of work relevant to a specific day.

It is not a primary persistent entity.

Instead, it is constructed from multiple sources.

```text
                    Daily Context
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
   Scheduled Tasks   Recurring Tasks   Other Work
```

For example:

```text
voy today
```

could produce:

```text
TODAY

TASKS
    Work out
    Read Sherlock code
    Begin porting hwcheck to C#

MISC
    Learn systemd
    curl vs ping

GOALS
    Read DDIA
```

The context is therefore a view over persistent data.

---

## 13. Sources of Daily Context

Daily context can be created from both predefined and user-defined
sources.

### Predefined Context

Predefined context comes from recurring tasks.

Example:

```text
Every Wednesday
    Work out
```

When Wednesday arrives:

```text
Wednesday
    [ ] Work out
```

appears in the daily context automatically.

### User-Defined Context

The user can explicitly add something to a future day's context.

For example, the user's mother tells them:

> Clean the gate tomorrow.

The user can create:

```text
Task:
    Clean the gate

Schedule:
    Tomorrow
```

The task then appears in tomorrow's context.

Another example:

```text
Today:
    Working on Sherlock

Discovery:
    pytest

Tomorrow:
    Learn pytest
```

The user can explicitly schedule the new task for tomorrow.

Both predefined and user-defined work can coexist in the same daily
context.

---

## 14. Explicitly Scheduled Work

The user can explicitly schedule a task for a future date.

For example:

```text
voy add task "Clean the gate" --tomorrow
```

creates:

```text
Task
----
title: Clean the gate
```

and:

```text
TaskSchedule
------------
scheduled_date: tomorrow
```

The task then appears in the context for that date.

This allows the user to plan work that was not previously known.

---

## 15. Carrying Tasks Forward

If a scheduled task is not completed, it may be carried forward.

Example:

```text
August 19
─────────
Learn pytest
```

The user does not complete it.

Voyage can move the task to:

```text
August 20
─────────
Learn pytest
```

The original task remains the same entity.

The system should preserve the fact that the task was previously
scheduled for August 19.

This information belongs in history.

Conceptually:

```text
Task
 │
 ├── Schedule: August 19
 │
 └── Schedule: August 20
```

The exact implementation may either update the active schedule or
maintain schedule history, but the fact that the task was carried
forward must remain recoverable.

---

## 16. Task Completion and New Work

Completing a task does not prevent the user from discovering new work.

Example:

```text
August 19

Learn pytest
    ↓
COMPLETED

New discovery:
    Write unit tests
```

The user can create a new task:

```text
Write unit tests
```

and schedule it for the next day.

The two tasks remain separate:

```text
Task 42
Learn pytest
COMPLETED

Task 43
Write unit tests
ACTIVE
```

The original task remains a record of what was actually accomplished.

The newly discovered work becomes a separate task.

This prevents the system from rewriting history.

---

## 17. Marooning

A user may decide that an active task is no longer worth pursuing.

For example:

```text
Learn pytest
    ↓
MAROONED
```

The task remains stored but is removed from active context.

The system should preserve:

```text
marooned_at
```

and the associated history.

Marooning is therefore different from deleting.

A marooned task should not appear in future daily contexts unless the
user explicitly revives or reschedules it.

---

## 18. History

History records significant events in the lifecycle of Voyage's
entities.

Examples:

* Task created
* Task scheduled
* Task carried forward
* Task completed
* Task marooned
* Project created
* Goal created
* Recurring task created
* Recurring occurrence generated

A history record can conceptually contain:

```text
History
-------
id
entity_type
entity_id
event_type
timestamp
metadata
```

For example:

```text
entity_type: task
entity_id: 42
event_type: carried_forward
timestamp: 2026-08-19
```

History should be append-oriented.

Events should not be deleted simply because the current state of an
entity changes.

History allows Voyage to answer questions such as:

```text
What did I work on yesterday?

What have I completed?

When did I work on this project?

How often do I carry tasks forward?

What did I abandon?

What progress have I made?
```

---

## 19. Entity Relationships

The core relationships are:

```text
Project
   │
   └──────── 0..* Tasks


Goal
   │
   └──────── 0..* Tasks


Task
   │
   └──────── 0..* Schedules


RecurringTask
   │
   └──────── 0..* Occurrences


Task / Project / Goal / RecurringTask
   │
   └──────── 0..* History Events
```

A task can exist independently:

```text
Task
 ├── project_id = NULL
 └── goal_id = NULL
```

A task can belong to a project:

```text
Task
 ├── project_id = 1
 └── goal_id = NULL
```

A task can support a goal:

```text
Task
 ├── project_id = NULL
 └── goal_id = 2
```

A task may also be associated with both.

---

## 20. Overall Data Flow

The overall model can be viewed as:

```text
                    PROJECTS
                       │
                       ▼
                      TASKS ◄──────── GOALS
                       │
              ┌────────┴────────┐
              ▼                 ▼
          SCHEDULES       TASK HISTORY
              │
              ▼
       ┌───────────────┐
       │ DAILY CONTEXT │
       └───────────────┘
              ▲
              │
       RECURRING TASKS
              │
              ▼
         OCCURRENCES
```

The user's command:

```text
voy today
```

does not simply retrieve a "today" record.

Voyage constructs today's context from the underlying data.

---

## 21. Core Design Principles

### Tasks are independent

A task does not require a project or goal.

### Context is derived

Daily context is constructed from persistent information.

### Scheduling is separate from identity

A task represents work; a schedule represents when that work should
appear.

### Recurrence is a domain concept

Cron or another scheduler may trigger the system, but Voyage owns the
meaning of recurrence.

### History is preserved

Completed, carried-forward, and marooned work should remain traceable.

### No destructive deletion by default

Finishing or abandoning work should not erase its history.

### New discoveries create new work

Completing one task and discovering another should result in separate
tasks rather than rewriting history.

### Daily context can be predefined or user-defined

Some context is generated automatically from recurring tasks, while
other context is explicitly created by the user.

### A task has a lifecycle

A task is not simply `done` or `not done`.

It can be:

```text
ACTIVE
COMPLETED
MAROONED
```

and can be carried forward while remaining active.

### Tasks and schedules are separate

A task represents the work.

A schedule represents when the work should appear.

This allows a task to move between days without creating duplicate
tasks.

---

## 22. Conceptual Example

Suppose the user has:

```text
Project:
    Sherlock

Goal:
    Read 5 books before the end of the year

Recurring Task:
    Work out every Wednesday
```

On Monday, the user is working on Sherlock and discovers pytest.

They create:

```text
Task:
    Learn pytest

Schedule:
    Tuesday
```

Their mother then tells them to clean the gate tomorrow.

They create:

```text
Task:
    Clean the gate

Schedule:
    Tuesday
```

On Tuesday, Voyage may show:

```text
TODAY

TASKS

    [ ] Learn pytest
    [ ] Clean the gate
    [ ] Work out
```

The user works on pytest but does not finish it.

Voyage carries it forward:

```text
Wednesday

    [ ] Learn pytest
```

On Wednesday, they finish learning pytest and discover that they
need to write unit tests.

They mark:

```text
Learn pytest → COMPLETED
```

and create:

```text
Task:
    Write unit tests

Schedule:
    Thursday
```

The history now preserves the chain:

```text
Learn pytest
    Created
    Scheduled Tuesday
    Carried forward Wednesday
    Completed Wednesday

Write unit tests
    Created Wednesday
    Scheduled Thursday
```

If instead the user decides they no longer care about pytest:

```text
Learn pytest → MAROONED
```

The task disappears from active context but remains in history.

---

## 23. Database Implementation

This document describes the conceptual data model.

It does not yet define the final database schema.

The eventual storage implementation will determine:

* Database engine
* Table definitions
* Column types
* Primary keys
* Foreign keys
* Indexes
* Constraints
* Date and time representation
* Recurrence representation
* History storage
* Migration strategy

These decisions should be made when the storage layer is designed.

The conceptual relationships defined in this document should remain
stable regardless of the underlying database implementation.

---

## 24. Summary

The fundamental distinction in Voyage is:

```text
Project
    = something I am working on over time

Goal
    = something I want to achieve

Task
    = something I need to do

Recurring Task
    = something I need to do repeatedly

Schedule
    = when a task should appear

Occurrence
    = a specific instance of a recurring task

Daily Context
    = what matters for a particular day

History
    = what has happened
```

These concepts should remain separate throughout the implementation.

In particular:

```text
Task ≠ Schedule
Task ≠ Context
Recurring Task ≠ Occurrence
Completed ≠ Deleted
Marooned ≠ Deleted
Project ≠ Task
Goal ≠ Task
```

Voyage's data model is designed to preserve the user's work over time
while making the relevant work visible in the context of each day.

```
```

