from base64 import b64encode, b64decode
from hashlib import sha256
from urllib import parse
from hmac import HMAC

import uamqp
import uuid
import urllib
import json
import os
import pandas
import random
import time

iot_hub_name = "lab11abakumova"
hostname = "lab11abakumova.azure-devices.net"
device_id = "device_iot_abakumova"
username = "device_iot_abakumova@sas.lab11abakumova"
access_key = os.getenv('ACCESS_KEY')


def generate_sas_token(uri, key, policy_name, expiry=3600):
    ttl = time.time() + expiry
    sign_key = "%s\n%d" % ((parse.quote_plus(uri)), int(ttl))
    print(sign_key)
    signature = b64encode(HMAC(b64decode(key), sign_key.encode('utf-8'), sha256).digest())

    rawtoken = {
        'sr': uri,
        'sig': signature,
        'se': str(int(ttl))
    }

    if policy_name is not None:
        rawtoken['skn'] = policy_name

    return 'SharedAccessSignature ' + parse.urlencode(rawtoken)


if __name__ == '__main__':
    sas_token = generate_sas_token('{hostname}/devices/{device_id}'.format(hostname=hostname, device_id=device_id),
                                   access_key, None)
    operation = '/devices/{device_id}/messages/events'.format(device_id=device_id)

    uri = 'amqps://{}:{}@{}{}'.format(urllib.parse.quote_plus(username),
                                      urllib.parse.quote_plus(sas_token), hostname, operation)

    send_client = uamqp.SendClient(uri, debug=True)

    dataframe = pandas.read_csv("puhatu.csv")
    messages = json.loads(dataframe.to_json(orient="records"))
    random.shuffle(messages)

    for i in range(len(messages)):
        msg_props = uamqp.message.MessageProperties()
        msg_props.message_id = str(uuid.uuid4())
        message_json = json.dumps(messages[i])
        msg_data = json.dumps(message_json)
        message = uamqp.Message(msg_data, properties=msg_props)
        send_client.send_message(message)
        print(f"Message sent: {message}")
        time.sleep(10)