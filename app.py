#Hoe gebruik je sqlite3?
# $ sqlite3
# $ .open result.db
# $ .tables
# $ .header on
# $ .mode column
# $ pragma table_info('results');
# https://www.sqlitetutorial.net/sqlite-tutorial/sqlite-describe-table/
import sqlite3
import json
import urllib.request

con = sqlite3.connect('result.db')
cur = con.cursor()

def menu():
    inp = input("Wilt u de Json lokaal halen of via de url. \nTyp L voor lokaal, U voor url of Q om te sluiten. \n")
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
              flow_1 real, flow_2 real, flow_3 real, flow_H2 real)''')
    cur.execute("INSERT INTO results VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [x["TA1"], x["TA2"], x["TA1_2"], x["TAP"], x["TB1"], x["TB2"], x["TB1_2"], x["TBP"], x["TC1"], x["TC2"], x["TC1_2"], x["TCP"], x["TD1"], x["TD2"], x["TD1_2"], x["TDP"], x["flow_1"], x["flow_2"], x["flow_3"], x["flow_H2"]])
    p = cur.execute('''SELECT * FROM results''')
    for row in p:
        print(row)
    con.commit()
    con.close()

def url():
    print("1")
    url = 'http://H2smart.local' #vind het goeie adres, want dit pakt nu de frontend html code 
    print("2")
    #r = requests.get(url_raspberry_pi)
    data = urllib.request.urlopen(url).read().decode()
    print("3")
    print(data)
    obj = json.loads(data)
    print("4")
    print(obj)
    #js = json.loads(r.text)
    print("5")
    cur.execute('''CREATE TABLE IF NOT EXISTS results (TA1 real, TA2 real, TA1_2 real, TAP real, TB1 real, TB2 real, TB1_2 real, TBP real, TC1 real, TC2 real, TC1_2 real, TCP real, TD1 real, TD2 real, TD1_2 real, TDP real,
              flow_1 real, flow_2 real, flow_3 real, flow_H2)''')
    cur.execute("INSERT INTO results VALUES (:TA1, :TA2, :TA1_2, :TAP, :TB1, :TB2, :TB1_2, :TBP, :TC1, :TC2, :TC1_2, :TCP, :TD1, :TD2, :TD1_2, :TDP, :flow_1, :flow_2, :flow_3, :flow_H2)", obj)
    print("6")
    con.commit()
    con.close()

#First function call    
menu()