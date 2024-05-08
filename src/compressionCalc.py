'''
    Used for calculating compression percentage after -c flag for convert.py
    given a source file-size & expected output file-size

    NOTE: This script assumes command line arguments are Megabytes (MB)
    NOTE: This has been tested only using relatively small files (~100MB max.)
'''

import math
import sys

# =======================================================================================================================

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('\n\t>> ERROR: Invalid number of arguments.\n\t>> Usage: "python calcSize.py <sourceFileSize> <expectedFileSize>"\n')
        sys.exit(1)

    _, sourceFileSize, expectedOutputFileSize = sys.argv

    try:
        sourceFileSize = float(sys.argv[1])
        expectedOutputFileSize = float(sys.argv[2])

        sourceFileSize = int(sourceFileSize) if int(sourceFileSize) == sourceFileSize else sourceFileSize
        expectedOutputFileSize = int(expectedOutputFileSize) if int(expectedOutputFileSize) == expectedOutputFileSize else expectedOutputFileSize
    except ValueError:
        print("\n\tERROR: Source & expected output file-sizes must be a FLOAT or INTEGER.\n")
        sys.exit(1)

    if sourceFileSize <= 0 or expectedOutputFileSize <= 0:
        print("\n\tERROR: Source & expected output file-sizes must NOT be negative.\n")
        sys.exit(1)
    elif expectedOutputFileSize > sourceFileSize:
        print("\n\t>> ERROR: Expected output file-size should be SMALLER than source file-size.\n")
        sys.exit(1)

    # =============================================================================================

    compressionPercentageFloat = (1 - (expectedOutputFileSize / sourceFileSize) ) * 100

    if sourceFileSize - expectedOutputFileSize <= 15:
        compressionPercentageInt = math.ceil(compressionPercentageFloat)
    else:
        compressionPercentageInt = int(compressionPercentageFloat)

    print(f"\n\t {sourceFileSize} MB => {expectedOutputFileSize} MB \n\n\t Use -c {compressionPercentageFloat:.1f}, or just -c {compressionPercentageInt}\n")