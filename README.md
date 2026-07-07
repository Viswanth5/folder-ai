# Folder AI | Intelligent Project Structure Generator

Folder AI is an intelligent tool that generates production-ready, custom folder structures, tech stacks, and files from a natural language prompt (e.g., *"i want to create a CRM platform in python full stack"*). 

It generates directory trees dynamically on your local disk in your active workspace, lets you filter files in real-time, and allows you to download the entire project structure as a ZIP archive.

---

## 🛠️ Technology Stack

### Backend (Python 3.12 + Flask)
* **Flask & Flask-CORS**: Web server framework hosting the API and serving the static frontend page.
* **Regular Expressions (Re)**: Custom keyword matching and token processing system for framework and database inference.
* **Zipfile & BytesIO**: On-the-fly zip packaging and memory-stream delivery of file hierarchies.

### Frontend (HTML5 + TailwindCSS + Vanilla JS)
* **TailwindCSS**: Premium responsive layouts.
* **Custom Vanilla CSS**: Glassmorphism elements, dynamic radial gradient grids, and custom animations.
* **GSAP (GreenSock Animation Platform)**: Staggered entry transitions, 3D tilt perspective animations, and custom list slide animations.
* **FontAwesome**: High-end technology and file-type icons.

---

## 📂 Project Directory Structure

```
"folder ai"/
├── ai_models/
│   ├── app.py                      # Flask web server (routing, download handlers, cache prevention)
│   ├── prompt_understanding.py     # NLP logic (archetype detection, fullstack inference, tech parsing)
│   ├── structure_generator.py      # Code templates for 15+ languages and frameworks (Flask, React, etc.)
│   ├── folder_generator.py         # Recursive disk builder (creates folders & files on local disk)
│   ├── template_recommender.py     # TF-IDF template recommender
│   ├── file_classifier.py          # Helper for identifying file extensions
│   ├── tree_parser.py              # Directory parser utilities
│   ├── utils.py                    # Helper utilities
│   └── server.log                  # Global exception and server log file (ignored by Git)
├── templates/
│   └── index.html                  # Responsive, premium front-end UI
├── generated_project/              # Folder created dynamically on disk when a project is generated
├── .gitignore                      # Git exclusion rules (ignores caches, temp files, and logs)
└── README.md                       # Comprehensive project documentation
```

---

## ⚙️ How the Core Components Work

### 1. Natural Language Parser (`prompt_understanding.py`)
This script uses a rule-based engine to analyze prompts:
* **Archetype Recognition**: Matches keywords like `crm`, `ecommerce`, `saas`, or `chat` and automatically extracts the required features (e.g., dashboard, database config, authentication, stripe integrations).
* **Framework Auto-Inference**: If you say *"python full stack"*, it infers **Flask** for the backend, **React** for the frontend, and **PostgreSQL** for the database.
* **Intent Classifier**: Identifies whether the project should be `fullstack`, `frontend`, `backend`, or a standalone language project.

### 2. Template Database (`structure_generator.py`)
Houses predefined structures for multiple technologies:
* **Frontend**: React, Vue, Angular, Svelte, Next.js.
* **Backend**: Express (Node), Django, Flask, FastAPI, Spring Boot, Ruby on Rails.
* **Languages**: Python, Go, Rust, Java, Php, C#, C++, C, Swift, Kotlin, Dart, Flutter.
* **Merge Logic**: Adds dynamic configuration files, auth controllers, database connectors, and mock readmes based on the parsed requirements.

### 3. Web Service & Download Flow (`app.py`)
* **Endpoint `/generate` (POST)**: Receives prompt text, parses it, cleans up the previous `generated_project/` folder at the root level, and creates the fresh directory structure on disk.
* **Endpoint `/download` (POST)**: Receives the selected tree structure from the frontend, compiles the matching directories/files on disk, packages them into a `.zip` archive using `zipfile.ZIP_DEFLATED`, and serves it to the browser as a download attachment with cache-prevention headers.

---

## 🚀 How to Run the Project

1. **Start the Flask Server**:
   Navigate to the `ai_models` directory and run the server script:
   ```bash
   cd ai_models
   python app.py
   ```
   The server will start on **`http://127.0.0.1:5000/`**.

2. **Open the Interface**:
   Open your browser and navigate to **`http://127.0.0.1:5000/`**.

3. **Generate a Structure**:
   * Enter a project description (e.g., *"i want to create a CRM platform in python full stack"*).
   * Click **Generate**.
   * The directory structure will instantly appear in the browser tree *and* be created on your local disk at `d:\Projects\folder ai\generated_project`.
   * Click the green **Download** button to download the project folder structure as a ZIP archive.
