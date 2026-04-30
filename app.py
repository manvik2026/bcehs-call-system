"""
AI-Powered School Call System
The British Co-Ed High School, Patiala
Backend: Flask + Twilio TwiML + Google Gemini AI
Full Knowledge Base v2.0 - English Only
"""

import os
import google.generativeai as genai
from flask import Flask, request, Response, url_for
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "bcehs-secret-2026")

# ─── Gemini Setup ─────────────────────────────────────────────────────────────
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", ""))
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

# ─── Full School Knowledge Base ───────────────────────────────────────────────
SCHOOL_KB = """
=== THE BRITISH CO-ED HIGH SCHOOL — FULL KNOWLEDGE BASE v2.0 ===

BASIC INFORMATION:
- Full Name: The British Co-Ed High School
- Short Name: BCEHS / British Co-Ed
- Founded: 1986
- Founder: Mrs. Rosa Alicia Kucharskyj
- Current Principal: Ms. Kiran Harika
- Founder / Executive Principal: Mrs. Rosa Alicia Kucharskyj
- Type: Private, Unaided, Day School
- Co-Educational: Yes (Boys and Girls both)
- Board: CISCE — ICSE (Class X) and ISC (Class XII). NOT CBSE.
- Classes: Nursery (age 3+) through Class XII
- Medium of Instruction: English throughout
- Academic Session: Starts in April, ends in March
- School Motto: Her banner we shall hold up high and guard her honour till we die. Long live our dear school.

LOCATION:
- Address: Devigarh Road, Patiala, Punjab 147001, India
- Area: Sanour Block, Patiala District
- Distance: Approximately 8 km from main city of Patiala
- GPS: 30.29679 N, 76.42814 E

CONTACT DETAILS:
- Main Phone 1: +91-175-265-1122
- Main Phone 2: +91-175-265-1123
- Nursery and Junior Admissions Phone: +91-175-222-9089
- General Email: info@britishcoed.edu.in
- Nursery and Junior Admissions Email: bces@britishcoed.edu.in
- Website: www.britishcoedschool.com
- Facebook: facebook.com/p/The-British-Co-Ed-High-School-100064538690341
- Office Hours: Monday to Saturday, 11:00 AM to 2:30 PM. Closed on Sundays.

ADMISSIONS:
- Minimum Age for Nursery: 3 years
- Seats at Entry Level: approximately 150
- Average Class Strength: 30 students per class
- Student to Teacher Ratio: 30 to 1
- Total Classrooms: 27 instructional classrooms
- How to apply for Nursery or Junior School: Email bces@britishcoed.edu.in or call +91-175-222-9089
- How to apply for Class 1 and above: Email info@britishcoed.edu.in or call +91-175-265-1122
- Online admission forms available at www.britishcoedschool.com
- Admission season: typically before April session start

FEES:
- Fee structure is NOT publicly disclosed on any platform
- For fee information, call +91-175-265-1122 or email info@britishcoed.edu.in
- Cash payments accepted
- Always say: Exact fees are not published online. Please contact the school directly.

ACADEMICS AND CURRICULUM:
- Board: CISCE (Council for the Indian School Certificate Examinations)
- ICSE exam for Class X
- ISC exam for Class XII
- DISE School Code: 03170203305
- Optional international qualifications: IGCSE (Cambridge) or IB (International Baccalaureate) on application

SUBJECTS TAUGHT:
- English Language and Literature: Classes V to XII, includes Cambridge ESOL
- Modern Foreign Languages: Spanish (DELE certification), French (DELF certification), IGCSE option
- Punjabi: Compulsory for all, NRIs may opt for French or Spanish
- Hindi and Sanskrit: Classes V to XII, taught in Devnagari script
- Humanities: History, Civics, Geography (V to X), Psychology, Sociology, Political Science, Legal Studies
- Mathematics: Classes V to XII, PISA-aligned mathematical literacy
- Science: Physics, Chemistry, Biology, Classes V to XII, fully equipped labs
- ICT and Computer Science: Classes V to XII, 75 functional computers
- Accountancy: Classes XI to XII (ISC)
- Commerce: Classes XI to XII (ISC)
- Economics: Classes XI to XII (ISC)
- Art and Craft: Classes V to XII, Warli Art, Mandala Art, oil pastels, watercolours
- Physical Education: Classes V to XII
- Home Science: Classes IX to X (ICSE)
- Mass Media and Communication: Classes IX to X (ICSE)
- STEM Programme: Interdisciplinary Science, Technology, Engineering and Math, partnered with AFS and BP Global

INFRASTRUCTURE AND FACILITIES:
- Smart Classrooms: YES, technology-integrated
- Computer Lab: YES, 75 functional computers, networked CAL lab
- Library: YES, 7,580 books
- Science Labs: YES, Physics, Chemistry, Biology labs
- Activity Rooms: YES, 2 non-teaching activity rooms
- Playground and Sports Ground: YES
- Indoor Sports: YES
- Outdoor Sports: YES
- School Bus and Transport: YES, confirmed
- Toilets: 12 boys plus 12 girls, all functional
- Boundary Wall: YES, pucca boundary wall
- Electric Connection: YES
- AC Classrooms: NO, air-conditioned classrooms are NOT available
- Swimming Pool: NO, not available
- Boarding or Residential: NO, day school only
- Wi-Fi: Not confirmed publicly
- CCTV: Not confirmed publicly
- Auditorium: Not confirmed publicly
- Medical Centre: Not confirmed publicly

SCHOOL HOUSES:
- Tagore House: Yellow, named after Rabindranath Tagore, Indian poet and Nobel Laureate
- Teresa House: Green, named after Mother Teresa, Nobel Peace Prize winner
- Tolstoy House: Red, named after Leo Tolstoy, Russian novelist
- Inter-house competitions: Soccer, Hockey, Chess, Drama, Painting, Debating, Quizzes

SPORTS:
- Sports Day: Every November
- Sports trained: Athletics, Football, Hockey, KhoKho, Cricket, Basketball, Badminton, Table Tennis, Boxing
- Regular inter-school, zonal, district, state and national sports competitions
- PE classes in weekly timetable for all students

CO-CURRICULAR ACTIVITIES:
- Drama: Four inter-house plays annually, winning play performed at Annual Prize Giving
- School Band: Performs prayers at weekly assemblies
- Art and Craft: Warli Art, Mandala Art, oil pastels, watercolours, palette knife, paper collage
- Annual art exhibitions and inter-house painting competitions
- Academic competitions: Albert Barrow Memorial All India Inter-School Creative Writing Competition
- Inter-house, inter-school, inter-city debates, quizzes, creative writing, science exhibitions
- Science Exhibition: students present working models, winners felicitated at Annual Prize Giving

SCHOOL ENTERPRISE CHALLENGE - THE TIFFIN BOX:
- The school participates in the international School Enterprise Challenge
- School enterprise is called The Tiffin Box, a student-run food business
- Students raise funds for charity
- Students apply Commerce, Economics, Accountancy in real business simulations
- Annual Fete and Community Lunches also run by students

FIELD TRIPS AND INTERNATIONAL:
- Regular field trips, educational visits to industries and banks
- Outstation camps for students and staff
- International trips to Australia, United States, Canada

WEEKLY ASSEMBLIES:
- Monday: Classes 9 to 12 (Senior School), class performance plus School Band prayers
- Tuesday: Classes 6 to 8 (Middle School), class performance plus School Band prayers
- Wednesday: Classes 3 to 5 (Junior School), class performance plus School Band prayers

INTERNATIONAL ORGANISATIONS AND PARTNERSHIPS:
1. Round Square: Official member, global network of schools united by IDEALS (Internationalism, Democracy, Environment, Adventure, Leadership, Service). Offers international exchange opportunities.
2. AFS Intercultural Programs: Partner organisation. BP Global STEM Academies — four-week international STEM programmes in Brazil, Egypt, India and USA. BP Global STEM Academy Scholarship available to students.
3. NCC National Cadet Corps: Active unit with Air Wing and Army Wing. Students can earn NCC A, B, C certificates.
4. UKIERI UK-India Education and Research Initiative: Annual UK visits, staff and student exchanges with UK schools.
5. Duke of Edinburgh Award: Registered centre. Programme for skills, physical fitness, volunteering and expedition.
6. Cambridge English and British Council: Cambridge English ESOL examinations offered as value-added component.
7. Instituto Cervantes: DELE Spanish examinations preparation.
8. Alliance Francaise: DELF French examinations preparation.
9. Centre for Sustainable Development: Green School initiative, environmental education, learning by doing approach.
10. PISA Alignment: Mathematics and Science curriculum aligned with OECD PISA standards.

RATINGS AND REPUTATION:
- JustDial: 4.3 out of 5 stars, 21 reviews, top-rated school in Patiala
- Facebook: 100% recommendation rate, 14 reviewers
- Described as top service provider in Schools, English Medium, Senior Secondary, Co-Education, Middle Schools in Patiala
- Consistently praised for student-centred approach and holistic development

STAFF:
- Staff types: Primary Residential Teachers (PRTs), Trained Graduate Teachers (TGTs), Post Graduate Teachers (PGTs), Physical Education Teachers (PETs)
- All staff undergo continuous professional development
- Exact staff headcount not publicly disclosed

ALUMNI:
- No public alumni directory available
- School operating since 1986, graduates across four decades
- For alumni information contact school directly or check website

SCHOOL PHILOSOPHY:
- Students cannot be categorised or limited in their ideas, knowledge and creativity
- Focus on academic, technological, social and emotional development
- Child-centred, progressive day school
- Strong emphasis on holistic development

COMMON COMPLAINTS AND HOW TO HANDLE:
- For any complaint: Ask caller to describe the issue, note it down, and offer to connect to the school office at +91-175-265-1122
- For transport complaints: Direct to school office
- For teacher or academic complaints: Direct to school office or principal
- For fee disputes: Direct to school accounts office at +91-175-265-1122

IMPORTANT NOTES:
- Some directories like Skoodos incorrectly say CBSE — the correct board is CISCE/ICSE
- Some directories incorrectly say AC classrooms are available — they are NOT
- Always refer to official website www.britishcoedschool.com for accurate information
"""

