from flask import Flask

UPLOAD_FOLDER = 'uploads'
try:
    import os
    os.mkdir('uploads')
except:
    pass

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
