import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { resultsAPI } from '../services/api';
import '../styles/MyResults.css';

const MyResults = () => {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  const navigate = useNavigate();

  useEffect(() => {
    loadResults();
  }, []);

  const loadResults = async () => {
    try {
      setLoading(true);
      const response = await resultsAPI.getMy();
      setResults(response.data);
    } catch (err) {
      setError('Failed to load results');
    } finally {
      setLoading(false);
    }
  };

  const handleViewDetail = (resultId) => {
    navigate(`/results/${resultId}`);
  };

  return (
    <div className="container">
      <div className="header">
        <h1>My Exam Results</h1>
        <button onClick={() => navigate('/')} className="btn-secondary">
          Back to Exams
        </button>
      </div>

      {loading && <p>Loading results...</p>}
      {error && <div className="error-message">{error}</div>}
      
      {!loading && results.length === 0 && (
        <div className="empty-state">
          <p>You haven't taken any exams yet.</p>
          <button onClick={() => navigate('/')}>Browse Exams</button>
        </div>
      )}

      <div className="results-list">
        {results.map((result) => (
          <div key={result.id} className="result-card">
            <div className="result-card-header">
              <h3>{result.exam_title}</h3>
              <span className={`score-badge ${result.score >= 70 ? 'passed' : 'failed'}`}>
                {result.score.toFixed(1)}%
              </span>
            </div>
            
            <div className="result-card-body">
              <p>
                <strong>Correct:</strong> {result.correct_answers} / {result.total_questions}
              </p>
              <p>
                <strong>Date:</strong> {new Date(result.created_at).toLocaleString()}
              </p>
              <p className={`status ${result.score >= 70 ? 'passed' : 'failed'}`}>
                {result.score >= 70 ? '✓ Passed' : '✗ Failed'}
              </p>
            </div>
            
            <button onClick={() => handleViewDetail(result.id)}>
              View Details
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MyResults;
