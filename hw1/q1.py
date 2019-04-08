# download the first 50000 rows of data
import requests
import pandas as pd
path = 'https://data.cityofchicago.org/resource/d62x-nvdr.json?$limit=50000'
r = requests.get(path).json()
crimes_2017 = pd.DataFrame(r[1:], columns=r[0])
crimes_2017

path = 'https://data.cityofchicago.org/resource/3i3m-jwuy.json?$limit=50000'
j = requests.get(path).json()
crimes_2018 = pd.DataFrame(j[1:], columns=j[0])

# count the frequency of each type of crime in the column 'primary_type'
frequency_2017 = crimes_2017['primary_type'].value_counts()
frequency_2018 = crimes_2018['primary_type'].value_counts()

# print out the results
print('The Three Most Common Types of Crime in 2017:')
print(frequency_2017.head(3))
print('The Three Most Common Types of Crime in 2018:')
print(frequency_2018.head(3))

# calculate the change over time
time_trend = frequency_2017.reset_index().merge(frequency_2018.reset_index(), on='index', how='outer')
time_trend.columns = ['Types', '2017', '2018']
time_trend['Sum'] = time_trend['2018'] + time_trend['2017']
time_trend['Change'] = time_trend['2018'] - time_trend['2017']
time_trend = time_trend.sort_values('Sum', ascending=False)
print(time_trend.head(3))

# plot the change over time
import matplotlib.pyplot as plt
ax1 = time_trend.plot.bar(x='Types', y='Change')
ax1

# the number of the community area with the most homicides in 2017
homicide_2017 = crimes_2017[crimes_2017['primary_type'] == 'HOMICIDE']
community_2017 = homicide_2017['community_area'].value_counts().reset_index()
homicide_2018 = crimes_2018[crimes_2018['primary_type'] == 'HOMICIDE']
community_2018 = homicide_2018['community_area'].value_counts().reset_index()

homicide = community_2017.merge(community_2018, on='index', how='outer').fillna(0)
homicide.columns = ['Community Area', '2017', '2018']

# calculate the change over time
homicide['Sum'] = homicide['2018'] + homicide['2017']
homicide['Change'] = homicide['2018'] - homicide['2017']
homicide = homicide.sort_values('Sum', ascending=False)
print(homicide.head(3))

## data from https://www.chicago.gov/content/dam/city/depts/doit/general/GIS/Chicago_Maps/Citywide_Maps/Community_Areas_W_Numbers.pdf
print('The Three Community Areas with Most Homicides: 25 Austin, 23 Humboldt Park, 49 Roseland')

# plot the change over time
ax2 = homicide[homicide['Sum']>5].plot.bar(x='Community Area', y='Change')
ax2
