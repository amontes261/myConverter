import ffmpeg
import os
import sys

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('\n\t>> ERROR: Invalid arguments.\n\t>> Usage: "python convert.py in_file out_file [ flags ]"\n')
        print('\tOptional flags:\n')
        print('\t\t-rm : Delete input file(s) after conversion')
        print('\t\t-mkdir <dir_name>: Make folder to store new file(s) in')
        print('\t\t-c <percentage>: Compress the input file\'s bitrate by X%')
        print('\t\t-o [created, modified, name, size]: Specify conversion order when converting multiple files.')
        print('\t\t-left : Convert to LEFT channel-focused dual-mono file')
        print('\t\t-right : Convert to RIGHT channel-focused dual-mono file')
        print()
        sys.exit(1)

    inputFilename = sys.argv[1]
    outputFilename = sys.argv[2]
    compressionPercentage = None
    conversionOrder = None
    deletionFlag = False
    leftDualMonoFlag = False
    rightDualMonoFlag = False
    storeDirectory = None

    if "-rm" in sys.argv:
        deletionFlag = True

    if "-left" in sys.argv and "-right" in sys.argv:
        print('\n\t>> ERROR: Invalid arguments.\n\t>> Can NOT use both \"-left\" and \"-right\"flags together."\n')
        pass
    elif "-left" in sys.argv:
        leftDualMonoFlag = True
    elif "-right" in sys.argv:
        rightDualMonoFlag = True
    
    if "-mkdir" in sys.argv:
        if sys.argv[-1] == '-mkdir':
            print("\n\tERROR: Last input argument can't be -mkdir.\n")
            sys.exit(1)

        for i in range(len(sys.argv) ):
            if sys.argv[i] == '-mkdir':
                storeDirectory = sys.argv[i + 1]

    if "-c" in sys.argv:
        if sys.argv[-1] == '-o':
            print("\n\tERROR: Last input argument can't be -c.\n")
            sys.exit(1)
        
        for i in range(len(sys.argv) ):
            if sys.argv[i] == '-c':
                try:
                    compressionPercentage = int(sys.argv[i + 1])
                    if compressionPercentage < 1 or compressionPercentage > 100:
                        print("\n\tERROR: Compression percentage must range from 1 to 100, inclusively.\n")
                        sys.exit(1)
                except ValueError:
                    print("\n\tERROR: Compression percentage must be an INTEGER.\n")
                    sys.exit(1)

        if compressionPercentage < 1 or compressionPercentage > 100 or type(compressionPercentage) == float:
            print("\n\tERROR: Compression percentage must be an INTEGER, inclusively ranging from 1 to 100.\n")
            sys.exit(1)

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

    if leftDualMonoFlag:
        audioFilter = 'pan=stereo|c0=c0|c1=c0'
    elif rightDualMonoFlag:
        audioFilter = 'pan=stereo|c0=c1|c1=c1'
    else: # No change: keep left to left & keep right to right
        audioFilter = 'pan=stereo|c0=c0|c1=c1'
    
    # ========================================================

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

        videoProbe = ffmpeg.probe(f'{f}.{inputExtension}')
        actualBitrate = int(next(stream for stream in videoProbe['streams'] if stream['codec_type'] == 'video')['bit_rate'])

        # Keep it lower than how it came in, but above 1000K
        targetBitrate = max(1000, min(actualBitrate, actualBitrate * ( (100 - compressionPercentage) / 100) ) )

        # =============================================================================================================

        ffmpeg.input(f"{f}.{inputExtension}").output(calculatedOutputPath, af=audioFilter, ac=2, b=targetBitrate).run()

        # ============================================================================================

        if deletionFlag:
                os.remove(f"{f}.{inputExtension}")

        # ========================================

        fileCounter += 1

    # ===============================================================================================