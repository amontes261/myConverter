# myConverter
A simple Python converter that utilizes [FFMPEG](https://pypi.org/project/ffmpeg-python/) for audio-visual file conversions.

### Usage

`python convert.py <input_file> <outpuf_file> [ flags ]`

#### Flags

     -rm : Delete input file(s) after conversion
     -mkdir <dir_name>: Make folder to store new file(s) in
     -c <percentage>: Compress the input file\'s bitrate by X%
     -o [created, modified, name, size]: Specify conversion order when converting multiple files
     -left : Convert to LEFT channel-focused dual-mono file
     -right : Convert to RIGHT channel-focused dual-mono file

### Examples

\> *Coming Soon*

<hr>

### Future Plans/Ideas

- [ ] Add support to specify individual files (middleground between converting a singular file and using \_all\_)
- [ ] Horizontally or vertically flip input-file(s)
<hr>

### Completed Features

- [x] Delete the input-file after it's been converted

     **\> Added as `-rm` flag**

- [x] Make directory to dump converted file(s) into

     **\> Added as `-mkdir` flag**

- [x] Compress output-file

     **\> Added as `-c` flag**

- [x] Specify conversion-order when converting more than 1 file

     **\> Added as `-o` flag**

- [x] Focus stereo input toward one channel, outputting as either as left or right dual-mono

     **\> Added as `-left` and `-right` flags, respectively**