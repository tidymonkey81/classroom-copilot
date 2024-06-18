from openai import OpenAI
import os
import requests
import shutil

# Example usage
# generate_image_from_prompt("A futuristic cityscape", "path/to/directory", "futuristic_cityscape")
def generate_image_from_prompt(prompt, output_path, file_name, n=1, size="1792x1024", quality="standard"):
    """
    Generates an image from a prompt using OpenAI's DALL-E 3 model and saves it to the specified path.
    """
    client = OpenAI()

    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1792x1024",
            quality=quality,
            n=n,
        )

        if response.data:
            images = []
            for i, item in enumerate(response.data):
                image_url = item.url
                image_full_path = f"{output_path}/{file_name}_{i}" if n > 1 else f"{output_path}/{file_name}"
                # if the path doesn't exist, create it
                directory = os.path.dirname(image_full_path)
                if not os.path.exists(directory):
                    os.makedirs(directory)
                # Download the image
                r = requests.get(image_url, stream=True)
                if r.status_code == 200:
                    with open(image_full_path, 'wb') as f:
                        r.raw.decode_content = True
                        shutil.copyfileobj(r.raw, f)
                    images.append(image_full_path)
                    print(f"Image saved to {image_full_path}")
                else:
                    print(f'Image {i} couldn\'t be retrieved')
            return images
        else:
            print("No images were generated.")
    except Exception as e:
        print(f"An error occurred: {e}")
