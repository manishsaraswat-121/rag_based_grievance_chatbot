import re
import requests

REGISTER_API = "http://localhost:8000/register"
STATUS_API = "http://localhost:8000/status"

def get_bot_response(user_input: str, session_state: dict) -> str:
    user_input = user_input.strip()
    lower_input = user_input.lower()
    greetings = ["hi", "hlo","hello", "hey", "good morning", "good evening"]

    # Handle greeting
    if any(greet in lower_input for greet in greetings):
        return ("👋 Hello! I’m your grievance assistant bot.\n"
                "You can say things like:\n"
                "• 'I want to register a complaint'\n"
                "• 'What’s the status of my complaint?'\n"
                "How may I help you today?")

    # Handle registration flow
    if 'register' in lower_input or ('complaint' in lower_input and 'track' not in lower_input and 'status' not in lower_input):

        session_state.clear()
        session_state["mode"] = "register"
        session_state["step"] = "ask_name"
        return "Sure! Let's register your complaint. What's your full name?"

    if session_state.get("mode") == "register":
        if session_state["step"] == "ask_name":
            if user_input.replace(" ", "").isalpha():
                session_state["name"] = user_input
                session_state["step"] = "ask_mobile"
                return "Great. Please enter your 10-digit mobile number."
            return "Please enter a valid name (letters only)."

        elif session_state["step"] == "ask_mobile":
            if re.match(r"^\d{10}$", user_input):
                session_state["mobile"] = user_input
                session_state["step"] = "ask_complaint"
                return "Thank you. Please describe your complaint."
            return "Please enter a valid 10-digit mobile number."

        elif session_state["step"] == "ask_complaint":
            if len(user_input) > 5:
                payload = {
                    "name": session_state["name"],
                    "mobile": session_state["mobile"],
                    "complaint": user_input
                }
                try:
                    response = requests.post(REGISTER_API, json=payload)
                    if response.status_code == 200:
                        session_state.clear()
                        return f"✅ Complaint registered successfully. Your Complaint ID is: {response.json()['complaint_id']}"
                    else:
                        return "❌ Failed to register complaint. Please try again."
                except Exception as e:
                    return f"⚠️ Server error: {e}"
            return "Please describe your complaint in more detail."

    # Handle status flow
    if "status" in lower_input or "track" in lower_input:
        session_state.clear()
        session_state["mode"] = "status"
        session_state["step"] = "ask_query"
        return "Sure, I can help you with that. Please enter your 10-digit mobile number or Complaint ID (e.g., CMP1234)."

    if session_state.get("mode") == "status" and session_state.get("step") == "ask_query":
        query = user_input.strip().upper()
        if re.match(r"^\d{10}$", query) or re.match(r"^CMP\d{4}$", query):
            try:
                resp = requests.get(f"{STATUS_API}/{query}")
                if resp.status_code == 200:
                    data = resp.json()
                    session_state.clear()
                    return (f"🔍 Complaint Details:\n"
                            f"• Complaint ID: {data['complaint_id']}\n"
                            f"• Name: {data['name']}\n"
                            f"• Mobile: {data['mobile']}\n"
                            f"• Complaint: {data['complaint']}\n"
                            f"• Status: {data['status']}")
                return "❌ Complaint not found. Please verify the ID or mobile number."
            except Exception as e:
                return f"⚠️ Could not fetch status due to server error: {e}"
        else:
            return "Please enter a valid 10-digit mobile number or Complaint ID (e.g., CMP1234)."

    return "🤖 I'm here to assist you. You can say 'register a complaint' or 'check complaint status'."
