import json
import re
from typing import Dict, Any, List, Tuple

class TreeParserModel:
    """
    Parses a string representing a directory tree into a nested JSON/dictionary structure.
    """
    
    def __init__(self):
        pass
        
    def clean_input(self, tree_text: str) -> List[str]:
        """Clean the input text and split into non-empty lines."""
        lines = tree_text.strip().split('\n')
        return [line for line in lines if line.strip()]
        
    def parse_line(self, line: str) -> Tuple[int, str, bool]:
        """
        Parse a single line to determine its depth, name, and if it's a folder.
        """
        # Match standard tree prefixes like "├── ", "│   └── ", etc.
        prefix_match = re.match(r'^[\s│├└─]*', line)
        prefix = prefix_match.group(0) if prefix_match else ""
        
        # Calculate visual depth assuming 4 characters per level
        depth = len(prefix) // 4
        
        name = line[len(prefix):].strip()
        
        is_folder = name.endswith('/')
        if is_folder:
            name = name[:-1]
            
        # Infer folder if it has no extension (no dot) and not explicitly checked
        if not is_folder and "." not in name:
            is_folder = True
            
        return depth, name, is_folder

    def build_tree(self, tree_text: str) -> Dict[str, Any]:
        """Convert the tree text into a nested dictionary."""
        lines = self.clean_input(tree_text)
        if not lines:
            return {}
            
        root_tree = {}
        # Keep track of the dictionary references at each depth
        depth_map = {-1: root_tree}
        
        for line in lines:
            depth, name, is_folder = self.parse_line(line)
            
            parent_depth = depth - 1
            # Find the nearest valid parent depth if there's a malformed jump
            while parent_depth not in depth_map and parent_depth > -1:
                parent_depth -= 1
                
            parent_dict = depth_map.get(parent_depth, root_tree)
            
            if is_folder:
                parent_dict[name] = {}
                depth_map[depth] = parent_dict[name]
            else:
                parent_dict[name] = None
                
        return root_tree

if __name__ == "__main__":
    parser = TreeParserModel()
    sample_tree = """
project/
├── client/
│   ├── src/
│   │   └── App.jsx
└── server/
    └── app.py
"""
    parsed = parser.build_tree(sample_tree)
    print(json.dumps(parsed, indent=2))
