# AyouOS - Light Operating System

AyouOS is a lightweight application that combines a fast web browser with a dedicated AI assistant powered by Groq (Llama 3 models). Designed for speed and productivity.

## ✨ Features

- **Integrated Browser:** Fast web browsing based on Chromium.
- **AI Assistant:** Real-time chat with Llama-3 (70B) via Groq API.
- **Privacy First:** Your API key is stored locally on your machine (`config.txt`) and never shared.
- **Search Integration:** Type keywords in the address bar to search directly on Google.

## 🚀 How to use

1. **Launch AyouOS:** Run the `test.exe` (or `AyouOS.exe`).
2. **Setup AI:** - Get a free API key at [console.groq.com](https://console.groq.com/).
   - Paste the key in the "Enter Groq API Key" field.
3. **Browse & Chat:** Use the left side for the web and the right side for the AI.

## 🛠️ Installation (For Developers)

If you want to run the source code:

1. Install Python 3.10+
2. Install dependencies:
   ```bash
   pip install PyQt6 PyQt6-WebEngine requests pyinstaller
Run the script:

Bash

python test.py
📦 Build your own EXE
To compile the project into a single executable file:

Bash

py -m PyInstaller --onefile --noconsole --clean test.py
⚖️ License & Privacy
AI Model: Powered by Groq/Llama-3.

Data: This app does not collect personal data. All browsing and chat history are handled by your local machine and the respective API providers.
