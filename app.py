from flask import Flask, request, render_template
import requests
import json
import csv

app = Flask(__name__)
app.config["DEBUG"] = True
url = 'https://jsonplaceholder.typicode.com/posts'
headers = {'authorization': "Basic API Key Ommitted", 'accept': "application/json", 'accept': "text/csv"}
headings = ("UserId","Id","Title","Body")
@app.route("/",methods=['GET'])
def stdata():
    r1 = requests.get(url)
    data = json.loads(r1.text)
    ##print(data)
    with open('dump.csv', 'w+') as outf:
        dw = csv.DictWriter(outf, data[0].keys())
        dw.writeheader()
        for row in data:
            dw.writerow(row)
            print(row)
    return(r1.text)
            ##return render_template("table.html", headings=headings, data=row)

@app.route("/getId/<int:user_Id>",methods=['GET'])
def getdata(user_Id):
    resp = list()
    with open('dump.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        lines = list(csv_reader)
        lines.pop(0)
        for row in lines:
            userID = row['userId']
            if userID == str(user_Id):
                r = {'userId': row['userId'],
                     'id': row['id'],
                     'title': row['title'],
                     'body': row['body']}
                ##print(r)
                resp.append(r)
    ##print(resp)
    return(json.dumps(resp))

@app.route("/", methods=['POST'])
def insData():
    request_data = request.get_json()
    lis = ['userId','id','title','body']
    if not all (k in request_data.keys() for k in lis):
        return "Invalid Payload", 400
    with open('dump.csv', 'a') as outf:
        dw = csv.DictWriter(outf,lis)
        dw.writerow(request_data)
    return("Saved")
