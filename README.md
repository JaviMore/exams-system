# Online Exam System

A complete web application for multiple-choice exams with administration backoffice.

## Features

### For Users:
- **Simple login**: Just enter your name
- **Exam selection**: Choose from multiple available exams
- **Intuitive exam interface**: Take exams with multiple-choice questions
- **Detailed results**: 
  - Final score
  - Correct and incorrect answers
  - Explanations for each question
  - Download report option

### For Administrators (Backoffice):
- **Create exams**: Add new exams with multiple questions
- **Question management**: 
  - Question text
  - 4 answer options
  - Mark the correct answer
  - Add explanation
- **View results**: 
  - List of all results
  - Filter by exam
  - Student information, date and score
- **Authentication**: Secure access with username and password

## Installation

1. Clone or download the project
2. No additional dependencies required (uses only native Python 3 modules including SQLite)

## Usage

### Option 1: Run with Python

```bash
python3 server.py
```

Or simply:
```bash
./server.py
```

### Option 2: Run with Docker

Build the image:
```bash
# Default port (3000)
docker build -t exams-system .

# Custom port
docker build --build-arg PORT=8080 -t exams-system .
```

Run the container:
```bash
# Basic run
docker run -p 3000:3000 exams-system

# With environment file
docker run -p 3000:3000 --env-file .env exams-system

# With persistent database
docker run -p 3000:3000 -v $(pwd)/data:/app/data --env DB_FILE=/app/data/exam_system.db exams-system
```

The server will start at http://localhost:3000

### Automatic Exam Loading from JSON

On startup, the server attempts to populate the database by reading all `*.json` files from the folder specified by the `EXAMS_DIR` environment variable (default is `exams`).

If that folder doesn't exist or contains no valid files, it will make a second attempt in the current directory (allowing direct use of the included `sample_exam.json`).

Steps to add exams:
1. Create `exams/` folder (optional but recommended).
2. Place one or more `.json` files inside with the correct format (see below).
3. Restart the server (exams are only loaded when the table is empty).

Example execution specifying folder:
```bash
EXAMS_DIR=exams PORT=3000 python3 server.py
```

## How to Use

### Users:
1. Go to http://localhost:3000
2. Enter your name
3. Select an exam
4. Answer the questions
5. View your detailed results
6. Download your report (optional)

### Cookie Persistence
The system uses cookies to improve the experience:
- `examUser`: remembers your name and avoids having to re-enter it (24h).
- `examState`: saves the exam in progress (id, start time and answers) to recover your progress if you accidentally reload the page or close the browser. The remaining time is recalculated on return.
  - If time has already expired on return, results are automatically submitted.
- `backofficeAuth`: keeps the backoffice session active (1h). Logging out removes it.

Limitations: This is not a real security mechanism; cookies are not encrypted. Do not use in production without adding proper authentication and secure expiration on the server.

### Administrators:
1. Go to http://localhost:3000/backoffice.html
2. Login with credentials (default: admin / admin123)
3. **Create Exam**:
   - **Option 1: Import from JSON**
     - Click "Upload JSON File" and select your JSON file
     - Or download the sample JSON template
     - The form will auto-populate with the exam data
   - **Option 2: Create Manually**
     - Enter exam title
     - Add questions with the "+ Add Question" button
     - For each question, complete:
       - Question text
       - 4 options (mark the correct one with the radio button)
       - Explanation
   - Save the exam
4. **View Results**:
   - Check all results
   - Filter by specific exam

## JSON Format for Importing Exams

You can create exams by uploading a JSON file with the following structure:

```json
{
  "title": "Exam Title",
  "durationMinutes": 30,
  "questions": [
    {
      "question": "Question text?",
      "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
      "correctAnswer": 0,
      "explanation": "Explanation for the correct answer"
    }
  ]
}
```

- `title`: String with the exam name
- `questions`: Array of question objects
  - `question`: The question text
  - `options`: Array of exactly 4 options
  - `correctAnswer`: Index (0-3) of the correct option
  - `explanation`: Text explaining why the answer is correct

Additional fields:
- `durationMinutes`: Duration of the exam in minutes (integer). If omitted, defaults to 30.

A sample file (`sample_exam.json`) is included in the project.

## Technologies

- **Backend**: Python 3 (native HTTP server, no frameworks)
- **Frontend**: HTML5, CSS3, vanilla JavaScript
- **Database**: SQLite (persistent local storage)

## Sample Exams
Hardcoded exams are no longer inserted. Instead, place your JSON files in `exams/` or use the existing `sample_exam.json` to initialize the empty database.

## Project Structure

```
forms/
├── server.py             # Python server
├── exam_system.db        # SQLite database (created on first run)
├── README.md             # This file
└── public/
    ├── index.html        # Main page (login + exams)
    ├── backoffice.html   # Administration panel
    └── styles.css        # Application styles
```

## Database

The application uses SQLite to persist data. The database file `exam_system.db` is automatically created on first run with the following tables:

- **exams**: Stores exam information
- **questions**: Stores questions associated with each exam
- **results**: Stores student exam results

All data persists between server restarts.
