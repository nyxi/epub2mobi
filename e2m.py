#!/usr/bin/env python2

# A simple app that lets you upload a epub, calls
# ebook-convert to convert it to mobi and returns
# the mobi file

import os
from flask import Flask, request, redirect, render_template
from werkzeug import secure_filename
from subprocess import call

UPLOAD_FOLDER = 'static/books'
ALLOWED_EXTENSIONS = set(['epub'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            pathnoext = '%s/%s' % (UPLOAD_FOLDER, filename[:-5])
            call('ebook-convert %s.epub %s.mobi' % (pathnoext, pathnoext))
            os.remove('%s.epub' % (pathnoext))
            return redirect('%s.mobi' % (pathnoext))

    return render_template('main.jinja2')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
