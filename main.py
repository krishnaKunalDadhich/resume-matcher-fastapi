from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from jd_matcher import calculate_match_score
import fitz  # PyMuPDF
import os
from mangum import Mangum  # For AWS Lambda
from pydantic import BaseModel
from tempfile import NamedTemporaryFile  # For handling PDFs in Lambda

app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lambda-friendly temp directory
TMP_DIR = "/tmp/resumes"
os.makedirs(TMP_DIR, exist_ok=True)

class MatchRequest(BaseModel):
    resume_text: str
    jd_text: str

@app.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):
    with NamedTemporaryFile(dir=TMP_DIR, suffix=".pdf") as temp_file:
        temp_file.write(await file.read())
        text = ""
        with fitz.open(temp_file.name) as doc:
            for page in doc:
                text += page.get_text()
    return {"resume_text": text.strip()}

@app.post("/match-resume/")
async def match_resume(data: MatchRequest):
    result = calculate_match_score(data.resume_text, data.jd_text)
    return result

# For AWS Lambda deployment (optional for Render)
handler = Mangum(app)

# For Render deployment
if __name__ == "__main__":
    import uvicorn
    PORT = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=PORT)
