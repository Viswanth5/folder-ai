from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from main_model import FolderAIBrain
from folder_generator import FolderGenerator
import os
import zipfile
from io import BytesIO

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes (needed if frontend is served from another port)

brain = FolderAIBrain()
generator = FolderGenerator()

# Resolve absolute path to templates and generated project directories
base_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(base_dir, '..', 'templates')
generated_project_dir = os.path.abspath(os.path.join(base_dir, '..', 'generated_project'))

# Set up logging to a file in the workspace
import logging
log_file = os.path.join(base_dir, 'server.log')
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
)

@app.before_request
def log_request_info():
    print(f"DEBUG REQUEST: {request.method} {request.url}", flush=True)
    app.logger.debug(f"Request: {request.method} {request.url} - Headers: {dict(request.headers)}")

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error("Unhandled Exception caught in global handler", exc_info=e)
    return jsonify({"error": str(e), "success": False}), 500

# Serve the frontend (index.html) at the root route
@app.route('/')
def index():
    return send_from_directory(templates_dir, 'index.html')

# Generate folder structure from prompt
@app.route("/generate", methods=["POST", "OPTIONS"])
def generate():
    if request.method == "OPTIONS":
        return '', 200
    data = request.json
    prompt = data.get("prompt", "")
    result = brain.generate(prompt)
    structure = result["structure"]
    
    # Clean up previous generated folders to prevent files bleeding into new projects
    import shutil
    shutil.rmtree(generated_project_dir, ignore_errors=True)
    
    # Create actual folder structure on disk
    generator.create_structure(structure, base_path=generated_project_dir)
    return jsonify({
        "success": True,
        "parsed_prompt": result["parsed_prompt"],
        "structure": structure
    })

# Download the generated folder as a ZIP archive
@app.route("/download", methods=["GET", "POST"])
def download_project():
    import json as json_module

    if request.method == "POST":
        structure = None
        # Support both JSON body and form-encoded data
        if request.is_json:
            data = request.json or {}
            structure = data.get("structure")
        else:
            structure_json = request.form.get("structure_json")
            if structure_json:
                structure = json_module.loads(structure_json)

        if structure:
            import shutil
            shutil.rmtree(generated_project_dir, ignore_errors=True)
            generator.create_structure(structure, base_path=generated_project_dir)

    folder_path = generated_project_dir
    if not os.path.exists(folder_path):
        return jsonify({"error": "No project generated yet. Please generate first."}), 404

    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(folder_path):
            for d in dirs:
                dir_path = os.path.join(root, d)
                arcname = os.path.relpath(dir_path, folder_path).replace("\\", "/") + '/'
                zf.write(dir_path, arcname)
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path).replace("\\", "/")
                zf.write(file_path, arcname)
    memory_file.seek(0)
    return send_file(
        memory_file,
        mimetype='application/zip',
        download_name="generated_project.zip",
        as_attachment=True
    )

# Optional: serve any other static files (if needed)
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(templates_dir, filename)

if __name__ == "__main__":
    app.run(debug=True)