import os
import pickle
import sys

# Ensure current directory is in python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from prompt_understanding import PromptUnderstandingModel
from structure_generator import StructureGeneratorModel
from template_recommender import TemplateRecommendationModel
from file_classifier import FileClassifier

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(base_dir, 'models')
    
    # Create models folder if it doesn't exist
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
        print(f"Created models directory: {models_dir}")
        
    # Instantiate models
    models = {
        'prompt_model.pkl': PromptUnderstandingModel(),
        'structure_model.pkl': StructureGeneratorModel(),
        'recommender.pkl': TemplateRecommendationModel(),
        'file_classifier.pkl': FileClassifier()
    }
    
    # Pickle each model
    for filename, model_instance in models.items():
        filepath = os.path.join(models_dir, filename)
        with open(filepath, 'wb') as f:
            pickle.dump(model_instance, f)
        print(f"Serialized {model_instance.__class__.__name__} to {filepath}")

if __name__ == '__main__':
    main()
