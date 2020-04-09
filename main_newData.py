import transfer_learning_experiment.from_one_art_to_another as foata
import transfer_learning_experiment.imagenet_to_art as ita
import os 
os.environ['HDF5_DISABLE_VERSION_CHECK']='2'

from reproducibility import data
import pandas as pd
#data.xml_files2csv()

tl_modes = ("fine_tuning" "off_the_shelf")
dataset_name = "test_new" #The name of your dataset

metadata_path = r"Newdatasets/Newdata_info.csv" #The path to your metadata file in .csv extension
jpg_images_path = r"Newdatasets/test/" #The path to your images in *.jpg

ANN = "RijksVGG19"

results_path = r"./Newdatasets/results/" #The path where wou would like to store your results
datasets_path = r"./Newdatasets/results/" #The path where the hdf5 files will be stored for the experiments

tl_mode = "off_the_shelf" #Choose a pre-training mode from tl_modes

if __name__ == '__main__':

    from transfer_learning_experiment.from_one_art_to_another.import_new_dataset import ExperimentHandler
    print('came here')
    experiment = ExperimentHandler(ANN, dataset_name, metadata_path, 
        jpg_images_path, results_path, 
        datasets_path, tl_mode)

    experiment.start_experiment()