import re
import json
from typing import Optional, Dict, Any

def parse_json(text: str) -> Optional[Dict[str, Any]]:
    """
    Extracts and parses a JSON object from a Markdown code block in a given text.

    Args:
        text (str): The input text containing a JSON code block.

    Returns:
        Optional[Dict[str, Any]]: The parsed JSON data as a dictionary, or None if no valid JSON is found.
    """
    match = re.search(r'```json(.*?)```', text, re.DOTALL)
    if match:
        json_str = match.group(1).strip()
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            return None
    return None

