from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from jd_matcher import calculate_match_score
import fitz  # PyMuPDF
import os
from mangum import Mangum  # <-- Add this
from pydantic import BaseModel
from tempfile import NamedTemporaryFile  # For handling PDFs in Lambda

app = FastAPI()

# CORS (Keep this if your frontend needs it)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lambda-friendly temp directory (no persistent storage)
TMP_DIR = "/tmp/resumes"
os.makedirs(TMP_DIR, exist_ok=True)

class MatchRequest(BaseModel):
    resume_text: str
    jd_text: str

@app.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):
    # Save to temp file (Lambda has no persistent storage)
    with NamedTemporaryFile(dir=TMP_DIR, suffix=".pdf") as temp_file:
        temp_file.write(await file.read())
        
        # Extract text from PDF
        text = ""
        with fitz.open(temp_file.name) as doc:
            for page in doc:
                text += page.get_text()

    return {"resume_text": text.strip()}

@app.post("/match-resume/")
async def match_resume(data: MatchRequest):
    result = calculate_match_score(data.resume_text, data.jd_text)
    return result

# Mangum handler for Lambda
handler = Mangum(app)  # <-- This wraps FastAPI for AWS Lambda