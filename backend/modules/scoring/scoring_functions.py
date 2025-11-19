# scoring_server.py
from fastapi import FastAPI
from final_scorer import score_candidates

app = FastAPI()

@app.post("/score")
async def score_route(payload: dict):
    try:
        resumes = payload["resumes"]
        job_description = payload["job_description"]

        result = score_candidates(resumes, job_description)

        return {
            "message": "Scoring completed",
            "selected": result["selected_count"],
            "files": {
                "selected": result["selected_file"],
                "all": result["all_file"]
            }
        }

    except Exception as e:
        return {"error": str(e)}
