import asyncio
import uuid
from azure.iot.device.aio import ProvisioningDeviceClient
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message
import json
import os
import time
import pandas
import random


async def main():
    provisioning_host = "global.azure-devices-provisioning.net"
    id_scope = os.getenv('SCOPE')
    print(f"Scope id: {id_scope}")
    request_key = os.getenv('REQUEST_KEY')
    print(f"Request key: {request_key}")
    device_id = os.getenv('DEVICE_ID')
    print(f"Device id: {device_id}")

    provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
        provisioning_host=provisioning_host,
        registration_id=device_id,
        id_scope=id_scope,
        symmetric_key=request_key,
    )

    registration_result = await provisioning_device_client.register()
    if registration_result.status == "assigned":
        print("Registration succeeded")
        device_client = IoTHubDeviceClient.create_from_symmetric_key(
            symmetric_key=request_key,
            hostname=registration_result.registration_state.assigned_hub,
            device_id=registration_result.registration_state.device_id,
        )
        # Connect the client
        await device_client.connect()
        print("Device connected successfully")

        dataframe = pandas.read_csv("puhatu.csv")
        messages = json.loads(dataframe.to_json(orient="records"))
        random.shuffle(messages)

        for i in range(len(messages)):
            message_json = json.dumps(messages[i])
            msg_data = json.dumps(message_json)
            message = Message(msg_data)
            message.message_id = uuid.uuid4()

            print(f"Message sent: {message}")
            await device_client.send_message(message)
            time.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
