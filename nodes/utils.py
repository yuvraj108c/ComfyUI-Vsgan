import os
import imageio
from imageio_ffmpeg import get_ffmpeg_exe

def get_video_metadata(video_path):
    reader = imageio.get_reader(video_path)
    return reader.get_meta_data()

def get_video_orientation(video_path):
    metadata = get_video_metadata(video_path)
    width,height = metadata["source_size"]
    if width == height:
        return "square"
    elif width < height:
        return "portrait"
    else:
        return "landscape"

def get_comfyui_basepath():
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(os.path.dirname(os.path.dirname(current_script_dir)))

def get_customnode_basepath():
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(current_script_dir)

def get_config_path():
    return os.path.join(get_customnode_basepath(),"config.json")

def get_models_path():
    return os.path.join(get_customnode_basepath(),"models.json")

from imageio_ffmpeg import get_ffmpeg_exe

def lazy_eval(func):
    class Cache:
        def __init__(self, func):
            self.res = None
            self.func = func
        def get(self):
            if self.res is None:
                self.res = self.func()
            return self.res
    cache = Cache(func)
    return lambda : cache.get()

def get_audio(file):
    imageio_ffmpeg_path = get_ffmpeg_exe()
    args = [imageio_ffmpeg_path, "-v", "error", "-i", file]
    try:
        res =  subprocess.run(args + ["-f", "wav", "-"],
                              stdout=subprocess.PIPE, check=True).stdout
    except subprocess.CalledProcessError as e:
        logger.warning(f"Failed to extract audio from: {file}")
        return False
    return res