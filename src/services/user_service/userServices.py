from flask import Flask, request
import json
import user
import mysql.connector
  
app = Flask(__name__)

dataBase = mysql.connector.connect(
  host ="127.0.0.1",
  port = "3306",
  user ="root",
  passwd ="password",
  database = "users"
) 


@app.route('/user', methods=['GET'])
def getUserDetails():
    if request.method == 'GET':
        cursorObject = dataBase.cursor()
        sql = "SELECT * FROM User"
        cursorObject.execute(sql)
        rows = cursorObject.fetchall()
        result = []
        for row in rows:
            d = {}
            for i,col in enumerate(cursorObject.description):
                d[col[0]] = row[i]
            result.append(d)
        return json.dumps(result)
    else:
        return json.dumps({"User":"Invalid"})

@app.route('/user', methods=['POST'])
def storeUserDetails():
    if request.method == 'POST':
        id, name, phone = request.form['userID'], request.form['name'], request.form['phone_number']
        obj = user.User(id, name, phone)
        cursorObject = dataBase.cursor()
        sql = "INSERT INTO User (ID, Name, Phone_Number) VALUES (%s, %s, %s)"
        val = (id, name, phone)
        cursorObject.execute(sql, val)
        dataBase.commit()
        dataBase.close()
        return json.dumps(obj.__dict__)
    else:
        return json.dumps({"User":"Invalid"})
 
# main driver function
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5005)