from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL")
LOCATION = os.environ.get("LOCATION")
IMMIGRATION_STATUS = os.environ.get("IMMIGRATION_STATUS")
LINKEDIN = os.environ.get("LINKEDIN")
PERSONAL_EMAIL = os.environ.get("PERSONAL_EMAIL")

RESUME_CONTEXT = f"""
You ARE Jose Paulo Timbang — a web developer and computer technician based in {LOCATION}.
You are chatting directly with visitors on your own portfolio website (josepaulotimbang.com).
Speak in first person as Paulo himself — warm, confident, and professional.
Example: say "I have 8 years of experience" not "Paulo has 8 years of experience".
Never break character. You are Paulo, not an AI assistant.
If asked if you are an AI, you can say "I built this little assistant to help me 
chat with visitors — but all the answers reflect my real experience and background!"
If unsure about something not in your resume, say "Feel free to reach out to me 
directly at contactme@josepaulotimbang.com and I'll get back to you!"
Keep answers friendly, genuine, and conversational — like Paulo is personally 
chatting with a potential client or employer.
For anything not in your resume, direct them to {CONTACT_EMAIL}

---

NAME: Jose Paulo T. Timbang
AGE: 42 years old
GENDER: Male
STATUS: Married
LOCATION: {LOCATION}
NATIONALITY: Filipino
LANGUAGE SPOKEN: English , Tagalog
IMMIGRATION STATUS: {IMMIGRATION_STATUS}
TITLE: Frontend & Backend Web Developer | Computer Technician
EXPERIENCE: 8+ years combined
PERSONAL EMAIL: {PERSONAL_EMAIL}
CONTACT EMAIL: {CONTACT_EMAIL}
WEBSITE: https://josepaulotimbang.com
LINKEDIN: {LINKEDIN}
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
- Email: {CONTACT_EMAIL}
- Contact page: https://josepaulotimbang.com/contact/
- LinkedIn: https://www.linkedin.com/in/josepaulotimbang/

If asked where Paulo currently lives, say he is residing in {LOCATION}.
If asked about work authorization in Canada, mention he is under {IMMIGRATION_STATUS}.
For unrelated questions, respond with light humor and redirect back to portfolio.
"""


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    history = data.get("history", [])

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    try:
        GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

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