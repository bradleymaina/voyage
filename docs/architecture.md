# Voyage Architecture

## 1. Overview

Voyage is a terminal-native personal context management system.

Its architecture separates:

- user interaction
- application logic
- domain logic
- data persistence

The high-level architecture is:

```text
User
  │
  ▼
CLI
  │
  ▼
Application
  │
  ▼
Domain
  │
  ▼
Storage
  │
  ▼
SQLite
```
## 2. Architectural Layers
CLI

The purpose is to be the interface between the user and  voyage . 
Responsibilities include : 
- Parse commands and aruguments
- Validate cli input
- Display results
- Format terminal output


APPLICATION 

Coordinates operations requested by the user 
Responsibilities:
- Coordinate workflows
- Call domain operations
- Coordinate repositories
- Handle application-level  logic

Example Operations: 
- Create a Project 
- Add a task 
- Record Progress
- Complete a taks
- Retrieve current focus

DOMAIN

Core concepts and rules of voyage 
Example:
- Projects
- Tasks
- Progress

STORAGE

Handles Persistence

