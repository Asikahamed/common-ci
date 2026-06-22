Controller
↓
Service
↓
Repository

Avoid:
- Controller → Repository
- Circular dependencies
- God classes

Prefer:
- Constructor injection
- DTO boundaries
- Separation of concerns