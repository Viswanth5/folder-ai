import json
from typing import Dict, Any, List

class StructureGeneratorModel:
    """
    Generates a folder and file hierarchy based on parsed project requirements.
    Uses predefined templates and merges them based on requested features.
    """
    
    def __init__(self):
        pass

    def generate_frontend_structure(self, frontend_name: str, features: List[str], raw_prompt: str) -> Dict[str, Any]:
        struct = {}
        raw_lower = raw_prompt.lower()
        
        # Check if Next.js
        if (frontend_name and "next" in frontend_name.lower()) or "next" in raw_lower:
            app_dir = {
                "layout.js": None,
                "page.js": None
            }
            # Custom routes/pages based on features / prompt words
            if "dashboard" in raw_lower or "dashboard" in features:
                app_dir["dashboard"] = {
                    "page.js": None,
                    "layout.js": None
                }
            if "auth" in raw_lower or "authentication" in features:
                app_dir["auth"] = {
                    "login": { "page.js": None },
                    "register": { "page.js": None }
                }
            if "ecommerce" in raw_lower or "e-commerce" in raw_lower or "shop" in raw_lower or "store" in raw_lower:
                app_dir["products"] = {
                    "page.js": None,
                    "[id]": { "page.js": None }
                }
                app_dir["cart"] = { "page.js": None }
                app_dir["checkout"] = { "page.js": None }
            if "portfolio" in raw_lower:
                app_dir["projects"] = { "page.js": None }
                app_dir["contact"] = { "page.js": None }
            if "chat" in raw_lower:
                app_dir["chat"] = { "page.js": None }
                
            struct["app"] = app_dir
            
            components = {}
            if "ecommerce" in raw_lower or "e-commerce" in raw_lower or "shop" in raw_lower or "store" in raw_lower:
                components["ProductCard.js"] = None
                components["CartIcon.js"] = None
            if "auth" in raw_lower or "authentication" in features:
                components["LoginForm.js"] = None
            if "chat" in raw_lower:
                components["ChatWindow.js"] = None
                components["Message.js"] = None
            if "portfolio" in raw_lower:
                components["ProjectCard.js"] = None
                components["Hero.js"] = None
            components["Navbar.js"] = None
            components["Footer.js"] = None
            struct["components"] = components
            
            struct["public"] = {
                "favicon.ico": None,
                "images": {}
            }
            struct["package.json"] = None
            struct["next.config.js"] = None
            struct["jsconfig.json"] = None
            struct["README.md"] = None
            
        elif (frontend_name in ["React", "Vue", "Angular", "Svelte"] or 
              (frontend_name is None and ("react" in raw_lower or "vue" in raw_lower or "svelte" in raw_lower))):
            
            src = {
                "components": {},
                "assets": {}
            }
            
            # Pages or Views based on features
            pages = {}
            is_vue = "vue" in str(frontend_name).lower() or "vue" in raw_lower
            is_svelte = "svelte" in str(frontend_name).lower() or "svelte" in raw_lower
            
            ext = "vue" if is_vue else ("svelte" if is_svelte else "jsx")
            pages[f"Home.{ext}"] = None
            
            if "dashboard" in raw_lower or "dashboard" in features:
                pages[f"Dashboard.{ext}"] = None
            if "auth" in raw_lower or "authentication" in features:
                pages[f"Login.{ext}"] = None
                pages[f"Register.{ext}"] = None
            if "ecommerce" in raw_lower or "e-commerce" in raw_lower or "shop" in raw_lower or "store" in raw_lower:
                pages[f"Products.{ext}"] = None
                pages[f"Cart.{ext}"] = None
            if "chat" in raw_lower:
                pages[f"Chat.{ext}"] = None
            if "portfolio" in raw_lower:
                pages[f"Portfolio.{ext}"] = None
                
            src["views" if is_vue else "pages"] = pages
            
            # Components
            components = src["components"]
            components[f"Navbar.{ext}"] = None
            components[f"Footer.{ext}"] = None
            if "auth" in raw_lower or "authentication" in features:
                components[f"AuthGuard.{ext}"] = None
            if "ecommerce" in raw_lower or "e-commerce" in raw_lower or "shop" in raw_lower or "store" in raw_lower:
                components[f"ProductList.{ext}"] = None
            if "chat" in raw_lower:
                components[f"MessageInput.{ext}"] = None
                components[f"MessageList.{ext}"] = None
                
            # App entry points
            if is_vue:
                src["App.vue"] = None
                src["main.js"] = None
                struct["vite.config.js"] = None
            elif is_svelte:
                src["App.svelte"] = None
                src["main.js"] = None
                struct["vite.config.js"] = None
            else: # React
                src["App.jsx"] = None
                src["main.jsx"] = None
                src["index.css"] = None
                struct["vite.config.js"] = None
                
            struct["src"] = src
            struct["public"] = {
                "index.html": None,
                "favicon.ico": None
            }
            struct["package.json"] = None
            struct["README.md"] = None
            
        elif "flutter" in raw_lower or "dart" in raw_lower or frontend_name in ["Flutter", "Dart"]:
            lib = {
                "main.dart": None,
                "models": {},
                "screens": {},
                "widgets": {}
            }
            screens = lib["screens"]
            screens["home_screen.dart"] = None
            if "auth" in raw_lower or "authentication" in features:
                screens["login_screen.dart"] = None
            if "chat" in raw_lower:
                screens["chat_screen.dart"] = None
                lib["widgets"]["message_bubble.dart"] = None
                lib["widgets"]["message_input.dart"] = None
            if "ecommerce" in raw_lower or "e-commerce" in raw_lower or "shop" in raw_lower or "store" in raw_lower:
                screens["catalog_screen.dart"] = None
                screens["cart_screen.dart"] = None
            if "dashboard" in raw_lower or "dashboard" in features:
                screens["dashboard_screen.dart"] = None
                
            struct["lib"] = lib
            struct["pubspec.yaml"] = None
            struct["README.md"] = None
            struct["android"] = {}
            struct["ios"] = {}
            
        else: # Generic HTML/CSS/JS frontend
            struct["index.html"] = None
            struct["style.css"] = None
            struct["app.js"] = None
            if "portfolio" in raw_lower:
                struct["portfolio.js"] = None
            if "auth" in raw_lower or "authentication" in features:
                struct["auth.js"] = None
            struct["README.md"] = None
            
        return struct

    def generate_backend_structure(self, backend_name: str, database_name: str, features: List[str], raw_prompt: str) -> Dict[str, Any]:
        struct = {}
        raw_lower = raw_prompt.lower()
        
        # Flask
        if backend_name == "Flask" or (backend_name is None and "flask" in raw_lower):
            app_dir = {
                "__init__.py": None,
                "routes.py": None,
                "models.py": None
            }
            if "auth" in raw_lower or "authentication" in features:
                app_dir["auth.py"] = None
            if "ai" in raw_lower or "machine learning" in raw_lower or "ml" in raw_lower:
                app_dir["ai_model.py"] = None
                app_dir["prediction.py"] = None
            if database_name:
                app_dir["database.py"] = None
                
            struct["app"] = app_dir
            struct["requirements.txt"] = None
            struct["run.py"] = None
            struct["config.py"] = None
            struct["README.md"] = None
            
        # FastAPI
        elif backend_name == "Fastapi" or backend_name == "FastAPI" or "fastapi" in raw_lower:
            app_dir = {
                "main.py": None,
                "config.py": None,
                "database.py": None,
                "models.py": None,
                "schemas.py": None,
                "routers": {
                    "items.py": None
                }
            }
            if "auth" in raw_lower or "authentication" in features:
                app_dir["routers"]["auth.py"] = None
            if "ai" in raw_lower or "machine learning" in raw_lower or "ml" in raw_lower:
                app_dir["routers"]["predict.py"] = None
                app_dir["ai_model.py"] = None
                
            struct["app"] = app_dir
            struct["requirements.txt"] = None
            struct["README.md"] = None
            struct["Dockerfile"] = None
            
        # Django
        elif backend_name == "Django" or "django" in raw_lower:
            struct["manage.py"] = None
            struct["requirements.txt"] = None
            struct["README.md"] = None
            
            project_name = "myproject"
            struct[project_name] = {
                "__init__.py": None,
                "settings.py": None,
                "urls.py": None,
                "wsgi.py": None
            }
            
            app_name = "myapp"
            struct[app_name] = {
                "migrations": {},
                "__init__.py": None,
                "admin.py": None,
                "apps.py": None,
                "models.py": None,
                "views.py": None,
                "urls.py": None
            }
            if "ai" in raw_lower or "machine learning" in raw_lower or "ml" in raw_lower:
                struct[app_name]["ai_services.py"] = None
                
        # Express / Node
        elif backend_name in ["Node.js", "Express"] or "express" in raw_lower or "node" in raw_lower:
            struct["controllers"] = {}
            struct["models"] = {}
            struct["routes"] = {
                "api.js": None
            }
            
            if "auth" in raw_lower or "authentication" in features:
                struct["controllers"]["authController.js"] = None
                struct["models"]["User.js"] = None
                struct["routes"]["authRoutes.js"] = None
                
            if "ecommerce" in raw_lower or "e-commerce" in raw_lower or "shop" in raw_lower or "store" in raw_lower:
                struct["controllers"]["productController.js"] = None
                struct["models"]["Product.js"] = None
                
            if "dashboard" in raw_lower or "dashboard" in features:
                struct["controllers"]["dashboardController.js"] = None
                
            if "chat" in raw_lower:
                struct["controllers"]["chatController.js"] = None
                struct["models"]["Message.js"] = None
                
            struct["app.js"] = None
            struct["package.json"] = None
            struct["README.md"] = None
            if database_name:
                struct["config"] = { "db.js": None }
                
        # Spring Boot
        elif backend_name == "Spring Boot" or "spring" in raw_lower:
            project_dir = {
                "Application.java": None,
                "controller": {},
                "model": {},
                "repository": {},
                "service": {}
            }
            if "auth" in raw_lower or "authentication" in features:
                project_dir["controller"]["AuthController.java"] = None
                project_dir["model"]["User.java"] = None
            if "ai" in raw_lower or "machine learning" in raw_lower or "ml" in raw_lower:
                project_dir["controller"]["PredictionController.java"] = None
                project_dir["service"]["AiService.java"] = None
                
            struct["src"] = {
                "main": {
                    "java": {
                        "com": {
                            "example": {
                                "project": project_dir
                            }
                        }
                    },
                    "resources": {
                        "application.properties": None
                    }
                }
            }
            struct["pom.xml"] = None
            struct["README.md"] = None
            
        # Go
        elif "go" in raw_lower or backend_name == "Go":
            struct["cmd"] = {
                "main.go": None
            }
            struct["pkg"] = {}
            struct["internal"] = {}
            if "auth" in raw_lower or "authentication" in features:
                struct["internal"]["auth"] = { "auth.go": None }
            if "ai" in raw_lower or "machine learning" in raw_lower or "ml" in raw_lower:
                struct["internal"]["ai"] = { "model.go": None }
            struct["go.mod"] = None
            struct["README.md"] = None
            
        # Rust
        elif "rust" in raw_lower or backend_name == "Rust":
            src = {
                "main.rs": None
            }
            if "auth" in raw_lower or "authentication" in features:
                src["auth.rs"] = None
            if "ai" in raw_lower or "machine learning" in raw_lower or "ml" in raw_lower:
                src["ai.rs"] = None
            struct["src"] = src
            struct["Cargo.toml"] = None
            struct["README.md"] = None
            
        # Python standalone (e.g. AI project)
        elif "python" in raw_lower or backend_name == "Python":
            if "ai" in raw_lower or "machine learning" in raw_lower or "ml" in raw_lower or "deep learning" in raw_lower or "neural network" in raw_lower:
                struct["data"] = {}
                struct["models"] = {}
                struct["src"] = {
                    "train.py": None,
                    "predict.py": None,
                    "utils.py": None
                }
                struct["requirements.txt"] = None
                struct["README.md"] = None
            else:
                struct["main.py"] = None
                struct["utils.py"] = None
                struct["requirements.txt"] = None
                struct["README.md"] = None
                
        else: # Generic backend
            struct["app.js"] = None
            struct["package.json"] = None
            struct["README.md"] = None
            
        return struct

    def generate_structure(self, parsed_prompt: Dict[str, Any]) -> Dict[str, Any]:
        frontend = parsed_prompt.get("frontend")
        backend = parsed_prompt.get("backend")
        project_type = parsed_prompt.get("project_type")
        database = parsed_prompt.get("database")
        language = parsed_prompt.get("language")
        features = parsed_prompt.get("features", [])
        raw_prompt = parsed_prompt.get("raw_prompt", "")
        
        if not raw_prompt:
            components = []
            if project_type: components.append(project_type)
            if frontend: components.append(frontend)
            if backend: components.append(backend)
            if database: components.append(database)
            if language: components.append(language)
            components.extend(features)
            raw_prompt = " ".join(components)
            
        raw_lower = raw_prompt.lower()
        
        is_fullstack = (project_type == "fullstack" or 
                        "fullstack" in raw_lower or "full stack" in raw_lower or 
                        "mern" in raw_lower or "mean" in raw_lower or "mevn" in raw_lower or
                        ("react" in raw_lower and "flask" in raw_lower) or
                        ("react" in raw_lower and "express" in raw_lower) or
                        ("react" in raw_lower and "node" in raw_lower) or
                        (frontend is not None and backend is not None))
                        
        if is_fullstack:
            client_struct = self.generate_frontend_structure(frontend, features, raw_prompt)
            server_struct = self.generate_backend_structure(backend, database, features, raw_prompt)
            
            return {
                "client": client_struct,
                "server": server_struct
            }
        
        elif project_type == "frontend" or frontend or "next" in raw_lower or "react" in raw_lower or "vue" in raw_lower or "angular" in raw_lower or "svelte" in raw_lower or "flutter" in raw_lower:
            return self.generate_frontend_structure(frontend or language, features, raw_prompt)
            
        elif project_type == "backend" or backend or "flask" in raw_lower or "fastapi" in raw_lower or "django" in raw_lower or "express" in raw_lower:
            return self.generate_backend_structure(backend, database, features, raw_prompt)
            
        else:
            return self.generate_backend_structure(backend or language, database, features, raw_prompt)

if __name__ == "__main__":
    generator = StructureGeneratorModel()
    sample_parsed = {
        "project_type": "fullstack",
        "frontend": "React",
        "backend": "Node.js",
        "database": "MongoDB",
        "features": ["authentication", "dashboard"],
        "raw_prompt": "Create a MERN Stack project with authentication and dashboard"
    }
    
    structure = generator.generate_structure(sample_parsed)
    print(json.dumps(structure, indent=2))
