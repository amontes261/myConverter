# myConverter
A simple Python converter that utilizes [FFMPEG](https://pypi.org/project/ffmpeg-python/) for audio-visual file conversions.

### Usage

     python convert.py <input_file> <outpuf_file> [ flags ]

#### Flags

     -rm : Delete input file(s) after conversion
     -mkdir <dir_name>: Make folder to store new file(s) in
     -c <percentage>: Compress the input file\'s bitrate by X%
     -o [created, modified, name, size]: Specify conversion order when converting multiple files
     -left : Convert to LEFT channel-focused dual-mono file
     -right : Convert to RIGHT channel-focused dual-mono file

### Examples

     python convert.py

<hr>

### Future Plans/Ideas

- [ ] Add support to specify individual files (middleground between converting a singular file and using \_all\_)
- [ ] Find a **STABLE** way to compress an input file so the output file's size meets/is below a specified threshold
<hr>

### Completed Features

- [x] Delete the input-file after it's been converted

     **\> Added as `-rm` flag**

- [x] Make directory to dump converted file(s) into

     **\> Added as `-mkdir` flag**

- [x] Compress output-file given a compression percentage

     **\> Added as `-c` flag**

- [x] Compress output-file given a target filesize

     **\> Added as a BETA command via `-fs` flag**

- [x] Specify conversion-order when converting more than 1 file

     **\> Added as `-o` flag**

- [x] Focus stereo input toward one channel, outputting as either as left or right dual-mono

     **\> Added as `-left` and `-right` flags, respectively**

- [x] Flip inputted file over X and/or Y axis

     **\> Added as `-vflip` and `-hflip` flags, respectively**