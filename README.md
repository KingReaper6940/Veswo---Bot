# Veswo Bot 🧠

**Your AI Study Companion — 100% Local, Private, and Cross-Platform**

---

## ⚠️ System Requirements & Redistributables

**Currently, Veswo Bot only supports macOS.** Windows and Linux support coming soon!

Before running or building Veswo Bot, make sure your system has:

- **macOS 10.13+** (required - Windows/Linux support planned)
- **Python 3.8+** (required for backend)
- **Node.js 16+ and npm** (required for frontend/build)
- **Rust** (required for Tauri build)
- **Ollama** (local LLM runner, auto-installed if missing)
- **Homebrew** (recommended for auto-installing Ollama on macOS)

> **Note:**
> - The DMG/app will attempt to auto-install Python, Ollama, and dependencies on first run.
> - If Homebrew is not present, you may need to install it manually from [https://brew.sh/](https://brew.sh/).
> - If Python is missing, you may need to install it from [https://www.python.org/downloads/macos/](https://www.python.org/downloads/macos/).

---

## ✨ Features

- **Chat**: Natural language chat with a local LLM (Gemma AI via Ollama)
- **Math Solver**: Solve equations, render LaTeX beautifully
- **Essay Writer**: Generate essays on any topic (LLM-powered)
- **Science Helper**: Physics, chemistry, biology Q&A
- **Code Helper**: Code explanations, debugging, and generation
- **Glass Mode**: Minimal, transparent, draggable always-on-top widget for multitasking
- **Dark/Light Mode**: Toggle for comfortable day or night use
- **100% Local**: No data leaves your device

> **Coming Soon:**
> - Screenshot capture and analysis
> - Image OCR functionality
> - Windows and Linux support

---

## 📁 Project Layout

```
Veswo---Bot/
├── backend/                # FastAPI backend (Python, LLM)
│   └── utils/              # AI model and utility functions
├── frontend/               # React + Tauri frontend
│   ├── src/                # Main React app (App.jsx, components, styles)
│   └── src-tauri/          # Tauri Rust backend, config, icons
├── launcher.sh             # Robust backend/venv/Ollama launcher
├── requirements.txt        # Python dependencies
├── build.sh                # Build script for DMG
├── README.md               # (This file)
└── ...                     # Other scripts, docs, and configs
```

---

## 🚀 Quick Start (for Users)

1. **Download the latest DMG** from [GitHub Releases](https://github.com/your-repo/releases)
2. **Open the DMG and drag Veswo Bot to Applications**
3. **Launch Veswo Bot**
   - On first run, dependencies (Python, venv, pip, Ollama, model) are auto-installed if needed
   - If anything is missing, you'll see a macOS popup with instructions
4. **Start chatting, solving math, writing essays, or using any feature!**

---

## 🛠️ Building from Source (for Developers)

1. **Clone the repo and install prerequisites:**
   - Node.js (>=16), npm
   - Python 3.8+
   - Rust (for Tauri)
   - [Ollama](https://ollama.com/download) (auto-installed if missing)

2. **Run a clean build:**
   ```sh
   chmod +x build.sh
   ./build.sh
   ```
   - This will build the Tauri app and DMG, always including the backend and all dependencies.

3. **Find your app and DMG in:**
   - `frontend/src-tauri/target/release/bundle/macos/`
   - `frontend/src-tauri/target/release/bundle/dmg/`

---

## 🖥️ Usage Guide

- **Chat**: Type any question or prompt and hit send.
- **Math Solver**: Enter math problems (supports LaTeX, e.g. `$$x^2+2x+1=0$$`).
- **Essay Writer**: Ask for essays on any topic — the LLM handles everything.
- **Science Helper**: Ask science questions (physics, chemistry, biology).
- **Code Helper**: Paste code or ask for code explanations/generation.
- **Glass Mode**: Click the eye icon in the header for a minimal, transparent, draggable always-on-top widget. Great for multitasking!
- **Dark/Light Mode**: Click the moon/sun icon to toggle.

---

## 🔒 Privacy & Local-First
- All AI processing is local (Gemma AI via Ollama)
- No data leaves your device
- No API keys required
- Open source and auditable

---

## 📦 Dependencies
- **Frontend**: React, Tauri, Tailwind CSS, KaTeX (LaTeX rendering)
- **Backend**: FastAPI, Python, Ollama, Gemma AI model
- **Build**: Node.js, Rust, npm, pip

---

## 🤝 Contributing
- Fork the repo, create a branch, submit a PR!
- See `build.sh` for the recommended build process.

---

## 🙏 Credits
- **Veswo Team** — Project authors
- **Powered by Gemma AI** (via Ollama)
- **Tauri** — Cross-platform desktop framework
- **FastAPI** — High-performance Python backend
- **KaTeX** — Beautiful math rendering

---

**Made with ❤️ by the Veswo Team — Powered by Gemma AI** 
