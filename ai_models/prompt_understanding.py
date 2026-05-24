import json
import re
from typing import Dict, Any, List

class PromptUnderstandingModel:
    """
    NLP model to understand natural language prompts and extract 
    project requirements like framework, database, and features.
    Can be extended to use spaCy or transformers for production.
    """
    
    def __init__(self):
        # Simulated knowledge base for entity extraction
        self.knowledge_base = {
            "frontend_framework": ["react", "vue", "angular", "svelte", "next.js", "nuxt", "html", "vanilla js"],
            "backend_framework": ["node.js", "express", "django", "flask", "fastapi", "spring boot", "ruby on rails"],
            "database": ["mongodb", "postgresql", "mysql", "sqlite", "redis", "firebase"],
            "features": ["authentication", "dashboard", "routing", "api", "graphql", "websockets", "payment", "auth"]
        }
    
    def preprocess(self, prompt: str) -> str:
        """Clean and normalize the input prompt."""
        text = prompt.lower().strip()
        # Expand common stack acronyms to help entity extraction
        text = text.replace("mern", "mongodb express react node.js")
        text = text.replace("mean", "mongodb express angular node.js")
        text = text.replace("mevn", "mongodb express vue node.js")
        return text
    
    def extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract technologies and features from the text."""
        entities = {
            "frontend": None,
            "backend": None,
            "database": None,
            "features": []
        }
        
        for category, keywords in self.knowledge_base.items():
            for kw in keywords:
                # Using simple word boundary regex for reliable matching
                if re.search(rf'\b{re.escape(kw)}\b', text):
                    if category == "frontend_framework":
                        entities["frontend"] = kw.title() if kw != "next.js" else "Next.js"
                    elif category == "backend_framework":
                        entities["backend"] = kw.title() if kw != "node.js" else "Node.js"
                    elif category == "database":
                        entities["database"] = kw.title()
                    elif category == "features":
                        if kw not in entities["features"]:
                            entities["features"].append(kw)
                            
        return entities
    
    def predict_intent(self, entities: Dict[str, Any]) -> str:
        """Determine the project type based on extracted entities."""
        has_front = bool(entities["frontend"])
        has_back = bool(entities["backend"])
        
        if has_front and has_back:
            return "fullstack"
        elif has_front:
            return "frontend"
        elif has_back:
            return "backend"
        else:
            return "unknown"
            
    def parse_prompt(self, prompt: str) -> Dict[str, Any]:
        """Full pipeline to parse a prompt into a structured dictionary."""
        clean_text = self.preprocess(prompt)
        entities = self.extract_entities(clean_text)
        project_type = self.predict_intent(entities)
        
        return {
            "project_type": project_type,
            "frontend": entities["frontend"],
            "backend": entities["backend"],
            "database": entities["database"],
            "features": entities["features"]
        }

if __name__ == "__main__":
    model = PromptUnderstandingModel()
    sample_prompt = "Create a MERN stack project with authentication and dashboard"
    print(json.dumps(model.parse_prompt(sample_prompt), indent=2))
