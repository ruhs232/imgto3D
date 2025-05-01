

import numpy as np
import cv2
import torch
import torchvision.transforms as T

from torchvision.models.segmentation import deeplabv3_resnet50

if not hasattr(np, "infty"):
    np.infty = np.inf

def load_segmentation_model():

    model = deeplabv3_resnet50(pretrained=True)
    model.eval()
    return model

def create_foreground_mask(model, image_path):

    image_bgr = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

    preprocess = T.Compose([
        T.ToPILImage(),
        T.Resize(520),
        T.ToTensor(),
        T.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        ),
    ])
    input_tensor = preprocess(image_rgb).unsqueeze(0)

    with torch.no_grad():
        output = model(input_tensor)["out"][0]
    labels = output.argmax(0).byte().cpu().numpy()

    mask = (labels > 0).astype(np.uint8) * 255
    cv2.imwrite("segmented.png", mask)
    return mask
