import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { resultsAPI } from '../services/api';
import '../styles/ResultDetail.css';

const ResultDetail = () => {
  const { resultId } = useParams();
  const navigate = useNavigate();
  
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadResult();
  }, [resultId]);

  const loadResult = async () => {
    try {
      setLoading(true);
      const response = await resultsAPI.getById(resultId);
      setResult(response.data);
    } catch (err) {
      setError('Failed to load result');
    } finally {
      setLoading(false);
    }
  };

  const downloadReport = () => {
    const reportText = `
EXAM RESULT REPORT
==================

Exam: ${result.exam_title}
Score: ${result.score.toFixed(2)}%
Correct Answers: ${result.correct_answers} / ${result.total_questions}
Date: ${new Date(result.created_at).toLocaleString()}

DETAILED RESULTS:
-----------------

${result.details.map((detail, idx) => `
Question ${idx + 1}: ${detail.is_correct ? '✓ CORRECT' : '✗ INCORRECT'}
${detail.question}

Your answer: ${detail.options[detail.user_answer] || 'Not answered'}
Correct answer: ${detail.options[detail.correct_answer]}

Explanation: ${detail.explanation}
${'='.repeat(80)}
`).join('\n')}
    `.trim();

    const blob = new Blob([reportText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `exam-result-${resultId}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  if (loading) return <div className="container"><p>Loading results...</p></div>;
  if (error) return <div className="container"><div className="error-message">{error}</div></div>;
  if (!result) return <div className="container"><p>Result not found</p></div>;

  const passed = result.score >= 70;

  return (
    <div className="container">
      <div className="result-header">
        <h1>Exam Results</h1>
        <button onClick={() => navigate('/')} className="btn-secondary">
          Back to Exams
        </button>
      </div>

      <div className="result-summary">
        <h2>{result.exam_title}</h2>
        <div className={`score-display ${passed ? 'passed' : 'failed'}`}>
          <div className="score-circle">
            <span className="score-number">{result.score.toFixed(1)}%</span>
          </div>
          <p className="score-text">
            {result.correct_answers} of {result.total_questions} correct
          </p>
          <p className={`result-status ${passed ? 'passed' : 'failed'}`}>
            {passed ? '✓ Passed' : '✗ Failed'}
          </p>
        </div>
        <p className="result-date">
          Completed: {new Date(result.created_at).toLocaleString()}
        </p>
      </div>

      <div className="result-actions">
        <button onClick={downloadReport}>📥 Download Report</button>
      </div>

      <div className="detailed-results">
        <h3>Detailed Results</h3>
        
        {result.details.map((detail, idx) => (
          <div key={detail.question_id} className={`result-item ${detail.is_correct ? 'correct' : 'incorrect'}`}>
            <div className="result-item-header">
              <h4>Question {idx + 1}</h4>
              <span className="result-icon">
                {detail.is_correct ? '✓' : '✗'}
              </span>
            </div>
            
            <p className="question-text">{detail.question}</p>
            
            <div className="answer-comparison">
              <div className="answer-box">
                <strong>Your answer:</strong>
                <p className={!detail.is_correct ? 'wrong-answer' : ''}>
                  {detail.options[detail.user_answer] || 'Not answered'}
                </p>
              </div>
              
              {!detail.is_correct && (
                <div className="answer-box">
                  <strong>Correct answer:</strong>
                  <p className="correct-answer">
                    {detail.options[detail.correct_answer]}
                  </p>
                </div>
              )}
            </div>
            
            <div className="explanation">
              <strong>Explanation:</strong>
              <p>{detail.explanation}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ResultDetail;
