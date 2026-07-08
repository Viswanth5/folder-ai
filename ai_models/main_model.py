import os
import pickle
from prompt_understanding import PromptUnderstandingModel
from structure_generator import StructureGeneratorModel
from template_recommender import TemplateRecommendationModel

class FolderAIBrain:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        models_dir = os.path.join(base_dir, 'models')
        
        # Load prompt model
        prompt_pkl = os.path.join(models_dir, 'prompt_model.pkl')
        if os.path.exists(prompt_pkl):
            try:
                with open(prompt_pkl, 'rb') as f:
                    self.prompt_model = pickle.load(f)
            except Exception:
                self.prompt_model = PromptUnderstandingModel()
        else:
            self.prompt_model = PromptUnderstandingModel()
            
        # Load structure model
        structure_pkl = os.path.join(models_dir, 'structure_model.pkl')
        if os.path.exists(structure_pkl):
            try:
                with open(structure_pkl, 'rb') as f:
                    self.structure_model = pickle.load(f)
            except Exception:
                self.structure_model = StructureGeneratorModel()
        else:
            self.structure_model = StructureGeneratorModel()
            
        # Load recommender model
        recommender_pkl = os.path.join(models_dir, 'recommender.pkl')
        if os.path.exists(recommender_pkl):
            try:
                with open(recommender_pkl, 'rb') as f:
                    self.recommender = pickle.load(f)
            except Exception:
                self.recommender = TemplateRecommendationModel()
        else:
            self.recommender = TemplateRecommendationModel()

    def generate(self, prompt: str):

        parsed = self.prompt_model.parse_prompt(prompt)

        recommendation = self.recommender.recommend(
            prompt,
            top_k=1
        )

        structure = self.structure_model.generate_structure(
            parsed
        )

        return {
            "parsed_prompt": parsed,
            "recommended_template": recommendation,
            "structure": structure
        }


if __name__ == "__main__":

    ai = FolderAIBrain()

    result = ai.generate(
        "Create MERN stack with authentication and dashboard"
    )

    import json
    print(json.dumps(result, indent=2))