from modules import aws_sript, firestorage_code
import os
from flask import Flask, jsonify
from flask import render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os, shutil
from flask_cors import CORS
from decorater_file import crossdomain

global app

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   dog'
app.config['CORS_HEADERS'] = ['Content-Type']

cors = CORS(app, resources={r"/*": {"origins": "*"}})

# Create a directory in a known location to uploaded files to.
uploads_dir = os.path.join(app.instance_path, 'uploads')
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)


# Create a directory in a known location to processed files to.
ml_output_dir = os.path.join(app.instance_path, 'ml_output')
if not os.path.exists(ml_output_dir):
    os.makedirs(ml_output_dir)


@app.route('/upload', methods=['GET', 'POST'])

def upload():
    if request.method == 'POST':
        # save the single "profile" file
        image = request.files['image']
        print(image)

        img_path = os.path.join(uploads_dir, secure_filename(image.filename))
        
        
        ml_out_img_path = os.path.join(ml_output_dir, secure_filename(image.filename))
        image.save(img_path)
        
        print("img_path",img_path)
        print("ml_out_img_path",ml_out_img_path)
        # ML model start
        print("Processing...")
        aws_sript.convert_image(img_path, ml_out_img_path)
        # ML model ends
        print("Image converted successfully")

        img_url = firestorage_code.upload_img(ml_out_img_path)

        print("Image uploaded to firebase storage successfully")

        print("Firebase Image URL ",img_url)



        # cleaning folders
        clean_folders()

        # save each "charts" file
        
        # for file in request.files.getlist('upload'):
        #     print(file.name)
        #     file.save(os.path.join(uploads_dir, file.name))

        # return redirect(url_for('upload'))
        data = {
            "img_url":img_url
        }
    return jsonify(data),{'Access-Control-Allow-Origin': '*'}
    

def clean_folders():
        folders = [uploads_dir,ml_output_dir]
        for folder in folders:
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))

if __name__ == '__main__':
    app.run(debug=True)