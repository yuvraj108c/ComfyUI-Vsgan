import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import vapoursynth as vs

core = vs.core
vs_api_below4 = vs.__api_version__.api_major < 4
core = vs.core
core.num_threads = 4  # can influence ram usage
# only needed if you are inside docker
core.std.LoadPlugin(path="/usr/local/lib/libvstrt.so")


def inference_clip(video_path="",engine_path="/root/vsgan/realesr-animevideov3.engine", clip=None):
    # ddfi is passing clip
    if clip is None:
        # bestsource
        clip = core.bs.VideoSource(source=video_path)

    ###############################################
    # COLORSPACE
    ###############################################

    # convert colorspace
    clip = vs.core.resize.Bicubic(clip, format=vs.RGBS, matrix_in_s="709")

    ######
    # UPSCALING WITH TENSORRT
    ######
    # vs-mlrt (you need to create the engine yourself, read the readme)
    clip = core.trt.Model(
        clip,
        engine_path=engine_path,
        # tilesize=[854, 480],
        overlap=[0, 0],
        num_streams=4,
    )

    ###############################################
    # OUTPUT
    ###############################################
    clip = vs.core.resize.Bicubic(clip, format=vs.YUV420P8, matrix_s="709")
    return clip
