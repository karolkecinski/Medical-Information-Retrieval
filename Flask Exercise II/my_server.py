
import os
from flask import Flask, render_template, request, send_from_directory, jsonify
#import cv2



database_path = "static/images/database/"
selected_image = None
app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))



@app.route("/")
def index():
    global selected_image
    return render_template("start.html", selected_image= selected_image)

@app.route("/selected_image", methods=['POST'])
def select_query_image():
    global selected_image
    target = os.path.join(APP_ROOT, 'static/images/query')

    #TODO:
    # make a the directory for query images if it is not available i.e os.mkdir(directory name)
    # get the filename and store the  file in the query directory 
       
    return render_template("start.html", selected_image= selected_image)

@app.route("/query_result", methods=['POST'])
def start_query():

    return render_template("query_result.html",selected_image= selected_image) 


if __name__ == "__main__":
    app.run(port=4050, debug=True)