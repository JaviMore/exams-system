# 🚀 Inicio Rápido - Exams System

## Estado Actual

✅ Backend corriendo en http://127.0.0.1:8000
✅ Frontend corriendo en http://localhost:5173
✅ Usuario administrador creado

## Credenciales de Administrador

```
Email: admin@example.com
Password: admin123
```

## Acceso a la Aplicación

1. Abre tu navegador en: http://localhost:5173
2. Inicia sesión con las credenciales de administrador
3. Desde el panel de administrador puedes:
   - Crear nuevos exámenes
   - Ver todos los resultados
   - Gestionar usuarios

## Crear Más Usuarios

Los usuarios pueden registrarse directamente desde la aplicación en:
http://localhost:5173/register

## Importar Exámenes Existentes

Si tienes exámenes en formato JSON en la carpeta `/exams`, puedes importarlos:

```bash
cd backend
venv/bin/python import_exams.py ../exams
```

## Comandos Útiles

### Iniciar los Servidores

```bash
# Backend
cd backend
venv/bin/uvicorn app.main:app --reload

# Frontend (en otra terminal)
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm use 18
cd frontend
npm run dev
```

### Ver Logs en Tiempo Real

```bash
# Backend
tail -f backend/backend.log

# Frontend
tail -f frontend/frontend.log
```

### Detener los Servidores

```bash
# Encuentra los procesos
ps aux | grep uvicorn
ps aux | grep vite

# O simplemente:
lsof -ti:8000 | xargs kill -9  # Backend
lsof -ti:5173 | xargs kill -9  # Frontend
```

## URLs Importantes

- **Frontend**: http://localhost:5173
- **Backend API**: http://127.0.0.1:8000
- **Documentación API (Swagger)**: http://127.0.0.1:8000/docs
- **Documentación API (ReDoc)**: http://127.0.0.1:8000/redoc

## Estructura de la Aplicación

```
exams-system/
├── backend/           # API FastAPI
│   ├── app/
│   │   ├── api/      # Endpoints
│   │   ├── core/     # Configuración y seguridad
│   │   ├── models/   # Modelos de base de datos
│   │   └── schemas/  # Schemas de validación
│   ├── venv/         # Entorno virtual Python
│   └── exam_system.db  # Base de datos SQLite
├── frontend/          # Aplicación React
│   ├── src/
│   │   ├── pages/    # Páginas de la app
│   │   ├── components/  # Componentes reutilizables
│   │   ├── services/    # Cliente API
│   │   └── context/     # Estado global
│   └── node_modules/
└── exams/            # Exámenes en formato JSON
```

## Solución de Problemas

### Error: "Address already in use"

```bash
# Matar proceso en puerto 8000
lsof -ti:8000 | xargs kill -9

# Matar proceso en puerto 5173
lsof -ti:5173 | xargs kill -9
```

### Error: "Module not found"

```bash
# Backend
cd backend
venv/bin/pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### Error con bcrypt

Si ves errores relacionados con bcrypt, asegúrate de usar Python 3.8:

```bash
cd backend
rm -rf venv
python3.8 -m venv venv
venv/bin/pip install -r requirements.txt
```

### Error con Node.js

Si ves errores de sintaxis con Vite, asegúrate de usar Node 18+:

```bash
# Instalar NVM si no lo tienes
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Cargar NVM
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Instalar Node 18
nvm install 18
nvm use 18
```

## Próximos Pasos

1. **Crear Exámenes**: Usa el panel de administrador para crear exámenes nuevos
2. **Importar Exámenes**: Si tienes exámenes JSON, impórtalos con `import_exams.py`
3. **Invitar Usuarios**: Comparte el link de registro con los estudiantes
4. **Revisar Resultados**: Ve los resultados en el panel de administrador

## Notas Importantes

- ⚠️ **Python 3.13 NO es compatible** - Usa Python 3.8
- ⚠️ **Node.js debe ser 18+** - Usa NVM para gestionar versiones
- ✅ La base de datos se crea automáticamente al iniciar el backend
- ✅ Los tokens JWT expiran después de 7 días
- ✅ Las contraseñas se hashean con bcrypt
