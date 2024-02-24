import os
import subprocess
import json
import torch, torchvision
import time
from .utils import get_comfyui_basepath, get_customnode_basepath, get_config_path, get_video_metadata, get_models_path, get_video_orientation

models_dict = json.load(open(get_models_path()))
models_dict = models_dict["upscaling"]

ENGINE_DIR = os.path.join(get_comfyui_basepath(),"models/upscaler_trt_engines")
ONNX_DIR = os.path.join(get_comfyui_basepath(),"models/onnx")

class UpscaleVideoTrtNode:
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
        subfolder = "upscaled"
        output_dir = f"output/{subfolder}"
        os.makedirs(output_dir,exist_ok=True)

        # convert images to video for processing
        temp_video_path = os.path.join(get_comfyui_basepath(),f"output/{subfolder}/temp_upscaled.mp4")
        images = torch.clamp(images *  255,  0,  255).byte() 
        torchvision.io.write_video(temp_video_path, images, 24)

        output_video_name = f"{engine.replace('.engine','')}_{int(round(time.time()))}.mp4"
        upscaled_video_path = os.path.join(get_comfyui_basepath(),os.path.join(output_dir,output_video_name))

        engine_path = os.path.join(ENGINE_DIR,engine)

        # save config.json
        with open(get_config_path(), 'w') as f:
            json.dump({"video": temp_video_path,"engine":engine_path}, f)

        subprocess.run(f"vspipe -c y4m {os.path.join(get_customnode_basepath(),'inference.py')} - | ffmpeg -i pipe: {upscaled_video_path} -y",shell=True)
        # subprocess.run(f"ffmpeg -f vapoursynth -i {os.path.join(get_customnode_basepath(),'inference.py')} {output_path} -y",shell=True)
                    
        metadata = get_video_metadata(upscaled_video_path)
        frame_rate = int(metadata["fps"])
        width,height = metadata["source_size"]

        # convert video_frames as tensor
        video_frames, _, _ =  torchvision.io.read_video(upscaled_video_path,pts_unit="sec")
        video_frames = video_frames.float() /  255.0

        previews = [
            {
                "filename":output_video_name,
                "subfolder":subfolder
            }
        ]
        data = [
            {
                "frame_rate":frame_rate,
                "resolution":f"{width} x {height}"
            }
        ] 
        return {"ui": {"previews": previews,"data":data},"result": (video_frames,)}