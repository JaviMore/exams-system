# Exams System - Backend

Backend API construido con FastAPI para el sistema de exámenes online.

## Características

- 🔐 Autenticación JWT
- 👥 Registro y login de usuarios
- 📝 CRUD completo de exámenes
- 📊 Sistema de resultados
- 🔒 Roles de usuario (admin/estudiante)
- 🗄️ Base de datos SQLite/PostgreSQL

## Requisitos

- Python 3.8+
- pip

## Instalación

1. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

4. Iniciar el servidor:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en: http://localhost:8000

## Documentación API

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints Principales

### Autenticación
- `POST /api/auth/register` - Registro de usuario
- `POST /api/auth/login` - Login (devuelve JWT token)
- `GET /api/auth/me` - Información del usuario actual

### Exámenes
- `GET /api/exams/` - Listar exámenes
- `GET /api/exams/{id}` - Obtener examen (sin respuestas correctas)
- `GET /api/exams/{id}/full` - Obtener examen completo (admin)
- `POST /api/exams/` - Crear examen (admin)
- `PUT /api/exams/{id}` - Actualizar examen (admin)
- `DELETE /api/exams/{id}` - Eliminar examen (admin)

### Resultados
- `POST /api/results/` - Enviar respuestas de examen
- `GET /api/results/my` - Mis resultados
- `GET /api/results/{id}` - Detalle de resultado
- `GET /api/results/` - Todos los resultados (admin)
- `DELETE /api/results/{id}` - Eliminar resultado (admin)

## Crear Usuario Administrador

Para crear un usuario administrador, puedes usar el script de inicialización o conectarte directamente a la base de datos:

```python
# En una sesión de Python
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

## Importar Exámenes desde JSON

Los exámenes pueden importarse usando la API POST /api/exams/ con el siguiente formato:

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

## Estructura del Proyecto

```
backend/
├── app/
│   ├── api/              # Endpoints
│   │   ├── auth.py
│   │   ├── exams.py
│   │   └── results.py
│   ├── core/             # Configuración
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   ├── models/           # Modelos SQLAlchemy
│   │   ├── user.py
│   │   ├── exam.py
│   │   ├── question.py
│   │   └── result.py
│   ├── schemas/          # Schemas Pydantic
│   │   ├── user.py
│   │   ├── exam.py
│   │   └── result.py
│   └── main.py          # Aplicación principal
├── requirements.txt
├── .env.example
└── README.md
```

## Desarrollo

Para desarrollo con hot-reload:
```bash
uvicorn app.main:app --reload
```

## Testing

```bash
pytest
```

## Producción

Para producción, usa gunicorn:
```bash
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Migraciones de Base de Datos

Si cambias a PostgreSQL y quieres usar Alembic para migraciones:

```bash
# Inicializar Alembic
alembic init alembic

# Crear migración
alembic revision --autogenerate -m "Initial migration"

# Aplicar migración
alembic upgrade head
```
