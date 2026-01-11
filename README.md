# Custom Authentication & Authorization System (FastAPI)

##  Project Overview
This is a custom-built backend authentication and authorization system. The primary goal was to design a secure, scalable architecture from scratch without relying on high-level "magic" frameworks. It features a complete **Role-Based Access Control (RBAC)** system and secure user lifecycle management.

##  Core Logic & Design Philosophy
This project prioritizes:
- **Granular Access Control:** Rights are tied to specific permissions, not just generic roles.
- **Predictable Security:** Explicit checks for every protected resource.
- **Clean Architecture:** Strict separation between models, services, and API routes.

---

##  Key Features

### Authentication
- **Secure Registration:** Includes password hashing (Argon2) and password confirmation validation.
- **JWT Protection:** Uses JSON Web Tokens for stateless authentication.
- **User Identification:** Every request is context-aware, identifying the user via the `sub` claim in the JWT.

### User Management
- **Profile Access:** Users can view and manage their own data.
- **Soft Delete Logic:** Users are never fully "purged" from the DB. Instead:
  - `is_deleted` is set to `True`
  - `is_active` is set to `False`
  - This ensures data integrity while preventing any further access for the user.

### RBAC System (Role-Based Access Control)
The system uses a 5-table relational structure to manage access:
- `users` ↔ `roles` (Many-to-Many via `user_roles`)
- `roles` ↔ `permissions` (Many-to-Many via `role_permissions`)

**Access Rules:**
- **401 Unauthorized:** No valid token provided.
- **403 Forbidden:** Authenticated, but missing the specific required permission (e.g., `reports:read`).

---

## 🏗️ Database Architecture


The database schema is designed to be highly flexible. Permissions (e.g., `users:delete`) are linked to Roles (e.g., `Admin`), which are then assigned to Users. This allows for easy permission updates without changing the application code.

---

##  Tech Stack
- **Python / FastAPI:** High-performance web framework.
- **SQLAlchemy:** SQL Toolkit and Object-Relational Mapper (ORM).
- **Argon2:** Modern, secure password hashing algorithm.
- **SQLite:** Lightweight database for development and demonstration.

---

## How to Setup and Run

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
Initialize Database & Seed Data: This script creates the database structure and adds the default Admin user (admin@example.com / admin123) and initial roles:

Bash
PYTHONPATH=. python3 setup_db.py
Launch the Server:

Bash
uvicorn app.main:app --reload
Interactive Documentation: Once running, visit http://127.0.0.1:8000/docs to test all endpoints using the Swagger UI.

Created as a demonstration of secure backend architecture.