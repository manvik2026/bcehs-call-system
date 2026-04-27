"""
AI-Powered School Call System
The British Co-Ed High School, Patiala
Backend: Flask + Twilio TwiML + Claude AI
"""

import os
import anthropic
from flask import Flask, request, Response, url_for
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "bcehs-secret-2026")

# ─── Anthropic client ─────────────────────────────────────────────────────────
claude_client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))

# ─── School Knowledge Base ────────────────────────────────────────────────────
SCHOOL_KB = """
SCHOOL: The British Co-Ed High School (BCEHS), Patiala
Founded: 1986 by Mrs. Rosa Alicia Kucharskyj
Principal: Ms. Kiran Harika | Founder/Executive Principal: Mrs. Rosa Alicia Kucharskyj
Board: CISCE — ICSE (Class X), ISC (Class XII). NOT CBSE.
Classes: Nursery (age 3+) to Class XII
Location: Devigarh Road, Patiala – 147001, Punjab (~8 km from city centre)
Phone: +91-175-265-1122 / +91-175-265-1123 | Nursery: +91-175-222-9089
Email: info@britishcoed.edu.in | Nursery: bces@britishcoed.edu.in
Website: www.britishcoedschool.com
Seats at entry: ~150 | Class strength: 30 | Student:Teacher ratio: 30:1
Session starts: April each year
Houses: Tagore (Yellow), Teresa (Green), Tolstoy (Red)
Facilities: Smart classrooms, Computer lab (75 PCs), Library (7,580 books), Science labs, Sports ground, School bus
NOT available: AC classrooms, Swimming pool, Boarding/Residential
Sports: Athletics, Football, Hockey, KhoKho, Cricket, Basketball, Badminton, Table Tennis, Boxing
International: Round Square member, AFS/BP STEM Academies, NCC (Air+Army Wings), UKIERI, Duke of Edinburgh Award
Languages: French (DELF cert), Spanish (DELE cert), Cambridge English/ESOL
Optional: IGCSE/IB on application
Fees: NOT publicly disclosed — callers must contact school at +91-175-265-1122 or info@britishcoed.edu.in
Office hours: Monday to Saturday, 11:00 AM – 2:30 PM
Admission email (Nursery/Junior): bces@britishcoed.edu.in
Subjects: English, Hindi, Punjabi, Sanskrit, Maths, Physics, Chemistry, Biology, History, Geography, Civics,
          Psychology, Sociology, Commerce, Economics, Accountancy, ICT/Computer Science, Art, PE, Home Science,
          Mass Media, STEM Programme
Rating: 4.3/5 on JustDial, 100% recommend on Facebook
"""

SYSTEM_EN = SCHOOL_KB + """
ROLE: You are a warm, professional phone receptionist for The British Co-Ed High School, Patiala.
STRICT RULES:
- Keep ALL responses under 40 words — this is a PHONE CALL, caller hears audio
- Be friendly, helpful, school-receptionist style (not robotic)
- For fees: say fees are not published, give contact number
- For unknown info: say you'll connect them to the office
- If off-topic/irrelevant: politely redirect to school matters only
- Never invent facts; use only the knowledge base above
- End with a brief helpful follow-up question
"""

SYSTEM_HI = SCHOOL_KB + """
ROLE: आप The British Co-Ed High School, Patiala की विनम्र फ़ोन रिसेप्शनिस्ट हैं। हिंदी में जवाब दें।
नियम:
- जवाब 40 शब्दों से कम रखें — यह फ़ोन कॉल है
- विनम्र, पेशेवर और मददगार रहें
- फीस के लिए: ऑनलाइन उपलब्ध नहीं, स्कूल से संपर्क करें
- अज्ञात जानकारी के लिए: ऑफ़िस से कनेक्ट करने का प्रस्ताव दें
- स्कूल से असंबंधित सवाल पर: विनम्रता से वापस स्कूल के विषय पर लाएं
- केवल knowledge base की जानकारी दें
"""

# ─── Voice config ─────────────────────────────────────────────────────────────
VOICE_EN = ("Polly.Aditi", "en-IN")
VOICE_HI = ("Polly.Aditi", "hi-IN")

# ─── In-memory session store (keyed by CallSid) ───────────────────────────────
sessions: dict = {}

# ─── Helpers ──────────────────────────────────────────────────────────────────

def get_sess(call_sid: str) -> dict:
    if call_sid not in sessions:
        sessions[call_sid] = {
            "lang": None, "name": None, "purpose": None,
            "step": "lang_select", "history": [], "irrelevant_count": 0,
        }
    return sessions[call_sid]

