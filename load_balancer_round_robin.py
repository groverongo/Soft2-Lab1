from flask import Flask, jsonify, g
import requests 
import json

with open('ports.json', 'r') as json_file:
    data = json.load(json_file)

app = Flask(__name__)
weights = data['weights']
ports = data['ports']
n_servers = len(weights) 
actual_server = 0
actual_request_number = weights[0] 


@app.get("/")
def get_hello():
    global actual_request_number,weights,ports,actual_server,actual_request_number

    if actual_request_number == 0:
        actual_server = (actual_server + 1) % n_servers 
        actual_request_number  = weights[actual_server]

    request_port = ports[actual_server]
    request_url = f"http://localhost:{request_port}/hello"

    result = requests.get(request_url).json()

    actual_request_number -= 1


    return {"value LB_RoundRobin":result}




if __name__ == '__main__':
    app.run("0.0.0.0", port=5005, debug=True)