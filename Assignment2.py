
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. This is the dataset to use for this assignment. Note: The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.

# In[7]:

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')


# In[33]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fd403b3054061a52e5c4a08dadc245bc6e1b0adabbf12a9eadba68e8.csv')
df.head()


# In[36]:

df['Year'] = df['Date'].apply(lambda x: x[:4])
df['Month-Day'] = df['Date'].apply(lambda x: x[5:])
df = df[df['Month-Day'] != '02-29']


# In[44]:

min_temp = df[(df['Element'] == 'TMIN') & (df['Year'] != '2015')].groupby('Month-Day')['Data_Value'].agg({'min_temp_mean': np.mean})
max_temp = df[(df['Element'] == 'TMAX') & (df['Year'] != '2015')].groupby('Month-Day')['Data_Value'].agg({'max_temp_mean': np.mean})

min_temp_2015 = df[(df['Element'] == 'TMIN') & (df['Year'] == '2015')].groupby('Month-Day')['Data_Value'].agg({'min_temp_2015_mean': np.mean})
max_temp_2015 = df[(df['Element'] == 'TMAX') & (df['Year'] == '2015')].groupby('Month-Day')['Data_Value'].agg({'max_temp_2015_mean': np.mean})


# In[45]:

min_temp = min_temp.reset_index()
max_temp = max_temp.reset_index()

min_temp_2015 = min_temp_2015.reset_index()
max_temp_2015 = max_temp_2015.reset_index()


# In[47]:

new_min = (min_temp_2015[min_temp_2015['min_temp_2015_mean'] < min_temp['min_temp_mean']]).index.tolist()
new_max = (max_temp_2015[max_temp_2015['max_temp_2015_mean'] > max_temp['max_temp_mean']]).index.tolist()


# In[83]:

plt.figure()

plt.plot(min_temp['min_temp_mean'], '-', c='y', alpha = 0.75, label = 'Low Temps')
plt.plot(max_temp['max_temp_mean'], '-', c='r', alpha = 0.75, label = 'High Temps')

plt.scatter(new_min, min_temp_2015['min_temp_2015_mean'].iloc[new_min], s = 1, c = 'b', label = 'New Min')
plt.scatter(new_max, max_temp_2015['max_temp_2015_mean'].iloc[new_max], s = 1, c = 'purple', label = 'New Max')

plt.xlabel('Month')
plt.ylabel('Temperatures')
plt.title('Changes in temperatures from 2005 to 2014 and additionally in 2015')
plt.gca().axis([-5,365, -100, 650])


# In[84]:

plt.gca().fill_between(range(len(min_temp)), min_temp['min_temp_mean'], max_temp['max_temp_mean'],
                      facecolor = 'lightblue', alpha = 0.2)

plt.legend(['10 Year High', '10 Year Low', 'Record High', 'Record Low'], frameon=False, loc = 1)

axes = plt.axes()
axes.set_xticklabels(['January','February', 'March','April','May', 'June', 'July', 'August', 
                      'September', 'October', 'November', 'December'])

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.show()


# In[85]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fd403b3054061a52e5c4a08dadc245bc6e1b0adabbf12a9eadba68e8.csv')
df.head()

df['Year'] = df['Date'].apply(lambda x: x[:4])
df['Month-Day'] = df['Date'].apply(lambda x: x[5:])
df = df[df['Month-Day'] != '02-29']

min_temp = df[(df['Element'] == 'TMIN') & (df['Year'] != '2015')].groupby('Month-Day')['Data_Value'].agg({'min_temp_mean': np.mean})
max_temp = df[(df['Element'] == 'TMAX') & (df['Year'] != '2015')].groupby('Month-Day')['Data_Value'].agg({'max_temp_mean': np.mean})
min_temp_2015 = df[(df['Element'] == 'TMIN') & (df['Year'] == '2015')].groupby('Month-Day')['Data_Value'].agg({'min_temp_2015_mean': np.mean})
max_temp_2015 = df[(df['Element'] == 'TMAX') & (df['Year'] == '2015')].groupby('Month-Day')['Data_Value'].agg({'max_temp_2015_mean': np.mean})

min_temp = min_temp.reset_index()
max_temp = max_temp.reset_index()
min_temp_2015 = min_temp_2015.reset_index()
max_temp_2015 = max_temp_2015.reset_index()

new_min = (min_temp_2015[min_temp_2015['min_temp_2015_mean'] < min_temp['min_temp_mean']]).index.tolist()
new_max = (max_temp_2015[max_temp_2015['max_temp_2015_mean'] > max_temp['max_temp_mean']]).index.tolist()

plt.figure()
plt.plot(min_temp['min_temp_mean'], '-', c='y', alpha = 0.75, label = 'Low Temps')
plt.plot(max_temp['max_temp_mean'], '-', c='r', alpha = 0.75, label = 'High Temps')
plt.scatter(new_min, min_temp_2015['min_temp_2015_mean'].iloc[new_min], s = 1, c = 'b', label = 'New Min')
plt.scatter(new_max, max_temp_2015['max_temp_2015_mean'].iloc[new_max], s = 1, c = 'purple', label = 'New Max')

plt.xlabel('Month')
plt.ylabel('Temperatures')
plt.title('Changes in temperatures from 2005 to 2014 and additionally in 2015')
plt.gca().axis([-5,365, -100, 650])
plt.gca().fill_between(range(len(min_temp)), min_temp['min_temp_mean'], max_temp['max_temp_mean'],
                      facecolor = 'lightblue', alpha = 0.2)

plt.legend(['10 Year High', '10 Year Low', 'Record High', 'Record Low'], frameon=False, loc = 1)

axes = plt.axes()
axes.set_xticklabels(['January','February', 'March','April','May', 'June', 'July', 'August', 
                      'September', 'October', 'November', 'December'])

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.show()


# In[ ]:



