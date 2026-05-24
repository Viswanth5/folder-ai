import json
from typing import Set

class FileClassifier:
    """
    Classifies files into categories (folder, source, config, asset)
    based on their names and extensions.
    """
    
    def __init__(self):
        self.asset_extensions: Set[str] = {
            ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", 
            ".webp", ".mp4", ".mp3", ".ttf", ".woff", ".woff2"
        }
        self.config_files: Set[str] = {
            "package.json", "tsconfig.json", "webpack.config.js", 
            "requirements.txt", "Pipfile", "dockerfile", 
            "docker-compose.yml", "setup.py", ".gitignore", ".env"
        }
        self.source_extensions: Set[str] = {
            ".py", ".js", ".jsx", ".ts", ".tsx", ".java", 
            ".c", ".cpp", ".cs", ".go", ".rs", ".rb", 
            ".php", ".html", ".css", ".scss"
        }
        
    def classify(self, item_name: str, is_folder: bool = False) -> str:
        """
        Classifies an item based on its name and properties.
        """
        if is_folder or item_name.endswith('/'):
            return "folder"
            
        # Often folders are passed without trailing slash
        if "." not in item_name and not item_name.startswith("."):
            # Check if it's a known configuration file with no extension (like Dockerfile)
            if item_name.lower() in [c.lower() for c in self.config_files]:
                return "config"
            return "folder"
            
        name_lower = item_name.lower()
        
        # Check specific config file names
        if name_lower in [c.lower() for c in self.config_files]:
            return "config"
            
        # Check config files by extension
        if any(name_lower.endswith(ext) for ext in [".json", ".yaml", ".yml", ".ini", ".cfg", ".toml", ".xml"]):
            return "config"
            
        # Check assets
        if any(name_lower.endswith(ext) for ext in self.asset_extensions):
            return "asset"
            
        # Check source code
        if any(name_lower.endswith(ext) for ext in self.source_extensions):
            return "source"
            
        # Default fallback
        return "source"

if __name__ == "__main__":
    classifier = FileClassifier()
    test_items = ["package.json", "App.jsx", "src", "logo.png", "main.py", ".gitignore"]
    
    results = {item: classifier.classify(item) for item in test_items}
    print(json.dumps(results, indent=2))
