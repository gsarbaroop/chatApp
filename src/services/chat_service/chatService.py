from json import dumps  
from flask import Flask, request
import os
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError

os.environ["GCLOUD_PROJECT"] = "uplifted-woods-362215"

cred_path = "../../resources/application_default_credentials.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_path

app = Flask(__name__)

@app.route('/receive', methods=['POST'])
def receiveMessage():
    userid = request.form['userid']
    messageText = request.form['message']
    send_to_id = request.form['send_to_ID']
    my_data = {"userID" : userid, "Message" : messageText, "Send_to_ID" : send_to_id} 
    
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path("uplifted-woods-362215", "m21aie253-sdb")
    
    # Data must be a bytestring
    data = request.encode("utf-8")
    # When you publish a message, the client returns a future.
    future = publisher.publish(topic_path, data)
    print(future.result())

    return dumps(my_data)   





# print(f"Published messages to {topic_path}.")

timeout = 5.0
subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_id}`
subscription_path = subscriber.subscription_path("uplifted-woods-362215", "Second_subscription")

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    print(f"Received {message}.")
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

# Wrap subscriber in a 'with' block to automatically call close() when done.
with subscriber:
    try:
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is encountered first.
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()  # Trigger the shutdown.
        streaming_pull_future.result()  # Block until the shutdown is complete.