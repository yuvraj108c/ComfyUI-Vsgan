from .nodes.upscale import UpscaleVideoTrtNode
from .nodes.depth_anything import DepthAnythingTrtNode

NODE_CLASS_MAPPINGS = { 
    "UpscaleVideoTrtNode" : UpscaleVideoTrtNode,
    "DepthAnythingTrtNode" : DepthAnythingTrtNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
     "UpscaleVideoTrtNode" : "Upscale Video Tensorrt", 
     "DepthAnythingTrtNode" : "Depth Anything Tensorrt", 
}

WEB_DIRECTORY = "./web"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS','WEB_DIRECTORY']