import ffmpeg
import os
import sys

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('\n\t>> ERROR: Invalid arguments.\n\t>> Usage: "python convert.py in_file out_file [ flags ]"\n')
        print('\tOptional flags:\n\t\t-d : Delete input file(s) after conversion')
        print('\t\t-ldm : Convert the audio track of the input file into a LEFT-focused dual-mono track')
        print('\t\t-rdm : Convert the audio track of the input file into a RIGHT-focused dual-mono track')
        print('\t\t-f <dir_name>: Make folder to store new file(s) in')
        print()
        sys.exit(1)

    inputFilename = sys.argv[1]
    outputFilename = sys.argv[2]
    deletionFlag = False
    storeDirectory = None
    leftDualMonoFlag = False
    rightDualMonoFlag = False

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


    if inputWithoutExtension == '_all_':
        # Indicates that ANY filename with the given input extension should be converted
        files = os.listdir('./')
        targetFiles = ['.'.join(file.split('.')[:-1]) for file in files if file.endswith(f'.{inputExtension}') and file[0] != '.']
        
        i = 1
        for f in targetFiles:
            if outputWithoutExtension != '_same_':
                if leftDualMonoFlag:
                    ffmpeg.input(f"{f}.{inputExtension}").output(f"{storeDirectory + '/' if storeDirectory else ''}{outputWithoutExtension} {i}.{outputExtension}", af='pan=stereo|c0=c0|c1=c0', ac=2).run()
                elif rightDualMonoFlag:
                    ffmpeg.input(f"{f}.{inputExtension}").output(f"{storeDirectory + '/' if storeDirectory else ''}{outputWithoutExtension} {i}.{outputExtension}", af='pan=stereo|c0=c1|c1=c1', ac=2).run()
                else:
                    ffmpeg.input(f"{f}.{inputExtension}").output(f"{storeDirectory + '/' if storeDirectory else ''}{outputWithoutExtension} {i}.{outputExtension}").run()
                i += 1
            else:
                if leftDualMonoFlag:
                    ffmpeg.input(f"{f}.{inputExtension}").output(f"{storeDirectory + '/' if storeDirectory else ''}{f}.{outputExtension}", af='pan=stereo|c0=c0|c1=c0', ac=2).run()
                elif rightDualMonoFlag:
                    ffmpeg.input(f"{f}.{inputExtension}").output(f"{storeDirectory + '/' if storeDirectory else ''}{f}.{outputExtension}", af='pan=stereo|c0=c1|c1=c1', ac=2).run()
                else:
                    ffmpeg.input(f"{f}.{inputExtension}").output(f"{storeDirectory + '/' if storeDirectory else ''}{f}.{outputExtension}").run()
            
            if deletionFlag:
                os.remove(f"{f}.{inputExtension}")

    else:
        if outputWithoutExtension == '_same_':
            # Indicates that the name should remain the same with this new extension
            if leftDualMonoFlag:
                ffmpeg.input(inputFilename).output(f"{storeDirectory + '/' if storeDirectory else ''}{inputWithoutExtension}.{outputExtension}", af='pan=stereo|c0=c0|c1=c0', ac=2).run()
            elif rightDualMonoFlag:
                ffmpeg.input(inputFilename).output(f"{storeDirectory + '/' if storeDirectory else ''}{inputWithoutExtension}.{outputExtension}", af='pan=stereo|c0=c1|c1=c1', ac=2).run()
            else:
                ffmpeg.input(inputFilename).output(f"{storeDirectory + '/' if storeDirectory else ''}{inputWithoutExtension}.{outputExtension}").run()
        else:
            # Standard conversion
            if leftDualMonoFlag:
                ffmpeg.input(inputFilename).output(f"{storeDirectory + '/' if storeDirectory else ''}" + outputFilename, af='pan=stereo|c0=c0|c1=c0', ac=2).run()
            elif rightDualMonoFlag:
                ffmpeg.input(inputFilename).output(f"{storeDirectory + '/' if storeDirectory else ''}" + outputFilename, af='pan=stereo|c0=c1|c1=c1', ac=2).run()
            else:
                ffmpeg.input(inputFilename).output(f"{storeDirectory + '/' if storeDirectory else ''}" + outputFilename).run()

        if deletionFlag:
            os.remove(inputFilename)

    # ===============================================================================================