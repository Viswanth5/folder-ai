import os
from typing import Dict, Any

class FolderGenerator:

    def create_structure(
        self,
        structure: Dict[str, Any],
        base_path: str = "generated_project"
    ):

        os.makedirs(base_path, exist_ok=True)

        self._create_recursive(
            structure,
            base_path
        )

    def _create_recursive(
        self,
        structure,
        current_path
    ):

        for name, content in structure.items():

            path = os.path.join(
                current_path,
                name
            )

            if isinstance(content, dict):

                os.makedirs(
                    path,
                    exist_ok=True
                )

                self._create_recursive(
                    content,
                    path
                )

            else:

                open(
                    path,
                    "w"
                ).close()


if __name__ == "__main__":

    sample = {

        "client":{

            "src":{
                "App.jsx":None,
                "index.js":None
            },

            "package.json":None
        },

        "server":{

            "app.py":None
        }
    }

    generator = FolderGenerator()

    generator.create_structure(sample)

    print("Folders generated")