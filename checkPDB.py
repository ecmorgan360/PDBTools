#!/usr/bin/env python

from PDBTools import pdblib

def printed_menu(curr_id):
    if curr_id == "":
        print("\nNo PDB file has been read in yet. Please open or download a file using option 1.")
    else:
        print("\nThe current PDB file you are working on has ID:", curr_id)
    print("\nPlease choose a functionality from the following (enter the number or letter):\n\
    1 - Get contents of PDB file locally or download PDB file from NSCB given a PDB ID\n\
    2 - Print details from a downloaded PDB file\n\
    3 - Print protein residues for a given chain ID from a downloaded PDB file\n\
    4 - Write protein residues of one or more chains from a PDB file in FASTA file format\n\
    5 - Print ATOM/HETATM lines for a chain ID of a downloaded PDB file\n\
    6 - Alter a chain ID of the downloaded PDB file\n\
    7 - Print any non-standard protein residues from a downloaded PDB file\n\
    8 - Plot the temperature factor of a protein for a chain\n\
    Q, q or quit - Quit the program \n")

def printed_detail_options():
    print("\n Please choose all options you wish to see, separated by commas:\n\
    1 - Header\n\
    2 - Title\n\
    3 - Source details\n\
    4 - Keywords\n\
    5 - Authors\n\
    6 - Resolution\n\
    7 - Journal Title\n")

# Variable to hold lines of PDB file
pdb_lines = []
curr_id = ""
# Strings that will cause the program to quit
quit_list = ["q", "Q", "quit"]

# Initially print the menu
printed_menu(curr_id)
while True:
    # Print all main functionality options
    
    # Receive user input
    option = input("Choose an option: ")
    # If user has asked to quit, break out of while loop
    if option in quit_list:
        break
        
    # If user does not provide any input, then print the menu
    elif option == "":
        printed_menu(curr_id)
        
    # If user wishes to get the file contents
    elif option == "1":
        # Ask for a PDB ID to access the file
        pdb_id = input("Please provide a PDB ID (case sensitive): ")
        # If user provides string to quit, break out of while loop
        if pdb_id in quit_list:
            break
        # Try to get file contents using provided input (returns empty list if PDB ID could not be found)
        else:
            (pdb_lines, curr_id) = pdblib.download_pdb(pdb_id)
            
    elif option == "5":
        # Get the filename
        filename = input("Please specify the name of the file to read/write from (e.g. 1HIV): ")
        # If given input to quit, quit the program
        if filename in quit_list:
            break
        # Get whether the user will read or write to the file
        open_type = input("Please specify if you want to read (r) or write (w) to this file: ")
        # Quit if input given is a a valid quitting string
        if open_type in quit_list:
            break
        # If we have been asked to write to a file, but no PDB file has been downloaded yet, go back to menu
        if (open_type != "r") and (pdb_lines == []):
            print("You cannot write to this file as no PDB file has been downloaded yet. Please download the PDB file first (option 1).")
        else:
            # Get the chain ID
            chain_id = input("Please give the chain ID to search for: ")
            if chain_id in quit_list:
                break
            # Get the type of record to print/write
            record_type = input("Please specify the record type of ATOM or HETATM (Enter if both should be included in the file): ")
            if record_type in quit_list:
                break
            pdblib.get_chain_residues(chain_id, record_type, filename, open_type, pdb_lines)
            
    # If no PDB file contents have been downloaded yet, go back to main menu
    elif (pdb_lines == []):
        print("No PDB file has been downloaded and read yet. Please download first.")
        
    elif option == "2":
        # Show all details that can be printed for a PDB file
        printed_detail_options()
        # Dictionary holding each option and corresponding line pattern for detail
        detail_dict = {"1":"HEADER", "2":"TITLE", "3":"SOURCE", "4":"KEYWDS", "5":"AUTHOR", "6":"REMARK   2 RESOLUTION.", "7":"JRNL        TITL"}
        # Get comma separated options from user
        detail_options = input("Please give a list of options:")
        options_list = detail_options.split(",")
        user_details = {}
        if detail_dict.keys() in quit_list:
            break
        # Add each option to a dictionary with the line pattern as a key, and empty string as value
        for option in options_list:
            if option in detail_dict.keys():
                detail = detail_dict[option]
                user_details[detail] = ""
            # If invalid option is given, print to user that invalid
            else:
                print("Option {0} could not be found".format(option))
        # Print the details if they can be found in the file
        pdblib.print_details(user_details, pdb_lines)
        
    # 
    elif option == "3":
        # Get the chain ID from the user
        chain_id = input("Please provide the chain ID:")
        # If asked to quit, then quit the program
        if chain_id in quit_list:
            break
        # Find the chain
        else:
            pdblib.print_prot_residues(chain_id, pdb_lines)
            
    elif option == "4":
        # Get the output filename
        output_filename = input("Please give the name of the FASTA file you wish to write the protein residues to (e.g. protein_resA): ")
        if output_filename in quit_list:
            break
        # Get the chain ID (if empty string is returned, want all of them)
        chain_id = input("Please provide the chain ID you wish to search for (Enter if all should be included): ")
        if output_filename in quit_list:
            break
        # Call function to write protein residues to FASTA file
        pdblib.get_fasta_protseqs(output_filename, chain_id, pdb_lines)
        
    elif option == "6":
        # Get the chain ID to alter
        old_chain_id = input("Please give the name of the chain ID to alter: ")
        if old_chain_id in quit_list:
            break
        # Get the new chain ID that will be replacing old
        new_chain_id = input("Please give the chain ID that will be replacing the old chain ID (one alphabetical character): ")
        if new_chain_id in quit_list:
            break
        # Alter the chain ID
        pdblib.alter_chain_id(old_chain_id, new_chain_id, pdb_lines)
        
    elif option == "7":
        pdblib.print_nonstandard_residues(pdb_lines)
        
    elif option == "8":
        chain_id = input("Please give the chain ID of the protein: ")
        if chain_id in quit_list:
            break
        height = input("Please give the height of the plot in inches: ")
        if height in quit_list:
            break
        width = input("Please give the width of the plot in inches: ")
        if width in quit_list:
            break
        filename = input("Please give full name of the file to save the plot as: ")
        if filename in quit_list:
            break
        pdblib.plot_temp_factor(chain_id, height, width, filename, pdb_lines)
    else:
        print("The option number you provided could not be determined. Please choose one of the given numbers/strings from the menu.")

print("You have quit the program.")
    