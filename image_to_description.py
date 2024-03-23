import os
import json
from PIL import Image
from clip_interrogator import Config, Interrogator

# Configuration
caption_model_name = 'blip-large'
clip_model_name = 'ViT-L-14/openai'
prompt_mode = 'best'
source_path = "D:/Projects/image_to_text/Download_images/Images"  # Path to the folder containing images
output_folder_path = "D:/Projects/image_to_text/Output_description"


# Initialize Interrogator with configuration
config = Config()
config.clip_model_name = clip_model_name
config.caption_model_name = caption_model_name
ci = Interrogator(config)

def image_to_prompt(image_path, mode):
    image = Image.open(image_path).convert('RGB')
    ci.config.chunk_size = 2048 if ci.config.clip_model_name == "ViT-L-14/openai" else 1024
    ci.config.flavor_intermediate_count = 2048 if ci.config.clip_model_name == "ViT-L-14/openai" else 1024
    image = image.convert('RGB')
    if mode == 'best':
        return ci.interrogate(image)
    elif mode == 'classic':
        return ci.interrogate_classic(image)
    elif mode == 'fast':
        return ci.interrogate_fast(image)
    elif mode == 'negative':
        return ci.interrogate_negative(image)


processed_image_file_name = os.listdir(output_folder_path)
processed_image_id = [x.split('.')[0] for x in processed_image_file_name]
processed_image_id = set(processed_image_id)

count = 0

for filename in os.listdir(source_path)[::-1]:
    count+=1
    print(count, filename)
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
        image_id = filename.split('.')[0]
        if image_id not in processed_image_id:
            image_path = os.path.join(source_path, filename)
            try:
                prompt = image_to_prompt(image_path, prompt_mode)
                
                # Read the existing content from the source txt file
                with open(os.path.join(source_path, f'{image_id}.txt'), 'r') as file:
                    info = json.load(file)

                # Update the content with the generated prompt
                info['prompt'] = prompt

                # Write the updated content to a new txt file in the output folder
                with open(os.path.join(output_folder_path, f'{image_id}.txt'), 'w') as file:
                    json.dump(info, file)

            except Exception as e:
                print(f"Error processing {filename}: {e}")




