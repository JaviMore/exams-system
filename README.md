# Exams System - Production Application

Complete online exams system with separated frontend and backend architecture.

## 🏗️ Architecture

### Backend (FastAPI + Python)
- **Framework**: FastAPI
- **Database**: SQLite (easily migratable to PostgreSQL)
- **Authentication**: JWT (JSON Web Tokens)
- **ORM**: SQLAlchemy
- **API Documentation**: Automatic Swagger UI

### Frontend (React + Vite)
- **Framework**: React 18
- **Build Tool**: Vite
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **State**: Context API

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

## 🚀 Quick Installation

### 1. Clone the repository
```bash
cd exams-system
```

### 2. Configure Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your configurations

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend available at: http://localhost:8000
API Documentation: http://localhost:8000/docs

### 3. Configure Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend available at: http://localhost:5173

## 👤 Create Administrator User

To create an administrator user, you can use the included script:

```bash
cd backend
source venv/bin/activate
python create_admin.py admin@example.com admin123 "Administrator"
```

## 📥 Import Existing Exams

To import exams from the previous system:

```bash
cd backend
source venv/bin/activate

# Import all exams from the exams/ folder
python import_exams.py ../exams

# Or import a specific file
python import_exams.py ../exams/dp900-exam-a.json
```

## 📚 Features

### Students
- ✅ Registration with email and password
- ✅ Login with JWT authentication
- ✅ View available exams
- ✅ Take exams with timer
- ✅ Navigate between questions
- ✅ Mark questions for review
- ✅ View detailed results with explanations
- ✅ Exam history
- ✅ Download reports

### Administrators
- ✅ Administration panel
- ✅ Create exams manually
- ✅ Import exams from JSON
- ✅ Manage exams
- ✅ View all results
- ✅ Delete exams and results

## 🗄️ Database Structure

### Tables

**users**
- id (PK)
- email (unique)
- hashed_password
- full_name
- is_admin
- is_active
- created_at, updated_at

**exams**
- id (PK)
- title
- duration_minutes
- created_at, updated_at

**questions**
- id (PK)
- exam_id (FK)
- question (text)
- options (JSON array)
- correct_answer (int)
- explanation (text)
- question_order

**results**
- id (PK)
- user_id (FK)
- exam_id (FK)
- answers (JSON)
- score (float)
- correct_answers (int)
- total_questions (int)
- created_at

## 🔐 Security

- Passwords hashed with bcrypt
- JWT tokens with configurable expiration (7 days by default)
- Authentication middleware on all protected routes
- User roles (admin/student)
- CORS configured
- Data validation with Pydantic

## 📝 JSON Format for Importing Exams

```json
{
  "title": "DP-900 Practice Exam",
  "durationMinutes": 45,
  "questions": [
    {
      "question": "What is Azure SQL Database?",
      "options": [
        "A managed relational database service",
        "A NoSQL database",
        "A file storage service",
        "A virtual machine"
      ],
      "correctAnswer": 0,
      "explanation": "Azure SQL Database is a fully managed relational database service..."
    }
  ]
}
```

## 🚀 Quick Start with Scripts

### Start everything with one command:
```bash
./start.sh
```

This script:
1. Configures the backend (creates venv, installs dependencies)
2. Configures the frontend (installs node_modules)
3. Starts both servers
4. Shows PIDs and log paths

### Stop servers:
```bash
./stop.sh
```


## 🌐 Production Deployment

### Backend (Railway, Render, Heroku, Azure)

1. Configure environment variables:
```
DATABASE_URL=postgresql://user:pass@host/db  # For PostgreSQL
SECRET_KEY=your-secure-secret-key
BACKEND_CORS_ORIGINS=https://your-frontend.com
```

2. For PostgreSQL, add to requirements.txt:
```
psycopg2-binary==2.9.9
```

3. Deploy from Git or CLI

