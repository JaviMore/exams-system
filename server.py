#!/usr/bin/env python3
import http.server
import socketserver
import json
import urllib.parse
from datetime import datetime
import os
import sqlite3
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", 3000))
DB_FILE = os.getenv("DB_FILE", 'exam_system.db')
EXAMS_DIR = os.getenv("EXAMS_DIR", 'exams')  # Carpeta donde se buscan ficheros .json de exámenes

# Backoffice credentials
BACKOFFICE_USER = os.getenv("BACKOFFICE_USER")
BACKOFFICE_PASSWORD = os.getenv("BACKOFFICE_PASSWORD")

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_database():
    """Initialize the database with tables and sample data"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Create exams table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                duration_minutes INTEGER DEFAULT 30,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create questions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exam_id INTEGER NOT NULL,
                question TEXT NOT NULL,
                options TEXT NOT NULL,
                correct_answer INTEGER NOT NULL,
                explanation TEXT NOT NULL,
                question_order INTEGER NOT NULL,
                FOREIGN KEY (exam_id) REFERENCES exams(id) ON DELETE CASCADE
            )
        ''')
        
        # Create results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT NOT NULL,
                exam_id INTEGER NOT NULL,
                exam_title TEXT NOT NULL,
                answers TEXT NOT NULL,
                score REAL NOT NULL,
                correct_answers INTEGER NOT NULL,
                total_questions INTEGER NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (exam_id) REFERENCES exams(id)
            )
        ''')
        
        # Insert data from JSON exam files if the DB is empty
        cursor.execute('SELECT COUNT(*) FROM exams')
        if cursor.fetchone()[0] == 0:
            loaded_exams = load_exams_from_folder(EXAMS_DIR)
            if not loaded_exams:
                # Fallback: intentar cargar JSON en el directorio actual (permite usar sample_exam.json existente)
                loaded_exams = load_exams_from_folder('.')
            if not loaded_exams:
                print(f"No exam files found in '{EXAMS_DIR}' or current directory. Empty database created.")
            else:
                for exam_spec in loaded_exams:
                    duration = exam_spec.get('durationMinutes', 30)
                    cursor.execute('INSERT INTO exams (title, duration_minutes) VALUES (?, ?)', (exam_spec['title'], duration))
                    exam_id = cursor.lastrowid
                    for idx, q in enumerate(exam_spec.get('questions', [])):
                        try:
                            cursor.execute(
                                'INSERT INTO questions (exam_id, question, options, correct_answer, explanation, question_order) VALUES (?, ?, ?, ?, ?, ?)',
                                (exam_id, q['question'], json.dumps(q['options']), q['correctAnswer'], q['explanation'], idx + 1)
                            )
                        except KeyError as e:
                            print(f"Question skipped due to missing field {e} in exam '{exam_spec['title']}'")
                print(f"Loaded {len(loaded_exams)} exams from JSON files.")
        
        conn.commit()
        print("Database initialized successfully")

def get_all_exams():
    """Get all exams with their questions"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM exams ORDER BY id')
        exams = []
        
        for exam_row in cursor.fetchall():
            exam = {
                'id': exam_row['id'],
                'title': exam_row['title'],
                'durationMinutes': exam_row['duration_minutes'],
                'questions': []
            }
            
            cursor.execute(
                'SELECT * FROM questions WHERE exam_id = ? ORDER BY question_order',
                (exam_row['id'],)
            )
            
            for q_row in cursor.fetchall():
                question = {
                    'id': q_row['id'],
                    'question': q_row['question'],
                    'options': json.loads(q_row['options']),
                    'correctAnswer': q_row['correct_answer'],
                    'explanation': q_row['explanation']
                }
                exam['questions'].append(question)
            
            exams.append(exam)
        
        return exams

