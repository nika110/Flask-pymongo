from flask import Flask, request, render_template, url_for
from flask_pymongo import PyMongo


app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('First.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'inputFile' in request.files:
        inputFile = request.files['inputFile']
        mongo.save_file(inputFile.filename, inputFile)
        mongo.db.users.insert({'username' : request.form.get('username'), 'imagename' : inputFile.filename})
        return "DONE"

@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)


@app.route('/profile/<username>')
def lastone(username):
    user = mongo.db.users.find_one_or_404({'username' : username})
    return f'''
<h1>{username}</h1>
<img src="{url_for('file', filename=user['imagename'])}">
'''





