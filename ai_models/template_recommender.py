import json
import math
from collections import Counter
from typing import List, Dict, Any

class TemplateRecommendationModel:
    """
    Recommends project templates based on project intent and features.
    Uses TF-IDF and Cosine Similarity to find the best match.
    """
    
    def __init__(self):
        # Sample templates corpus
        self.templates = [
            {"id": "flask_ai", "name": "Flask AI Template", "tags": ["python", "flask", "ai", "machine learning", "backend", "api"]},
            {"id": "mern", "name": "MERN Stack Template", "tags": ["mongodb", "express", "react", "node.js", "fullstack", "dashboard", "authentication"]},
            {"id": "django_webapp", "name": "Django Web App", "tags": ["python", "django", "fullstack", "postgresql", "authentication"]},
            {"id": "flutter_mobile", "name": "Flutter Mobile App", "tags": ["dart", "flutter", "mobile", "ios", "android", "cross-platform"]},
            {"id": "nextjs_portfolio", "name": "Next.js Portfolio", "tags": ["react", "next.js", "frontend", "portfolio", "ssg", "tailwindcss"]}
        ]
        self.tfidf_vectors: List[Dict[str, float]] = []
        self.idf: Dict[str, float] = {}
        
        # Auto-train on init
        self.train()
        
    def _compute_tf(self, document: List[str]) -> Dict[str, float]:
        tf_dict = {}
        doc_len = len(document)
        if doc_len == 0:
            return tf_dict
        counts = Counter(document)
        for word, count in counts.items():
            tf_dict[word] = count / float(doc_len)
        return tf_dict

    def _compute_idf(self, documents: List[List[str]]) -> Dict[str, float]:
        idf_dict = {}
        N = len(documents)
        all_words = set(word for doc in documents for word in doc)
        
        for word in all_words:
            containing_docs = sum(1 for doc in documents if word in doc)
            idf_dict[word] = math.log10(N / float(containing_docs))
            
        return idf_dict
        
    def train(self) -> None:
        """Train the TF-IDF model on the available templates."""
        documents = [t["tags"] for t in self.templates]
        self.idf = self._compute_idf(documents)
        
        self.tfidf_vectors = []
        for doc in documents:
            tf = self._compute_tf(doc)
            tfidf = {word: tf[word] * self.idf.get(word, 0) for word in doc}
            self.tfidf_vectors.append(tfidf)
            
    def _cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        intersection = set(vec1.keys()) & set(vec2.keys())
        if not intersection:
            return 0.0
            
        dot_product = sum(vec1[w] * vec2[w] for w in intersection)
        sum1 = sum(val**2 for val in vec1.values())
        sum2 = sum(val**2 for val in vec2.values())
        
        if sum1 == 0 or sum2 == 0:
            return 0.0
            
        return dot_product / (math.sqrt(sum1) * math.sqrt(sum2))
        
    def recommend(self, intent_description: str, top_k: int = 1) -> List[Dict[str, Any]]:
        """Recommend templates based on an intent query."""
        query_tokens = intent_description.lower().split()
        
        query_tf = self._compute_tf(query_tokens)
        query_tfidf = {word: query_tf[word] * self.idf.get(word, 0) for word in query_tokens if word in self.idf}
        
        scores = []
        for i, doc_vector in enumerate(self.tfidf_vectors):
            score = self._cosine_similarity(query_tfidf, doc_vector)
            scores.append((score, self.templates[i]))
            
        scores.sort(key=lambda x: x[0], reverse=True)
        
        results = []
        for score, template in scores[:top_k]:
            results.append({
                "template_id": template["id"],
                "template_name": template["name"],
                "score": round(score, 4)
            })
            
        return results

if __name__ == "__main__":
    recommender = TemplateRecommendationModel()
    
    queries = [
        "AI project with machine learning and python",
        "react node.js fullstack with authentication",
        "mobile cross-platform app"
    ]
    
    for q in queries:
        print(f"Query: '{q}'")
        print(json.dumps(recommender.recommend(q, top_k=1), indent=2))