SYSTEM_PROMPT = SCHOOL_KB + """

=== YOUR ROLE ===
You are a warm, professional, helpful phone receptionist for The British Co-Ed High School, Patiala.
Your name is Priya. You speak only in clear, simple English.

=== STRICT RULES FOR PHONE CALLS ===
1. Keep ALL responses under 35 words — this is a phone call, the caller hears audio only
2. Be warm, friendly and professional — like a real school receptionist
3. Never say you are an AI — behave like a real human receptionist
4. For fees: always say fees are not published, give phone number +91-175-265-1122
5. For complaints: be empathetic, note the issue, offer to connect to office
6. For unknown information: say you will check and connect them to the right person
7. Never make up any information not in the knowledge base
8. If caller asks something off-topic: politely say you can only help with school matters
9. Always end your response with one short follow-up question to help the caller further
10. Be natural — do not sound robotic or like a script

=== CONVERSATION STYLE ===
- Warm and welcoming
- Clear and concise
- Patient and helpful
- Professional school receptionist tone
"""

# ─── Voice config ─────────────────────────────────────────────────────────────
VOICE = "Polly.Aditi"
LANG  = "en-IN"

# ─── In-memory session store ──────────────────────────────────────────────────
sessions: dict = {}

# ─── Helpers ──────────────────────────────────────────────────────────────────

