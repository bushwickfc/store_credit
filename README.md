# Store Credit Assessment
> By @darren

Python script for pulling and processing data related to purchase/use of store credit.

To run this script, use the command

``` sh
python3 store_credit.py
```

Ultimately, it will output a file to this app's root directory named 'revolving_balance.csv'.

### Requirements

This script requires an adjaent local copy of a file named 'credentials.py', which would be written like so:

``` py
username = 'xxx'
password = 'xxx'
database = 'xxx'
hostname = 'xxx'
```

Please contact an IT Committee member for the values to fill in for these variables.

You will also need to install the MySQLdb module:

``` sh
pip install mysqlclient
```