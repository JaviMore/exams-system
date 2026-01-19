# Exams System - Frontend

Frontend construido con React + Vite para el sistema de exámenes online.

## Características

- ⚛️ React 18
- ⚡ Vite para desarrollo rápido
- 🎨 CSS moderno y responsivo
- 🔐 Autenticación JWT
- 📱 Diseño responsivo
- 🎯 Navegación con React Router

## Requisitos

- Node.js 16+
- npm o yarn

## Instalación

1. Instalar dependencias:
```bash
npm install
```

2. Configurar variables de entorno (opcional):
Editar `src/services/api.js` si el backend está en una URL diferente.

3. Iniciar servidor de desarrollo:
```bash
npm run dev
```

La aplicación estará disponible en: http://localhost:5173

## Scripts Disponibles

- `npm run dev` - Iniciar servidor de desarrollo
- `npm run build` - Construir para producción
- `npm run preview` - Previsualizar build de producción

## Estructura del Proyecto

```
frontend/
├── public/              # Archivos estáticos
├── src/
│   ├── components/      # Componentes reutilizables
│   │   └── PrivateRoute.jsx
│   ├── context/         # Context API
│   │   └── AuthContext.jsx
│   ├── pages/          # Páginas/Vistas
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   ├── ExamList.jsx
│   │   ├── TakeExam.jsx
│   │   ├── ResultDetail.jsx
│   │   ├── MyResults.jsx
│   │   └── Admin.jsx
│   ├── services/       # Servicios API
│   │   └── api.js
│   ├── styles/         # Estilos CSS
│   │   ├── App.css
│   │   ├── Auth.css
│   │   ├── ExamList.css
│   │   ├── TakeExam.css
│   │   ├── ResultDetail.css
│   │   ├── MyResults.css
│   │   └── Admin.css
│   ├── App.jsx         # Componente principal
│   └── main.jsx        # Punto de entrada
├── index.html
├── package.json
└── vite.config.js
```

## Funcionalidades

### Para Estudiantes
- ✅ Registro e inicio de sesión
- ✅ Ver lista de exámenes disponibles
- ✅ Realizar exámenes con temporizador
- ✅ Navegación entre preguntas
- ✅ Marcar preguntas para revisión
- ✅ Ver resultados detallados
- ✅ Descargar reporte de resultados
- ✅ Historial de exámenes realizados

### Para Administradores
- ✅ Panel de administración
- ✅ Crear exámenes manualmente
- ✅ Importar exámenes desde JSON
- ✅ Gestionar exámenes existentes
- ✅ Ver todos los resultados
- ✅ Eliminar exámenes y resultados

## Formato JSON para Importar Exámenes

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

## Rutas de la Aplicación

- `/login` - Página de inicio de sesión
- `/register` - Página de registro
- `/` - Lista de exámenes (requiere autenticación)
- `/exam/:id` - Realizar examen (requiere autenticación)
- `/results` - Mis resultados (requiere autenticación)
- `/results/:id` - Detalle de resultado (requiere autenticación)
- `/admin` - Panel de administración (requiere ser admin)

## Desarrollo

El proyecto usa Vite con Hot Module Replacement (HMR) para desarrollo rápido.

## Build para Producción

```bash
npm run build
```

Los archivos se generarán en la carpeta `dist/`

## Despliegue

Los archivos estáticos generados en `dist/` pueden desplegarse en:
- Netlify
- Vercel
- GitHub Pages
- Cualquier servidor web estático

### Variables de Entorno para Producción

Asegúrate de actualizar la URL del backend en `src/services/api.js` antes del build:

```javascript
const API_URL = 'https://tu-backend-url.com/api';
```

## Proxy de Desarrollo

El archivo `vite.config.js` incluye un proxy para redirigir `/api` al backend en desarrollo:

```javascript
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true,
  }
}
```

## Soporte de Navegadores

- Chrome (últimas 2 versiones)
- Firefox (últimas 2 versiones)
- Safari (últimas 2 versiones)
- Edge (últimas 2 versiones)
