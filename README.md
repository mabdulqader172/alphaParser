# alphaParser
`alphaParser` is a python software that parses AlphaFold/ColabFold results into a PyMOL `.pse` file of the best predicted model 
and a `.png` visualization of the Predicted Alignment Error matrix. More details relative to the `.pse` and `.png` files
will be explained below.

## Installing alphaParser

Requirements for alphaParser are listed below:
```bash
setuptools~=61.2.0
numpy~=1.21.5
matplotlib~=3.5.1
seaborn~=0.11.2
pymol-open-source~=2.5.0
```


### Linux and macOS Installation
Using `git` or `wget` you can download `alphaParser` via
```bash
git clone https://github.com/mabdulqader172/alphaParser.git
```
or
```bash
wget https://github.com/mabdulqader172/alphaParser.git
```

Once downloaded, move the dot `.pyz` program to your `bin`

```bash
mv alphaParser/alphaParser.pyz /usr/local/bin
```

If you don't have `sudo` access simply `mv` to your local bin.

```bash
mkdir ~/bin # do this only if you don't have one yet
mv <location of the repository>/alphaParser/alphaParser.pyz ~/bin
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.profile
source ~/.profile
```

Once in your path, call `alphaParser` 
```bash
alphaParser.pyz -h
```
You should get the following help message back
```text
usage: alphaParser [-h] [-o OUTPUT] [-t TITLE] results

A python software to parse AlphaFold results into PyMOL PSE and PAE plots.

positional arguments:
  results               the `results` directory or zipfile produced from your AlphaFold prediction. Files will have same 
                        name as the zipfile/directory given. To change the output file names for the pse and png files 
                        use '-o'/'--output' metavar.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        name of the output pse and png files to use.
  -t TITLE, --title TITLE
                        The desired title for your PAE plot, remember to wrap the title in quotations. 
                        Example: "PAE Plot"
```

## Running `alphaParser`
### Creating `.pse` and `.png` Files

Create your annotated `.pse` and `.png` file by calling
```bash
alphaParser.pyz <path to your zipfile>
```
If you wish to input a directory just call
```bash
alphaParser.pyz <path to your directory>
```
Note that all the files produced will have the name of the zipfile or the directory name as a prefix.

### Adding a target directory for your output
If you wish to output your data to a specific target call the `-o` metavar.
```bash
alphaParser.pyz <path to your directory or zipfile> -o <output dir>
```

### Adding a title to your PAE plot.
The default title is `"PAE Plot"` so if you wish to add a more descriptive name, use the `-t` metavar
```bash
alphaParser.pyz <path to your directory or zipfile> -t <your descriptive title>
```

## Reaching Out/Feedback
If `alphaParser` is running into an error, or if you have any feedback on any features to add just raise an issue 
and will get back to you soon!



