# Exams System - Frontend

Frontend built with React + Vite for the online exams system.

## Features

- ⚛️ React 18
- ⚡ Vite for fast development
- 🎨 Modern and responsive CSS
- 🔐 JWT Authentication
- 📱 Responsive design
- 🎯 Navigation with React Router

## Requirements

- Node.js 16+
- npm or yarn

## Installation

1. Install dependencies:
```bash
npm install
```

2. Configure environment variables (optional):
Edit `src/services/api.js` if the backend is at a different URL.

3. Start development server:
```bash
npm run dev
```

The application will be available at: http://localhost:5173

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

## Project Structure

```
frontend/
├── public/              # Static files
├── src/
│   ├── components/      # Reusable components
│   │   └── PrivateRoute.jsx
│   ├── context/         # Context API
│   │   └── AuthContext.jsx
│   ├── pages/          # Pages/Views
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   ├── ExamList.jsx
│   │   ├── TakeExam.jsx
│   │   ├── ResultDetail.jsx
│   │   ├── MyResults.jsx
│   │   └── Admin.jsx
│   ├── services/       # API Services
│   │   └── api.js
│   ├── styles/         # CSS Styles
│   │   ├── App.css
│   │   ├── Auth.css
│   │   ├── ExamList.css
│   │   ├── TakeExam.css
│   │   ├── ResultDetail.css
│   │   ├── MyResults.css
│   │   └── Admin.css
│   ├── App.jsx         # Main component
│   └── main.jsx        # Entry point
├── index.html
├── package.json
└── vite.config.js
```

## Features

### For Students
- ✅ Registration and login
- ✅ View list of available exams
- ✅ Take exams with timer
- ✅ Navigate between questions
- ✅ Mark questions for review
- ✅ View detailed results
- ✅ Download results report
- ✅ History of completed exams

### For Administrators
- ✅ Administration panel
- ✅ Create exams manually
- ✅ Import exams from JSON
- ✅ Manage existing exams
- ✅ View all results
- ✅ Delete exams and results

## JSON Format for Importing Exams

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

## Application Routes

- `/login` - Login page
- `/register` - Registration page
- `/` - Exams list (requires authentication)
- `/exam/:id` - Take exam (requires authentication)
- `/results` - My results (requires authentication)
- `/results/:id` - Result detail (requires authentication)
- `/admin` - Administration panel (requires admin)

## Development

The project uses Vite with Hot Module Replacement (HMR) for fast development.

## Production Build

```bash
npm run build
```

Files will be generated in the `dist/` folder

## Deployment

The static files generated in `dist/` can be deployed to:
- Netlify
- Vercel
- GitHub Pages
- Any static web server

### Production Environment Variables

Make sure to update the backend URL in `src/services/api.js` before build:

```javascript
const API_URL = 'https://your-backend-url.com/api';
```

## Development Proxy

The `vite.config.js` file includes a proxy to redirect `/api` to the backend in development:

```javascript
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true,
  }
}
```

## Browser Support

- Chrome (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Edge (latest 2 versions)
