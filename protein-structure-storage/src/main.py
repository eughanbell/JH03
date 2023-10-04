from flask import Flask

print("Hello, World!")

app = Flask(__name__)

DEBUG_MODE = True
HOST = "0.0.0.0"
PORT = 5000


@app.route("/example_endpoint")
def example_endpoint():
    return "Hello from this endpoint!\n"


if __name__ == "__main__":
    if not DEBUG_MODE:
        # use waitress for WSGI server in a production setting
        from waitress import serve
        serve(app, host=HOST, port=PORT)
    else:
        app.run(host=HOST, port=PORT, debug=DEBUG_MODE)
