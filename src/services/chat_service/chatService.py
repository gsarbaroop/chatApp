import json
from flask import Flask, request
import os
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError
import requests

os.environ["GCLOUD_PROJECT"] = "uplifted-woods-362215"

cred_path = "../../resources/application_default_credentials.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_path

app = Flask(__name__)

@app.route('/receive', methods=['GET', 'POST'])
def receiveMessage():
    my_data = {}
    timeout = 10.0
    subscriber = pubsub_v1.SubscriberClient()
    # The `subscription_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/subscriptions/{subscription_id}`
    subscription_path = subscriber.subscription_path("uplifted-woods-362215", "Second_subscription")

    def call_mediaService(data):
        url = 'http://172.22.241.38:8082/store'
        headers = {
        'content-type' : 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
        }
        response = requests.post(url, data=data, headers=headers, allow_redirects=True,)

    def callback(message: pubsub_v1.subscriber.message.Message) -> None:
        message_new = message.data.decode("utf-8")
        json_text = json.loads(message_new)

        data = {"userID" : json_text["userID"], "Message" : json_text["message"], "Send_to_ID" : json_text["send_to_ID"]}
        print("data: ", data)
        # calling media service
        call_mediaService(data)

        # Call notify service
        url = 'http://172.22.241.38:8081/notify'
        headers = {
        'content-type' : 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
        }
        response = requests.post(url, data=data, headers=headers, allow_redirects=True)

        my_data = data
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


    return json.dumps(my_data)   

# main driver function
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8080)


