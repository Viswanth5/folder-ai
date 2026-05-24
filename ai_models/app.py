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

# Serve the frontend (index.html) at the root route
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Generate folder structure from prompt
@app.route("/generate", methods=["POST", "OPTIONS"])
def generate():
    if request.method == "OPTIONS":
        return '', 200
    data = request.json
    prompt = data.get("prompt", "")
    result = brain.generate(prompt)
    structure = result["structure"]
    # Create actual folder structure on disk
    generator.create_structure(structure)
    return jsonify({
        "success": True,
        "parsed_prompt": result["parsed_prompt"],
        "structure": structure
    })

# Download the generated folder as a ZIP archive
@app.route("/download", methods=["GET"])
def download_project():
    folder_path = "generated_project"
    if not os.path.exists(folder_path):
        return jsonify({"error": "No project generated yet. Please generate first."}), 404

    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zf.write(file_path, arcname)
    memory_file.seek(0)
    return send_file(memory_file, download_name="generated_project.zip", as_attachment=True)

# Optional: serve any other static files (if needed)
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

if __name__ == "__main__":
    app.run(debug=True)