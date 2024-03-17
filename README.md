# PDBTools Package 

## Written by ecmorgan360

### What is it for?
The PDBTools Package can be used to download and read a PDB file, and query its contents. The pdblib module functionalities include:
1. Reading a local PDB file, or downloading and reading a PDB file from NSCB 
2. Print details from a PDB file
3. Print protein residues for a chain ID in the PDB file
4. Write protein residues to a FASTA file for one or more chain IDs in the PDB file
5. Print residue lines from a PDB file, or write residue lines to a text file
6. Alter a chain ID of a PDB file
7. Print any non-standard protein residues in a PDB file
8. Plot the temperature factor of a protein residue chain in the PDB file

### How do you create a Conda environment to run PDBTools?
First, you will need to make a new Conda environment that uses Python 3.11 - this example environment will be named py311.

The following is first run:

`conda create -n py311 -c conda-forge python=3.11`

Make sure to answer yes (y) when asked if you wish to proceed.

Next, the envirnoment must be activated by running:

`conda activate py311`

Then, the requests and matplotlib modules must be installed, using the following:

`conda install requests`

`conda install matplotlib`

Make sure to answer yes (y) when asked if you wish to proceed.

The environment should now be ready to use. If deactivated, you can always reactivate using `conda activate py311`.

### How do you retrieve the PDBTools repository from GitHub?
First, move to the local folder that you wish to download the PDBTools repository inside.

Then, you will retrieve the repository by running the following:

`git clone https://github.com/ecmorgan360/PDBTools.git`

This should create a folder inside your current folder called PDBTools. You can now move into this PDBTools folder.

### How do you run checkPDB.py?
Make sure you have changed directories so you are in the main PDBTools repository cloned from GitHub (you should see checkPDB.py if you run the `ls` command).

Once you are in this directory, make sure that checkPDB.py is executable, by running the following:

`chmod +x checkPDB.py`

Then, you should be able to start running checkPDB.py by executing the following:

`./checkPDB.py`

