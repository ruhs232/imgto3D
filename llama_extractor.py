import subprocess
import json

from shape_mapping import OBJECT_TO_PRIMITIVE

def get_shape_and_color_from_text(prompt):

    instruction = f"""
Pick one shape (cube, sphere, cylinder)
and one color (red, green, blue, yellow, white) from the text below.
Respond in JSON like:
  {{ "shape": "...", "color": "..." }}

Text:
{prompt}
"""

    result = subprocess.run(
        ["ollama", "run", "llama3", instruction],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="ignore",
    )

    try:
        raw_output = result.stdout
        json_data = raw_output[raw_output.find("{"):]
        parsed = json.loads(json_data)
        shape = parsed.get("shape")
        color = parsed.get("color", "gray")
    except Exception:
        shape, color = None, "gray"

    valid_shapes = {"cube", "sphere", "cylinder"}

    if shape not in valid_shapes:
        lower_prompt = prompt.lower()
        for word, fallback_shape in OBJECT_TO_PRIMITIVE.items():
            if word in lower_prompt:
                shape = fallback_shape
                break

    if shape not in valid_shapes:
        shape = "cube"

    return shape, color
