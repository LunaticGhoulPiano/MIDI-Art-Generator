import json
import os
import requests
import copy

# read settings
with open("prompts.json", "r", encoding="utf-8") as f:
    all_prompts = json.load(f)

with open("workflow_ComfyUI.json", "r", encoding="utf-8") as f:
    base_workflow = json.load(f)

epochs = ["epoch1", "epoch3", "epoch10", "epoch30", "epoch50"]
base_ckpt_folder = "./models./checkpoints"
save_prefix_template = "{category}_{index}_{epoch}"

# ComfyUI server URL
COMFYUI_API_URL = "http://127.0.0.1:8000/prompt"

# main
for category, prompt_set in all_prompts.items():
    for prompt_index in ["1", "2", "3"]:
        prompts = prompt_set[prompt_index]
        positive = prompts["positive"]
        negative = prompts["negative"]

        for epoch in epochs:
            # copy base workflow
            wf = copy.deepcopy(base_workflow)

            # checkpoint model path
            ckpt_path = f"{epoch}\\{epoch}.safetensors"
            wf["8"]["inputs"]["ckpt_name"] = ckpt_path

            # get node of pos and neg
            pos_key = wf["4"]["inputs"]["positive"][0]
            neg_key = wf["4"]["inputs"]["negative"][0]

            # set prompt
            wf[pos_key]["inputs"]["text"] = positive
            wf[neg_key]["inputs"]["text"] = negative

            # set file path
            filename_prefix = save_prefix_template.format(category=category, index=prompt_index, epoch=epoch)
            wf["3"]["inputs"]["filename_prefix"] = f"./output./{filename_prefix}"

            # send to ComfyUI
            response = requests.post(COMFYUI_API_URL, json = {"prompt": wf})
            if response.status_code == 200:
                print(f"✅ Generated: {filename_prefix}")
            else:
                print(f"❌ Failed: {filename_prefix} ({response.status_code})")
