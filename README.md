# Map coloring
This project focuses on developing an algorithm for automatic coloring of a map using only a raster image as input. The process involves constructing a country adjacency graph and determining its chromatic number.

**Map Creation**:
1. Encode each country by specifying its neighboring countries
2. Manually embed the generated barcodes onto the corresponding regions of the image

**Image Processing Algorithm**:
1. Detect barcodes on each country from the image
2. Decode the extracted barcodes
3. Assign a color to each country based on the decoded data
4. Apply the coloring to the image

# Project demonstration

**Main page information block**

![](https://github.com/nikorr0/map-coloring/blob/main/screenshots/main-page.png)

**Options**

The user can upload their own map or select from existed examples.

![](https://github.com/nikorr0/map-coloring/blob/main/screenshots/options.png)

**Result**

![](https://github.com/nikorr0/map-coloring/blob/main/screenshots/result.png)

**Cell generation page**

The user can put the dictionary in a text field with countries and their borders and get the generated cells. They can place cells on their map to then color it.

![](https://github.com/nikorr0/map-coloring/blob/main/screenshots/dict-page.png)

**Generated cells**

![](https://github.com/nikorr0/map-coloring/blob/main/screenshots/dict-page-result.png)

# Map coloring step by step

**Graph version**

![](https://github.com/nikorr0/map-coloring/blob/main/screenshots/gifs/europe_map_drawing_graph.gif)

**Filled version**

![](https://github.com/nikorr0/map-coloring/blob/main/screenshots/gifs/europe_map_drawing_filled.gif)
