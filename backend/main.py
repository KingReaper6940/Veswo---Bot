from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from utils.ai_model import GemmaAssistant
from utils.essay_writer import EssayWriter
from utils.problem_solver import ProblemSolver
from utils.screen_recognizer import ScreenRecognizer

app = FastAPI(
    title="veswo1-bot API",
    description="AI-powered study assistant with Gemma AI (via Ollama) for chat, math, essay, and code help",
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
essay_writer = EssayWriter()
problem_solver = ProblemSolver()
screen_recognizer = ScreenRecognizer()

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
    prompt = data.get("prompt", "") or data.get("message", "")
    response = gemma.chat(prompt)
    return {"response": response, "method": "gemma"}

@app.post("/api/write/essay")
async def write_essay(request: Request):
    data = await request.json()
    topic = data.get("topic", "")
    essay_type = data.get("essay_type", "analytical")
    length = data.get("length", "medium")
    
    # Use the essay writer utility
    essay_result = essay_writer.generate_essay(topic, essay_type, "formal", length)
    return {"response": essay_result["content"], "method": "essay_writer"}

@app.post("/api/solve/problem")
async def solve_problem(request: Request):
    data = await request.json()
    problem_text = data.get("problem", "")
    
    # Use the problem solver utility
    problem = problem_solver.parse_problem(problem_text)
    solution = problem_solver.solve_problem(problem)
    
    # Format the solution for display
    formatted_solution = "Problem: " + problem_text + "\n\n"
    if solution.get('solution'):
        formatted_solution += "Solution:\n"
        for var, value in solution['solution'].items():
            formatted_solution += f"{var} = {value}\n"
    
    if solution.get('steps'):
        formatted_solution += "\nSteps:\n"
        for i, step in enumerate(solution['steps'], 1):
            formatted_solution += f"{i}. {step}\n"
    
    return {"response": formatted_solution, "method": "problem_solver"}

@app.post("/api/analyze/image")
async def analyze_image(request: Request):
    data = await request.json()
    image_data = data.get("image_data", "")
    question = data.get("question", "What's in this image?")
    
    # Use the screen recognizer utility
    # For now, use a simple analysis since analyze_image doesn't exist
    analysis = f"Image analysis for question: {question}\n\nThis feature is currently being implemented. The image data has been received and will be processed using OCR and AI analysis."
    return {"response": analysis, "method": "screen_recognizer"}

@app.post("/api/help/code")
async def help_with_code(request: Request):
    data = await request.json()
    code_input = data.get("code", "")
    question = data.get("question", "")
    
    # Combine code and question for Gemma
    prompt = f"Code:\n{code_input}\n\nQuestion: {question}\n\nPlease help with this code."
    response = gemma.chat(prompt)
    return {"response": response, "method": "gemma"}

@app.post("/api/help/science")
async def help_with_science(request: Request):
    data = await request.json()
    subject = data.get("subject", "physics")
    question = data.get("question", "")
    
    prompt = f"Subject: {subject}\nQuestion: {question}\n\nPlease help with this {subject} question."
    response = gemma.chat(prompt)
    return {"response": response, "method": "gemma"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 