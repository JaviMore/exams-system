import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { examsAPI, resultsAPI } from '../services/api';
import '../styles/TakeExam.css';

const TakeExam = () => {
  const { examId } = useParams();
  const navigate = useNavigate();
  
  const getStorageKey = (key) => `exam_${examId}_${key}`;
  
  const [exam, setExam] = useState(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(() => {
    const saved = localStorage.getItem(getStorageKey('currentQuestion'));
    return saved ? parseInt(saved) : 0;
  });
  const [answers, setAnswers] = useState(() => {
    const saved = localStorage.getItem(getStorageKey('answers'));
    return saved ? JSON.parse(saved) : {};
  });
  const [flaggedQuestions, setFlaggedQuestions] = useState(() => {
    const saved = localStorage.getItem(getStorageKey('flagged'));
    return saved ? new Set(JSON.parse(saved)) : new Set();
  });
  const [timeRemaining, setTimeRemaining] = useState(0);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [showConfirmModal, setShowConfirmModal] = useState(false);
  const [showWarningModal, setShowWarningModal] = useState(false);
  const [unansweredCount, setUnansweredCount] = useState(0);

  useEffect(() => {
    loadExam();
  }, [examId]);

  useEffect(() => {
    if (!exam) return;

    const timer = setInterval(() => {
      setTimeRemaining((prev) => {
        if (prev <= 1) {
          handleSubmit();
          return 0;
        }
        const newTime = prev - 1;
        localStorage.setItem(getStorageKey('timeRemaining'), newTime.toString());
        localStorage.setItem(getStorageKey('timestamp'), Date.now().toString());
        return newTime;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [exam]);

  // Save current question index
  useEffect(() => {
    localStorage.setItem(getStorageKey('currentQuestion'), currentQuestionIndex.toString());
  }, [currentQuestionIndex]);

  const loadExam = async () => {
    try {
      setLoading(true);
      const response = await examsAPI.getById(examId);
      setExam(response.data);
      
      // Load saved time or use full duration
      const savedTime = localStorage.getItem(getStorageKey('timeRemaining'));
      const savedTimestamp = localStorage.getItem(getStorageKey('timestamp'));
      
      if (savedTime && savedTimestamp) {
        const elapsed = Math.floor((Date.now() - parseInt(savedTimestamp)) / 1000);
        const remaining = Math.max(0, parseInt(savedTime) - elapsed);
        setTimeRemaining(remaining);
      } else {
        setTimeRemaining(response.data.duration_minutes * 60);
        localStorage.setItem(getStorageKey('timestamp'), Date.now().toString());
      }
    } catch (err) {
      setError('Failed to load exam');
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerSelect = (questionId, optionIndex) => {
    const newAnswers = {
      ...answers,
      [questionId]: optionIndex,
    };
    setAnswers(newAnswers);
    localStorage.setItem(getStorageKey('answers'), JSON.stringify(newAnswers));
  };

  const toggleFlag = () => {
    const questionId = exam.questions[currentQuestionIndex].id;
    setFlaggedQuestions((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(questionId)) {
        newSet.delete(questionId);
      } else {
        newSet.add(questionId);
      }
      localStorage.setItem(getStorageKey('flagged'), JSON.stringify([...newSet]));
      return newSet;
    });
  };

  const handleSubmitClick = () => {
    if (submitting) return;

    // Check for unanswered questions
    const unanswered = exam.questions.filter(q => answers[q.id] === undefined).length;
    
    if (unanswered > 0) {
      setUnansweredCount(unanswered);
      setShowWarningModal(true);
    } else {
      setShowConfirmModal(true);
    }
  };

  const handleSubmit = async () => {
    setShowConfirmModal(false);
    setShowWarningModal(false);
    setSubmitting(true);

    try {
      const answersArray = exam.questions.map((q) => ({
        question_id: q.id,
        selected_answer: answers[q.id] ?? -1,
      }));

      const response = await resultsAPI.submit({
        exam_id: parseInt(examId),
        answers: answersArray,
      });

      // Clear saved data after successful submission
      localStorage.removeItem(getStorageKey('answers'));
      localStorage.removeItem(getStorageKey('flagged'));
      localStorage.removeItem(getStorageKey('timeRemaining'));
      localStorage.removeItem(getStorageKey('timestamp'));
      localStorage.removeItem(getStorageKey('currentQuestion'));
      
      navigate(`/results/${response.data.id}`);
    } catch (err) {
      setError('Failed to submit exam');
      setSubmitting(false);
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  if (loading) return <div className="container"><p>Loading exam...</p></div>;
  if (error) return <div className="container"><div className="error-message">{error}</div></div>;
  if (!exam) return <div className="container"><p>Exam not found</p></div>;

  const currentQuestion = exam.questions[currentQuestionIndex];
  const progress = ((currentQuestionIndex + 1) / exam.questions.length) * 100;

  return (
    <div className="exam-container">
      <div className="exam-header">
        <h1>{exam.title}</h1>
        <div className="timer" style={{ color: timeRemaining < 300 ? '#ef4444' : '#10b981' }}>
          ⏱️ {formatTime(timeRemaining)}
        </div>
      </div>

      <div className="progress-bar">
        <div className="progress-fill" style={{ width: `${progress}%` }}></div>
      </div>

      <div className="question-navigator">
        {exam.questions.map((q, idx) => (
          <button
            key={q.id}
            className={`question-nav-btn ${idx === currentQuestionIndex ? 'active' : ''} ${
              answers[q.id] !== undefined ? 'answered' : ''
            } ${flaggedQuestions.has(q.id) ? 'flagged' : ''}`}
            onClick={() => setCurrentQuestionIndex(idx)}
          >
            {idx + 1}
          </button>
        ))}
      </div>

      <div className="question-content">
        <div className="question-header">
          <h2>Question {currentQuestionIndex + 1} of {exam.questions.length}</h2>
          <button onClick={toggleFlag} className="flag-btn">
            {flaggedQuestions.has(currentQuestion.id) ? '🚩' : '⚐'} Flag
          </button>
        </div>

        <p className="question-text">{currentQuestion.question}</p>

        <div className="options">
          {currentQuestion.options.map((option, idx) => (
            <div
              key={idx}
              className={`option ${answers[currentQuestion.id] === idx ? 'selected' : ''}`}
              onClick={() => handleAnswerSelect(currentQuestion.id, idx)}
            >
              <input
                type="radio"
                name="answer"
                checked={answers[currentQuestion.id] === idx}
                onChange={() => {}}
              />
              <span>{option}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="exam-controls">
        <button
          onClick={() => setCurrentQuestionIndex((prev) => Math.max(0, prev - 1))}
          disabled={currentQuestionIndex === 0}
        >
          ← Previous
        </button>

        {currentQuestionIndex < exam.questions.length - 1 ? (
          <button
            onClick={() => setCurrentQuestionIndex((prev) => prev + 1)}
            className="btn-next"
          >
            Next →
          </button>
        ) : (
          <button onClick={handleSubmitClick} disabled={submitting} className="btn-submit">
            {submitting ? 'Submitting...' : 'Submit Exam'}
          </button>
        )}
      </div>

      {/* Warning Modal - Unanswered Questions */}
      {showWarningModal && (
        <div className="modal-overlay" onClick={() => setShowWarningModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3>⚠️ Unanswered Questions</h3>
            <p>
              You have <strong>{unansweredCount}</strong> unanswered question{unansweredCount > 1 ? 's' : ''}.
            </p>
            <p>Are you sure you want to submit the exam?</p>
            <div className="modal-actions">
              <button onClick={() => setShowWarningModal(false)} className="btn-secondary">
                Review Answers
              </button>
              <button onClick={handleSubmit} className="btn-submit">
                Submit Anyway
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Confirmation Modal */}
      {showConfirmModal && (
        <div className="modal-overlay" onClick={() => setShowConfirmModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3>✓ Submit Exam</h3>
            <p>Are you sure you want to submit your exam?</p>
            <p className="modal-warning">This action cannot be undone.</p>
            <div className="modal-actions">
              <button onClick={() => setShowConfirmModal(false)} className="btn-secondary">
                Cancel
              </button>
              <button onClick={handleSubmit} className="btn-submit">
                Submit Exam
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TakeExam;
