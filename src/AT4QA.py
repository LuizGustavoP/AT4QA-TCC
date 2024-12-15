import subprocess
from flask import Flask, Response, render_template, request, url_for, jsonify, send_from_directory, flash, redirect
import os

app = Flask(__name__)

pytest_process = None

EDITOR_UPLOAD_FOLDER = 'editor'
FEATURE_UPLOAD_FOLDER= 'features'
DOCUMENTATION_UPLOAD_FOLDER = 'documentation'
TRANSLATOR_MASKS_UPLOAD_FOLDER = 'translator/masks'
TRANSLATOR_DICTIONARIES_UPLOAD_FOLDER = 'translator/dictionaries'

app.config['EDITOR_UPLOAD_FOLDER'] = EDITOR_UPLOAD_FOLDER
app.config['FEATURE_UPLOAD_FOLDER'] = FEATURE_UPLOAD_FOLDER
app.config['DOCUMENTATION_UPLOAD_FOLDER'] = DOCUMENTATION_UPLOAD_FOLDER
app.config['TRANSLATOR_MASKS_UPLOAD_FOLDER'] = TRANSLATOR_MASKS_UPLOAD_FOLDER
app.config['TRANSLATOR_DICTIONARIES_UPLOAD_FOLDER'] = TRANSLATOR_DICTIONARIES_UPLOAD_FOLDER

app.config["ALLOWED_FILE_EXTENSIONS"] = ["feature", "mask", "dictionary", "yaml", "json"]

if not os.path.exists(app.config["EDITOR_UPLOAD_FOLDER"]):
    os.makedirs(app.config["EDITOR_UPLOAD_FOLDER"])

if not os.path.exists(app.config["FEATURE_UPLOAD_FOLDER"]):
    os.makedirs(app.config["FEATURE_UPLOAD_FOLDER"])

if not os.path.exists(app.config["DOCUMENTATION_UPLOAD_FOLDER"]):
    os.makedirs(app.config["DOCUMENTATION_UPLOAD_FOLDER"])

if not os.path.exists(app.config["TRANSLATOR_MASKS_UPLOAD_FOLDER"]):
    os.makedirs(app.config["TRANSLATOR_MASKS_UPLOAD_FOLDER"])

if not os.path.exists(app.config["TRANSLATOR_DICTIONARIES_UPLOAD_FOLDER"]):
    os.makedirs(app.config["TRANSLATOR_DICTIONARIES_UPLOAD_FOLDER"])

def check_file_extension(file):
    return "." in file and file.rsplit(".", 1)[1].lower() in app.config["ALLOWED_FILE_EXTENSIONS"]

@app.route('/')
def homepage():
    return render_template(
        'home.html',
        title="Home - AT4QA Project"
    )

@app.route('/agbdd')
def agbdd():
    return render_template(
        'agbdd.html',
        title="AGBDD - AT4QA Project"
    )

@app.route('/generator')
def generator():
    return render_template(
        'generator.html',
        title="Generator - AT4QA Project"
    )

@app.route('/editor')
def editor():
    return render_template(
        'editor.html',
        title="Editor - AT4QA Project"
    )

@app.route('/translator')
def translator():
    return render_template(
        'translator.html',
        title="Translator - AT4QA Project"
    )

@app.route('/test_builder')
def test_builder():
    return render_template(
        'test_builder.html',
        title="Builder - AT4QA Project"
    )

@app.route('/upload_file', methods=['POST'])
def upload_file():

    type = request.args.get('type', '')

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    files = request.files.getlist('file')

    for file in files:
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if file and type == 'features':
            file.save(os.path.join(app.config['FEATURE_UPLOAD_FOLDER'], file.filename))
        elif file and type == 'documentation':
            file.save(os.path.join(app.config['DOCUMENTATION_UPLOAD_FOLDER'], file.filename))
        elif file and type == 'masks':
            file.save(os.path.join(app.config['TRANSLATOR_MASKS_UPLOAD_FOLDER'], file.filename))
        elif file and type == 'dictionaries':
            file.save(os.path.join(app.config['TRANSLATOR_DICTIONARIES_UPLOAD_FOLDER'], file.filename))

    return jsonify({'message': 'Files successfully uploaded'}), 200

