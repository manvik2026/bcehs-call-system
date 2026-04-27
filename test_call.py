"""
Local test script — simulates Twilio webhook calls without a real phone.
Run: python test_call.py
Make sure app.py is running first: python app.py
"""

import requests

BASE = "http://localhost:5000"
CALL_SID = "TEST_CALL_SID_001"

def post(url, data):
    r = requests.post(url, data=data)
    print(f"\n{'='*60}")
    print(f"POST {url}")
    print(f"Input: {data}")
    print(f"TwiML Response:\n{r.text}")
    return r

def test_english_admission():
    print("\n" + "🏫 "*10)
    print("TEST: English — Admission Enquiry")
    print("🏫 "*10)

    # 1. Incoming call
    post(f"{BASE}/voice", {"CallSid": CALL_SID})

    # 2. Press 2 for English
    post(f"{BASE}/lang_select", {"CallSid": CALL_SID, "Digits": "2"})

    # 3. Say name
    post(f"{BASE}/ask_name", {"CallSid": CALL_SID, "SpeechResult": "Rajveer Singh"})

    # 4. Say purpose
    post(f"{BASE}/ask_purpose", {"CallSid": CALL_SID, "SpeechResult": "I want to take admission for my son"})

    # 5. Say class
    post(f"{BASE}/ask_class", {"CallSid": CALL_SID, "SpeechResult": "Class 6"})

    # 6. Follow-up question
    post(f"{BASE}/ai_chat", {"CallSid": CALL_SID, "SpeechResult": "What documents are required?"})

    # 7. Goodbye
    post(f"{BASE}/ai_chat", {"CallSid": CALL_SID, "SpeechResult": "Thank you, goodbye"})

def test_hindi_fees():
    CALL_SID2 = "TEST_CALL_SID_002"
    print("\n" + "🏫 "*10)
    print("TEST: Hindi — Fees Enquiry")
    print("🏫 "*10)

    post(f"{BASE}/voice", {"CallSid": CALL_SID2})
    post(f"{BASE}/lang_select", {"CallSid": CALL_SID2, "Digits": "1"})
    post(f"{BASE}/ask_name", {"CallSid": CALL_SID2, "SpeechResult": "Priya Sharma"})
    post(f"{BASE}/ask_purpose", {"CallSid": CALL_SID2, "SpeechResult": "फीस के बारे में जानना है"})
    post(f"{BASE}/ai_chat", {"CallSid": CALL_SID2, "SpeechResult": "वार्षिक फीस कितनी है?"})

def test_irrelevant_caller():
    CALL_SID3 = "TEST_CALL_SID_003"
    print("\n" + "🏫 "*10)
    print("TEST: Irrelevant Caller — Should be ended politely")
    print("🏫 "*10)

    post(f"{BASE}/voice", {"CallSid": CALL_SID3})
    post(f"{BASE}/lang_select", {"CallSid": CALL_SID3, "Digits": "2"})
    post(f"{BASE}/ask_name", {"CallSid": CALL_SID3, "SpeechResult": "Random Guy"})
    post(f"{BASE}/ask_purpose", {"CallSid": CALL_SID3, "SpeechResult": "I want to order a pizza"})
    post(f"{BASE}/ask_purpose", {"CallSid": CALL_SID3, "SpeechResult": "Tell me a joke"})

if __name__ == "__main__":
    test_english_admission()
    test_hindi_fees()
    test_irrelevant_caller()
    print("\n✅ All tests complete!")
