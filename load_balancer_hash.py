from flask import Flask, jsonify, request,Response
import requests 
from datetime import datetime
import hashlib
import json

with open('ports.json', 'r') as json_file:
    data = json.load(json_file)

app = Flask(__name__)
weights = data['weights']
ports = data['ports']
n_servers = len(weights) 
actual_server = 0
actual_request_number = weights[0]

#429
counters = [0 for _ in range(len(ports))]
is_full = [0 for _ in range(len(ports))]
timeout = ["" for _ in range(len(ports))]

LIMITE_ARBITRARIO = 5 

@app.get("/")
def get_hello():
    global is_full
    tiempo = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    hash_val = int(hashlib.sha256(tiempo.encode()).hexdigest(),16)

    index = hash_val % len(ports)

    if is_full[index] and (datetime.now() - timeout[index]).seconds > LIMITE_ARBITRARIO:
        is_full[index] = 0
        counters[index] = 0
    elif is_full[index]:
        selected_index = None
        min_requests = float('-inf')

        for rel_index in range(len(counters)):
            if not is_full[rel_index] and actual_request_number > min_requests:
                selected_index = rel_index
                break

        if selected_index is None:
            return Response(status=429)
        index = selected_index


    counters[index] += 1

    select_port = ports[index]

    request_url = f"http://localhost:{select_port}/hello"
    result = requests.get(request_url).json()

    if counters[index] == weights[index]:
        timeout[index] = datetime.now()
        is_full[index] = 1
    
    print(counters)


    return {'value LB_HASH': result}

if __name__ == '__main__':
    app.run("0.0.0.0", port=5010, debug=True)