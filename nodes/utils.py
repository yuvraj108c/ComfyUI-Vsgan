import os
import imageio
import httpx
from tqdm import tqdm

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


def download_file(url, save_path):
    print(f"downloading {url} ...")
    with httpx.stream("GET", url, follow_redirects=True) as stream:
        total = int(stream.headers["Content-Length"])
        with open(save_path, "wb") as f, tqdm(
            total=total, unit_scale=True, unit_divisor=1024, unit="B"
        ) as progress:
            num_bytes_downloaded = stream.num_bytes_downloaded
            for data in stream.iter_bytes():
                f.write(data)
                progress.update(
                    stream.num_bytes_downloaded - num_bytes_downloaded
                )
                num_bytes_downloaded = stream.num_bytes_downloaded