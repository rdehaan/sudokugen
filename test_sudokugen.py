import argparse
import sys

from sudokugen import examples

def main():

    # Take command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--num",
                        help="which example to run",
                        type=int, default=1)
    args = parser.parse_args(map(lambda x: x.lower(), sys.argv[1:]))
    num = args.num

    # Run the required example
    examples.generate_example(num)


if __name__ == "__main__":
    main()
