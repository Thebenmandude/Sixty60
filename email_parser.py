from bs4 import BeautifulSoup
import re
import datetime
import pytz

class EmailParser:
    def __init__(self, email):
        self.email = email

    def get_order_number(self):
        # Get the subject
        subject = self.email['Subject']

        # Get the order number from the subject
        order_number = re.search(r'\b[A-Z0-9]+\b$', subject).group()

        return order_number

    def get_order_details(self,order_number):
        # If the email is multipart
        if self.email.is_multipart():
            # Get the HTML part
            for part in self.email.walk():
                if part.get_content_type() == "text/html":
                    html_content = part.get_payload(decode=True)

        # If the email is not multipart
        else:
            html_content = self.email.get_payload(decode=True)

        # Parse the HTML content
        soup = BeautifulSoup(html_content, "html.parser")

        # Find the order details table
        # order_details_table = soup.find('table', {'class': 'x_MsoNormalTable'})
        tables = soup.find_all('table')
        order_details = []
        order_date = None
        # For each table in the list of tables
        for table in tables:
            # If the table contains "Order Details"
            

            first_row = table.find('tr')
            if 'Order Details' in first_row.text:
                header_rows = table.find_all('tr')
                for item in header_rows:
                    if item.text.__contains__('Delivery Date'):
                        date_string = item.find_all('td')[1].find_all('span')[0].text.strip()
                        order_date = datetime.datetime.strptime(date_string, '%d %B %Y, %H:%M')
                        order_date_string = order_date.strftime('%Y-%m-%d %H:%M')

                        
            if 'Product Details' in first_row.text:
                orderstable = table.find_all('table')
                for item in orderstable:
                    for row in item.find_all('tr'):
                        cells = row.find_all('td')
                        if len(cells) == 4:
                            product_name = cells[0].text.strip()
                            qty = cells[1].text.strip()
                            price_per_item = cells[2].text.strip()
                            total_price = cells[3].text.strip()
                            print(f'Product: {product_name}, Quantity: {qty}, Price per Item: {price_per_item}, Total Price: {total_price}')
                            order_details.append({
                                'order_date':order_date_string,
                                'order_number': order_number,
                                'product_name': product_name,
                                'quantity': qty,
                                'price_per_item': price_per_item,
                                'total_price': total_price
                            })
        # For each row in the table
        # for row in order_details_table.find_all('tr'):
        #     # Get the cells
        #     cells = row.find_all('td')

        #     # If there are 3 cells
        #     if len(cells) == 3:
        #         # Get the product name, quantity, and price
        #         product_name = cells[0].text.strip()
        #         quantity = int(cells[1].text.strip())
        #         price = float(cells[2].text.strip())

        #         # Add the order detail to the list of order details
        #         order_details.append({
        #             'product_name': product_name,
        #             'quantity': quantity,
        #             'price': price
        #         })

        return order_details
