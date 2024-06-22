import os
import shutil
import requests

# function to search the internet for 5 images and download them to a folder
def get_images(search_term, image_folder):
    # create the image folder if it doesn't exist
    if not os.path.exists(image_folder):
        print("Creating image folder: " + image_folder)
        os.makedirs(image_folder)
    # search the internet for images
    url = "https://www.google.com/search?q=" + search_term + "&tbm=isch"
    print("Searching for images: " + url)
    response = requests.get(url)
    # print(response.text)
    # parse the response
    image_urls = []
    for line in response.text.splitlines():
        if "data-src=" in line:
            image_urls.append(line.split("data-src=")[1].split(" ")[0].replace('"', ''))
    # print(image_urls)
    # download the images
    for i, image_url in enumerate(image_urls):
        print("Downloading image " + str(i + 1) + " of " + str(len(image_urls)) + ": " + image_url)
        response = requests.get(image_url, stream=True)
        with open(os.path.join(image_folder, search_term + "_" + str(i + 1) + ".jpg"), 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
    return image_urls