import MySQLdb
import datetime
import json
from operator import itemgetter
import credentials

print('Initializing connection to remote DB...')

# Convert the datetime.datetime data from the queries into a string.
# Concept borrowed from https://code-maven.com/serialize-datetime-object-as-json-in-python
def datetime_converter(d):
    if isinstance(d, datetime.datetime):
        return d.__str__()

db = MySQLdb.connect(credentials.hostname, credentials.username, credentials.password, credentials.database)
prepay_cursor = db.cursor()
debt_cursor = db.cursor()

# Get every transaction where a member purchased store credit as DATE and TOTAL
member_prepay_query = """SELECT r.DATENEW AS DATE,
                         (tl.UNITS * tl.PRICE) AS TOTAL
                         FROM RECEIPTS r 
                         JOIN TICKETS t on r.ID = t.ID 
                         JOIN TICKETLINES tl on tl.TICKET = t.ID 
                         JOIN PRODUCTS p on tl.PRODUCT = p.ID 
                         WHERE (p.NAME LIKE "%MEMBER PREPAY%");"""

# Get every transaction where a member used store credit as DATE and TOTAL
debt_query = """SELECT r.DATENEW AS DATE, TOTAL
                FROM RECEIPTS r
                JOIN PAYMENTS p on p.RECEIPT = r.ID 
                WHERE p.PAYMENT="debt";"""

prepay_cursor.execute(member_prepay_query)
debt_cursor.execute(debt_query)

# Use the transaction_dict to combine transactions based on date - so multiple
# transactions will get 'squashed' into a single date key.
transaction_dict = {}
# The transaction_dict will be iterated over and the items will be pushed into the
# transaction_list to be sorted by date.
transaction_list = []

for row in prepay_cursor:
    date = json.dumps(row[0], default = datetime_converter)[1:].split(' ')[0]

    if date in transaction_dict:
        transaction_dict[date]['member_prepay'] += row[1]
    else:
        transaction_dict[date] = {
            'member_prepay': row[1],
            'debt': 0
        }

for row in debt_cursor:
    date = json.dumps(row[0], default = datetime_converter)[1:].split(' ')[0]

    if date in transaction_dict:
        transaction_dict[date]['debt'] += row[1]
    else:
        transaction_dict[date] = {
            'member_prepay': 0,
            'debt': row[1]
        }

for key in transaction_dict:
    transaction_dict[key]['date'] = key
    transaction_list.append(transaction_dict[key])

sorted_transaction_list = sorted(transaction_list, key = itemgetter('date'))

db.close()