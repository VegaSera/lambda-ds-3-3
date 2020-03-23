from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    print("Visited hello page")
    return "Hewwo World"

@app.route("/about")
def about():
    print("Visited about page")
    return "About Page"