from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/hello")
def get_hello():
    return jsonify({'message': 'Success 5001'})
    pass



if __name__ == '__main__':
    app.run("0.0.0.0", port=5001, debug=True)