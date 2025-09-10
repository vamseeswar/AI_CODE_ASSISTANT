import os
import re
import tempfile
import subprocess
from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv
from PIL import Image
import pytesseract

# ------------------ Load environment variables ------------------
load_dotenv()
app = Flask(__name__)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# ------------------ Configure Tesseract ------------------
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ------------------ Supported Languages ------------------
LANGUAGE_EXTENSIONS = {
    "python": "py",
    "java": "java",
    "cpp": "cpp",
    "c": "c",
    "javascript": "js",
    "go": "go",
    "r": "r",
    "ruby": "rb",
    "kotlin": "kt",
}

def build_command(lang, filepath):
    """Return execution command for given language & filepath."""
    base, ext = os.path.splitext(filepath)

    if lang == "python":
        return ["python", filepath]

    elif lang == "java":
        classname = os.path.basename(base)  # Use temp filename as class
        return ["bash", "-c", f"javac {filepath} && java {classname}"]

    elif lang == "cpp":
        exe = base + ".exe" if os.name == "nt" else base + ".out"
        return ["bash", "-c", f"g++ {filepath} -o {exe} && {exe}"]

    elif lang == "c":
        exe = base + ".exe" if os.name == "nt" else base + ".out"
        return ["bash", "-c", f"gcc {filepath} -o {exe} && {exe}"]

    elif lang == "javascript":
        return ["node", filepath]

    elif lang == "go":
        return ["go", "run", filepath]

    elif lang == "r":
        return ["Rscript", filepath]

    elif lang == "ruby":
        return ["ruby", filepath]

    elif lang == "kotlin":
        jarfile = base + ".jar"
        return ["bash", "-c", f"kotlinc {filepath} -include-runtime -d {jarfile} && java -jar {jarfile}"]

    return None

# ------------------ Helper functions ------------------
def ask_groq(prompt, system_message="You are an expert developer and teacher."):
    """Ask Groq API for code solution with explanation and complexities."""
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error querying Groq API: {str(e)}"

def ocr_function(file_storage):
    """Extract text from uploaded image using Tesseract OCR."""
    try:
        image = Image.open(file_storage)
        text = pytesseract.image_to_string(image, config="--psm 6")
        return text.strip()
    except Exception as e:
        return f"⚠ OCR Error: {str(e)}"

def extract_code_and_language(text: str):
    """Extract all code blocks and language from Groq's response."""
    matches = re.findall(r"(\w+)?\n([\s\S]*?)", text, re.MULTILINE)
    if matches:
        lang = matches[0][0].lower() if matches[0][0] else "python"
        code = "\n\n".join(m[1] for m in matches)
        return lang, code.strip()
    return "python", ""  # default to Python

def execute_code(lang: str, code: str):
    """Execute code in multiple languages."""
    if not code.strip():
        return "⚠ No code detected."

    if lang not in LANGUAGE_EXTENSIONS:
        return f"⚠ Language {lang} not supported."

    try:
        ext = LANGUAGE_EXTENSIONS[lang]
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}", mode="w", encoding="utf-8") as tmp:
            tmp.write(code)
            tmp_path = tmp.name

        # Force print for Python if no print statement exists
        if lang == "python" and "print(" not in code:
            code += "\n\nprint('⚠ No print statement found, only function defined.')\n"
            with open(tmp_path, "w", encoding="utf-8") as f:
                f.write(code)

        # Build execution command
        cmd = build_command(lang, tmp_path)
        if not cmd:
            return "⚠ Unsupported language."

        result = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, shell=(os.name == "nt"), timeout=20
        )

        output = result.stdout.strip()
        error = result.stderr.strip()

        if error and not output:
            return f"⚠ Error:\n{error}"
        elif output and error:
            return f"{output}\n⚠ Errors:\n{error}"
        return output or "⚠ No output produced."
    except Exception as e:
        return f"⚠ Execution error: {str(e)}"

# ------------------ Routes ------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message, extracted_text = "", ""

    if request.content_type.startswith("multipart/form-data"):
        image_file = request.files.get("image")
        text_input = request.form.get("query", "").strip()
        user_message = text_input
        if image_file:
            extracted_text = ocr_function(image_file)
            user_message += "\n" + extracted_text
    elif request.is_json:
        user_message = request.json.get("message", "").strip()
    else:
        return jsonify({"response": "⚠ Unsupported request type"}), 415

    if not user_message:
        return jsonify({"response": "⚠ No input received"}), 400

    # Prompt for Groq
    prompt = f"""
Write a complete solution for the following problem:

{user_message}

Requirements:
1. Provide working code in the appropriate language.
2. Include explanation of the approach.
3. Mention Time Complexity and Space Complexity.
4. Use Markdown code fences with correct language (python, java, cpp, c, javascript, go, r, ruby, kotlin).
"""

    # Ask Groq
    groq_response = ask_groq(prompt)
    if groq_response.startswith("Error querying Groq API"):
        return jsonify({"response": f"<div class='bg-red-100 text-red-800 p-4 rounded'><pre>{groq_response}</pre></div>"})

    # Extract code & language
    lang, code_to_exec = extract_code_and_language(groq_response)
    execution_output = execute_code(lang, code_to_exec)

    # Prepare response
    return jsonify({
        "response": f"<h2>📄 Extracted Text from Image:</h2><pre>{extracted_text}</pre>"
                    f"<h2>💡 Suggested {lang.title()} Solution with Explanation:</h2><pre>{groq_response}</pre>"
                    f"<div class='bg-green-100 text-green-900 p-4 rounded'><strong>✅ Output:</strong><br><pre>{execution_output}</pre></div>"
    })

# ------------------ Run Flask ------------------
if __name__ == "__main__":
    app.run(debug=True)