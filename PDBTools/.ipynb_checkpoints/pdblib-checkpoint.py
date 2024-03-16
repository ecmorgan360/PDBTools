import requests
import os
import matplotlib.pyplot as plt

def download_pdb(pdb_id):
    """Reads local PDB file contents, or downloads PDB file from RSCB site and saves to a file if no local copy. It returns the contents of the file as a list of lines."""
    # Create a string of the filename
    filename = pdb_id + ".pdb"
    # If the filename is found locally, open the file and read the contents
    if os.path.isfile(filename):
        # Print message to tell user that local file has been found
        print("A local file for this ID, {0}.pdb was found. The contents of this file are now being read.".format(pdb_id))
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
            return ([], "")
        # If successfully downloaded
        else:
            # Get the file contents
            contents = response.text
            # Save the file locally
            with open(filename, 'w') as fobject:
                fobject.write(contents)
            print("The PDB file has been downloaded, and saved to the file {0}.pdb".format(pdb_id))
    # Convert string to list of lines of the file
    lines = contents.split("\n")
    # Return list of lines
    return (lines, pdb_id)

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

def get_prot_residues(chain_id, lines):
    """Returns the single letter protein residues for a given chain_id of the PDB file"""
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
    return prot_res

def print_prot_residues(chain_id, lines):
    """Prints the single letter protein residues for a given chain_id of a PDB file"""
    # Check that chain ID is syntactically valid
    if is_valid_chain(chain_id):
        # Get the single letter protein residues for the chain
        prot_res = get_prot_residues(chain_id, lines)
        # If no protein residues were found, it indicates that the chain ID given does not exist in that folder
        if prot_res == "":
            print("Protein residues for a chain ID of {0} could not be found.".format(chain_id))
        # Else print protein residues
        else:
            print(prot_res)

def get_fasta_protseqs(filename, chain_id, lines):
    # If the chain ID was not given, find all chain IDs for protein residues
    if chain_id == "":
        # Empty set of chain IDs
        chain_ids = set()
        # Go through each line
        for line in lines:
            # If a protein residue line with alpha-carbon found
            if (line.startswith("ATOM")) and ("CA" in line):
                chain_id = line[21]
                # Add chain ID to the set
                chain_ids.add(chain_id)
    else:
        # Check if given chain ID is syntactically valid
        if is_valid_chain(chain_id):
            # Set of chains only contains that ID
            chain_ids = {chain_id}

    # String to hold all contents to write to file
    contents = ""
    # Go through each chain ID
    for chain_id in chain_ids:
        # Get the protein sequence
        prot_res = get_prot_residues(chain_id, lines)
        # If the protein sequence is empty, then the chain ID was not found
        if prot_res == "":
            print("Protein residues for a chain ID of {0} could not be found. Please try with a different ID.".format(chain_id))
        # Otherwise, add header and formatted protein sequence to contents
        else:
            header = ">" + " ".join((lines[0][10:-1]).split()) + ": {0}\n".format(chain_id)
            formatted_seq = format_80(prot_res)
            contents += header + formatted_seq
    # Only write to the FASTA file if any protein sequences were found
    if contents != "":
        with open(filename+".fasta", 'w') as fobject:
            fobject.write(contents)
        # Tell user then name of the file it was written to, and the chains it was written to
        print("The protein residues from chains {0} were written to the FASTA file {1}.fasta".format(chain_ids, filename))

def get_residue_lines(chain_id, starting, lines):
    """Returns a string containing all lines which start with the given strings in the starting list and contain the chain ID"""
    res_lines = ""
    for line in lines:
        for record in starting:
            if (line.startswith(record)) and (line[21] == chain_id):
                res_lines += (line + "\n")
    return res_lines
                
def get_chain_residues(chain_id, record_type, filename, read_write, pdb_lines):
    """Prints the lines matching the record type asked for from the given filename, or writes these lines to a file to the given filename for a particular chain ID"""
    # Find ATOM and HETATM if record type is anything other than ATOM or HETATM
    if (record_type != "ATOM") and (record_type != "HETATM"):
        starting = ["ATOM", "HETATM"]
    else:
        starting = [record_type]
    # If asked to read from the file
    if read_write == "r":
        (contents, pdb_id) = download_pdb(filename)
        print(get_residue_lines(chain_id, starting, contents))
    # Otherwise assume we are writing to the filename given
    else:
        # Get the lines needed
        file_contents = get_residue_lines(chain_id, starting, pdb_lines)
        # Write the lines to the file
        with open((filename+".txt"), "w") as fobject:
            fobject.write(file_contents)
        print("Your resultant lines for chain {0} are in {1}.txt".format(chain_id, filename))

def is_valid_chain(chain_id):
    """Returns True if the chain ID is syntactically correct, False otherwise"""
    valid = False
    # Must not be empty
    if chain_id == "":
        print("One or more provided chain IDs were empty. Please provide a single alphabetical character for each chain.")
    # Can only be one character long
    elif len(chain_id) > 1:
        chain_length = len(chain_id)
        print("A chain ID can only be one character long. The chain ID provided, {0}, had a length of {1}".format(chain_id, chain_length))
    # Must be an alphabetical character
    elif chain_id.isnumeric():
        print("A chain ID can only be an alphabetic character, not a numeric character.")
    else:
        valid = True
    return valid

