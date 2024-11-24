import imaplib
import email

# Outlook IMAP server settings
IMAP_SERVER = 'outlook.office365.com'
EMAIL_ACCOUNT = 'teclelatul@outlook.com'
PASSWORD = 'YCaQIjwS1RYLw'

def read_outlook_mail():
    # Connect to the Outlook IMAP server
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, PASSWORD)

    # Select the inbox
    mail.select("inbox")

    # Search for all emails
    status, email_ids = mail.search(None, 'ALL')
    email_ids = email_ids[0].split()

    # Fetch and display the most recent emails
    print("Your latest emails:")
    for eid in email_ids[-5:]:  # Fetch the last 5 emails
        status, data = mail.fetch(eid, '(RFC822)')
        message = email.message_from_bytes(data[0][1])

        print(f"From: {message['From']}")
        print(f"Subject: {message['Subject']}")
        print('-' * 50)

    mail.logout()

if __name__ == "__main__":
    read_outlook_mail()