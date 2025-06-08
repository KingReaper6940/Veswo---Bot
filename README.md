# Veswo - AI Study Assistant

A local AI assistant for students that helps with homework, essay writing, and problem-solving. The assistant can be triggered with a keyboard shortcut and can read screen content to provide contextual help.

## Features

- 🔍 Screen content recognition (OCR)
- 📝 Essay writing and editing assistance
- 🧮 Math and physics problem solving
- 🖼️ Image recognition and analysis
- 🔒 Privacy-focused (all processing done locally)
- ⌨️ Quick access via keyboard shortcut (Ctrl+Shift+A)

## Prerequisites

- Python 3.8+
- Node.js 16+
- Rust (for Tauri)
- Tesseract OCR
- Git

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Veswo---Bot.git
cd Veswo---Bot
```

2. Install Python dependencies:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Install frontend dependencies:
```bash
cd ../frontend
npm install
```

4. Install Tesseract OCR:
- macOS: `brew install tesseract`
- Ubuntu: `sudo apt-get install tesseract-ocr`
- Windows: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

## Development

1. Start the development server:
```bash
# From the project root
./run.sh
```

This will start both the Python backend and Tauri frontend.

2. Build for production:
```bash
cd frontend
npm run tauri build
```

## Project Structure

```
/frontend         → Tauri + React frontend
  /src           → React components
  /src-tauri     → Tauri backend
/backend         → Python FastAPI server
  /utils         → Utility modules
/models          → AI models
```

## Features in Detail

### Screen Reading
- Uses Tesseract OCR for text recognition
- Supports image capture and analysis
- Can process mathematical equations

### Math Solving
- Symbolic math with SymPy
- Step-by-step solutions
- Support for equations and expressions

### Essay Writing
- Multiple essay types (persuasive, analytical, etc.)
- Different writing tones
- Outline generation

### Privacy
- All processing done locally
- No data sent to external servers
- Optional encrypted storage

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Tesseract OCR
- SymPy
- Tauri
- React
- FastAPI 