def twiml_resp(vr: VoiceResponse) -> Response:
    return Response(str(vr), mimetype="text/xml")

def say(vr: VoiceResponse, text: str, lang: str = "en") -> None:
    v, l = VOICE_HI if lang == "hi" else VOICE_EN
    vr.say(text, voice=v, language=l)

def gather_say(vr: VoiceResponse, action: str, text: str,
               lang: str = "en", timeout: int = 5) -> None:
    v, l = VOICE_HI if lang == "hi" else VOICE_EN
    g = Gather(input="speech dtmf", action=action, method="POST",
               timeout=timeout, speech_timeout="3", language=l)
    g.say(text, voice=v, language=l)
    vr.append(g)

def ai_reply(user_input: str, history: list, lang: str) -> str:
    system = SYSTEM_HI if lang == "hi" else SYSTEM_EN
    msgs = history[-6:] + [{"role": "user", "content": user_input}]
    try:
        resp = claude_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=150,
            system=system,
            messages=msgs,
        )
        return resp.content[0].text.strip()
    except Exception as e:
        print(f"[Claude Error] {e}")
        if lang == "hi":
            return "क्षमा करें, तकनीकी समस्या है। कृपया 0175-265-1122 पर कॉल करें।"
        return "Sorry, technical issue. Please call the school at 0175-265-1122."

def irrelevant(text: str) -> bool:
    keywords = ["pizza","movie","weather","joke","game","stock","crypto",
                 "girlfriend","boyfriend","politics","cricket score","netflix"]
    return any(k in text.lower() for k in keywords)

def farewell(text: str) -> bool:
    words = ["bye","goodbye","thank you","thanks","धन्यवाद","अलविदा","बाय","ok bye","thx"]
    return any(w in text.lower() for w in words)

# ═══════════════════════════════════════════════════════════════════════════════
# ROUTES
# ═══════════════════════════════════════════════════════════════════════════════

@app.route("/voice", methods=["GET", "POST"])
def voice():
    """Entry point — Twilio webhook when someone calls."""
    call_sid = request.values.get("CallSid", "test")
    sess = get_sess(call_sid)
    sess["step"] = "lang_select"
    sessions[call_sid] = sess

    vr = VoiceResponse()
    g = Gather(num_digits=1, action=url_for("lang_select", _external=True),
               method="POST", timeout=8)
    g.say(
        "Namaste! Welcome to The British Co-Ed High School, Patiala. "
        "Press 1 for Hindi.  Press 2 for English.  "
        "हिंदी के लिए 1 दबाएं।  English के लिए 2 दबाएं।",
        voice="Polly.Aditi", language="en-IN"
    )
    vr.append(g)
    say(vr, "We did not receive your input. Please call again. Dhanyavaad.")
    vr.hangup()
    return twiml_resp(vr)


@app.route("/lang_select", methods=["POST"])
def lang_select():
    call_sid = request.values.get("CallSid", "test")
    digit    = request.values.get("Digits", "")
    sess     = get_sess(call_sid)

    if digit == "1":
        sess["lang"] = "hi"
    elif digit == "2":
        sess["lang"] = "en"
    else:
        vr = VoiceResponse()
        g = Gather(num_digits=1, action=url_for("lang_select", _external=True),
                   method="POST", timeout=8)
        g.say("Invalid input. Press 1 for Hindi, 2 for English.  "
              "गलत इनपुट। हिंदी के लिए 1, English के लिए 2 दबाएं।",
              voice="Polly.Aditi", language="en-IN")
        vr.append(g)
        vr.hangup()
        return twiml_resp(vr)

    sess["step"] = "ask_name"
    sessions[call_sid] = sess
    lang = sess["lang"]

    vr = VoiceResponse()
    if lang == "hi":
        gather_say(vr, url_for("ask_name", _external=True),
                   "नमस्ते! ब्रिटिश को-एड हाई स्कूल, पटियाला में आपका स्वागत है। "
                   "कृपया अपना नाम बताएं।", lang="hi")
        say(vr, "कोई जवाब नहीं मिला। कृपया दोबारा कॉल करें।", "hi")
    else:
        gather_say(vr, url_for("ask_name", _external=True),
                   "Good day! Thank you for calling The British Co-Ed High School, Patiala. "
                   "May I know your good name, please?", lang="en")
        say(vr, "No response received. Please call again. Thank you.")
    vr.hangup()
    return twiml_resp(vr)


