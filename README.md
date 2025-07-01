# Veswo Assistant 🧠

An AI-powered study companion powered by **Meta Llama 3 7B** that helps with math problems, essay writing, code analysis, and image recognition - **100% local and private**.

![Veswo Assistant](https://img.shields.io/badge/Version-1.0.0-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Cross--Platform-orange)
![AI Model](https://img.shields.io/badge/AI%20Model-Llama%203%207B-purple)
![Privacy](https://img.shields.io/badge/Privacy-100%25%20Local-red)

## ✨ Features

### 🧮 **Math Problem Solver**
- Solve complex equations step-by-step using Llama 3
- Handle arithmetic expressions instantly
- Support for algebra, calculus, and more
- Handwritten math recognition via screenshots

### 📝 **Essay Writer**
- Generate well-structured essays on any topic using Llama 3
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
- Code explanation and documentation using Llama 3
- Bug detection and debugging assistance
- Code generation for common tasks
- Programming language support

### 🔬 **Science Helper**
- Physics problem solving
- Chemistry explanations
- Biology concepts
- Scientific formula assistance

### 🌙 **Dark Mode**
- Toggle dark/light mode with a single click for comfortable day or night use

### 🔒 **Privacy & Security**
- **100% Local**: No data sent to external servers
- **Open Source**: Llama 3 model is completely transparent
- **Offline Capable**: Works without internet connection
- **No Data Collection**: Your conversations stay private

## 🚀 Quick Start

### Option 1: One-Click Launch (Recommended)

1. **Build the application** (one-time setup):
   ```bash
   ./build.sh
   ```

2. **Launch the application**:
   - Double-click the `.app` file in `frontend/src-tauri/target/release/bundle/macos/`
   - The app will automatically start the backend and frontend, and load the Llama 3 model

### Option 2: Development Mode

1. **Start everything with one command**:
   ```bash
   ./start.sh
   ```

2. **Or start components individually**:
   ```bash
   # Terminal 1: Start backend
   cd backend && source ../venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   
   # Terminal 2: Start frontend
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
- Type: `2+3` → Get instant answer using Llama 3
- Type: `Solve: 2x + 5 = 13` → Get step-by-step solution
- Screenshot a math problem → Get OCR + Llama 3 solution

### Essay Writing
1. Go to "Essay Writer" tab
2. Enter topic: "Climate Change"
3. Select type: "Analytical"
4. Choose length: "Medium"
5. Click "Write Essay" → Llama 3 generates content

### Image Analysis
1. Go to "Image Analysis" tab
2. Take screenshot or upload image
3. Ask: "What's in this image?"
4. Get Llama 3 analysis

### Code Help
1. Go to "Code Helper" tab
2. Use quick actions or type code questions
3. Get Llama 3 explanations, debugging help, or code generation

### Dark Mode
- Click the moon/sun icon in the header to toggle dark/light mode instantly

## 🏗️ Architecture

```
Veswo Assistant
├── Frontend (React + Tauri)
│   ├── Modern UI with Tailwind CSS
│   ├── Tabbed interface for different features
│   ├── Real-time chat with AI
│   └── Dark mode toggle
├── Backend (FastAPI + Python)
│   ├── Llama 3 7B AI Model (local model)
│   ├── Math problem solver (Llama 3 powered)
│   ├── Essay writer (Llama 3 powered)
│   ├── Image analysis (Llama 3 powered)
│   └── Code analysis (Llama 3 powered)
└── AI Integration
    ├── Llama 3 Language Model
    ├── Local inference (no internet required)
    └── Privacy-focused processing
```

## 🛠️ Technology Stack

- **Frontend**: React, Tauri, Tailwind CSS
- **Backend**: FastAPI, Python
- **AI/ML**: Meta Llama 3 7B, Transformers, PyTorch
- **Math**: Llama 3 mathematical reasoning
- **Image Processing**: PIL, OpenCV
- **Packaging**: Tauri bundler

## 📱 Platform Support

- ✅ **macOS** (10.13+)
- ✅ **Windows** (10+)
- ✅ **Linux** (Ubuntu 18.04+)

## 🔒 Privacy Features

- **No Internet Required**: Llama 3 runs completely locally
- **No Data Collection**: Your conversations never leave your device
- **Open Source Model**: Llama 3 is transparent and auditable
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

- **Meta** for the Llama 3 model
- **Hugging Face** for the Transformers library
- **Tauri** for the cross-platform framework
- **FastAPI** for the high-performance backend
- **Tailwind CSS** for the beautiful UI

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/veswo/veswo-assistant/issues)
- **Discussions**: [GitHub Discussions](https://github.com/veswo/veswo-assistant/discussions)
- **Email**: support@veswo.ai

---

**Made with ❤️ by the Veswo Team - Powered by Llama 3 7B** 