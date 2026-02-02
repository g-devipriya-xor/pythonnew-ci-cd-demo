from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    	print("Demo branch endpoint called")
	return "Hello from Python CI/CD Pipeline updated test PR"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
