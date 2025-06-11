# Local AI Assistant

A powerful local AI assistant that helps with screen content recognition, math and physics problem solving, and essay writing.

## Features

- **Screen Content Recognition**
  - Capture and analyze screen content
  - Extract text using OCR
  - Find specific text on screen
  - Detect mathematical equations

- **Math and Physics Problem Solver**
  - Solve mathematical equations
  - Handle physics problems
  - Support for various problem types
  - Step-by-step solutions

- **Essay Writer**
  - Generate essays on any topic
  - Multiple essay types (analytical, persuasive, descriptive, narrative)
  - Adjustable tone (formal, casual, academic)
  - Customizable length

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/local-ai-assistant.git
cd local-ai-assistant
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Tesseract OCR:
- **macOS**: `brew install tesseract`
- **Linux**: `sudo apt-get install tesseract-ocr`
- **Windows**: Download and install from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

## Usage

1. Start the backend server:
```bash
cd backend
python main.py
```

2. The API will be available at `http://localhost:8000`

3. API Documentation is available at `http://localhost:8000/docs`

## API Endpoints

### Screen Analysis
- `POST /api/screen/analyze` - Analyze screen content
- `POST /api/screen/find-text` - Find specific text on screen
- `POST /api/screen/detect-equations` - Detect mathematical equations

### Problem Solving
- `POST /api/solve/problem` - Solve math or physics problems

### Essay Writing
- `POST /api/write/essay` - Generate essays

## Development

### Project Structure
```
local-ai-assistant/
├── backend/
│   ├── main.py
│   └── utils/
│       ├── screen_recognizer.py
│       ├── problem_solver.py
│       └── essay_writer.py
├── requirements.txt
└── README.md
```

### Adding New Features
1. Create new utility class in `backend/utils/`
2. Add new endpoints in `backend/main.py`
3. Update requirements.txt if needed
4. Test thoroughly

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [SymPy](https://www.sympy.org/)
- [OpenCV](https://opencv.org/) 