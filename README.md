# AI Interview Simulator

An AI-powered interview simulator application that helps candidates practice and improve their interview skills with AI-generated questions, real-time feedback, and comprehensive performance analysis.

## Features

- **Resume Parser**: Extract key information from resumes
- **Question Generator**: Generate interview questions based on skills and difficulty
- **Speech-to-Text**: Convert audio responses to text transcripts
- **Emotion Detector**: Analyze candidate emotions and sentiment
- **Evaluator**: Score and evaluate candidate responses
- **Report Generator**: Create comprehensive interview reports

## Project Structure

```
AI-Interview-Simulator/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── modules/
│   ├── resume_parser.py      # Resume parsing module
│   ├── question_generator.py # Interview question generation
│   ├── speech_to_text.py     # Audio-to-text conversion
│   ├── emotion_detector.py   # Emotion and sentiment analysis
│   ├── evaluator.py          # Answer evaluation
│   └── report_generator.py   # Report generation
├── uploads/                  # User uploaded files
├── database/                 # Interview data storage
├── models/                   # ML models
├── utils/                    # Utility functions
├── assets/                   # Static assets
└── data/
    └── questions.csv         # Interview questions database
```

## Installation

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
streamlit run app.py
```

## Usage

1. Upload your resume
2. Select interview difficulty level
3. Answer interview questions
4. Get real-time feedback and performance analysis
5. Download your interview report

## Technologies Used

- Streamlit: Frontend framework
- OpenCV: Video processing
- Librosa: Audio processing
- Scikit-learn: ML algorithms
- ReportLab: PDF generation

## License

MIT License
