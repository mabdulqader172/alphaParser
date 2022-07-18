import os
import shutil
import subprocess


class PSEBuilder:
    """
    Class object the produces a PyMOL pse file for user analysis.

    Attributes
    ----------
    _dir : str
        Path to directory where pdb data is located.
    _fname : str
        Name of pse file that will contain the `best_model` object.
    _spec : dict
        Dictionary of spectrum color options that can be passed to PyMOL
    _script : str
        Contains the PyMOL commands to produce the desired pse file environment.
    _status : bool
        If `True` the pse file was successfully written. if any issue had occurred,
        `_status` will be set to `False`
    _make_pse : func
        Private `PSEBuilder` function the writes the PyMOL pse file. Function returns
        a boolean to `_status` attribute.
    get_status : func
        Public `PSEBuilder` function that returns the `_status` attribute.

    """
    def __init__(self, dir, path_str, spec='ygb'):
        """
        Parameters
        ----------
        dir : str
            The directory to find `best_model.pdb`.
        path_str : str
            The filename with the relative path for the output pse file.
        spec : {'ygb', 'rg', 'mwc'}, default: 'ygb'
            Controls the color gradient for the pse file given the pdb pLDDT
            (b-factor) data. Each option is defined below

            - 'ygb' or *yellow_green_blue* in PyMOL where yellow is the least
                accurate and blue is the more accurate region.
            - 'ryg' or *red_yellow_green* in PyMOL where red is the least
                accurate and green is more accurate.
            - 'mwc' or *magenta_white_cyan* in PyMOL where magenta is the least
                accurate and cyan is the most accurate.

        """
        self._dir = dir
        self._fname = f'{path_str}_pLDDT.pse'
        self._spec = {
            'ygb': 'yellow_green_blue',
            'rg': 'red_yellow_green',
            'mwc': 'magenta_white_cyan'
        }
        self._script = f'''
            pymol -cq {self._dir}/best_model.pdb -d "spectrum b, {self._spec[spec]}; save {self._fname}"
        '''
        # https://pymolwiki.org/index.php/Spectrum for spectrum command help

        # if PyMOL exists, make the PSE file
        self._status = self._make_pse()

    def _make_pse(self):
        """
        Private `PSEBuilder` function the writes the PyMOL pse file. Function returns
        a boolean to `_status` attribute.

        Parameters
        ----------
        None

        Returns
        -------
        status : bool
            If a pse file was written, `status` will be `True`, else `False`.

        """
        # check if pymol installed and best model pdb exists
        if not shutil.which('pymol'):
            raise Exception('alphaParser Error: PyMOL not installed or not in PATH.')
        if not os.path.isfile(f'{self._dir}/best_model.pdb'):
            print('No PSE file was written. Please make sure the pdb file "best_model.pdb" was not renamed.')
            return False

        # once verified run pymol
        pse_run = subprocess.run(
            args=self._script.split()[:4] + self._script.split('"')[1:-1],
            capture_output=True,
            text=True
        )

        # Check if file exits and subprocess run was successful
        if os.path.isfile(self._fname) and pse_run.returncode == 0:
            _file = os.path.split(self._fname)
            _path = 'the current directory' if _file[:-1] == ('.',) else f"{'/'.join(_file[:-1])}"
            print(f'Wrote "{_file[-1]}" in {_path}')
            return True
        else:
            print('No PSE file was written. Please make sure the pdb file "best_model.pdb" was not renamed.')
            return False

    def get_status(self):
        """
        Public `PSEBuilder` function that returns the `_status` attribute.

        Parameters
        ----------
        None

        Returns
        -------
        status : bool
            If a pse file was written, `status` will be `True`, else `False`.

        """
        return self._status
