#!/usr/bin/env python

from PDBTools import pdblib

# Design decisions:
# Checks for syntactical validity of chain IDs, dimensions and filenames are performed in this file as well
# This means that there are repeated checks in this file and in the module functions themselves - this was done
# so that we could keep asking for user input until a valid input was checked here, but the functions in
# the module would also not throw errors if used outside of this program.

# If the inputs are not valid, the user will continue to be prompted to give a valid input - there is no way to 
# go back to main menu other than giving a syntactially valid input. They would have to quit the program if
# unable to give valid input, which can happen at any point in the program.

# Users can use quit at any point, and q or Q for any inputs other than chain IDs to exit the program, as a chain
# ID of q or Q could be a valid input.

# If an input is syntactically correct, (e.g. chain ID of X), but does not exist in the file, it will 
# print that it could not be found in the file, but return the user to the main menu. Because there is no
# back input to go to main menu, I made it so that the user would not get stuck trying to give input that they 
# cannot decipher even using the hints.

# I did not force the user to choose a PDB Id first, as option 5 allows for any file to be read even if a
# file is not downloaded yet. So I decided to give the user all the options before getting them to choose
# option 1 or 5. However, it does not allow for any other options to happen until option 1 has been chosen
# and a file is downloaded.

# Other than at the start of runtime, the main menu will not be shown automatically. THe user has to press enter
# to see the menu. This is to make sure that any output printed to standard output is not obscured by the new
# printing of the menu every time you get back to the main menu.


def printed_menu(curr_id):
    print("\nThe functionalities of this program are listed below (enter the number or letter to choose):\n\
    1 - Provide a PDB ID to get contents of the local PDB file or download the PDB file from NSCB\n\
    2 - Print details from a downloaded PDB file\n\
    3 - Print protein residues for a given chain ID from a downloaded PDB file\n\
    4 - Write protein residues of one or more chains from a PDB file in FASTA file format\n\
    5 - Print/write residue lines from or to a file\n\
    6 - Alter a chain ID of the downloaded PDB file\n\
    7 - Print any non-standard protein residues from a downloaded PDB file\n\
    8 - Plot the temperature factor of a protein for a chain from a downloaded PDB file\n\
    Q, q or quit - Quit the program \n")
    if curr_id == "":
        print("No PDB file has been read in yet. Please open or download a file using option 1.\n")
    else:
        print("The current PDB file you are working on has ID:", curr_id, "\n")

def printed_detail_options():
    print("\n Please choose all options you wish to see, separated by commas:\n\
    1 - Header\n\
    2 - Title\n\
    3 - Source details\n\
    4 - Keywords\n\
    5 - Authors\n\
    6 - Resolution\n\
    7 - Journal Title\n")

def get_valid_input(prompt_message, check_function, list_quit):
    """Will prompt user for input until a valid string is given"""
    # Get intial input
    user_input = input(prompt_message)
    # While not syntactically valid or not given input to quit, keep asking for valid input
    while (user_input not in list_quit) and (not check_function(user_input)):
        user_input = input(prompt_message)
    # Return valid input or quit input
    return user_input

# Variable to hold lines of PDB file
pdb_lines = []
# Variable that keeps track of the current PDB filename/ID
curr_id = ""
# Strings that will cause the program to quit
quit_list = ["q", "Q", "quit"]
# Strings causing program to quit for chain ID input
chain_quit = ["quit"]

