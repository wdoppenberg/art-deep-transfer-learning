import glob
import random
import xml.etree.ElementTree as ET

ART_DATASET = 'https://ndownloader.figshare.com/articles/5660617/versions/1'

# Not functional at this time
def download():
    """
    Helper function for downloading a file to disk
    """

    data_dir = u"./dataset/"

    urllib3.request.urlretrieve(ART_DATASET, data_dir + "/art")

def random_art():
    """
    Returns XML data from randomly chosen piece of art in dataset
    """
    path = random.choice(glob.glob('datasets/xml2/*.xml'))
    tree = ET.parse(path)
    root = tree.getroot()
    return root