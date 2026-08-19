# Voyage Concepts

Voyage is a personal context management system.

Its purpose is to bring together the different things the user is
working toward and produce a useful picture of what should be done
today.

The core concepts of Voyage are:

- Projects
- Goals
- Tasks
- Recurring Tasks
- Miscellaneous Work
- Context
- History

---

## 1. Projects

A project is something the user is working on that requires sustained
attention over time.

A project does not have to have a predefined lifespan or completion
date. It may continue indefinitely.

Examples:

- Voyage
- Sherlock
- hwcheck
- Learning C
- NSE quantitative trading

Projects are primarily organizational structures for long-running work.

A project itself is not necessarily something that appears directly in
the user's daily context.

Instead, work associated with a project can be broken down into tasks
that eventually become part of the user's daily context.

For example:

    Project: Voyage

    Tasks:
        - Write architecture.md
        - Define core concepts
        - Implement CLI
        - Build storage layer

The project provides the larger context for the tasks.

---

## 2. Goals

A goal is a desired outcome that the user wants to achieve.

Goals describe what the user wants to accomplish rather than the
specific work required to accomplish it.

Examples:

- Read 5 books before the end of the year
- Learn about the NSE
- Become proficient in C
- Earn 100,000 KES

A goal may have a target, deadline, or measurable outcome.

Goals can generate or be supported by tasks.

For example:

    Goal:
        Read 5 books before the end of the year

    Related work:
        - Read DDIA
        - Read book X
        - Read book Y

The goal represents the desired outcome while the tasks represent
actions that contribute toward it.

---

## 3. Tasks

A task is an actionable unit of work.

Tasks are generally smaller and more immediately actionable than
projects.

A task can be:

- Completed
- Repeated
- Scheduled
- Associated with a project
- Associated with a goal
- Independent

Examples:

    - Read Sherlock code
    - Implement SQLite storage
    - Fix phone number normalization
    - Read chapter 4 of DDIA
    - Work out for 30 minutes

A task does not necessarily belong to a project.

For example:

    Work out for 30 minutes

can exist as a task without belonging to any project.

---

## 4. Recurring Tasks

A recurring task is a task that is expected to occur repeatedly
according to a defined schedule or recurrence pattern.

Examples:

    Every Tuesday:
        Work out for 30 minutes

    Every Wednesday:
        Read

Recurring tasks are different from ordinary tasks because their
appearance in the user's daily context is determined by their
recurrence rules.

For example:

    Tuesday
        → Work out appears in today's context

    Wednesday
        → Read appears in today's context

The recurrence definition should be persistent, while each occurrence
represents work for a particular day.

---

## 5. Miscellaneous Work

Miscellaneous work represents things the user wants or needs to do
without requiring them to belong to a project or goal.

Examples:

    - Learn systemd
    - curl vs ping
    - Investigate a Linux command
    - Try a new tool

Miscellaneous work is useful for capturing short-lived or
unclassified work.

It prevents the user from having to create a project or goal simply
to record something they want to do today.

---

## 6. Context

Context is the user's actionable picture for a given day.

It is the collection of things the user should consider, work on, or
accomplish during that day.

Context can contain work originating from multiple sources:

    - Recurring tasks
    - Project-related tasks
    - Goal-related work
    - Miscellaneous work

For example:

    voy today

might produce:

    TASKS
        Work out
        Read Sherlock code

    PROJECT WORK
        Begin porting hwcheck to C#

    MISC
        Learn systemd
        curl vs ping

    GOALS
        Read DDIA

Context is therefore not necessarily a permanent entity.

It is a daily view assembled from the user's persistent work,
commitments, goals, and priorities.

The purpose of context is to answer:

    "What should I be doing today?"

---

## 7. History

History represents the record of what the user has done over time.

Voyage should preserve enough historical information to allow the
user to understand their previous activity and progress.

Examples include:

    - Tasks completed
    - Work performed
    - Progress made on projects
    - Progress toward goals
    - Previous daily contexts

History allows Voyage to answer questions such as:

    What did I work on yesterday?

    What have I accomplished on this project?

    When did I last work on this?

    How much progress have I made?

History is important because Voyage is intended to preserve context
and progress, not simply generate a list of tasks.

---

# 8. Relationships Between Concepts

The concepts are related but serve different purposes.

A simplified relationship is:

    Project
       │
       └── produces/contains ──> Tasks

    Goal
       │
       └── can be supported by ──> Tasks

    Recurring Task
       │
       └── generates occurrences ──> Daily Context

    Project Tasks ────────────────┐
    Goal-related Tasks ───────────┤
    Recurring Tasks ──────────────┼──> Daily Context
    Miscellaneous Work ───────────┘

    Completed Work ───────────────> History

The same task may therefore have multiple pieces of context:

    Task
       ├── Project: Sherlock
       ├── Goal: Learn software engineering
       └── Appears in today's context

The project or goal provides meaning and provenance, while the daily
context determines what is relevant to the user today.

---

# 9. Context Is the Central Concept

Although projects, goals, and tasks are persistent concepts, the
primary purpose of Voyage is to bring them together into useful daily
context.

The user should not have to manually inspect every project, goal, and
task to determine what to work on.

Instead:

    Persistent Information
            │
            ▼
    ┌───────────────────────┐
    │       Voyage          │
    │                       │
    │  Projects             │
    │  Goals                │
    │  Tasks                │
    │  Recurrence           │
    │  History              │
    └───────────┬───────────┘
                │
                ▼
          Daily Context
                │
                ▼
            voy today

The daily context is therefore the primary interface between the
user's broader body of work and the work they need to perform today.

---

# 10. Example

Consider the following information:

    Project:
        Voyage

    Goal:
        Read 5 books before the end of the year

    Recurring Tasks:
        Tuesday → Work out for 30 minutes
        Wednesday → Read

    Project Tasks:
        Read Sherlock code
        Begin porting hwcheck to C#

    Miscellaneous:
        Learn systemd
        curl vs ping

On a Tuesday, `voy today` could produce:

    TODAY

    TASKS
        [ ] Work out for 30 minutes
        [ ] Read Sherlock code
        [ ] Begin porting hwcheck to C#

    MISC
        [ ] Learn systemd
        [ ] curl vs ping

    GOALS
        [ ] Read DDIA

The project itself does not need to appear as a daily item.

Instead, its relevant work appears in the context.

---

# 11. Design Principle

Voyage should distinguish between:

    What I am working on
        → Project

    What I want to achieve
        → Goal

    What I need to do
        → Task

    What I repeatedly need to do
        → Recurring Task

    What I want to do without a larger structure
        → Miscellaneous Work

    What matters today
        → Context

    What I have already done
        → History

These distinctions should remain clear throughout the implementation.
