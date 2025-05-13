# Lucid Financials

A simple FastAPI-based project for user registration, authentication, and post management.

## Features

- User registration and login with JWT authentication
- Secure password hashing
- Create, view, and delete posts
- Caching for user posts
- SQLAlchemy ORM models and Pydantic schemas

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/OstapTelychko/Lucid-Financials
   cd Lucid-Financials
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   uvicorn project.main:app --reload
   ```

## Notes

- All required Python libraries are listed in `requirements.txt`.  
- Make sure to configure your database and environment variables as needed.

---