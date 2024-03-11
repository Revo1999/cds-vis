# Assignment 1 
###### Victor Rasmussen, Visual Analytics, Aarhus University
-----

This project include a assignment1.py files that go through txt and extracts: relative frequency of nouns, verbs, adjective, and adverbs per 10,000 words, aswell as total number of unique PER, LOC, ORGS per text, using spaCy.

More information and download link for data (Beware of terms of usage!): [click here](https://ota.bodleian.ox.ac.uk/repository/xmlui/handle/20.500.12024/2457)

## Project Structure

```
.
└── Assignment1/
    ├── data/
    │   ├── image_0001.jpg
    │   └── image_0002.jpg
    ├── out/
    │   └── table.csv
    ├── src/
    │   └── assignemnt1.py
    ├── readme.md
    ├── requirements.txt
    └── setup.sh
```

## Dependencies

```
opencv (cv2)
numpy
tqdm
pandas
```

 ### ```bash start.sh``` will download dependencies

<br>
<br>

## Usage
Insert data from USEcorpus to match what is shown i project structure or change the value of ```directory``` (shown below) if you follow forementioned structure also "cd" into the "Assignment 1"-folder **to avoid path problems.**


1. run ```bash start.sh``` in console and accept
2. run ```python src\assignment1.py```

<br>
<br>

### These settings can be changed in  when runned:


Change the input path: 


Change the output path:

