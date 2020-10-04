import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas_profiling import ProfileReport
from sklearn.cluster import KMeans, DBSCAN

# https://data.worldbank.org/indicator/NY.GDP.MKTP.CD?end=2019&start=2019
data_PIB_Total = pd.read_csv('data/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_Total.csv', sep=',')
# https://data.worldbank.org/indicator/NY.GDP.PCAP.PP.CD
data_PIB_percapita = pd.read_csv('data/API_NY.GDP.PCAP.PP.CD_DS2_en_csv_v2_1345144.csv', sep=',')
# https://gist.github.com/tadast/8827699
data_city = pd.read_csv('data/countries_codes_and_coordinates.csv', sep=',')

# Clean unnused data
data_PIB_Total = data_PIB_Total.drop(
    ['Country Name', 'Unnamed: 64', 'Indicator Name', 'Indicator Code', '1960', '1961', '1962', '1963', '1964', '1965',
     '1966', '1967', '1968', '1969', '1970', '1971', '1972', '1973', '1974', '1975', '1976', '1977', '1978', '1979',
     '1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989', '1990', '1991', '1992', '1993',
     '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007',
     '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018'], axis=1)
data_PIB_clean = data_PIB_percapita.drop(
    ['Unnamed: 64', 'Indicator Name', 'Indicator Code', '1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967',
     '1968', '1969', '1970', '1971', '1972', '1973', '1974', '1975', '1976', '1977', '1978', '1979', '1980', '1981',
     '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995',
     '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009',
     '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018'], axis=1)
data_city_clean = data_city.drop(['Alpha-2 code', 'Numeric code', 'Country'], axis=1)

# Replace missing info with NaN
data_PIB_percapita = data_PIB_clean.fillna(value=0)
data_city = data_city_clean.fillna(method='ffill')
data_PIB_percapita = data_PIB_clean.dropna()

# Join cleaned tables
data_PIB_percapita = data_PIB_percapita.rename(columns={'Country Code': 'Alpha-3 code'})
data_PIB_Total = data_PIB_Total.rename(columns={'Country Code': 'Alpha-3 code', '2019': 'GDP Total'})
data = pd.merge(data_PIB_percapita, data_city, on='Alpha-3 code', how='inner')
data = pd.merge(data, data_PIB_Total, on='Alpha-3 code', how='inner')
data = data.drop_duplicates(['Alpha-3 code'])

# Create a report for visualize the final data
prof = ProfileReport(data)
prof.to_file(output_file='data.html')

# Clustering by closeness DBScan
variable = np.array(data[['Longitude(average)', 'Latitude(average)']])
eps = 0.1858
db = DBSCAN(algorithm='ball_tree', eps=eps, min_samples=0, metric="haversine").fit(np.radians(variable))
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

# Print DBSCAN results for visualization
unique_labels = set(labels)
colors = [plt.cm.Spectral(each)
          for each in np.linspace(0, 1, len(unique_labels))]
for k, col in zip(unique_labels, colors):
    class_member_mask = (labels == k)
    xy = variable[class_member_mask & core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=14)
    xy = variable[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=6)
plt.title('Number of clusters: %d' % n_clusters_)
plt.show()

# Add a cluster number to every Country
data['geocluster_value'] = labels

# Using KMeans for clustering PIB + position
variable = np.array(data[['2019', 'geocluster_value']])
kmeans = KMeans(n_clusters=10).fit(variable)
centroids = kmeans.cluster_centers_

# Predicting the clusters
labels = kmeans.predict(variable)
data['group_label'] = labels

# Getting the cluster centers
centers = kmeans.cluster_centers_

# Draw the clusters
colour = ['red', 'green', 'blue', 'cyan', 'yellow', 'black', 'white', 'magenta', 'purple', 'brown']
colour_vector = []
for row in labels:
    colour_vector.append(colour[row])

plt.scatter(variable[:, 0], variable[:, 1], c=colour_vector, s=30)
plt.scatter(centers[:, 0], centers[:, 1], marker='*', c=colour, s=100)
plt.show()

# Prepare data for output in the requested format
output = data.copy()
output = output.drop(['Alpha-3 code', 'Longitude(average)', 'Latitude(average)', 'geocluster_value'], axis=1)
output = output.rename(columns={'2019': 'GDP per capita'})

# Adding means for each group
means = []
group_sum = []
for i in range(0, 10):
    group = output[output['group_label'] == i]
    means.append((np.double(group['GDP per capita'].sum()) / len(group)).round(decimals=2))
    group_sum.append(np.double(group['GDP Total'].sum()))

conditions = [
    (output['group_label'] == 0), (output['group_label'] == 1),
    (output['group_label'] == 2), (output['group_label'] == 3),
    (output['group_label'] == 4), (output['group_label'] == 5),
    (output['group_label'] == 6), (output['group_label'] == 9),
    (output['group_label'] == 7), (output['group_label'] == 8)]
output['group average'] = np.select(conditions, means, default='')
output['group average'] = output['group average'].astype('double')

# Order table
output = output.sort_values(['group average', 'GDP Total'], kind='mergesort', ascending=[False, False])

# Cumulative GDP fraction
cumulatives = []
for index, row in output.iterrows():
    i = row['group_label']
    cumulatives.append(row['GDP Total'] / group_sum[i])
output['GDP Cumulative'] = cumulatives

# Create a report for visualize the output
prof = ProfileReport(output)
prof.to_file(output_file='output.html')

# Export to csv
output.to_csv(r'C:/Users/i100v/PycharmProjects/Geoeconomical clustering/output/geoeconomical-clustering.csv',
              index=False)
