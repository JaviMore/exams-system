from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user, get_current_admin_user
from app.models.user import User as UserModel
from app.models.exam import Exam as ExamModel
from app.models.question import Question as QuestionModel
from app.schemas.exam import (
    Exam, ExamCreate, ExamUpdate, ExamList, ExamForStudent,
    QuestionForStudent
)

router = APIRouter()


@router.get("/", response_model=List[ExamList])
def get_exams(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get all exams (list view)"""
    exams = db.query(ExamModel).offset(skip).limit(limit).all()
    
    result = []
    for exam in exams:
        exam_dict = {
            "id": exam.id,
            "title": exam.title,
            "duration_minutes": exam.duration_minutes,
            "created_at": exam.created_at,
            "question_count": len(exam.questions)
        }
        result.append(exam_dict)
    
    return result


@router.get("/{exam_id}", response_model=ExamForStudent)
def get_exam(
    exam_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get a specific exam (without correct answers for students)"""
    exam = db.query(ExamModel).filter(ExamModel.id == exam_id).first()
    
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found"
        )
    
    # Return exam without correct answers
    questions_for_student = [
        QuestionForStudent(
            id=q.id,
            question=q.question,
            options=q.options
        )
        for q in sorted(exam.questions, key=lambda x: x.question_order)
    ]
    
    return ExamForStudent(
        id=exam.id,
        title=exam.title,
        duration_minutes=exam.duration_minutes,
        created_at=exam.created_at,
        questions=questions_for_student
    )


@router.get("/{exam_id}/full", response_model=Exam)
def get_exam_full(
    exam_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_admin_user)
):
    """Get a specific exam with all details including correct answers (admin only)"""
    exam = db.query(ExamModel).filter(ExamModel.id == exam_id).first()
    
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found"
        )
    
    return exam


@router.post("/", response_model=Exam, status_code=status.HTTP_201_CREATED)
def create_exam(
    exam_data: ExamCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_admin_user)
):
    """Create a new exam (admin only)"""
    # Create exam
    db_exam = ExamModel(
        title=exam_data.title,
        duration_minutes=exam_data.duration_minutes
    )
    
    db.add(db_exam)
    db.flush()  # Get the exam ID
    
    # Create questions
    for idx, question_data in enumerate(exam_data.questions):
        db_question = QuestionModel(
            exam_id=db_exam.id,
            question=question_data.question,
            options=question_data.options,
            correct_answer=question_data.correct_answer,
            explanation=question_data.explanation,
            question_order=idx + 1
        )
        db.add(db_question)
    
    db.commit()
    db.refresh(db_exam)
    
    return db_exam


@router.put("/{exam_id}", response_model=Exam)
def update_exam(
    exam_id: int,
    exam_data: ExamUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_admin_user)
):
    """Update an exam (admin only)"""
    exam = db.query(ExamModel).filter(ExamModel.id == exam_id).first()
    
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found"
        )
    
    # Update basic fields
    if exam_data.title is not None:
        exam.title = exam_data.title
    if exam_data.duration_minutes is not None:
        exam.duration_minutes = exam_data.duration_minutes
    
    # Update questions if provided
    if exam_data.questions is not None:
        # Delete existing questions
        db.query(QuestionModel).filter(QuestionModel.exam_id == exam_id).delete()
        
        # Create new questions
        for idx, question_data in enumerate(exam_data.questions):
            db_question = QuestionModel(
                exam_id=exam.id,
                question=question_data.question,
                options=question_data.options,
                correct_answer=question_data.correct_answer,
                explanation=question_data.explanation,
                question_order=idx + 1
            )
            db.add(db_question)
    
    db.commit()
    db.refresh(exam)
    
    return exam


@router.delete("/{exam_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_exam(
    exam_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_admin_user)
):
    """Delete an exam (admin only)"""
    exam = db.query(ExamModel).filter(ExamModel.id == exam_id).first()
    
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found"
        )
    
    db.delete(exam)
    db.commit()
    
    return None