def get_sess(call_sid: str) -> dict:
    if call_sid not in sessions:
        sessions[call_sid] = {
            "name": None,
            "purpose": None,
            "step": "ask_name",
            "history": [],
            "irrelevant_count": 0,
            "no_response_count": 0,
        }
    return sessions[call_sid]

def twiml_resp(vr: VoiceResponse) -> Response:
    return Response(str(vr), mimetype="text/xml")

def say(vr: VoiceResponse, text: str) -> None:
    vr.say(text, voice=VOICE, language=LANG)

def gather_say(vr: VoiceResponse, action: str, text: str, timeout: int = 6) -> None:
    g = Gather(input="speech dtmf", action=action, method="POST",
               timeout=timeout, speech_timeout="3", language=LANG)
    g.say(text, voice=VOICE, language=LANG)
    vr.append(g)

def ai_reply(user_input: str, history: list) -> str:
    """Call Gemini for a dynamic school receptionist response."""
    try:
        history_text = ""
        for msg in history[-8:]:
            role = "Receptionist (Priya)" if msg["role"] == "assistant" else "Caller"
            history_text += f"{role}: {msg['content']}\n"

        prompt = (
            f"{SYSTEM_PROMPT}\n\n"
            f"=== CONVERSATION SO FAR ===\n{history_text}\n"
            f"Caller: {user_input}\n"
            f"Receptionist (Priya):"
        )
        response = gemini_model.generate_content(prompt)
        reply = response.text.strip()
        # Remove any asterisks or markdown from Gemini response
        reply = reply.replace("*", "").replace("#", "").replace("_", "")
        return reply
    except Exception as e:
        print(f"[Gemini Error] {e}")
        return "I apologize for the technical difficulty. Please call us directly at 0175-265-1122. We are happy to help you."

