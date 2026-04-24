from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Temporary in-memory storage for user conversations
# Format:
# users = {
#   "whatsapp:+91xxxxxxxxxx": {
#       "step": 1,
#       "name": "Piyush",
#       "service": "Logo Design",
#       "budget": "5000",
#       "deadline": "3 days"
#   }
# }
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

    # New user setup
    if sender not in users:
        users[sender] = {"step": 0}

    step = users[sender]["step"]
    text = incoming_msg.lower()

    # Start conversation
    if text in ["hello", "hi", "start"]:
        users[sender] = {"step": 1}
        msg.body("Hi 👋 Welcome!\nWhat is your name?")

    # Step 1: Name
    elif step == 1:
        users[sender]["name"] = incoming_msg
        users[sender]["step"] = 2
        msg.body("Great 😊 What service do you need?")

    # Step 2: Service
    elif step == 2:
        users[sender]["service"] = incoming_msg
        users[sender]["step"] = 3
        msg.body("Nice 👍 What is your budget?")

    # Step 3: Budget
    elif step == 3:
        users[sender]["budget"] = incoming_msg
        users[sender]["step"] = 4
        msg.body("Perfect 💼 What is your deadline?")

    # Step 4: Deadline + Summary
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

        # Reset conversation
        users[sender]["step"] = 0

    # Unknown input
    else:
        msg.body("Please type Hello to begin 😊")

    return str(resp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)