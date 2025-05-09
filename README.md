## Photo & Prompt to 3D Converter README 

### Overview




https://github.com/user-attachments/assets/1b5bcf78-469c-44ab-b290-9112df61fdbe







This tool converts either:  

1. **Photo of an object** → segments the foreground → generates a **gray cube** mesh.  
2. **Free-form text prompt** → uses LLaMA3 to pick **both** a primitive shape (cube, sphere, cylinder) **and** a color (red, green, blue, yellow, white), then builds that colored mesh.

---

### New Customizations in This Version
- **LLaMA3 Integration**  
  - **Before:** text mode simply matched keywords against a static map.  
  - **Now:** we prompt a local `llama3` model (via `ollama run llama3`) to suggest exactly one shape + one color in JSON.  
  - **Fallbacks:** if LLaMA’s output isn’t one of *cube/sphere/cylinder*, we still check `shape_mapping.py`; default is a gray cube.
- **Color Support**  
  - Prompts can specify color (e.g. “make me a yellow box” → yellow cube).  
  - LLaMA picks both shape & color, so users aren’t limited to pre-mapped objects.
- **New Output: `mesh.png`**  
  - Alongside `*.obj` and `*.stl`, the script now snapshots the rendered mesh to `mesh.png` for quick previews.

---

### Output Files

- **Segmented image**:  
  - `segmented.png` — binary mask (object=white, background=black)  
- **3D model files**:  
  - *Photo mode:*  
    - `photo_output.obj`  
    - `photo_output.stl` (binary)  
    - `mesh.png` (snapshot of the cube)  
  - *Text mode:*  
    - `text_output.obj`  
    - `text_output.stl` (binary)  
    - `mesh.png` (snapshot of the colored primitive)  

---

### Installation

```bash
git clone https://github.com/ruhs232/imageto3Dll
cd imageto3Dll
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Ensure you’ve pulled the local llama3 model:
ollama pull llama3
