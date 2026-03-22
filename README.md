# Paulo AI Resume Chatbot — Setup Guide
**100% Free Stack: Python + Flask + Google Gemini + WordPress**

---

## 📁 Project Structure

```
paulo-ai-chatbot/
├── app.py                        ← Python Flask server (backend AI)
├── requirements.txt              ← Python dependencies
├── .env                          ← Your API key (create this yourself)
└── wordpress-plugin/
    ├── paulo-ai-chatbot.php      ← WordPress plugin
    ├── chat-widget.js            ← Chat UI behavior
    └── chat-widget.css           ← Chat UI styles
```

---

## STEP 1 — Get Free Gemini API Key

1. Go to https://aistudio.google.com/app/apikey
2. Sign in with a Google account
3. Click "Create API Key"
4. Copy the key — it's FREE (no credit card needed)

---

## STEP 2 — Set Up the Python Server Locally

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Create a .env file with your API key
echo "GEMINI_API_KEY=your_api_key_here" > .env

# 3. Run the server
python app.py
# Server runs at: http://localhost:5000
```

Test it:
```bash
curl http://localhost:5000/health
# Should return: {"status": "ok"}
```

---

## STEP 3 — Deploy Python Server for FREE

You need the Python server live on the internet so your WordPress site can reach it.
Here are the best FREE options:

### Option A: Render.com (Recommended — easiest)
1. Create free account at https://render.com
2. New → Web Service → connect your GitHub repo
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn app:app`
5. Add environment variable: `GEMINI_API_KEY = your_key`
6. Deploy → get your URL like: `https://paulo-chatbot.onrender.com`

### Option B: Railway.app
1. Create free account at https://railway.app
2. New Project → Deploy from GitHub
3. Add env var: `GEMINI_API_KEY = your_key`
4. Get URL like: `https://paulo-chatbot.up.railway.app`

### Option C: Your own VPS / cPanel hosting
If your web host supports Python:
```bash
# Upload files, then run with gunicorn
gunicorn --bind 0.0.0.0:5000 app:app
```

---

## STEP 4 — Install WordPress Plugin

1. Upload the `wordpress-plugin/` folder to:
   `/wp-content/plugins/paulo-ai-chatbot/`

2. Go to WordPress Admin → Plugins → Activate "Paulo AI Resume Chatbot"

3. Go to Settings → AI Chatbot
   - Enter your Python server URL (e.g., `https://paulo-chatbot.onrender.com`)
   - Save

4. Visit your site — chat bubble appears bottom-right ✅

---

## STEP 5 — Update Your Resume

To update the AI's knowledge about you, edit the `RESUME_CONTEXT` string in `app.py`
and redeploy. No changes needed to WordPress.

---

## Cost Summary

| Component        | Cost   |
|-----------------|--------|
| Plugin code      | Free   |
| WordPress        | Free   |
| Python / Flask   | Free   |
| Google Gemini API| Free (15 req/min, 1500 req/day) |
| Render.com hosting | Free tier available |

**Total: $0/month for a personal portfolio**

---

## Troubleshooting

- **Chat says "Connection error"** → Check that your Python server URL is correct in WP settings
- **CORS error in browser console** → The `flask-cors` package handles this; make sure it's installed
- **Gemini rate limit hit** → Free tier allows 15 requests/min; more than enough for a portfolio
