
from xml_generator import build_xml
import sys


def main(args):
    build_xml(sys.argv[1], sys.argv[2], sys.argv[3])
    #print("Arguments passed to main:", args)


if __name__ == "__main__":
    main(sys.argv[1:])

# python main.py "permanent.json" "variable.json" "result.xml"



