from fpdf import FPDF
from fpdf.enums import XPos, YPos

# Use a Unicode-compatible font like DejaVu (or install one you prefer)
pdf = FPDF()
pdf.add_page()

# Load a proper Unicode font (you can also download 'DejaVuSans.ttf')
pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
pdf.set_font("DejaVu", size=12)

def clean_text(text):
    return (
        text.replace("“", '"')
            .replace("”", '"')
            .replace("‘", "'")
            .replace("’", "'")
            .replace("–", "-")
            .replace("—", "-")
            .replace("…", "...")
    )

content = """
Grievance Registration & Status Chatbot - FAQ

1. How can I register a complaint?
You can simply tell the chatbot what your issue is. It will ask for your name, mobile number, and complaint details, and then register your grievance.

2. What information do I need to provide?
You will be asked for:
- Your full name
- Your mobile number
- A brief description of your complaint

3. What happens after I register my complaint?
The bot will provide you with a Complaint ID and your issue will be stored in the system. You can use this Complaint ID to track your complaint later.

4. How can I check the status of my complaint?
Just say “What’s the status of my complaint?” or something similar. The chatbot will use your mobile number to retrieve your latest complaint status.

5. What are the possible statuses of a complaint?
A complaint can be:
- In Progress
- Resolved
- Closed

6. Can I file multiple complaints?
Yes, but the chatbot will always retrieve the most recent one based on your mobile number.

7. Is my data stored securely?
Yes, all complaint details are securely stored in the database and only used for tracking your issue.

8. I didn’t get my Complaint ID. What should I do?
Please re-register the complaint by talking to the chatbot again, making sure you provide correct details.

This document helps the chatbot answer common user queries using retrieval-based question answering.
"""

for line in content.strip().split("\n"):
    pdf.cell(200, 10, text=clean_text(line.strip()), new_x=XPos.LMARGIN, new_y=YPos.NEXT)

pdf.output("sample_faq.pdf")
