# Spring Boot Architecture Skill

Expected patterns:

Controller
 ↓
Service
 ↓
Repository

Guidelines:

- Controllers should not access repositories directly.
- Business logic belongs in services.
- Repository layer handles persistence only.
- Avoid circular dependencies.
- Prefer constructor injection.
- Minimize shared mutable state.
- Avoid god classes.