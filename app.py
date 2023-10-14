
import os
import requests
import pytesseract
from PIL import Image

from bs4 import BeautifulSoup as bs
from flask import (
    Flask, 
    request, 
    redirect,
    render_template, 
    send_from_directory
)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'images/')

    if not os.path.isdir(target):
        os.mkdir(target)
    else:
        pass

    for upload in request.files.getlist("file"):
        filename = upload.filename
        destination = "/".join([target, filename])
        upload.save(destination)
    
    return render_template("complete.html")

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)

@app.route('/gallery')
def get_gallery():
    new_term = {}

    target = os.path.join(APP_ROOT, 'images/')
    image_names = os.listdir('./images')
    pytesseract.pytesseract.tesseract_cmd = 'Tesseract-OCR/tesseract.exe'
    
    for i in image_names:
        destination = "/".join([target, i])
        image = Image.open(destination)
        text = pytesseract.image_to_string(image, lang="eng")
        term = {i : text.split()}
        new_term.update(term)

    return render_template("gallery.html", 
                           new_term=new_term)

@app.route('/upload')
def upload_complete():
    return render_template('complete.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/skills')
def skills():
    return render_template('skills.html')

@app.route('/news')
def news():
    return redirect('https://imvickykumar999.pythonanywhere.com/')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
