from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Stores user progress
users = {}

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

    # Create user if new
    if sender not in users:
        users[sender] = {"step": 0}

    step = users[sender]["step"]

    # ---------------- FAQ REPLIES ----------------
    if "service" in text or "what do you provide" in text:
        msg.body(
            "We provide:\n"
            "✅ WhatsApp Bots\n"
            "✅ AI Chatbots\n"
            "✅ Website Development\n"
            "✅ Automation Tools\n"
            "✅ Custom Python Solutions\n\n"
            "What service do you need?"
        )
        return str(resp)

    elif "price" in text or "cost" in text or "pricing" in text:
        msg.body(
            "Our pricing depends on project type 😊\n"
            "Basic bots start from ₹5,000.\n"
            "Tell us your requirement for exact quote."
        )
        return str(resp)

    elif "contact" in text:
        msg.body(
            "You can contact us here on WhatsApp anytime 😊"
        )
        return str(resp)

    # ---------------- LEAD FLOW ----------------
    if text in ["hello", "hi", "start"]:
        users[sender] = {"step": 1}
        msg.body("Hi 👋 Welcome!\nWhat is your name?")

    elif step == 1:
        users[sender]["name"] = incoming_msg
        users[sender]["step"] = 2
        msg.body("Great 😊 What service do you need?")

    elif step == 2:
        users[sender]["service"] = incoming_msg
        users[sender]["step"] = 3
        msg.body("Nice 👍 What is your budget?")

    elif step == 3:
        users[sender]["budget"] = incoming_msg
        users[sender]["step"] = 4
        msg.body("Perfect 💼 What is your deadline?")

    elif step == 4:
        users[sender]["deadline"] = incoming_msg

        summary = f"""
✅ NEW CLIENT LEAD

Name: {users[sender]['name']}
Service: {users[sender]['service']}
Budget: {users[sender]['budget']}
Deadline: {users[sender]['deadline']}
Phone: {sender}
"""
        print(summary)

        msg.body(
            "Thank you 🙌\n"
            "Your details have been submitted successfully.\n"
            "Our team will contact you soon."
        )

        users[sender]["step"] = 0

    else:
        msg.body("Please type Hello to begin 😊")

    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)