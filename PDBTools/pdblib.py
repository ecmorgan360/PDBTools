import requests
import os

def download_pdb(pdb_id):
    """Reads local PDB file contents, or downloads PDB file from RSCB site if no local copy, returning the contents of the file as a list of lines"""
    # Create a string of the filename
    filename = pdb_id.upper() + ".pdb"
    # If the filename is found locally, open the file and read the contents
    if os.path.isfile(filename):
        # Print message to tell user that local file has been found
        print("A local file for this ID, {0}.pdb was found. The contents of this file are now being read.".format(pdb_id.upper()))
        with open(filename, 'r') as fobject:
            # Get all contents as a string
            contents = fobject.read()
    # If the file is not found locally, use requests to download it
    else:
        # Print message telling user that local file was not found
        print("A local file {0}.pdb was not found. Trying to download a file with PDB ID {0}.".format(pdb_id))
        response = requests.get("https://files.rcsb.org/download/" + pdb_id + ".pdb")
        # if not successful, return an empty list
        if response.status_code != 200:
            print("A file for PDB ID {0} could not be downloaded. Please check the PDB ID given.".format(pdb_id))
            return []
        # Get full contents as a string if successfully downloaded
        else:
            contents = response.text
    # Convert string to list of lines of the file
    lines = contents.split("\n")
    # Return list of lines
    return lines

# def print_details(details):
#     """Prints each given detail from the list of details, each detail on a separate line. If the detail is longer than 80 characters, wrapping to the next line is performed."""
    
