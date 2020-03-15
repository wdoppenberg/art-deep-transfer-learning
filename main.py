import transfer_learning_experiment.from_one_art_to_another as foata
import transfer_learning_experiment.imagenet_to_art as ita

from reproducibility import data

#data.xml_files2csv()

tl_modes = ("fine_tuning" "off_the_shelf")
dataset_name = "test" #The name of your dataset

metadata_path = r"metadata/labels/export_info_art_df_run3.csv" #The path to your metadata file in .csv extension
jpg_images_path = r"metadata/data/rijks/" #The path to your images in *.jpg

ANN = "RijksVGG19"

results_path = r"./results/" #The path where wou would like to store your results
datasets_path = r"./datasets/" #The path where the hdf5 files will be stored for the experiments

tl_mode = "off_the_shelf" #Choose a pre-training mode from tl_modes

if __name__ == '__main__':

    from transfer_learning_experiment.from_one_art_to_another.transfer_learning_experiment_torch import ExperimentHandler

    experiment = ExperimentHandler(ANN, dataset_name, metadata_path, 
        jpg_images_path, results_path, 
        datasets_path, tl_mode)

    experiment.start_experiment()