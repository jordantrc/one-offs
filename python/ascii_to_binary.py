#!/usr/bin/env python3
#
# Usage:
# ascii_to_binary.py [OPTIONS] <ascii text>
# Options:
#   -d, --detail    provide the letter converted
#                   as well as the binary equivalent
#                   in the output
#   -s, --separator use this separator during output
# If no text is provided the program
# will prompt the user to provide input.
# The program only works with the original
# 7-bit ASCII character set.
#

import argparse
import math
import sys

def char_to_binary(char):
    """Converts a character to it's binary representation. This is a hacky way to do this, I know
    the most efficient way would involve bit shifting and all that, but I'm lazy."""
    binary = ""

    exponent = 6
    remainder = ord(char)
    while exponent >= 0:
        divisor = int(math.pow(2, exponent))
        if remainder / divisor >= 1:
            binary = binary + "1"
            remainder = remainder - divisor
        else:
            binary = binary + "0"
        exponent = exponent - 1
    return binary

def main():
    """main function"""
    detail = False
    separator = "\n"
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--detail", action="store_true", help="provide the character converted in output")
    parser.add_argument("-s", "--separator", nargs=1, help="use the character as separator")
    parser.add_argument("input", nargs="?", help="string to convert")
    args = parser.parse_args()

    if args.detail:
        detail = True

    if args.separator is not None:
        separator = args.separator[0]

    if args.input is None:
        # prompt for input
        ascii_input = input("Enter ASCII text: ")
    else:
        ascii_input = args.input
    
    output = ""
    if len(ascii_input) > 0:
        for c in ascii_input:
            binary = char_to_binary(c)
            if detail:
                output = output + "%s%s - %s" % (separator, c, binary)
            else:
                output = output + separator + binary
    
    print("Binary:")
    print(output)


if __name__ == "__main__":
    main()
