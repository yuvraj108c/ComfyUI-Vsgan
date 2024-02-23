import os
import folder_paths
import subprocess
import json
from .utils import get_comfyui_basepath, get_customnode_basepath, get_config_path, get_video_metadata, get_models_path, download_file, get_video_orientation

models_dict = json.load(open(get_models_path()))
models_dict = models_dict["upscaling"]

ENGINE_DIR = os.path.join(get_comfyui_basepath(),"models/upscaler_trt_engines")
ONNX_DIR = os.path.join(get_comfyui_basepath(),"models/onnx")

class UpscaleVideoTrtNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": { 
                "Filenames": ("VHS_FILENAMES",),
                "model": (list(models_dict.keys()),)
            }
        }

    RETURN_NAMES = ("video_path",)
    RETURN_TYPES = ("STRING",)
    FUNCTION = "main"
    CATEGORY = "Vsgan"
    OUTPUT_NODE=True

    def main(self, Filenames, model):
        _, filenames = Filenames
        video_path = filenames[1]

        video_orientation = get_video_orientation(video_path)

        # check if engine exists
        engine_path = os.path.join(ENGINE_DIR,f"{model}_{video_orientation}.engine")
        if not os.path.exists(engine_path):
            
            # Download onnx if not exists
            os.makedirs(ONNX_DIR, exist_ok=True)
            onnx_path = os.path.join(ONNX_DIR,f"{model}.onnx")

            if not os.path.exists(onnx_path):
                download_file(models_dict[model], onnx_path )

            # Create engine from onnx file
            if video_orientation == "landscape":
                cmd = f"trtexec --fp16 --onnx={onnx_path} --minShapes=input:1x3x8x8 --optShapes=input:1x3x720x1280 --maxShapes=input:1x3x720x1280 --saveEngine={engine_path} --tacticSources=+CUDNN,-CUBLAS,-CUBLAS_LT --skipInference --infStreams=4 --builderOptimizationLevel=4"
                subprocess.run(cmd,shell=True)
            elif video_orientation == "portrait":
                cmd = f"trtexec --fp16 --onnx={onnx_path} --minShapes=input:1x3x8x8 --optShapes=input:1x3x1280x720 --maxShapes=input:1x3x1280x720 --saveEngine={engine_path} --tacticSources=+CUDNN,-CUBLAS,-CUBLAS_LT --skipInference --infStreams=4 --builderOptimizationLevel=4"
                subprocess.run(cmd,shell=True)
            else:
                raise Exception("[vsgan] Portrait not supported..")            



        # save config.json
        with open(get_config_path(), 'w') as f:
            json.dump({"video": video_path,"engine":engine_path}, f)

        video_name = f"{model}_{os.path.basename(video_path)}"
        output_path = os.path.join(os.path.join(get_comfyui_basepath(),"output"),video_name)
        subprocess.run(f"vspipe -c y4m {os.path.join(get_customnode_basepath(),'inference.py')} - | ffmpeg -i pipe: {output_path} -y",shell=True)
        # subprocess.run(f"ffmpeg -f vapoursynth -i {os.path.join(get_customnode_basepath(),'inference.py')} {output_path} -y",shell=True)
                    
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
        return {"ui": {"previews": previews,"data":data},"result": (output_path,)}

