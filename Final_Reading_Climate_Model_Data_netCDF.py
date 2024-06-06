#!/usr/bin/env python
# coding: utf-8

# # **This notebook will go over how to read netCDF files**

# ## **Reading in netCDF files:**
# * We will use xarray (a Python package) to read data stored in Network Common Data Format(netCDF)

# ```python 
# import xarray as xr 
# import numpy as np
# 
# data_ncdf = xr.open_dataset('file_path4.cdf') # use xarray to open the data file
# ```

# * To view the contents of the data, which is stored as an xarray.Dataset object, you can use '.head()'syntax or 'print()' command.
# ```python
# data_ncdf.head()
# ```
# ```python
# print(data_ncdf)
# ```

# * We can also use the 'netCDF4' library to read and manipulate data stored in NetCDF format.

# ```python
# import netCDF4 as nc
# 
# nc_file = nc.Dataset('file_path5.nc', 'r') # opening netCDF file, read-only
# ```

# * You can acess and work with data in the file using the attributes 'variables' and 'dimensions'.
# 
# Print a list of the variables in the file using
# ```python
# print(nc_file.variables) 
# ```
# 
# Print the dimensions in the file
# ```python
# print(nc_file.dimensions) 
# ```
# 
# Access a specific variable by name
# ```python
# print(nc_file.variables['variable_name']) 
# ```

# ## NetCDF: Dimensions and Variables
# 
# **Dimensions** define the sizes of the data arrays along specific axes in the file, providing shape and size information for variables.
# 
# * Typically used to define coordinate variables. Ex: a dimension 'time' with size 365 means there are 365 data values along the time axis in the corresponding variable
# * Usefulness of dimensions:
# 
# 1.   Data Extraction: knowing the structure of the data allows you to extract specific subsets of the data (such as data within a certain time frame, region, or depth level, which are determined by the dimensions)
# 2.   Data Analysis and Visualization: dimensions provide context for data analysis and for the creation of meaningful plots, maps, and other visuals
# 3.   Metadata Interpretation: associated meta data (units, description, etc.) is helpful when interpreting and using data correctly
# 4.   Data Integration: understanding dimensions is critical when integrating/merging data from different files or sources
# 
# 
# **Variables** hold the actual data values as multidimensional arrays associated with dimensions.
# 
# * They are defined using one or more dimensions that specify the size of each dimension of the variable.
# * Ex: a variable 'temperature' with dimensions time, lat, and lon
# 
# ```
# temperature(time, lat, lon)
# ```

# ## Next: using the files we opened using python and its packages to create figures

# Decide which data to use: 
# * from NCAR CESM2 (CMIP6 20th century experiments (1850-2014) with CAM6, interactive land (CLM5), coupled ocean (POP2) with biogeochemistry (MARBL), interactive sea ice (CICE5.1), and non-evolving land ice (CISM2.1)) _(.nc)_

# import necessary libraries (or use conda on terminal)
# ```python
# import xarray as xr
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# ```

# ### netCDF from CMIP6 CESM2 future scenario SSP2-4.5
# * downloading it: things to consider
# - model version, scenario, time period, variable to look at, variant id
# > * variant id 
# > - CMIP6 netCDF file metadata includes the variant-id global attribute (w/ format r1i1p1f1), where the numbers are indices for particular configurations of:
# r: realisation (i.e. ensemble member)
# i: initialisation method
# p: physics
# f: forcing 
# https://ukesm.ac.uk/cmip6/variant-id/ (source for above...note that org. is based in the UK)

# In[24]:


# open netCDF file using xarray
import xarray as xr
data = xr.open_dataset('Downloads/tas_day_CESM2-WACCM_ssp245_r1i1p1f1_gn_20150101-20241231.nc')

# viewing the data
print(data)


# In[25]:


type(data)

# call for the variables being stored in the file 
print(data.variables.keys())


# In[26]:


# explore each of the variables individually

lon = data.variables['lon']
print(lon)

# this will show what the units are for the variable, as well as other useful information such as the the standard name

# there are 288 horizontal lines


# In[27]:


lat = data.variables['lat']
print(lat)
# there are 192 verticle lines 


# In[28]:


time = data.variables['time']
print(time)

# we can see that first date and the last date that is included 
# notice that 'time' is an object here 


# In[29]:


# first entry for time: we'll need to change this format to datetime64[ns]

data.coords['time'].values[0] 


# In[30]:


# convert 'time' coordinate to datetime64[ns]

data['time'] = data.indexes['time'].to_datetimeindex()
data.close()

# format of time: xarray decodes datetime and timedelta arrays using CF conventions 


# In[31]:


print(data) # now time is in a datatime format


# In[32]:


# viewing array in netCDF using xarray 

time = data.variables['time']
view_time = data['time'].values 
print(view_time)


# ### Now that we have data ready, we'll define an area of interest to make a time series

# In[33]:


# extracting the data into a time series 


# Box defining region of interest (you must select what area you want to look at or the computer will crash --> too much data in climate model)
regbox = [-15,15,90,270]  # tropical Pacific

# Mask: True where longitude is inside the box, False if it is outside
mask_lon = (data.lon >= regbox[2]) & (data.lon <= regbox[3])

# Mask: True where latitude is inside the box, False if it is outside
mask_lat = (data.lat >= regbox[0]) & (data.lat <= regbox[1])

# Do regional average
regavg = data.where(mask_lon & mask_lat, drop=True).squeeze()

print(regavg) # notice that the region is now smaller: lat and lon size


# In[34]:


# choose coordinates 


lat_idx, lon_idx = 9, 124 # around the pacific ocean (Philippines: Bohol Sea)
time_series = regavg['tas'][:, lat_idx, lon_idx]
print(time_series)


# In[35]:


import matplotlib.pyplot as plt
plt.figure(figsize=(10,6), dpi=300)
plt.plot(time_series['time'], time_series.values)
plt.title('TAS for in the Pacific Ocean (CMIP6)', fontsize=16)
plt.xlabel('Year', fontsize=14)
plt.ylabel('TAS (K)', fontsize=14)
#convert the timeseries to one that matplotlib can read (data does not account for leap yrs.)

