import os
import subprocess
from .utils import get_comfyui_basepath
import torch, torchvision
import time

ENGINE_DIR = os.path.join(get_comfyui_basepath(),"models/depth_trt_engines")

class DepthAnythingTrtNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": { 
                "images": ("IMAGE",),
                "engine": (os.listdir(ENGINE_DIR),)
            }
        }

    RETURN_NAMES = ("images",)
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "main"
    CATEGORY = "Vsgan"
    OUTPUT_NODE=True

    def main(self, images, engine):

        subfolder = "depthmap"
        output_dir = f"output/{subfolder}"
        os.makedirs(output_dir,exist_ok=True)

        # convert images to video for processing
        temp_video_path = os.path.join(get_comfyui_basepath(),f"output/{subfolder}/temp_depth.mp4")
        images = torch.clamp(images *  255,  0,  255).byte() 
        torchvision.io.write_video(temp_video_path, images, 24)

        output_video_name = f"depth_{int(round(time.time()))}.mp4"
        depthmap_video_path = os.path.join(get_comfyui_basepath(),os.path.join(output_dir,output_video_name))

        cmd = f"depth-anything-tensorrt \"{os.path.join(ENGINE_DIR,engine)}\" \"{os.path.join(get_comfyui_basepath(),temp_video_path)}\" \"{depthmap_video_path}\""
        subprocess.run(cmd,shell=True)
                    
        previews = [
            {
                "filename":output_video_name,
                "subfolder":subfolder,
            }
        ]

        # convert video_frames as tensor
        video_frames, _, _ =  torchvision.io.read_video(depthmap_video_path,pts_unit="sec")
        video_frames = video_frames.float() /  255.0

        return {"ui": {"previews": previews},"result": (video_frames,)}

