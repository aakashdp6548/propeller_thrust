"""
    7/1/2017
    Reads thrust data file output by Arduino code for propeller project
    Intent Design Engineering
"""

from __future__ import print_function

import sys
import collections

def open_file():
    lines = []
    filename = "DATA.txt"
    
    # allows user to enter filename as command line argument
    if (len(sys.argv) > 1 and sys.argv[1]):
        filename = sys.argv[1]
    else:
        filename = raw_input("Enter the file name: ")

    # opens file as read-only, removes newline chars
    try:
        data_file = open(filename, "r")
        for line in list(data_file):
            # adds list of items in line to new list
            lines.append(line[:-1].replace("/t", " ").split())

        return lines
    except IOError:
        print("Error in opening file ", filename, ": file not found.")

def print_options():

    options = collections.OrderedDict([
        ("bar",   {"summary": "Creates a bar graph of the data.",
                   "function": create_bar_graph} ),
        ("line",  {"summary": "Creates a line graph of the data.",
                   "function": create_line_graph} ),
        ("table", {"summary": "Creates a table of the data.",
                   "function": create_table} ),
        ("exit", {"summary": "Exits the program.",
                  "function": ""} )
        ]
    )
    
    print("\nOptions\n", ("-" * len("options")))
    for option in options:
        print(option + "\n\t" + options[option]["summary"])
        
def create_bar_graph(data):
    print("bar")
    
def create_line_graph(data):
    print("line")
    
def create_table(data):
    # prints headings based on received data
    headings = "\n"
    for item in data[0]:
        headings += item + "\t "
    print(headings)
    print("-" * len(headings))
    
    # print data
    for line in data[1:]:
        for item in line:
            print(item + "\t|", end="")
        print()

def main():
    
    raw_data = open_file()
    input_command = ""
    end = False

    if (raw_data):
        while (not end):

            # reset data to be used
            data = []
    
            #take input from user
            input_command = raw_input("\nEnter command: ")
            inputs = input_command.split(" ")

            if (len(inputs) > 1):
                print ("", end="")
                data.append(raw_data[0])
                for i in range(1, len(raw_data)):
                    # if reading # matches parameter, add to data list to be analyzed
                    if (raw_data[i][0] == inputs[1]):
                        data.append(raw_data[i])
            else:
                data = raw_data
            
            if (inputs[0] == "help"):
                print_options()
            
            elif (inputs[0] == "bar"):
                create_bar_graph(data)
                    
            elif (inputs[0] == "line"):
                create_line_graph(data)
                    
            elif (inputs[0] == "table"):
                create_table(data)
                    
            elif (inputs[0] == "exit"):
                end = True

            else:
                print("Command not found: " + inputs[0])

if __name__=="__main__":
    main()
