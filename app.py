import streamlit as st
from modules.resume_parser import extract_resume_text
from modules.skill_extractor import SkillExtractor
from modules.question_generator import QuestionGenerator
from modules.speech_to_text import SpeechToText
from modules.emotion_detector import EmotionDetector, detect_emotion
from modules.evaluator import Evaluator
from modules.report_generator import ReportGenerator

st.set_page_config(page_title="AI Interview Simulator", layout="wide")

st.title("AI Interview Simulator")
st.write("Practice your interview skills with AI-powered feedback")

# Sidebar
with st.sidebar:
    st.header("Navigation")
    page = st.radio("Select a module:", [
        "Upload Resume",
        "Start Interview",
        "View Results",
        "Settings"
    ])

if page == "Upload Resume":
    st.header("Upload Your Resume")
    uploaded_file = st.file_uploader("Choose a resume file", type=["pdf", "docx", "txt"])
    if uploaded_file:
        # Extract resume text (PDF)
        try:
            resume_text = extract_resume_text(uploaded_file)
        except Exception:
            resume_text = None

        if resume_text:
            st.subheader("Resume Extracted")
            st.write(resume_text[:1000])

            # Extract skills using the skills list
            skill_extractor = SkillExtractor(skills_file="data/skills.txt")
            skills = skill_extractor.extract(resume_text)
            st.subheader("Detected Skills")
            st.write(skills)

            # Generate questions from detected skills
            qgen = QuestionGenerator(questions_path="data/questions.csv")
            questions = qgen.generate_questions(skills)
            st.subheader("Generated Interview Questions")
            for i, question in enumerate(questions, start=1):
                st.write(f"{i}. {question}")

        st.success("Resume uploaded successfully!")

elif page == "Start Interview":
    st.header("Interview Session")
    
    # Initialize session state for storing answers and scores
    if "interview_started" not in st.session_state:
        st.session_state.interview_started = False
        st.session_state.questions = []
        st.session_state.answers = {}
        st.session_state.scores = {}
    
    # Get questions (from previous session or generate new)
    if not st.session_state.questions:
        qgen = QuestionGenerator(questions_path="data/questions.csv")
        st.session_state.questions = qgen.generate_questions()
    
    questions = st.session_state.questions[:5]  # Limit to 5 questions
    st.write(f"Answering {len(questions)} interview questions")
    st.write("---")
    
    # Display questions and collect answers
    for i, question in enumerate(questions, start=1):
        st.subheader(f"Question {i}")
        st.write(question)
        
        # Text Answer Input
        col1, col2 = st.columns([3, 1])
        with col1:
            user_answer = st.text_area(
                f"Your Answer",
                key=f"answer_{i}",
                height=100
            )
        
        # Voice Answer Button
        with col2:
            if st.button(f"🎤 Record", key=f"record_{i}"):
                st.info("Voice recording not yet implemented in this version. Please use text input.")
        
        # Emotion Detection Button
        if st.button(f"Detect Emotion {i}", key=f"detect_emotion_{i}"):
            st.info("Opening Camera...")
            emotion, confidence = detect_emotion()
            st.success(f"Emotion: {emotion}")
            st.write(f"Confidence Level: {confidence}%")
        
        # Store answer in session state
        if user_answer:
            st.session_state.answers[i] = user_answer
        
        # Evaluation Button
        if user_answer and st.button(f"Evaluate", key=f"evaluate_{i}"):
            evaluator = Evaluator(reference_file="data/qa_reference.csv")
            result = evaluator.evaluate_answer(question, user_answer)
            st.session_state.scores[i] = result
            
            # Display score and feedback
            col_score, col_clarity = st.columns(2)
            with col_score:
                st.metric("Relevance Score", f"{result['relevance_score']}%")
            with col_clarity:
                st.metric("Overall Score", f"{result['overall_score']}%")
            
            st.success(result["feedback"])
        
        st.write("---")
    
    # Summary after all questions answered
    if len(st.session_state.scores) == len(questions):
        st.subheader("Interview Summary")
        evaluator = Evaluator(reference_file="data/qa_reference.csv")
        avg_score = evaluator.calculate_overall_score(list(st.session_state.scores.values()))
        st.metric("Average Score", f"{avg_score}%")
        
        st.info(f"You answered {len(st.session_state.scores)} out of {len(questions)} questions.")


elif page == "View Results":
    st.header("Interview Results")
    st.info("No interview results yet. Start an interview to see results.")

elif page == "Settings":
    st.header("Settings")
    st.write("Configure interview preferences here")

if __name__ == "__main__":
    st.write("---")
    st.caption("AI Interview Simulator © 2026")
