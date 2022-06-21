from asyncio import selector_events
from flask import request, flash, redirect, Blueprint, render_template
import os
from werkzeug.utils import secure_filename
from search_engine.handler import Handler
import json

views = Blueprint('views', __name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
QUERY_FOLDER = f'static{os.sep}uploaded'
PACKAGE = 'website'
##DATA_FOLDER = f'search_engine{os.sep}data{os.sep}images{os.sep}training'

ALLOWED_EXT = ['jpg', 'png']
handler = Handler()
selected_image = ""
selected_images = []
not_selected_images = []

@views.route("/")
def index():
    global selected_image
    return render_template("start.html", selected_image=selected_image)# selected_image)

@views.route("/selected_image", methods=['POST', 'GET'])
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

        filename, ext = secure_filename(file.filename.lower()).split('.')
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

    flash(f'Searching', 'success')

    image_path = os.path.join(PACKAGE, QUERY_FOLDER, selected_image)

    query_results = handler.query(image_path)

    print(query_results, flush=True)

    return render_template("query_result.html", selected_image = selected_image, query_results = query_results)

@views.route("/modified_result", methods=['POST', 'GET'])
def modified_query():
    json_data = json.loads(request.get_data())
    selected_images = json_data["selected_images"]
    not_selected_images = json_data["not_selected_images"]

    if request.method == 'GET':
        return redirect('/')

    print(not_selected_images)
    ### TODO: retrieve images for modified query

    query_results = handler.relevance_feedback(selected_images, not_selected_images) #SEQ.Query().relevance_feedback(selected_images, not_selected_images)

    # image_name = selected_image.split('.')[0]
    # flash(f'Searching', 'success')
    # image_path = os.path.join(PACKAGE, QUERY_FOLDER, selected_image)
    # query_results = handler.query(image_path)
    print(query_results, flush=True)
    return render_template("query_result.html", selected_image = selected_image, query_results = query_results)
