# Copyright 2021 Dakewe Biotech Corporation. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""File description: Realize the verification function after model training."""
import os

import numpy as np
import torch
from PIL import Image
from natsort import natsorted

import config
import imgproc
from model import ESPCN


def main() -> None:
    # Create a folder of super-resolution experiment results
    results_dir = os.path.join("results", "test", config.exp_name)
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    # Initialize the super-resolution model
    print("Build SR model...")
    model = ESPCN(config.upscale_factor).to(config.device)
    print("Build SR model successfully.")

    # Load the super-resolution model weights
    print(f"Load SR model weights `{os.path.abspath(config.model_path)}`...")
    state_dict = torch.load(config.model_path, map_location=config.device)
    model.load_state_dict(state_dict)
    print(f"Load SR model weights `{os.path.abspath(config.model_path)}` successfully.")

    # Start the verification mode of the model.
    model.eval()
    # Turn on half-precision inference.
#    model.half()
    model.float()

    # Initialize the image evaluation index.
    total_psnr = 0.0

    # Get a list of test image file names.
    file_names = natsorted(os.listdir(config.hr_dir))
    # Get the number of test image files.
    total_files = len(file_names)

    for index in range(total_files):
        lr_image_path = os.path.join(config.lr_dir, file_names[index])
        sr_image_path = os.path.join(config.sr_dir, file_names[index])
        hr_image_path = os.path.join(config.hr_dir, file_names[index])

        print(f"Processing `{os.path.abspath(hr_image_path)}`...")
        lr_image = Image.open(lr_image_path).convert("RGB")
        bic_image = lr_image.resize([int(lr_image.width * config.upscale_factor), 
                                     int(lr_image.height * config.upscale_factor)], Image.BICUBIC)
        hr_image = Image.open(hr_image_path).convert("RGB")

        # Extract Y channel lr image data
        lr_image = np.array(lr_image).astype(np.float32)
        lr_ycbcr_image = imgproc.convert_rgb_to_ycbcr(lr_image)
        lr_y_tensor = imgproc.image2tensor(lr_ycbcr_image, range_norm=False, half=False).to(config.device).unsqueeze_(0)

        # Extract Y channel bic image data
        bic_image = np.array(bic_image).astype(np.float32)
        bic_ycbcr_image = imgproc.convert_rgb_to_ycbcr(bic_image)

        # Extract Y channel hr image data.
        hr_image = np.array(hr_image).astype(np.float32)
        hr_ycbcr_image = imgproc.convert_rgb_to_ycbcr(hr_image)
        hr_y_tensor = imgproc.image2tensor(hr_ycbcr_image, range_norm=False, half=False).to(config.device).unsqueeze_(0)

        # Only reconstruct the Y channel image data.
        with torch.no_grad():
            sr_y_tensor = model(lr_y_tensor)

        # Cal PSNR
        total_psnr += 10. * torch.log10(1. / torch.mean((sr_y_tensor - hr_y_tensor) ** 2))

        sr_y_image = imgproc.tensor2image(sr_y_tensor, range_norm=False, half=False)
        sr_image = np.array([sr_y_image, bic_ycbcr_image[..., 1], bic_ycbcr_image[..., 2]]).transpose([1, 2, 0])
        sr_image = np.clip(imgproc.convert_ycbcr_to_rgb(sr_image), 0.0, 255.0).astype(np.uint8)
        sr_image = Image.fromarray(sr_image)
        sr_image.save(sr_image_path)

    print(f"PSNR: {total_psnr / total_files:.2f}.\n")


if __name__ == "__main__":
    main()
