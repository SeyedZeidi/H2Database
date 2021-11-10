#flask run --host=0.0.0.0

from flask import Flask, request
import sqlite3
import json

app = Flask(__name__)

@app.route('/', methods=['POST'])
def result():
    print(request.json)
    addDb(request.json)
    return 'done'

def addDb(data):
    obj = json.loads(data)
    con = sqlite3.connect('result.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS results (TIMESTAMP string, TA1 real, TA2 real, TA1_2 real, TAP real, TB1 real, TB2 real, TB1_2 real, TBP real, TC1 real, TC2 real, TC1_2 real, TCP real, TD1 real, TD2 real, TD1_2 real, TDP real,
              flow_1 real, flow_2 real, flow_3 real, flow_H2)''')
    cur.execute("INSERT INTO results VALUES (:TIMESTAMP, :TA1, :TA2, :TA1_2, :TAP, :TB1, :TB2, :TB1_2, :TBP, :TC1, :TC2, :TC1_2, :TCP, :TD1, :TD2, :TD1_2, :TDP, :flow_1, :flow_2, :flow_3, :flow_H2)", obj)
    con.commit()
    #p = cur.execute('''SELECT * FROM results''')
    #for row in p:
    #    print(row)
    con.close()

#run the app
if __name__ == "__main__":
        app.run(debug=True, host="0.0.0.0")