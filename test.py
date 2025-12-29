import sys
import requests
import os
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLineEdit, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QWidget, QTextEdit, QLabel, QFrame)
from PyQt6.QtWebEngineWidgets import QWebEngineView

class AyouOS(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AyouOS")
        self.resize(1280, 720)
        self.config_file = "config.txt"

        # --- UI COMPONENTS ---
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))

        # Navigation Bar
        self.address_bar = QLineEdit()
        self.address_bar.setPlaceholderText("Search or enter URL...")
        self.address_bar.returnPressed.connect(self.load_url)
        
        btn_back = QPushButton("←")
        btn_next = QPushButton("→")
        btn_reload = QPushButton("↻")
        btn_back.clicked.connect(self.browser.back)
        btn_next.clicked.connect(self.browser.forward)
        btn_reload.clicked.connect(self.browser.reload)

        # AI Sidebar
        self.ai_panel = QFrame()
        self.ai_panel.setFixedWidth(320)
        self.ai_panel.setStyleSheet("background-color: #f8f9fa; border-left: 1px solid #dee2e6;")
        
        ai_layout = QVBoxLayout()
        
        # API Key management
        self.api_input = QLineEdit()
        self.api_input.setPlaceholderText("Enter Groq API Key...")
        self.api_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.load_saved_key() # Load key if exists

        self.ai_display = QTextEdit()
        self.ai_display.setReadOnly(True)
        self.ai_display.setStyleSheet("background-color: white; border-radius: 5px;")

        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Ask AI anything...")
        self.chat_input.returnPressed.connect(self.ask_groq)

        send_btn = QPushButton("Send to AI")
        send_btn.clicked.connect(self.ask_groq)

        ai_layout.addWidget(QLabel("<b>AyouOS AI ASSISTANT</b>"))
        ai_layout.addWidget(self.api_input)
        ai_layout.addWidget(self.ai_display)
        ai_layout.addWidget(self.chat_input)
        ai_layout.addWidget(send_btn)
        self.ai_panel.setLayout(ai_layout)

        # --- LAYOUT SETUP ---
        nav_layout = QHBoxLayout()
        nav_layout.addWidget(btn_back)
        nav_layout.addWidget(btn_next)
        nav_layout.addWidget(btn_reload)
        nav_layout.addWidget(self.address_bar)

        left_container = QVBoxLayout()
        left_container.addLayout(nav_layout)
        left_container.addWidget(self.browser)

        main_layout = QHBoxLayout()
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        main_layout.addLayout(left_container, stretch=4)
        main_layout.addWidget(self.ai_panel, stretch=1)

        self.setCentralWidget(main_widget)

    def load_url(self):
        url = self.address_bar.text()
        if "." not in url:
            url = f"https://www.google.com/search?q={url}"
        elif not url.startswith("http"):
            url = "https://" + url
        self.browser.setUrl(QUrl(url))

    def load_saved_key(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                self.api_input.setText(f.read().strip())

    def save_key(self, key):
        with open(self.config_file, "w") as f:
            f.write(key)

    def ask_groq(self):
        user_text = self.chat_input.text()
        api_key = self.api_input.text()
        
        if not api_key or not user_text:
            self.ai_display.append("<b style='color:red;'>System:</b> Please enter API Key and a question.")
            return

        self.save_key(api_key) # Save key for next time
        self.ai_display.append(f"<b>You:</b> {user_text}")
        self.chat_input.clear()
        
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": user_text}]
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            data = response.json()
            if 'choices' in data:
                answer = data['choices'][0]['message']['content']
                self.ai_display.append(f"<b>AI:</b> {answer}<br>")
            else:
                self.ai_display.append("<b style='color:red;'>System:</b> Invalid API Key or limit reached.")
        except Exception as e:
            self.ai_display.append(f"<b style='color:red;'>System Error:</b> {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AyouOS()
    window.show()
    sys.exit(app.exec())