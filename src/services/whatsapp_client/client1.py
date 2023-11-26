from flask import Flask, request
import json
import message, os
from google.cloud import pubsub_v1
from urllib.parse import unquote

os.environ["GCLOUD_PROJECT"] = "uplifted-woods-362215"

cred_path = "../../resources/application_default_credentials.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_path

app = Flask(__name__)

@app.route('/send', methods=['POST'])
def sendMessage():
    messageText = request.form.get('message')
    # messageText = request.get_data().decode("ISO-8859-1")
    userid = request.form['userID']
    send_to_id = request.form['send_to_ID']
    obj = message.Message(userid, messageText, send_to_id)
    
    # Data must be a bytestring
    data = {"userID" : userid, "message" : messageText, "send_to_ID" : send_to_id}
    data = json.dumps(data)
    data = data.encode("utf-8")

    # Publisher code
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path("uplifted-woods-362215", "m21aie253-sdb")
    print("Publishing to publisher")
    future = publisher.publish(topic_path, data)
    print("Message to ID: " + send_to_id + " = " + messageText)
    return json.dumps(obj.__dict__)

@app.route('/receive', methods=['GET'])
def receiveMessage():
    response = request.get_data()
    response = response.decode("utf-8").split("&")
    srcID, message = response[0].split("=")[1], response[1].split("=")[1]
    response = unquote(message)
    response = response.replace("+"," ").replace("%2C",",")
    # response = request.get_data().decode("utf-8")
    if len(response)>50:
        print("A file format message has been sent from ID: ", srcID, " which can't be shown here")
        return "A file format message has been sent which can't be shown here"
    print("Message from ID: " + srcID + " = " + response)
    return "Message from ID: " + srcID + " = " + response
 
# main driver function
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)