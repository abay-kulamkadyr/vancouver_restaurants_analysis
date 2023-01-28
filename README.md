## Computational Data Science Project
by Abay Kulamkadyr, Aditya Kulkarni, and Kenneth So 

### **Please read this before viewing any code!**

## What's in this repository?
This repository does not follow a conventional git branch workflow.

## How to run the code
To run our notebooks, the modules `seaborn`, `plotly`, and `GeoPandas` must be installed. GeoPandas is best installed in a new virtual environment, and a quick guide is available below. Once the `GeoPandas` is installed, the first two modules should also be installed in that same environment. 

The main notebooks (`crime-vancouver.ipynb`, `geopandas_cuisine.ipynb`, `plot-amenities.ipynb`, and `yelpdata_analysis.ipynb`) simply display their resulting graphs, plots, and maps within the notebook after running all cells. 

The notebooks/code for processing the data (`clean-amenities.ipynb`, `yelp_cleaningDataScript.py`) will output an updated file. The `clean-amenities.ipynb` file will accept the provided `amenities-vancouver.json` and create `cleaned-amenities-vancouver.json`. The `yelp_cleaningDataScript.py` takes this [raw Kaggle data](https://www.kaggle.com/datasets/yelp-dataset/yelp-dataset) and outputs much smaller JSONs.

Note: our individual branches (`abay`, `adi`, `ken`) contain additional raw notebooks for scratch work that may not run as intended. 

## How to view the Folium maps
To generate some of the maps that represent our results and findings, we used Geopandas and Folium to do so. Unfortunately, these maps do not natively render in Github / Gitlab. As a workaround, we use https://nbviewer.org/ to view our notebooks. Another issue arises however: nbviewer only works on public repositories, and SFU Gitlab is not available to viewing without credentials. Our workaround is to cut our rendered maps to an empty notebook (and only the maps, no code!), push that notebook to a public Gitlab repository, and link it here.

Our maps can be viewed without running any code here:

[All Amenities Map](https://nbviewer.org/github/k-a-so/folium-map/blob/amenities/plot-amenities.ipynb)

[Find Nearest Amenities Map](https://nbviewer.org/github/k-a-so/folium-map/blob/nearest/find-nearest-amenity.ipynb)

[Cuisine Demographics Map](https://nbviewer.org/github/k-a-so/folium-map/blob/main/cuisines-map.ipynb)

[Crime in Vancouver Map](https://nbviewer.org/github/k-a-so/folium-map/blob/crime/crime-vancouver.ipynb)

## Installing Geopandas
If you want to view our maps on your own Jupyter instance, you'll need to install Geopandas and configure a new kernel. Here's a brief guide, based off this [stackoverflow post](https://stackoverflow.com/a/58068850).
1. Start up an instance of the anaconda prompt.
2. Create a new conda environment: `conda create -n geo-env`
3. Activate the new environment: `conda activate geo-env`
4. Install the Python kernel in this environment: `conda install ipykernel`
5. Configure Jupyter with this new kernel: `ipython kernel install --user --name=geo-env-kernel`
6. Run jupyter - the new kernel should be available, and the Geopandas-based notebooks should now be functional.