@app.route('/list_uploaded_files', methods=['GET'])
def list_uploaded_documentation():

    type = request.args.get('type', '')

    try:
        if(type == 'features'):
            files = os.listdir(FEATURE_UPLOAD_FOLDER)
        elif(type == 'documentation'):
            files = os.listdir(DOCUMENTATION_UPLOAD_FOLDER)
        elif(type == 'masks'):
            files = os.listdir(TRANSLATOR_MASKS_UPLOAD_FOLDER)
        elif(type == 'dictionaries'):
            files = os.listdir(TRANSLATOR_DICTIONARIES_UPLOAD_FOLDER)
        return jsonify({'files': files}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 

@app.route('/delete_file', methods=['POST'])
def delete_file():

    type = request.args.get('type', '')

    try:
        file_name = request.json.get('file_name')
        if not file_name:
            return jsonify({'error': 'No file name provided'}), 400

        if(type == 'feature'):
            file_path = os.path.join(FEATURE_UPLOAD_FOLDER, file_name)
        elif(type == 'documentation'):
            file_path = os.path.join(DOCUMENTATION_UPLOAD_FOLDER, file_name)

        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({'message': f'{file_name} deleted successfully'}), 200
        else:
            return jsonify({'error': 'File not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload_file_for_editing', methods=['POST'])
def upload_file_for_editing():

    file = request.files.get('file')

    if file:
        file_content = file.read().decode('utf-8')
        return jsonify({'content': file_content}) 
    
    return jsonify({'error': 'No file uploaded'}), 400

@app.route('/save_edited_file', methods=['POST'])
def save_edited_file():

    operation_type = request.args.get('type', '')

    data = request.get_json()
    content = data.get('content')
    name = data.get('name')
    new_name = data.get('new_name')  

    if not content:
        return jsonify({'error': 'No content provided'}), 400

    if operation_type == 'save':
        if not name:
            return jsonify({'error': 'File name not provided for save'}), 400

        file_path = os.path.join('editor', name)
        with open(file_path, 'w') as f:
            f.write(content)
        return jsonify({'message': 'File saved successfully'})

    elif operation_type == 'save_as':
        new_name = data.get('new_name')  
        if not new_name:
            return jsonify({'error': 'New file name not provided for save_as'}), 400

        file_path = os.path.join('editor', new_name)
        with open(file_path, 'w') as f:
            f.write(content)
        return jsonify({'message': f'File saved as {new_name} successfully'})

    return jsonify({'error': 'Invalid operation type'}), 400

@app.route('/run_test', methods=['GET'])
def run_test():
    tags = request.args.get('tags', '')

    report_html_url = url_for('static', filename='reports/report.html')
    report_json_url = url_for('static', filename='reports/.report.json')

    return Response(generate_output(tags, report_html_url, report_json_url), mimetype='text/event-stream')

@app.route('/stop_test', methods=['POST'])
def stop_test():
    if pytest_process and pytest_process.poll() is None:
        pytest_process.terminate()
        pytest_process = None
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "No running process found."})

@app.route('/report.html')
def download_report_html():
    return send_from_directory(directory=os.getcwd(), path='report.html')

@app.route('/report.json')
def download_report_json():
    return send_from_directory(directory=os.getcwd(), path='report.json')

@app.route('/generate_feature', methods=['POST'])
def generate_feature():
    try:
        data = request.get_json()
        selectedPaths = data.get('paths', '')
        selectedFiles = data.get('file', '')

        if not selectedFiles:
            return jsonify({'error': 'No files selected for translation'}), 400
        
        command = f"python generic_api_testing/generator/GenerateFeature.py {selectedFiles} {selectedPaths}"
        print(f"Executing command: {command}")

        os.system(command)

        return jsonify({'message': 'Translation started successfully!'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/translate_feature', methods=['POST'])
def translate_feature():
    try:
        data = request.get_json()
        selected_files = data.get('files', [])

        if not selected_files:
            return jsonify({'error': 'No files selected for translation'}), 400

        selectedFiles = ' '.join(f'"{file}"' for file in selected_files)
        command = f"python generic_api_testing/translator/FeatureTranslator.py {selectedFiles}"
        print(f"Executing command: {command}")

        os.system(command)

        return jsonify({'message': 'Translation started successfully!'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/glossary')
def glossary():
    return render_template(
    'glossary.html',
    title="Glossary - AT4QA Project"
    )

if __name__ == '__main__':
    app.run(debug=True)

def generate_output(tags, report_html_url, report_json_url):
    try:
        command = ["pytest", "generic_api_testing/tester/step_defs/custom/test_Custom.py"]
        if tags:
            command.append(f"-m {tags}")

        pytest_process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

        for line in iter(pytest_process.stdout.readline, ''):
            yield f"data: {line}\n\n"

        pytest_process.stdout.close()
        pytest_process.wait()

        if pytest_process.returncode == 0:
            yield "data: Tests completed successfully!\n\n"
        else:
            yield "data: Tests failed!\n\n"

        report_html_path = os.path.join('static', 'reports', 'report.html')
        report_json_path = os.path.join('static', 'reports', '.report.json')

        if os.path.exists(report_html_path) and os.path.exists(report_json_path):
            yield f"data: Report available: {report_html_url}\n\n"
            yield f"data: Report available: {report_json_url}\n\n"
        else:
            yield "data: No report files found.\n\n"

        yield "event: end\ndata: end\n\n"

    except Exception as e:
        yield f"data: Error: {str(e)}\n\n"