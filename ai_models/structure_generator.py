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
                    "App.js": None,
                    "index.js": None
                },
                "package.json": None
            },
            "Node.js": {
                "src": {
                    "controllers": {},
                    "models": {},
                    "routes": {},
                    "app.js": None
                },
                "package.json": None
            },
            "Flask": {
                "app": {
                    "routes.py": None,
                    "models.py": None,
                    "__init__.py": None
                },
                "requirements.txt": None
            }
        }
        
    def merge_features(self, base_structure: Dict[str, Any], features: List[str]) -> Dict[str, Any]:
        """Add specific folders/files based on requested features."""
        structure = json.loads(json.dumps(base_structure)) # Deep copy
        
        if "authentication" in features or "auth" in features:
            if "src" in structure and isinstance(structure["src"], dict):
                structure["src"]["middleware"] = {"auth.js": None}
            elif "app" in structure and isinstance(structure["app"], dict): # Flask
                structure["app"]["auth.py"] = None
                
        if "dashboard" in features:
            if "src" in structure and "pages" in structure["src"]:
                structure["src"]["pages"]["Dashboard"] = {"index.js": None}
                
        return structure

    def generate_structure(self, parsed_prompt: Dict[str, Any]) -> Dict[str, Any]:
        """Generate the final directory structure as a nested dictionary."""
        frontend = parsed_prompt.get("frontend")
        backend = parsed_prompt.get("backend")
        project_type = parsed_prompt.get("project_type")
        features = parsed_prompt.get("features", [])
        
        final_structure = {}
        
        if project_type == "fullstack":
            client_base = self.templates.get(frontend, {}) if frontend else {}
            server_base = self.templates.get(backend, {}) if backend else {}
            
            client_struct = self.merge_features(client_base, features)
            server_struct = self.merge_features(server_base, features)
            
            final_structure = {
                "client": client_struct,
                "server": server_struct
            }
        else:
            tech = frontend if frontend else backend
            base = self.templates.get(tech, {}) if tech else {}
            final_structure = self.merge_features(base, features)
            
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
