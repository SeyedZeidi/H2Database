import sqlite3
import requests
import json

con = sqlite3.connect('result.db')
cur = con.cursor()

def menu():
    inp = input("Wilt u de Json lokaal halen of via de url. \nTyp L voor lokaal, U voor url, Q om te sluiten. \n")
    print("Keuze is: " + inp + '\n')
    if (inp == 'l' or inp == 'L'):
        lokaal()
    elif (inp == 'u' or inp == 'U'):
        url()
    elif (inp == 'q' or inp == 'Q'):
        quit()
    else:
        print("Foute keuze, probeer het opnieuw")
        menu()

def lokaal():
    with open('./format.json', encoding='utf-8-sig') as json_file:
        x = json.loads(json_file.read())
    cur.execute('''CREATE TABLE IF NOT EXISTS results (TA1 real, TA2 real, TA1_2 real, TAP real, TB1 real, TB2 real, TB1_2 real, TBP real, TC1 real, TC2 real, TC1_2 real, TCP real, TD1 real, TD2 real, TD1_2 real, TDP real,
              flow_1 real, flow_2 real, flow_3 real, flow_H2)''')
    cur.execute("INSERT INTO results VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", x["TA1"], x["TA2"], x["TA1_2"], x["TAP"], x["TB1"], x["TB2"], x["TB1_2"], x["TBP"], x["TC1"], x["TC2"], x["TC1_2"], x["TCP"], x["TD1"], x["TD2"], x["TD1_2"], x["TDP"], x["flow_1"], x["flow_2"], x["flow_3"], x["flow_H2"])
    con.commit()
    con.close()


def url():
    url_raspberry_pi = ''
    r = requests.get(url_raspberry_pi)
    js = json.loads(r.text)
    cur.execute('''CREATE TABLE IF NOT EXISTS results (TA1 real, TA2 real, TA1_2 real, TAP real, TB1 real, TB2 real, TB1_2 real, TBP real, TC1 real, TC2 real, TC1_2 real, TCP real, TD1 real, TD2 real, TD1_2 real, TDP real,
              flow_1 real, flow_2 real, flow_3 real, flow_H2)''')
    cur.execute("INSERT INTO results2 VALUES (:TA1, :TA2, :TA1_2, :TAP, :TB1, :TB2, TB1_2, :TBP, :TC1, :TC2, :TC1_2, :TCP, :TD1, :TD2, :TD1_2, :TDP, :flow_1, :flow_2, :flow_3, :flow_H2)", js)
    con.commit()
    con.close()

#First function call    
menu()