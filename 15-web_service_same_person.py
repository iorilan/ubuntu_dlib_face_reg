# this sample is to compare if the 2 input photo is the same person

import face_recognition
from flask import Flask, jsonify, request, redirect

# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file1' not in request.files or 'file2' not in request.files:
            return redirect(request.url)

        file1 = request.files['file1']
	file2 = request.files['file2']

        if file1.filename == '' or file2.filename == '':
            return redirect(request.url)

        if file1 and allowed_file(file1.filename) and file2 and allowed_file(file2.filename):
            # The image file seems valid! Detect faces and return the result.
            return detect_faces_in_image(file1, file2)

    # If no valid image file was uploaded, show the file upload form:
    return '''
    <!doctype html>
    <title>Is this a picture of Obama?</title>
    <h1>Upload a picture and see if it's a picture of Obama!</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    '''


def detect_faces_in_image(file_stream1, file_stream2):
    # get the encoding of 1st image
    img1 = face_recognition.load_image_file(file_stream1)
    face1_encoding = face_recognition.face_encodings(img1)[0]

    # get the encoding of the 2nd image
    img2 = face_recognition.load_image_file(file_stream2)
    face2_encoding = face_recognition.face_encodings(img2)

    face_found = False
    is_same = False

    if len(face2_encoding) > 0:
        face_found = True
        # See if the first face in the uploaded image matches the known face of Obama
        match_results = face_recognition.compare_faces([face1_encoding], face2_encoding[0])
        if match_results[0]:
            is_same = True

    # Return the result as json
    result = {
        "face_found_in_image": face_found,
        "is same person": is_same
    }
    return jsonify(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
