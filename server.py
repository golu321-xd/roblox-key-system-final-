from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Load database
def load_data():
    try:
        with open("database.json", "r") as f:
            return json.load(f)
    except:
        return {"keys": {}}

data = load_data()

@app.route("/verify", methods=["POST"])
def verify():
    req = request.json
    hwid = req.get("hwid")
    key = req.get("key")
    
    data = load_data()
    
    if key in data["keys"]:
        key_data = data["keys"][key]
        if float(key_data["expiry"]) < datetime.utcnow().timestamp():
            return jsonify({"status": "fail", "reason": "Key expired"})
        if key_data["hwid"] != hwid:
            return jsonify({"status": "fail", "reason": "HWID mismatch"})
        return jsonify({"status": "ok"})
    else:
        return jsonify({"status": "fail", "reason": "Key not found"})

if __name__ == "__main__":
    app.run()
