import torch
from torchvision.models import resnet50
import torchvision.transforms as transforms
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image
import cv2

# Step 1: Load the pretrained model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = resnet50(pretrained=True).to(device)
model.eval()

# Step 2: Specify the target layer for Grad-CAM
target_layers = [model.layer4[-1]]


def image_grad_cam(image_path):
    rgb_img = cv2.imread(image_path, 1)  # Read as BGR
    rgb_img = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2RGB)  # Convert to RGB
    rgb_img = cv2.resize(rgb_img, (224, 224))  # Resize to model input size
    rgb_img_normalized = rgb_img / 255.0  # Normalize to [0, 1]

    transform = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )
    # Convert image to float32 explicitly
    input_tensor = (
        transform(rgb_img_normalized).unsqueeze(0).to(torch.float32).to(device)
    )

    with GradCAM(model=model, target_layers=target_layers) as cam:
        grayscale_cam = cam(input_tensor=input_tensor)
        grayscale_cam = grayscale_cam[0, :]  # Get the CAM for the first image

        # Visualize the CAM on the original image
        visualization = show_cam_on_image(
            rgb_img_normalized, grayscale_cam, use_rgb=True
        )

    return visualization
