# Exams System - Aplicación Productiva

Sistema completo de exámenes online con arquitectura separada en frontend y backend.

## 🏗️ Arquitectura

### Backend (FastAPI + Python)
- **Framework**: FastAPI
- **Base de datos**: SQLite (fácilmente migrable a PostgreSQL)
- **Autenticación**: JWT (JSON Web Tokens)
- **ORM**: SQLAlchemy
- **Documentación API**: Swagger UI automática

### Frontend (React + Vite)
- **Framework**: React 18
- **Build Tool**: Vite
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **Estado**: Context API

## 📋 Requisitos Previos

- Python 3.8+
- Node.js 16+
- npm o yarn

## 🚀 Instalación Rápida

### 1. Clonar el repositorio
```bash
cd exams-system
```

### 2. Configurar Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones

# Iniciar servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend disponible en: http://localhost:8000
Documentación API: http://localhost:8000/docs

### 3. Configurar Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

Frontend disponible en: http://localhost:5173

## 👤 Crear Usuario Administrador

Para crear un usuario administrador, puedes usar el script incluido:

```bash
cd backend
source venv/bin/activate
python create_admin.py admin@example.com admin123 "Administrator"
```

## 📥 Importar Exámenes Existentes

Para importar los exámenes del sistema anterior:

```bash
cd backend
source venv/bin/activate

# Importar todos los exámenes de la carpeta exams/
python import_exams.py ../exams

# O importar un archivo específico
python import_exams.py ../exams/dp900-exam-a.json
```

## 📚 Funcionalidades

### Estudiantes
- ✅ Registro con email y contraseña
- ✅ Login con autenticación JWT
- ✅ Ver exámenes disponibles
- ✅ Realizar exámenes con temporizador
- ✅ Navegación entre preguntas
- ✅ Marcar preguntas para revisión
- ✅ Ver resultados detallados con explicaciones
- ✅ Historial de exámenes
- ✅ Descargar reportes

### Administradores
- ✅ Panel de administración
- ✅ Crear exámenes manualmente
- ✅ Importar exámenes desde JSON
- ✅ Gestionar exámenes
- ✅ Ver todos los resultados
- ✅ Eliminar exámenes y resultados

## 🗄️ Estructura de Base de Datos

### Tablas

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

## 🔐 Seguridad

- Passwords hasheados con bcrypt
- Tokens JWT con expiración configurable (7 días por defecto)
- Middleware de autenticación en todas las rutas protegidas
- Roles de usuario (admin/estudiante)
- CORS configurado
- Validación de datos con Pydantic

## 📝 Formato JSON para Importar Exámenes

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

## 🚀 Inicio Rápido con Scripts

### Iniciar todo con un comando:
```bash
./start.sh
```

Este script:
1. Configura el backend (crea venv, instala dependencias)
2. Configura el frontend (instala node_modules)
3. Inicia ambos servidores
4. Muestra los PIDs y rutas de logs

### Detener servidores:
```bash
./stop.sh
```

## 🐳 Docker (Opcional)

### Iniciar con Docker Compose:
```bash
docker-compose up -d
```

### Ver logs:
```bash
docker-compose logs -f
```

### Detener:
```bash
docker-compose down
```

## 🌐 Despliegue en Producción

### Backend (Railway, Render, Heroku, Azure)

1. Configurar variables de entorno:
```
DATABASE_URL=postgresql://user:pass@host/db  # Para PostgreSQL
SECRET_KEY=tu-clave-secreta-segura
BACKEND_CORS_ORIGINS=https://tu-frontend.com
```

2. Para PostgreSQL, añadir a requirements.txt:
```
psycopg2-binary==2.9.9
```

3. Deploy desde Git o CLI

### Frontend (Netlify, Vercel, GitHub Pages, Azure Static Web Apps)

1. Actualizar API_URL en `frontend/src/services/api.js`:
```javascript
const API_URL = 'https://tu-backend.com/api';
```

2. Build:
```bash
cd frontend
npm run build
```

3. Deploy carpeta `dist/`

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

## 📊 Migración de Datos

Para migrar datos del sistema antiguo:

```bash
cd backend
source venv/bin/activate
python migrate_data.py
```

Este script:
1. Migra todos los exámenes y preguntas
2. Crea usuarios a partir de los resultados antiguos
3. Asigna password por defecto: `password123`

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

## 📖 Documentación API

Documentación interactiva disponible en:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints Principales

#### Autenticación
- `POST /api/auth/register` - Registro de usuario
- `POST /api/auth/login` - Login (devuelve JWT token)
- `GET /api/auth/me` - Información del usuario actual

#### Exámenes
- `GET /api/exams/` - Listar exámenes
- `GET /api/exams/{id}` - Obtener examen (sin respuestas correctas)
- `GET /api/exams/{id}/full` - Obtener examen completo (admin)
- `POST /api/exams/` - Crear examen (admin)
- `PUT /api/exams/{id}` - Actualizar examen (admin)
- `DELETE /api/exams/{id}` - Eliminar examen (admin)

#### Resultados
- `POST /api/results/` - Enviar respuestas de examen
- `GET /api/results/my` - Mis resultados
- `GET /api/results/{id}` - Detalle de resultado
- `GET /api/results/` - Todos los resultados (admin)
- `DELETE /api/results/{id}` - Eliminar resultado (admin)

## 🛠️ Tecnologías Utilizadas

### Backend
- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para Python
- **Pydantic** - Validación de datos
- **python-jose** - JWT tokens
- **passlib** - Hashing de passwords
- **uvicorn** - ASGI server

