#!/usr/bin/python3

# based on work done here:  https://www.youtube.com/watch?v=7IzxZKL2uUE
import struct
import argparse

parser = argparse.ArgumentParser(description='Translate input string to PSK31 bits and save to binary file for transmission with gnuradio.')
parser.add_argument('-f', '--file', help='Binary output file', default='')
parser.add_argument('-s', '--string', help="String to translate (don't forget to include your callsign first if transmitting on amateur radio bands)", default='')
parser.add_argument('-l', '--line', help='Send line feed after string', action='store_true', default=False)
parser.add_argument('-p', '--print', help='print binary stream to stdout', action='store_true', default=False)

args = parser.parse_args()

if len(args.file) == 0:
    print("ERROR: Please provide an output file.")
    exit(1)
    
if len(args.string) == 0:
    print("ERROR: Please provide an input string to translate.")
    exit(1)
    
transmit_text=args.string

if args.line:
    transmit_text+='\n'
    
# See https://en.wikipedia.org/wiki/Varicode for full dictionary
varicode_dictionary = {'a':'1011',
                                     'b':'1011111', 
                                     'c':'101111', 
                                     'd':'101101', 
                                     'e':'11', 
                                     'f':'111101',
                                     'g':'1011011', 
                                     'h':'101011', 
                                     'i':'1101', 
                                     'j':'111101011', 
                                     'k':'10111111', 
                                     'l':'11011', 
                                     'm':'111011', 
                                     'n':'1111', 
                                     'o':'111', 
                                     'p':'111111', 
                                     'q':'110111111', 
                                     'r':'10101', 
                                     's':'10111', 
                                     't':'101', 
                                     'u':'110111', 
                                     'v':'1111011', 
                                     'w':'1101011', 
                                     'x':'11011111', 
                                     'y':'1011101', 
                                     'z':'111010101', 
                                     'A':'1111101', 
                                     'B':'11101011', 
                                     'C':'10101101', 
                                     'D':'10110101', 
                                     'E':'1110111', 
                                     'F':'11011011', 
                                     'G':'11111101', 
                                     'H':'101010101', 
                                     'I':'1111111', 
                                     'J':'111111101', 
                                     'K':'101111101', 
                                     'L':'11010111', 
                                     'M':'10111011', 
                                     'N':'10111011', 
                                     'O':'10101011', 
                                     'P':'11010101', 
                                     'Q':'111011101', 
                                     'R':'10101111', 
                                     'S':'1101111', 
                                     'T':'1101101', 
                                     'U':'101010111', 
                                     'V':'110110101', 
                                     'W':'101011101', 
                                     'X':'101110101', 
                                     'Y':'101111011', 
                                     'Z':'1010101101', 
                                     ' ':'1', 
                                     '0':'10110111', 
                                     '1':'10111101', 
                                     '2':'11101101', 
                                     '3':'11111111', 
                                     '4':'101110111', 
                                     '5':'101011011', 
                                     '6':'101101011', 
                                     '7':'110101101', 
                                     '8':'110101011', 
                                     '9':'110110111', 
                                     '!':'111111111', 
                                     '"':'101011111', 
                                     '#':'111110101',
                                     '$':'111011011', 
                                     '%':'1011010101', 
                                     '&':'1010111011', 
                                     "'":'101111111', 
                                     '(':'11111011', 
                                     ')':'11110111', 
                                     '*':'101101111', 
                                     '+':'111011111', 
                                     ',':'1110101', 
                                     '-':'110101', 
                                     '.':'1010111', 
                                     '/':'110101111', 
                                     '@':'1010111101', 
                                     ':':'11110101', 
                                     ';':'110111101', 
                                     '<':'111101101', 
                                     '=':'1010101', 
                                     '>':'111010111', 
                                     '?':'1010101111', 
                                     '[':'111110111', 
                                     "\\":'111101111', 
                                     ']':'111111011', 
                                     '^':'1010111111', 
                                     '_':'101101101', 
                                     '{':'1010110111', 
                                     '|':'110111011', 
                                     '}':'1010110101', 
                                     '~':'1011010111', 
                                     '\n':'11101', 
                                     '\r':'11111', 
                                     '\t':'11101111'}
                                     
# 8-bit preamble (this gets inverted later)
varicode_string='00000000'

for char in transmit_text:
    if char in varicode_dictionary:
        varicode_string += varicode_dictionary[char]
        # Each char gets transmitted with a terminator:
        varicode_string += '00'

# Postamble
varicode_string += '11111111'

if args.print:
    print(varicode_string)
    
# Pad with ones to form whole bytes for the file:
while len(varicode_string)%8 != 0:
    varicode_string += '1'
    
f=open(args.file,'wb')

for n in range(0, int(len(varicode_string)/8)):
    u8=~int(varicode_string[8*n:8*(n+1)], 2) % 2**8
    f.write(struct.pack('@B', u8))
    
f.close()

print('Binary written to ', args.file)
