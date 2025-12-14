# Sweet Shop Management System

## Overview
A robust, full-stack **Sweet Shop Management System** built to demonstrate modern development practices, including **Test-Driven Development (TDD)**, modular architecture, and secure API design.

### Tech Stack
- **Backend**: Python (FastAPI), MongoDB (Motor), Pydantic for validation.
- **Frontend**: React (Vite), Tailwind CSS, Lucide Icons.
- **Testing**: `pytest` (Backend), manual verification (Frontend).
- **Authentication**: JWT (JSON Web Tokens).

## Features
- **User Authentication**: Secure Register & Login with JWT.
- **Role-Based Access**: separate tailored experiences for Users and Admins.
- **Sweet Catalog**: Searchable, filterable list of sweets with stock tracking.
- **Order Management**: Users can place orders (atomic stock reduction) and view history.
- **Admin Panel**: Full CRUD for sweets, image uploads (S3), and inventory management.

## Credentials
- **Admin**: admin/Admin@lalsweets9363
- **User**: users can register and login with their credentials

## Screenshots
### Dashboard (Redesigned)
Full-width layout with Quick Actions and Featured Sweets grid.
<img width="1903" height="987" alt="image" src="https://github.com/user-attachments/assets/0eb549a5-cc93-4157-b618-a6c1215492ab" />

### User Profile
Order history and account management.
<img width="1914" height="983" alt="image" src="https://github.com/user-attachments/assets/d2267238-7703-4c25-9806-f54191a924f3" />

### Admin Dashboard
<img width="1902" height="990" alt="image" src="https://github.com/user-attachments/assets/c1c11ace-c170-4bfd-a71f-3e7a3fd91322" />


### Admin Sweet Management
<img width="1919" height="927" alt="image" src="https://github.com/user-attachments/assets/c281f692-7f53-4892-8f67-d5f05aac5e42" />


### Admin Inventory Management
<img width="1919" height="991" alt="image" src="https://github.com/user-attachments/assets/511a0002-1168-4c8f-a434-be5f8aa19cf0" />




## Local Setup Instructions

### Prerequisites
- Python 3.9+
- Node.js 16+
- MongoDB running locally or defined in `.env`.

### 1. Backend Setup
```bash
cd backend
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```
API will be live at `http://localhost:8000`. Documentation at `/docs`.

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Application will be live at `http://localhost:5173`.

## Test Report
The backend was built using a strict TDD "Red-Green-Refactor" cycle.
- **Total Tests**: 20+ passing tests.
- **Coverage**: Auth, Catalog, Admin, Inventory, Orders.
- **Latest Run**: All tests passed (including new security validation rules).

## My AI Usage
I used **Google Gemini** (via Antigravity) extensively as a co-pilot to accelerate development while clearly directing the architectural decisions myself.

### Tools Used
- **Google Gemini**: For code generation, debugging, and TDD workflow.

### How I Used It
1.  **TDD Workflow**: I asked Gemini to write *failing tests* for my `orders` and `auth` modules before writing a single line of implementation code. This enforced strict TDD.
2.  **Boilerplate & Architecture**: I used it to generate the initial file structure and Pydantic schemas, saving hours of manual setup.
3.  **Debugging & Refactoring**: When I encountered dependency conflicts (e.g., `pytest-asyncio` versions), Gemini helped suggest compatible versions.
4.  **UI Design**: I leveraged its ability to generate Tailwind CSS classes to create the modern, responsive Dashboard layout.

### Reflection
AI acted as a "force multiplier," allowing me to focus on high-level logic and security architecture (like enforcing input validation) while it handled the implementation details. It didn't replace my judgment; for instance, I manually corrected its layout suggestions and enforced specific project structure rules.
