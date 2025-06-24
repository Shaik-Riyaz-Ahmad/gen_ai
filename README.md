# GenAI Document Comprehension Assistant

A powerful AI-driven document analysis tool that enables deep comprehension and logical reasoning over uploaded documents. Built with Google's Gemini AI, FastAPI, and Streamlit.

## 🚀 Features

- **Document Upload**: Support for PDF and TXT files
- **Auto Summary**: Generate concise summaries (≤150 words) immediately after upload
- **Ask Anything Mode**: Ask free-form questions with contextual understanding
- **Challenge Me Mode**: AI-generated logic-based questions with evaluation
- **Contextual Grounding**: All answers referenced to source document
- **Memory Handling**: Follow-up questions with context maintenance
- **Answer Highlighting**: Source snippets displayed with responses

## 🏗️ Architecture

```
Frontend (Streamlit) ←→ Backend (FastAPI) ←→ AI Engine (Gemini)
                                ↓
                        Document Processor
                                ↓
                          File Storage
```

### Components

1. **Frontend (Streamlit)**: Interactive web interface
2. **Backend (FastAPI)**: REST API for document processing and AI interactions
3. **Document Processor**: Handles PDF/TXT extraction and storage
4. **AI Engine**: Google Gemini integration for comprehension and reasoning
5. **Models**: Pydantic models for data validation

## 📋 Requirements

- Python 3.8+
- Google Gemini API key
- 10MB+ available storage for documents

## 🛠️ Setup Instructions

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd gen_ai
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Gemini API key
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### 4. Get Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your `.env` file

### 5. Run the Application

**Terminal 1 - Start Backend:**
```bash
cd src
python backend/api.py
```

**Terminal 2 - Start Frontend:**
```bash
cd src
streamlit run app.py
```

### 6. Access the Application
Open your browser and navigate to: `http://localhost:8501`

## 🎯 Usage Guide

### Document Upload
1. Click "Choose a PDF or TXT file"
2. Select your document
3. Wait for processing and auto-summary generation

### Ask Anything Mode
1. Click "Ask Anything Mode"
2. Type your question in the text input
3. Click "Get Answer" to receive AI-powered responses with:
   - Comprehensive answer
   - Detailed justification
   - Source reference from document

### Challenge Me Mode
1. Click "Challenge Me Mode"
2. Click "Generate Challenge Questions"
3. Answer the 3 AI-generated logic-based questions
4. Receive evaluation and feedback for each response

## 🔧 API Endpoints

### Document Management
- `POST /upload-document/` - Upload and process documents
- `GET /health/` - Health check

### AI Interactions
- `POST /ask-question/` - Ask questions about documents
- `POST /generate-challenge/` - Generate challenge questions
- `POST /evaluate-answer/` - Evaluate challenge responses

## 🧠 AI Reasoning Flow

1. **Document Processing**:
   - Text extraction (PDF/TXT)
   - Content validation and storage
   - Unique ID generation

2. **Summary Generation**:
   - Gemini AI analyzes full document
   - Extracts key points and findings
   - Generates ≤150 word summary

3. **Question Answering**:
   - Context-aware processing
   - Document-grounded responses
   - Source reference identification

4. **Challenge Generation**:
   - Deep comprehension analysis
   - Logic-based question creation
   - Difficulty assessment

5. **Answer Evaluation**:
   - Response comparison
   - Feedback generation
   - Scoring (0-100)

## 📁 Project Structure

```
gen_ai/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── .env.example             # Environment template
├── src/
│   ├── app.py              # Streamlit frontend
│   ├── backend/
│   │   ├── api.py          # FastAPI backend
│   │   ├── models.py       # Pydantic models
│   │   └── document_processor.py # Document handling & AI
│   └── utils/
│       └── helpers.py      # Utility functions
└── uploads/                # Document storage
```

## 🎨 Features Implemented

### Core Requirements
- ✅ PDF/TXT document upload
- ✅ Ask Anything mode with contextual understanding
- ✅ Challenge Me mode with AI-generated questions
- ✅ Auto summary (≤150 words)
- ✅ Source-grounded responses
- ✅ Clean web interface

### Bonus Features
- ✅ Memory handling for follow-up questions
- ✅ Answer highlighting with source snippets
- ✅ Conversation history
- ✅ Modern responsive UI
- ✅ Error handling and validation

## 🔍 Example Interactions

### Ask Anything Mode
```
Q: "What are the main conclusions of this research?"
A: "Based on the document analysis, the main conclusions are... 
   [Detailed response with justification and source reference]"
```

### Challenge Me Mode
```
Generated Question: "Based on the methodology described, what potential 
limitations might affect the study's validity?"
[User provides answer]
[AI evaluates with detailed feedback and scoring]
```

## 🛡️ Error Handling

- File type validation (PDF/TXT only)
- File size limits (configurable)
- API error responses
- Connection health checks
- Graceful fallbacks

## 🚀 Deployment Considerations

### Local Development
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:8501`

### Production
- Use environment variables for API keys
- Implement proper logging
- Add rate limiting
- Use HTTPS
- Configure CORS appropriately

## 🔧 Configuration

### Environment Variables
```bash
GEMINI_API_KEY=your_key_here    # Required
DEBUG=True                      # Optional
MAX_FILE_SIZE_MB=10            # Optional
UPLOAD_DIR=uploads             # Optional
```

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues, questions, or contributions, please open an issue in the repository.

---

**Built with ❤️ using Google Gemini AI, FastAPI, and Streamlit**
