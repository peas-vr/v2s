# v2s - Video 2 Sprite Sheet

Video/GIF to Sprite Sheet for use as animated VRChat emoji's. 

This script will automatically batch process the file extensions `.gif`, `.mp4`, `.avi`, `.mov`, or `.mkv` into an 8x8 sprite sheet compatible with VRChat's web emoji uploader. It is recommended that input videos be short in length as an 8x8 sprite sheet will be a **maximum of 64 frames**. The script will attempt to skip frames to hit the maximum 64 frames. It will also create the correct output filename to upload to VRChat with automatic Frame/FPS detection.

## Usage
### Windows
1. Place v2s.exe into a folder
2. Place movie files with supported extensions into the same folder
3. Run v2s.exe

All files will be batch processed and all original files will be placed into a folder called `originals`. All processed sprite sheets will be placed into a folder called `spritesheets`.

### Linux

#### Prereqsuisites
- Python >3.13.3
- PIP

1. Clone the repository
2. Install the requirements   
```
pip install -r requirements.txt
```
3. Place movie files with a supported extension into the same folder
4. Run the script   
```
python v2s.py
```

All files will be batch processed and all original files will be placed into a folder called `originals`. All processed sprite sheets will be placed into a folder called `spritesheets`.

## VRChat
It is **REQUIRED** to have an active VRChat+ subscription to use this feature.

Once you have processed sprite sheets, you can upload the individual sprite sheets on the VRChat website by going to `Gallery -> Emoji -> Upload Emoji`. At this time you must check the box `Enable Sprite Sheet Mode [BETA]` before uploading.
