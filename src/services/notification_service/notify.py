# import concurrent.futures
from json import dumps  
from flask import Flask, request
import os
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError
import requests
 
os.environ["GCLOUD_PROJECT"] = "uplifted-woods-362215"

cred_path = "../../resources/application_default_credentials.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_path

app = Flask(__name__)

@app.route('/notify', methods=['GET','POST'])
def notifyClients():
    data = request.get_data()
    data = data.decode("utf-8")
    data_list = data.split("&")
    srcID, message, dstID = data_list[0].split("=")[1], data_list[1].split("=")[1], data_list[2].split("=")[1]
    data = {"srcID":srcID, "message":message}
    print("srcID = ", srcID)
    print("destID = ", dstID)
    url = ""
    if dstID == "1":
        url = "http://127.0.0.1:5000/receive"
    elif dstID == "2":
        url = "http://127.0.0.1:8083/receive"
    elif dstID == "3":
        url = "http://127.0.0.1:8084/receive"
    elif dstID == "4":
        url = "http://127.0.0.1:8085/receive"
    headers = {
        'content-type' : 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
        }
    response = requests.get(url, data=data, headers=headers, allow_redirects=True,)
    print("Notification sent")
    return "Notification sent"

# main driver function
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8081)