from flask import Flask
from flask import request
#Import Alexa modules

#from hello_world import handler

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def hello():
    print(request.data)
    return "Hello"




if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
