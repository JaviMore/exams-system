import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { examsAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import '../styles/ExamList.css';

const ExamList = () => {
  const [exams, setExams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    loadExams();
  }, []);

  const loadExams = async () => {
    try {
      setLoading(true);
      const response = await examsAPI.getAll();
      setExams(response.data);
    } catch (err) {
      setError('Failed to load exams');
    } finally {
      setLoading(false);
    }
  };

  const handleStartExam = (examId) => {
    navigate(`/exam/${examId}`);
  };

  const handleViewResults = () => {
    navigate('/results');
  };

  const handleBackoffice = () => {
    navigate('/admin');
  };

  return (
    <div className="container">
      <div className="header">
        <div className="header-content">
          <h1>📝 Exams System</h1>
          <div className="user-info">
            <span>Welcome, {user?.full_name || user?.email}!</span>
            <button onClick={handleViewResults} className="btn-secondary">
              My Results
            </button>
            {user?.is_admin && (
              <button onClick={handleBackoffice} className="btn-admin">
                Admin Panel
              </button>
            )}
            <button onClick={logout} className="btn-logout">
              Logout
            </button>
          </div>
        </div>
      </div>

      <div className="content">
        <h2>Available Exams</h2>
        
        {loading && <p>Loading exams...</p>}
        {error && <div className="error-message">{error}</div>}
        
        {!loading && exams.length === 0 && (
          <p>No exams available at the moment.</p>
        )}
        
        <div className="exam-grid">
          {exams.map((exam) => (
            <div key={exam.id} className="exam-card">
              <h3>{exam.title}</h3>
              <div className="exam-info">
                <p>⏱️ Duration: {exam.duration_minutes} minutes</p>
                <p>📝 Questions: {exam.question_count}</p>
              </div>
              <button onClick={() => handleStartExam(exam.id)}>
                Start Exam
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ExamList;
