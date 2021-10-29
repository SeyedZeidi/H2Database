import os
import sqlite3
import requests
import json

url_raspberry_pi = ''
con = sqlite3.connect('result.db')

cur = con.cursor()
payload = {}
#r = requests.get(url_raspberry_pi)
#js = json.loads(r.text)
#js["TA1"]
#print(r.url)
x = '{"TA1":33.33, "TA2":55.55}'
payload = ["0", "1", "2", "3","4", "5", "6","7", "8", "9","10", "12", "13","14", "15", "16","17", "18", "19"]
# Create table
#cur.execute('''CREATE TABLE results
#               (TA1 real, TA2 real, TA1_2 real, TAP real, TB1 real, TB2 real, TB1_2 real, TBP real, TC1 real, TC2 real, TC1_2 real, TCP real, TD1 real, TD2 real, TD1_2 real, TDP real,
#               flow_1 real, flow_2 real, flow_3 real, flow_H2)''')

# Insert a row of data
#cur.execute("SELECT*")

cur.execute("INSERT INTO results VALUES (payload[0],payload[1],payload[2],payload[3],payload[4],payload[5],payload[6],payload[7],payload[8],payload[9],payload[10],payload[11],payload[12],payload[13],payload[14],payload[15],payload[16],payload[17],payload[18],payload[19])")

# Save (commit) the changes
con.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
con.close()