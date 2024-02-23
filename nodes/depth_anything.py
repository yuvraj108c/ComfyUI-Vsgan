import os
import subprocess
from .utils import get_comfyui_basepath

ENGINE_DIR = os.path.join(get_comfyui_basepath(),"models/depth_trt_engines")

class DepthAnythingTrtNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": { 
                "video_path": ("STRING",{"default":""}),
                "engine": (os.listdir(ENGINE_DIR),)
            }
        }

    RETURN_NAMES = ("video_path",)
    RETURN_TYPES = ("STRING",)
    FUNCTION = "main"
    CATEGORY = "Vsgan"
    OUTPUT_NODE=True

    def main(self, video_path, engine):

        subfolder = "depthmap"
        output_dir = f"output/{subfolder}"
        os.makedirs(output_dir,exist_ok=True)
        
        output_video_name = f"depth_{os.path.basename(video_path)}"
        video_save_path = os.path.join(get_comfyui_basepath(),os.path.join(output_dir,output_video_name))

        if not os.path.exists(video_save_path):
            cmd = f"depth-anything-tensorrt \"{os.path.join(ENGINE_DIR,engine)}\" \"{os.path.join(get_comfyui_basepath(),video_path)}\" \"{video_save_path}\""
            subprocess.run(cmd,shell=True)
                    
        previews = [
            {
                "filename":output_video_name,
                "subfolder":subfolder,
            }
        ]

        return {"ui": {"previews": previews},"result": (video_save_path,)}

