import MySQLdb
import csv
from operator import itemgetter
import credentials
import util

print('Initializing connection to remote DB...')

db = MySQLdb.connect(credentials.hostname, credentials.username, credentials.password, credentials.database)
prepay_cursor = db.cursor()
debt_cursor = db.cursor()

# Get every transaction where a member purchased store credit as DATE and TOTAL
member_prepay_query = """SELECT r.DATENEW AS DATE, (tl.UNITS * tl.PRICE) AS TOTAL
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

db.close()

# Use the transaction_dict to combine transactions based on date - so multiple
# transactions on the same date will get 'squashed' into a single date key.
transaction_dict = {}
# The transaction_dict will be iterated over and the items will be pushed into the
# transaction_list to be sorted by date.
transaction_list = []

for row in prepay_cursor:
    date = util.format_date(row[0])
    amount = round(row[1], 2)

    if date in transaction_dict:
        transaction_dict[date]['member_prepay'] += amount
    else:
        transaction_dict[date] = {
            'date': date,
            'member_prepay': amount,
            'debt': 0,
        }

for row in debt_cursor:
    date = util.format_date(row[0])
    amount = round(row[1], 2)

    if date in transaction_dict:
        transaction_dict[date]['debt'] += amount
    else:
        transaction_dict[date] = {
            'date': date,
            'member_prepay': 0,
            'debt': amount
        }

# Now that the transactions have been 'squashed' by date, push them into a list to be sorted
for key in transaction_dict:
    transaction_list.append(transaction_dict[key])

# Sort the list by date
sorted_transaction_list = sorted(transaction_list, key = itemgetter('date'))

# Prepare to export the final list, in which each dict will have an additional 'revolving_balance' key
to_csv = util.calculate_revolving_balance(sorted_transaction_list)
keys = to_csv[0].keys()

print('Writing results to \'revolving_balance.csv\'...')

with open('revolving_balance.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(to_csv)

print("Done!")