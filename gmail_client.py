import imaplib
import email
from email.header import decode_header

class GmailClient:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.mail = None

    def connect(self):
        # Connect to Gmail
        self.mail = imaplib.IMAP4_SSL("imap.gmail.com")
        self.mail.login(self.username, self.password)

    def retrieve_emails(self):
        # Select the mailbox you want to delete in
        self.mail.select("inbox")

        # Search for specific mail by sender
        result, data = self.mail.uid('search', None, '(HEADER Subject "Sixty60 invoice")')

        # If there is no data, return an empty list
        if not data[0]:
            return []

        # Get the list of mail IDs
        mail_ids = data[0].split()

        # Initialize the list of emails
        emails = []

        # For each mail ID
        for mail_id in mail_ids:
            # Fetch the mail
            result, data = self.mail.uid('fetch', mail_id, '(BODY.PEEK[])')

            # Parse the raw email
            raw_email = data[0][1].decode("utf-8")
            email_message = email.message_from_string(raw_email)

            # Add the email to the list of emails
            emails.append(email_message)

        return emails
