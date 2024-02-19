import os
import folder_paths
import subprocess
import json
from .utils import get_comfyui_basepath, get_customnode_basepath, get_config_path, get_video_metadata

ENGINE_DIR = os.path.join(get_comfyui_basepath(),"models/upscaler_trt_engines")

class UpscaleVideoTrtNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": { 
                "Filenames": ("VHS_FILENAMES",),
                "engine": (os.listdir(ENGINE_DIR),),
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "main"
    CATEGORY = "Vsgan"
    OUTPUT_NODE=True

    def main(self,Filenames,engine):
        _, filenames = Filenames
        video_path = filenames[1]
        engine_path = os.path.join(ENGINE_DIR,engine)

        # save config.json
        with open(get_config_path(), 'w') as f:
            json.dump({"video": video_path,"engine":engine_path}, f)

        video_name = f"{engine.replace('.engine','')}_{os.path.basename(video_path)}"
        output_path = os.path.join(os.path.join(get_comfyui_basepath(),"output"),video_name)
        subprocess.run(f"ffmpeg -f vapoursynth -i {os.path.join(get_customnode_basepath(),'inference.py')} {output_path} -y",shell=True)
                    
        metadata = get_video_metadata(output_path)
        frame_rate = int(metadata["fps"])
        width,height = metadata["source_size"]

        previews = [
            {
                "filename":video_name,
                "subfolder":"",
                "format":"video/h264-mp4",
                "type":"output",
            }
        ]
        data = [
            {
                "frame_rate":frame_rate,
                "resolution":f"{width} x {height}"
            }
        ] 
        return {"ui": {"previews":previews,"data":data},}

