from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user, get_current_admin_user
from app.models.user import User as UserModel
from app.models.exam import Exam as ExamModel
from app.models.question import Question as QuestionModel
from app.models.result import Result as ResultModel
from app.schemas.result import (
    Result, ResultCreate, ResultWithDetails, ResultDetailed, ResultDetail
)

router = APIRouter()


@router.post("/", response_model=ResultDetailed, status_code=status.HTTP_201_CREATED)
def submit_exam(
    result_data: ResultCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Submit exam answers and get results"""
    # Get exam with questions
    exam = db.query(ExamModel).filter(ExamModel.id == result_data.exam_id).first()
    
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found"
        )
    
    # Get all questions
    questions = sorted(exam.questions, key=lambda x: x.question_order)
    
    # Calculate score
    correct_count = 0
    answers_list = []
    details = []
    
    for answer in result_data.answers:
        # Find the question
        question = next((q for q in questions if q.id == answer.question_id), None)
        
        if not question:
            continue
        
        is_correct = question.correct_answer == answer.selected_answer
        if is_correct:
            correct_count += 1
        
        answers_list.append({
            "question_id": answer.question_id,
            "selected_answer": answer.selected_answer,
            "is_correct": is_correct
        })
        
        details.append(ResultDetail(
            question_id=question.id,
            question=question.question,
            options=question.options,
            user_answer=answer.selected_answer,
            correct_answer=question.correct_answer,
            is_correct=is_correct,
            explanation=question.explanation
        ))
    
    total_questions = len(questions)
    score = (correct_count / total_questions * 100) if total_questions > 0 else 0
    
    # Save result
    db_result = ResultModel(
        user_id=current_user.id,
        exam_id=exam.id,
        answers=answers_list,
        score=score,
        correct_answers=correct_count,
        total_questions=total_questions
    )
    
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    
    return ResultDetailed(
        id=db_result.id,
        user_id=db_result.user_id,
        exam_id=db_result.exam_id,
        answers=db_result.answers,
        score=db_result.score,
        correct_answers=db_result.correct_answers,
        total_questions=db_result.total_questions,
        created_at=db_result.created_at,
        exam_title=exam.title,
        details=details
    )


@router.get("/my", response_model=List[ResultWithDetails])
def get_my_results(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get current user's exam results"""
    results = db.query(ResultModel).filter(
        ResultModel.user_id == current_user.id
    ).order_by(ResultModel.created_at.desc()).offset(skip).limit(limit).all()
    
    results_with_details = []
    for result in results:
        exam = db.query(ExamModel).filter(ExamModel.id == result.exam_id).first()
        results_with_details.append(ResultWithDetails(
            id=result.id,
            user_id=result.user_id,
            exam_id=result.exam_id,
            answers=result.answers,
            score=result.score,
            correct_answers=result.correct_answers,
            total_questions=result.total_questions,
            created_at=result.created_at,
            user_email=current_user.email,
            user_name=current_user.full_name or current_user.email,
            exam_title=exam.title if exam else "Unknown"
        ))
    
    return results_with_details


@router.get("/{result_id}", response_model=ResultDetailed)
def get_result_detail(
    result_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get detailed result for a specific exam submission"""
    result = db.query(ResultModel).filter(ResultModel.id == result_id).first()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Result not found"
        )
    
    # Check if user owns this result or is admin
    if result.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this result"
        )
    
    # Get exam and questions
    exam = db.query(ExamModel).filter(ExamModel.id == result.exam_id).first()
    
    details = []
    for answer in result.answers:
        question = db.query(QuestionModel).filter(
            QuestionModel.id == answer["question_id"]
        ).first()
        
        if question:
            details.append(ResultDetail(
                question_id=question.id,
                question=question.question,
                options=question.options,
                user_answer=answer["selected_answer"],
                correct_answer=question.correct_answer,
                is_correct=answer["is_correct"],
                explanation=question.explanation
            ))
    
    return ResultDetailed(
        id=result.id,
        user_id=result.user_id,
        exam_id=result.exam_id,
        answers=result.answers,
        score=result.score,
        correct_answers=result.correct_answers,
        total_questions=result.total_questions,
        created_at=result.created_at,
        exam_title=exam.title if exam else "Unknown",
        details=details
    )


@router.get("/", response_model=List[ResultWithDetails])
def get_all_results(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_admin_user)
):
    """Get all exam results (admin only)"""
    results = db.query(ResultModel).order_by(
        ResultModel.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    results_with_details = []
    for result in results:
        user = db.query(UserModel).filter(UserModel.id == result.user_id).first()
        exam = db.query(ExamModel).filter(ExamModel.id == result.exam_id).first()
        
        results_with_details.append(ResultWithDetails(
            id=result.id,
            user_id=result.user_id,
            exam_id=result.exam_id,
            answers=result.answers,
            score=result.score,
            correct_answers=result.correct_answers,
            total_questions=result.total_questions,
            created_at=result.created_at,
            user_email=user.email if user else "Unknown",
            user_name=user.full_name if user and user.full_name else (user.email if user else "Unknown"),
            exam_title=exam.title if exam else "Unknown"
        ))
    
    return results_with_details


@router.delete("/{result_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_result(
    result_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_admin_user)
):
    """Delete a result (admin only)"""
    result = db.query(ResultModel).filter(ResultModel.id == result_id).first()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Result not found"
        )
    
    db.delete(result)
    db.commit()
    
    return None
