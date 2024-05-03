import ffmpeg
import os
import sys

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('\n\t>> ERROR: Invalid arguments.\n\t>> Usage: "python convert.py in_file out_file [ flags ]"\n')
        print('\tOptional flags:\n')
        print('\t\t-d : Delete input file(s) after conversion')
        print('\t\t-ldm : Convert to LEFT channel-focused dual-mono file')
        print('\t\t-rdm : Convert to RIGHT channel-focused dual-mono file')
        print('\t\t-f <dir_name>: Make folder to store new file(s) in')
        print('\t\t-o [created, modified, name, size]: Specify conversion order when converting multiple files.')
        print()
        sys.exit(1)

    inputFilename = sys.argv[1]
    outputFilename = sys.argv[2]
    conversionOrder = None
    deletionFlag = False
    leftDualMonoFlag = False
    rightDualMonoFlag = False
    storeDirectory = None

    if "-d" in sys.argv:
        deletionFlag = True

    if "-ldm" in sys.argv and "-rdm" in sys.argv:
        print('\n\t>> ERROR: Invalid arguments.\n\t>> Can NOT use both \"-ldm\" and \"-rdm\"flags together."\n')
        pass
    elif "-ldm" in sys.argv:
        leftDualMonoFlag = True
    elif "-rdm" in sys.argv:
        rightDualMonoFlag = True
    
    if "-f" in sys.argv:
        if sys.argv[-1] == '-f':
            print("\n\tERROR: Last input argument can't be -f.\n")
            sys.exit(1)

        for i in range(len(sys.argv) ):
            if sys.argv[i] == '-f':
                storeDirectory = sys.argv[i + 1]

    if "-o" in sys.argv:
        if inputFilename[0:5] != '_all_':
            print("\n\tERROR: Ordering flag can not be used unless \"_all_\" is specified as the input filename.\n")
            sys.exit(1)
        elif sys.argv[-1] == '-o':
            print("\n\tERROR: Last input argument can't be -o.\n")
            sys.exit(1)
        
        for i in range(len(sys.argv) ):
            if sys.argv[i] == '-o':
                conversionOrder = sys.argv[i + 1]
        
        if conversionOrder not in ['created', 'modified', 'name', 'size']:
            print('\n\tERROR: Specified conversion order must be one of "created", "modified", "name" or "size". \n')
            sys.exit(1)

    # ===============================================================================================

    inputWithoutExtension = '.'.join(inputFilename.split('.')[:-1])
    inputExtension = inputFilename.split('.')[-1]

    outputWithoutExtension = '.'.join(outputFilename.split('.')[:-1])
    outputExtension = outputFilename.split('.')[-1]

    # ===============================================================================================

    if storeDirectory:
        # Check if specified store-directory exists. If not, create it.
        if not os.path.exists(storeDirectory):
            os.makedirs(storeDirectory)

    targetFiles = [] # Can be a list containing one file if file was specified, or a list of many if _all_ was used

    if inputWithoutExtension == '_all_':
        # Indicates that ANY filename with the given input extension should be converted

        if conversionOrder:
            if conversionOrder == 'created': # Most-original first
                files = sorted(os.listdir(os.curdir), key=lambda x: os.path.getctime(os.path.join(os.curdir, x) ) )
            elif conversionOrder == 'modified': # Most-original first
                files = sorted(os.listdir(os.curdir), key=lambda x: os.path.getmtime(os.path.join(os.curdir, x) ) )
            elif conversionOrder == 'name': # Alphabetical order
                files = sorted(os.listdir(os.curdir) )
            elif conversionOrder == 'size': # Smallest first
                files = sorted(os.listdir(os.curdir), key=lambda x: os.path.getsize(os.path.join(os.curdir, x) ), reverse=True)
            else:
                print('\n\tERROR: Specified conversion order must be one of "created", "modified", "name" or "size". \n')
                sys.exit(1)
        else:
            files = os.listdir(os.curdir)

        for f in files:
            if f.endswith(f'.{inputExtension}') and f[0] != '.':
                targetFiles.append('.'.join(f.split('.')[:-1]) )
    else:
        targetFiles.append(inputWithoutExtension)
    
    fileCounter = 1
    for f in targetFiles:
        calculatedOutputPath = ''

        if storeDirectory:
            calculatedOutputPath += storeDirectory + '/'

        if outputWithoutExtension == '_same_':
            # Indicates that the name should remain the same with this new extension
            calculatedOutputPath += f'{f}.{outputExtension}'
        else:
            if len(targetFiles) == 1:
                calculatedOutputPath += f'{outputWithoutExtension}.{outputExtension}'
            else:
                calculatedOutputPath += f'{outputWithoutExtension} {fileCounter}.{outputExtension}'

        # =============================================================================================================

        if leftDualMonoFlag:
            ffmpeg.input(f"{f}.{inputExtension}").output(calculatedOutputPath, af='pan=stereo|c0=c0|c1=c0', ac=2).run()
        elif rightDualMonoFlag:
            ffmpeg.input(f"{f}.{inputExtension}").output(calculatedOutputPath, af='pan=stereo|c0=c1|c1=c1', ac=2).run()
        else:
            ffmpeg.input(f"{f}.{inputExtension}").output(calculatedOutputPath).run()

        # ==========================================================================

        if deletionFlag:
                os.remove(f"{f}.{inputExtension}")

        # ========================================

        fileCounter += 1

    # ===============================================================================================