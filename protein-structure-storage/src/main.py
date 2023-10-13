from flask import Flask

# prints Hello World!
print("Hello, World!")

app = Flask(__name__)

DEBUG_MODE = True
HOST = "0.0.0.0"
PORT = 5000


@app.route("/example_endpoint")
def example_endpoint():
    return "Hello from this endpoint!\n"


@app.route("/retrieve_by_uniprot_id/<id>")
def retrieve_by_uniprot_id(id):
    return f"You asked for id {id}\n"


@app.route("/retrieve_by_sequence/<seq>")
def retrieve_by_sequence(seq):
    return f"You asked for seq {seq}\n"


@app.route("/retrieve_by_key/<key>")
def retrieve_by_key(key):
    print(f"got key: {key}")
    return f"You asked for key {key}\n"


@app.errorhandler(404)
def unknown_url(error):
    return "Error: The requested endpoint does not exist!\n", 404


if __name__ == "__main__":
    if not DEBUG_MODE:
        # use waitress for WSGI server in a production setting
        from waitress import serve
        serve(app, host=HOST, port=PORT)
    else:
        app.run(host=HOST, port=PORT, debug=DEBUG_MODE)
