from flask import Flask, request, jsonify
from github import Github
import os
import requests
import json
from link import *
from threading import Thread
import time

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def result():
    if request.method == 'GET':
        return "get method invoked - THIS URL IS USED FOR POSTING. COME BACK WITH POST. GET OUT WITH YOUR GETS."
    else:

        # dictionary mapping for slash commands:
        # add class to link.py and add mapping switcher
        switcher = {
            '/link': Link
        }

        # obtain command class form switcher
        func = switcher.get(request.form['command'], lambda: "Invalid month")

        # start new command thread
        thread = func(request.__copy__())
        thread.start()

        # confirm request received
        return 'Link request received'
