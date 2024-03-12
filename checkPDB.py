#!/usr/bin/env python

from PDBTools import pdblib

def printed_menu():
    print("\nPlease choose a functionality from the following (enter the number or letter):\n\
    1 - Get contents of PDB file locally or download PDB file from NSCB given a PDB ID\n\
    2 - Print details from a PDB file\n\
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
# Strings that will cause the program to quit
quit_list = ["q", "Q", "quit"]
while True:
    # Print all main functionality options
    printed_menu()
    # Receive user input
    option = input("Option: ")
    # If user has asked to quit, break out of while loop
    if option in quit_list:
        break
    # If user does not provide any input, then return to menu
    if option == "":
        pass
    # If user wishes to get the file contents
    elif option == "1":
        # Ask for a PDB ID to access the file
        pdb_id = input("Please provide a PDB ID: ")
        # If user provides string to quit, break out of while loop
        if pdb_id in quit_list:
            quit_list = False
            break
        # Try to get file contents using provided input (returns empty list if PDB ID could not be found)
        else:
            pdb_lines = pdblib.download_pdb(pdb_id)
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
    # Invalid option is given
    else:
        print("The option number you provided could not be determined. Please choose one of the given numbers/strings from the menu.")

print("You have quit the program.")
    