@app.route("/ask_name", methods=["POST"])
def ask_name():
    call_sid = request.values.get("CallSid", "test")
    speech   = request.values.get("SpeechResult", "").strip()
    sess     = get_sess(call_sid)
    lang     = sess.get("lang", "en")

    if not speech or len(speech) < 2:
        vr = VoiceResponse()
        if lang == "hi":
            gather_say(vr, url_for("ask_name", _external=True),
                       "क्षमा करें, मैं आपका नाम नहीं सुन पाई। कृपया दोबारा बताएं।", "hi")
        else:
            gather_say(vr, url_for("ask_name", _external=True),
                       "I'm sorry, I didn't catch your name. Could you please repeat it?")
        vr.hangup()
        return twiml_resp(vr)

    sess["name"] = speech
    sess["step"] = "ask_purpose"
    sess["history"].append({"role": "user", "content": f"My name is {speech}"})
    sessions[call_sid] = sess

    vr = VoiceResponse()
    if lang == "hi":
        gather_say(vr, url_for("ask_purpose", _external=True),
                   f"{speech} जी, धन्यवाद! आपकी कॉल का उद्देश्य क्या है? "
                   "प्रवेश, फीस, शिकायत, जानकारी, या कुछ और?", "hi")
        say(vr, "कोई जवाब नहीं। धन्यवाद।", "hi")
    else:
        gather_say(vr, url_for("ask_purpose", _external=True),
                   f"Thank you, {speech}! How may I assist you today? "
                   "You can say — Admission, Fees enquiry, Complaint, or General information.")
        say(vr, "No response. Thank you for calling. Goodbye!")
    vr.hangup()
    return twiml_resp(vr)


@app.route("/ask_purpose", methods=["POST"])
def ask_purpose():
    call_sid = request.values.get("CallSid", "test")
    speech   = request.values.get("SpeechResult", "").strip()
    sess     = get_sess(call_sid)
    lang     = sess.get("lang", "en")
    name     = sess.get("name", "")

    if not speech:
        vr = VoiceResponse()
        if lang == "hi":
            gather_say(vr, url_for("ask_purpose", _external=True),
                       "क्षमा करें, कृपया अपनी कॉल का उद्देश्य बताएं।", "hi")
        else:
            gather_say(vr, url_for("ask_purpose", _external=True),
                       "Sorry, could you please tell me the purpose of your call?")
        vr.hangup()
        return twiml_resp(vr)

    if irrelevant(speech):
        sess["irrelevant_count"] += 1
        sessions[call_sid] = sess
        if sess["irrelevant_count"] >= 2:
            return _end_call(lang)
        vr = VoiceResponse()
        if lang == "hi":
            gather_say(vr, url_for("ask_purpose", _external=True),
                       "मैं केवल स्कूल से संबंधित सहायता कर सकती हूँ। "
                       "कृपया अपनी कॉल का उद्देश्य बताएं।", "hi")
        else:
            gather_say(vr, url_for("ask_purpose", _external=True),
                       "I can only assist with school-related matters. "
                       "Could you please tell me the purpose of your call?")
        vr.hangup()
        return twiml_resp(vr)

    sess["purpose"] = speech
    sess["history"].append({"role": "user", "content": f"Purpose of call: {speech}"})
    sess["step"] = "ai_conversation"
    sessions[call_sid] = sess

    # Check if admission-related (needs class info)
    admission_words = ["admission","admissions","enroll","enrolment","join","nursery",
                       "प्रवेश","दाखिला","join the school"]
    needs_class = any(w in speech.lower() for w in admission_words)

    vr = VoiceResponse()
    if needs_class:
        if lang == "hi":
            gather_say(vr, url_for("ask_class", _external=True),
                       f"बहुत अच्छा, {name} जी! ब्रिटिश को-एड में आपका स्वागत है। "
                       "आप किस कक्षा के लिए प्रवेश चाहते हैं?", "hi")
        else:
            gather_say(vr, url_for("ask_class", _external=True),
                       f"Wonderful, {name}! We'd love to welcome you to The British Co-Ed family. "
                       "Which class or grade are you seeking admission for?")
    else:
        ai_text = ai_reply(
            f"Caller name: {name}. They say: {speech}. Address their query helpfully.",
            sess["history"], lang
        )
        sess["history"].append({"role": "assistant", "content": ai_text})
        sessions[call_sid] = sess
        gather_say(vr, url_for("ai_chat", _external=True), ai_text, lang, timeout=7)
        if lang == "hi":
            say(vr, "कोई जवाब नहीं। धन्यवाद। नमस्ते!", "hi")
        else:
            say(vr, "Thank you for calling. Goodbye!")

    vr.hangup()
    return twiml_resp(vr)