def is_irrelevant(text: str) -> bool:
    """Check if caller input is completely off-topic."""
    keywords = [
        "pizza", "burger", "food delivery", "movie", "film", "weather",
        "joke", "game", "stock market", "crypto", "bitcoin", "girlfriend",
        "boyfriend", "dating", "politics", "cricket score", "netflix",
        "amazon", "flipkart", "shopping", "lottery", "casino"
    ]
    return any(k in text.lower() for k in keywords)

def is_farewell(text: str) -> bool:
    """Check if caller wants to end the call."""
    words = [
        "bye", "goodbye", "good bye", "thank you", "thanks", "ok bye",
        "that is all", "thats all", "nothing else", "i am done", "all good",
        "no more questions", "okay thank you", "ok thank you"
    ]
    return any(w in text.lower() for w in words)

def is_complaint(text: str) -> bool:
    words = ["complaint", "complain", "problem", "issue", "unhappy",
             "upset", "wrong", "bad", "not good", "terrible", "worst"]
    return any(w in text.lower() for w in words)

def is_admission(text: str) -> bool:
    words = ["admission", "admissions", "enroll", "enrolment", "join",
             "nursery", "new student", "apply", "application", "register"]
    return any(w in text.lower() for w in words)

def is_fees(text: str) -> bool:
    words = ["fee", "fees", "cost", "price", "charges", "tuition",
             "how much", "payment", "money", "pay"]
    return any(w in text.lower() for w in words)

# ═══════════════════════════════════════════════════════════════════════════════
# ROUTES
# ═══════════════════════════════════════════════════════════════════════════════

@app.route("/voice", methods=["GET", "POST"])
def voice():
    """Entry point — Twilio calls this when someone dials the number."""
    call_sid = request.values.get("CallSid", "test")
    sess = get_sess(call_sid)
    sessions[call_sid] = sess

    vr = VoiceResponse()
    gather_say(
        vr,
        url_for("ask_name", _external=True),
        "Hello and welcome to The British Co-Ed High School, Patiala. "
        "This is Priya speaking. "
        "May I know your good name please?",
        timeout=8
    )
    say(vr, "We did not receive your response. Please call again. Thank you. Goodbye.")
    vr.hangup()
    return twiml_resp(vr)


@app.route("/ask_name", methods=["POST"])
def ask_name():
    """Collect caller name."""
    call_sid = request.values.get("CallSid", "test")
    speech   = request.values.get("SpeechResult", "").strip()
    sess     = get_sess(call_sid)

    if not speech or len(speech) < 2:
        sess["no_response_count"] += 1
        sessions[call_sid] = sess
        if sess["no_response_count"] >= 2:
            vr = VoiceResponse()
            say(vr, "We are unable to hear you clearly. Please call again. Thank you. Goodbye.")
            vr.hangup()
            return twiml_resp(vr)
        vr = VoiceResponse()
        gather_say(vr, url_for("ask_name", _external=True),
                   "I am sorry, I could not hear your name clearly. "
                   "Could you please say your name?")
        vr.hangup()
        return twiml_resp(vr)

    sess["name"] = speech
    sess["no_response_count"] = 0
    sess["history"].append({"role": "user", "content": f"My name is {speech}"})
    sess["history"].append({"role": "assistant", "content": f"Thank you {speech}! How may I assist you today?"})
    sessions[call_sid] = sess

    vr = VoiceResponse()
    gather_say(
        vr,
        url_for("ask_purpose", _external=True),
        f"Thank you, {speech}! "
        "How may I assist you today? "
        "You can ask about admissions, fees, academics, facilities, sports, "
        "or any other information about the school.",
        timeout=8
    )
    say(vr, "No response received. Thank you for calling. Goodbye.")
    vr.hangup()
    return twiml_resp(vr)


