# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 15:23:13 2020

@author: roysoumy
"""

from flask import Flask, render_template
app = Flask(__name__)


###Creating the home page - thats what route does
@app.route("/")
@app.route("/home")
def home():
    return "<h1>Home Page</h1>"

@app.route("/about")
def about():
    return "<h1>About Page</h1>"

if __name__ == "__main__":
    app.run(debug = True)