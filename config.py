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
"""Realize the parameter configuration function of dataset, model, training and verification code."""
import torch
from torch.backends import cudnn as cudnn

# ==============================================================================
# General configuration
# ==============================================================================
torch.manual_seed(0)
#device = torch.device("cuda", 0)
device = torch.device("cpu")
cudnn.benchmark = True
upscale_factor = 3
# mode = "train"
# mode = "valid"
mode = "quantize"
exp_name = "baseline"

# ==============================================================================
# Training configuration
# ==============================================================================
if mode == "train":
    # Dataset
    # Image format
    train_image_dir = f"data/T91/ESPCN/train"
    valid_image_dir = f"data/T91/ESPCN/valid"
    # LMDB format
    train_lr_lmdb_path = f"data/train_lmdb/ESPCN/T91_LRbicx3_lmdb"
    train_hr_lmdb_path = f"data/train_lmdb/ESPCN/T91_HR_lmdb"
    valid_lr_lmdb_path = f"data/valid_lmdb/ESPCN/T91_LRbicx3_lmdb"
    valid_hr_lmdb_path = f"data/valid_lmdb/ESPCN/T91_HR_lmdb"

    image_size = 51
    batch_size = 4
    num_workers = 4

    # Incremental training and migration training
    resume = False
    strict = True
    start_epoch = 0
    resume_weight = ""

    # Total num epochs
    epochs = 2000

    # Adam optimizer parameter
    model_optimizer_name = "adam"
    model_lr = 1e-2
    model_betas = (0.9, 0.999)

    # Optimizer scheduler parameter
    lr_scheduler_name = "multiStepLR"
    lr_scheduler_milestones = [1600, 1800]
    lr_scheduler_gamma = 0.1

    print_frequency = 100

# ==============================================================================
# Verify configuration
# ==============================================================================
if mode == "valid":
    # Test data address
    lr_dir = f"data/Set5/LRbicx{upscale_factor}"
    sr_dir = f"results/test/{exp_name}"
    hr_dir = f"data/Set5/GTmod12"

    model_path = f"results/{exp_name}/best.pth"
    
# ==============================================================================
# Quantize configuration
# ==============================================================================
if mode == "quantize":
    train_image_dir = f"data/T91/ESPCN/train"
    
    lr_dir = f"data/Set5/LRbicx{upscale_factor}"
    sr_dir = f"results/test/{exp_name}"
    hr_dir = f"data/Set5/GTmod12"
    
    image_size = 51 
    batch_size = 1
    num_workers = 4
    
    quant_mode = "calib"
    
    model_path = f"results/{exp_name}/best.pth"