@app.route("/ask_purpose", methods=["POST"])
def ask_purpose():
    """Determine purpose and route to the right handler."""
    call_sid = request.values.get("CallSid", "test")
    speech   = request.values.get("SpeechResult", "").strip()
    sess     = get_sess(call_sid)
    name     = sess.get("name", "")

    # No speech
    if not speech:
        sess["no_response_count"] += 1
        sessions[call_sid] = sess
        if sess["no_response_count"] >= 2:
            vr = VoiceResponse()
            say(vr, "We are unable to hear you. Please call again at 0175-265-1122. Thank you. Goodbye.")
            vr.hangup()
            return twiml_resp(vr)
        vr = VoiceResponse()
        gather_say(vr, url_for("ask_purpose", _external=True),
                   "I am sorry, could you please tell me how I can help you today?")
        vr.hangup()
        return twiml_resp(vr)

    sess["no_response_count"] = 0

    # Irrelevant check
    if is_irrelevant(speech):
        sess["irrelevant_count"] += 1
        sessions[call_sid] = sess
        if sess["irrelevant_count"] >= 2:
            return _end_call_irrelevant()
        vr = VoiceResponse()
        gather_say(vr, url_for("ask_purpose", _external=True),
                   "I am sorry, I can only assist with school related queries. "
                   "Could you please tell me how I can help you regarding the school?")
        vr.hangup()
        return twiml_resp(vr)

    # Farewell
    if is_farewell(speech):
        return _farewell_call(name)

    sess["purpose"] = speech
    sess["history"].append({"role": "user", "content": speech})
    sessions[call_sid] = sess

    # Smart routing based on purpose
    vr = VoiceResponse()

    if is_admission(speech):
        # Ask for class
        gather_say(
            vr,
            url_for("ask_class", _external=True),
            f"Certainly {name}! We would love to welcome you to The British Co-Ed family. "
            "Which class or grade are you seeking admission for?",
            timeout=8
        )

    elif is_fees(speech):
        # Direct fee answer
        fee_reply = (
            f"Thank you for asking, {name}. "
            "Our fee structure is not published online. "
            "Please contact us at 0175-265-1122 or email info at britishcoed dot edu dot in "
            "for complete fee details. Is there anything else I can help you with?"
        )
        sess["history"].append({"role": "assistant", "content": fee_reply})
        sessions[call_sid] = sess
        gather_say(vr, url_for("ai_chat", _external=True), fee_reply, timeout=8)

    elif is_complaint(speech):
        # Handle complaint
        complaint_reply = (
            f"I am sorry to hear that, {name}. "
            "I understand your concern and I want to make sure it is addressed properly. "
            "Could you please briefly describe the issue so I can note it down?"
        )
        sess["history"].append({"role": "assistant", "content": complaint_reply})
        sessions[call_sid] = sess
        gather_say(vr, url_for("ai_chat", _external=True), complaint_reply, timeout=10)

    else:
        # General AI reply
        ai_text = ai_reply(speech, sess["history"])
        sess["history"].append({"role": "assistant", "content": ai_text})
        sessions[call_sid] = sess
        gather_say(vr, url_for("ai_chat", _external=True), ai_text, timeout=8)

    say(vr, "Thank you for calling The British Co-Ed High School. Goodbye.")
    vr.hangup()
    return twiml_resp(vr)


