from flask import Flask, request, jsonify
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def result():
    if request.method == 'GET':
        return 'get'
    else:
        return request.form['foo'] # should display 'bar'
        # return data # response to your request.

