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
            "language": ["python", "go", "rust", "java", "php", "c#", "cpp", "c++", "ruby", "kotlin", "swift", "flutter", "dart", "typescript", "javascript", "c"],
            "features": ["authentication", "dashboard", "routing", "api", "graphql", "websockets", "payment", "auth"]
        }

        # Project archetype patterns that imply specific features
        self.project_archetypes = {
            "crm": ["authentication", "dashboard", "api"],
            "e-commerce": ["authentication", "payment", "api", "dashboard"],
            "ecommerce": ["authentication", "payment", "api", "dashboard"],
            "shop": ["authentication", "payment", "api"],
            "store": ["authentication", "payment", "api"],
            "blog": ["authentication", "api"],
            "portfolio": [],
            "chat": ["authentication", "websockets", "api"],
            "social": ["authentication", "api", "dashboard"],
            "admin": ["authentication", "dashboard", "api"],
            "saas": ["authentication", "payment", "dashboard", "api"],
            "todo": ["authentication", "api"],
            "task manager": ["authentication", "dashboard", "api"],
            "inventory": ["authentication", "dashboard", "api"],
            "booking": ["authentication", "payment", "api", "dashboard"],
            "learning": ["authentication", "dashboard", "api"],
            "lms": ["authentication", "dashboard", "api"],
            "hospital": ["authentication", "dashboard", "api"],
            "management": ["authentication", "dashboard", "api"],
        }

        # Default framework inference: when user says a language + "full stack" but no framework
        self.language_to_backend = {
            "Python": "Flask",
            "Javascript": "Express",
            "Typescript": "Express",
            "Java": "Spring Boot",
            "Ruby": "Ruby On Rails",
            "Php": "Flask",  # fallback
            "Go": "Express",  # fallback
        }

        self.language_to_frontend = {
            "Python": "React",
            "Javascript": "React",
            "Typescript": "React",
            "Java": "React",
            "Ruby": "React",
            "Php": "React",
            "Go": "React",
        }

        self.language_to_database = {
            "Python": "Postgresql",
            "Javascript": "Mongodb",
            "Typescript": "Mongodb",
            "Java": "Mysql",
            "Ruby": "Postgresql",
            "Php": "Mysql",
            "Go": "Postgresql",
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
            "language": None,
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
                    elif category == "language":
                        entities["language"] = kw.title() if kw != "c#" else "C#"
                    elif category == "features":
                        if kw not in entities["features"]:
                            entities["features"].append(kw)
                            
        return entities

    def detect_fullstack_intent(self, text: str) -> bool:
        """Check if the prompt implies a full stack project."""
        fullstack_patterns = [
            r'\bfull\s*stack\b', r'\bfullstack\b',
            r'\bfront\s*end\s+and\s+back\s*end\b',
            r'\bweb\s+app\b', r'\bweb\s+application\b',
            r'\bplatform\b', r'\bportal\b',
        ]
        for pattern in fullstack_patterns:
            if re.search(pattern, text):
                return True
        return False

    def detect_archetype_features(self, text: str) -> List[str]:
        """Detect project archetype keywords and return implied features."""
        features = []
        for archetype, implied_features in self.project_archetypes.items():
            if re.search(rf'\b{re.escape(archetype)}\b', text):
                for f in implied_features:
                    if f not in features:
                        features.append(f)
        return features

    def predict_intent(self, entities: Dict[str, Any], text: str) -> str:
        """Determine the project type based on extracted entities and text."""
        has_front = bool(entities["frontend"])
        has_back = bool(entities["backend"])
        has_lang = bool(entities["language"])
        
        # Explicit fullstack intent from the prompt text
        if self.detect_fullstack_intent(text):
            return "fullstack"
        
        if has_front and has_back:
            return "fullstack"
        elif has_front:
            return "frontend"
        elif has_back:
            return "backend"
        elif has_lang:
            if entities["language"] in ["Flutter", "Dart"]:
                return "frontend"
            return "backend"
        else:
            return "unknown"

    def infer_frameworks(self, entities: Dict[str, Any], project_type: str, text: str) -> Dict[str, Any]:
        """Auto-infer frontend/backend frameworks when user only specifies a language + fullstack intent."""
        lang = entities["language"]

        # If fullstack but no backend framework specified, infer from language
        if project_type == "fullstack":
            if not entities["backend"] and lang:
                entities["backend"] = self.language_to_backend.get(lang, "Flask")
            if not entities["frontend"] and lang:
                entities["frontend"] = self.language_to_frontend.get(lang, "React")
            if not entities["database"] and lang:
                entities["database"] = self.language_to_database.get(lang, "Postgresql")
        
        # If backend but no framework, infer from language
        elif project_type == "backend":
            if not entities["backend"] and lang:
                entities["backend"] = self.language_to_backend.get(lang)
        
        return entities
            
    def parse_prompt(self, prompt: str) -> Dict[str, Any]:
        """Full pipeline to parse a prompt into a structured dictionary."""
        clean_text = self.preprocess(prompt)
        entities = self.extract_entities(clean_text)

        # Detect archetype features (crm, e-commerce, etc.)
        archetype_features = self.detect_archetype_features(clean_text)
        for f in archetype_features:
            if f not in entities["features"]:
                entities["features"].append(f)

        project_type = self.predict_intent(entities, clean_text)

        # Auto-infer frameworks when language is known but framework is not
        entities = self.infer_frameworks(entities, project_type, clean_text)
        
        return {
            "project_type": project_type,
            "frontend": entities["frontend"],
            "backend": entities["backend"],
            "database": entities["database"],
            "language": entities["language"],
            "features": entities["features"]
        }

if __name__ == "__main__":
    model = PromptUnderstandingModel()
    test_prompts = [
        "Create a MERN stack project with authentication and dashboard",
        "i want to create a CRM platform in python full stack",
        "python full stack web application for an crm platform",
        "Build a Flask + React fullstack app with PostgreSQL",
        "simple todo app in javascript",
    ]
    for p in test_prompts:
        print(f"\nPrompt: '{p}'")
        print(json.dumps(model.parse_prompt(p), indent=2))

