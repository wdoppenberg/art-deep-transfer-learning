import pandas as pd, numpy as np
import h5py
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

import glob, os

metadata_path = 'metadata_rijks.csv'
datasets_path = 'datasets/'
images_path = 'images/'

metadata = pd.read_csv(metadata_path, sep='|')

# Filter data
metadata.dropna(inplace=True)
metadata = metadata[~metadata['fullname_creator'].str.contains('anoniem')]
metadata = metadata[metadata['fullname_creator'] != ' ']

df_images = pd.DataFrame({'filename': os.listdir(images_path)})
df_images['image_id'] = df_images['filename'].str.replace('.jpg','')

metadata = pd.merge(metadata, df_images, on='image_id')

# Encode data
encoder = LabelEncoder()

metadata['fullname_creator_cat'] = encoder.fit_transform(metadata['fullname_creator'].astype(str))
metadata['material_cat'] = encoder.fit_transform(metadata['material'].astype(str))
metadata['type_cat'] = encoder.fit_transform(metadata['type'].astype(str))

# Save metadata
metadata.to_csv('metadata_rijks_enc.csv')

# Create splits
df_train, df_val = train_test_split(metadata, test_size=0.2, random_state=42)
df_val, df_test = train_test_split(df_val, test_size=0.2, random_state=42)

df_train.reset_index(inplace=True)
df_val.reset_index(inplace=True)
df_test.reset_index(inplace=True)

# Create HDF5 files
def create_h5(df, hdf5name):
    # Exception occurs when files already exist.
    with h5py.File(hdf5name, 'w-') as f:
        dt_string = h5py.string_dtype()
        dset_fullname_creator = f.create_dataset('fullname_creator', (len(df.index),), dtype=dt_string)
        dset_material = f.create_dataset('material', (len(df.index),), dtype=dt_string)
        dset_type = f.create_dataset('type', (len(df.index),), dtype=dt_string)

        dset_fullname_creator_cat = f.create_dataset('fullname_creator_cat', (len(df.index),), dtype=dt_string)
        dset_material_cat = f.create_dataset('material_cat', (len(df.index),), dtype=dt_string)
        dset_type_cat = f.create_dataset('type_cat', (len(df.index),), dtype=dt_string)

        dt_uint8 = h5py.special_dtype(vlen=np.dtype('uint8'))
        dset_img = f.create_dataset('images', (len(df.index),), dtype=dt_uint8)
        
        for i, r in df.iterrows():
            filename = str(r['filename'])
            print(f'[{i}]: {filename}')
            with open(images_path+filename, 'rb') as fin:
                dset_img[i] = np.frombuffer(fin.read(), dtype='uint8')
            
            dset_fullname_creator[i] = r['fullname_creator']
            dset_fullname_creator_cat[i] = r['fullname_creator_cat']

            dset_material[i] = r['material']
            dset_material_cat[i] = r['material_cat']

            dset_type[i] = r['type']
            dset_type_cat[i] = r['type_cat']
    print('Done')

create_h5(df_train, 'datasets/training.hdf5')
create_h5(df_val, 'datasets/validation.hdf5')
create_h5(df_test, 'datasets/testing.hdf5')