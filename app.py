from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
	return "Hello from Python CI/CD Pipeline updated test four"
@app.route("/status")
def status():
    return "App is running new-branch"
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
