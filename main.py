import argparse
from utils import load_segmentation_model, segment_image, create_3d_shape, visualize_mesh, save_mesh

def main():
    parser = argparse.ArgumentParser(description="Photo/Text to Simple 3D Model Converter")
    parser.add_argument('--mode', type=str, required=True, help="Choose 'photo' or 'text'")
    parser.add_argument('--input', type=str, required=True, help="Path to photo (.jpg/.png) or Text prompt")
    args = parser.parse_args()

    if args.mode == "photo":
        model = load_segmentation_model()
        mask = segment_image(model, args.input)
        mesh = create_3d_shape("cube")
        save_mesh(mesh, "photo_output")
        visualize_mesh(mesh)

    elif args.mode == "text":
        text_prompt = args.input.lower()
        if "car" in text_prompt:
            shape_type = "cube"
        elif "ball" in text_prompt or "sphere" in text_prompt:
            shape_type = "sphere"
        elif "bottle" in text_prompt:
            shape_type = "cylinder"
        else:
            shape_type = "cube"
        mesh = create_3d_shape(shape_type)
        save_mesh(mesh, "text_output")
        visualize_mesh(mesh)

    else:
        print("Invalid mode selected! Use 'photo' or 'text'.")

if __name__ == "__main__":
    main()
