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


# main driver function
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8082)