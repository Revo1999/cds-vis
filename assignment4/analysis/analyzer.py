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
        # Initialize tqdm progress bar
        pbar = tqdm(files, desc="Processing images", unit="image")
        # looks through files
        for file_name in pbar:
            # check for jpg
            if file_name.endswith('.jpg'):
                # Get image path
                image_path = os.path.join(root, file_name)
                
                # Opens image and get width and height
                try:
                    with Image.open(image_path) as img:
                        width, height = img.size

                        # Appends data
                        filepaths.append(image_path)
                        widths.append(width)
                        heights.append(height)
                except Exception as e:
                    print(f"Error processing {file_name}: {e}")
            # give the loading bar a tick
            pbar.update(1)

    # Creates polars dataframe
    df = pl.DataFrame({
        "Filepath": filepaths,
        "Width": widths,
        "Height": heights
    })

    return df

def main():
    # Path to the in
    folder_path = os.path.join("../in")

    image_df = get_image_info(folder_path)

    # gets number of occurances of images of same dimensions
    grouped_df = image_df.group_by(["Width", "Height"]).agg(pl.count("*").alias("Count"))

    grouped_df.write_csv("dimensionchart.csv")


if __name__ == "__main__":
    main()