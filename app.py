from flask import Flask, request, jsonify, render_template
from azure.cosmos import CosmosClient
import os, uuid

app = Flask(__name__)

COSMOS_URL = os.environ.get("COSMOS_URL")
COSMOS_KEY = os.environ.get("COSMOS_KEY")
DB_NAME = "feedback"
CONTAINER_NAME = "messages"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/feedback", methods=["POST"])
def submit_feedback():
    data = request.get_json()
    email = data.get("email")
    message = data.get("message")

    client = CosmosClient(COSMOS_URL, COSMOS_KEY)
    db = client.get_database_client(DB_NAME)
    container = db.get_container_client(CONTAINER_NAME)

    item = {
        "id": str(uuid.uuid4()),
        "email": email,
        "message": message
    }
    container.create_item(item)

    return jsonify({"status": "ok", "msg": "Feedback enregistré !"}), 200

if __name__ == "__main__":
    app.run(debug=True)
