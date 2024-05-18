# Assignment 4

#### Victor Rasmussen
##### Aarhus University, Language Analytics

<br>
It will prompt you to check

> ![](image.png?raw=true)


### Results

![Description](out/LineChart1.png?raw=true)

![Description](out/LineChart.png?raw=true)

### To Batch or not to Batch?

The code is fairly ressource intensive. While the code is written so it doesn't utilize batch processing, as to batch process its required for the images to have the same dimensions(if you try it will tell you so in the console). To explore the idea a bit more, there is 4624 images, hence an overlap in image dimensions could be present. I've looked at the images, and organized them by image size (in polars). In the table (GroupedResults.csv), it shows has 354 entries meaning you would have to have 354 different batches. This is without any modification of the images, this might improve performance, given that batch-processing often is faster than individual processing when using models.

I've abandoned the idea, due to the dataset having a picture, with missing bites, an issue Pillow's ```img.verify() ``` can't detect. This would then make a whole batch unprocessable, and will first tell you when it gives an error, again leading to loss in efficiency, because the code needs to be rerun. While other dataset with uniform picture width and heights, might benefit from using batch processing, defect images cause it trouble. The code is therefore written to accommodate damaged files, and different image sizes.






Python 3.12.3