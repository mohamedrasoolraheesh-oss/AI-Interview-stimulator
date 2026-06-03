import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class Evaluator:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2', reference_file: str = "data/qa_reference.csv"):
        """Initialize evaluator with semantic similarity model and reference answers.
        
        Args:
            model_name: HuggingFace model ID for sentence embeddings
            reference_file: Path to CSV with reference answers (columns: question, answer)
        """
        self.model = SentenceTransformer(model_name)
        self.reference_df = None
        try:
            self.reference_df = pd.read_csv(reference_file)
        except FileNotFoundError:
            pass

    def evaluate_answer(self, question: str, user_answer: str) -> dict:
        """Evaluate candidate's answer using semantic similarity.
        
        Returns:
            dict with relevance_score, clarity_score, overall_score (0-100), and feedback.
        """
        if self.reference_df is None or self.reference_df.empty:
            return {
                "relevance_score": 0.0,
                "clarity_score": 0.0,
                "overall_score": 0.0,
                "feedback": "No reference answers available for evaluation."
            }

        # Find reference answer for the question
        ref_row = self.reference_df[self.reference_df["question"].str.lower() == question.lower()]
        if ref_row.empty:
            return {
                "relevance_score": 0.0,
                "clarity_score": 0.0,
                "overall_score": 0.0,
                "feedback": "No reference answer found for this question."
            }

        reference_answer = ref_row.iloc[0]["answer"]

        # Generate embeddings and calculate similarity
        try:
            embeddings = self.model.encode([user_answer, reference_answer])
            similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
            relevance_score = round(similarity * 100, 2)
        except Exception:
            relevance_score = 0.0

        # Estimate clarity based on answer length and structure
        clarity_score = min(100, 50 + (len(user_answer) / 10))
        clarity_score = round(clarity_score, 2)

        # Overall score is weighted average
        overall_score = round((relevance_score * 0.7 + clarity_score * 0.3), 2)

        # Generate feedback based on score
        if overall_score > 80:
            feedback = "Excellent answer. Shows strong understanding."
        elif overall_score > 60:
            feedback = "Good answer but could improve with more detail or precision."
        elif overall_score > 40:
            feedback = "Average answer. Consider addressing key concepts more directly."
        else:
            feedback = "Needs improvement. Try to align closer with core concepts of the question."

        return {
            "relevance_score": relevance_score,
            "clarity_score": clarity_score,
            "overall_score": overall_score,
            "feedback": feedback
        }
    
    def calculate_overall_score(self, evaluations: list) -> float:
        """Calculate average overall score from multiple evaluations."""
        if not evaluations:
            return 0.0
        scores = [e.get("overall_score", 0.0) for e in evaluations]
        return round(sum(scores) / len(scores), 2)
    
    def generate_feedback(self, evaluation_results: dict) -> str:
        """Generate detailed feedback summary from evaluation results."""
        overall = evaluation_results.get("overall_score", 0.0)
        base_feedback = evaluation_results.get("feedback", "No feedback available.")
        
        if overall > 80:
            summary = "Great interview performance! You demonstrated strong knowledge."
        elif overall > 60:
            summary = "Good performance overall. Focus on improving clarity and depth in your answers."
        else:
            summary = "You have potential. Review core concepts and practice articulating your knowledge more clearly."
        
        return f"{summary}\n\nDetails: {base_feedback}"
