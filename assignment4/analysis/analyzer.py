import polars as pl
import os
from PIL import Image
from tqdm import tqdm

def get_image_info(folder_path):
    
    # Data-storage
    filepaths = []
    widths = []
    heights = []

    for root, dirs, files in os.walk(folder_path):
        # Initializes tqdm progress bar
        pbar = tqdm(files, desc="Processing images")
        # looks through files
        for file_name in pbar:
            # checks for jpg
            if file_name.endswith('.jpg'):
                # Gets image path
                image_path = os.path.join(root, file_name)
                
                # Opens image and get width and height
                try:
                    with Image.open(image_path) as img:
                        width, height = img.size

                        # Appends data
                        filepaths.append(image_path)
                        widths.append(width)
                        heights.append(height)
                except Exception as e: # To handle the images with missing bytes
                    print(f"Error processing {file_name}: {e}")
            # gives the loading bar a tick
            pbar.update(1)

    # Creates polars dataframe
    data = pl.DataFrame({
        "Filepath": filepaths,
        "Width": widths,
        "Height": heights
    })

    return data

def main():
    
    folder_path = os.path.join("../in")

    image_data = get_image_info(folder_path)

    # gets number of occurances of images of same dimensions
    grouped_data = image_data.group_by(["Width", "Height"]).agg(pl.count("*").alias("Count"))

    grouped_data.write_csv("dimensionchart.csv")


if __name__ == "__main__":
    main()