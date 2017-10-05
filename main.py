'''
Sam Congdon, Kendall Dilorenzo, Michel Hewitt
CSCI 447: MachineLearning
Project 1: Data Converter Main
September 18, 2017

This python module handles the creation of the list of files to be converted,
as well as initializes the conversion of each file while keeping the user 
updated with command line statements. 
'''

import file


def main():
    # parses user input for file names
    file_list = input("Enter the names of files to be converted, separated by commas: ")
    file_list = file_list.replace(' ', '').split(',')

    # creates a File object for each file specified by the user
    for i in range(len(file_list)):
        new_file = file.File(file_list[i])
        file_list[i] = new_file

    # processes each file, printing progress as it goes
    for current_file in file_list:
        file_names = current_file.get_names()
        print("\nCurrently converting {} into {} ...".format(file_names[0], file_names[1]))
        current_file.process_file()
        print("Conversion complete.")

if __name__ == "__main__":
    main()