@app.route("/ask_class", methods=["POST"])
def ask_class():
    """Handle admission class query."""
    call_sid = request.values.get("CallSid", "test")
    speech   = request.values.get("SpeechResult", "").strip()
    sess     = get_sess(call_sid)
    name     = sess.get("name", "")

    if not speech:
        vr = VoiceResponse()
        gather_say(vr, url_for("ask_class", _external=True),
                   "Could you please tell me which class you are looking for?")
        vr.hangup()
        return twiml_resp(vr)

    sess["history"].append({"role": "user", "content": f"I want admission for class {speech}"})
    sessions[call_sid] = sess

    ai_text = ai_reply(
        f"I want admission for class {speech}. Please give me all relevant admission information.",
        sess["history"]
    )
    sess["history"].append({"role": "assistant", "content": ai_text})
    sessions[call_sid] = sess

    vr = VoiceResponse()
    gather_say(vr, url_for("ai_chat", _external=True), ai_text, timeout=8)
    say(vr, "Thank you for calling The British Co-Ed High School. Have a wonderful day. Goodbye.")
    vr.hangup()
    return twiml_resp(vr)


@app.route("/ai_chat", methods=["POST"])
def ai_chat():
    """Main multi-turn AI conversation loop."""
    call_sid = request.values.get("CallSid", "test")
    speech   = request.values.get("SpeechResult", "").strip()
    sess     = get_sess(call_sid)
    name     = sess.get("name", "")

    # No speech — end call
    if not speech:
        sess["no_response_count"] += 1
        sessions[call_sid] = sess
        if sess["no_response_count"] >= 2:
            vr = VoiceResponse()
            say(vr, f"Thank you for calling, {name}. "
                    "Please do not hesitate to call again if you need any help. "
                    "Have a wonderful day. Goodbye.")
            vr.hangup()
            sessions.pop(call_sid, None)
            return twiml_resp(vr)
        vr = VoiceResponse()
        gather_say(vr, url_for("ai_chat", _external=True),
                   "I am still here. Is there anything else I can help you with?", timeout=6)
        vr.hangup()
        return twiml_resp(vr)

    sess["no_response_count"] = 0

    # Farewell
    if is_farewell(speech):
        return _farewell_call(name)

    # Irrelevant
    if is_irrelevant(speech):
        sess["irrelevant_count"] += 1
        sessions[call_sid] = sess
        if sess["irrelevant_count"] >= 3:
            return _end_call_irrelevant()
        vr = VoiceResponse()
        gather_say(vr, url_for("ai_chat", _external=True),
                   "I am sorry, I can only help with school related questions. "
                   "Is there anything about the school I can assist you with?")
        vr.hangup()
        return twiml_resp(vr)

    # Normal AI conversation
    sess["history"].append({"role": "user", "content": speech})
    ai_text = ai_reply(speech, sess["history"])
    sess["history"].append({"role": "assistant", "content": ai_text})
    sessions[call_sid] = sess

    vr = VoiceResponse()
    gather_say(vr, url_for("ai_chat", _external=True), ai_text, timeout=8)
    say(vr, "Thank you for calling. Goodbye.")
    vr.hangup()
    return twiml_resp(vr)


def _farewell_call(name: str) -> Response:
    """Warm goodbye."""
    vr = VoiceResponse()
    say(vr,
        f"Thank you so much for calling, {name}. "
        "It was a pleasure assisting you. "
        "We look forward to welcoming you to The British Co-Ed High School. "
        "Have a wonderful day. Goodbye!")
    vr.hangup()
    return twiml_resp(vr)


def _end_call_irrelevant() -> Response:
    """Politely end call for off-topic callers."""
    vr = VoiceResponse()
    say(vr,
        "I am sorry, we are unable to assist with this matter. "
        "Please call again if you have any school related queries. "
        "Thank you for calling The British Co-Ed High School. Goodbye.")
    vr.hangup()
    return twiml_resp(vr)


@app.route("/health", methods=["GET"])
def health():
    return {
        "status": "ok",
        "school": "The British Co-Ed High School, Patiala",
        "website": "www.britishcoedschool.com",
        "active_sessions": len(sessions),
        "ai_engine": "Google Gemini 1.5 Flash"
    }


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"School Call System (Gemini) running on port {port}")
    app.run(debug=True, host="0.0.0.0", port=port)
