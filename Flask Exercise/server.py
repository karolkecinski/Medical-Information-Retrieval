from werkzeug.utils import secure_filename
from flask import Flask, render_template, request
import os
app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = 'static'

'''
Tutorial help: https://www.tutorialspoint.com/flask/flask_file_uploading.htm
'''

@app.route('/')
def start():
   return render_template('upload.html')
	
@app.route("/selected_image", methods=['POST'])
def select_query_image():
    if request.method == 'POST':
       file = request.files['file']
       filename = secure_filename(file.filename)
       pathToFile = os.path.join('static', filename)
       file.save(pathToFile)
       return render_template('show_image.html', image = filename)
		
if __name__ == '__main__':
   app.run(debug = True)