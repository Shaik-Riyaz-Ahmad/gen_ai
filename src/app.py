import streamlit as st
import requests
import json
import os
import sys
from typing import Dict, List

# Add backend directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Page configuration
st.set_page_config(
    page_title="GenAI Document Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Modern Robot-Themed CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #1a1d29 0%, #2d3748 50%, #1a1d29 100%);
        font-family: 'Inter', sans-serif;
        color: #e2e8f0;
    }
    
    /* Add subtle robot pattern */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 25% 25%, #667eea15 0%, transparent 50%),
            radial-gradient(circle at 75% 75%, #764ba215 0%, transparent 50%);
        z-index: -1;
        pointer-events: none;
    }
    
    .main .block-container {
        padding: 2rem;
        background: rgba(45, 55, 72, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        margin: 1rem;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    /* Header Styles */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #e2e8f0;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #cbd5e0;
        margin: 1.5rem 0;
        padding-left: 1rem;
        border-left: 4px solid #667eea;
    }
    
    /* Card Styles */
    .summary-card, .question-card, .answer-card, .evaluation-card {
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(102, 126, 234, 0.3);
    }
    
    .summary-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .question-card {
        background: rgba(102, 126, 234, 0.1);
        color: #e2e8f0;
        border-color: #667eea;
    }
    
    .answer-card {
        background: rgba(17, 153, 142, 0.1);
        color: #e2e8f0;
        border-color: #11998e;
    }
    
    .evaluation-card {
        background: rgba(118, 75, 162, 0.1);
        color: #e2e8f0;
        border-color: #764ba2;
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    /* Input Styles */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(45, 55, 72, 0.8);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 8px;
        color: #e2e8f0;
        padding: 0.75rem;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
    
    /* File Uploader */
    .stFileUploader > div {
        border: 2px dashed #667eea;
        border-radius: 12px;
        padding: 2rem;
        background: rgba(102, 126, 234, 0.05);
        text-align: center;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1d29 0%, #2d3748 100%);
    }
    
    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stDeployButton {display:none;}
    
    [data-testid="stDecoration"] {display:none;}
    
</style>
""", unsafe_allow_html=True)

class DocumentAssistant:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        
    def upload_document(self, file):
        """Upload document to backend"""
        files = {"file": (file.name, file.getvalue(), file.type)}
        response = requests.post(f"{self.base_url}/upload-document/", files=files)
        return response.json()
    
    def ask_question(self, document_id: str, question: str):
        """Ask a question about the document"""
        data = {"document_id": document_id, "question": question}
        response = requests.post(f"{self.base_url}/ask-question/", json=data)
        return response.json()
    
    def generate_challenge(self, document_id: str):
        """Generate challenge questions"""
        response = requests.post(f"{self.base_url}/generate-challenge/", params={"document_id": document_id})
        return response.json()
    
    def evaluate_answer(self, document_id: str, question_id: int, user_answer: str):
        """Evaluate user's answer"""
        data = {
            "document_id": document_id,
            "question_id": question_id,
            "user_answer": user_answer
        }
        response = requests.post(f"{self.base_url}/evaluate-answer/", json=data)
        return response.json()

def initialize_session_state():
    """Initialize session state variables"""
    if 'document_uploaded' not in st.session_state:
        st.session_state.document_uploaded = False
    if 'document_id' not in st.session_state:
        st.session_state.document_id = None
    if 'document_summary' not in st.session_state:
        st.session_state.document_summary = None
    if 'challenge_questions' not in st.session_state:
        st.session_state.challenge_questions = []
    if 'current_mode' not in st.session_state:
        st.session_state.current_mode = None
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

def display_header():
    """Display the main header with animations and robot theme"""
    st.markdown('''
    <div class="fade-in-up" style="position: relative;">
        <div style="text-align: center; margin-bottom: 1rem;">
            <div style="font-size: 4rem; margin-bottom: 0.5rem;">🤖</div>
            <h1 class="main-header">GenAI Document Assistant</h1>
            <div style="display: flex; justify-content: center; align-items: center; gap: 1rem; margin: 1rem 0;">
                <span style="font-size: 1.5rem;">🧠</span>
                <div style="width: 50px; height: 2px; background: linear-gradient(90deg, #667eea, #764ba2); border-radius: 1px;"></div>
                <span style="font-size: 1.5rem;">📚</span>
                <div style="width: 50px; height: 2px; background: linear-gradient(90deg, #764ba2, #667eea); border-radius: 1px;"></div>
                <span style="font-size: 1.5rem;">✨</span>
            </div>
            <p style="font-size: 1.2rem; color: #4a5568; font-weight: 500; max-width: 600px; margin: 0 auto;">
                Transform your documents into interactive knowledge with AI-powered comprehension
            </p>
        </div>
    </div>
    
    <style>
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
    </style>
    ''', unsafe_allow_html=True)
    
    # Status indicator
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            response = requests.get("http://localhost:8000/health/", timeout=2)
            if response.status_code == 200:
                st.markdown('''
                <div style="text-align: center;">
                    <span class="status-badge status-online">🟢 AI Engine Online</span>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown('''
                <div style="text-align: center;">
                    <span class="status-badge status-offline">🔴 AI Engine Offline</span>
                </div>
                ''', unsafe_allow_html=True)
        except:
            st.markdown('''
            <div style="text-align: center;">
                <span class="status-badge status-offline">🔴 AI Engine Offline</span>
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown("---")

def handle_document_upload():
    """Handle document upload functionality with enhanced UI"""
    st.markdown('<h2 class="sub-header">📁 Document Upload</h2>', unsafe_allow_html=True)
    
    # Upload area
    uploaded_file = st.file_uploader(
        "",
        type=['pdf', 'txt'],
        help="Upload a PDF or TXT document to get started with AI analysis",
        label_visibility="collapsed"
    )
    
    if uploaded_file is None:
        st.markdown('''
        <div class="metric-card" style="text-align: center;">
            <h3 style="color: #667eea; margin-bottom: 1rem;">📄 Ready to Upload</h3>
            <p style="color: #718096; margin: 0;">
                Drop your PDF or TXT file above to begin intelligent document analysis
            </p>
        </div>
        ''', unsafe_allow_html=True)
    
    # Features card below upload area
    st.markdown('''
    <div class="metric-card">
        <h4 style="color: #667eea; margin-bottom: 1rem; text-align: left;">✨ Features</h4>
        <div style="text-align: justify; color: #718096;">
            <p>🔍 Auto Summarization</p>
            <p>💬 Smart Q&A</p>
            <p>🎯 Challenge Mode</p>
            <p>📚 Source Citations</p>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    if uploaded_file is not None and not st.session_state.document_uploaded:
        # Progress indicator
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Simulate processing steps
            status_text.text("🔄 Uploading document...")
            progress_bar.progress(25)
            
            assistant = DocumentAssistant()
            status_text.text("🧠 Processing with AI...")
            progress_bar.progress(50)
            
            result = assistant.upload_document(uploaded_file)
            progress_bar.progress(75)
            
            if result.get("success"):
                status_text.text("✅ Analysis complete!")
                progress_bar.progress(100)
                
                st.session_state.document_uploaded = True
                st.session_state.document_id = result["document_id"]
                st.session_state.document_summary = result["summary"]
                
                # Success animation
                st.success(f"🎉 Document '{result['filename']}' processed successfully!")
                st.balloons()
                st.rerun()
            else:
                st.error("❌ Failed to upload document")
                
        except Exception as e:
            st.error(f"❌ Error uploading document: {str(e)}")

def display_document_summary():
    """Display document summary with enhanced styling"""
    if st.session_state.document_summary:
        st.markdown('<h2 class="sub-header">📄 Document Intelligence</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f'''
            <div class="summary-card fade-in-up">
                <h3 style="margin-bottom: 1rem; font-size: 1.4rem;">📊 Auto-Generated Summary</h3>
                <p style="font-size: 1.1rem; line-height: 1.6; margin: 0;">
                    {st.session_state.document_summary}
                </p>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'''
            <div class="metric-card">
                <h4 style="color: #667eea; margin-bottom: 1rem;">📈 Analytics</h4>
                <div style="text-align: center;">
                    <p><strong>Document ID</strong></p>
                    <p style="color: #718096; font-family: monospace; font-size: 0.8rem;">
                        {st.session_state.document_id[:8]}...
                    </p>
                    <br>
                    <p><strong>Status</strong></p>
                    <span class="status-badge status-online">Ready</span>
                </div>
            </div>
            ''', unsafe_allow_html=True)

def handle_ask_anything_mode():
    """Handle Ask Anything interaction mode with enhanced UI"""
    st.markdown('<h2 class="sub-header">💬 Ask Anything Mode</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        question = st.text_input(
            "",
            placeholder="Ask me anything about your document...",
            key="ask_question",
            label_visibility="collapsed"
        )
    
    with col2:
        ask_button = st.button("🚀 Get Answer", key="ask_button", use_container_width=True)
    
    if ask_button and question:
        with st.spinner("🧠 AI is analyzing your question..."):
            try:
                assistant = DocumentAssistant()
                result = assistant.ask_question(st.session_state.document_id, question)
                
                # Display question
                st.markdown(f'''
                <div class="question-card fade-in-up">
                    <h4 style="margin-bottom: 1rem;">❓ Your Question</h4>
                    <p style="font-size: 1.1rem; margin: 0;">{question}</p>
                </div>
                ''', unsafe_allow_html=True)
                
                # Display answer
                st.markdown(f'''
                <div class="answer-card fade-in-up">
                    <h4 style="margin-bottom: 1rem;">🤖 AI Response</h4>
                    <p style="font-size: 1.1rem; line-height: 1.6; margin-bottom: 1.5rem;">
                        {result["answer"]}
                    </p>
                    <div style="border-top: 1px solid rgba(255,255,255,0.3); padding-top: 1rem;">
                        <p style="margin-bottom: 0.5rem;"><strong>📝 Reasoning:</strong></p>
                        <p style="margin-bottom: 1rem; opacity: 0.9;">{result["justification"]}</p>
                        <p style="margin-bottom: 0.5rem;"><strong>📍 Source:</strong></p>
                        <p style="margin: 0; opacity: 0.9;">{result["source_reference"]}</p>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                
                # Add to conversation history
                st.session_state.conversation_history.append({
                    "question": question,
                    "answer": result["answer"],
                    "justification": result["justification"],
                    "source_reference": result["source_reference"]
                })
                
            except Exception as e:
                st.error(f"❌ Error getting answer: {str(e)}")
    elif ask_button and not question:
        st.warning("⚠️ Please enter a question to get started!")
    
    # Display recent conversations if any
    if st.session_state.conversation_history:
        st.markdown("---")
        st.markdown('<h3 class="sub-header">📚 Recent Conversations</h3>', unsafe_allow_html=True)
        
        # Show last 3 conversations
        for i, conv in enumerate(st.session_state.conversation_history[-3:]):
            with st.expander(f"💬 {conv['question'][:50]}..."):
                st.markdown(f"**Answer:** {conv['answer']}")
                st.markdown(f"**Source:** {conv['source_reference']}")

def handle_challenge_mode():
    """Handle Challenge Me interaction mode with enhanced UI"""
    st.markdown('<h2 class="sub-header">🎯 Challenge Me Mode</h2>', unsafe_allow_html=True)
    
    if not st.session_state.challenge_questions:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('''
            <div class="metric-card pulse">
                <h3 style="color: #f093fb; margin-bottom: 1rem;">🎯 Ready for Challenge?</h3>
                <p style="color: #718096; margin-bottom: 1.5rem;">
                    Test your comprehension with AI-generated questions based on your document
                </p>
            </div>
            ''', unsafe_allow_html=True)
            
            if st.button("🚀 Generate Challenge Questions", key="generate_challenge", use_container_width=True):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                with st.spinner("🧠 AI is crafting challenging questions..."):
                    try:
                        status_text.text("🔍 Analyzing document complexity...")
                        progress_bar.progress(33)
                        
                        assistant = DocumentAssistant()
                        status_text.text("🎯 Generating comprehension challenges...")
                        progress_bar.progress(66)
                        
                        result = assistant.generate_challenge(st.session_state.document_id)
                        progress_bar.progress(100)
                        status_text.text("✅ Challenge ready!")
                        
                        if result.get("success"):
                            st.session_state.challenge_questions = result["questions"]
                            st.success("🎉 Challenge questions generated! Get ready to test your knowledge!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to generate questions")
                            
                    except Exception as e:
                        st.error(f"❌ Error generating questions: {str(e)}")
    
    else:
        st.markdown('''
        <div class="metric-card">
            <h3 style="color: #f093fb; text-align: center;">🎯 Challenge Active</h3>
            <p style="color: #718096; text-align: center; margin: 0;">
                Answer the questions below based on your document knowledge
            </p>
        </div>
        ''', unsafe_allow_html=True)
        
        for i, question_data in enumerate(st.session_state.challenge_questions):
            st.markdown(f"### Question {i+1} of {len(st.session_state.challenge_questions)}")
            
            st.markdown(f'''
            <div class="question-card">
                <h4 style="margin-bottom: 1rem;">🤔 Challenge Question</h4>
                <p style="font-size: 1.1rem; line-height: 1.6; margin: 0;">
                    {question_data["question"]}
                </p>
            </div>
            ''', unsafe_allow_html=True)
            
            user_answer = st.text_area(
                f"Your answer for question {i+1}:",
                key=f"answer_{i}",
                placeholder="Type your comprehensive answer here...",
                height=100
            )
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button(f"📝 Submit Answer {i+1}", key=f"submit_{i}", use_container_width=True):
                    if user_answer.strip():
                        with st.spinner("🔍 AI is evaluating your response..."):
                            try:
                                # Display evaluation
                                st.markdown(f'''
                                <div class="evaluation-card fade-in-up">
                                    <h4 style="color: #2d3748; margin-bottom: 1rem;">📊 Evaluation Results</h4>
                                    
                                    <div style="margin-bottom: 1rem; padding: 1rem; background: rgba(255,255,255,0.7); border-radius: 10px;">
                                        <p style="margin-bottom: 0.5rem;"><strong>Your Answer:</strong></p>
                                        <p style="margin: 0; color: #4a5568;">{user_answer}</p>
                                    </div>
                                    
                                    <div style="margin-bottom: 1rem; padding: 1rem; background: rgba(255,255,255,0.7); border-radius: 10px;">
                                        <p style="margin-bottom: 0.5rem;"><strong>Expected Answer:</strong></p>
                                        <p style="margin: 0; color: #4a5568;">{question_data["correct_answer"]}</p>
                                    </div>
                                    
                                    <div style="padding: 1rem; background: rgba(255,255,255,0.7); border-radius: 10px;">
                                        <p style="margin-bottom: 0.5rem;"><strong>📚 Explanation & Reasoning:</strong></p>
                                        <p style="margin: 0; color: #4a5568;">{question_data["explanation"]}</p>
                                    </div>
                                </div>
                                ''', unsafe_allow_html=True)
                                
                            except Exception as e:
                                st.error(f"❌ Error evaluating answer: {str(e)}")
                    else:
                        st.warning("⚠️ Please provide an answer before submitting!")
            
            st.markdown("---")
        
        # Option to generate new questions
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Generate New Challenge", key="new_questions", use_container_width=True):
                st.session_state.challenge_questions = []
                st.rerun()

def display_conversation_history():
    """Display conversation history in sidebar with enhanced styling"""
    if st.session_state.conversation_history:
        st.markdown("### 💬 Recent Conversations")
        
        # Show last 3 conversations
        for i, conv in enumerate(st.session_state.conversation_history[-3:]):
            with st.expander(f"Q{len(st.session_state.conversation_history)-2+i}: {conv['question'][:25]}...", expanded=False):
                st.markdown(f'''
                <div style="background: #2d3748; padding: 0.8rem; border-radius: 8px; margin-bottom: 0.5rem; border: 1px solid #667eea;">
                    <p style="color: #e2e8f0; font-size: 0.85rem; margin: 0;">
                        <strong>Q:</strong> {conv['question'][:80]}...
                    </p>
                </div>
                <div style="background: #1a1d29; padding: 0.8rem; border-radius: 8px; border: 1px solid #667eea;">
                    <p style="color: #cbd5e0; font-size: 0.8rem; margin: 0;">
                        <strong>A:</strong> {conv['answer'][:100]}...
                    </p>
                </div>
                ''', unsafe_allow_html=True)

def main():
    """Main application function"""
    initialize_session_state()
    display_header()
    
    # Document upload section
    if not st.session_state.document_uploaded:
        handle_document_upload()
    else:
        # Display document summary
        display_document_summary()
        
        # Mode selection with enhanced UI
        st.markdown("---")
        st.markdown('<h2 class="sub-header">🎯 Choose Your Interaction Mode</h2>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown('''
            <div style="text-align: center; margin-bottom: 2rem;">
                <p style="color: #718096; font-size: 1.1rem;">
                    Select how you'd like to interact with your document
                </p>
            </div>
            ''', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💬 Ask Anything Mode", key="ask_mode", use_container_width=True):
                st.session_state.current_mode = "ask_anything"
            st.markdown('''
            <div class="metric-card" style="text-align: center; margin-top: 1rem;">
                <h4 style="color: #667eea;">💬 Ask Anything</h4>
                <p style="color: #718096; font-size: 0.9rem;">
                    Ask free-form questions and get intelligent answers with source references
                </p>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            if st.button("🎯 Challenge Me Mode", key="challenge_mode", use_container_width=True):
                st.session_state.current_mode = "challenge_me"
            st.markdown('''
            <div class="metric-card" style="text-align: center; margin-top: 1rem;">
                <h4 style="color: #f093fb;">🎯 Challenge Me</h4>
                <p style="color: #718096; font-size: 0.9rem;">
                    Take AI-generated comprehension tests with detailed feedback
                </p>
            </div>
            ''', unsafe_allow_html=True)
        
        # Display selected mode
        if st.session_state.current_mode == "ask_anything":
            handle_ask_anything_mode()
        elif st.session_state.current_mode == "challenge_me":
            handle_challenge_mode()
        
        # Enhanced sidebar
        with st.sidebar:
            st.markdown('''
            <div style="text-align: center; padding: 1rem; margin-bottom: 2rem; background: #2d3748; border-radius: 10px; border: 1px solid #667eea;">
                <h2 style="color: #e2e8f0; margin-bottom: 0.5rem;">📊 Dashboard</h2>
                <p style="color: #cbd5e0; margin: 0; font-size: 0.9rem;">
                    Document Analysis Control Panel
                </p>
            </div>
            ''', unsafe_allow_html=True)
            
            # Document info
            st.markdown("### 📋 Document Info")
            if st.session_state.document_id:
                st.markdown(f'''
                <div style="background: #2d3748; padding: 1rem; border-radius: 10px; margin-bottom: 1rem; border: 1px solid #667eea;">
                    <p style="color: #e2e8f0; margin-bottom: 0.5rem;"><strong>ID:</strong></p>
                    <p style="color: #cbd5e0; font-family: monospace; font-size: 0.8rem; margin: 0;">
                        {st.session_state.document_id[:16]}...
                    </p>
                </div>
                ''', unsafe_allow_html=True)
            
            # Quick actions
            st.markdown("### ⚡ Quick Actions")
            if st.button("🔄 Upload New Document", use_container_width=True):
                # Reset all session state
                for key in ['document_uploaded', 'document_id', 'document_summary', 
                           'challenge_questions', 'current_mode', 'conversation_history']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
            
            # Stats
            if st.session_state.conversation_history:
                st.markdown("### 📈 Session Stats")
                st.markdown(f'''
                <div style="background: #2d3748; padding: 1rem; border-radius: 10px; border: 1px solid #667eea;">
                    <p style="color: #e2e8f0; text-align: center; margin: 0;">
                        <strong>{len(st.session_state.conversation_history)}</strong><br>
                        <small style="color: #cbd5e0;">Questions Asked</small>
                    </p>
                </div>
                ''', unsafe_allow_html=True)
            
            # Conversation history
            display_conversation_history()
            
            # Footer
            st.markdown("---")

if __name__ == "__main__":
    # Check if backend is running
    try:
        response = requests.get("http://localhost:8000/health/")
        if response.status_code != 200:
            st.error("❌ Backend server is not running. Please start the FastAPI server first.")
            st.code("cd src && python backend/api.py")
            st.stop()
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend server. Please start the FastAPI server first.")
        st.code("cd src && python backend/api.py")
        st.stop()
    
    main()
