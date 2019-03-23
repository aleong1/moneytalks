#Team
#SoftDev1 pd8
#K
#2018

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "flask template"

if (__name__) = ("__main__"):
    app.debug = True
    app.run()

