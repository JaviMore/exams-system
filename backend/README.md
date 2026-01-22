# Exams System - Backend

Backend API built with FastAPI for the online exams system.

## Features

- 🔐 JWT Authentication
- 👥 User registration and login
- 📝 Complete CRUD for exams
- 📊 Results system
- 🔒 User roles (admin/student)
- 🗄️ SQLite/PostgreSQL database

## Requirements

- Python 3.8+
- pip

## Installation

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configurations
```

4. Start the server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: http://localhost:8000

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Main Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - Login (returns JWT token)
- `GET /api/auth/me` - Current user information

### Exams
- `GET /api/exams/` - List exams
- `GET /api/exams/{id}` - Get exam (without correct answers)
- `GET /api/exams/{id}/full` - Get complete exam (admin)
- `POST /api/exams/` - Create exam (admin)
- `PUT /api/exams/{id}` - Update exam (admin)
- `DELETE /api/exams/{id}` - Delete exam (admin)

### Results
- `POST /api/results/` - Submit exam answers
- `GET /api/results/my` - My results
- `GET /api/results/{id}` - Result detail
- `GET /api/results/` - All results (admin)
- `DELETE /api/results/{id}` - Delete result (admin)

## Create Administrator User

To create an administrator user, you can use the initialization script or connect directly to the database:

```python
# In a Python session
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

db = SessionLocal()
admin = User(
    email="admin@example.com",
    hashed_password=get_password_hash("admin123"),
    full_name="Administrator",
    is_admin=True
)
db.add(admin)
db.commit()
```

## Import Exams from JSON

Exams can be imported using the POST /api/exams/ API with the following format:

```json
{
  "title": "Exam Title",
  "durationMinutes": 30,
  "questions": [
    {
      "question": "Question text?",
      "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
      "correctAnswer": 0,
      "explanation": "Explanation here"
    }
  ]
}
```

## Project Structure

```
backend/
├── app/
│   ├── api/              # Endpoints
│   │   ├── auth.py
│   │   ├── exams.py
│   │   └── results.py
│   ├── core/             # Configuration
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   ├── models/           # SQLAlchemy Models
│   │   ├── user.py
│   │   ├── exam.py
│   │   ├── question.py
│   │   └── result.py
│   ├── schemas/          # Pydantic Schemas
│   │   ├── user.py
│   │   ├── exam.py
│   │   └── result.py
│   └── main.py          # Main application
├── requirements.txt
├── .env.example
└── README.md
```

## Development

For development with hot-reload:
```bash
uvicorn app.main:app --reload
```

## Testing

```bash
pytest
```

## Production

For production, use gunicorn:
```bash
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Database Migrations

If you switch to PostgreSQL and want to use Alembic for migrations:

```bash
# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```
