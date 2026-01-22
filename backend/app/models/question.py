from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.core.database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id", ondelete="CASCADE"), nullable=False)
    question = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)  # List of options
    correct_answer = Column(Integer, nullable=False)  # Index of correct option
    explanation = Column(Text, nullable=False)
    question_order = Column(Integer, nullable=False)

    # Relationships
    exam = relationship("Exam", back_populates="questions")
