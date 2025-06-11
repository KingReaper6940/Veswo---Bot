from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional, List, Tuple
import uvicorn
import os
import json
from dotenv import load_dotenv

from utils.screen_recognizer import ScreenRecognizer
from utils.problem_solver import ProblemSolver, Problem
from utils.essay_writer import EssayWriter

# Load environment variables
load_dotenv()

# Get configuration from environment
PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "0.0.0.0")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
CORS_ORIGINS = json.loads(os.getenv("CORS_ORIGINS", '["http://localhost:3000", "http://localhost:8000"]'))

# Initialize FastAPI app
app = FastAPI(
    title="Local AI Assistant API",
    description="API for local AI assistant with screen recognition, problem solving, and essay writing capabilities",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
screen_recognizer = ScreenRecognizer()
problem_solver = ProblemSolver()
essay_writer = EssayWriter()

# Request/Response Models
class ScreenAnalysisRequest(BaseModel):
    region: Optional[Tuple[int, int, int, int]] = None  # (left, top, width, height)

class ProblemRequest(BaseModel):
    problem_text: str

class EssayRequest(BaseModel):
    topic: str
    essay_type: str = "analytical"
    tone: str = "formal"
    length: str = "medium"

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint returning API information"""
    return {
        "name": "Local AI Assistant API",
        "version": "1.0.0",
        "status": "operational"
    }

@app.post("/api/screen/analyze")
async def analyze_screen(request: ScreenAnalysisRequest):
    """Analyze screen content"""
    try:
        analysis = screen_recognizer.analyze_screen_content(request.region)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/screen/find-text")
async def find_text(request: ScreenAnalysisRequest, search_text: str):
    """Find specific text on screen"""
    try:
        matches = screen_recognizer.find_text_on_screen(search_text, request.region)
        return {"matches": matches}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/screen/detect-equations")
async def detect_equations(request: ScreenAnalysisRequest):
    """Detect mathematical equations on screen"""
    try:
        equations = screen_recognizer.detect_math_equations(request.region)
        return {"equations": equations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/solve/problem")
async def solve_problem(request: ProblemRequest):
    """Solve a math or physics problem"""
    try:
        # Parse the problem
        problem = problem_solver.parse_problem(request.problem_text)
        
        # Solve the problem
        solution = problem_solver.solve_problem(problem)
        
        return {
            "problem_type": problem.type.value,
            "solution": solution
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/write/essay")
async def write_essay(request: EssayRequest):
    """Generate an essay"""
    try:
        essay = essay_writer.generate_essay(
            topic=request.topic,
            essay_type=request.essay_type,
            tone=request.tone,
            length=request.length
        )
        return essay
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=DEBUG  # Enable auto-reload during development
    ) 