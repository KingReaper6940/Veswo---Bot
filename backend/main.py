from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional, List, Tuple
import uvicorn
import os
import json
import time
from dotenv import load_dotenv

from utils.ai_model import Llama3Assistant

# Load environment variables
load_dotenv()

# Get configuration from environment
PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "0.0.0.0")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
CORS_ORIGINS = json.loads(os.getenv("CORS_ORIGINS", '["http://localhost:3000", "http://localhost:8000", "http://localhost:1420", "tauri://localhost"]'))

# Initialize FastAPI app
app = FastAPI(
    title="Veswo Assistant API",
    description="AI-powered study assistant with Llama 3 7B for math solving, essay writing, and image analysis",
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

# Global variable to track Llama 3 initialization status
llama_ready = False
ai_assistant = None
initialization_error = None

def initialize_llama():
    """Initialize Llama 3 model with proper error handling"""
    global llama_ready, ai_assistant, initialization_error
    try:
        print("🔄 Initializing Llama 3 7B model...")
        print("📥 Downloading model files (this may take a few minutes on first run)...")
        ai_assistant = Llama3Assistant()
        print("🧪 Testing Llama 3 model...")
        test_response = ai_assistant.general_chat("test")
        if test_response and "error" not in test_response.lower():
            llama_ready = True
            print("✅ Llama 3 7B model initialized successfully!")
            return True
        else:
            initialization_error = "Llama 3 model test failed"
            print(f"❌ Llama 3 model test failed: {test_response}")
            return False
    except Exception as e:
        initialization_error = str(e)
        print(f"❌ Failed to initialize Llama 3 model: {e}")
        return False

# Initialize Llama 3 on startup
@app.on_event("startup")
async def startup_event():
    global llama_ready
    llama_ready = initialize_llama()

# Request/Response Models
class ChatRequest(BaseModel):
    message: str

class EssayRequest(BaseModel):
    topic: str
    essay_type: str = "analytical"
    tone: str = "formal"
    length: str = "medium"

class ImageAnalysisRequest(BaseModel):
    image_description: str
    question: str

class CodeHelpRequest(BaseModel):
    code: str
    question: str

class ScienceHelpRequest(BaseModel):
    subject: str
    question: str

class StatusResponse(BaseModel):
    status: str
    llama_ready: bool
    error: Optional[str] = None
    model_info: Optional[Dict[str, Any]] = None

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint returning API information"""
    return {
        "name": "Veswo Assistant API",
        "version": "1.0.0",
        "status": "operational" if llama_ready else "initializing",
        "description": "AI-powered study assistant with Llama 3 7B for math solving, essay writing, and image analysis",
        "model": "Llama 3 7B",
        "llama_ready": llama_ready
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy" if llama_ready else "initializing",
        "timestamp": "2024-01-01T00:00:00Z",
        "version": "1.0.0",
        "model": "Llama 3 7B",
        "llama_ready": llama_ready,
        "error": initialization_error if not llama_ready else None
    }

@app.get("/api/status")
async def get_status():
    """Get detailed status of the Llama 3 model"""
    if llama_ready and ai_assistant:
        model_info = {
            "model_name": getattr(ai_assistant, "model_name", "Llama 3 7B"),
            "status": "ready"
        }
    else:
        model_info = None
    
    return StatusResponse(
        status="ready" if llama_ready else "initializing",
        llama_ready=llama_ready,
        error=initialization_error if not llama_ready else None,
        model_info=model_info
    )

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """General chat endpoint using Llama 3"""
    if not llama_ready or ai_assistant is None:
        raise HTTPException(
            status_code=503,
            detail="Llama 3 model is still initializing. Please wait a moment and try again."
        )
    
    try:
        message = request.message.lower().strip()
        
        # Check for fallback responses first
        fallback = ai_assistant.get_fallback_response(request.message)
        if fallback:
            return {
                "response": fallback,
                "method": "Fallback Response"
            }
        
        # Check if it's a math problem
        if any(keyword in message for keyword in ['solve', 'calculate', 'find', 'equation', 'math', '=', '+', '-', '*', '/', '^']):
            try:
                # Extract the actual problem from the message
                problem_text = request.message
                if 'solve:' in problem_text.lower():
                    problem_text = problem_text.split('solve:', 1)[1].strip()
                elif 'solve' in problem_text.lower():
                    problem_text = problem_text.split('solve', 1)[1].strip()
                
                # Use Llama 3 to solve the math problem
                result = ai_assistant.solve_math_problem(problem_text)
                
                return {
                    "response": result.get("solution", "Could not solve the problem"),
                    "steps": result.get("steps", []),
                    "method": result.get("method", "Llama 3 7B AI Model")
                }
            except Exception as e:
                return {
                    "response": f"I tried to solve your math problem but encountered an error: {str(e)}. Please try rephrasing your question.",
                    "steps": [],
                    "method": "Llama 3 7B AI Model"
                }
        
        # Check if it's an essay request
        elif any(keyword in message for keyword in ['write', 'essay', 'article', 'paper']):
            try:
                # Extract topic from message
                topic = request.message.replace('write', '').replace('essay', '').replace('about', '').strip()
                if topic:
                    essay = ai_assistant.write_essay(topic=topic, length="medium")
                    return {
                        "response": essay.get("content", "Could not generate essay"),
                        "metadata": essay.get("metadata", {}),
                        "method": "Llama 3 7B AI Model"
                    }
            except Exception as e:
                return {
                    "response": f"I tried to write an essay but encountered an error: {str(e)}. Please try again.",
                    "steps": [],
                    "method": "Llama 3 7B AI Model"
                }
        
        # Check if it's a code help request
        elif any(keyword in message for keyword in ['code', 'program', 'debug', 'function', 'class']):
            try:
                response = ai_assistant.help_with_code("", request.message)
                return {
                    "response": response,
                    "method": "Llama 3 7B AI Model"
                }
            except Exception as e:
                return {
                    "response": f"I tried to help with code but encountered an error: {str(e)}. Please try again.",
                    "method": "Llama 3 7B AI Model"
                }
        
        # Check if it's a science help request
        elif any(keyword in message for keyword in ['physics', 'chemistry', 'biology', 'science', 'experiment']):
            try:
                # Determine subject from message
                subject = "science"
                if 'physics' in message:
                    subject = "physics"
                elif 'chemistry' in message:
                    subject = "chemistry"
                elif 'biology' in message:
                    subject = "biology"
                
                response = ai_assistant.science_help(subject, request.message)
                return {
                    "response": response,
                    "method": "Llama 3 7B AI Model"
                }
            except Exception as e:
                return {
                    "response": f"I tried to help with science but encountered an error: {str(e)}. Please try again.",
                    "method": "Llama 3 7B AI Model"
                }
        
        # Default response for general questions using Llama 3
        else:
            response = ai_assistant.general_chat(request.message)
            return {
                "response": response,
                "method": "Llama 3 7B AI Model"
            }
            
    except Exception as e:
        return {
            "response": f"Sorry, I encountered an error: {str(e)}. Please try again.",
            "method": "Llama 3 7B AI Model"
        }

@app.post("/api/write/essay")
async def write_essay(request: EssayRequest):
    """Generate an essay using Llama 3"""
    if not llama_ready or ai_assistant is None:
        raise HTTPException(
            status_code=503,
            detail="Llama 3 model is still initializing. Please wait a moment and try again."
        )
    
    try:
        essay = ai_assistant.write_essay(
            topic=request.topic,
            essay_type=request.essay_type,
            length=request.length
        )
        return essay
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze/image")
async def analyze_image(request: ImageAnalysisRequest):
    """Analyze image content using Llama 3"""
    if not llama_ready or ai_assistant is None:
        raise HTTPException(
            status_code=503,
            detail="Llama 3 model is still initializing. Please wait a moment and try again."
        )
    
    try:
        response = ai_assistant.analyze_image_content(
            request.image_description,
            request.question
        )
        return {
            "response": response,
            "method": "Llama 3 7B AI Model"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/help/code")
async def help_with_code(request: CodeHelpRequest):
    """Help with code using Llama 3"""
    if not llama_ready or ai_assistant is None:
        raise HTTPException(
            status_code=503,
            detail="Llama 3 model is still initializing. Please wait a moment and try again."
        )
    
    try:
        response = ai_assistant.help_with_code(
            request.code,
            request.question
        )
        return {
            "response": response,
            "method": "Llama 3 7B AI Model"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/help/science")
async def help_with_science(request: ScienceHelpRequest):
    """Help with science using Llama 3"""
    if not llama_ready or ai_assistant is None:
        raise HTTPException(
            status_code=503,
            detail="Llama 3 model is still initializing. Please wait a moment and try again."
        )
    
    try:
        response = ai_assistant.science_help(
            request.subject,
            request.question
        )
        return {
            "response": response,
            "method": "Llama 3 7B AI Model"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT) 