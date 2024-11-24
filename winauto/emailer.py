import imaplib
import email
from email.header import decode_header
from lxml import html
import csv 

class Emailer:
    def __init__(self, username, app_password, sender) -> None:
        self.username = username
        self.password = app_password
        self.sender = sender 
        
    def get_verification_code(self):
        verification_code = "no matching"
        # Connect to Gmail's IMAP server
        imap = imaplib.IMAP4_SSL("imap.gmail.com")

        try:
            # Log in
            imap.login(self.username, self.password)

            # Select the mailbox you want to use (inbox by default)
            imap.select("inbox")

            sender_email = self.sender

            # Search for all emails
            # status, messages = imap.search(None, f'FROM "{sender_email}"')
            status, messages = imap.search(None, "ALL")

            # Get the list of email IDs
            email_ids = messages[0].split()

            # Fetch the latest 5 emails (you can adjust the range)
            for email_id in email_ids[-5:]:
                res, msg = imap.fetch(email_id, "(RFC822)")

                for response_part in msg:
                    if isinstance(response_part, tuple):
                        # Parse the email content
                        msg = email.message_from_bytes(response_part[1])

                        # Decode email subject
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            # Convert to string
                            subject = subject.decode(encoding if encoding else "utf-8")

                        # Decode sender
                        from_ = msg.get("From")

                        print(f"Subject: {subject}")
                        print(f"From: {from_}")

                        # If the email has a body, fetch it
                        if msg.is_multipart():
                            for part in msg.walk():
                                content_type = part.get_content_type()
                                content_disposition = str(part.get("Content-Disposition"))

                                try:
                                    # Get the email body
                                    if content_type == "text/html" and "attachment" not in content_disposition:
                                        body = part.get_payload(decode=True).decode()
                                        tree = html.fromstring(body)
                                        # # Extract the verification code
                                        verification_code = tree.cssselect("table[role=presentation]")[0].cssselect("a")[0].get("href")
                                        # print(f"Code:\n{verification_code}")
                                        break
                                except Exception as e:
                                    print("Error decoding body:", e)
                        else:
                            # Handle single-part emails
                            body = msg.get_payload(decode=True).decode()

                        print("=" * 50)

            # Close the connection
            imap.close()
            imap.logout()
            return verification_code
        except imaplib.IMAP4.error as e:
            print(f"IMAP error: {e}")
            return "Getting verification code error"
    
if __name__ == '__main__':
    emailer = Emailer("awuxepopoy77@gmail.com", "jjjjohyakawabkma", "")
    emailer.get_verification_code()

