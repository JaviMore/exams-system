# Guía Rápida - Exams System

## 🚀 Instalación en 3 Pasos

### 1. Setup Inicial
```bash
./setup.sh
```

### 2. Crear Admin
```bash
cd backend
source venv/bin/activate
python create_admin.py admin@example.com admin123 "Administrator"
cd ..
```

### 3. Iniciar Aplicación
```bash
./start.sh
```

**Listo!** 
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 📥 Importar Exámenes

```bash
cd backend
source venv/bin/activate
python import_exams.py ../exams
```

---

## 🛑 Detener Aplicación

```bash
./stop.sh
```

---

## 🐳 Con Docker

```bash
# Iniciar
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

---

## 👥 Usuarios por Defecto

Después de crear el admin, usa:
- **Email**: admin@example.com
- **Password**: admin123

Los estudiantes deben registrarse desde el frontend.

---

## 📝 Estructura de Examen JSON

```json
{
  "title": "Mi Examen",
  "durationMinutes": 30,
  "questions": [
    {
      "question": "¿Pregunta?",
      "options": ["Op1", "Op2", "Op3", "Op4"],
      "correctAnswer": 0,
      "explanation": "Explicación aquí"
    }
  ]
}
```

---

## 🔧 Comandos Útiles

### Backend
```bash
cd backend
source venv/bin/activate

# Iniciar servidor
uvicorn app.main:app --reload

# Crear admin
python create_admin.py email@example.com password "Name"

# Importar exámenes
python import_exams.py ruta/al/archivo.json

# Migrar datos antiguos
python migrate_data.py
```

### Frontend
```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar desarrollo
npm run dev

# Build producción
npm run build
```

---

## 📂 Estructura Básica

```
exams-system/
├── backend/           # API FastAPI
│   ├── app/
│   │   ├── api/      # Endpoints
│   │   ├── models/   # Base de datos
│   │   └── schemas/  # Validación
│   └── *.py          # Scripts utilidad
├── frontend/         # React App
│   └── src/
│       ├── pages/    # Páginas
│       └── styles/   # CSS
├── exams/            # JSON exámenes
├── setup.sh          # Instalación
├── start.sh          # Iniciar
└── stop.sh           # Detener
```

---

## 🆘 Problemas Comunes

### Puerto 8000 ocupado
```bash
# Linux/Mac
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Puerto 5173 ocupado
```bash
# Linux/Mac
lsof -ti:5173 | xargs kill -9

# Windows
netstat -ano | findstr :5173
taskkill /PID <PID> /F
```

### Python venv no activa
```bash
cd backend
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Node modules error
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## 📚 Más Información

- README completo: [README.md](README.md)
- Backend docs: [backend/README.md](backend/README.md)
- Frontend docs: [frontend/README.md](frontend/README.md)
- API docs: http://localhost:8000/docs (cuando esté corriendo)
