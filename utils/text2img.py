import requests

def_text2img={
    "restore_faces": False,
    "face_restorer": "CodeFormer",
    "codeformer_weight": 0.5,
    "sd_model": "Anylora.safetensor",
    "prompt": "masterpiece, high quality, SNAKE, galverse, ayaka_gal_style<lora:ayaka_gal_style_V4.2_ft-000011:0.8>",
    "negative_prompt": "NSFW",
    "seed": "-1",
    "seed_enable_extras": False,
    "subseed": -1,
    "subseed_strength": 0,
    "seed_resize_from_h": 0,
    "seed_resize_from_w": 0,
    "sampler_name": "Euler a",
    "steps": "15",
    "cfg_scale": "5",
      "denoising_strength": 0,
    "batch_count": 1,
    "batch_size": 1,
    "base_size": 512,
    "max_size": 768,
    "tiling": False,
    "highres_fix": False,
    "firstphase_height": 512,
    "firstphase_width": 512,
    "upscaler_name": "None",
    "filter_nsfw": False,
    "include_grid": False,
    "sample_path": "outputs/krita-out",
    "orig_width": 512,
    "orig_height": 512
    }


def SD_APICALL(payload:dict,url:str):

    #print("API Call")
    #print(url)
    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
    r = response.json()
    #print(r)
    return r