import time
import sys
import datetime
import json


# pylint: disable=E0611
from azure.iot.device import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult, Message
from azure.iot.device import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue

# The device connection string to authenticate the device with your IoT hub.
# Using the Azure CLI:
# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
CONNECTION_STRING = "HostName=Iothubh2database.azure-devices.net;DeviceId=H2Heating;SharedAccessKey=3kDgzO43OJPPRjSEuyFARsF2lBJH8kAm+oo61M/ahaQ="

# Using the MQTT protocol.
PROTOCOL = IoTHubTransportProvider.MQTT
MESSAGE_TIMEOUT = 10000


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

def send_confirmation_callback(message, result, user_context):
    print ( "IoT Hub responded to message with status: %s" % (result) )

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
    return client

def iothub_client_telemetry_sample_run():

    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )

        while True:
            # Build the message with simulated telemetry values.

            # Add a custom application property to the message.
            # An IoT hub can filter on these properties without access to the message body.
            message = Message(get_message())
            # Send the message.
            #print( "Sending Message")
            client.send_event_async(message, send_confirmation_callback, None)
            time.sleep(300)

    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    print ( "IoT Hub Quickstart #1 - Simulated device" )
    print ( "Press Ctrl-C to exit" )
    iothub_client_telemetry_sample_run()