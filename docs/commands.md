# Voyage Commands

## 1. Overview

Voyage is a terminal-native system for managing projects, goals, tasks, books, schedules, daily priorities, and history.

Voyage's command language is inspired by the language of a voyage.

However, nautical terminology is used selectively. It is primarily applied to the **daily lifecycle of tasks**, where the metaphor is most useful.

The core task commands are:

```text
board
dock
anchor
maroon
```

History is accessed through:

```text
log
```

The central philosophy is:

> **Persistent entities describe the user's ongoing work. Daily context describes what the user is actively working on today.**

---

# 2. The Task Lifecycle

Tasks are the primary unit of daily work in Voyage.

A task has a persistent identity, but its **active daily context has a 24-hour lifespan**.

The lifecycle is:

```text
                         ┌─────────────┐
                         │             │
                         ▼             │
                     ┌────────┐        │
                     │ ACTIVE │────────┤
                     └────────┘        │
                         │             │
                 ┌───────┼───────┐     │
                 ▼       ▼       ▼     │
               DOCK    ANCHOR  MAROON  │
                 │       │       │      │
                 ▼       ▼       ▼      │
             COMPLETED PAUSED ABANDONED│
                                       │
                         24h expires ──┘
                              │
                              ▼
                           TOMORROW
```

The commands represent explicit decisions:

| Command  | Meaning                           |
| -------- | --------------------------------- |
| `board`  | Begin today's work on a task      |
| `dock`   | Complete a task                   |
| `anchor` | Intentionally pause a task        |
| `maroon` | Intentionally abandon a task      |
| `log`    | View the history of these actions |

---

# 3. `board`

## Purpose

`board` places a task into today's active context.

If the task does not already exist, `board` creates it.

Therefore, creating a task and adding it to today's work are **one operation**.

```bash
voy board "<task>"
```

Example:

```bash
voy board "Wash gate"
```

This creates the task:

```text
Wash gate
```

and immediately makes it part of today's active work.

There is intentionally no requirement to first create a task and then board it.

### Why?

The user's natural interaction should be:

> "I need to wash the gate."

not:

```bash
voy task create "Wash gate"
voy board "Wash gate"
```

Voyage should minimize the distance between **intention** and **action**.

---

## 3.1 Board a task belonging to a project

A task may optionally be associated with a project:

```bash
voy board "Fix contact normalization" --project Sherlock
```

The task is:

1. created
2. associated with Sherlock
3. placed into today's active context

in a single operation.

---

## 3.2 Board an existing task

If a persistent task already exists but is not currently active:

```bash
voy board "Wash gate"
```

brings it into today's context.

`board` therefore has two possible effects:

```text
Task does not exist
        ↓
Create task
        ↓
Board task


Task already exists
        ↓
Board existing task
```

---

# 4. `dock`

## Purpose

`dock` marks a task as completed.

```bash
voy dock "<task>"
```

Example:

```bash
voy dock "Wash gate"
```

This indicates that the intended work has been completed.

The completion is recorded in the history.

Example:

```text
09:32  BOARDED  Wash gate
11:04  DOCKED   Wash gate
```

Once docked, the task does not roll forward into the next day.

---

# 5. `anchor`

## Purpose

`anchor` intentionally pauses a task.

```bash
voy anchor "<task>"
```

Example:

```bash
voy anchor "Study SQL"
```

Anchoring means:

> This work is not being pursued right now, but I have not abandoned it.

This is different from simply leaving a task unfinished.

### Unfinished task

If the user does nothing:

```text
Today
  [ ] Study SQL
```

the task is carried forward into the next day's context.

### Anchored task

If the user explicitly anchors it:

```bash
voy anchor "Study SQL"
```

the user has made a deliberate decision to pause the work.

The event is recorded in the log.

---

# 6. `maroon`

## Purpose

`maroon` intentionally abandons a task.

```bash
voy maroon "<task>"
```

Example:

```bash
voy maroon "Build mobile app"
```

Marooning means:

> This work is no longer worth pursuing.

A marooned task is **not deleted**.

Its history remains available.

This distinction is important because abandoning work is itself meaningful information.

For example:

```text
13:40  MAROONED  Build mobile app
```

The task may also record an optional reason:

```bash
voy maroon "Build mobile app" --reason "Scope became too large"
```

The reason becomes part of the historical record.

---

# 7. Daily Task Rollover

Tasks are designed around a 24-hour daily working window.

A task that remains active when the day ends is carried forward.

For example:

### August 19

```text
TODAY

[ ] Write commands documentation
[ ] Study SQL
[ ] Wash gate
```

If `Wash gate` is docked:

```bash
voy dock "Wash gate"
```

it is completed.

If `Study SQL` is anchored:

```bash
voy anchor "Study SQL"
```

it is intentionally paused.

If `Write commands documentation` remains unfinished, Voyage carries it forward.

