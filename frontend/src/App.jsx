import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import PrivateRoute from './components/PrivateRoute';

import Login from './pages/Login';
import Register from './pages/Register';
import ExamList from './pages/ExamList';
import TakeExam from './pages/TakeExam';
import ResultDetail from './pages/ResultDetail';
import MyResults from './pages/MyResults';
import Admin from './pages/Admin';

import './styles/App.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          
          <Route
            path="/"
            element={
              <PrivateRoute>
                <ExamList />
              </PrivateRoute>
            }
          />
          
          <Route
            path="/exam/:examId"
            element={
              <PrivateRoute>
                <TakeExam />
              </PrivateRoute>
            }
          />
          
          <Route
            path="/results"
            element={
              <PrivateRoute>
                <MyResults />
              </PrivateRoute>
            }
          />
          
          <Route
            path="/results/:resultId"
            element={
              <PrivateRoute>
                <ResultDetail />
              </PrivateRoute>
            }
          />
          
          <Route
            path="/admin"
            element={
              <PrivateRoute>
                <Admin />
              </PrivateRoute>
            }
          />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
