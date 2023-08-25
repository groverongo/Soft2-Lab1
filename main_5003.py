from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/hello")
def get_hello():
    return jsonify({'message': 'Success 5003'})
    pass



if __name__ == '__main__':
    app.run("0.0.0.0", port=5003, debug=True)