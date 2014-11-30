import unittest
import os
import shutil
from geobricks_gdal_calc.core.gdal_calc import calc_layers

path = "../test_data/burundi_maize_area/"
layer1 = path + "burundi_maize_area_3857.tif"
layer2 = path + "burundi_maize_area_3857.tif"
files_path = []
files_path.append(layer1)
files_path.append(layer1)
outputpath = path + "output/"

if os.path.isdir(outputpath):
    shutil.rmtree(outputpath)
os.makedirs(outputpath)

class GeobricksUnitTest(unittest.TestCase):

    def test_sum(self):
        outputfile = outputpath + "output_sum.tif"
        result = calc_layers(files_path, outputfile, "sum")
        self.assertEqual(result, True)





