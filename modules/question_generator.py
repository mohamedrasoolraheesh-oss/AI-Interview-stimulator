import pandas as pd
import random
from typing import List


class QuestionGenerator:
    def __init__(self, questions_path: str = "data/questions.csv"):
        self.questions_path = questions_path
        self.questions_df = self.load_questions()

    def load_questions(self) -> pd.DataFrame:
        """Load questions CSV into a DataFrame and normalize column names.

        Expected source columns: `question_id`, `category` (treated as skill),
        `difficulty`, `question_text`.
        """
        try:
            df = pd.read_csv(self.questions_path)
        except FileNotFoundError:
            return pd.DataFrame(columns=["question_id", "category", "difficulty", "question_text"])

        # Ensure expected columns exist
        expected = ["question_id", "category", "difficulty", "question_text"]
        for col in expected:
            if col not in df.columns:
                df[col] = ""

        return df

    def generate_questions(self, skills: List[str] = None, per_skill: int = 2, difficulty: str = None) -> List[str]:
        """Generate questions for the given skills.

        - `skills`: list of skill names (matches `category` column case-insensitively)
        - `per_skill`: max number of questions to select per skill
        - `difficulty`: optional difficulty filter (e.g., 'Easy', 'Medium', 'Hard')
        """
        if self.questions_df.empty:
            return []

        selected_questions = []

        if not skills:
            # fallback: return a small random sample of questions
            sample_df = self.questions_df
            if difficulty:
                sample_df = sample_df[sample_df["difficulty"].str.lower() == difficulty.lower()]
            return sample_df["question_text"].dropna().sample(min(5, len(sample_df))).tolist()

        for skill in skills:
            skill_mask = self.questions_df["category"].str.lower() == skill.lower()
            skill_df = self.questions_df[skill_mask]
            if difficulty:
                skill_df = skill_df[skill_df["difficulty"].str.lower() == difficulty.lower()]

            questions = skill_df["question_text"].dropna().tolist()
            if questions:
                k = min(per_skill, len(questions))
                selected_questions.extend(random.sample(questions, k))

        return selected_questions

    def get_followup_question(self, previous_answer: str) -> str:
        """Simple follow-up generator (placeholder)."""
        return "Can you elaborate more on that?"
