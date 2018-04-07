# Store Credit Assessment
> Author @darren

Python script for pulling and processing data related to purchase/use of store credit, calculating the revolving balance, and outputting a .csv summary.

To run this script, use the command

``` sh
python3 store_credit.py
```

## Overview

This script will query for two datasets:
- Dates and totals of customer purchases of 'Member Prepay Payment'
- Dates and totals of customer use of 'debt' payment type

The returned data will be combined into one date-ordered dataset, and then used to calculate the revolving balance of store credit.

Ultimately, it will output a file to this app's root directory named 'revolving_balance.csv'.

## Requirements

This script requires an adjacent local copy of a file named 'credentials.py', which would be written like so:

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

### Notes

At the time of publishing, the author is not 100% confident that the data returned by the queries is exactly what we want - it is possible that the meaning and application of the 'debt' payment type (on the PAYMENTS table) has changed over time, or is more encompassing than initially thought. The queries (or our understanding of the data) may need to evolve.