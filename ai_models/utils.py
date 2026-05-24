import json
import re
from typing import Dict, Any

def clean_text(text: str) -> str:
    """Clean and normalize input text."""
    if not text:
        return ""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def save_json(data: Dict[str, Any], filepath: str) -> None:
    """Save a dictionary to a JSON file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def load_json(filepath: str) -> Dict[str, Any]:
    """Load a dictionary from a JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def is_valid_json(json_string: str) -> bool:
    """Check if a given string is valid JSON."""
    try:
        json.loads(json_string)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    print(f"Cleaned text: '{clean_text('  This   is  a test  ')}'")
