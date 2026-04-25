# WhatsApp AI Bot 🤖

Smart WhatsApp chatbot built with **Python, Flask, Twilio, and Google Sheets** for lead generation, customer support, and business automation.

## 🌐 What It Does

This bot can automate WhatsApp conversations for businesses by replying instantly, collecting customer details, and storing leads directly in Google Sheets.

## 🚀 Features

* 👋 Greets users by name
* 📋 Numbered service menu
* 🧠 Smart FAQ replies
* 📥 Collects leads automatically
* 💰 Captures budget & deadline
* 📊 Saves data to Google Sheets
* ⚡ Instant automated responses

## 💼 Ideal For

* Agencies
* Local businesses
* Coaches
* Ecommerce stores
* Service providers

## 🛠️ Tech Stack

* Python
* Flask
* Twilio WhatsApp API
* Google Sheets API
* Render / Ngrok

## 📸 Demo Preview

(Add screenshot here)

## ⚙️ Setup Guide

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Add Google Credentials

* Create Google Cloud Service Account
* Download JSON key
* Rename file to:

```bash
credentials.json
```

* Place inside project root folder

### 3️⃣ Run App

```bash
python app.py
```

### 4️⃣ Connect Twilio Webhook

Use ngrok:

```bash
ngrok http 5000
```

Then set webhook URL:

```bash
https://your-ngrok-url/whatsapp
```

## 🔒 Security

Never upload:

```bash
credentials.json
```

Keep it inside `.gitignore`

## 👨‍💻 Built By

**Piyush Thakkar**

GitHub: https://github.com/piyushthakkar321

Portfolio: https://portfolio-website-seven-chi-27.vercel.app/
