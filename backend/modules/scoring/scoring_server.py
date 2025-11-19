# main.py
import json
import requests

# load mock data
resumes = json.load(open("resume.json"))
job_description = json.load(open("job_description.json"))

payload = {
    "resumes": resumes,
    "job_description": job_description
}

response = requests.post("http://localhost:8000/score", json=payload)

print("\n### RAW RESPONSE ###")
print(response.text)

try:
    print("\n### JSON RESPONSE ###")
    print(response.json())
except Exception:
    print("Server did not return valid JSON.")
