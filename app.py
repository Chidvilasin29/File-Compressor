from flask import Flask, request, send_file, jsonify, render_template
import os
import zipfile

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create upload folder if it doesn't exist

@app.route('/')
def index():
    return render_template('index.html')  # Serves the HTML file

@app.route('/compress', methods=['POST'])
def compress_file():
    # Check if a file is provided
    if 'file' not in request.files:
        return "No file provided", 400
    file = request.files['file']

    # Get the compression level
    try:
        compression_level = int(request.form['level'])
        if compression_level < 0 or compression_level > 9:
            raise ValueError
    except ValueError:
        return "Invalid compression level. Must be between 0 and 9.", 400

    # Save the file to the upload folder
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)

    # Compress the file
    zip_path = os.path.splitext(input_path)[0] + '.zip'
    with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=compression_level) as zipf:
        zipf.write(input_path, arcname=file.filename)

    # Send the compressed file back
    return send_file(zip_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
