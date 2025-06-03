# Veswo - AI Study Assistant

A local AI assistant for students that helps with homework, essay writing, and problem-solving. The assistant can be triggered with a keyboard shortcut and can read screen content to provide contextual help.

## Features

- 🔍 Screen content recognition (OCR)
- 📝 Essay writing and editing assistance
- 🧮 Math and physics problem solving
- 🖼️ Image recognition and analysis
- 🔒 Privacy-focused (all processing done locally)
- ⌨️ Quick access via keyboard shortcut

## Project Structure

```
/frontend         → Chat UI (Tauri)
/backend          → LLM, OCR, Math Solver
/models           → LLMs (GGML format), OCR data
/utils            → Task routing, file handling
```

## Setup

### Prerequisites

- Python 3.8+
- Node.js 16+
- Rust (for Tauri)
- Tesseract OCR

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Veswo---Bot.git
cd Veswo---Bot
```

2. Set up Python environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Install frontend dependencies:
```bash
cd frontend
npm install
```

4. Build and run:
```bash
npm run tauri dev
```

## Development

This project is built with:
- Frontend: Tauri (Rust + Web)
- Backend: Python
- AI: llama.cpp, Tesseract OCR
- Math: SymPy

## License

MIT License 