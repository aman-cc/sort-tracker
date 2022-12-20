# Simple Online Realtime Tracker
Implementation of SORT tracker by Alex Bewley designed for online tracking applications where only past and current frames are available and the method produces object identities on the fly. While this minimalistic tracker doesn't handle occlusion or re-entering objects its purpose is to serve as a baseline and testbed for the development of future trackers. [[Source]](https://github.com/abewley/sort)

![Car tracking](assets/drive-track.gif?raw=true "Car tracking")

[[Source]](https://www.youtube.com/watch?v=FQINAGuleoU&t=616s)

![Person tracking](assets/walk-track.gif?raw=true "Person tracking")

[[Source]](https://www.youtube.com/watch?v=Af0SUwah1bQ&t=545s)

## Usage:
1. Activate virtualenv and install requirements
```
python3.10 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

2. Set parameters in `config.yaml`
```
tracker_max_age: 30   # Max age of object until it is disassociated
tracker_min_hits: 6   # Min hits of detector object until it is registered by tracker
video_path: del-drive.mp4   # Video filename present in root dir
detected_class_num: 2     # 2 for car, 0 for person
...
```

3. Run SORT Tracker
```
python track.py
```
Output is stored in out.avi