### Frontend (Netlify, Vercel, GitHub Pages, Azure Static Web Apps)

1. Update API_URL in `frontend/src/services/api.js`:
```javascript
const API_URL = 'https://your-backend.com/api';
```

2. Build:
```bash
cd frontend
npm run build
```

3. Deploy `dist/` folder

#### Netlify
```bash
npm install -g netlify-cli
netlify deploy --prod --dir=dist
```

#### Vercel
```bash
npm install -g vercel
vercel --prod
```

## 📊 Data Migration

To migrate data from the old system:

```bash
cd backend
source venv/bin/activate
python migrate_data.py
```

This script:
1. Migrates all exams and questions
2. Creates users from old results
3. Assigns default password: `password123`

## 🧪 Testing

### Backend
```bash
cd backend
source venv/bin/activate
pytest
```

### Frontend
```bash
cd frontend
npm test
```

## 📖 API Documentation

Interactive documentation available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Main Endpoints

#### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - Login (returns JWT token)
- `GET /api/auth/me` - Current user information

#### Exams
- `GET /api/exams/` - List exams
- `GET /api/exams/{id}` - Get exam (without correct answers)
- `GET /api/exams/{id}/full` - Get complete exam (admin)
- `POST /api/exams/` - Create exam (admin)
- `PUT /api/exams/{id}` - Update exam (admin)
- `DELETE /api/exams/{id}` - Delete exam (admin)

#### Results
- `POST /api/results/` - Submit exam answers
- `GET /api/results/my` - My results
- `GET /api/results/{id}` - Result detail
- `GET /api/results/` - All results (admin)
- `DELETE /api/results/{id}` - Delete result (admin)

## 🛠️ Technologies Used

### Backend
- **FastAPI** - Modern and fast web framework
- **SQLAlchemy** - ORM for Python
- **Pydantic** - Data validation
- **python-jose** - JWT tokens
- **passlib** - Password hashing
- **uvicorn** - ASGI server

### Frontend
- **React 18** - UI Library
- **Vite** - Build tool
- **React Router v6** - Routing
- **Axios** - HTTP client
- **CSS3** - Modern styles

## 📁 Project Structure

```
exams-system/
├── backend/
│   ├── app/
│   │   ├── api/           # Endpoints
│   │   ├── core/          # Config, DB, Security
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic schemas
│   │   └── main.py        # Main app
│   ├── create_admin.py    # Script to create admin
│   ├── import_exams.py    # Script to import exams
│   ├── migrate_data.py    # Migration script
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── components/    # Components
│   │   ├── context/       # Context API
│   │   ├── pages/         # Pages
│   │   ├── services/      # API calls
│   │   ├── styles/        # CSS
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── README.md
├── exams/                 # JSON exams
├── scripts/               # Useful scripts
└── README.md
```

## 🤝 Contributing

1. Fork the project
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is under the MIT license.

## 🆘 Support

For issues or questions:
- Open an issue on GitHub
- Documentation: See README in backend/ and frontend/

## ⚙️ Advanced Configuration

### Backend Environment Variables

Edit `backend/.env`:

```env
DEBUG=True
DATABASE_URL=sqlite:///./exam_system.db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
BACKEND_CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Switch to PostgreSQL

1. Update `DATABASE_URL` in `.env`:
```
DATABASE_URL=postgresql://user:password@localhost/exam_system
```

2. Add to `requirements.txt`:
```
psycopg2-binary==2.9.9
```

3. Reinstall dependencies:
```bash
pip install -r requirements.txt
```

## 🔄 Changelog

### v1.0.0 (2024)
- ✨ Complete JWT authentication system
- ✨ Complete CRUD for exams
- ✨ Results system with details
- ✨ Administration panel
- ✨ JSON exam import
- ✨ React Frontend with Vite
- ✨ FastAPI Backend
- ✨ Migration and utility scripts
- ✨ Docker support
- ✨ Complete documentation
