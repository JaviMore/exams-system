import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { examsAPI, resultsAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import '../styles/Admin.css';

const Admin = () => {
  const [activeTab, setActiveTab] = useState('exams');
  const [exams, setExams] = useState([]);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  // Create/Edit exam form
  const [examTitle, setExamTitle] = useState('');
  const [examDuration, setExamDuration] = useState(30);
  const [questions, setQuestions] = useState([]);
  const [editingExamId, setEditingExamId] = useState(null);
  
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!user?.is_admin) {
      navigate('/');
      return;
    }
    
    if (activeTab === 'exams') {
      loadExams();
    } else if (activeTab === 'results') {
      loadResults();
    }
  }, [activeTab, user, navigate]);

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

  const loadResults = async () => {
    try {
      setLoading(true);
      const response = await resultsAPI.getAll();
      setResults(response.data);
    } catch (err) {
      setError('Failed to load results');
    } finally {
      setLoading(false);
    }
  };

  const handleEditExam = async (examId) => {
    try {
      setLoading(true);
      const response = await examsAPI.getFullById(examId);
      const exam = response.data;
      
      // Populate form with exam data
      setExamTitle(exam.title);
      setExamDuration(exam.duration_minutes);
      setQuestions(exam.questions.map(q => ({
        question: q.question,
        options: q.options,
        correct_answer: q.correct_answer,
        explanation: q.explanation
      })));
      setEditingExamId(examId);
      setActiveTab('create');
    } catch (err) {
      setError('Failed to load exam for editing');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteExam = async (examId) => {
    if (!window.confirm('Are you sure you want to delete this exam?')) return;

    try {
      await examsAPI.delete(examId);
      loadExams();
    } catch (err) {
      setError('Failed to delete exam');
    }
  };

  const handleCancelEdit = () => {
    setExamTitle('');
    setExamDuration(30);
    setQuestions([]);
    setEditingExamId(null);
  };

  const handleDeleteResult = async (resultId) => {
    if (!window.confirm('Are you sure you want to delete this result?')) return;

    try {
      await resultsAPI.delete(resultId);
      loadResults();
    } catch (err) {
      setError('Failed to delete result');
    }
  };

  const addQuestion = () => {
    setQuestions([
      ...questions,
      {
        question: '',
        options: ['', '', '', ''],
        correct_answer: 0,
        explanation: '',
      },
    ]);
  };

  const updateQuestion = (index, field, value) => {
    const newQuestions = [...questions];
    newQuestions[index][field] = value;
    setQuestions(newQuestions);
  };

  const updateOption = (qIndex, oIndex, value) => {
    const newQuestions = [...questions];
    newQuestions[qIndex].options[oIndex] = value;
    setQuestions(newQuestions);
  };

  const removeQuestion = (index) => {
    setQuestions(questions.filter((_, i) => i !== index));
  };

  const handleCreateExam = async (e) => {
    e.preventDefault();
    
    if (questions.length === 0) {
      setError('Add at least one question');
      return;
    }

    try {
      setLoading(true);
      
      const examData = {
        title: examTitle,
        duration_minutes: examDuration,
        questions: questions,
      };
      
      if (editingExamId) {
        // Update existing exam
        await examsAPI.update(editingExamId, examData);
      } else {
        // Create new exam
        await examsAPI.create(examData);
      }
      
      // Reset form
      setExamTitle('');
      setExamDuration(30);
      setQuestions([]);
      setEditingExamId(null);
      setActiveTab('exams');
      loadExams();
    } catch (err) {
      setError(editingExamId ? 'Failed to update exam' : 'Failed to create exam');
    } finally {
      setLoading(false);
    }
  };

  const handleImportJSON = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      try {
        const data = JSON.parse(event.target.result);
        
        if (data.title) setExamTitle(data.title);
        if (data.durationMinutes) setExamDuration(data.durationMinutes);
        if (data.questions) setQuestions(data.questions.map(q => ({
          question: q.question,
          options: q.options,
          correct_answer: q.correctAnswer,
          explanation: q.explanation
        })));
      } catch (err) {
        setError('Invalid JSON file');
      }
    };
    reader.readAsText(file);
  };

  return (
    <div className="admin-container">
      <div className="admin-header">
        <h1>Admin Panel</h1>
        <button onClick={() => navigate('/')} className="btn-secondary">
          Back to Exams
        </button>
      </div>

      <div className="tabs">
        <button
          className={activeTab === 'exams' ? 'active' : ''}
          onClick={() => setActiveTab('exams')}
        >
          Manage Exams
        </button>
        <button
          className={activeTab === 'create' ? 'active' : ''}
          onClick={() => setActiveTab('create')}
        >
          Create Exam
        </button>
        <button
          className={activeTab === 'results' ? 'active' : ''}
          onClick={() => setActiveTab('results')}
        >
          View Results
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {activeTab === 'exams' && (
        <div className="tab-content">
          <h2>Manage Exams</h2>
          {loading && <p>Loading...</p>}
          
          <div className="admin-table">
            <table>
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Duration</th>
                  <th>Questions</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {exams.map((exam) => (
                  <tr key={exam.id}>
                    <td>{exam.title}</td>
                    <td>{exam.duration_minutes} min</td>
                    <td>{exam.question_count}</td>
                    <td>
                      <div className="action-buttons">
                        <button
                          onClick={() => handleEditExam(exam.id)}
                          className="btn-edit"
                        >
                          Edit
                        </button>
                        <button
                          onClick={() => handleDeleteExam(exam.id)}
                          className="btn-delete"
                        >
                          Delete
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {activeTab === 'create' && (
        <div className="tab-content">
          <div className="form-header">
            <h2>{editingExamId ? 'Edit Exam' : 'Create New Exam'}</h2>
            {editingExamId && (
              <button 
                type="button" 
                onClick={handleCancelEdit}
                className="btn-secondary"
              >
                Cancel Edit
              </button>
            )}
          </div>
          
          {!editingExamId && (
            <div className="import-section">
              <h3>Import from JSON</h3>
              <input
                type="file"
                accept=".json"
                onChange={handleImportJSON}
              />
            </div>
          )}

          <form onSubmit={handleCreateExam}>
            <div className="form-group">
              <label>Exam Title:</label>
              <input
                type="text"
                value={examTitle}
                onChange={(e) => setExamTitle(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label>Duration (minutes):</label>
              <input
                type="number"
                value={examDuration}
                onChange={(e) => setExamDuration(parseInt(e.target.value))}
                min="1"
                required
              />
            </div>

            <h3>Questions</h3>
            
            {questions.map((q, qIdx) => (
              <div key={qIdx} className="question-builder">
                <div className="question-header">
                  <h4>Question {qIdx + 1}</h4>
                  <button
                    type="button"
                    onClick={() => removeQuestion(qIdx)}
                    className="btn-delete"
                  >
                    Remove
                  </button>
                </div>

                <div className="form-group">
                  <label>Question:</label>
                  <textarea
                    value={q.question}
                    onChange={(e) => updateQuestion(qIdx, 'question', e.target.value)}
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Options:</label>
                  {q.options.map((opt, oIdx) => (
                    <div key={oIdx} className="option-input">
                      <input
                        type="radio"
                        name={`correct-${qIdx}`}
                        checked={q.correct_answer === oIdx}
                        onChange={() => updateQuestion(qIdx, 'correct_answer', oIdx)}
                      />
                      <input
                        type="text"
                        value={opt}
                        onChange={(e) => updateOption(qIdx, oIdx, e.target.value)}
                        placeholder={`Option ${oIdx + 1}`}
                        required
                      />
                    </div>
                  ))}
                </div>

                <div className="form-group">
                  <label>Explanation:</label>
                  <textarea
                    value={q.explanation}
                    onChange={(e) => updateQuestion(qIdx, 'explanation', e.target.value)}
                    required
                  />
                </div>
              </div>
            ))}

            <div className="form-actions">
              <button type="button" onClick={addQuestion} className="btn-secondary">
                + Add Question
              </button>

              <button type="submit" disabled={loading}>
                {loading 
                  ? (editingExamId ? 'Updating...' : 'Creating...') 
                  : (editingExamId ? 'Update Exam' : 'Create Exam')
                }
              </button>
            </div>
          </form>
        </div>
      )}

      {activeTab === 'results' && (
        <div className="tab-content">
          <h2>All Results</h2>
          {loading && <p>Loading...</p>}
          
          <div className="admin-table">
            <table>
              <thead>
                <tr>
                  <th>Student</th>
                  <th>Exam</th>
                  <th>Score</th>
                  <th>Date</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {results.map((result) => (
                  <tr key={result.id}>
                    <td>{result.user_name}</td>
                    <td>{result.exam_title}</td>
                    <td className={result.score >= 70 ? 'passed' : 'failed'}>
                      {result.score.toFixed(1)}%
                    </td>
                    <td>{new Date(result.created_at).toLocaleDateString()}</td>
                    <td>
                      <div className="action-buttons">
                        <button
                          onClick={() => navigate(`/results/${result.id}`)}
                          className="btn-view"
                        >
                          View
                        </button>
                        <button
                          onClick={() => handleDeleteResult(result.id)}
                          className="btn-delete"
                        >
                          Delete
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default Admin;
