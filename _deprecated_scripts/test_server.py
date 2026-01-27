from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from minimal server"

if __name__ == "__main__":
    print("Starting minimal server...")
    app.run(host='0.0.0.0', port=5000)
