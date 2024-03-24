import os
import zipfile
from io import BytesIO
from flask import Flask, request, send_file, make_response
from flask_cors import CORS 
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app) 

def remove_comments(file_path, language):
    if language == 'python':
        single_line_comment = '#'
        multi_line_comment_starts = ("'''", '"""')
        multi_line_comment_ends = ("'''", '"""')
    elif language == 'javascript':
        single_line_comment = '//'
        multi_line_comment_starts = ('/*', '<!--')
        multi_line_comment_ends = ('*/', '-->')
    else: 
        single_line_comment = '//'
        multi_line_comment_starts = ('/*',)
        multi_line_comment_ends = ('*/',)

    inside_multi_line_comment = False
    multi_line_comment_started = None

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    new_lines = []
    for line in lines:
        original_line = line  
        cleaned_line = ''
        if not inside_multi_line_comment:
          
            parts = line.split(single_line_comment, 1)
            line = parts[0]
            if len(parts) > 1 and not parts[0].strip(): 
                continue

        i = 0
        while i < len(line):
            if not inside_multi_line_comment:
                for start in multi_line_comment_starts:
                    if line[i:].startswith(start):
                        inside_multi_line_comment = True
                        multi_line_comment_started = start
                        i += len(start) - 1
                        break
                else: 
                    cleaned_line += line[i]
            else:

                for end in multi_line_comment_ends:
                    if line[i:].startswith(end):
                        inside_multi_line_comment = False
                        i += len(end) - 1
                        break
            i += 1


        if cleaned_line.strip():
       
            if original_line.endswith('\n') and cleaned_line:
                cleaned_line += '\n'
            new_lines.append(cleaned_line)
        elif not inside_multi_line_comment:
            if original_line.strip() == '' and original_line.endswith('\n'):
                new_lines.append('\n')

    with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(new_lines)

    return new_lines 


def process_folder(zip_bytes, language):
    temp_dir = 'temp_extracted'
    os.makedirs(temp_dir, exist_ok=True)

    with zipfile.ZipFile(BytesIO(zip_bytes), 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            file_path = os.path.join(root, file)
            print(f"Processing file: {file_path}") 
            updated_lines = remove_comments(file_path, language)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.writelines(updated_lines)

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file_path = os.path.relpath(file_path, temp_dir)
                print(f"Adding to zip: {zip_file_path}")
                zip_file.write(file_path, zip_file_path)

    zip_buffer.seek(0)
    for root, dirs, files in os.walk(temp_dir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(temp_dir)
    return zip_buffer


def is_zip_file(file_bytes):
    try:
        with zipfile.ZipFile(BytesIO(file_bytes), 'r') as zip_ref:
            return True 
    except zipfile.BadZipFile:
        return False


@app.route('/upload', methods=['POST'])
def upload_files():
    if not request.files:
        return "No file part", 400
    if len(request.files) > 1:
        return "Only one file is allowed", 400
    language = request.form.get('language')
    if not language:
        return "Missing language", 400


    temp_dir = 'temp'
    os.makedirs(temp_dir, exist_ok=True)


    for file_key, file in request.files.items():
        file_bytes = file.read()

        if is_zip_file(file_bytes):

            zip_buffer = process_folder(file_bytes, language)
            with open(os.path.join(temp_dir, secure_filename(file.filename)), 'wb') as temp_file:
                temp_file.write(zip_buffer.read())
        else:

            temp_file_path = os.path.join(temp_dir, secure_filename(file.filename))
            with open(temp_file_path, 'wb') as temp_file:
                temp_file.write(file_bytes)
            remove_comments(temp_file_path, language)

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, os.path.relpath(file_path, temp_dir))
    zip_buffer.seek(0)

    for root, dirs, files in os.walk(temp_dir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(temp_dir)

    response = make_response(send_file(zip_buffer, mimetype='application/zip', as_attachment=True, download_name='processed.zip'))
    return response
if __name__ == '__main__':
    app.run(debug=True)