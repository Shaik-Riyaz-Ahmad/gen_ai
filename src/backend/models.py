from pydantic import BaseModel
from typing import List, Optional

class DocumentUpload(BaseModel):
    filename: str
    content: str

class QuestionRequest(BaseModel):
    question: str
    document_id: str

class ChallengeQuestion(BaseModel):
    question: str
    correct_answer: str
    explanation: str

class ChallengeResponse(BaseModel):
    user_answer: str
    question_id: int
    document_id: str

class AnswerResponse(BaseModel):
    answer: str
    justification: str
    source_reference: str

class ChallengeEvaluation(BaseModel):
    is_correct: bool
    feedback: str
    correct_answer: str
    justification: str
    score: int  # 0-100
