from datetime import date
import time

pexpiry = date(2029,10,23)
today = date.today()

print(pexpiry,today)
if pexpiry>today:
    print("sughalle")
else:
    print("podei")


