---
title: Decoder
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
---

# Decoder | Intelligent AI Coding Assistant

**Decoder** is a powerful, open-source AI coding assistant designed to help developers debug, generate, and understand code instantly. It bridges the gap between visual problem statements (images) and executable solutions.

![Decoder Interface](https://img.shields.io/badge/Status-Active-success) ![License](https://img.shields.io/badge/License-MIT-blue) ![Python](https://img.shields.io/badge/Python-3.9%2B-yellow)

## 🚀 Features

-   **📸 OCR-Powered extraction**: Upload an image (screenshot, photo) of code or an error message, and Decoder will extract the text automatically using Tesseract OCR.
-   **🧠 Advanced AI Logic**: Powered by **Groq (Llama 3)**, providing lightning-fast and accurate coding solutions.
-   **⚡ Multi-Language Execution**: Write and **execute** code directly within the app. Supported languages include:
    *   Python (`.py`)
    *   Java (`.java`)
    *   C (`.c`) & C++ (`.cpp`)
    *   JavaScript (`.js`)
    *   Go (`.go`)
    *   Ruby (`.rb`)
    *   R (`.r`)
    *   Kotlin (`.kt`)
-   **🎨 Dynamic UI**:
    *   **Single Page Application (SPA)** architecture.
    *   **4 Beautiful Themes**: Default (Space), Ocean, Sunset, Neon.
    *   **Sidebar Navigation**: Easy access to Home, History, Settings, and About.
-   **📜 Request History**: Automatically saves your queries and solutions locally so you can revisit them later.
-   **🐳 Dockerized**: Fully containerized for easy deployment on compatible platforms like Hugging Face Spaces.

## 🛠️ Tech Stack

-   **Backend**: Flask (Python)
-   **AI Engine**: Groq API (Llama 3.1 8B)
-   **OCR Engine**: Tesseract OCR
-   **Frontend**: HTML5, CSS3 (Glassmorphism), JavaScript (Vanilla)
-   **Infrastructure**: Docker

## 📦 Installation & Local Setup

### Prerequisites
1.  **Python 3.9+** installed.
2.  **Tesseract OCR** installed on your system.
    *   *Windows*: [Download Installer](https://github.com/UB-Mannheim/tesseract/wiki) (Set path to `C:\Program Files\Tesseract-OCR\tesseract.exe`)
    *   *Linux/Mac*: `sudo apt install tesseract-ocr` / `brew install tesseract`
3.  **Compilers** (Optional, for code execution):
    *   `GCC`/`G++` for C/C++
    *   `JDK` for Java
    *   `Node.js` for JavaScript

### Steps

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/decoder.git
    cd decoder
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Environment Variables**
    Create a `.env` file in the root directory and add your Groq API key:
    ```env
    GROQ_API_KEY=gsk_your_actual_api_key_here
    ```

5.  **Run the Application**
    ```bash
    python app.py
    ```
    Access the app at `http://localhost:7860`.

## 🐳 Deployment (Hugging Face Spaces)

This project is configured to run seamlessly on **Hugging Face Spaces** using Docker.

1.  Create a new Space on Hugging Face.
2.  Select **Docker** as the SDK.
3.  Upload the contents of this repository.
4.  Go to **Settings > Secrets** in your Space and add:
    *   `GROQ_API_KEY`: Your Groq API key.
5.  The `Dockerfile` handles the installation of all necessary system dependencies (Tesseract, Java, GCC, etc.).

## 📂 Project Structure

```
decoder/
├── app.py              # Main Flask application & execution logic
├── Dockerfile          # Docker configuration for HF Spaces
├── requirements.txt    # Python dependencies
├── .env                # API Keys (not committed)
├── static/
│   └── style.css       # Dynamic styles & themes
└── templates/
    └── index.html      # Main SPA interface
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---
Built with ❤️ by **Vamseeswar**
