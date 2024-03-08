import os
import imageio
import asyncio
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

# https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite/blob/main/videohelpersuite/utils.py#L156
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

# https://github.com/ceruleandeep/ComfyUI-LLaVA-Captioner/blob/8fcd56888ca9eb13d7dd91ab0e6431ebc2ccfc9c/llava.py#L154
def wait_for_async(async_fn, loop=None):
    res = []

    async def run_async():
        r = await async_fn()
        res.append(r)

    if loop is None:
        try:
            loop = asyncio.get_event_loop()
        except:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

    loop.run_until_complete(run_async())

    return res[0]