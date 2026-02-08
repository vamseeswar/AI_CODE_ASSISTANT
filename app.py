import os
import re
import tempfile
import subprocess
from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv
# from PIL import Image # Not needed anymore server-side
# import pytesseract # Not needed anymore server-side

# ------------------ Load environment variables ------------------
load_dotenv()
app = Flask(__name__)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# ------------------ Configure Tesseract ------------------
# REMOVED: Tesseract is now handled on the client-side via Tesseract.js for Vercel compatibility.
# The server only processes text and code.

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
    is_windows = os.name == "nt"

    if lang == "python":
        return ["python", filepath]

    elif lang == "java":
        dirname = os.path.dirname(filepath)
        classname = os.path.basename(base)
        if is_windows:
            return f'javac "{filepath}" && java -cp "{dirname}" {classname}'
        return ["bash", "-c", f"javac {filepath} && java -cp {dirname} {classname}"]

    elif lang == "cpp":
        exe = base + ".exe" if is_windows else base + ".out"
        if is_windows:
            return f'g++ "{filepath}" -o "{exe}" && "{exe}"'
        return ["bash", "-c", f"g++ {filepath} -o {exe} && {exe}"]

    elif lang == "c":
        exe = base + ".exe" if is_windows else base + ".out"
        if is_windows:
            return f'gcc "{filepath}" -o "{exe}" && "{exe}"'
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
        if is_windows:
            return f'kotlinc "{filepath}" -include-runtime -d "{jarfile}" && java -jar "{jarfile}"'
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

# REMOVED: ocr_function (Client-side OCR used instead)

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

        # Vercel Serverless Constraint
        # Vercel functions are read-only and don't have compilers installed.
        # Simple Python scripts might run, but other languages will fail.
        if os.environ.get("VERCEL"):
             if lang != "python":
                 return f"⚠ Execution of {lang} is not supported on Vercel Serverless environment. Please use Hugging Face Spaces for full feature set."
             
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

    try:
        extracted_text = ""
        user_message = ""

        if request.is_json:
            data = request.json
            user_message = data.get("message", "").strip()
            # If the client sent extracted text separately for display purposes
            extracted_text = data.get("extracted_text", "")
        else:
            return jsonify({"error": "Unsupported request type. Use JSON."}), 415

        if not user_message:
            return jsonify({"error": "No input received"}), 400

        # Prompt for Groq
        prompt = f"""
Write a complete solution for the following problem:

{user_message}

Requirements:
1. Provide working code in one of the following supported languages if applicable: Python, Java, C++, C, JavaScript, Go, R, Ruby, Kotlin.
2. If the problem requires a specific language not listed, provide the code but note that it cannot be executed in this environment.
3. Include a clear and concise explanation of the approach.
4. Mention Time Complexity and Space Complexity.
5. Use Markdown code fences with correct language identifier (e.g., ```python ... ```).
"""

        # Ask Groq
        groq_response = ask_groq(prompt)
        if groq_response.startswith("Error querying Groq API"):
            return jsonify({"error": groq_response}), 500

        # Extract code & language
        # Improved regex to find markdown code blocks accurately
        code_block_match = re.search(r"```(\w+)\n([\s\S]*?)```", groq_response)
        if code_block_match:
            lang = code_block_match.group(1).lower()
            code_to_exec = code_block_match.group(2).strip()
        else:
            lang, code_to_exec = "python", ""

        execution_output = ""
        if code_to_exec:
            execution_output = execute_code(lang, code_to_exec)

        # Prepare response
        return jsonify({
            "extracted_text": extracted_text,
            "solution": groq_response,
            "language": lang,
            "code": code_to_exec,
            "output": execution_output,
            "status": "success"
        })

    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

# ------------------ Run Flask ------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port, debug=True)
