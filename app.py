from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

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

He has a deep-rooted passion for technology, having spent years building and repairing computers,
giving him a solid foundation in troubleshooting and technical problem-solving. His background
also includes digital marketing assistance and tech support, allowing him to bridge the gap
between development, user needs, and business goals.

---

WORK EXPERIENCE:

1. Web Designer (2013-2022)
   - Designed and developed responsive websites for various clients
   - Technologies: HTML, CSS, JavaScript, PHP, WordPress
   - Focus: UX, performance optimization, SEO, digital marketing strategies

2. Web Developer (2013-2022)
   - Built and maintained responsive websites, custom tools, and CMS-driven platforms
   - Integrated SEO, analytics, and social media features
   - Optimized code performance and site functionality

3. Computer Technician (2008-2022)
   - PC assembly, hardware/software support, and repairs for residential and business clients
   - BIOS/UEFI configuration, OS installation, data recovery
   - Cybersecurity implementation, network setup and troubleshooting
   - Remote technical support, inventory and client communication management

4. Graphic Designer (2020-2022)
   - Created marketing materials, social media graphics, and custom website visuals
   - Designed responsive layouts and maintained visual brand consistency

5. Digital Marketing Assistant (2020-2022)
   - Supported brand identity and online engagement through creative visuals
   - Assisted with social media and digital campaigns

---

TECHNICAL SKILLS:

Web Development & Design:
- HTML, CSS, JavaScript, PHP
- WordPress (themes, plugins, customization)
- Shopify, Laravel, CodeIgniter
- Figma, Adobe Photoshop
- Responsive & mobile-first design
- SEO optimization

Computer Technician Skills:
- PC Assembly & Repair
- Hardware Replacement & Upgrades
- Networking Setup & Troubleshooting
- BIOS/UEFI Configuration
- Operating System installation & management
- Data Recovery, Cybersecurity Measures
- Remote Technical Support

---

SERVICES PAULO OFFERS:
- Web Development (custom websites, WordPress, Shopify)
- Web Design / UI-UX
- Digital Marketing (SEO, social media)
- Computer Tech Support (PC repair, networking)
- Graphic Design (logos, banners, marketing materials)
- Frontend & Backend Development

---

PORTFOLIO:
Paulo has a portfolio visible at https://josepaulotimbang.com/portfolio/

---

AVAILABILITY & RATES:
Direct visitors to:
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

        # Call Gemini REST API directly
        response = requests.post(
            GEMINI_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )

        result = response.json()

        # Extract reply text
        reply = result["candidates"][0]["content"]["parts"][0]["text"]

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "Paulo AI Chatbot is running"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)