from flask import Flask, request, send_file
import os
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return '''
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit">
        </form>
    '''

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    output_filename = f"{os.path.splitext(file.filename)[0]}.sb3"
    output_filepath = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

    try:


        subprocess.run(["python", "video2sb3.py", filepath, output_filepath], check=True)

        # Provide the file for download
        return send_file(output_filepath, as_attachment=True, download_name=output_filename)
    
    except subprocess.CalledProcessError as e:
        return f"Error during conversion: {e}"
    
    finally:

        if os.path.exists(filepath):
            os.remove(filepath)
        if os.path.exists(output_filepath):
            os.remove(output_filepath)

if __name__ == '__main__':
    app.run(debug=True)
