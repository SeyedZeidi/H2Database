#az iot hub monitor-events --hub-name Iothubh2database --device-id H2Heating

from os import EX_SOFTWARE
import time
from azure.iot.device import IoTHubDeviceClient, Message
import json
import requests
import datetime

#Azure Connection
CONNECTION_STRING = "HostName=Iothubh2database.azure-devices.net;DeviceId=H2Heating;SharedAccessKey=3kDgzO43OJPPRjSEuyFARsF2lBJH8kAm+oo61M/ahaQ="

#local database url
url = "http://192.168.178.139:5000"

#Initialize client
def iothub_client_init():  
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)  
    return client  
 
#json
def get_message():
    a_datetime = datetime.datetime.now()
    formatted_datetime = a_datetime.isoformat()
    payload = [2,6,54,4,3,23,5,6,7,8,4,6,4,5,5,7,3,4,2,4]
    payload2 = {
        "TIMESTAMP":formatted_datetime,
        "TA1":payload[0],
        "TA2":payload[1],
        "TA1_2":payload[2],
        "TAP":payload[3],

        "TB1":payload[4],
        "TB2":payload[5],
        "TB1_2":payload[6],
        "TBP":payload[7],

        "TC1":payload[8],
        "TC2":payload[9],
        "TC1_2":payload[10],
        "TCP":payload[11],

        "TD1":payload[12],
        "TD2":payload[13],
        "TD1_2":payload[14],
        "TDP":payload[15],

        "flow_1":payload[16],
        "flow_2":payload[17],
        "flow_3":payload[18],
        "flow_H2":payload[19]
            }    
    return json.dumps(payload2)

def iothub_client_telemetry_sample_run():  
    try:  
        
        client = iothub_client_init()  
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )  
        while True:
            a_datetime = datetime.datetime.now()
            formatted_datetime = a_datetime.isoformat()
            
            client.connect()
            
            message = Message(get_message())
 
            print("Sending message")  
            
            try: 
                client.send_message(message)  
            except:
                print("sending to iot hub failed")
            else:  
                print ( "Message successfully sent to flask at", formatted_datetime) 
            try:
                requests.post(url, json = get_message())
            except:
                print("sending to flask failed")
            else:  
                print ( "Message successfully sent to iot hub at", formatted_datetime) 
            client.disconnect() 
            time.sleep(5)  
            
    except KeyboardInterrupt:  
        print ( "IoTHubClient sample stopped" )  
 


 
if __name__ == '__main__':  
    print ( "IoT Hub Quickstart #1 - Simulated device" )  
    print ( "Press Ctrl-C to exit" )  
    iothub_client_telemetry_sample_run()