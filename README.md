# 📧 Email Automation Assistant

An automated email bot built with Python that monitors a Gmail inbox for unread messages, classifies them based on content, and sends appropriate auto-replies.

## Features

- **Automatic Inbox Monitoring** — Continuously polls your Gmail inbox for new unread emails using IMAP.
- **Smart Classification** — Categorizes incoming emails based on keywords:
  | Keyword Detected | Auto-Reply |
  |---|---|
  | `price` | "The price is 100$" |
  | `issue` | "Can you give us more details?" |
  | *(anything else)* | "Thanks for your message" |
- **Auto-Reply via SMTP** — Sends a contextual reply back to the sender automatically.
- **Polling Loop** — Checks for new emails at a configurable interval (default: every 10 seconds for testing).

## Prerequisites

- **Python 3.8+**
- A **Gmail account** with:
  - [2-Step Verification](https://myaccount.google.com/signinoptions/two-step-verification) enabled
  - A [16-character App Password](https://myaccount.google.com/apppasswords) generated for this bot

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/email-automation-assistant.git
   cd email-automation-assistant
   ```

2. **Configure credentials:**

   Create a `.env` file (recommended) or update the variables directly in `email_bot.py`:
   ```
   EMAIL_ADDRESS=your-email@gmail.com
   APP_PASSWORD=your-16-char-app-password
   ```

   > ⚠️ **Never commit your real credentials.** Use environment variables or a `.env` file and add it to `.gitignore`.

3. **Install dependencies:**

   This project uses only Python standard library modules — no extra packages required.

4. **Run the bot:**
   ```bash
   python email_bot.py
   ```

## How It Works

```
┌──────────────┐     IMAP/SSL     ┌───────────┐
│  Gmail Inbox │ ◄──────────────► │ email_bot  │
└──────────────┘                  │            │
                                  │ 1. Fetch   │
                                  │ 2. Classify│
                                  │ 3. Reply   │
┌──────────────┐     SMTP/TLS     │            │
│   Sender     │ ◄──────────────► │            │
└──────────────┘                  └───────────┘
```

1. Connects to Gmail via **IMAP SSL** and logs in.
2. Searches for **unread (UNSEEN)** emails in the inbox.
3. Fetches the latest unread email and extracts the **subject**, **sender**, and **body**.
4. Classifies the email content using keyword matching.
5. Constructs and sends an auto-reply via **SMTP TLS**.
6. Waits for the configured interval, then repeats.

## Project Structure

```
Email automation assistant/
├── email_bot.py    # Main bot script
├── .gitignore      # Git ignore rules
└── README.md       # This file
```

## Security Notes

- **Do not** commit your app password or email credentials to version control.
- Use environment variables or a `.env` file to manage secrets.
- The `.gitignore` in this repo is pre-configured to exclude `.env` files.

## Future Improvements

- [ ] Load credentials from environment variables / `.env` file
- [ ] Add logging instead of `print()` statements
- [ ] Support more advanced classification (regex, NLP, or AI-based)
- [ ] Handle HTML-only emails gracefully
- [ ] Add rate limiting and error retry logic
- [ ] Support multiple email accounts

## License

This project is for educational and personal use.
