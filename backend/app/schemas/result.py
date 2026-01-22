from pydantic import BaseModel
from typing import List
from datetime import datetime


class AnswerSubmit(BaseModel):
    question_id: int
    selected_answer: int


class ResultCreate(BaseModel):
    exam_id: int
    answers: List[AnswerSubmit]


class ResultInDB(BaseModel):
    id: int
    user_id: int
    exam_id: int
    answers: List[dict]
    score: float
    correct_answers: int
    total_questions: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class Result(ResultInDB):
    pass


class ResultWithDetails(Result):
    user_email: str
    user_name: str
    exam_title: str


class ResultDetail(BaseModel):
    question_id: int
    question: str
    options: List[str]
    user_answer: int
    correct_answer: int
    is_correct: bool
    explanation: str


class ResultDetailed(Result):
    exam_title: str
    details: List[ResultDetail]
