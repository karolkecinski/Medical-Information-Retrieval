from asyncio import selector_events
from flask import request, flash, redirect, Blueprint, render_template
import os
from werkzeug.utils import secure_filename
from query_handler import Handler

views = Blueprint('views', __name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
QUERY_FOLDER = f'static{os.sep}queries'
PACKAGE = 'website'
##DATA_FOLDER = f'search_engine{os.sep}data{os.sep}images{os.sep}training'

ALLOWED_EXT = ['jpg', 'png']


@views.route("/")
def index():
    global selected_image
    return render_template("start.html", selected_image=selected_image)# selected_image)

@views.route("/selected_image", methods=['POST, GET'])
def select_query_image():

    if request.method == 'GET':
        return index()

    global selected_image
    target = os.path.join(APP_ROOT, QUERY_FOLDER)

    if os.path.isdir(target) == False:
        os.mkdir(target)

    if request.method == 'POST':
    
        file = request.files['file']
        if not file:
            flash(f'No file chosen', 'error')
            return redirect('/')

        filename, ext = secure_filename(file.filename.lower().split('.'))
        if ext not in ALLOWED_EXT:
            flash(f'Invalid filetype: .{ext}', 'error')
            return redirect('/')

        selected_image = f'{filename}.{ext}'
        file_path = os.path.join(target, selected_image)
        file.save(file_path)

        return render_template("start.html", selected_image = selected_image)

@views.route("/query_result", methods=['POST', 'GET'])
def start_query():
    global selected_image
    global query_results

    if request.method == 'GET':
        if query_results:
            return render_template("query_result.html", selected_image = selected_image, query_results = query_results)
        else:
            return redirect('/')

    image_name = selected_image.split('.')[0]

    flash(f'Searching')

    image

    return render_template("query_result.html",selected_image= selected_image) 


if __name__ == "__main__":
    app.run(port=4050, debug=True)