import PyPDF2
import io
import hashlib
from typing import Dict, List
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re

load_dotenv()

class DocumentProcessor:
    def __init__(self):
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.documents: Dict[str, str] = {}
        self.summaries: Dict[str, str] = {}
    
    def extract_text_from_pdf(self, pdf_content: bytes) -> str:
        """Extract text from PDF bytes"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            raise ValueError(f"Error processing PDF: {str(e)}")
    
    def extract_text_from_txt(self, txt_content: bytes) -> str:
        """Extract text from TXT bytes"""
        try:
            return txt_content.decode('utf-8')
        except Exception as e:
            raise ValueError(f"Error processing TXT: {str(e)}")
    
    def generate_document_id(self, content: str) -> str:
        """Generate unique ID for document based on content"""
        return hashlib.md5(content.encode()).hexdigest()[:16]
    
    def store_document(self, filename: str, content: str) -> str:
        """Store document and return document ID"""
        doc_id = self.generate_document_id(content)
        self.documents[doc_id] = content
        return doc_id
    
    def generate_summary(self, content: str, max_words: int = 150) -> str:
        """Generate summary using Gemini AI"""
        prompt = f"""
        Please provide a concise summary of the following document in no more than {max_words} words.
        Focus on the main points, key findings, and overall purpose of the document.
        
        Document:
        {content[:8000]}
        
        Summary (max {max_words} words):
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def answer_question(self, document_id: str, question: str) -> Dict[str, str]:
        """Answer question based on document content"""
        if document_id not in self.documents:
            raise ValueError("Document not found")
        
        content = self.documents[document_id]
        
        prompt = f"""
        Based on the following document, please answer the question with:
        1. A clear, comprehensive answer
        2. Justification explaining your reasoning
        3. Specific reference to the part of the document that supports your answer
        
        Document:
        {content}
        
        Question: {question}
        
        Please format your response as:
        ANSWER: [Your answer here]
        JUSTIFICATION: [Your reasoning here]
        SOURCE_REFERENCE: [Specific reference to document section/paragraph]
        """
        
        try:
            response = self.model.generate_content(prompt)
            result = self._parse_answer_response(response.text)
            return result
        except Exception as e:
            return {
                "answer": f"Error generating answer: {str(e)}",
                "justification": "",
                "source_reference": ""
            }
    
    def generate_challenge_questions(self, document_id: str) -> List[Dict[str, str]]:
        """Generate 3 logic-based challenge questions"""
        if document_id not in self.documents:
            raise ValueError("Document not found")
        
        content = self.documents[document_id]
        
        prompt = f"""
        Based on the following document, generate exactly 3 challenging questions that require:
        - Deep comprehension
        - Logical reasoning
        - Critical thinking
        
        For each question, provide:
        1. The question itself
        2. The correct answer
        3. A detailed explanation with document reference
        
        Document:
        {content}
        
        Please format your response as:
        QUESTION_1: [Question here]
        ANSWER_1: [Correct answer here]
        EXPLANATION_1: [Detailed explanation with reference]
        
        QUESTION_2: [Question here]
        ANSWER_2: [Correct answer here]
        EXPLANATION_2: [Detailed explanation with reference]
        
        QUESTION_3: [Question here]
        ANSWER_3: [Correct answer here]
        EXPLANATION_3: [Detailed explanation with reference]
        """
        
        try:
            response = self.model.generate_content(prompt)
            questions = self._parse_challenge_questions(response.text)
            return questions
        except Exception as e:
            return [{"question": f"Error generating questions: {str(e)}", "correct_answer": "", "explanation": ""}]
    
    def evaluate_challenge_answer(self, document_id: str, question: str, correct_answer: str, user_answer: str) -> Dict[str, any]:
        """Evaluate user's answer to challenge question"""
        if document_id not in self.documents:
            raise ValueError("Document not found")
        
        content = self.documents[document_id]
        
        prompt = f"""
        Based on the following document and challenge question, evaluate the user's answer:
        
        Document:
        {content}
        
        Question: {question}
        Correct Answer: {correct_answer}
        User's Answer: {user_answer}
        
        Please evaluate the user's answer and provide:
        1. Whether it's correct or not
        2. Detailed feedback
        3. The correct answer
        4. Justification with document reference
        5. A score from 0-100
        
        Format your response as:
        IS_CORRECT: [True/False]
        FEEDBACK: [Detailed feedback on user's answer]
        CORRECT_ANSWER: [The correct answer]
        JUSTIFICATION: [Explanation with document reference]
        SCORE: [0-100]
        """
        
        try:
            response = self.model.generate_content(prompt)
            result = self._parse_evaluation_response(response.text)
            return result
        except Exception as e:
            return {
                "is_correct": False,
                "feedback": f"Error evaluating answer: {str(e)}",
                "correct_answer": correct_answer,
                "justification": "",
                "score": 0
            }
    
    def _parse_answer_response(self, response_text: str) -> Dict[str, str]:
        """Parse the structured response from Gemini AI for answers"""
        answer = re.search(r'ANSWER:\s*(.*?)(?=JUSTIFICATION:|$)', response_text, re.DOTALL)
        justification = re.search(r'JUSTIFICATION:\s*(.*?)(?=SOURCE_REFERENCE:|$)', response_text, re.DOTALL)
        source_ref = re.search(r'SOURCE_REFERENCE:\s*(.*?)$', response_text, re.DOTALL)
        
        return {
            "answer": answer.group(1).strip() if answer else "Unable to parse answer",
            "justification": justification.group(1).strip() if justification else "Unable to parse justification",
            "source_reference": source_ref.group(1).strip() if source_ref else "Unable to parse source reference"
        }
    
    def _parse_challenge_questions(self, response_text: str) -> List[Dict[str, str]]:
        """Parse the structured response from Gemini AI for challenge questions"""
        questions = []
        
        for i in range(1, 4):
            question_match = re.search(fr'QUESTION_{i}:\s*(.*?)(?=ANSWER_{i}:|$)', response_text, re.DOTALL)
            answer_match = re.search(fr'ANSWER_{i}:\s*(.*?)(?=EXPLANATION_{i}:|$)', response_text, re.DOTALL)
            explanation_match = re.search(fr'EXPLANATION_{i}:\s*(.*?)(?=QUESTION_{i+1}:|$)', response_text, re.DOTALL)
            
            if question_match:
                questions.append({
                    "question": question_match.group(1).strip(),
                    "correct_answer": answer_match.group(1).strip() if answer_match else "",
                    "explanation": explanation_match.group(1).strip() if explanation_match else ""
                })
        
        return questions if questions else [{"question": "Error parsing questions", "correct_answer": "", "explanation": ""}]
    
    def _parse_evaluation_response(self, response_text: str) -> Dict[str, any]:
        """Parse the structured response from Gemini AI for evaluation"""
        is_correct_match = re.search(r'IS_CORRECT:\s*(True|False)', response_text, re.IGNORECASE)
        feedback_match = re.search(r'FEEDBACK:\s*(.*?)(?=CORRECT_ANSWER:|$)', response_text, re.DOTALL)
        correct_answer_match = re.search(r'CORRECT_ANSWER:\s*(.*?)(?=JUSTIFICATION:|$)', response_text, re.DOTALL)
        justification_match = re.search(r'JUSTIFICATION:\s*(.*?)(?=SCORE:|$)', response_text, re.DOTALL)
        score_match = re.search(r'SCORE:\s*(\d+)', response_text)
        
        return {
            "is_correct": is_correct_match.group(1).lower() == 'true' if is_correct_match else False,
            "feedback": feedback_match.group(1).strip() if feedback_match else "Unable to parse feedback",
            "correct_answer": correct_answer_match.group(1).strip() if correct_answer_match else "Unable to parse correct answer",
            "justification": justification_match.group(1).strip() if justification_match else "Unable to parse justification",
            "score": int(score_match.group(1)) if score_match else 0
        }
