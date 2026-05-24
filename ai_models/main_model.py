from prompt_understanding import PromptUnderstandingModel
from structure_generator import StructureGeneratorModel
from template_recommender import TemplateRecommendationModel

class FolderAIBrain:
    def __init__(self):
        self.prompt_model = PromptUnderstandingModel()
        self.structure_model = StructureGeneratorModel()
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