import os
import json
import requests
import time
from pathlib import Path
from urllib.parse import urlparse
from tqdm import tqdm
# Define paths
IMAGE_DIR = "/home/yoonseok-yang/images"
JSON_PATH = "/home/yoonseok-yang/LLaMA-Factory-vlm/data/processed_training_dataset.json"
NEW_JSON_PATH = "/home/yoonseok-yang/LLaMA-Factory-vlm/data/processed_training_dataset_saved.json"

# Create image directory if it doesn't exist
os.makedirs(IMAGE_DIR, exist_ok=True)

# Load the JSON file
with open(JSON_PATH, 'r') as f:
    data = json.load(f)

# Process each item in the dataset
for i, item in tqdm(enumerate(data)):
    # Get the image URLs from the current item
    image_urls = item.get('images', [])
    saved_images = []
    
    # Download each image
    for j, url in enumerate(image_urls):
        try:
            # Parse the URL to get the filename
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            
            # Create the local path for the image
            local_path = os.path.join(IMAGE_DIR, filename)
            
            # Download the image if it doesn't exist
            if not os.path.exists(local_path):
                # print(f"Downloading image {i+1}/{len(data)}, {j+1}/{len(image_urls)}: {url}")
                response = requests.get(url, stream=True)
                response.raise_for_status()
                
                with open(local_path, 'wb') as img_file:
                    for chunk in response.iter_content(chunk_size=8192):
                        img_file.write(chunk)
                
                # Add a small delay to avoid overwhelming the server
                time.sleep(0.5)
            else:
                print(f"Image {filename} already exists, skipping download")
            
            # Add the local path to the saved images list
            saved_images.append(local_path)
        
        except Exception as e:
            print(f"Error downloading {url}: {e}")
            # Add the original URL if download fails
            saved_images.append(url)
    
    # Update the images field with local paths
    item['images'] = saved_images

# Save the updated JSON file
with open(NEW_JSON_PATH, 'w') as f:
    json.dump(data, f, indent=2)

print(f"Completed! Updated dataset saved to {NEW_JSON_PATH}")
