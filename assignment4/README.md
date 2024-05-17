


### To Batch or not to Batch?

The code is fairly ressource intensive. While the code is written so it doesn't utilize batch processing, as to batch process its required for the images to have the same dimensions. To explore the idea a bit more, there is 4624 images, hence an overlap in image dimensions could be present. I've looked at the images, and organized them by image size (in polars). In the table (GroupedResults.csv), it shows has 354 entries meaning you would have to have 354 different batches. This is without any modification of the images, this might improve performance, given that batch-processing often is faster than individual processing when using models.

I've abandoned the idea, due to the dataset having a picture, with missing bites, an issue Pillow's ```img.verify() ``` can't detect. This would then make a whole batch unprocessable, again leading to loss in efficiency. While other dataset with uniform picture width and heights, might benefit from using batch processing. The code is therefore written to accommodate dataset similar to this.
