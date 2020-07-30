# from pywebcopy import save_webpage
import requests
import os
from flask import Flask , render_template, request



path = os.path.dirname(__file__)
print(path)
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("home.html")
   
@app.route("/main" ,methods=["POST"])
def main():
    url = request.form.get("url")
    res = requests.get(url)
    # api work
    f = open("./templates/cloned.html", 'w')
    f.write(res.text)
    print(res.cookies)
    return render_template("cloned.html")
    

    


