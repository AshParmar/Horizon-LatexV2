# final_scorer.py
import json
from llm_scorer import LLMScorer

THRESHOLD = 70

def score_candidates(resumes, job_description):
    scorer = LLMScorer()

    all_results = []
    selected = []

    for c in resumes:
        scores = scorer.get_final_score(c, job_description)

        status = (
            "selected" if scores["final_score"] >= THRESHOLD else
            "pending" if scores["final_score"] >= 60 else
            "rejected"
        )

        summary = (
            f"{c.get('name')} scored {scores['final_score']}%. "
            f"JD {scores['jd_match']}%, Hard {scores['hard_skills']}%, "
            f"Soft {scores['soft_skills']}%, Keyword {scores['keyword_match']}%, "
            f"Cultural {scores['cultural_fit']}%. Status: {status}."
        )

        result = {
            "candidate": c,
            "scores": scores,
            "status": status,
            "summary": summary
        }

        all_results.append(result)
        if status == "selected":
            selected.append(result)

    # Write JSON files
    with open("selected_candidates.json", "w") as f:
        json.dump(selected, f, indent=4)

    with open("all_candidates_with_status.json", "w") as f:
        json.dump(all_results, f, indent=4)

    return {
        "selected_count": len(selected),
        "selected_file": "selected_candidates.json",
        "all_file": "all_candidates_with_status.json"
    }
