# Sweet Shop Management System

## Overview
A full-stack Sweet Shop Management System built with FastAPI (Backend) and React (Frontend).

## Backend Setup
1. Navigate to `backend/`
2. Install dependencies: `pip install -r requirements.txt`
3. Run server: `uvicorn app.main:app --reload`

## AI Usage
### My AI Usage
I used **Google Gemini** (via Antigravity) to assist with the development of this project.

**How I used it:**
- **Project Structure & Planning**: I used Gemini to brainstorm the modular "MNC-style" architecture and create the implementation plan.
- **Boilerplate Generation**: I used Gemini to generate the initial FastAPI setup, including database connection logic and Pydantic models.
- **Test-Driven Development**: I asked Gemini to write failing tests for each module (Auth, Catalog, Inventory) before implementing the logic, ensuring a strict TDD workflow.
- **Debugging**: I used Gemini to troubleshoot dependency issues (e.g., `motor` vs `pymongo` version conflict, `bcrypt` incompatibility with `passlib`).
- **Refactoring**: I used Gemini to refactor the project structure based on feedback to separate concerns into distinct modules.

**Reflection:**
AI significantly accelerated the development process, especially in setting up the boilerplate and writing comprehensive tests. It helped identify and resolve obscure dependency issues quickly. However, manual oversight was crucial to ensure the architecture met specific requirements (like the modular structure) and to verify that the generated code was correct and secure.
