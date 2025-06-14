import re
import requests

# API endpoints
REGISTER_API_URL = "http://localhost:8000/register"
STATUS_API_URL = "http://localhost:8000/status"

def get_bot_response(user_input, session_state):
    user_input = user_input.strip()
    lower_input = user_input.lower()
    greetings = ["hi", "hello", "hey", "good morning", "good evening"]

    # Greeting
    if any(greet in lower_input for greet in greetings):
        return ("👋 Hello! I’m your grievance assistant bot.\n"
                "You can say things like:\n"
                "• 'I want to register a complaint'\n"
                "• 'What’s the status of my complaint?'\n"
                "How may I help you today?")

    # Handle Complaint Registration Flow
    if "register" in lower_input or "complaint" in lower_input:
        session_state.clear()
        session_state['registering'] = True
        session_state['step'] = 'ask_name'
        return "Sure! Let's register your complaint. What's your full name?"

    if session_state.get("registering"):
        if session_state["step"] == "ask_name":
            if user_input.replace(" ", "").isalpha():
                session_state["name"] = user_input
                session_state["step"] = "ask_mobile"
                return "Thanks! Please enter your 10-digit mobile number."
            else:
                return "❗ Please enter a valid name using only alphabets."

        elif session_state["step"] == "ask_mobile":
            if re.match(r"^\d{10}$", user_input):
                session_state["mobile"] = user_input
                session_state["step"] = "ask_complaint"
                return "Got it. Please describe your complaint."
            else:
                return "❗ Please enter a valid 10-digit mobile number."

        elif session_state["step"] == "ask_complaint":
            if len(user_input) > 5:
                session_state["complaint"] = user_input
                payload = {
                    "name": session_state["name"],
                    "mobile": session_state["mobile"],
                    "complaint": session_state["complaint"]
                }
                try:
                    resp = requests.post(REGISTER_API_URL, json=payload)
                    if resp.status_code == 200:
                        data = resp.json()
                        session_state.clear()
                        return f"✅ Complaint registered successfully!\nYour Complaint ID is: {data['complaint_id']}"
                    else:
                        return "❌ Error while registering your complaint. Please try again."
                except Exception as e:
                    return f"⚠️ Could not connect to server: {e}"
            else:
                return "❗ Please describe your complaint in more detail."

    # Handle Complaint Status Check Flow
    if "status" in lower_input or "track" in lower_input:
        session_state.clear()
        session_state["checking_status"] = True
        session_state["step"] = "ask_identifier"
        return "Sure! Please provide either your **Complaint ID** (e.g., CMP1234) or your **registered mobile number**."

    if session_state.get("checking_status") and session_state["step"] == "ask_identifier":
        input_val = user_input.strip()

        # Validate as Complaint ID
        if re.match(r'^CMP\d{4}$', input_val.upper()):
            complaint_id = input_val.upper()
            try:
                resp = requests.get(f"{STATUS_API_URL}/{complaint_id}")
                if resp.status_code == 200:
                    data = resp.json()
                    session_state.clear()
                    return (f"📋 Complaint Details:\n"
                            f"• Complaint ID: {data['complaint_id']}\n"
                            f"• Name: {data['name']}\n"
                            f"• Mobile: {data['mobile']}\n"
                            f"• Complaint: {data['complaint']}\n"
                            f"• Status: {data['status']}")
                else:
                    return "❌ No complaint found with this Complaint ID. Please try again."
            except Exception as e:
                return f"⚠️ Server error: {e}"

        # Validate as Mobile Number
        elif re.match(r'^\d{10}$', input_val):
            try:
                resp = requests.get(f"{STATUS_API_URL}?mobile={input_val}")
                if resp.status_code == 200:
                    records = resp.json()
                    if records:
                        result = ["📋 Complaints linked to this mobile:\n"]
                        for data in records:
                            result.append(
                                f"• Complaint ID: {data['complaint_id']}\n"
                                f"  Complaint: {data['complaint']}\n"
                                f"  Status: {data['status']}\n"
                            )
                        session_state.clear()
                        return "\n".join(result)
                    else:
                        return "❌ No complaints found for this number."
                else:
                    return "❌ Could not fetch complaints. Try again."
            except Exception as e:
                return f"⚠️ Server error: {e}"

        else:
            return "❗ Please enter a valid 10-digit mobile number or Complaint ID (e.g., CMP1234)."

    return ("🤖 I'm here to assist you. You can say things like:\n"
            "• 'Register a complaint'\n"
            "• 'Check complaint status'\n"
            "How may I help you today?")
