from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os
import json

app = Flask(__name__)
users = {}

# ── Google Sheets Setup ──────────────────────────
def save_to_sheet(data):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
import json
creds_json = json.loads(os.environ["GOOGLE_CREDENTIALS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
    client = gspread.authorize(creds)
    sheet = client.open("WhatsApp Leads").sheet1  # Change sheet name if needed
    sheet.append_row([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        data["phone"],
        data["name"],
        data["service"],
        data["budget"],
        data["deadline"],
    ])

# ── Services Menu ────────────────────────────────
SERVICES = {
    "1": "WhatsApp Bots",
    "2": "AI Chatbots",
    "3": "Website Development",
    "4": "Automation Tools",
    "5": "Custom Python Solutions",
}

def services_menu():
    menu = "Please choose a service by replying with a number:\n\n"
    for num, name in SERVICES.items():
        menu += f"{num}. {name}\n"
    return menu.strip()

# ── Main Route ───────────────────────────────────
@app.route("/")
def home():
    return "WhatsApp Bot is Running!"

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "")
    resp = MessagingResponse()
    msg = resp.message()
    text = incoming_msg.lower()

    if sender not in users:
        users[sender] = {"step": 0}

    step = users[sender]["step"]

    # ── If user is mid-flow, don't interrupt with FAQ ──
    if step > 0:
        handle_flow(msg, sender, incoming_msg, text, step)
        return str(resp)

    # ── FAQ replies (only when step == 0) ──
    if any(word in text for word in ["service", "what do you provide", "provide"]):
        msg.body(
            "We provide:\n"
            "✅ WhatsApp Bots\n"
            "✅ AI Chatbots\n"
            "✅ Website Development\n"
            "✅ Automation Tools\n"
            "✅ Custom Python Solutions\n\n"
            "Type *hello* to get started 👋"
        )
    elif any(word in text for word in ["price", "cost", "pricing"]):
        msg.body(
            "Our pricing depends on project type 😊\n"
            "Basic bots start from ₹5,000.\n"
            "Tell us your requirement for an exact quote.\n\n"
            "Type *hello* to get started 👋"
        )
    elif "contact" in text:
        msg.body("You can contact us here on WhatsApp anytime 😊")

    elif text in ["hello", "hi", "start", "hey"]:
        users[sender] = {"step": 1}
        msg.body("Hi 👋 Welcome!\nWhat is your name?")

    else:
        msg.body(
            "Hello! 👋 I didn't understand that.\n\n"
            "You can ask about:\n"
            "• Our *services*\n"
            "• Our *pricing*\n"
            "• How to *contact* us\n\n"
            "Or type *hello* to get started!"
        )

    return str(resp)


def handle_flow(msg, sender, incoming_msg, text, step):
    name = users[sender].get("name", "there")

    # Step 1 — Save name, show service menu
    if step == 1:
        users[sender]["name"] = incoming_msg.title()
        users[sender]["step"] = 2
        msg.body(
            f"Great to meet you, *{incoming_msg.title()}*! 😊\n\n"
            + services_menu()
        )

    # Step 2 — Save service choice
    elif step == 2:
        if incoming_msg in SERVICES:
            users[sender]["service"] = SERVICES[incoming_msg]
            users[sender]["step"] = 3
            msg.body(f"Nice choice! 👍 What is your *budget* for this project?")
        else:
            msg.body(
                "Please reply with a number (1-5) to choose a service:\n\n"
                + services_menu()
            )

    # Step 3 — Save budget
    elif step == 3:
        users[sender]["budget"] = incoming_msg
        users[sender]["step"] = 4
        msg.body(f"Got it 💰 What is your *deadline* or expected timeline?")

    # Step 4 — Save deadline, store lead
    elif step == 4:
        users[sender]["deadline"] = incoming_msg

        lead = {
            "phone": sender,
            "name": users[sender].get("name"),
            "service": users[sender].get("service"),
            "budget": users[sender].get("budget"),
            "deadline": incoming_msg,
        }

        # Save to Google Sheets
        try:
            save_to_sheet(lead)
            print("✅ Lead saved to Google Sheets")
        except Exception as e:
            print(f"❌ Sheet error: {e}")

        msg.body(
            f"Thank you, *{name}*! 🙌\n"
            "Your details have been submitted successfully.\n"
            "Our team will contact you soon. 🚀"
        )
        users[sender]["step"] = 0
import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)