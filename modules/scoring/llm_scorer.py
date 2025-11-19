# llm_scorer.py
import random
import google.generativeai as genai

class LLMScorer:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.model = None
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel("gemini-1.5-flash")

    def score_with_llm(self, resume, job_description):
        if not self.model:
            return None

        prompt = f"""
        Score the resume against the job description.
        Return JSON with:
        jd_match, hard_skills, soft_skills, keyword_match, cultural_fit (0-100)
        Resume: {resume}
        Job Description: {job_description}
        """

        try:
            response = self.model.generate_content(prompt)
            import json
            return json.loads(response.text)
        except Exception:
            return None

    def fallback_score(self, resume, job_description):
        resume_text = str(resume).lower()
        keywords = ["python", "django", "api", "ai", "ml", "docker"]

        hits = sum(1 for k in keywords if k in resume_text)

        return {
            "jd_match": min(100, 50 + hits * 5),
            "hard_skills": min(100, 45 + hits * 6),
            "soft_skills": 60 + random.randint(0, 20),
            "keyword_match": min(100, hits * 10),
            "cultural_fit": 60 + random.randint(0, 20),
        }

    def get_final_score(self, resume, job_description):
        scores = self.score_with_llm(resume, job_description)

        fallback = False
        if not scores:
            scores = self.fallback_score(resume, job_description)
            fallback = True

        final = (
            scores["jd_match"] * 0.30 +
            scores["hard_skills"] * 0.30 +
            scores["soft_skills"] * 0.20 +
            scores["keyword_match"] * 0.10 +
            scores["cultural_fit"] * 0.10
        )

        scores["final_score"] = round(final, 2)
        scores["fallback_used"] = fallback

        return scores
