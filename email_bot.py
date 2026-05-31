import imaplib
import email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
# Set up your email credentials
EMAIL_ADDRESS = ""
# Put the 16-character app password here (without spaces)
APP_PASSWORD = "" 
IMAP_SERVER = ""


while True:
    # Connect to the Gmail IMAP server securely using SSL
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)

    # Login to your email account
    mail.login(EMAIL_ADDRESS, APP_PASSWORD)

    # If no errors happen, print a success message
    print("Logged in successfully!")

    # Select the inbox folder
    mail.select("INBOX")

    # Search for unread emails using the "UNSEEN" criteria
    status, messages = mail.search(None, "UNSEEN")

    # Print the results
    print("Search Status:", status)
    print("Messages found:", messages)

    # 'messages' is a list like [b'1 2 3'], we get the first item and split it into a list of individual IDs
    email_ids = messages[0].split()

    if email_ids:
        # Let's get the latest email (the last ID in the list)
        latest_email_id = email_ids[-1]
        
        # Fetch the raw email data using the ID
        # "(RFC822)" is the standard format used to fetch the entire email message
        status, msg_data = mail.fetch(latest_email_id, "(RFC822)")
        
        # msg_data contains a lot of things, we loop through it to find the actual content
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                # Convert the raw bytes into a readable email object
                msg = email.message_from_bytes(response_part[1])
                
                # Extract the Subject and Sender
                subject = msg["Subject"]
                sender = msg["From"]
                
                print(f"From: {sender}")
                print(f"Subject: {subject}")
                # Check if the email has multiple parts (text, HTML, attachments)
                if msg.is_multipart():
                    # Loop through all the parts of the email
                    for part in msg.walk():
                        # Look for the plain text part
                        if part.get_content_type() == "text/plain":
                            # Extract the body and decode it into a readable string
                            body = part.get_payload(decode=True).decode()
                            print(f"Body:\n{body}")
                else:
                    # If it's just a simple text email (not multipart)
                    body = msg.get_payload(decode=True).decode()
                    print(f"Body:\n{body}")

            if "price" in body.lower():
                reply_message = "The price is 100$"
            elif "issue" in body.lower():
                reply_message = "Can you give us more details?"
            else:
                reply_message = "Thanks for your message"
                
            print(f"Message classified! Reply will be: {reply_message}")

            # 2. Sending the Reply (SMTP)
            # Create the email message container
            msg_reply = MIMEMultipart()

            # Set the sender, recipient, and subject
            msg_reply['From'] = EMAIL_ADDRESS
            msg_reply['To'] = sender
            msg_reply['Subject'] = "Automated Reply: We received your message"

            # Add the reply message body that we generated from the if conditions
            msg_reply.attach(MIMEText(reply_message, 'plain'))

            # Connect to the SMTP server to send the email
            try:
                # Use port 587 for TLS connection
                server = smtplib.SMTP("smtp.gmail.com", 587)
                
                # Secure the connection (upgrades the connection to be encrypted like SSL)
                server.starttls() 
                
                # Login using your credentials
                server.login(EMAIL_ADDRESS, APP_PASSWORD)
                
                # Send the email
                server.send_message(msg_reply)
                print("Reply sent successfully to:", sender)
                
                # Close the connection
                server.quit()
                
            except Exception as e:
                print(f"Error sending email: {e}")
    else:
        print("No unread emails found.")
    
    # Wait for 5 minutes before checking again
    time.sleep(10)
