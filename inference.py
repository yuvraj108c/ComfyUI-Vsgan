import warnings
warnings.filterwarnings("ignore")
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from inference_config import inference_clip

import json
config = json.load(open(os.path.join(BASE_DIR,"config.json")))

clip = inference_clip(config["video"], config["engine"])
clip.set_output()
