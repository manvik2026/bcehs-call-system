# 🏫 AI-Powered School Call System
### The British Co-Ed High School, Patiala
**Twilio + Flask + Claude AI · Bilingual (Hindi / English)**

---

## What This Does

When someone calls your Twilio number, the system:
1. **Greets** the caller professionally (Hindi + English simultaneously)
2. **Asks language preference** — Press 1 for Hindi, Press 2 for English
3. **Collects name** via speech recognition
4. **Asks purpose** — Admission, Fees, Complaint, General Info, etc.
5. **Routes smartly** — admission queries also ask for class/grade
6. **Responds with Claude AI** — dynamic, contextual, school-specific answers
7. **Handles irrelevant callers** — politely ends call after 2–3 off-topic inputs
8. **Ends gracefully** — warm farewell in chosen language

---

## Project Structure

```
school_call_system/
├── app.py              ← Main Flask application (all routes + AI logic)
├── requirements.txt    ← Python dependencies
├── .env.example        ← Environment variable template
├── test_call.py        ← Local test simulator (no real phone needed)
├── dashboard.html      ← Visual system reference dashboard
└── README.md           ← This file
```

---

## Prerequisites

| Tool | Get It |
|------|--------|
| Python 3.9+ | python.org |
| Twilio Account | twilio.com (free trial works) |
| Anthropic API Key | console.anthropic.com |
| ngrok | ngrok.com (for local dev) |

---

## Step-by-Step Setup

### Step 1 — Install Dependencies
```bash
cd school_call_system
pip install -r requirements.txt
```

### Step 2 — Configure Environment
```bash
cp .env.example .env
```
Edit `.env` and fill in your keys:
```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=+1XXXXXXXXXX
ANTHROPIC_API_KEY=sk-ant-xxxxxxxx
```

### Step 3 — Run the Server
```bash
python app.py
```
You'll see: `🏫 BCEHS Call System running on port 5000`

### Step 4 — Expose via ngrok
In a new terminal:
```bash
ngrok http 5000
```
Copy the HTTPS URL, e.g. `https://abc123.ngrok-free.app`

### Step 5 — Configure Twilio Webhook
1. Go to [Twilio Console](https://console.twilio.com)
2. Phone Numbers → Manage → Active Numbers → click your number
3. Under **Voice & Fax**:
   - **A Call Comes In** → Webhook → `https://abc123.ngrok-free.app/voice`
   - Method: `HTTP POST`
4. Save

### Step 6 — Test!
Call your Twilio number from any phone. Or run the local simulator:
```bash
python test_call.py
```

---

## Call Flow

```
📞 Incoming Call
      │
      ▼
  /voice ──────── "Welcome to British Co-Ed... Press 1 Hindi, 2 English"
      │
      ▼
  /lang_select ── Detects DTMF digit (1 or 2)
      │
      ▼
  /ask_name ───── "May I know your name?" (speech input)
      │
      ▼
  /ask_purpose ── "How may I assist you?" (Admission / Fees / Complaint...)
      │
      ├─── Admission? ──▶ /ask_class ── "Which class?"
      │
      └─── Other ───────▶ /ai_chat ─── Claude AI loop (multi-turn)
                               │
                               └─── Farewell / Irrelevant ──▶ Graceful end
```

---

## AI Behavior

Claude is given a **system prompt** containing the full school knowledge base:

- School history, leadership, board affiliation
- Facilities, sports, co-curricular activities
- Contact numbers and email addresses
- International programs (Round Square, AFS, NCC, Duke of Edinburgh...)
- Admission process and office hours
- Fee policy: "not publicly disclosed, contact school"

Claude responds in **under 40 words** (phone-optimized, no long paragraphs).

---

## Handling Edge Cases

| Situation | System Response |
|-----------|----------------|
| No speech detected | Re-prompts once, then hangs up |
| Irrelevant input (pizza, jokes...) | Redirects; ends after 2-3 attempts |
| Fees question | "Fees not online — call 0175-265-1122" |
| Unknown info | "Let me connect you to our office" |
| Farewell detected | Warm goodbye in chosen language |
| Claude API error | Falls back to hardcoded contact number |

---

## Voice Configuration

- **TTS Engine**: Amazon Polly (Aditi voice) — Indian English + Hindi
- **STT**: Twilio speech recognition
- **Input modes**: Speech + DTMF (touch-tone) simultaneously
- **Speech timeout**: 3 seconds of silence = end of input
- **Gather timeout**: 5-7 seconds to start speaking

---

## Deployment to Production

### Option A: Railway / Render / Fly.io
```bash
# Add environment variables in the platform dashboard
# Set start command: gunicorn app:app --bind 0.0.0.0:$PORT
```

### Option B: VPS (Ubuntu)
```bash
pip install gunicorn
gunicorn app:app --bind 0.0.0.0:5000 --workers 2
```

Then use nginx as reverse proxy and set Twilio webhook to your domain.

---

## School Contact Reference (Built into AI)

| Contact | Details |
|---------|---------|
| Main Phone | +91-175-265-1122 / +91-175-265-1123 |
| Nursery Admissions | +91-175-222-9089 |
| General Email | info@britishcoed.edu.in |
| Nursery Email | bces@britishcoed.edu.in |
| Website | www.britishcoedschool.com |
| Office Hours | Mon–Sat, 11 AM – 2:30 PM |

---

## License
Built for The British Co-Ed High School, Patiala · April 2026
