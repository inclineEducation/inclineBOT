from flask import Flask, request, jsonify
from github import Github
import os
import requests
import json

def link(request):
    data = str(request.form['text'])

    user = None
    try:
        user = str(request.form['user_name'])
    except:
        user = 'anon'
    index = 0
    while index < len(data) and (not data[index] == ' '):
        index = index + 1
    if index == len(data):
        return 'Please enter a destination URL'
    source = data[0:index]
    dest = data[index + 1:len(data)]
    if len(dest) < 8 or ((not dest[0:8] == "https://") and (not dest[0:7] == "http://")):
        return "invalid destination string - please prefix website URLs with http:// or https:// "
    print('token: ' + token)
    g = Github(str(token))
    repo = g.get_repo("inclineEducation/inclineEducation.github.io")
    redirects = repo.get_contents("_redirects")
    repo.update_file(redirects.path, user + " added http://inclineedu.org/" + source + " -> " + dest + " to redirects", \
                     str(redirects.decoded_content) + "/" + source + "    " + dest + "     # added by: " + user + "\n",
                     redirects.sha)
    return 'inclineedu.org/' + source + " now redirects to " + dest
    # return 'success'
    # return data # response to your request.