### Frontend
- **React 18** - Librería UI
- **Vite** - Build tool
- **React Router v6** - Routing
- **Axios** - HTTP client
- **CSS3** - Estilos modernos

## 📁 Estructura del Proyecto

```
exams-system/
├── backend/
│   ├── app/
│   │   ├── api/           # Endpoints
│   │   ├── core/          # Config, DB, Security
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic schemas
│   │   └── main.py        # App principal
│   ├── create_admin.py    # Script crear admin
│   ├── import_exams.py    # Script importar exámenes
│   ├── migrate_data.py    # Script migración
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── components/    # Componentes
│   │   ├── context/       # Context API
│   │   ├── pages/         # Páginas
│   │   ├── services/      # API calls
│   │   ├── styles/        # CSS
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── README.md
├── exams/                 # Exámenes JSON
├── docker-compose.yml
├── start.sh              # Script inicio rápido
├── stop.sh               # Script detener
└── README.md
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT.

## 🆘 Soporte

Para problemas o preguntas:
- Abrir un issue en GitHub
- Documentación: Ver README en backend/ y frontend/

## ⚙️ Configuración Avanzada

### Variables de Entorno Backend

Editar `backend/.env`:

```env
DEBUG=True
DATABASE_URL=sqlite:///./exam_system.db
SECRET_KEY=tu-clave-secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
BACKEND_CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Cambiar a PostgreSQL

1. Actualizar `DATABASE_URL` en `.env`:
```
DATABASE_URL=postgresql://user:password@localhost/exam_system
```

2. Añadir a `requirements.txt`:
```
psycopg2-binary==2.9.9
```

3. Reinstalar dependencias:
```bash
pip install -r requirements.txt
```

## 🔄 Changelog

### v1.0.0 (2024)
- ✨ Sistema completo de autenticación JWT
- ✨ CRUD completo de exámenes
- ✨ Sistema de resultados con detalles
- ✨ Panel de administración
- ✨ Importación de exámenes JSON
- ✨ Frontend React con Vite
- ✨ Backend FastAPI
- ✨ Scripts de migración y utilidades
- ✨ Docker support
- ✨ Documentación completa

If that folder doesn't exist or contains no valid files, it will make a second attempt in the current directory (allowing direct use of the included `sample_exam.json`).

Steps to add exams:
1. Create `exams/` folder (optional but recommended).
2. Place one or more `.json` files inside with the correct format (see below).
3. Restart the server (exams are only loaded when the table is empty).

Example execution specifying folder:
```bash
EXAMS_DIR=exams PORT=3000 python3 server.py
```

## How to Use

### Users:
1. Go to http://localhost:3000
2. Enter your name
3. Select an exam
4. Answer the questions
5. View your detailed results
6. Download your report (optional)

### Cookie Persistence
The system uses cookies to improve the experience:
- `examUser`: remembers your name and avoids having to re-enter it (24h).
- `examState`: saves the exam in progress (id, start time and answers) to recover your progress if you accidentally reload the page or close the browser. The remaining time is recalculated on return.
  - If time has already expired on return, results are automatically submitted.
- `backofficeAuth`: keeps the backoffice session active (1h). Logging out removes it.

Limitations: This is not a real security mechanism; cookies are not encrypted. Do not use in production without adding proper authentication and secure expiration on the server.

### Administrators:
1. Go to http://localhost:3000/backoffice.html
2. Login with credentials (default: admin / admin123)
3. **Create Exam**:
   - **Option 1: Import from JSON**
     - Click "Upload JSON File" and select your JSON file
     - Or download the sample JSON template
     - The form will auto-populate with the exam data
   - **Option 2: Create Manually**
     - Enter exam title
     - Add questions with the "+ Add Question" button
     - For each question, complete:
       - Question text
       - 4 options (mark the correct one with the radio button)
       - Explanation
   - Save the exam
4. **View Results**:
   - Check all results
   - Filter by specific exam

## JSON Format for Importing Exams

You can create exams by uploading a JSON file with the following structure:

```json
{
  "title": "Exam Title",
  "durationMinutes": 30,
  "questions": [
    {
      "question": "Question text?",
      "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
      "correctAnswer": 0,
      "explanation": "Explanation for the correct answer"
    }
  ]
}
```

- `title`: String with the exam name
- `questions`: Array of question objects
  - `question`: The question text
  - `options`: Array of exactly 4 options
  - `correctAnswer`: Index (0-3) of the correct option
  - `explanation`: Text explaining why the answer is correct

Additional fields:
- `durationMinutes`: Duration of the exam in minutes (integer). If omitted, defaults to 30.

A sample file (`sample_exam.json`) is included in the project.

## Technologies

- **Backend**: Python 3 (native HTTP server, no frameworks)
- **Frontend**: HTML5, CSS3, vanilla JavaScript
- **Database**: SQLite (persistent local storage)

## Sample Exams
Hardcoded exams are no longer inserted. Instead, place your JSON files in `exams/` or use the existing `sample_exam.json` to initialize the empty database.

## Project Structure

```
forms/
├── server.py             # Python server
├── exam_system.db        # SQLite database (created on first run)
├── README.md             # This file
└── public/
    ├── index.html        # Main page (login + exams)
    ├── backoffice.html   # Administration panel
    └── styles.css        # Application styles
```

## Database

The application uses SQLite to persist data. The database file `exam_system.db` is automatically created on first run with the following tables:

- **exams**: Stores exam information
- **questions**: Stores questions associated with each exam
- **results**: Stores student exam results

All data persists between server restarts.
