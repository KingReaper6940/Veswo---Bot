from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional, List, Tuple
import uvicorn
import os
import json
import time
from dotenv import load_dotenv

from utils.ai_model import GPT2Assistant

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
    description="AI-powered study assistant with GPT-2 for math solving, essay writing, and image analysis",
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

# Global variable to track GPT-2 initialization status
gpt2_ready = False
ai_assistant = None
initialization_error = None

def initialize_gpt2():
    """Initialize GPT-2 model with proper error handling"""
    global gpt2_ready, ai_assistant, initialization_error
    
    try:
        print("🔄 Initializing GPT-2 model...")
        print("📥 Downloading model files (this may take a few minutes on first run)...")
        
        # Initialize GPT-2 Assistant
        ai_assistant = GPT2Assistant()
        
        # Test the model with a simple query
        print("🧪 Testing GPT-2 model...")
        test_response = ai_assistant.general_chat("test")
        if test_response and "error" not in test_response.lower():
            gpt2_ready = True
            print("✅ GPT-2 model initialized successfully!")
            print(f"🖥️  Running on: {ai_assistant.device}")
            print(f"🧠 Model: {ai_assistant.model_name}")
            return True
        else:
            initialization_error = "GPT-2 model test failed"
            print(f"❌ GPT-2 model test failed: {test_response}")
            return False
            
    except Exception as e:
        initialization_error = str(e)
        print(f"❌ Failed to initialize GPT-2 model: {e}")
        return False

# Initialize GPT-2 on startup
@app.on_event("startup")
async def startup_event():
    """Initialize GPT-2 when the server starts"""
    global gpt2_ready
    gpt2_ready = initialize_gpt2()

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
    gpt2_ready: bool
    error: Optional[str] = None
    model_info: Optional[Dict[str, Any]] = None

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint returning API information"""
    return {
        "name": "Veswo Assistant API",
        "version": "1.0.0",
        "status": "operational" if gpt2_ready else "initializing",
        "description": "AI-powered study assistant with GPT-2 for math solving, essay writing, and image analysis",
        "model": "GPT-2",
        "gpt2_ready": gpt2_ready
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy" if gpt2_ready else "initializing",
        "timestamp": "2024-01-01T00:00:00Z",
        "version": "1.0.0",
        "model": "GPT-2",
        "gpt2_ready": gpt2_ready,
        "error": initialization_error if not gpt2_ready else None
    }

@app.get("/api/status")
async def get_status():
    """Get detailed status of the GPT-2 model"""
    if gpt2_ready and ai_assistant:
        model_info = {
            "model_name": ai_assistant.model_name,
            "device": str(ai_assistant.device),
            "status": "ready"
        }
    else:
        model_info = None
    
    return StatusResponse(
        status="ready" if gpt2_ready else "initializing",
        gpt2_ready=gpt2_ready,
        error=initialization_error if not gpt2_ready else None,
        model_info=model_info
    )

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """General chat endpoint using GPT-2"""
    if not gpt2_ready:
        raise HTTPException(
            status_code=503, 
            detail="GPT-2 model is still initializing. Please wait a moment and try again."
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
                
                # Use GPT-2 to solve the math problem
                result = ai_assistant.solve_math_problem(problem_text)
                
                return {
                    "response": result.get("solution", "Could not solve the problem"),
                    "steps": result.get("steps", []),
                    "method": result.get("method", "GPT-2 AI Model")
                }
            except Exception as e:
                return {
                    "response": f"I tried to solve your math problem but encountered an error: {str(e)}. Please try rephrasing your question.",
                    "steps": [],
                    "method": "GPT-2 AI Model"
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
                        "method": "GPT-2 AI Model"
                    }
            except Exception as e:
                return {
                    "response": f"I tried to write an essay but encountered an error: {str(e)}. Please try again.",
                    "steps": [],
                    "method": "GPT-2 AI Model"
                }
        
        # Check if it's a code help request
        elif any(keyword in message for keyword in ['code', 'program', 'debug', 'function', 'class']):
            try:
                response = ai_assistant.help_with_code("", request.message)
                return {
                    "response": response,
                    "method": "GPT-2 AI Model"
                }
            except Exception as e:
                return {
                    "response": f"I tried to help with code but encountered an error: {str(e)}. Please try again.",
                    "method": "GPT-2 AI Model"
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
                    "method": "GPT-2 AI Model"
                }
            except Exception as e:
                return {
                    "response": f"I tried to help with science but encountered an error: {str(e)}. Please try again.",
                    "method": "GPT-2 AI Model"
                }
        
        # Default response for general questions using GPT-2
        else:
            response = ai_assistant.general_chat(request.message)
            return {
                "response": response,
                "method": "GPT-2 AI Model"
            }
            
    except Exception as e:
        return {
            "response": f"Sorry, I encountered an error: {str(e)}. Please try again.",
            "method": "GPT-2 AI Model"
        }

@app.post("/api/write/essay")
async def write_essay(request: EssayRequest):
    """Generate an essay using GPT-2"""
    if not gpt2_ready:
        raise HTTPException(
            status_code=503, 
            detail="GPT-2 model is still initializing. Please wait a moment and try again."
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
    """Analyze image content using GPT-2"""
    if not gpt2_ready:
        raise HTTPException(
            status_code=503, 
            detail="GPT-2 model is still initializing. Please wait a moment and try again."
        )
    
    try:
        response = ai_assistant.analyze_image_content(
            request.image_description,
            request.question
        )
        return {
            "response": response,
            "method": "GPT-2 AI Model"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/help/code")
async def help_with_code(request: CodeHelpRequest):
    """Help with code using GPT-2"""
    if not gpt2_ready:
        raise HTTPException(
            status_code=503, 
            detail="GPT-2 model is still initializing. Please wait a moment and try again."
        )
    
    try:
        response = ai_assistant.help_with_code(
            request.code,
            request.question
        )
        return {
            "response": response,
            "method": "GPT-2 AI Model"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/help/science")
async def help_with_science(request: ScienceHelpRequest):
    """Help with science using GPT-2"""
    if not gpt2_ready:
        raise HTTPException(
            status_code=503, 
            detail="GPT-2 model is still initializing. Please wait a moment and try again."
        )
    
    try:
        response = ai_assistant.science_help(
            request.subject,
            request.question
        )
        return {
            "response": response,
            "method": "GPT-2 AI Model"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT) 