print("Welcome! This program makes use of the PDBTools package.")
# Initially print the menu
printed_menu(curr_id)
while True:
    # Receive user input
    option = input("Choose from the main options (press Enter to see list of main options): ")
    # If user has asked to quit, break out of while loop
    if option in quit_list:
        break
        
    # If user does not provide any input, then print the menu
    elif option == "":
        printed_menu(curr_id)
        
    # If user wishes to get the file contents
    elif option == "1":
        # Ask for a PDB ID to access the file
        pdb_id = input("Please provide a PDB ID: ")
        # If user provides string to quit, break out of while loop
        if pdb_id in quit_list:
            break
        # Try to get file contents using provided input (returns empty list if PDB ID could not be found)
        else:
            (pdb_lines, curr_id) = pdblib.download_pdb(pdb_id)

    # If user wishes to read/write residue lines
    elif option == "5":
        # Get the filename
        filename = get_valid_input("Please specify the name of the file to read/write from (e.g. 1HIV): ", pdblib.is_valid_filename, quit_list)
        # If given input to quit, quit the program
        if filename in quit_list:
            break
        # Get whether the user will read or write to the file
        open_type = input("Please specify if you want to read (r) or write (any other input) to this file: ")
        # Quit if input given is a a valid quitting string
        if open_type in quit_list:
            break
        # If we have been asked to write to a file, but no PDB file has been downloaded yet, go back to menu
        if (open_type.lower() != "r") and (pdb_lines == []):
            print("You cannot write to this file as no PDB file has been downloaded yet. Please download the PDB file first (option 1).")
        else:
            # Get the chain ID
            chain_id = get_valid_input("Please give the chain ID to search for: ", pdblib.is_valid_chain, chain_quit)
            if chain_id in chain_quit:
                break
            # Get the type of record to print/write
            record_type = input("Please specify the record type - ATOM (protein residue) or HETATM (non-protein residue).\nWrite anything else if both should be included in the file: ")
            if record_type in quit_list:
                break
            pdblib.get_chain_residues(chain_id, record_type, filename, open_type, pdb_lines)
            
    # If no PDB file contents have been downloaded yet, go back to main menu
    elif (pdb_lines == []):
        print("No PDB file has been downloaded and read yet. Please download the PDB file first (option 1).")

    # If user wishes to see PDB file details
    elif option == "2":
        # Show all details that can be printed for a PDB file
        printed_detail_options()
        # Dictionary holding each option and corresponding line pattern for detail
        detail_dict = {"1":"HEADER", "2":"TITLE", "3":"SOURCE", "4":"KEYWDS", "5":"AUTHOR", "6":"REMARK   2 RESOLUTION.", "7":"JRNL        TITL"}
        # Get comma separated options from user
        detail_options = input("Please give a list of options:")
        options_list = detail_options.split(",")
        user_details = {}
        # Add each option to a dictionary with the line pattern as a key, and empty string as value
        quit_from_program = False
        for option in options_list:
            if option in quit_list:
                quit_from_program = True
                break
            elif option in detail_dict.keys():
                detail = detail_dict[option]
                user_details[detail] = ""
            # If invalid option is given, print to user that invalid
            else:
                print("Option {0} could not be found".format(option))
        if quit_from_program:
            break
        # Print the details if they can be found in the file
        pdblib.print_details(user_details, pdb_lines)
        
    # If user wishes to get protein residues for a chain
    elif option == "3":
        # Get the chain ID from the user
        chain_id = get_valid_input("Please provide the chain ID: ", pdblib.is_valid_chain, chain_quit)
        # If asked to quit, then quit the program
        if chain_id in chain_quit:
            break
        # Find the chain
        else:
            pdblib.print_prot_residues(chain_id, pdb_lines)

    # If user wishes to write protein residues to FASTA file
    elif option == "4":
        # Get the output filename
        output_filename = get_valid_input("Please give the name of the FASTA file you wish to write the protein residues to (e.g. protein_resA): ", pdblib.is_valid_filename, quit_list)
        if output_filename in quit_list:
            break
        # Get the chain ID (if empty string is returned, want all of them)
        chain_id = input("Please provide the chain ID you wish to search for (Enter if all should be included): ")
        while (chain_id != "") and (not pdblib.is_valid_chain(chain_id)) and (chain_id not in chain_quit):
            chain_id = input("Please provide the chain ID you wish to search for (Enter if all should be included): ")
        if chain_id in chain_quit:
            break
        # Call function to write protein residues to FASTA file
        pdblib.get_fasta_protseqs(output_filename, chain_id, pdb_lines)

    # If user wishes to alter a chain ID of a PDB file
    elif option == "6":
        # Get the chain ID to alter
        old_chain_id = get_valid_input("Please give the name of the chain ID to alter: ", pdblib.is_valid_chain, chain_quit)
        if old_chain_id in chain_quit:
            break
        # Get the new chain ID that will be replacing old chain ID
        new_chain_id = get_valid_input("Please give the chain ID that will be replacing the old chain ID (one alphabetical character): ", pdblib.is_valid_chain, chain_quit)
        if new_chain_id in chain_quit:
            break
        # Alter the chain ID
        (pdb_lines, curr_id) = pdblib.alter_chain_id(old_chain_id, new_chain_id, pdb_lines, curr_id)

    # If the user wishes to see if there are any non_standard protein residues
    elif option == "7":
        pdblib.print_nonstandard_residues(pdb_lines)

    # If the user wants to plot temperature factor for a chain ID
    elif option == "8":
        # Get a chain ID
        chain_id = get_valid_input("Please give the chain ID of the protein: ", pdblib.is_valid_chain, chain_quit)
        if chain_id in chain_quit:
            break
        # Get a height value 
        height = get_valid_input("Please give the height of the plot in inches: ", pdblib.is_valid_dimension, quit_list)
        if height in quit_list:
            break
        # Get a width value
        width = get_valid_input("Please give the width of the plot in inches: ", pdblib.is_valid_dimension, quit_list)
        if width in quit_list:
            break
        # Get a valid filename
        filename = get_valid_input("Please give the name of the file to save the plot as (e.g. 1HIV_A_tempfact): ", pdblib.is_valid_filename, quit_list)
        if filename in quit_list:
            break
        # Plot the temperature factor and save to the given filename
        pdblib.plot_temp_factor(chain_id, height, width, filename, pdb_lines, curr_id)

    # User provided option that does not currently exist
    else:
        print("The option number you provided could not be determined. Please choose one of the given numbers/strings from the menu.")

print("You have quit the program.")
    