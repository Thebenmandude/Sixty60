To achieve this, we will need to use several Python libraries such as imaplib and email for connecting to Gmail and retrieving emails, BeautifulSoup for parsing the HTML content of the emails, json for formatting the data into JSON, and azure-kusto-data for writing the data to Azure Data Explorer.

Here are the core classes and functions that will be necessary:

1. GmailClient: This class will be responsible for connecting to Gmail and retrieving the emails. It will have the following methods:
   - __init__: Initializes the GmailClient with the necessary credentials.
   - connect: Connects to Gmail.
   - retrieve_emails: Retrieves all emails with a subject line that contains "Sixty60 invoice".

2. EmailParser: This class will be responsible for parsing the emails and extracting the order information. It will have the following methods:
   - __init__: Initializes the EmailParser with the email to parse.
   - get_order_number: Gets the order number from the subject line.
   - get_order_details: Gets the order details from the HTML content of the email.

3. DataWriter: This class will be responsible for writing the data to a file and to Azure Data Explorer. It will have the following methods:
   - __init__: Initializes the DataWriter with the data to write.
   - write_to_file: Writes the data to a file.
   - write_to_azure: Writes the data to Azure Data Explorer.

Now, let's start with the "entrypoint" file:

main.py
#   S i x t y 6 0  
 