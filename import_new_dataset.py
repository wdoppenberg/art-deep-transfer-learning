'''
import pandas as pd
metadata_pd = pd.read_csv('./openaccess/MetObjects.csv') 
 
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(metadata_pd.head())

'''

import requests


response = requests.get("http://collectionapi.metmuseum.org/public/collection/v1/objects/")
print(response.status_code)
