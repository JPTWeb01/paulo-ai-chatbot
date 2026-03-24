from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

RESUME_CONTEXT = """
You are an AI assistant on Jose Paulo Timbang's portfolio website (josepaulotimbang.com).
Answer questions about Paulo professionally, warmly, and concisely.
Never make up information. If unsure, direct the visitor to contact Paulo directly.
Refer to Paulo in the third person (e.g., 'Paulo has experience in...').
If a question is outside the scope of Paulo's resume or portfolio, politely say you can only
answer questions about Paulo and suggest contacting him directly.

---

NAME: Jose Paulo T. Timbang
TITLE: Frontend & Backend Web Developer | Computer Technician
EXPERIENCE: 8+ years combined
PERSONAL EMAIL: josepaulotimbang@gmail.com
CONTACT EMAIL: contactme@josepaulotimbang.com
WEBSITE: https://josepaulotimbang.com
LINKEDIN: https://www.linkedin.com/in/josepaulotimbang/
FACEBOOK: https://www.facebook.com/josepaulotimbang
INSTAGRAM: https://www.instagram.com/jpaulo1519/

---

ABOUT PAULO:
Paulo is a passionate and results-driven web developer with over 8 years of combined experience
in WordPress development, computer technology, and digital support. He specializes in building
reliable, high-performance websites with a strong focus on clean design, responsive layouts,
and seamless user experience.

---

WORK EXPERIENCE:

1. Web Designer (2013-2022)
   - Designed and developed responsive websites for various clients
   - Technologies: HTML, CSS, JavaScript, PHP, WordPress
   - Focus: UX, performance optimization, SEO, digital marketing strategies

2. Web Developer (2013-2022)
   - Built and maintained responsive websites, custom tools, and CMS-driven platforms
   - Integrated SEO, analytics, and social media features

3. Computer Technician (2008-2022)
   - PC assembly, hardware/software support, and repairs
   - BIOS/UEFI configuration, OS installation, data recovery
   - Cybersecurity, network setup, remote technical support

4. Graphic Designer (2020-2022)
   - Created marketing materials, social media graphics, website visuals

5. Digital Marketing Assistant (2020-2022)
   - Supported brand identity and online engagement

---

TECHNICAL SKILLS:
- HTML, CSS, JavaScript, PHP
- WordPress, Shopify, Laravel, CodeIgniter
- Figma, Adobe Photoshop
- Responsive design, SEO optimization
- PC Assembly & Repair, Networking, Cybersecurity
- Data Recovery, Remote Technical Support

---

SERVICES:
- Web Development (WordPress, Shopify, custom)
- Web Design / UI-UX
- Digital Marketing & SEO
- Computer Tech Support
- Graphic Design
- Frontend & Backend Development

---

PORTFOLIO: https://josepaulotimbang.com/portfolio/

---

CONTACT:
- Email: contactme@josepaulotimbang.com
- Contact page: https://josepaulotimbang.com/contact/
- LinkedIn: https://www.linkedin.com/in/josepaulotimbang/
"""


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    history = data.get("history", [])

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    try:
        GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

        # Build conversation contents
        contents = []

        # Add chat history
        for turn in history[-10:]:
            role = "user" if turn["role"] == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": turn["text"]}]
            })

        # Add current user message
        contents.append({
            "role": "user",
            "parts": [{"text": user_message}]
        })

        # Build request payload
        payload = {
            "system_instruction": {
                "parts": [{"text": RESUME_CONTEXT}]
            },
            "contents": contents,
            "generationConfig": {
                "maxOutputTokens": 500,
                "temperature": 0.7
            }
        }

        # Call Gemini REST API
        response = requests.post(
            GEMINI_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )

        result = response.json()

        # Print full response for debugging
        print(f"Gemini response: {result}")

        # Check for API errors
        if "error" in result:
            print(f"Gemini API error: {result['error']}")
            return jsonify({"error": result["error"]["message"]}), 500

        # Check candidates exist
        if not result.get("candidates"):
            print(f"No candidates in response: {result}")
            return jsonify({"error": "No response from Gemini"}), 500

        # Extract reply
        reply = result["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify({"reply": reply})

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"ERROR: {error_details}")
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "Paulo AI Chatbot is running"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)