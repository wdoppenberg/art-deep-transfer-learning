import glob
import random
import xmltodict
import os
import pandas as pd
import numpy as np

ART_DATASET = 'https://ndownloader.figshare.com/articles/5660617/versions/1'

# Not functional at this time
'''def download():
    """
    Helper function for downloading a file to disk
    """

    data_dir = u"./dataset/"

    urllib3.request.urlretrieve(ART_DATASET, data_dir + "/art")'''

def random_art():
    """
    Returns XML data from randomly chosen piece of art in dataset
    """
    path = random.choice(glob.glob('datasets/xml2/*.xml'))
    d = {}
    with open(path) as f:
        d = xmltodict.parse(f.read())

    return d

def xml_files2csv():
    directory = r"..\metadata\data\rijksxml\xml2"
    directory_excel_export = r'..\metadata\data\export_info_art_df_run3.csv'
    columns_df = ['ImageId', 'dc_creator', 'dc_materiaal', 'dc_type']
    i = 0
    for filename in os.listdir(directory):
        try:
            dict_xml = xmltodict.parse(open(os.path.join(directory, filename)).read())
            try:
                creators = dict_xml["record"]["metadata"]["oai_dc:dc"]["dc:creator"]
                type_art = dict_xml["record"]["metadata"]["oai_dc:dc"]["dc:type"]
                format_art = dict_xml["record"]["metadata"]["oai_dc:dc"]["dc:format"]
            except KeyError:
                continue
            if isinstance(creators, list):
                list_creators = []
                for creator in creators:
                    list_creators.append(creator.split(':')[1])
                creator = ','.join(list_creators)

            else:
                creator = creators.split(':')[1]
        
            
            materials_art = []
            for string in format_art:
                try:
                    split_string = string.split(':')
                    if split_string[0] == 'materiaal':
                        materials_art.append(split_string[1].strip())
                except AttributeError:
                    materials_art = ['']
            if isinstance(type_art, list):
                
                try:
                    type_art = ','.join(type_art)
                except TypeError:
                    filter_none = filter(None, type_art)
                    type_art = []
                    for type__ in filter_none:
                        type_art.append(type__)
                    type_art = ','.join(type_art)    
            data = [filename[:-4], creator, ','.join(materials_art), type_art]
            dataframe_art = pd.DataFrame(data = np.array([data]), columns = columns_df)
            if i == 0:
                info_art_dataframe = dataframe_art
                i+=1
            else:
                info_art_dataframe = pd.concat([info_art_dataframe, dataframe_art])
                i+=1
        except UnicodeDecodeError:
            continue        
    info_art_dataframe.to_csv (directory_excel_export, index = False, header=True)


print(xml_files2csv())