# Veswo Assistant 🧠

An AI-powered study companion powered by GPT-2 that helps with math problems, essay writing, code analysis, and image recognition - **100% local and private**.

![Veswo Assistant](https://img.shields.io/badge/Version-1.0.0-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Cross--Platform-orange)
![AI Model](https://img.shields.io/badge/AI%20Model-GPT--2-purple)
![Privacy](https://img.shields.io/badge/Privacy-100%25%20Local-red)

## ✨ Features

### 🧮 **Math Problem Solver**
- Solve complex equations step-by-step using GPT-2
- Handle arithmetic expressions instantly
- Support for algebra, calculus, and more
- Handwritten math recognition via screenshots

### 📝 **Essay Writer**
- Generate well-structured essays on any topic using GPT-2
- Multiple essay types: analytical, persuasive, descriptive, narrative
- Customizable length and tone
- Professional writing assistance

### 📷 **Image Analysis**
- Screenshot and analyze any content
- OCR for text extraction from images
- Math problem recognition from screenshots
- Code analysis from screenshots
- General image content understanding

### 💻 **Code Helper**
- Code explanation and documentation using GPT-2
- Bug detection and debugging assistance
- Code generation for common tasks
- Programming language support

### 🔬 **Science Helper**
- Physics problem solving
- Chemistry explanations
- Biology concepts
- Scientific formula assistance

### 🔒 **Privacy & Security**
- **100% Local**: No data sent to external servers
- **Open Source**: GPT-2 model is completely transparent
- **Offline Capable**: Works without internet connection
- **No Data Collection**: Your conversations stay private

## 🚀 Quick Start

### Prerequisites
- **Node.js** (v16 or higher)
- **Rust** (for Tauri backend)
- **Python** (v3.8 or higher)
- **4GB+ RAM** (for GPT-2 model)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/veswo/veswo-assistant.git
   cd veswo-assistant
   ```

2. **Set up Python backend**
   ```bash
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies (this will download GPT-2 model ~500MB)
   pip install -r requirements.txt
   ```

3. **Set up frontend**
   ```bash
   cd frontend
   npm install
   ```

4. **Start the application**
   ```bash
   # Use the automated startup script
   ./start.sh
   
   # Or manually:
   # Terminal 1: Backend
   cd backend && source ../venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   
   # Terminal 2: Frontend
   cd frontend && npm run tauri dev
   ```

## 📦 Building for Distribution

### Development Build
```bash
cd frontend
npm run tauri:dev
```

### Production Build
```bash
cd frontend
npm run tauri:build
```

This will create platform-specific installers in `frontend/src-tauri/target/release/bundle/`.

## 🎯 Usage Examples

### Math Problems
- Type: `2+3` → Get instant answer using GPT-2
- Type: `Solve: 2x + 5 = 13` → Get step-by-step solution
- Screenshot a math problem → Get OCR + GPT-2 solution

### Essay Writing
1. Go to "Essay Writer" tab
2. Enter topic: "Climate Change"
3. Select type: "Analytical"
4. Choose length: "Medium"
5. Click "Write Essay" → GPT-2 generates content

### Image Analysis
1. Go to "Image Analysis" tab
2. Take screenshot or upload image
3. Ask: "What's in this image?"
4. Get GPT-2 analysis

### Code Help
1. Go to "Code Helper" tab
2. Use quick actions or type code questions
3. Get GPT-2 explanations, debugging help, or code generation

## 🏗️ Architecture

```
Veswo Assistant
├── Frontend (React + Tauri)
│   ├── Modern UI with Tailwind CSS
│   ├── Tabbed interface for different features
│   └── Real-time chat with AI
├── Backend (FastAPI + Python)
│   ├── GPT-2 AI Model (500MB local model)
│   ├── Math problem solver (GPT-2 powered)
│   ├── Essay writer (GPT-2 powered)
│   ├── Image analysis (GPT-2 powered)
│   └── Code analysis (GPT-2 powered)
└── AI Integration
    ├── GPT-2 Language Model
    ├── Local inference (no internet required)
    └── Privacy-focused processing
```

## 🛠️ Technology Stack

- **Frontend**: React, Tauri, Tailwind CSS
- **Backend**: FastAPI, Python
- **AI/ML**: GPT-2 (OpenAI), Transformers, PyTorch
- **Math**: GPT-2 mathematical reasoning
- **Image Processing**: PIL, OpenCV
- **Packaging**: Tauri bundler

## 📱 Platform Support

- ✅ **macOS** (10.13+)
- ✅ **Windows** (10+)
- ✅ **Linux** (Ubuntu 18.04+)

## 🔒 Privacy Features

- **No Internet Required**: GPT-2 runs completely locally
- **No Data Collection**: Your conversations never leave your device
- **Open Source Model**: GPT-2 is transparent and auditable
- **Offline Capable**: Works without any external services
- **No API Keys**: No need for OpenAI or other API keys

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for the GPT-2 model
- **Hugging Face** for the Transformers library
- **Tauri** for the cross-platform framework
- **FastAPI** for the high-performance backend
- **Tailwind CSS** for the beautiful UI

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/veswo/veswo-assistant/issues)
- **Discussions**: [GitHub Discussions](https://github.com/veswo/veswo-assistant/discussions)
- **Email**: support@veswo.ai

---

**Made with ❤️ by the Veswo Team - Powered by GPT-2** 