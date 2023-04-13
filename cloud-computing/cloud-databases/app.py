import json
import os
import uuid
from datetime import datetime

from azure.storage.blob import BlobServiceClient
from flask import Flask, render_template, request
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions

COSMOS_URL = os.getenv('APPSETTING_COSMOS_URL')
MasterKey = os.getenv('APPSETTING_MASTER_KEY')
DATABASE_ID = 'lab5messagesdb'
CONTAINER_ID = 'lab5messages'
cosmos_db_client = cosmos_client.CosmosClient(COSMOS_URL, {'masterKey': MasterKey} )
cosmos_db = cosmos_db_client.get_database_client(DATABASE_ID)
container = cosmos_db.get_container_client(CONTAINER_ID)
STORAGE_ACCOUNT=os.getenv('APPSETTING_STORAGE_ACCOUNT')
CONN_KEY = os.getenv('APPSETTING_CONN_KEY')



def insert_cosmos(content, img_path):
    new_message = {
        'id': str(uuid.uuid4()),
        'content': content,
        'img_path': img_path,
        'timestamp': datetime.now().isoformat(" ", "seconds")
    }
    try:
        container.create_item(body=new_message)
    except exceptions.CosmosResourceExistsError:
        print("Resource  already exists, didn't insert message.")


def read_cosmos():
    messages = []
    messages = list(container.read_all_items(max_item_count=10))
    return messages


app = Flask(__name__)
UPLOAD_FOLDER = './static/images'
CONN_KEY = os.getenv('CONN_KEY')
storage_account = os.getenv('STORAGE_ACCOUNT')
images_container = "images"
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
# blob_service_client = BlobServiceClient(account_url="https://" + storage_account + ".blob.core.windows.net/",
#                                        credential=CONN_KEY)
blob_service_client = BlobServiceClient.from_connection_string(conn_str=connect_str)


def insert_blob(img_path):
    filename = img_path.split('/')[-1]
    blob_client = blob_service_client.get_blob_client(container=images_container, blob=filename)
    with open(file=img_path, mode="rb") as data:
        blob_client.upload_blob(data, overwrite=True)


def read_messages_from_file():
    """ Read all messages from a JSON file"""
    with open('data.json') as messages_file:
        return json.load(messages_file)


def append_message_to_file(blob_path, new_message):
    """ Read the contents of JSON file, add this message to it's contents, then write it back to disk. """
    data = read_messages_from_file()
    new_message = {
        'content': new_message,
        'img_path': blob_path,
        'timestamp': datetime.now().isoformat(" ", "seconds")
    }
    data['messages'].append(new_message)
    with open('data.json', mode='w') as messages_file:
        json.dump(data, messages_file)


# The Flask route, defining the main behaviour of the webserver:
@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        new_message = request.form["msg"]
        if new_message and 'file' in request.files:
            image = request.files['file']
            img_path = os.path.join(UPLOAD_FOLDER, image.filename)
            blob_path = 'https://' + storage_account + '.blob.core.windows.net/' + images_container + '/' + image.filename
            insert_cosmos(new_message, blob_path)
            image.save(img_path)
            insert_blob(img_path)
    data = read_cosmos()

    # Return a Jinja HTML template, passing the messages as an argument to the template:
    return render_template('home.html', messages=data)
