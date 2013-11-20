#!/usr/bin/env python2

# A simple app that lets you upload a epub, calls
# ebook-convert to convert it to mobi and returns
# the mobi file

import os
from flask import Flask, request, redirect, render_template
from werkzeug import secure_filename
from subprocess import call

UPLOAD_FOLDER = 'static/books' #Where we save the uploaded files
ALLOWED_EXTENSIONS = set(['epub']) #Allowed file extensions for uploaded files

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# From the example in the Flask docs, checks file extension
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            epubpath = '%s/%s' % (UPLOAD_FOLDER, filename)
            mobipath = '%s/%s.mobi' % (UPLOAD_FOLDER, filename[:-5])
            file.save(epubpath)
            try:
                call(['ebook-convert', epubpath, mobipath])
                os.remove(epubpath)
                return redirect(mobipath)
            except:
                return 'Something went wrong when trying to convert the book'
    return render_template('main.jinja2')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
