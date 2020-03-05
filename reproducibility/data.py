import glob
import random
import xmltodict

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
    d = {}
    with open(path) as f:
        d = xmltodict.parse(f.read())

    return d
    
print(random_art()['record']['metadata']['oai_dc:dc']['dc:creator'])