\# WhatsApp Bot 🤖



A WhatsApp chatbot built with Python, Flask, Twilio, and Google Sheets.



\## Features

\- Greets users by name

\- Numbered service menu

\- Collects leads (name, service, budget, deadline)

\- Saves leads to Google Sheets

\- FAQ replies for services, pricing, contact



\## Setup



\### 1. Install dependencies

```bash

pip install -r requirements.txt

```



\### 2. Add credentials.json

\- Create a Google Cloud service account

\- Download the JSON key and rename to `credentials.json`

\- Place it in the project root



\### 3. Run the bot

```bash

python app.py

```



\### 4. Expose with ngrok

```bash

ngrok http 5000

```

Set the ngrok URL as your Twilio webhook:

`https://your-ngrok-url/whatsapp`



\## Environment

Never push `credentials.json` to GitHub. It is in `.gitignore`.

