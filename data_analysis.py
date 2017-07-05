"""
    7/1/2017
    Reads thrust data file output by Arduino code for propeller project
    Intent Design Engineering
"""

import sys

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
            lines.append(line[:-1])

        return lines
    except IOError:
        print "Error in opening file " + filename + ": file not found."

def print_options():

    options = {"bar":   {"summary": "Creates a bar graph of the data.",
                       "function": create_bar_graph},
               "line":  {"summary": "Creates a line graph of the data.",
                       "function": create_line_graph},
               "table": {"summary": "Creates a table of the data.",
                         "function": create_table},
               "exit": {"summary": "Exits the program.",
                         "function": ""}
           }
    
    print "\nOptions\n" + ("-" * len("options"))
    for option in options:
        print option + "\n\t" + options[option]["summary"]       
        
def create_bar_graph(data):
    print "bar"
    
def create_line_graph(data):
    print "line"
    
def create_table(data):
    # prints headings based on received data
    headings = "\n"
    for item in data[0].replace("\t", " ").split():
        headings += item + "\t "
    print headings
    print "-" * len(headings)
    
    # print data
    for line in data[1:]:
        line = line.replace("\t", " ").split()
        for item in line:
            print item + "\t|",
        print

def main():
    raw_data = open_file()
    input_command = ""
    end = False

    if (raw_data):
        while (not end):
    
            #take input from user
            input_command = raw_input("\nEnter command: ")
            inputs = input_command.split(" ")
            
            if (inputs[0] == "help"):
                print_options()
            
            elif (inputs[0] == "bar"):
                # if no additional commands given, use all data
                if (len(inputs) == 1):
                    create_bar_graph(raw_data)
                    
            elif (inputs[0] == "line"):
                # if no additional commands given, use all data
                if (len(inputs) == 1):
                    create_line_graph(raw_data)
                    
            elif (inputs[0] == "table"):
                # if no additional commands given, use all data
                if (len(inputs) == 1):
                    create_table(raw_data)
                    
            elif (inputs[0] == "exit"):
                end = True

            else:
                print "Command not found: " + inputs[0]

if __name__=="__main__":
    main()
