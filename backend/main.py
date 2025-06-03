from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn

app = FastAPI(title="Veswo AI Assistant")

# Enable CORS for Tauri frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    content: str
    type: str = "text"  # text, image, math
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response: str
    type: str = "text"
    metadata: Optional[Dict[str, Any]] = None

@app.get("/")
async def root():
    return {"status": "online", "service": "Veswo AI Assistant"}

@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    try:
        # TODO: Implement chat logic with appropriate routing
        # This will be expanded to handle different types of requests
        return ChatResponse(
            response="I'm here to help! What would you like assistance with?",
            type="text"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ocr")
async def process_ocr(image_data: bytes):
    try:
        # TODO: Implement OCR processing
        return {"text": "OCR processing will be implemented here"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True) 