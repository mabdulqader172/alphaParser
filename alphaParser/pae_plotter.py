import json
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class PAEPlotter:
    """
    Class object that produces a Predicated Alignment Error (PAE) Plot given the
    best predicted model.

    Attributes
    ----------
    _dir : str
        Path to directory where PAE JSON data is located.
    _fname : str
        Name of png file that will contain the PAE plot.
    _matrix : np.ndarray, shape=(n_residue, n_residue)
        The 2D matrix produced from the PAE JSON data. Where `n_residue` is the
        total number of amino acids in the protein.
    _make_pae_matrix : func
        Private `PAEPlotter` function that wrangles the json into a 2D matrix.
    _extract_json : func
        Private `PAEPlotter` function that parses the PAE JSON and passes the
        data to `_make_pae_matrix`.
    plot : func
        Public `PAEPlotter` function that produces the PAE plot given the `_matrix`
        attribute data. The file name is defined by the `_fname` attribute.

    """
    def __init__(self, dir, path_str):
        """
        Parameters
        ----------
        dir : str
            The path were the best model PAE json data is stored.
        path_str : str
            The relative path where the PAE plot will be written.

        """
        self._dir = f'{dir}/best_model_pae.json'
        self._fname = f'{path_str}_pae_matrix.png'
        self._matrix = self._extract_json()

    @staticmethod
    def _make_pae_matrix(r1, r2, pae):
        """
        Private `PAEPlotter` function that wrangles the json into a 2D matrix.

        Parameters
        ----------
        r1 : np.ndarray, shape=(n_residue**2,)
            The reference residue vector, where `r2` contains the residues `r1`
            is aligned to.
        r2 : np.ndarray, shape=(n_residue**2,)
            The aligned residue vector, given reference `r1`.
        pae : np.ndarray, shape=(n_residue**2,)
            The PAE value associated to each respective (`r1`, `r2`) pairing.

        Returns
        -------
        pae_matrix : np.ndarray, shape=(n_residue, n_residue)
            The 2D PAE matrix that is given to `_matrix` attribute.

        """

        # ensure json has no missing data
        if not r1.shape == r2.shape == pae.shape:
            raise Exception('alphaParser Error: PAE JSON contains missing data.')

        # make pae matrix
        _dim = int(np.sqrt(pae.shape[0]))
        pae_matrix = np.zeros(shape=(_dim, _dim))
        pae_matrix[r1 - 1, r2 - 1] = pae

        return pae_matrix

    def _extract_json(self):
        """
        Private `PAEPlotter` function that parses the PAE JSON and passes the
        data to `_make_pae_matrix`.

        Parameters
        ----------
        None

        Returns
        -------
        pae_matrix : np.ndarray, shape=(n_residue, n_residue)
            Returns 2D PAE matrix to `_matrix` attribute. Matrix was made via
            private function `_make_pae_matrix`.

        """

        # assert that you have the json file
        if not os.path.isfile(self._dir):
            raise Exception('AlphaParser Error: "best_model_pae.json" is missing.')

        # extract the json and make the matrix
        _json_obj = open(self._dir, 'r')
        pae_dict = json.load(_json_obj)[0]
        _json_obj.close()
        return self._make_pae_matrix(*[np.array(pae_dict[i]) for i in list(pae_dict.keys())[:-1]])

    def plot(self, title):
        """
        Public `PAEPlotter` function that produces the PAE plot given the `_matrix`
        attribute data. The file name is defined by the `_fname` attribute.

        Parameters
        ----------
        title : str or None
            If a title is given, the title of the plot will be modified. If no title
            is given, the default title 'PAE Plot' is written.

        Returns
        -------
        None

        """

        # set theme and initialize figure object
        sns.set_theme()
        fig, ax = plt.subplots(figsize=(5, 3.75))

        # plot PAE Matrix + save and close figure
        sns.heatmap(data=self._matrix, cmap='YlGnBu_r', ax=ax)
        ax.set_title(f'{title} PAE Plot' if title else 'PAE Plot')
        ax.set_xlabel('Residue 1')
        ax.set_ylabel('Residue 2')
        plt.savefig(self._fname, bbox_inches='tight', dpi=600)
        plt.close(fig)

        # Check if file exits
        if os.path.isfile(self._fname):
            _file = os.path.split(self._fname)
            _path = 'the current directory' if _file[:-1] == ('.',) else f"{'/'.join(_file[:-1])}"
            print(f'Wrote "{_file[-1]}" in {_path}')
        else:
            print('No PAE plot was drawn. Please make sure the json file "best_model_pae.json" was not renamed.')
