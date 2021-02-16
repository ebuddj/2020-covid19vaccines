#!/usr/bin/python
# -*- coding: UTF8 -*-
# @See http://www.python.org/dev/peps/pep-0263/

#######
# ABOUT
#######

# Fire location analysis

########
# AUTHOR
########

# Teemo Tebest (teemo.tebest@gmail.com)

#########
# LICENSE
#########

# CC-BY-SA 4.0 EBU / Teemo Tebest

#######
# USAGE
#######

# python 2021-covid19vaccines.py

# Load the Pandas libraries with alias pd.
import pandas as pd

# Import glob for reading files.
import glob

# Import datetime for getting the current date.
from datetime import datetime

# Read the file and filter columns.
f = '../data/owid-covid-data.csv'
f = 'https://covid.ourworldindata.org/data/owid-covid-data.csv?v=' + str(datetime.date(datetime.now()))
df = pd.read_csv(f, usecols=['continent','location','date','total_vaccinations_per_hundred'])

# Filter data by row values.
df = df[df['continent'] == 'Europe']

# Convert NaN to None
# https://stackoverflow.com/questions/28639953/python-json-encoder-convert-nans-to-null-instead/34467382#34467382
df = df.where(pd.notnull(df), 0)

# List of ERNO countries
erno_countries = ['Albania','Bosnia and Herzegovina','Bulgaria','Croatia','Hungary','Kosovo','Montenegro','North Macedonia','Romania','Serbia','Slovenia']

# Loop throught the ERNO countries and create data.
data = {}
df_erno = df[df['date'] > '2020-12-24']
for erno_country in erno_countries:
  previous_value = 0
  data[erno_country] = {'Province_State':erno_country}
  for index, values in (df_erno[df_erno['location'] == erno_country]).iterrows():
    if values.total_vaccinations_per_hundred != 0:
      previous_value = values.total_vaccinations_per_hundred
      data[erno_country][values.date] = values.total_vaccinations_per_hundred
    else:
      data[erno_country][values.date] = previous_value

# Export data.
import json
data = {'vaccinated':data}
with open('../media/data/data_erno.json', 'w') as outfile:
  json.dump(data, outfile)

data = {}
df = df[df['date'] > '2020-12-10']
# https://chrisalbon.com/python/data_wrangling/pandas_list_unique_values_in_column/
for country in df.location.unique():
  country_data_name = country
  if country == 'Vatican':
    country_data_name = 'Holy See';
  if country == 'Isle of Man' or country == 'Faeroe Islands' or country == 'Guernsey' or country == 'Jersey' or country == 'Gibraltar':
    continue
  previous_value = 0
  data[country_data_name] = {'Province_State':country_data_name}
  for index, values in (df[df['location'] == country]).iterrows():
    if values.total_vaccinations_per_hundred != 0:
      previous_value = values.total_vaccinations_per_hundred
      data[country_data_name][values.date] = values.total_vaccinations_per_hundred
    else:
      data[country_data_name][values.date] = previous_value

# Export data.
import json
data = {'vaccinated':data}
with open('../media/data/data.json', 'w') as outfile:
  json.dump(data, outfile)

