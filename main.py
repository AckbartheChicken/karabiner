import json
import parser
import writer
import sys

def main():
    path = sys.argv[1]
    lines = open(path,'r').readlines()
    tokens = parser.tokenize(lines)
    script = parser.parse(tokens)
    print(script)

    

if __name__ == "__main__":
    main()
