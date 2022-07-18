import os
import tempfile
from zipfile import ZipFile


def check_args(results, outfile):
    """
    Checks and handles input arguments from commandline.

    Parameters
    ----------
    results : str
       The path to zip or directory where the Alpha Fold data is stored.
    outfile : str, optional, default: "."
       Path where the user wishes to store the '.pse' and '.png' files.

    Returns
    ----------
    _dir : str
        Path to the directory where the Alpha Fold contents are stored, if
        input path is a `.zip` file; then `_dir` is a path to a
        `tempfile.TemporaryDirectory` object.
    _path_str : str
        String containing the path (with the file name) for the resulting .pse
        and .png files
    _temp : tempfile.TemporaryDirectory or None
        If the user gave `alphaParser` a zip file, `_temp` is `TemporaryDirectory`
        object from the `tempfile` module; else `_temp` is just `None`.

    """

    # first check if we have a zip or a directory
    if results[-4:] == '.zip':
        print('Input file is a ".zip" file, extracting to a temporary directory...')
        _temp = tempfile.TemporaryDirectory()
        _dir = tempfile.tempdir
        zf = ZipFile(results, 'r')
        zf.extractall(_dir)
        _fname = results[:-4]
    elif os.path.isdir(results):
        _temp = None
        _dir = results
        _fname = results
    else:
        raise Exception('AlphaParser Error: `results` must be a directory or a zipfile.')

    # check if output path exists
    if outfile and os.path.isdir(outfile):
        _path_str = os.path.join(outfile, _fname)
    elif outfile and not os.path.isdir(outfile):
        os.mkdir(outfile)
        _path_str = os.path.join(outfile, _fname)
    else:
        _path_str = os.path.join('.', _fname)

    return _dir, _path_str, _temp


def clean_files(results, temp):
    """
    Checks and handles input arguments from commandline.

    Parameters
    ----------
    results : str
       The path to zip or directory where the Alpha Fold data is stored.
    temp : tempfile.TemporaryDirectory, or None object
       `TemporaryDirectory` object that contains the temporary directory that
       must be cleaned. If the user inputted a directory `temp` is a `None` object.

    Returns
    ----------
    _dir : str
        Path to the directory where the Alpha Fold contents are stored, if
        input path is a `.zip` file; then `_dir` is a path to a
        `tempfile.TemporaryDirectory` object.
    _path_str : str
        String containing the path (with the file name) for the resulting .pse
        and .png files
    _temp : tempfile.TemporaryDirectory or None
        If the user gave `alphaParser` a zip file, `_temp` is `TemporaryDirectory`
        object from the `tempfile` module; else `_temp` is just `None`.

    """

    # if a temp directory was made, clean it up
    if results[-4:] == '.zip' and temp:
        temp.cleanup()
        print('Deleted temporary directory...')
        return True

    # if the input was just a directory, nothing to clean.
    if os.path.isdir(results):
        return True

    # if you get here something went wrong (Permission Error, etc.)
    return False
