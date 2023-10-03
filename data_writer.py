import json
import datetime
import csv
import io
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder

def datetime_serializer(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError(f"Type not serializable: {type(obj)}")

class DataWriter:
    def __init__(self, order_number, order_details):
        self.order_number = order_number
        self.order_details = order_details

    def write_to_file(self):
        # Format the data into a JSON object
        data = {
            'order_number': self.order_number,
            'order_details': self.order_details,
            'timestamp': datetime.datetime.utcnow()  # Convert the datetime object to a string
        }

        # Write the JSON object to a file
        with open(f'{self.order_number}.json', 'w') as f:
            json.dump(data, f, default=datetime_serializer)

    def write_to_azure(self):
        kcsb = KustoConnectionStringBuilder("http://localhost:8080")
        client = KustoClient(kcsb)

        # Create a string buffer
        output = io.StringIO()

        # Create a CSV writer object
        writer = csv.writer(output)

        # Write data rows
        for item in self.order_details:
            writer.writerow(item.values())

        # Get the CSV data as a string
        csv_string = output.getvalue()

        # Don't forget to close the StringIO object once you're done with it
        output.close()
        # Write the data to Azure Data Explorer
        client.execute('NetDefaultDB', f'.ingest inline into table raw_Sixty60Orders with(format ="csv") <| {csv_string}')

# Usage:
# data_writer = DataWriter(order_number, order_details)
# data_writer.write_to_file()
# data_writer.write_to_azure()

# Kusto Create Table
# .create table raw_Sixty60Orders (
#     order_date: datetime,
#     order_number: string,
#     product_name: string,
#     quantity: string,
#     price_per_item: string,
#     total_price: string
# )