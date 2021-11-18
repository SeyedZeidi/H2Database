import subprocess
import sys
import send

payload = [2,6,54,4,3,23,5,6,7,8,4,6,4,5,5,7,3,4,2,4]
payload2 = [str(x) for x in payload]

send.iothub_client_telemetry_sample_run(payload)


