from google.cloud import storage
import os
from flask import Flask, request
import json
# from base64 import b64decode

os.environ["GCLOUD_PROJECT"] = "uplifted-woods-362215"

cred_path = "../../resources/application_default_credentials.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_path

app = Flask(__name__)

bucket_name = "bucketz-for-webapp"


# def list_blobs(bucket_name):
#         storage_client = storage.Client()

#         blobs = storage_client.list_blobs(bucket_name)

#         for blob in blobs:
#                 print(blob.name)


# def read(bucket_name, blob_name):
#         storage_client = storage.Client()
#         bucket = storage_client.bucket(bucket_name)
#         blob = bucket.blob(blob_name)

#         with blob.open("r") as f:
#                 print(f.read())


@app.route('/store', methods=['GET','POST'])
def write_read():
        data = request.get_data()
        data = data.decode("utf-8")
        # print(data)
        # json_text = json.loads(data)
        srcid, message, destid = data.split("&")
        print(srcid, destid)
        srcid = srcid.split("=")[1]
        destid = destid.split("=")[1]
        message = message.split("=")[1]

        name = srcid + "_to_" + destid
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        d = 'bucketz-for-webapp/' + name
        d = bucket.blob(d)
        # if "jpg" in message or "pdf" in message or "txt" in message:
        name += "_file"
        message = message.encode()
        # bytes = b64decode(message, validate=True)
        with open(name, "+wb") as my_file:
               my_file.write(message)
        with open(name, "rb") as my_file:
               d.upload_from_file(my_file)
        # else:
        #         d.upload_from_string(message)
        return "uploaded"

# write_read("bucketz-for-webapp", "../../resources/media/IMG-20230902-WA0008.jpg")
# list_blobs("bucketz-for-webapp")
# read("bucketz-for-webapp","bucketz-for-webapp/IMG-20230902-WA0008.jpg")

# main driver function
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8082)