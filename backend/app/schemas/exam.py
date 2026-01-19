from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class QuestionBase(BaseModel):
    question: str
    options: List[str]
    correct_answer: int
    explanation: str


class QuestionCreate(QuestionBase):
    pass


class QuestionInDB(QuestionBase):
    id: int
    exam_id: int
    question_order: int
    
    class Config:
        from_attributes = True


class Question(QuestionInDB):
    pass


class QuestionForStudent(BaseModel):
    """Question without correct answer for students taking exam"""
    id: int
    question: str
    options: List[str]
    
    class Config:
        from_attributes = True


class ExamBase(BaseModel):
    title: str
    duration_minutes: int = 30


class ExamCreate(ExamBase):
    questions: List[QuestionCreate]


class ExamUpdate(BaseModel):
    title: Optional[str] = None
    duration_minutes: Optional[int] = None
    questions: Optional[List[QuestionCreate]] = None


class ExamInDB(ExamBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class Exam(ExamInDB):
    questions: List[Question] = []


class ExamForStudent(ExamInDB):
    """Exam without correct answers for students"""
    questions: List[QuestionForStudent] = []


class ExamList(ExamInDB):
    """Exam in list view without questions"""
    question_count: Optional[int] = 0