@app.route("/ask_class", methods=["POST"])
def ask_class():
    call_sid = request.values.get("CallSid", "test")
    speech   = request.values.get("SpeechResult", "").strip()
    sess     = get_sess(call_sid)
    lang     = sess.get("lang", "en")
    name     = sess.get("name", "")

    if not speech:
        vr = VoiceResponse()
        if lang == "hi":
            gather_say(vr, url_for("ask_class", _external=True),
                       "कृपया कक्षा बताएं।", "hi")
        else:
            gather_say(vr, url_for("ask_class", _external=True),
                       "Could you please tell me the class or grade?")
        vr.hangup()
        return twiml_resp(vr)

    sess["history"].append({"role": "user", "content": f"Wants admission for class: {speech}"})
    sessions[call_sid] = sess

    ai_text = ai_reply(
        f"{name} wants admission for class {speech}. Give admission process and contact details.",
        sess["history"], lang
    )
    sess["history"].append({"role": "assistant", "content": ai_text})
    sessions[call_sid] = sess

    vr = VoiceResponse()
    gather_say(vr, url_for("ai_chat", _external=True), ai_text, lang, timeout=7)
    if lang == "hi":
        say(vr, "धन्यवाद। नमस्ते!", "hi")
    else:
        say(vr, "Thank you for calling The British Co-Ed High School. Have a lovely day. Goodbye!")
    vr.hangup()
    return twiml_resp(vr)


@app.route("/ai_chat", methods=["POST"])
def ai_chat():
    """Main AI conversation loop — handles follow-up questions."""
    call_sid = request.values.get("CallSid", "test")
    speech   = request.values.get("SpeechResult", "").strip()
    sess     = get_sess(call_sid)
    lang     = sess.get("lang", "en")

    if not speech:
        vr = VoiceResponse()
        if lang == "hi":
            say(vr, "धन्यवाद, कॉल करने के लिए शुक्रिया। नमस्ते!", "hi")
        else:
            say(vr, "Thank you for calling The British Co-Ed High School. Goodbye!")
        vr.hangup()
        sessions.pop(call_sid, None)
        return twiml_resp(vr)

    if farewell(speech):
        vr = VoiceResponse()
        if lang == "hi":
            say(vr, "धन्यवाद! ब्रिटिश को-एड में आपका हमेशा स्वागत है। नमस्ते!", "hi")
        else:
            say(vr, "Thank you for calling! We look forward to welcoming you to "
                    "The British Co-Ed High School. Have a wonderful day. Goodbye!")
        vr.hangup()
        sessions.pop(call_sid, None)
        return twiml_resp(vr)

    if irrelevant(speech):
        sess["irrelevant_count"] += 1
        sessions[call_sid] = sess
        if sess["irrelevant_count"] >= 3:
            return _end_call(lang)

    sess["history"].append({"role": "user", "content": speech})
    ai_text = ai_reply(speech, sess["history"], lang)
    sess["history"].append({"role": "assistant", "content": ai_text})
    sessions[call_sid] = sess

    vr = VoiceResponse()
    gather_say(vr, url_for("ai_chat", _external=True), ai_text, lang, timeout=7)
    if lang == "hi":
        say(vr, "धन्यवाद। नमस्ते!", "hi")
    else:
        say(vr, "Thank you for calling. Goodbye!")
    vr.hangup()
    return twiml_resp(vr)


def _end_call(lang: str) -> Response:
    """Politely terminate call for irrelevant/time-wasting callers."""
    vr = VoiceResponse()
    if lang == "hi":
        say(vr,
            "क्षमा करें, हम आपकी और सहायता करने में असमर्थ हैं। "
            "यदि आपको स्कूल से संबंधित सहायता चाहिए तो कृपया दोबारा कॉल करें। "
            "धन्यवाद। नमस्ते!", "hi")
    else:
        say(vr,
            "I'm sorry, we are unable to assist further. "
            "Please call again if you have school-related queries. "
            "Thank you for calling The British Co-Ed High School. Goodbye!")
    vr.hangup()
    return twiml_resp(vr)


@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok", "school": "The British Co-Ed High School, Patiala",
            "active_sessions": len(sessions)}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🏫 BCEHS Call System running on port {port}")
    app.run(debug=True, host="0.0.0.0", port=port)