### August 20

```text
TODAY

[ ] Write commands documentation
```

The task itself has not been recreated.

Its **daily context has moved forward**.

This distinction allows Voyage to preserve both:

* the persistent identity of the task
* the history of which days it remained active

---

# 8. Tasks and Persistent Entities

Tasks are not the only entities in Voyage.

Voyage also contains persistent entities such as:

```text
Projects
Goals
Books
Recurring Tasks
Schedules
```

These entities do not use the same lifecycle as daily tasks.

The nautical task vocabulary therefore should not be forced onto every entity.

For example:

```bash
voy board "Fix webhook"
```

is natural because the command represents an action being brought into today's work.

But a project remains a project:

```bash
voy project ...
```

A goal remains a goal:

```bash
voy goal ...
```

A book remains a book:

```bash
voy book ...
```

The nautical vocabulary describes **the user's relationship with active work**, rather than the structure of the entire database.

---

# 9. Projects

Projects represent persistent bodies of related work.

Example:

```text
Sherlock
├── Goal: Launch Sherlock
├── Fix contact normalization
├── Add lecturer search
└── Deploy to Raspberry Pi
```

Projects persist independently of daily context.

A task can belong to a project while still being boarded for a particular day:

```bash
voy board "Fix contact normalization" --project Sherlock
```

The project remains persistent while the task participates in today's context.

---

# 10. Goals

Goals represent desired outcomes.

A goal answers:

> **What am I ultimately trying to accomplish?**

A task answers:

> **What am I doing today to move toward it?**

For example:

```text
Goal
└── Launch Sherlock

Tasks
├── Fix contact normalization
├── Add lecturer search
└── Deploy to Raspberry Pi
```

Goals are persistent and are not subject to the 24-hour task lifecycle.

A goal may have many tasks associated with it over time.

---

# 11. Books

Books represent sources of knowledge or learning material.

For example:

```text
Designing Data-Intensive Applications
```

Books are persistent entities and should not be treated as daily tasks.

Reading a book may generate tasks or daily work:

```bash
voy board "Read chapter 5 of DDIA"
```

The book itself remains persistent.

This allows Voyage to distinguish between:

```text
BOOK
Designing Data-Intensive Applications

TASK
Read chapter 5
```

The book is the persistent source.

The task represents today's intended action.

---

# 12. `log`

## Purpose

`log` displays the historical record of the user's activity.

```bash
voy log
```

The log records meaningful events such as:

```text
BOARDED
DOCKED
ANCHORED
MAROONED
```

Example:

```text
VOYAGE LOG

19 AUG 2026

09:32  BOARDED   Wash gate
10:15  BOARDED   Write commands documentation
11:04  DOCKED    Wash gate
12:10  ANCHORED  Study SQL
13:40  MAROONED  Old mobile app
```

The log is not simply a list of completed tasks.

It is a **record of the user's journey through their work**.

---

# 13. System-Generated History

Not every event in the log must correspond to a user command.

Voyage may generate historical events automatically.

For example, when an unfinished task moves into the next day:

```text
20 AUG 2026

00:00  CARRIED   Write commands documentation
```

`CARRIED` is not a user command.

It is a system-generated event representing the daily rollover.

The user therefore interacts with a small command vocabulary while Voyage can maintain a richer internal history.

---

# 14. Command Philosophy

Voyage commands should follow several principles.

## 14.1 Commands should represent intent

The CLI should model what the user is trying to accomplish.

```bash
voy board "Wash gate"
```

is preferable to:

```bash
voy task create "Wash gate"
voy task activate "Wash gate"
```

The latter exposes implementation steps that the user should not need to understand.

---

## 14.2 One command should perform one meaningful action

```bash
voy board ...
voy dock ...
voy anchor ...
voy maroon ...
```

Each command represents a meaningful decision about work.

---

## 14.3 Nautical vocabulary should remain limited

Voyage should not turn every operation into nautical terminology.

The vocabulary is deliberately restricted to:

```text
board
dock
anchor
maroon
log
```

These words are reserved for concepts where the metaphor improves understanding.

---

## 14.4 Persistent work and daily context must remain distinct

A task can persist while its daily context changes.

For example:

```text
Persistent task
    "Write commands documentation"
          │
          ├── Aug 19 → active
          ├── Aug 20 → carried forward
          └── Aug 21 → completed
```

This allows Voyage to preserve history without forcing the user to recreate unfinished work every morning.

---

# 15. Initial Command Set

The initial Voyage command vocabulary is therefore intentionally small:

```text
voy board "<task>"
voy dock "<task>"
voy anchor "<task>"
voy maroon "<task>"
voy log
```

Everything else in Voyage should be designed around these core concepts rather than expanding the vocabulary unnecessarily.

> **Board what you intend to do.
> Dock what you finish.
> Anchor what you pause.
> Maroon what you abandon.
> Log what happened.**

