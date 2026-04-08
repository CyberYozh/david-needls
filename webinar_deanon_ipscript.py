from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def get_ip():
    ip = request.remote_addr
    print(ip)
    return f"TEST\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
