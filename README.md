## Output

- **Segmented image**: `segmented.png` (your object mask)
- **3D model files**:  
  - `photo_output.obj` & `photo_output.stl` (for photo mode)  
  - `text_output.obj` & `text_output.stl` (for text mode)

## How to Run

1. **Photo mode** (with your downloaded test image, e.g. `test_images/toy_car.jpg`):
   ```bash
   python main.py --mode photo --input test_images/toy_car.jpg