def get_exam_by_id(exam_id):
    """Get a specific exam with its questions"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM exams WHERE id = ?', (exam_id,))
        exam_row = cursor.fetchone()
        
        if not exam_row:
            return None
        
        exam = {
            'id': exam_row['id'],
            'title': exam_row['title'],
            'durationMinutes': exam_row['duration_minutes'],
            'questions': []
        }
        
        cursor.execute(
            'SELECT * FROM questions WHERE exam_id = ? ORDER BY question_order',
            (exam_id,)
        )
        
        for q_row in cursor.fetchall():
            question = {
                'id': q_row['id'],
                'question': q_row['question'],
                'options': json.loads(q_row['options']),
                'correctAnswer': q_row['correct_answer'],
                'explanation': q_row['explanation']
            }
            exam['questions'].append(question)
        
        return exam

def create_exam(title, questions, duration_minutes=30):
    """Create a new exam with questions"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO exams (title, duration_minutes) VALUES (?, ?)', (title, duration_minutes))
        exam_id = cursor.lastrowid
        
        for idx, q in enumerate(questions):
            cursor.execute(
                'INSERT INTO questions (exam_id, question, options, correct_answer, explanation, question_order) VALUES (?, ?, ?, ?, ?, ?)',
                (exam_id, q['question'], json.dumps(q['options']), q['correctAnswer'], q['explanation'], idx + 1)
            )
        
        conn.commit()
        return exam_id

def save_result(result):
    """Save exam result to database"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO results (user_name, exam_id, exam_title, answers, score, correct_answers, total_questions) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (result['userName'], result['examId'], result['examTitle'], json.dumps(result['answers']), 
             result['score'], result['correctAnswers'], result['totalQuestions'])
        )
        result_id = cursor.lastrowid
        conn.commit()
        
        # Get the inserted result with timestamp
        cursor.execute('SELECT * FROM results WHERE id = ?', (result_id,))
        row = cursor.fetchone()
        
        return {
            'id': row['id'],
            'userName': row['user_name'],
            'examId': row['exam_id'],
            'examTitle': row['exam_title'],
            'answers': json.loads(row['answers']),
            'score': row['score'],
            'correctAnswers': row['correct_answers'],
            'totalQuestions': row['total_questions'],
            'date': row['date']
        }

def get_all_results():
    """Get all results from database"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM results ORDER BY date DESC')
        results = []
        
        for row in cursor.fetchall():
            result = {
                'id': row['id'],
                'userName': row['user_name'],
                'examId': row['exam_id'],
                'examTitle': row['exam_title'],
                'answers': json.loads(row['answers']),
                'score': row['score'],
                'correctAnswers': row['correct_answers'],
                'totalQuestions': row['total_questions'],
                'date': row['date']
            }
            results.append(result)
        
        return results

def update_exam(exam_id, title=None, duration_minutes=None):
    """Update exam title and/or duration"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if title is not None:
            updates.append('title = ?')
            params.append(title)
        
        if duration_minutes is not None:
            updates.append('duration_minutes = ?')
            params.append(duration_minutes)
        
        if not updates:
            return None
        
        params.append(exam_id)
        query = f"UPDATE exams SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()
        
        return get_exam_by_id(exam_id)

def delete_exam(exam_id):
    """Delete exam and all associated questions and results"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM results WHERE exam_id = ?', (exam_id,))
        cursor.execute('DELETE FROM questions WHERE exam_id = ?', (exam_id,))
        cursor.execute('DELETE FROM exams WHERE id = ?', (exam_id,))
        conn.commit()
        return True

def delete_result(result_id):
    """Delete a specific result"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM results WHERE id = ?', (result_id,))
        conn.commit()
        return True

def clear_all_results():
    """Delete all results"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM results')
        conn.commit()
        return True
def load_exams_from_folder(folder):
    """Load exam specifications from all .json files in a folder.
    Each file must have structure {"title": str, "questions": [ ... ]}.
    An array of exams at the root of the JSON is also accepted.
    """
    exams = []
    if not os.path.isdir(folder):
        return exams
    for name in sorted(os.listdir(folder)):
        if not name.lower().endswith('.json'):
            continue
        path = os.path.join(folder, name)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if isinstance(data, dict) and 'title' in data and 'questions' in data:
                exams.append(data)
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and 'title' in item and 'questions' in item:
                        exams.append(item)
            else:
                print(f"Unknown format in {path}, ignoring.")
        except Exception as e:
            print(f"Error reading {path}: {e}")
    return exams
class ExamHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        # Serve static files
        if path == '/' or path == '/index.html':
            self.serve_file('public/index.html', 'text/html')
        elif path == '/backoffice.html':
            self.serve_file('public/backoffice.html', 'text/html')
        elif path == '/styles.css':
            self.serve_file('public/styles.css', 'text/css')
        # API endpoints
        elif path == '/api/exams':
            exams = get_all_exams()
            self.send_json_response(exams)
        elif path.startswith('/api/exams/'):
            exam_id = int(path.split('/')[-1])
            exam = get_exam_by_id(exam_id)
            if exam:
                self.send_json_response(exam)
            else:
                self.send_error(404, 'Exam not found')
        elif path == '/api/results':
            results = get_all_results()
            self.send_json_response(results)
        elif path == '/api/backoffice/login':
            # Handle backoffice login
            query = urllib.parse.parse_qs(parsed_path.query)
            username = query.get('username', [''])[0]
            password = query.get('password', [''])[0]
            
            if username == BACKOFFICE_USER and password == BACKOFFICE_PASSWORD:
                self.send_json_response({"success": True, "message": "Login successful"})
            else:
                self.send_json_response({"success": False, "message": "Invalid credentials"}, 401)
        else:
            self.send_error(404, 'Not Found')
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        if path == '/api/backoffice/login':
            username = data.get('username', '')
            password = data.get('password', '')
            
            if username == BACKOFFICE_USER and password == BACKOFFICE_PASSWORD:
                self.send_json_response({"success": True, "message": "Login successful"})
            else:
                self.send_json_response({"success": False, "message": "Invalid credentials"}, 401)
        elif path == '/api/exams':
            # Create new exam
            title = data.get('title')
            questions = data.get('questions', [])
            duration_minutes = data.get('durationMinutes', 30)
            exam_id = create_exam(title, questions, duration_minutes)
            exam = get_exam_by_id(exam_id)
            self.send_json_response(exam, 201)
        elif path == '/api/results':
            # Save result
            result = save_result(data)
            self.send_json_response(result, 201)
        else:
            self.send_error(404, 'Not Found')
    
    def do_PUT(self):
        content_length = int(self.headers['Content-Length'])
        put_data = self.rfile.read(content_length)
        data = json.loads(put_data.decode('utf-8'))
        
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        if path.startswith('/api/exams/'):
            exam_id = int(path.split('/')[-1])
            title = data.get('title')
            duration_minutes = data.get('durationMinutes')
            exam = update_exam(exam_id, title, duration_minutes)
            
            if exam:
                self.send_json_response(exam)
            else:
                self.send_error(404, 'Exam not found')
        else:
            self.send_error(404, 'Not Found')
    
    def do_DELETE(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        if path.startswith('/api/exams/'):
            exam_id = int(path.split('/')[-1])
            success = delete_exam(exam_id)
            self.send_json_response({'success': success, 'message': 'Exam deleted successfully'})
        elif path.startswith('/api/results/') and path != '/api/results/clear-all':
            result_id = int(path.split('/')[-1])
            success = delete_result(result_id)
            self.send_json_response({'success': success, 'message': 'Result deleted successfully'})
        elif path == '/api/results/clear-all':
            success = clear_all_results()
            self.send_json_response({'success': success, 'message': 'All results cleared successfully'})
        else:
            self.send_error(404, 'Not Found')
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def serve_file(self, filepath, content_type):
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, 'File not found')
    
    def send_json_response(self, data, status=200):
        json_data = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', len(json_data))
        self.end_headers()
        self.wfile.write(json_data)
    
    def log_message(self, format, *args):
        # Custom log format
        print(f"{self.address_string()} - [{self.log_date_time_string()}] {format % args}")

if __name__ == '__main__':
    os.chdir('/home/javas/workspace/exams-system')
    
    # Initialize database
    print("Initializing database...")
    init_database()
    
    with socketserver.TCPServer(("", PORT), ExamHandler) as httpd:
        print(f"Server running at http://localhost:{PORT}")
        print(f"Backoffice available at http://localhost:{PORT}/backoffice.html")
        print(f"Database: {DB_FILE}")
        print("Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")
