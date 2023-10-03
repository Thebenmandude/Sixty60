from gmail_client import GmailClient
from email_parser import EmailParser
from data_writer import DataWriter

def main():
    # Initialize the Gmail client
    gmail_client = GmailClient('thebenmandude@gmail.com', 'zgzr hnoe xsmr gcra')

    # Connect to Gmail
    gmail_client.connect()

    # Retrieve the emails
    emails = gmail_client.retrieve_emails()

    # For each email
    for email in emails:
        # Initialize the email parser
        email_parser = EmailParser(email)

        # Get the order number
        order_number = email_parser.get_order_number()

        # Get the order details
        order_details = email_parser.get_order_details(order_number)

        # Initialize the data writer
        data_writer = DataWriter(order_number, order_details)

        # Write the data to a file
        data_writer.write_to_file()

        # Write the data to Azure Data Explorer
        data_writer.write_to_azure()

if __name__ == "__main__":
    main()
