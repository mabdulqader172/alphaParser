import argparse
from handler import check_args, clean_files
from pse_builder import PSEBuilder
from pae_plotter import PAEPlotter


def main(results, outfile, title):
    """
    Main function for `alphaParser`

    Parameters
    ----------
    results : str
        the path to zip or directory where the Alpha Fold data is stored.
    outfile : str, optional, default: "."
        the path were the user wishes to store the '.pse' and '.png' files.
    title: str, optional, default: "PAE Plot"
        the desired title to be given for the users PAE Plot.

    Returns
    -------
    None

    """
    _dir, _path_str, _temp = check_args(results, outfile)

    # make PSE Object
    pse = PSEBuilder(_dir, _path_str)
    if not pse.get_status():
        print('No "best_model.pdb" was provided; continuing PAE (Predicted Alignment Error) Plot...')

    # make PAE plot
    pae_plotter = PAEPlotter(_dir, _path_str)
    pae_plotter.plot(title=title)

    # clean excess data
    status = clean_files(results, _temp)
    if not status:
        print('Excess data could not be deleted.')
    print('Complete.')

    return


# Make the argument parser and parse the input vars.
if __name__ == "__main__":
    p = argparse.ArgumentParser(
        prog='alphaParser', add_help=True,
        description='A python software to parse AlphaFold results into PyMOL PSE and PAE error plots.',
    )
    p.add_argument('results', help='''
        the `results` directory or zipfile produced from your AlphaFold prediction. Files will have same name 
        as the zipfile/directory given. To change the output file names for the pse and png files 
        use '-o'/'--output' metavar.
        ''')
    p.add_argument('-o', '--output', type=str, help='''
        name of the output pse and png files to use. 
        ''')
    p.add_argument('-t', '--title', type=str, help='''
        The desired title for your PAE plot, remember to wrap the title in quotations.
        Example: "PAE Plot" 
        ''')
    main(p.parse_args().results, p.parse_args().output, p.parse_args().title)
