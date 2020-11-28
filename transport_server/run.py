from flask import Flask
app = Flask(__name__)


@app.route("/hello")
def hello():
    # return "Hello World!"
    return {
        'Auth:': "AutomationTestTeam"
    }


if __name__ == "__main__":
    app.run('0.0.0.0', 8086)
