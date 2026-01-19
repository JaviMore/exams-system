"""
Script para importar exámenes desde archivos JSON
"""
import json
import os
import sys
from pathlib import Path

from app.core.database import SessionLocal
from app.models import Exam, Question


def import_exam_from_json(file_path: str):
    """Import an exam from a JSON file"""
    db = SessionLocal()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle both single exam and array of exams
        exams_data = data if isinstance(data, list) else [data]
        
        imported_count = 0
        
        for exam_data in exams_data:
            if 'title' not in exam_data or 'questions' not in exam_data:
                print(f"⚠️ Skipping invalid exam format in {file_path}")
                continue
            
            # Check if exam already exists
            existing = db.query(Exam).filter(Exam.title == exam_data['title']).first()
            if existing:
                print(f"⚠️ Exam '{exam_data['title']}' already exists, skipping...")
                continue
            
            # Create exam
            exam = Exam(
                title=exam_data['title'],
                duration_minutes=exam_data.get('durationMinutes', 30)
            )
            db.add(exam)
            db.flush()
            
            # Create questions
            for idx, q_data in enumerate(exam_data['questions']):
                question = Question(
                    exam_id=exam.id,
                    question=q_data['question'],
                    options=q_data['options'],
                    correct_answer=q_data.get('correctAnswer', 0),
                    explanation=q_data.get('explanation', ''),
                    question_order=idx + 1
                )
                db.add(question)
            
            db.commit()
            imported_count += 1
            print(f"✅ Imported exam: {exam_data['title']} ({len(exam_data['questions'])} questions)")
        
        return imported_count
        
    except Exception as e:
        print(f"❌ Error importing {file_path}: {e}")
        db.rollback()
        return 0
        
    finally:
        db.close()


def import_exams_from_directory(directory: str = '../exams'):
    """Import all JSON files from a directory"""
    path = Path(directory)
    
    if not path.exists():
        print(f"❌ Directory not found: {directory}")
        return
    
    json_files = list(path.glob('*.json'))
    
    if not json_files:
        print(f"⚠️ No JSON files found in {directory}")
        return
    
    print(f"Found {len(json_files)} JSON files")
    print("=" * 50)
    
    total_imported = 0
    
    for json_file in json_files:
        print(f"\nImporting {json_file.name}...")
        count = import_exam_from_json(str(json_file))
        total_imported += count
    
    print("\n" + "=" * 50)
    print(f"✅ Successfully imported {total_imported} exams!")


if __name__ == "__main__":
    print("=" * 50)
    print("Exam Import Tool")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        # Import specific file or directory
        path = sys.argv[1]
        
        if os.path.isfile(path):
            print(f"\nImporting file: {path}")
            import_exam_from_json(path)
        elif os.path.isdir(path):
            print(f"\nImporting from directory: {path}")
            import_exams_from_directory(path)
        else:
            print(f"❌ Path not found: {path}")
    else:
        # Default: import from ../exams directory
        import_exams_from_directory('../exams')
