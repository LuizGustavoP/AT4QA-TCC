from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)
app.config["FEATURE_FILE_FOLDER"] = "features"
app.config["ALLOWED_FILE_EXTENSIONS"] = ["feature", "mask", "dictionary", "yaml", "json"]

if not os.path.exists(app.config["FEATURE_FILE_FOLDER"]):
  os.makedirs(app.config["FEATURE_FILE_FOLDER"])

def check_file_extension(file):
  return "." in file and file.rsplit(".", 1)[1].lower() in app.config["ALLOWED_FILE_EXTENSIONS"]

@app.route('/')
def homepage():
  return render_template(
    'home.html',
    title="Home - AT4QA Project"
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

@app.route('/test_builder')
def test_builder():
  return render_template(
    'test_builder.html',
    title="Builder - AT4QA Project"
  )

@app.route('/test_runner')
def test_runner():
  return render_template(
    'test_runner.html',
    title="Runner - AT4QA Project"
  )

@app.route('/glossary')
def glossary():
  return render_template(
    'glossary.html',
    title="Glossary - AT4QA Project"
  )

@app.route('/account')
def account():
  return render_template(
    'account.html',
    title="Account - AT4QA Project"
  )

@app.route('/upload_test', methods=["POST"])
def upload_test():
  if request.method == "POST":
    if request.files:
      file = request.files["file"]
      if file.filename == "":
        print("No filename")
        return redirect(request.url)
      if check_file_extension(file.filename):
        file.save(os.path.join(app.config["FEATURE_FILE_FOLDER"], file.filename))
        print("File saved")
        return redirect(request.url)
      else:
        print("File not allowed")
        return redirect(request.url)
  return render_template(
    'builder.html',
    title="Upload File - AT4QA Project"
  )

if __name__ == '__main__':
  app.run(debug=True)