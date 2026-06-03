from PyPDF2 import PdfReader


def extract_resume_text(pdf_file):
    """Extract text from a PDF resume file using PyPDF2."""
    text = ""
    reader = PdfReader(pdf_file)

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    return text


class ResumeParser:
    def __init__(self):
        pass

    def parse(self, file):
        """Parse resume file and extract information

        If a PDF file-like object is provided, `extract_resume_text` will be used
        to obtain the raw text. This method currently returns a placeholder
        structured result and should be expanded with real parsing logic.
        """
        try:
            # attempt to extract text if file looks like a PDF or file-like
            resume_text = extract_resume_text(file)
        except Exception:
            resume_text = None

        # TODO: Implement resume parsing logic using `resume_text`
        return {
            "name": "Candidate Name",
            "email": "candidate@example.com",
            "phone": "+1234567890",
            "experience": "5+ years",
            "skills": ["Python", "Machine Learning", "Data Science"],
            "education": "Bachelor's in Computer Science",
            "raw_text": resume_text,
        }

    def extract_skills(self, resume_text):
        """Extract skills from resume text using `data/skills.txt`.

        Reads the skills list from `data/skills.txt` (one per line) and
        performs case-insensitive matching against the resume text.
        """
        if not resume_text:
            return []

        extracted_skills = []

        skills_path = "data/skills.txt"
        try:
            with open(skills_path, "r", encoding="utf-8") as file:
                skills = [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            return []

        lower_text = resume_text.lower()
        for skill in skills:
            if skill.lower() in lower_text:
                extracted_skills.append(skill)

        return extracted_skills
