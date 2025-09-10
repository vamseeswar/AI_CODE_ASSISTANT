---
# 🚀 AI Code Assistant with Groq + OCR + Multi-Language Execution

This project is an **AI-powered coding assistant** that:
- Accepts **text or image-based problem statements** (via OCR using Tesseract).  
- Uses **Groq LLM** to generate a solution with explanation and complexities.  
- Extracts code, detects the programming language, and **executes it automatically**.  
- Supports multiple programming languages (Python, Java, C++, C, JavaScript, Go, R, Ruby, Kotlin).  
- Runs as a **Flask web application** with a simple frontend.  

---

## ✨ Features
- 📷 **Image to Code**: Upload coding problems as images (OCR with Tesseract).  
- 🤖 **AI Solution Generation**: Powered by Groq’s `llama-3.1-8b-instant` model.  
- 💻 **Code Execution**: Runs code in multiple languages.  
- 📊 **Complexity Analysis**: Explains time and space complexities.  
- 🌐 **Web Interface**: Flask backend with an interactive UI.  

---

## ⚙️ Requirements

### 🐍 Python Dependencies
Install Python packages with:

```bash
pip install -r requirements.txt
````

**requirements.txt**

```
Flask
groq
python-dotenv
pillow
pytesseract
```

### 🖥 System Dependencies

* **Tesseract OCR** → [Download here](https://github.com/tesseract-ocr/tesseract)
  (Ensure path matches in `app.py`: `C:\Program Files\Tesseract-OCR\tesseract.exe`)

* **Language Runtimes / Compilers** (install as needed):

  * Python ≥ 3.10
  * Java (JDK with `javac` and `java`)
  * GCC / G++ (C & C++)
  * Node.js (JavaScript)
  * Go (GoLang)
  * R (`Rscript`)
  * Ruby
  * Kotlin (`kotlinc`, `java`)

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key_here
```

---

## ▶️ Run the App

```bash
python app.py
```

Then open your browser at:
👉 `http://127.0.0.1:5000/`

---

## 📂 Project Structure

```
AI-Code-Assistant/
│-- app.py                # Main Flask application
│-- templates/
│   └── index.html        # Frontend UI
│-- requirements.txt      # Python dependencies
│-- .env                  # API keys and environment variables
│-- README.md             # Documentation
```

---

## 💡 Example Queries & Outputs

### Example 1: Python Problem

**Input (text):**

```
Write a Python function to find the minimum element in a rotated sorted array.
```

**AI Response (Extracted):**

```python
def find_min(nums):
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid
    return nums[left]

print(find_min([4,5,6,7,0,1,2]))
```

**Output:**

```
0
```

---

### Example 2: Java Problem

**Input (image OCR + text):**

```
Write a Java program to check if a string is a palindrome.
```

**AI Response (Extracted):**

```java
public class Palindrome {
    public static boolean isPalindrome(String s) {
        int left = 0, right = s.length() - 1;
        while (left < right) {
            if (s.charAt(left) != s.charAt(right)) return false;
            left++;
            right--;
        }
        return true;
    }

    public static void main(String[] args) {
        System.out.println(isPalindrome("racecar")); // true
    }
}
```

**Output:**

```
true
```

---

### Example 3: JavaScript Problem

**Input (text):**

```
Write a JavaScript function to reverse a string.
```

**AI Response (Extracted):**

```javascript
function reverseString(str) {
    return str.split("").reverse().join("");
}

console.log(reverseString("hello"));
```

**Output:**

```
olleh
```

---

## 🌍 Deployment

You can deploy this app on platforms like:

* [Render](https://render.com/)
* [Heroku](https://www.heroku.com/)
* [Vercel + Flask (via serverless)](https://vercel.com/)

Make sure to install system dependencies (Tesseract + compilers) in your deployment environment.

---



