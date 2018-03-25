import time
from datetime import datetime
import requests

from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration

def get_listeners_number():
    resp = requests.get("http://radio.mipt.ru:8410/status-json.xsl")
    try:
        return resp.json()["icestats"]["source"]["listeners"]
    except:

        return 0

def publish_callback(result, status):
#     print("Successfully sent")
    pass

period_in_seconds = 5  # cant be less than 3 (free trial)

if len(sys.argv) < 3:
	print("Not enough arguments")
	exit()

# pubnub keys
publish_key = sys.argv[1]
subscribe_key = sys.argv[2]

channel_name = 'radiostream_listeners'


pnconfig = PNConfiguration()

pnconfig.subscribe_key = subscribe_key
pnconfig.publish_key = publish_key
pubnub = PubNub(pnconfig)

print("Start to publish number of listeners")
while True:
    listeners_number = get_listeners_number()
    timestamp = int(datetime.now().timestamp() * 1000)

    data_to_send = dict(time=timestamp, y=listeners_number)
    pubnub.publish().channel(channel_name).message(data_to_send).async(publish_callback)

    time.sleep(period_in_seconds)
