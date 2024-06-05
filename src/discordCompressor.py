'''
    Used for automatically compressing video files down to 25MB and adding
    "_compressed" to the end of the filename for sending via Discord.
'''

import sys
from convert import convert

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('\n\t>> ERROR: Invalid arguments.\n\t>> Usage: "python discordCompressor.py in_file [ flags ]"\n')
        print('\tOptional flags:\n')
        print('\t\t-rename <new_name>: Specify new name for output file')
        print()
        sys.exit(1)

    newName = None
    inputExtension = sys.argv[1].split('.')[-1].lower()

    if newName:
        sys.argv += [newName]
    else:
        sys.argv += ["{same}_compressed." + inputExtension]

    sys.argv += ["-fs", "25"]
    
    convert()