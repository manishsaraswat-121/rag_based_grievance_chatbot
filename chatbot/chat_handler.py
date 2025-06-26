import re
import requests
from chatbot.rag_chatbot import query_rag

REGISTER_API = "https://rag-based-grievance-chatbot.onrender.com/complaints"
STATUS_API = "https://rag-based-grievance-chatbot.onrender.com/complaints/{complaint_id}"

def get_bot_response(user_input: str, session_state: dict) -> str:
    user_input = user_input.strip()
    lower_input = user_input.lower()
    greetings = ["hi", "hlo", "hello", "hey", "good morning", "good evening"]

    # Greeting
    if any(greet in lower_input for greet in greetings):
        return ("\U0001F44B Hello! I’m your grievance assistant bot.\n"
                "You can say things like:\n"
                "• 'I want to register a complaint'\n"
                "• 'What’s the status of my complaint?'\n"
                "How may I help you today?")
    # Status inquiry
    if "status" in lower_input or "track" in lower_input or "query" in lower_input:
        session_state.clear()
        session_state["mode"] = "status"
        session_state["step"] = "ask_query"
        return "Sure, I can help you with that. Please enter your Complaint ID (e.g., CMP1234)."

    # Register complaint
    if 'register' in lower_input or (
    'complaint' in lower_input and
    'track' not in lower_input and
    'query' not in lower_input and
    'status' not in lower_input
    ):
        session_state.clear()
        session_state["mode"] = "register"
        session_state["step"] = "ask_name"
        return "Sure! Let's register your complaint. What's your full name?"

    if session_state.get("mode") == "register":
        if session_state["step"] == "ask_name":
            if user_input.replace(" ", "").isalpha():
                session_state["name"] = user_input.strip().title()
                session_state["step"] = "ask_mobile"
                return "Great. Please enter your 10-digit mobile number."
            return "Please enter a valid name (letters only)."

        elif session_state["step"] == "ask_mobile":
            if re.fullmatch(r"^\d{10}$", user_input):
                session_state["phone_number"] = user_input.strip()
                session_state["step"] = "ask_email"
                return "Thanks. What's your email address?"
            return "Please enter a valid 10-digit mobile number."

        elif session_state["step"] == "ask_email":
            if re.fullmatch(r"^[\w\.-]+@[\w\.-]+\.\w+$", user_input):
                session_state["email"] = user_input.strip().lower()
                session_state["step"] = "ask_complaint"
                return "Perfect. Now, please describe your complaint."
            return "Please enter a valid email address."

        elif session_state["step"] == "ask_complaint":
            if len(user_input.strip()) > 5:
                payload = {
                    "name": session_state["name"],
                    "phone_number": session_state["phone_number"],
                    "email": session_state["email"],
                    "complaint_details": user_input.strip()
                }
                try:
                    response = requests.post(REGISTER_API, json=payload)
                    session_state.clear()
                    if response.status_code == 200:
                        complaint_id = response.json().get("complaint_id")
                        return f"✅ Complaint registered successfully. Your Complaint ID is: {complaint_id}"
                    elif response.status_code == 409:
                        existing_id = response.json().get("complaint_id", "UNKNOWN")
                        return f"⚠️ A complaint is already registered with this number. Your Complaint ID is: {existing_id}"
                    else:
                        return f"❌ Failed to register complaint. Server responded with: {response.text}"
                except Exception as e:
                    session_state.clear()
                    return f"⚠️ Server error: {e}"
            return "Please describe your complaint in more detail."

    
    if session_state.get("mode") == "status" and session_state.get("step") == "ask_query":
        query = user_input.strip().upper()
        if re.fullmatch(r"CMP\d{4}", query):
            try:
                resp = requests.get(STATUS_API.replace("{complaint_id}", query))
                print(resp)
                session_state.clear()
                if resp.status_code == 200:
                    # plain text response
                    print(resp.text)
                    return resp.text
                elif resp.status_code == 404:
                    return "❌ Complaint not found. Please verify the ID."
                else:
                    return f"⚠️ Could not fetch status. Server responded with: {resp.text}"
            except Exception as e:
                session_state.clear()
                return f"⚠️ Could not fetch status due to server error: {e}"
        else:
            return "❌ Please enter a valid Complaint ID (e.g., CMP1234)."

    # Fallback to RAG for general queries
    try:
        rag_answer = query_rag(user_input)
        if rag_answer and len(rag_answer.strip()) > 0:
            return f"\U0001F4A1 Here's what I found:\n{rag_answer}"
        return "❓ I'm not sure how to answer that. Could you rephrase your question?"
    except Exception as e:
        return f"⚠️ I couldn’t find an answer using the knowledge base. Error: {e}"
