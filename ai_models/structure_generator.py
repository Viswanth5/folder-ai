import json
from typing import Dict, Any, List

class StructureGeneratorModel:
    """
    Generates a folder and file hierarchy based on parsed project requirements.
    Uses predefined templates and merges them based on requested features.
    """
    
    def __init__(self):
        self.templates = self.load_templates()
        
    def load_templates(self) -> Dict[str, Any]:
        """Load base folder structure templates for different technologies."""
        return {
            "React": {
                "src": {
                    "components": {},
                    "pages": {},
                    "assets": {},
                    "App.jsx": None,
                    "main.jsx": None
                },
                "public": {
                    "index.html": None,
                    "favicon.ico": None
                },
                "package.json": None,
                "vite.config.js": None
            },
            "Vue": {
                "src": {
                    "components": {},
                    "views": {},
                    "router": {},
                    "store": {},
                    "App.vue": None,
                    "main.js": None
                },
                "public": {
                    "index.html": None
                },
                "package.json": None,
                "vite.config.js": None
            },
            "Angular": {
                "src": {
                    "app": {
                        "components": {},
                        "app.component.ts": None,
                        "app.module.ts": None
                    },
                    "assets": {},
                    "index.html": None,
                    "main.ts": None
                },
                "angular.json": None,
                "package.json": None
            },
            "Svelte": {
                "src": {
                    "components": {},
                    "App.svelte": None,
                    "main.js": None
                },
                "package.json": None,
                "vite.config.js": None
            },
            "Next.js": {
                "app": {
                    "components": {},
                    "layout.js": None,
                    "page.js": None
                },
                "public": {},
                "package.json": None,
                "next.config.js": None
            },
            "Nuxt": {
                "components": {},
                "pages": {},
                "layouts": {},
                "nuxt.config.js": None,
                "package.json": None
            },
            "Html": {
                "index.html": None,
                "style.css": None,
                "app.js": None
            },
            "Vanilla Js": {
                "index.html": None,
                "style.css": None,
                "app.js": None
            },
            "Node.js": {
                "src": {
                    "controllers": {},
                    "models": {},
                    "routes": {},
                    "app.js": None,
                    "server.js": None
                },
                "package.json": None
            },
            "Express": {
                "src": {
                    "controllers": {},
                    "models": {},
                    "routes": {},
                    "middleware": {},
                    "index.js": None
                },
                "package.json": None
            },
            "Django": {
                "project_name": {
                    "__init__.py": None,
                    "settings.py": None,
                    "urls.py": None,
                    "wsgi.py": None
                },
                "app_name": {
                    "migrations": {},
                    "__init__.py": None,
                    "admin.py": None,
                    "models.py": None,
                    "views.py": None
                },
                "manage.py": None,
                "requirements.txt": None
            },
            "Flask": {
                "app": {
                    "routes.py": None,
                    "models.py": None,
                    "__init__.py": None
                },
                "requirements.txt": None,
                "run.py": None
            },
            "Fastapi": {
                "app": {
                    "api": {},
                    "core": {},
                    "models": {},
                    "schemas": {},
                    "main.py": None
                },
                "requirements.txt": None,
                "Dockerfile": None
            },
            "Spring Boot": {
                "src": {
                    "main": {
                        "java": {
                            "com": {
                                "project": {
                                    "Application.java": None,
                                    "controller": {},
                                    "service": {},
                                    "repository": {},
                                    "model": {}
                                }
                            }
                        },
                        "resources": {
                            "application.properties": None
                        }
                    }
                },
                "pom.xml": None
            },
            "Ruby On Rails": {
                "app": {
                    "controllers": {},
                    "models": {},
                    "views": {},
                    "helpers": {},
                    "mailers": {}
                },
                "config": {
                    "routes.rb": None,
                    "database.yml": None
                },
                "db": {
                    "migrate": {}
                },
                "Gemfile": None
            },
            # Languages
            "Python": {
                "src": {
                    "main.py": None
                },
                "tests": {},
                "requirements.txt": None,
                "README.md": None
            },
            "Go": {
                "cmd": {
                    "main.go": None
                },
                "pkg": {},
                "internal": {},
                "go.mod": None,
                "README.md": None
            },
            "Rust": {
                "src": {
                    "main.rs": None
                },
                "Cargo.toml": None,
                "README.md": None
            },
            "Java": {
                "src": {
                    "main": {
                        "java": {
                            "com": {
                                "project": {
                                    "Main.java": None
                                }
                            }
                        }
                    },
                    "test": {}
                },
                "pom.xml": None,
                "README.md": None
            },
            "Php": {
                "src": {},
                "public": {
                    "index.php": None
                },
                "composer.json": None,
                "README.md": None
            },
            "C#": {
                "src": {
                    "Program.cs": None
                },
                "Project.csproj": None,
                "README.md": None
            },
            "Cpp": {
                "src": {
                    "main.cpp": None
                },
                "include": {},
                "CMakeLists.txt": None,
                "README.md": None
            },
            "C++": {
                "src": {
                    "main.cpp": None
                },
                "include": {},
                "CMakeLists.txt": None,
                "README.md": None
            },
            "C": {
                "src": {
                    "main.c": None
                },
                "include": {},
                "Makefile": None,
                "README.md": None
            },
            "Ruby": {
                "src": {
                    "main.rb": None
                },
                "Gemfile": None,
                "README.md": None
            },
            "Kotlin": {
                "src": {
                    "main": {
                        "kotlin": {
                            "com": {
                                "project": {
                                    "Main.kt": None
                                }
                            }
                        }
                    }
                },
                "build.gradle.kts": None,
                "README.md": None
            },
            "Swift": {
                "Sources": {
                    "main.swift": None
                },
                "Tests": {},
                "Package.swift": None,
                "README.md": None
            },
            "Flutter": {
                "lib": {
                    "main.dart": None,
                    "src": {}
                },
                "android": {},
                "ios": {},
                "pubspec.yaml": None,
                "README.md": None
            },
            "Dart": {
                "bin": {
                    "main.dart": None
                },
                "lib": {},
                "pubspec.yaml": None,
                "README.md": None
            }
        }
        
    def merge_features(self, base_structure: Dict[str, Any], features: List[str], database: str = None) -> Dict[str, Any]:
        """Add specific folders/files based on requested features and database."""
        structure = json.loads(json.dumps(base_structure)) # Deep copy
        
        # 1. Authentication feature
        if "authentication" in features or "auth" in features:
            # Node / Express
            if "src" in structure and isinstance(structure["src"], dict) and any(k in structure["src"] for k in ["controllers", "routes", "models"]):
                if "middleware" not in structure["src"]:
                    structure["src"]["middleware"] = {}
                structure["src"]["middleware"]["auth.js"] = None
                if "controllers" in structure["src"] and isinstance(structure["src"]["controllers"], dict):
                    structure["src"]["controllers"]["authController.js"] = None
                if "routes" in structure["src"] and isinstance(structure["src"]["routes"], dict):
                    structure["src"]["routes"]["authRoutes.js"] = None
            # Go
            elif "cmd" in structure and isinstance(structure["cmd"], dict):
                if "internal" in structure and isinstance(structure["internal"], dict):
                    structure["internal"]["auth"] = {"auth.go": None}
                elif "pkg" in structure and isinstance(structure["pkg"], dict):
                    structure["pkg"]["auth"] = {"auth.go": None}
            # Rust
            elif "Cargo.toml" in structure:
                if "src" in structure and isinstance(structure["src"], dict):
                    structure["src"]["auth.rs"] = None
            # Python standalone
            elif "requirements.txt" in structure and "src" in structure and isinstance(structure["src"], dict):
                structure["src"]["auth.py"] = None
            # Flask
            elif "app" in structure and isinstance(structure["app"], dict):
                structure["app"]["auth.py"] = None
            # FastAPI
            elif "app" in structure and isinstance(structure["app"], dict) and "api" in structure["app"]:
                if isinstance(structure["app"]["api"], dict):
                    structure["app"]["api"]["auth.py"] = None
            # Django
            elif "app_name" in structure and isinstance(structure["app_name"], dict):
                structure["app_name"]["auth.py"] = None
            # PHP
            elif "composer.json" in structure:
                if "src" in structure and isinstance(structure["src"], dict):
                    structure["src"]["Auth.php"] = None
            # C#
            elif "Project.csproj" in structure:
                if "src" in structure and isinstance(structure["src"], dict):
                    structure["src"]["Auth.cs"] = None
            # Spring Boot / Java
            elif "src" in structure:
                try:
                    project_dir = structure["src"]["main"]["java"]["com"]["project"]
                    if isinstance(project_dir, dict):
                        if "config" not in project_dir:
                            project_dir["config"] = {}
                        project_dir["config"]["SecurityConfig.java"] = None
                except KeyError:
                    pass
            # Ruby on Rails / Ruby
            elif "app" in structure and isinstance(structure["app"], dict):
                if "controllers" in structure["app"] and isinstance(structure["app"]["controllers"], dict):
                    if "concerns" not in structure["app"]["controllers"]:
                        structure["app"]["controllers"]["concerns"] = {}
                    structure["app"]["controllers"]["concerns"]["authenticatable.rb"] = None

        # 2. Dashboard feature
        if "dashboard" in features:
            # React/Vue/Svelte
            if "src" in structure and isinstance(structure["src"], dict) and not any(k in structure["src"] for k in ["controllers", "models"]):
                if "pages" in structure["src"] and isinstance(structure["src"]["pages"], dict):
                    structure["src"]["pages"]["Dashboard.jsx"] = None
                elif "views" in structure["src"] and isinstance(structure["src"]["views"], dict):
                    structure["src"]["views"]["Dashboard.vue"] = None
                elif "components" in structure["src"] and isinstance(structure["src"]["components"], dict):
                    structure["src"]["components"]["Dashboard.svelte"] = None
            # Next.js
            elif "app" in structure and isinstance(structure["app"], dict) and "layout.js" in structure["app"]:
                structure["app"]["dashboard"] = {"page.js": None, "layout.js": None}

        # 3. Database integration
        if database:
            db_lower = database.lower()
            # Node / Express
            if "src" in structure and isinstance(structure["src"], dict) and any(k in structure["src"] for k in ["controllers", "routes", "models"]):
                if "config" not in structure["src"]:
                    structure["src"]["config"] = {}
                if "mongodb" in db_lower:
                    structure["src"]["config"]["db.js"] = None
                elif "firebase" in db_lower:
                    structure["src"]["config"]["firebase.js"] = None
                else:
                    structure["src"]["config"]["database.js"] = None
            # Go
            elif "cmd" in structure and isinstance(structure["cmd"], dict):
                if "internal" in structure and isinstance(structure["internal"], dict):
                    structure["internal"]["db"] = {"db.go": None}
                elif "pkg" in structure and isinstance(structure["pkg"], dict):
                    structure["pkg"]["db"] = {"db.go": None}
            # Rust
            elif "Cargo.toml" in structure:
                if "src" in structure and isinstance(structure["src"], dict):
                    structure["src"]["db.rs"] = None
            # Python standalone / Flask / FastAPI
            elif "requirements.txt" in structure or "app" in structure:
                if "src" in structure and isinstance(structure["src"], dict):
                    structure["src"]["database.py"] = None
                elif "app" in structure and isinstance(structure["app"], dict):
                    structure["app"]["database.py"] = None
            # Django
            elif "project_name" in structure and isinstance(structure["project_name"], dict):
                structure["project_name"]["database.py"] = None
            # PHP
            elif "composer.json" in structure:
                if "src" in structure and isinstance(structure["src"], dict):
                    structure["src"]["Database.php"] = None
            # C#
            elif "Project.csproj" in structure:
                if "src" in structure and isinstance(structure["src"], dict):
                    structure["src"]["Database.cs"] = None
            # Spring Boot
            elif "src" in structure:
                try:
                    resources_dir = structure["src"]["main"]["resources"]
                    if isinstance(resources_dir, dict):
                        resources_dir["application-db.properties"] = None
                except KeyError:
                    pass

        return structure

    def generate_structure(self, parsed_prompt: Dict[str, Any]) -> Dict[str, Any]:
        """Generate the final directory structure as a nested dictionary."""
        frontend = parsed_prompt.get("frontend")
        backend = parsed_prompt.get("backend")
        project_type = parsed_prompt.get("project_type")
        database = parsed_prompt.get("database")
        language = parsed_prompt.get("language")
        features = parsed_prompt.get("features", [])
        
        final_structure = {}
        
        # Fallback frontend base template if parsed name is not supported but project_type is fullstack/frontend
        def get_frontend_base():
            if frontend and frontend in self.templates:
                return self.templates[frontend]
            if language in ["Flutter", "Dart"]:
                return self.templates.get(language, {})
            return {
                "src": {
                    "components": {},
                    "App.jsx": None,
                    "main.jsx": None
                },
                "package.json": None
            }

        # Fallback backend base template if parsed name is not supported but project_type is fullstack/backend
        def get_backend_base():
            if backend and backend in self.templates:
                return self.templates[backend]
            if language and language in self.templates:
                return self.templates[language]
            return {
                "src": {
                    "controllers": {},
                    "routes": {},
                    "index.js": None
                },
                "package.json": None
            }
            
        if project_type == "fullstack":
            client_base = get_frontend_base()
            server_base = get_backend_base()
            
            client_struct = self.merge_features(client_base, features, database=None)
            server_struct = self.merge_features(server_base, features, database=database)
            
            final_structure = {
                "client": client_struct,
                "server": server_struct
            }
        elif project_type == "frontend":
            client_base = get_frontend_base()
            final_structure = self.merge_features(client_base, features, database=None)
        elif project_type == "backend":
            server_base = get_backend_base()
            final_structure = self.merge_features(server_base, features, database=database)
        else:
            if language and language in self.templates:
                final_structure = self.merge_features(self.templates[language], features, database=database)
            elif frontend:
                client_base = get_frontend_base()
                final_structure = self.merge_features(client_base, features, database=None)
            elif backend:
                server_base = get_backend_base()
                final_structure = self.merge_features(server_base, features, database=database)
            else:
                final_structure = {
                    "src": {},
                    "README.md": None,
                    "package.json": None
                }
            
        return final_structure

if __name__ == "__main__":
    generator = StructureGeneratorModel()
    sample_parsed = {
        "project_type": "fullstack",
        "frontend": "React",
        "backend": "Node.js",
        "database": "MongoDB",
        "features": ["authentication", "dashboard"]
    }
    
    structure = generator.generate_structure(sample_parsed)
    print(json.dumps(structure, indent=2))
