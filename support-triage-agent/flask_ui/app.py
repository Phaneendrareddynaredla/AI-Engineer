from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

FASTAPI_URL = "https://judson-feuilletonistic-cullen.ngrok-free.dev/"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    text = request.form.get("description", "")
    res = requests.post(FASTAPI_URL, json={"description": text})
    return jsonify(res.json())

if __name__ == "__main__":
    app.run(port=5000)
