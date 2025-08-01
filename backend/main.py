from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import google.generativeai as genai
import os

# Replace this with your real key or use environment variable for security
GOOGLE_API_KEY = "AIzaSyBM68gk1KUgnq2eoZFEfc5YKg-bBRzrKLw"

genai.configure(api_key=GOOGLE_API_KEY)

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request and response models
class GoalInput(BaseModel):
    goal: str

class GoalResponse(BaseModel):
    checklist: List[str]

def generate_checklist_from_goal(goal: str) -> List[str]:
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
Convert the following goal into a checklist of actionable tasks. 
Goal: "{goal}"

Return each item as a separate bullet point.
"""
    response = model.generate_content(prompt)
    text = response.text

    # Parse checklist items from bullet points
    lines = text.strip().splitlines()
    checklist = [line.lstrip("-• ").strip() for line in lines if line.strip()]
    return checklist

@app.post("/generate", response_model=GoalResponse)
async def generate_checklist(data: GoalInput):
    try:
        checklist = generate_checklist_from_goal(data.goal)
        return {"checklist": checklist}
    except Exception as e:
        return {"checklist": [f"Error: {str(e)}"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
