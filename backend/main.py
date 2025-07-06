from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from utils.ai_model import GemmaAssistant
import base64
from io import BytesIO
from PIL import Image
import pytesseract

app = FastAPI(
    title="veswo-bot API",
    description="AI-powered study assistant with Gemma AI (via Ollama) for chat, math, essay, code, and OCR",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gemma = GemmaAssistant()

@app.get("/api/status")
def status():
    try:
        # Test if Gemma is working
        test_response = gemma.chat("Hello")
        return {
            "status": "ready",
            "gemma_ready": True,
            "message": "Backend is ready and Gemma AI is working"
        }
    except Exception as e:
        return {
            "status": "error",
            "gemma_ready": False,
            "error": str(e)
        }

@app.post("/api/chat")
async def chat(request: Request):
    data = await request.json()
    prompt = data.get("prompt") or data.get("message") or ""
    response = gemma.chat(prompt)
    return {"response": response, "method": "gemma"}

@app.post("/api/ocr")
async def ocr(request: Request):
    data = await request.json()
    image_data = data.get("image_data")
    if not image_data:
        return {"error": "No image data provided."}
    try:
        # Remove base64 header if present
        if "," in image_data:
            image_data = image_data.split(",", 1)[1]
        image_bytes = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_bytes))
        text = pytesseract.image_to_string(image)
        return {"text": text.strip()}
    except Exception as e:
        return {"error": f"OCR failed: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 