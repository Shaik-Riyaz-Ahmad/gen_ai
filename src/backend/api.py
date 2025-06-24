from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from document_processor import DocumentProcessor
from models import QuestionRequest, ChallengeResponse, AnswerResponse, ChallengeEvaluation
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="GenAI Document Assistant", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize document processor
doc_processor = DocumentProcessor()

@app.post("/upload-document/")
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document (PDF or TXT)"""
    try:
        # Validate file type
        if not file.filename.lower().endswith(('.pdf', '.txt')):
            raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported")
        
        # Read file content
        content = await file.read()
        
        # Extract text based on file type
        if file.filename.lower().endswith('.pdf'):
            text = doc_processor.extract_text_from_pdf(content)
        else:
            text = doc_processor.extract_text_from_txt(content)
        
        # Store document
        doc_id = doc_processor.store_document(file.filename, text)
        
        # Generate summary
        summary = doc_processor.generate_summary(text)
        
        return JSONResponse({
            "success": True,
            "document_id": doc_id,
            "filename": file.filename,
            "summary": summary,
            "word_count": len(text.split())
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask-question/")
async def ask_question(request: QuestionRequest):
    """Answer a question based on the uploaded document"""
    try:
        result = doc_processor.answer_question(request.document_id, request.question)
        
        return AnswerResponse(
            answer=result["answer"],
            justification=result["justification"],
            source_reference=result["source_reference"]
        )
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-challenge/")
async def generate_challenge(document_id: str):
    """Generate challenge questions for the document"""
    try:
        questions = doc_processor.generate_challenge_questions(document_id)
        
        return JSONResponse({
            "success": True,
            "questions": questions
        })
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/evaluate-answer/")
async def evaluate_answer(request: ChallengeResponse):
    """Evaluate user's answer to a challenge question"""
    try:
        # This would need to be enhanced to store challenge questions
        # For now, we'll use a simplified approach
        result = doc_processor.evaluate_challenge_answer(
            request.document_id,
            "question",  # You'd need to store and retrieve the actual question
            "correct_answer",  # You'd need to store and retrieve the correct answer
            request.user_answer
        )
        
        return ChallengeEvaluation(
            is_correct=result["is_correct"],
            feedback=result["feedback"],
            correct_answer=result["correct_answer"],
            justification=result["justification"],
            score=result["score"]
        )
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health/")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
