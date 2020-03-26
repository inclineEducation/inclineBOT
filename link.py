from flask import Flask, request, jsonify
from github import Github
import os
import requests
import json
from threading import Thread
import time


def post(request, data):
    requests.post(
        request.form['response_url'], data=json.dumps({"text": data}),
        headers={'Content-Type': 'application/json'}
    )


class Link(Thread):
    def __init__(self, request):
        Thread.__init__(self)
        self.request = request

    def run(self):
        data = str(self.request.form['text'])
        user = None
        try:
            user = str(self.request.form['user_name'])
        except:
            user = 'anon'
        index = 0

        # move index to end of first argument
        while index < len(data) and (not data[index] == ' '):
            index = index + 1

        # if no second argument
        if index == len(data):
            post(self.request, "Please enter a destination URL")
            return

        # set destination variable
        source = data[0:index]
        dest = data[index + 1:len(data)]

        # check destination URL - Not valid link
        if len(dest) < 8 or (not dest[0:8] == "https://" and not dest[0:7] == "http://"):
            post(self.request, "invalid destination string - please prefix website URLs with http:// or https:// ")
            return

        # get GitHub token
        app_root = os.path.dirname(os.path.abspath(__file__))
        token_file = open(os.path.join(app_root, 'token'), "r")
        token = token_file.readline().rstrip('\n')
        token_file.close()

        # open GitHub Repo
        g = Github(str(token))
        repo = g.get_repo("inclineEducation/inclineEducation.github.io")
        redirects = repo.get_contents("_redirects")

        # update _redirects file
        repo.update_file(redirects.path, user + " added www.inclineedu.org/" + source + " -> " + dest + " to redirects",
                         str(redirects.decoded_content) + "/" + source + "    " + dest + "     # added by: " + user + "\n",
                         redirects.sha)

        # respond to /link
        post(self.request, 'inclineedu.org/' + source + " now redirects to " + dest)
        return

