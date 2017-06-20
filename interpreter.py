# Paul Miller 2016
# All rights reserved
 
import sys
import parser

def parse_source_code(file_path):
    source = open(file_path)
    code = source.read()
    print code
    root = parser.parse(code)
     


def main():
    argc = len(sys.argv)
    if argc == 1:  # if only script is called, use as realtime parsing interpter
        command = raw_input('>')
        lines = []
        while command != 'quit': # while quit command is not entered
            if command == 'run': # if run command, prompt for file
                parse_source_code((raw_input('File:'))) 
            else:
                lines.append(parser.parse(command))
            print lines[-1]
            command = raw_input(">")
    elif argc == 2:  # source file is passed
        parse_source_code(sys.argv[1])


if __name__ == "__main__":
    main()





