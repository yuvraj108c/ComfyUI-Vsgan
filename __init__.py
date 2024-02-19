from .nodes.upscale import UpscaleVideoTrtNode

NODE_CLASS_MAPPINGS = { 
    "UpscaleVideoTrtNode" : UpscaleVideoTrtNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
     "UpscaleVideoTrtNode" : "Upscale Video Tensorrt", 
}

WEB_DIRECTORY = "./web"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS','WEB_DIRECTORY']