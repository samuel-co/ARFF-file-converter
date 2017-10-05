'''
Sam Congdon, Kendall Dilorenzo, Michael Hewitt
CSCI 447: Machine Learning
Project 1: Data Converter File
September 18, 2017

This python module handles the File class. The __inti__ method creates
the object with user input. Other helper methods allow for the conversion of any 
input files into .arff files for use with WEKA. Note that if the class is not in the 
last column of data (as assumed by WEKA) this program does not move it there. WEKA has
built in functionality to manually select the class column, so programming the that 
functionality would have been a waste. 
'''

import os
import re


class File:
    def __init__(self, name):
        ''' Method to initialize File object and set relevant variables'''

        # set variable names for in and out files, and opens said files
        self.file_in = name
        self.file_out = os.path.splitext(name)[0] + ".arff"
        self.fin = open(self.file_in, 'r')
        self.fout = open(self.file_out, 'w')

        # gets user input for the data's class and attribute names
        print("\n----For " + self.file_in + " please supply the following info----")
        self.class_column = int(input("Enter the column number of the class (starting at 0): "))
        self.attribute_list = input("Enter the names of the attributes, separated by commas: ")
        self.attribute_list = self.attribute_list.replace(' ', '').split(',')
        self.data = ''

    def get_names(self):
        ''' Returns the names of the in and out files the object utilizes'''

        return (self.file_in, self.file_out)

    def get_column_values(self, column, name):
        '''determine all possible values a column of data holds in order to determine
            a nominal data type'''

        value_list = {}     # Dictionary to hold all the classes present in the data

        # checks the value contained in column in each line, adding new values to the dict
        for line in self.data.split('\n'):
            line = line.split(',')
            if len(line) > 1: value_list.update({line[column]: 1})

        # formats the output line using all the keys input into the dict (representing all possible values)
        value_string = '{'
        for key in value_list.keys():
            value_string += key + ','
        return ("@ATTRIBUTE {} {}".format(name, value_string[0:-1]) + "}\n")

    def process_file(self):
        ''' Translates files data into csv format, then creates file header and ouputs the new
            file to file_out'''

        for line in self.fin:
            line = re.sub("\s+", ',', line.strip()) # strips all white space, adding commas to separate values
            self.data += line + '\n'                # adds the converted line to the data string

        # Header of the arff file, defines the relation
        self.fout.write("@RELATION " + os.path.splitext(self.file_in)[0] + '\n\n')
        global column_list
        # iterates over the user input attributes, outputting them to the arff file in order, with the attribute type
        for i in range(len(self.attribute_list)):
            if i == self.class_column: self.fout.write(self.get_column_values(self.class_column, "class"))

            # checks if the attribute is of type REAL
            try:
                column_list = self.get_column_values(i, self.attribute_list[i])    # retrieves all values in the column
                column_data = column_list[13+len(self.attribute_list[i]):-2]
                column_data = column_data.split(',')       # parses string down to be an array of values
                for data in column_data:                   # tests that every instance of the data is a number
                    float(data)

                # if every peice of data is a number the attribute is of type REAL
                self.fout.write("@ATTRIBUTE " + self.attribute_list[i] + " REAL\n")

            # if not of type real ask user if of type NOMINAL
            except ValueError:
                att_type = input("Is ATTRIBUTE {} of type NOMINAL? (y or n): ".format(self.attribute_list[i]))

                # if NOMINAL retrieves all possible values of a column present in the data
                if att_type.strip() == 'y':
                    #self.fout.write(self.get_column_values(i, self.attribute_list[i]))
                    self.fout.write(column_list)

                # else asks the user for the ATTRIBUTE TYPE
                else:
                    att_type = input("Enter the type for ATTRIBUTE {}".format(self.attribute_list[i])).strip()
                    self.fout.write("@ATTRIBUTE {} {}\n".format(self.attribute_list[i], att_type))

        # if the class_string was not output in the for loop,write it last
        if len(self.attribute_list) == self.class_column: self.fout.write(self.get_column_values(self.class_column, "class"))

        # lastly output the previously converted data from the input file
        self.fout.write("\n@DATA\n" + self.data)

        # close the files
        self.fin.close()
        self.fout.close()