def is_valid_dimension(dim):
    """Returns True if the dimension is syntactically correct, False otherwise"""
    valid = False
    # Must not be empty
    if dim == "":
        print("No dimension was given. Please give a numerical value.")
    # Must only contain numeric characters
    elif (not dim.isnumeric()):
        print("The dimension given can only be a numerical type. Please only use digits (integers only, not floats).")
    else:
        valid = True
    return valid

def is_valid_filename(filename):
    """Returns True if a valid name for a file without an extension, False otherwise"""
    valid = False
    # Must not be empty
    if filename == "":
        print("Filename is empty. Please provide a filename containing alphanumerical characters.")
    else:
        valid = True
    return valid

def alter_chain_id(old_chain_id, new_chain_id, lines, pdb_id):
    """Alters the old chain ID to a new chain ID for all residues in the PDB file, saving the changed contents to a file"""
    # If both chain IDs are syntactically valid
    if (is_valid_chain(old_chain_id)) and (is_valid_chain(new_chain_id)):
        # Check if old chain ID is actually in the PDB file for any residues
        found_old_id = False
        for line in lines:
            if (line.startswith("ATOM") and (line[21] == old_chain_id)) or (line.startswith("HETATM") and (line[21] == old_chain_id)):
                found_old_id = True
                break
        # If the old chain ID is there
        if found_old_id:
            new_lines = []
            altered_text = ""
            # Iterate through each line
            for line in lines:
                # If a protein residue or non-protein residue line, and the old chain ID matches
                if (line.startswith("ATOM") and (line[21] == old_chain_id)) or (line.startswith("HETATM") and (line[21] == old_chain_id)):
                    # Replace old chain ID with new chain ID
                    new_line = (line[:21] + new_chain_id + line[22:])
                    altered_text += new_line + "\n"
                    new_lines.append(new_line)
                # If not a residue line, then just add the line with no changes
                else:
                    altered_text += (line) + "\n"
                    new_lines.append(line)
            # Get the name of the file from the header
            filename = pdb_id + "_" + new_chain_id + ".pdb"
            # Write the altered text to the file named according to the header
            with open(filename, 'w') as fobject:
                fobject.write(altered_text)
            print("The chain ID {0} has been altered to {1} for all residue lines, saved to file {2}. File {2} is now the PDB file being used".format(old_chain_id, new_chain_id, filename))
            # Update the list of lines in main program to also be altered
            return (new_lines, filename)
        # If old chain ID was not found, tell user to choose another ID that exists
        else:
            print("The old chain ID {0} does not exist in this file. Please give a different chain ID.".format(old_chain_id))
    # Return original contents if never altered
    return (lines, pdb_id)


def print_nonstandard_residues(lines):
    """Prints any non-standard protein residues given the contents of the PDB file"""
    # List of three-letter codes for all standard protein residues
    codes = ["ALA", "ASX", "CYS", "ASP", "GLU", "PHE", "GLY", "HIS", "ILE", "LYS", "LEU", "MET", "ASN", "PRO", 
             "GLN", "ARG", "SER", "THR", "SEC", "VAL", "TRP", "XAA", "TYR", "GLX"]
    non_standards = ""
    curr_chain = ""
    counter = 0
    for line in lines:
        # If we have reached a new chain, reset counter to 0 and keep track of next chain
        if line.startswith("ATOM") and (line[21] != curr_chain):
            curr_chain = line[21]
            counter = 0
        # If we have not looked at a protein residue yet
        if line.startswith("ATOM") and (counter < int(line[23:26])):
            # Increase the counter to find the next protein residue
            counter = int(line[23:26])
            # Find the current code
            res_code = line[17:20]
            # Add code if not in list of standard protein residues
            if res_code not in codes:
                non_standards += res_code
    # If no non-standard codes found, print that all were standard
    if non_standards == "":
        print("All protein residues were standard.")
    # Print any non-stnadard codes
    else:
        print(non_standards)

def plot_temp_factor(chain_id, height, width, output_filename, lines):
    """Plots the temperature factor for all atoms of the protein chain, writing to an output file a plot of given height and width"""
    if is_valid_dimension(height) and is_valid_dimension(width):
        height = int(height)
        width = int(width)
        # Get all atom numbers in one list, and temperature factors in a second one
        atom_nums = []
        temp_factors = []
        for line in lines:
            # Get each line detailing an atom of a protein residue
            if line.startswith("ATOM"):
                atom_num = int(line[4:11])
                temp_factor = float(line[61:66])
                atom_nums.append(atom_num)
                temp_factors.append(int(temp_factor))
        # Plotting line graph of size height by width
        fig = plt.figure(figsize=(height, width))
        # X axis is atom numbers, y axis is temperature factor
        plt.plot(atom_nums, temp_factors)
        # Label x and y axes
        plt.xlabel("Atom number")
        plt.ylabel("Temperature factor")
        plt.savefig(output_filename)

