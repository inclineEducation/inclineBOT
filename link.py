from flask import Flask, request, jsonify
from github import Github
import os
import requests
import json
from threading import Thread

'''
    post_data = {"text": "link request received"}
    r = requests.post(
        request.form['response_url'], data=json.dumps(post_data),
        headers={'Content-Type': 'application/json'}
    )

    return str(r.status_code) + r.reason + " " + request.form['response_url']
'''


def post(request, data):
    requests.post(
        request.form['response_url'], data=json.dumps({"text": data}),
        headers={'Content-Type': 'application/json'}
    )


class Link(Thread):
    def __init__(self, request, token):
        Thread.__init__(self)
        self.request = request
        self.token = token
    def run(self):
        print ("INSIDE THREAD")
        data = str(self.request.form['text'])
        user = None
        try:
            user = str(self.request.form['user_name'])
        except:
            user = 'anon'
        index = 0
        while index < len(data) and (not data[index] == ' '):
            index = index + 1
        if index == len(data):
            # return 'Please enter a destination URL'
            post(self.request, "Please enter a destination URL")
            return
        source = data[0:index]
        dest = data[index + 1:len(data)]
        if len(dest) < 8 or ((not dest[0:8] == "https://") and (not dest[0:7] == "http://")):
            # return "invalid destination string - please prefix website URLs with http:// or https:// "
            post(self.request, "invalid destination string - please prefix website URLs with http:// or https:// ")
            return
        print('token: ' + self.token)
        g = Github(str(self.token))
        repo = g.get_repo("inclineEducation/inclineEducation.github.io")
        redirects = repo.get_contents("_redirects")
        repo.update_file(redirects.path, user + " added http://inclineedu.org/" + source + " -> " + dest + " to redirects", \
                         str(redirects.decoded_content) + "/" + source + "    " + dest + "     # added by: " + user + "\n",
                         redirects.sha)
        post(self.request, 'inclineedu.org/' + source + " now redirects to " + dest)
        return
        # return 'inclineedu.org/' + source + " now redirects to " + dest
        # return 'success'
        # return data # response to your request.

