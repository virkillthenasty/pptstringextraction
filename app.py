from flask import Flask, render_template, url_for, request, send_file, after_this_request, redirect
from werkzeug.utils import secure_filename
import os, io
from extraction import extraction

app= Flask(__name__)


@app.route('/', methods =['POST','GET'])
def index():
   return render_template('index.html')



@app.route('/upload', methods =['POST','GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        filename = secure_filename(f.filename)
        return downloadFile(str(filename))


# @app.route('/download')
def downloadFile (filename):
    cwd = os.getcwd()
    newFileName = extraction(filename)
    path = os.path.join(cwd, newFileName)

    return_data = io.BytesIO()
    with open(path, 'rb') as fo:
        return_data.write(fo.read())
    return_data.seek(0)
    os.remove(path)

    return send_file(return_data, attachment_filename=newFileName , as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host="192.168.153.197",debug=True)
