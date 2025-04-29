import numpy as np
if not hasattr(np, "infty"):
    np.infty = np.inf

import torch
import torchvision.transforms as T
from torchvision.models.segmentation import deeplabv3_resnet50
import cv2
import trimesh
import pyrender

def load_segmentation_model():
    model = deeplabv3_resnet50(pretrained=True)
    model.eval()
    return model

def segment_image(model, img_path):
    img = cv2.imread(img_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    transform = T.Compose([
        T.ToPILImage(),
        T.Resize(520),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225]),
    ])
    input_tensor = transform(img_rgb).unsqueeze(0)
    with torch.no_grad():
        output = model(input_tensor)['out'][0]
    output_predictions = output.argmax(0).byte().cpu().numpy()
    mask = (output_predictions > 0).astype(np.uint8) * 255
    cv2.imwrite("segmented.png", mask)
    return mask

def create_3d_shape(shape_type="cube"):
    if shape_type == "cube":
        mesh = trimesh.creation.box(extents=(1, 1, 1))
    elif shape_type == "sphere":
        mesh = trimesh.creation.icosphere(subdivisions=2, radius=0.5)
    elif shape_type == "cylinder":
        mesh = trimesh.creation.cylinder(radius=0.3, height=1.0)
    else:
        mesh = trimesh.creation.box(extents=(1, 1, 1))
    return mesh

def visualize_mesh(mesh):
    scene = pyrender.Scene()
    mesh_node = pyrender.Mesh.from_trimesh(mesh)
    scene.add(mesh_node)
    pyrender.Viewer(scene, use_raymond_lighting=True)

def save_mesh(mesh, base_name="output"):
    mesh.export(f"{base_name}.obj")
    mesh.export(f"{base_name}.stl")
    print(f"[INFO] Saved {base_name}.obj and {base_name}.stl")
