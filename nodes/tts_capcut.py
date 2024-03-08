import os
import folder_paths
import asyncio
import websockets
import json
from .utils import get_audio

async def convert_tts(text, speaker):
    async with websockets.connect("wss://sami-maliva.byteintlapi.com/internal/api/v1/ws") as ws:
        # Sending the initial message
        data = {
            "appkey": "ddjeqjLGMn",
            "event": "StartTask",
            "namespace": "TTS",
            "payload": json.dumps({
                "audio_config": {
                    "bit_rate": 64000,
                    "enable_timestamp": True,
                    "format": "ogg_opus",
                    "pitch_rate": 0,
                    "sample_rate": 24000
                },
                "speaker": speaker,
                "texts": [text]
            }),
            "token": "WEtPclZJR0V6SHVUZXAyT09yhoz2s7BkBQVoosFp/Y7M7kD2WGxHTWPNx2VyD3XykHyBAEsefstrFWiyqz8XCZI4Jdj3d3zF64VVl5hoHB/b21vBPVB1sHOEEJ030SOit5EZQc5+nCrWlz6oW1JCEjyItAzuWC3Jj6pvSSEuJtUHbQjHaAJYUTq3fWg93bkj4R9TVyR8FextiJsx5Iv9VmK3eGFyvlMdyUiULKCfJV7k6lm2oX+mGld90xSUHLEhjeMmTbqnCLFSRkP2taVacMCvQ29GM1BqaY2h3hIVyNaOWWG1oZbBYmqTLCFKIgLKlAf3yr7IXalg+J7scCrbaJVVTY0GrgrBhWEnUDz+A5GtBTz2BvTi4JAfe7ZUryf+rhTI6OAVPuu0ge0imweVUPp4FOze291IqdRIVnDVsgKMtmqVT4UraLwgQlvooiO7wKvzYhcWdkfolpCwjDvqCEocy5UYtxFuvfdf7iACigeozAJoerCtsY6z677EvYPF/v6rhvRB5sEOvMv+dBcrD+Q+1m8DBcVx+bmzAWt/BHMovFoQuLx1EPbuOmg2Q2tzU58Y160etJqnUMgWM7QhcI4Q1rf9CFGPundxxWKdIJDpIS09cTiOQRpuZO68T0aUWjv41KpXvbFFc2uNkp7Xm0azAW9Dv/YPQTn4Gk9Yi8ZMVvBUzMsvX+6Jwm6q2QAwMNxbbER4LPwJ2MMm2ByKzw==",
            "version": "sdk_v1",
        }
        await ws.send(json.dumps(data))

        data = {}

        # 2nd response contains json payload
        response = await ws.recv()
        response = await ws.recv()
        response_data = json.loads(response)
        data['payload'] = json.loads(response_data['payload'])
        data['message_id'] = response_data['message_id']

        # 3rd payload contains audio
        response = await ws.recv()
        data['audio'] = response
        return data

class TTSCapcutNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": { 
                "text": ("STRING", {"default": "", "multiline": True}),
                "speaker": (["en_us_006","en_female_jennifer_clone2"],),
            }
        }

    RETURN_NAMES = ("audio","audio_path",)
    RETURN_TYPES = ("VHS_AUDIO","STRING",)
    FUNCTION = "main"
    CATEGORY = "Vsgan"

    def main(self, text, speaker):

        subfolder = "tts"
        output_dir = os.path.join(folder_paths.get_output_directory(), subfolder)
        os.makedirs(output_dir,exist_ok=True)

        result = await convert_tts(text, speaker)
        audio_save_path = os.path.join(output_dir,f"{result["message_id"]}.wav")
        with open(audio_save_path, 'wb') as file:
            file.write(result['audio'])

        vhs_audio = lambda : get_audio(audio_save_path)
        return (vhs_audio, audio_save_path,)

