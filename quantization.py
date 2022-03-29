import os
from statistics import mode
import torch
from torch import nn
from PIL import Image
from pytorch_nndct.apis import torch_quantizer
from dataset import ImageDataset

from torch.utils.data import DataLoader
import config
from model import ESPCN


from tqdm import tqdm

def load_dataset() -> [DataLoader]:
    quant_datasets = ImageDataset(config.train_image_dir, config.image_size, config.upscale_factor, "train")
    quant_dataloader = DataLoader(quant_datasets,
                                  batch_size=config.batch_size,
                                  shuffle=False,
                                  num_workers=config.num_workers,
                                  pin_memory=False,
                                  persistent_workers=True)

    return quant_dataloader

def define_loss() -> nn.MSELoss:
    criterion = nn.MSELoss().to(config.device)

    return criterion

def evaluate(model, loader, loss_func):
    
    model.eval()
    model = model.to(config.device)
    

if __name__ == "__main__":
    

    print("Load train dataset and valid dataset...")
    quant_dataloader = load_dataset()
    print("Load train dataset and valid dataset successfully.")
    
    # Initialize the super-resolution model
    print("Build SR model...")
    model = ESPCN(config.upscale_factor).to(config.device)
    print("Build SR model successfully.")
    
    print("Define all loss functions...")
    criterion = define_loss()
    print("Define all loss functions successfully.")

    # Load the super-resolution model weights
    print(f"Load SR model weights `{os.path.abspath(config.model_path)}`...")
    state_dict = torch.load(config.model_path, map_location=config.device)
    model.load_state_dict(state_dict)
    print(f"Load SR model weights `{os.path.abspath(config.model_path)}` successfully.")

    input = torch.randn([config.batch_size, 1, 51, 51])
    if config.quant_mode == 'float':
        quant_model = model
    else:
        quantizer = torch_quantizer(
            config.quant_mode, model, (input), device=config.device)

        quant_model = quantizer.quant_model
        
        # quantizer.export_quant_config()
        
        # quantizer.export_xmodel()


    print("Finish!")
