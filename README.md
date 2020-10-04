# Geoeconomical-clustering
Data Science proyect for classify all countries in the world in 10 different groups according to the distance between them and their GDP (Gross Domestic Product) per capita.

## Obtaining the data
First, a search was made for the data sources to be used for the analysis. Two sources were selected:
1. Firstly, the economic data provided by the World Bank at [World Bank](https://data.worldbank.org) was obtained.
2. To obtain the geolocation data of the countries, the following source has been used [Geolocations](https://gist.github.com/tadast/8827699) , which places the locations of the countries in the averages of latitude and longitude that they occupy. This measure helps us to centralize the position of the countries, since using the capitals can greatly displace the assumed position of the country, as can be the case of Argentina, whose capital is located at the top of the country.

## Data cleaning and processing
After obtaining the data, we proceed to visualize it, in search of possible anomalous or missing values. To do this we use the report provided by the Pandas library.

Null values are observed, which are eliminated by the consideration of the enunciation, but in an environment of greater exigency as far as the results, we would look for a treatment adapted for these values (For example, to look for other sources that could complement these data to us). In addition, since we obtained more values than necessary from the World Bank, they are no longer considered.

Finally, we unified the data in a single Dataframe to perform the necessary clustering processes.
You can view the report of the final data used for analysis in the following file:

## Clustering process
Two clustering processes are carried out:
1. Firstly, the DBSCAN clustering algorithm is considered, which allows the use of multiple metrics. In this case, since the data we use are of longitude/latitude, we will use Harvesine's metric which is the angular distance between two points on the surface of a sphere. The first distance of each point is assumed to be the latitude, the second is the longitude, given in radians. Where the following clustering is obtained.
![GeoCluster](https://github.com/i100van/Geoeconomical-clustering/blob/main/geocluster.JPG)

2. Secondly, we carry out the K-means method to obtain the ten clusters by using the economic measures and the cluster indicator of the previous step. In this way, we obtain groupings of nearby countries and similar economic conditions.
![Geoeconomical cluster](https://github.com/i100van/Geoeconomical-clustering/blob/main/geoeconomical.JPG)

In this way we achieve the requested country labeling

## Preparation of the output
To finish, we will make the calculations on the requested dataframe, and we will make the requested ordering, checking the output variables in the same way as in the beginning, using the pandas report. 
