"""
Script para migrar datos del sistema antiguo al nuevo
"""
import json
import sqlite3
from app.core.database import SessionLocal
from app.models import Exam, Question, User, Result
from app.core.security import get_password_hash


def migrate_exams(old_db_path: str = '../exam_system.db'):
    """Migrate exams and questions from old database"""
    db = SessionLocal()
    old_conn = sqlite3.connect(old_db_path)
    old_conn.row_factory = sqlite3.Row
    old_cursor = old_conn.cursor()
    
    try:
        # Get all exams
        old_cursor.execute('SELECT * FROM exams')
        old_exams = old_cursor.fetchall()
        
        print(f"Found {len(old_exams)} exams to migrate...")
        
        for old_exam in old_exams:
            # Create new exam
            new_exam = Exam(
                title=old_exam['title'],
                duration_minutes=old_exam['duration_minutes']
            )
            db.add(new_exam)
            db.flush()
            
            # Get questions for this exam
            old_cursor.execute(
                'SELECT * FROM questions WHERE exam_id = ? ORDER BY question_order',
                (old_exam['id'],)
            )
            old_questions = old_cursor.fetchall()
            
            for old_q in old_questions:
                new_question = Question(
                    exam_id=new_exam.id,
                    question=old_q['question'],
                    options=json.loads(old_q['options']),
                    correct_answer=old_q['correct_answer'],
                    explanation=old_q['explanation'],
                    question_order=old_q['question_order']
                )
                db.add(new_question)
            
            print(f"✅ Migrated exam: {old_exam['title']} with {len(old_questions)} questions")
        
        db.commit()
        print(f"\n✅ Successfully migrated {len(old_exams)} exams!")
        
    except Exception as e:
        print(f"❌ Error migrating data: {e}")
        db.rollback()
        
    finally:
        old_conn.close()
        db.close()


def create_users_from_results(old_db_path: str = '../exam_system.db'):
    """Create user accounts from old results' user_name field"""
    db = SessionLocal()
    old_conn = sqlite3.connect(old_db_path)
    old_conn.row_factory = sqlite3.Row
    old_cursor = old_conn.cursor()
    
    try:
        # Get unique user names from results
        old_cursor.execute('SELECT DISTINCT user_name FROM results')
        old_users = old_cursor.fetchall()
        
        print(f"\nFound {len(old_users)} unique users from results...")
        
        created_users = {}
        
        for old_user in old_users:
            user_name = old_user['user_name']
            email = f"{user_name.lower().replace(' ', '.')}@example.com"
            
            # Check if user already exists
            existing = db.query(User).filter(User.email == email).first()
            if existing:
                created_users[user_name] = existing.id
                continue
            
            # Create user with default password
            new_user = User(
                email=email,
                hashed_password=get_password_hash('password123'),
                full_name=user_name,
                is_admin=False,
                is_active=True
            )
            db.add(new_user)
            db.flush()
            
            created_users[user_name] = new_user.id
            print(f"✅ Created user: {user_name} ({email})")
        
        db.commit()
        print(f"\n✅ Successfully created {len(created_users)} users!")
        
        return created_users
        
    except Exception as e:
        print(f"❌ Error creating users: {e}")
        db.rollback()
        return {}
        
    finally:
        old_conn.close()
        db.close()


if __name__ == "__main__":
    print("=" * 50)
    print("Data Migration Tool")
    print("=" * 50)
    
    old_db = input("Path to old database (default: ../exam_system.db): ") or '../exam_system.db'
    
    print("\n1. Migrating exams and questions...")
    migrate_exams(old_db)
    
    print("\n2. Creating users from results...")
    user_map = create_users_from_results(old_db)
    
    print("\n" + "=" * 50)
    print("Migration completed!")
    print("=" * 50)
    print("\nNOTE: All migrated users have password: 'password123'")
    print("Users should change their password on first login.")
