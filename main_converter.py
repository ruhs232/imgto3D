
import argparse
import trimesh
import pyrender

from segmenter import load_segmentation_model, create_foreground_mask

from llama_extractor import get_shape_and_color_from_text

COLOR_TABLE = {
    "red":    [255,   0,   0, 255],
    "green":  [  0, 255,   0, 255],
    "blue":   [  0,   0, 255, 255],
    "yellow": [255, 255,   0, 255],
    "white":  [255, 255, 255, 255],
    "gray":   [150, 150, 150, 255],
}

def create_colored_mesh(shape, color_name):

    if shape == "cube":
        mesh = trimesh.creation.box(extents=(1, 1, 1))
    elif shape == "sphere":
        mesh = trimesh.creation.icosphere(subdivisions=2, radius=0.5)
    elif shape == "cylinder":
        mesh = trimesh.creation.cylinder(radius=0.3, height=1.0)
    else:
        mesh = trimesh.creation.box(extents=(1, 1, 1))

    rgba = COLOR_TABLE.get(color_name.lower(), COLOR_TABLE["gray"])
    mesh.visual.vertex_colors = rgba
    return mesh

def save_and_display(mesh, filename):

    # Export OBJ
    mesh.export(f"{filename}.obj", file_type='obj')
    # Explicitly request binary STL to avoid null-filled files
    mesh.export(f"{filename}.stl", file_type='stl')
    print(f"[✓] Saved {filename}.obj and {filename}.stl (binary)")

    scene = pyrender.Scene()
    scene.add(pyrender.Mesh.from_trimesh(mesh))
    pyrender.Viewer(scene, use_raymond_lighting=True)

def main():
    parser = argparse.ArgumentParser(
        description="Turn a photo or text prompt into a 3D model"
    )
    parser.add_argument("--mode", choices=["photo", "text"], required=True)
    parser.add_argument("--input", required=True)
    args = parser.parse_args()

    if args.mode == "photo":
        model = load_segmentation_model()
        mask = create_foreground_mask(model, args.input)
        mesh = create_colored_mesh("cube", "gray")
        save_and_display(mesh, "photo_output")

    else:
        user_input = args.input
        shape, color = get_shape_and_color_from_text(user_input)
        print(f"[INFO] Extracted → Shape: {shape}, Color: {color}")
        mesh = create_colored_mesh(shape, color)
        save_and_display(mesh, "text_output")

if __name__ == "__main__":
    main()


