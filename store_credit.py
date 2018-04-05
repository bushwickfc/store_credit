import MySQLdb
import credentials

print('Initializing connection to remote DB...')

db = MySQLdb.connect(credentials.hostname, credentials.username, credentials.password, credentials.database)
cursor_a = db.cursor()
cursor_b = db.cursor()

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

cursor_a.execute(member_prepay_query)
cursor_b.execute(debt_query)

print('Member Prepay results...')

for row in cursor_a:
    print(row)

print('Debt results...')

for row in cursor_b:
    print(row)

db.close()