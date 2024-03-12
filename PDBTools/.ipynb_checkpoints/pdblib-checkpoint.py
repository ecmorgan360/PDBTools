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

def format_80(contents):
    formatted = ""
    for char_idx in range(len(contents)):
        if ((char_idx % 80) == 0) and (char_idx != 0):
            formatted += "\n" + contents[char_idx]
        else:
            formatted += contents[char_idx]
    return formatted

def print_details(details, lines):
    """Prints each given detail from the list of details, each detail on a separate line. If the detail is longer than 80 characters, wrapping to the next line is performed."""
    # Iterate through each line
    for line in lines:
        for starting_str in details.keys():
            if line.startswith(starting_str):
                if starting_str == "JRNL        TITL":
                    details[starting_str] += line[17:-1]
                else:
                    details[starting_str] += line[10:-1]
    for key, value in details.items():
        if value == "":
            print("There is no {0} in this PDB file.".format(key))
        else:
            formatted = format_80((" ".join(value.split())))
            print(formatted)
    
