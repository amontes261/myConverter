import ffmpeg
import math
import os
import send2trash
import sys

# =============================================================================================================

def convert():
    if len(sys.argv) < 3:
        print('\n\t>> ERROR: Invalid arguments.\n\t>> Usage: "python convert.py in_file out_file [ flags ]"\n')
        print('\tOptional flags:\n')
        print('\t\t-c <percentage> : Compress the input file\'s bitrate by X%')
        print('\t\t-fs <size_in_MB> : Attempt to compress the input file\'s bitrate to an inputted size [ BETA ]')
        print('\t\t-hflip : Horizontally flip video along the Y axis')
        print('\t\t-mkdir <dir_name> : Make folder to store new file(s) in')
        print('\t\t-o [created, modified, name, size] : Specify conversion order when converting multiple files')
        print('\t\t-left : Convert to LEFT channel-focused dual-mono file')
        print('\t\t-right : Convert to RIGHT channel-focused dual-mono file')
        print('\t\t-rm : Delete input file(s) after conversion')
        print('\t\t-vflip : Vertically flip video along the X axis')
        print()
        sys.exit(1)

    inputFilename = sys.argv[1]
    outputFilename = sys.argv[2]
    compressionFileSize = None
    compressionPercentage = None
    conversionOrder = None
    deletionFlag = False
    horizontalFlipFlag = False
    leftDualMonoFlag = False
    rightDualMonoFlag = False
    storeDirectory = None
    verticalFlipFlag = False

    if "-rm" in sys.argv:
        deletionFlag = True

    if "-left" in sys.argv and "-right" in sys.argv:
        print('\n\t>> ERROR: Invalid arguments.\n\t>> Can NOT use both \"-left\" and \"-right\"flags together."\n')
        sys.exit(1)
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

    if "-fs" in sys.argv:
        if sys.argv[-1] == '-fs':
            print("\n\tERROR: Last input argument can't be -fs.\n")
            sys.exit(1)
            
        if "-c" in sys.argv:
            print("\n\tERROR: Can NOT declare both -fs and -c flags. Please use one or the other.\n")
            sys.exit(1)
        
        for i in range(len(sys.argv) ):
            if sys.argv[i] == '-fs':
                try:
                    compressionFileSize = float(sys.argv[i + 1])
                    if compressionFileSize < 1:
                        print("\n\tERROR: Compression file size must be 1MB or greater.\n")
                        sys.exit(1)
                except ValueError:
                    print("\n\tERROR: Compression file size must be a FLOAT or INTEGER.\n")
                    sys.exit(1)

    if "-c" in sys.argv:
        if sys.argv[-1] == '-c':
            print("\n\tERROR: Last input argument can't be -c.\n")
            sys.exit(1)

        if "-fs" in sys.argv:
            print("\n\tERROR: Can NOT declare both -c and -fs flags. Please use one or the other.\n")
            sys.exit(1)
        
        for i in range(len(sys.argv) ):
            if sys.argv[i] == '-c':
                try:
                    compressionPercentage = float(sys.argv[i + 1])
                    if compressionPercentage < 1 or compressionPercentage > 100:
                        print("\n\tERROR: Compression percentage must range from 1 to 100, inclusively.\n")
                        sys.exit(1)
                except ValueError:
                    print("\n\tERROR: Compression percentage must be a FLOAT or INTEGER.\n")
                    sys.exit(1)

    if "-o" in sys.argv:
        if inputFilename[0:5] != '{all}':
            print("\n\tERROR: Ordering flag can not be used unless \"{all}\" is specified as the input filename.\n")
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

    if "-hflip" in sys.argv:
        horizontalFlipFlag = True

    if "-vflip" in sys.argv:
        verticalFlipFlag = True

    # ===============================================================================================

    inputWithoutExtension = '.'.join(inputFilename.split('.')[:-1])
    inputExtension = inputFilename.split('.')[-1].lower()

    outputWithoutExtension = '.'.join(outputFilename.split('.')[:-1])
    outputExtension = outputFilename.split('.')[-1].lower()

    # ===============================================================================================

    if storeDirectory:
        # Check if specified store-directory exists. If not, create it.
        if not os.path.exists(storeDirectory):
            os.makedirs(storeDirectory)

    targetFiles = [] # Can be a list containing one file if file was specified, or a list of many if {all} was used

    if inputWithoutExtension == '{all}':
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
                print('\n\tERROR: Specified conversion order must be one of "created", "modified", "name" or "size".\n')
                sys.exit(1)
        else:
            files = os.listdir(os.curdir)

        for f in files:
            if f.lower().endswith(f'.{inputExtension}') and f[0] != '.':
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

        if outputWithoutExtension == "{same}":
            # Indicates that the name should remain the same with this new extension
            if inputExtension == outputExtension:
                # Add '.' to beginning of output file path to store converted data, changed on last-step
                calculatedOutputPath += '.'
            
            calculatedOutputPath += f'{f}.{outputExtension}'
        elif "{same}" not in outputWithoutExtension:
            if len(targetFiles) == 1:
                calculatedOutputPath += f'{outputWithoutExtension}.{outputExtension}'
            else:
                calculatedOutputPath += f'{outputWithoutExtension} {fileCounter}.{outputExtension}'
        elif "{same}" in outputWithoutExtension:
            if outputWithoutExtension.count("{same}") != 1:
                print('\n\tERROR: "{same}" indicator should only appear ONCE in the specified output file string.\n')
                sys.exit(1)

            sameSplit = outputWithoutExtension.split("{same}")
            ouputFilenameWithInput = f'{sameSplit[0]}{f}{sameSplit[1]}'

            calculatedOutputPath += f'{ouputFilenameWithInput}.{outputExtension}'

        # =============================================================================================================

        if compressionPercentage or compressionFileSize:
            videoProbe = ffmpeg.probe(f'{f}.{inputExtension}')
            try: # Try and get the bitrate of the video coming in. This will catch if only an audio file's coming in.
                actualBitrate = int(next(stream for stream in videoProbe['streams'] if stream['codec_type'] == 'video')['bit_rate'])
            except StopIteration: # Case: Input file has NO video stream, so the bitrate will be pulled from the audio instead.
                actualBitrate = int(next(stream for stream in videoProbe['streams'] if stream['codec_type'] == 'audio')['bit_rate'])

            if compressionPercentage:
                # Keep it lower than how it came in, but above 1000K
                targetBitrate = max(1000, min(actualBitrate, actualBitrate * ( (100 - compressionPercentage) / 100) ) )
            else:
                sourceFilesize = os.path.getsize(inputFilename) # 65355856 -> 65.4MB
                calculatedCompressionPct = math.ceil( (1 - (compressionFileSize * 1000000 / sourceFilesize) ) * 100) + 3 # Add 3-ish to the percentage to ensure under target file-size
                targetBitrate = max(1000, min(actualBitrate, actualBitrate * ( (100 - calculatedCompressionPct) / 100) ) )
        # =============================================================================================================

        inputPath = f"{f}.{inputExtension}"

        ffmpegObject = ffmpeg.input(inputPath)

        if horizontalFlipFlag:
            ffmpegObject = ffmpeg.hflip(ffmpegObject)

        if verticalFlipFlag:
            ffmpegObject = ffmpeg.vflip(ffmpegObject)
        
        if compressionPercentage or compressionFileSize:
            ffmpegObject = ffmpegObject.output(calculatedOutputPath, af=audioFilter, ac=2, b=targetBitrate)
        else:
            ffmpegObject = ffmpegObject.output(calculatedOutputPath, af=audioFilter, ac=2)

        ffmpegObject.run()
        # ============================================================================================

        if inputPath == calculatedOutputPath[1:]:
            # Remove '.' from beginning of converted file once input-file of the same name is deleted
            send2trash.send2trash(inputPath)
            os.rename(calculatedOutputPath, calculatedOutputPath[1:])
        elif deletionFlag:
            send2trash.send2trash(inputPath)

        # ========================================

        fileCounter += 1

    # ===============================================================================================

if __name__ == "__main__":
    convert()
