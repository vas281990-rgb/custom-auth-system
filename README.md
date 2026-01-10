# Custom Authentication & Authorization System (FastAPI)

## 📌 Project Overview

This project is a custom-built backend authentication and authorization system implemented with **FastAPI** and **SQLAlchemy**, without using ready-made authentication frameworks.

The main goal is to demonstrate the ability to design and implement:
- a custom authentication mechanism
- role-based access control (RBAC)
- permission-based resource protection
- secure user lifecycle management

---

## 🔐 Authentication

### Registration
Users can register by providing:
- full name
- email
- password

Passwords are securely hashed before being stored in the database.

### Login
Users authenticate using email and password.
After successful login, the system issues a **JWT access token**.

### Logout
Logout is implemented using a stateless JWT approach.
The client invalidates the session by removing the token.

### User Identification
All protected endpoints identify users via JWT tokens.

---

## 👤 User Management

- Users can view their own profile
- Admin users can view all users
- User deletion is implemented as **soft delete**
  - `is_deleted = true`
  - `is_active = false`
- Deleted users cannot log in again

---

## 🛂 Authorization (RBAC)

The system uses **Role-Based Access Control** with fine-grained permissions.

### Database Structure
- `users`
- `roles`
- `permissions`
- `user_roles` (many-to-many)
- `role_permissions` (many-to-many)

### Access Rules
- If the user is not authenticated → **401 Unauthorized**
- If the user is authenticated but lacks permission → **403 Forbidden**
- Only users with appropriate permissions can access protected resources

---

## 🧑‍💼 Admin Capabilities

Admin users can:
- access protected endpoints
- manage users
- control access to resources via permissions

Initial roles and permissions are seeded into the database for demonstration.

---

## 🏗️ Business Resources

The system protects application resources using permissions.
Access to each resource is granted only if the user has the required permission.

---

## 🚀 Tech Stack

- Python
- FastAPI
- SQLAlchemy
- JWT
- PostgreSQL / SQLite
- Alembic

---

## ✅ Key Features Summary

- Custom authentication (no built-in auth frameworks)
- JWT-based security
- Soft delete for users
- Role & permission management
- Clear separation of concerns (routers, services, models)
- Ready for extension and scaling

---

## 🧠 Design Philosophy

This project prioritizes:
- explicit access control
- predictable security behavior
- readable and maintainable code
- real-world backend architecture
