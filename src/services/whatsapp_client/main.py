from flask import Flask, request
import json
import message

app = Flask(__name__)

@app.route('/send', methods=['POST'])
def sendMessage():
    userid = request.form['userid']
    messageText = request.form['message']
    send_to_id = request.form['send_to_ID']
    obj = message.Message(userid, messageText, send_to_id)
    return json.dumps(obj.__dict__)
 
# main driver function
if __name__ == '__main__':
    app.run()