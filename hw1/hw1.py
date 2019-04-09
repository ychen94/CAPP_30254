# Problem 1: Data Acquisition and Analysis
## download the first 50000 rows of data
import requests
import pandas as pd
path = 'https://data.cityofchicago.org/resource/d62x-nvdr.json?$limit=50000'
r = requests.get(path).json()
crimes_2017 = pd.DataFrame(r[1:], columns=r[0])
crimes_2017

path = 'https://data.cityofchicago.org/resource/3i3m-jwuy.json?$limit=50000'
j = requests.get(path).json()
crimes_2018 = pd.DataFrame(j[1:], columns=j[0])

## 1. count the frequency of each type of crime
frequency_2017 = crimes_2017['primary_type'].value_counts()
frequency_2018 = crimes_2018['primary_type'].value_counts()

print('The Three Most Common Types of Crime in 2017:')
print(frequency_2017.head(3))
print('The Three Most Common Types of Crime in 2018:')
print(frequency_2018.head(3))

## 2. calculate the change of crimes over time
time_trend = frequency_2017.reset_index().merge(frequency_2018.reset_index(), on='index', how='outer')
time_trend.columns = ['Types', '2017', '2018']
time_trend['Sum'] = time_trend['2018'] + time_trend['2017']
time_trend['Change'] = time_trend['2018'] - time_trend['2017']
time_trend = time_trend.sort_values('Sum', ascending=False)
print('The Change of Three Most Common Types of Crime over Time:')
print(time_trend.head(3))

## plot the change over time
import matplotlib.pyplot as plt
ax1 = time_trend.plot.bar(x='Types', y='Change')
ax1.set_title('The Change of Three Most Common Types of Crime over Time')
ax1

## 3. find the three community area with the most homicides
homicide_2017 = crimes_2017[crimes_2017['primary_type'] == 'HOMICIDE']
community_2017 = homicide_2017['community_area'].value_counts().reset_index()
homicide_2018 = crimes_2018[crimes_2018['primary_type'] == 'HOMICIDE']
community_2018 = homicide_2018['community_area'].value_counts().reset_index()

homicide = community_2017.merge(community_2018, on='index', how='outer').fillna(0)
homicide.columns = ['Community Area', '2017', '2018']

## 4. calculate the change by community area over time
homicide['Sum'] = homicide['2018'] + homicide['2017']
homicide['Change'] = homicide['2018'] - homicide['2017']
homicide = homicide.sort_values('Sum', ascending=False)
print('The Three Community Areas with Most Homicides:')
print('25 Austin, 23 Humboldt Park, 49 Roseland')
print(homicide.head(3))
## data from https://www.chicago.gov/content/dam/city/depts/doit/general/GIS/Chicago_Maps/Citywide_Maps/Community_Areas_W_Numbers.pdf

## plot the change over time
ax2 = homicide[homicide['Sum']>5].plot.bar(x='Community Area', y='Change')
ax2.set_title('The Change of Homicides in Each Community Area over Time')
ax2




# Problem 2: Data Augmentation and APIs
## download the census data
api = 'https://data.cityofchicago.org/resource/kn9c-c2s2.json'
j = requests.get(api).json()
census = pd.DataFrame(j[1:], columns=j[0])

## 1. What types of blocks have reports of “BATTERY”?
battery_2017 = crimes_2017[crimes_2017['primary_type'] == 'BATTERY']
community_2017 = battery_2017['community_area'].value_counts().reset_index()
battery_2018 = crimes_2018[crimes_2018['primary_type'] == 'BATTERY']
community_2018 = battery_2018['community_area'].value_counts().reset_index()

battery = community_2017.merge(community_2018, on='index', how='outer').fillna(0)
battery.columns = ['ca', '2017', '2018']
batteries = battery.head(3).merge(census, how='left')
batteries = batteries.append(census[census['community_area_name'] == 'CHICAGO'])
print(batteries)
print('Compare to the Average Level of Chicago, Community Areas with Most Batteries have:')
print('lower per capita income, higher unemployment rate, and lower education level.')

## 2. What types of blocks get “Homicide”?
homicides = homicide.head(3).merge(census, left_on='Community Area', right_on='ca', how='left')
homicides = homicides.append(census[census['community_area_name'] == 'CHICAGO'])
print(homicides)
print('Compare to the Average Level of Chicago, Community Areas with Most Homicides have:')
print('lower per capita income, higher unemployment rate, and lower education level.')

## 3. Does that change over time in the data you collected?
battery['Sum'] = battery['2018'] + battery['2017']
battery['Change'] = battery['2018'] - battery['2017']
battery = battery.sort_values('Sum', ascending=False)
ax3 = battery[battery['Sum']>200].plot.bar(x='ca', y='Change')
ax3.set_xlabel('Community Areas')
ax3.set_title('The Change of Homicides in Each Community Area over Time')
ax3

ax2

## 4. What is the difference in blocks that get “Deceptive Practice” vs “Sex Offense”?
## deceptive practice
deceptive_2017 = crimes_2017[crimes_2017['primary_type'] == 'DECEPTIVE PRACTICE']
community_2017 = battery_2017['community_area'].value_counts().reset_index()
deceptive_2018 = crimes_2018[crimes_2018['primary_type'] == 'DECEPTIVE PRACTICE']
community_2018 = battery_2018['community_area'].value_counts().reset_index()

deceptive = community_2017.merge(community_2018, on='index', how='outer').fillna(0)
deceptive.columns = ['ca', '2017', '2018']
deceptive['Sum'] = deceptive['2018'] + deceptive['2017']
deceptive['Change'] = deceptive['2018'] - deceptive['2017']
deceptive = deceptive.sort_values('Sum', ascending=False)

deceptives = deceptive.head(3).merge(census, how='left')
deceptives[['per_capita_income_', 'percent_aged_16_unemployed', 'percent_aged_25_without_high_school_diploma']]

## sex offense
sex_2017 = crimes_2017[crimes_2017['primary_type'] == 'SEX OFFENSE']
community_2017 = sex_2017['community_area'].value_counts().reset_index()
sex_2018 = crimes_2018[crimes_2018['primary_type'] == 'SEX OFFENSE']
community_2018 = sex_2018['community_area'].value_counts().reset_index()

sex = community_2017.merge(community_2018, on='index', how='outer').fillna(0)
sex.columns = ['ca', '2017', '2018']
sex['Sum'] = sex['2018'] + sex['2017']
sex['Change'] = sex['2018'] - sex['2017']
sex = sex.sort_values('Sum', ascending=False)

sex_offenses = sex.head(3).merge(census, how='left')
sex_offenses[['per_capita_income_', 'percent_aged_16_unemployed', 'percent_aged_25_without_high_school_diploma']]

## print out results
print('Compare to Community Areas with Most Deceptive Practice, Areas with Most Sex Offense have:')
print('lower per capita income, higher unemployment rate, and lower education level.')
