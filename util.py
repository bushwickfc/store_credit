import datetime
import json

# Format the datetime as just the date - ex. 2015-04-01
def format_date(date):
	return json.dumps(date, default = datetime_converter)[1:].split(' ')[0]

# Convert the datetime.datetime data from the queries into a string.
# Concept borrowed from https://code-maven.com/serialize-datetime-object-as-json-in-python
def datetime_converter(d):
    if isinstance(d, datetime.datetime):
        return d.__str__()

def calculate_revolving_balance(list):
    output_list = []
    revolving_balance = 0

    for transaction_summary in list:
        revolving_balance += transaction_summary['member_prepay'] - transaction_summary['debt']
        transaction_summary['revolving_balance'] = round(revolving_balance, 2)
        output_list.append(transaction_summary)

    return output_list