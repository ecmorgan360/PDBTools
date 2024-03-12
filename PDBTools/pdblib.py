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
    """Converts a string to a formatted string with 80 characters on each line"""
    formatted = ""
    # Iterates through each index corresponding to a character in the string
    for char_idx in range(len(contents)):
        # If the end of the line is reached, add newline character and current character on new line
        if ((char_idx % 80) == 0) and (char_idx != 0):
            formatted += "\n" + contents[char_idx]
        # Else add character to the line
        else:
            formatted += contents[char_idx]
    return formatted

def print_details(details, lines):
    """Prints each given detail from the list of details, each detail on a separate line. If the detail is longer than 80 characters, wrapping to the next line is performed."""
    # Iterate through each line
    for line in lines:
        # Iterate through each key in the dictionary
        for starting_str in details.keys():
            # If the key matches the start of the line
            if line.startswith(starting_str):
                # Get contents of the line (journal title contetns starts at a different index to the others), add to string for that key
                if starting_str == "JRNL        TITL":
                    details[starting_str] += line[17:-1]
                else:
                    details[starting_str] += line[10:-1]
    # Iterate through each item in the dictionary
    for key, value in details.items():
        # If the line was never found, print that could not find it
        if value == "":
            print("There is no {0} in this PDB file.".format(key))
        # Else, print the formatted string contents
        else:
            formatted = format_80((" ".join(value.split())))
            print(formatted)

def print_prot_residues(chain_id, lines):
    """Prints the single letter protein residues for a given chain_id and PDB file lines"""
    # Dictionary with three-letter amino acid residues as keys, and one-letter aas as values
    codes = {"ALA":"A", "ASX":"B", "CYS":"C", "ASP":"D", "GLU":"E", "PHE":"F", "GLY":"G", "HIS":"H", "ILE":"I", "LYS":"K", "LEU":"L", "MET":"M", "ASN":"N", "PRO":"P", 
             "GLN":"Q", "ARG":"R", "SER":"S", "THR":"T", "SEC":"U", "VAL":"V", "TRP":"W", "XAA":"X", "TYR":"Y", "GLX":"Z"}
    prot_res = ""
    # Iterate through each line in the pdb file
    for line in lines:
        # Check that it is a line for a protein residue, carbon atom to not repeat the same residue, and find the correct chain
        if (line.startswith("ATOM")) and ("CA" in line) and (line[21] == chain_id):
            # Splice the three-letter amino acid code from the line
            aa_three_code = line[17:20]
            # Convert to 1-letter code using the dictionary codes, then add the code to the string of residues
            prot_res += codes[aa_three_code]
    # If no protein residues were found, it indicates that the chain ID given does not exist
    if prot_res == "":
        print("Protein residues for a chain ID of {0} could not be found.".format(chain_id))
    # Else print protein residues
    else:
        print(prot_res)








