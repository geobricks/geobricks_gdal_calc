import subprocess
import os
import random
import string
import glob
from geobricks_gdal_calc.utils.log import logger

log = logger(__file__)

# base script location
base_script_gdal_calculations = os.path.join(os.path.dirname(__file__), "scripts", "gdal_calculations.py")


def _random_char(char_numbers=5):
    """
    Create random char_numbers used for the id of the layers in the alphalist
    :param char_numbers: number of chars
    :type int
    :return: a random sequence of chars
    """
    return ''.join(random.choice(string.ascii_letters) for x in range(char_numbers)).lower()


def _create_cmd_filelist_from_path(files_path, alphalist):
    """
    Create cmd command for the list of files
    :param files_path: path to the files i.e. "/path/*.tif"
    :type string
    :param alphalist: array used as alphalist.
    :type array
    :return: return the cmd command part related
    """
    return _create_cmd_filelist_from_array(glob.glob(files_path), alphalist)

def _create_cmd_filelist_from_array(files, alphalist):
    """
    Create cmd command for the list of files
    :param files: List of the files i.e. ["/path/a.tif","/path/b.tif"]
    :type array
    :param alphalist: array used as alphalist.
    :type array
    :return: cmd command
    """
    cmd = ""
    for file_path in files:
        try:
            file_var = _random_char()
            alphalist.append(file_var)
            cmd += " --" + file_var + " " + file_path
        except Exception, e:
            raise Exception(e)
    return cmd


def _create_cmd_calc_sum(alphalist):
    """
    Create cmd "--calc" to SUM all the layers
    :param alphalist: List of files alias
    :type array
    :return: cmd command
    """
    cmd = ' --calc="('
    index=0
    for filevar in alphalist :
        cmd += filevar
        index += 1
        if index < len(alphalist):
            cmd += "+"
    cmd += ')"'
    return cmd

def _create_cmd_calc_avg(alphalist):
    """
    Create cmd "--calc" to AVG all the layers
    :param alphalist: List of files alias
    :type array
    :return: cmd command
    """
    cmd = ' --calc="('
    index=0
    for filevar in alphalist :
        cmd += filevar
        index += 1
        if index < len(alphalist):
            cmd += "+"
    cmd += ')/' + str(len(alphalist)) + '"'
    return cmd


def _create_cmd_calc_diff(alphalist):
    """
    Create cmd "--calc"
    Difference between the first layer and all the other layers
    :param alphalist: List of files alias
    :type array
    :return: cmd command
    """
    cmd = ' --calc="('
    index=0
    for filevar in alphalist :
        cmd += filevar
        index += 1
        if index < len(alphalist):
            cmd += "-"
    cmd += ')"'
    return cmd


def _create_cmd_calc_mult(alphalist):
    """
    Create cmd "--calc"
    Difference between the first layer and all the other layers
    :param alphalist: List of files alias
    :type array
    :return: cmd command
    """
    cmd = ' --calc="('
    index=0
    for filevar in alphalist :
        cmd += filevar
        index += 1
        if index < len(alphalist):
            cmd += "*"
    cmd += ')"'
    return cmd


def _create_cmd_calc_ratio(alphalist):
    """
    Create cmd "--calc"
    Ration between the first layer and the second layer
    :param alphalist: List of files alias
    :type array
    :return: cmd command
    """
    # TODO: doesn't make a float there are problems with the 0 values otherwise
    cmd = " --type Float32 --NoDataValue=0 "
    # TODO: check if the conversion can affect the perfomance
    conversion_file_to_float = "*1.0"

    cmd += ' --calc="('
    index=0
    for filevar in alphalist :
        cmd += filevar + conversion_file_to_float
        index += 1
        if index < len(alphalist):
            cmd += "/"
    cmd += ')"'
    if len(alphalist) > 2:
        raise Exception("Function Available between two layers")
    return cmd


def _create_cmd_outputfile(outputfile):
    """
    Create cmd "--output"
    :param outputfile: path of the output file
    :type string
    :return: cmd command
    """
    return " --outfile=" + outputfile


def _create_cmd_alphalist(alphalist):
    """
    Create cmd "--alphalist"
    :param alphalist: List of files alias
    :type array
    :return: cmd command
    """
    return ' --alphalist "' + str(alphalist) + '"'


def _process_layers(cmd):
    """
    Process the cmd command
    :param cmd:
    :return: True if the layer has bee processes
    """
    # using the base_script_gdal_calculations + cmd
    cmd = base_script_gdal_calculations + cmd
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    log.info(output)
    if error:
        log.error(error)
        #raise Exception(error)
    return True


def calc_layers(files, outputfile, calc_type="avg", options=[], overwrite=True):
    """
    :param files: array of files or String with the path
    :type array or string: Array of files ["/path/a.tif","/path/b.tif"] or string with the path i.e. "/path/*.tif"
    :param outputfile: path of the output file
    :type: string
    :param calc_type: i.e. "avg", "sum", "diff", "ratio"
    :return: True if the layer has been processed
    """
    cmd = ""

    if overwrite:
        cmd += " --overwrite "

    alphalist = []
    if isinstance(files, basestring):
        cmd += _create_cmd_filelist_from_path(files, alphalist)
    elif isinstance(files, (list, tuple)):
        cmd += _create_cmd_filelist_from_array(files, alphalist)

    # output file
    cmd += _create_cmd_outputfile(outputfile)

    # calc
    if calc_type.lower() == "avg":
        cmd += _create_cmd_calc_avg(alphalist)
    elif calc_type.lower() == "sum":
        cmd += _create_cmd_calc_sum(alphalist)
    elif calc_type.lower() == "diff":
        cmd += _create_cmd_calc_diff(alphalist)
    elif calc_type.lower() == "ratio":
        cmd += _create_cmd_calc_ratio(alphalist)
    elif calc_type.lower() == "mult":
        cmd += _create_cmd_calc_mult(alphalist)
    else:
        log.warn("TODO: custom calc")

    # alphalist
    cmd += _create_cmd_alphalist(alphalist)

    # add options
    for option in options:
        cmd += " " + option + " "

    # process layers
    return _process_layers(cmd)


