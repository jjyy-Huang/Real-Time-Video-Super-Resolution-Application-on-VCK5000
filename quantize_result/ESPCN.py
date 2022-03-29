# GENETARED BY NNDCT, DO NOT EDIT!

import torch
import pytorch_nndct as py_nndct
class ESPCN(torch.nn.Module):
    def __init__(self):
        super(ESPCN, self).__init__()
        self.module_0 = py_nndct.nn.Input() #ESPCN::input_0
        self.module_1 = py_nndct.nn.Conv2d(in_channels=1, out_channels=64, kernel_size=[5, 5], stride=[1, 1], padding=[2, 2], dilation=[1, 1], groups=1, bias=True) #ESPCN::ESPCN/Sequential[feature_maps]/Conv2d[0]/231
        self.module_2 = py_nndct.nn.Tanh() #ESPCN::ESPCN/Sequential[feature_maps]/Tanh[1]/input.2
        self.module_3 = py_nndct.nn.Conv2d(in_channels=64, out_channels=32, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #ESPCN::ESPCN/Sequential[feature_maps]/Conv2d[2]/251
        self.module_4 = py_nndct.nn.Tanh() #ESPCN::ESPCN/Sequential[feature_maps]/Tanh[3]/input
        self.module_5 = py_nndct.nn.Conv2d(in_channels=32, out_channels=9, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #ESPCN::ESPCN/Sequential[sub_pixel]/Conv2d[0]/271
        self.module_6 = py_nndct.nn.Module('pixel_shuffle',upscale_factor=3) #ESPCN::ESPCN/Sequential[sub_pixel]/PixelShuffle[1]/273

    def forward(self, *args):
        self.output_module_0 = self.module_0(input=args[0])
        self.output_module_1 = self.module_1(self.output_module_0)
        self.output_module_2 = self.module_2(self.output_module_1)
        self.output_module_3 = self.module_3(self.output_module_2)
        self.output_module_4 = self.module_4(self.output_module_3)
        self.output_module_5 = self.module_5(self.output_module_4)
        self.output_module_6 = self.module_6(self.output_module_5)
        return self.output_module_6
