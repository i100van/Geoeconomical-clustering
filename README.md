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
