#!/usr/bin/env python3
#
# Usage:
# ascii_to_binary.py <ascii text>
# If not text is provided the program
# will prompt the user to provide some.
#

import math
import sys

def char_to_binary(char):
    """Converts a character to it's binary representation. This is a hacky way to do this, I know
    the most efficient way would involve bit shifting and all that, but I'm lazy."""
    binary = ""

    exponent = 7
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
    if len(sys.argv) == 1:
        # prompt for input
        ascii_input = input("Enter ASCII text: ")
    else:
        ascii_input = sys.argv[1]
    
    output = ""
    if len(ascii_input) > 0:
        for c in ascii_input:
            binary = char_to_binary(c)
            output = output + "\n" + binary
    
    print("Binary:")
    print(output)


if __name__ == "__main__":
    main()
