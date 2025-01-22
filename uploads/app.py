from flask import Flask, request, send_file, render_template
import os
import zipfile

app = Flask(__name__)

# Define upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")  # Your HTML file

@app.route("/compress", methods=["POST"])
def compress_file():
    if "file" not in request.files:
        return "No file uploaded", 400

    uploaded_file = request.files["file"]
    compression_level = int(request.form.get("level", 5))  # Default to 5 if not provided

    if uploaded_file.filename == "":
        return "No selected file", 400

    # Save the uploaded file
    filepath = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
    uploaded_file.save(filepath)

    # Compress the file
    zip_filepath = os.path.splitext(filepath)[0] + ".zip"
    with zipfile.ZipFile(zip_filepath, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=compression_level) as zipf:
        zipf.write(filepath, arcname=os.path.basename(filepath))

    # Send the compressed file back to the user
    return send_file(zip_filepath, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
