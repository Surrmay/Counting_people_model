# STEP-BY-STEP INSTALLATION & RUN GUIDE
# =======================================

## COMPLETE GUIDE TO RUN THE PEOPLE COUNTER
## ==========================================

This guide will walk you through EVERY step from installation to running the program.
Follow these steps in order!

---

## PART 1: INSTALL PYTHON (if not already installed)
## ==================================================

### Check if Python is installed:
1. Open Command Prompt (Windows) or Terminal (Mac/Linux)
2. Type: python --version
3. Press Enter

If you see "Python 3.8" or higher → SKIP to PART 2
If you see an error → Continue below to install Python

### Install Python:
1. Go to: https://www.python.org/downloads/
2. Download Python 3.11 or 3.12 (latest stable version)
3. Run the installer
4. ⚠️ IMPORTANT: Check the box "Add Python to PATH"
5. Click "Install Now"
6. Wait for installation to complete
7. Restart your computer

---

## PART 2: CREATE PROJECT FOLDER
## ===============================

1. Create a new folder on your Desktop called "people_counter"
2. Place your video file in this folder
3. Rename your video to "mall_entrance.mp4" OR remember its exact name

Your folder should look like:
```
people_counter/
    mall_entrance.mp4  (your video file)
```

---

## PART 3: DOWNLOAD THE PYTHON FILES
## ==================================

You need 3 Python files:
1. CentroidTracker.py
2. people_counter.py  
3. requirements.txt (we'll create this)

Save all 3 files in the "people_counter" folder you created.

Your folder should now look like:
```
people_counter/
    CentroidTracker.py
    people_counter.py
    requirements.txt
    mall_entrance.mp4
```

---

## PART 4: CREATE REQUIREMENTS.TXT
## =================================

1. Open Notepad (Windows) or TextEdit (Mac)
2. Copy and paste these lines EXACTLY:

ultralytics>=8.0.0
opencv-python>=4.8.0
numpy>=1.24.0
scipy>=1.10.0

3. Save the file as "requirements.txt" in the people_counter folder
4. ⚠️ Make sure it's saved as .txt, not .txt.txt

---

## PART 5: INSTALL REQUIRED LIBRARIES
## ====================================

### Windows:
1. Open Command Prompt
2. Navigate to your folder:
   cd Desktop\people_counter
3. Create virtual environment (optional but recommended):
   python -m venv venv
4. Activate it:
   venv\Scripts\activate
5. Install libraries:
   pip install -r requirements.txt
6. Wait 2-5 minutes for installation

### Mac/Linux:
1. Open Terminal
2. Navigate to your folder:
   cd Desktop/people_counter
3. Create virtual environment (optional but recommended):
   python3 -m venv venv
4. Activate it:
   source venv/bin/activate
5. Install libraries:
   pip install -r requirements.txt
6. Wait 2-5 minutes for installation

You should see messages like "Successfully installed ultralytics-8.x.x..."

---

## PART 6: VERIFY INSTALLATION
## =============================

Test if libraries are installed correctly:

### Windows:
python -c "import cv2; print('OpenCV OK')"
python -c "from ultralytics import YOLO; print('YOLO OK')"
python -c "import numpy; print('NumPy OK')"
python -c "import scipy; print('SciPy OK')"

### Mac/Linux:
python3 -c "import cv2; print('OpenCV OK')"
python3 -c "from ultralytics import YOLO; print('YOLO OK')"
python3 -c "import numpy; print('NumPy OK')"
python3 -c "import scipy; print('SciPy OK')"

If all show "OK" → Proceed to PART 7
If any shows an error → Re-run the pip install command from PART 5

---

## PART 7: CONFIGURE THE PROGRAM
## ===============================

1. Open people_counter.py in Notepad or any text editor
2. Find this line (near the bottom):
   video_path = "mall_entrance.mp4"
3. Change "mall_entrance.mp4" to YOUR video filename
   Examples:
   - video_path = "entrance.mp4"
   - video_path = "shopping_mall.mp4"
   - video_path = "C:/Videos/my_video.mp4"  (full path)
4. Save the file

---

## PART 8: RUN THE PROGRAM! 🚀
## ============================

### Windows:
1. Open Command Prompt
2. Navigate to folder:
   cd Desktop\people_counter
3. If using virtual environment, activate it:
   venv\Scripts\activate
4. Run the program:
   python people_counter.py

### Mac/Linux:
1. Open Terminal
2. Navigate to folder:
   cd Desktop/people_counter
3. If using virtual environment, activate it:
   source venv/bin/activate
4. Run the program:
   python3 people_counter.py

---

## WHAT YOU'LL SEE:
## =================

The program will:
1. Load the YOLO model (auto-downloads on first run, ~6MB)
2. Open your video file
3. Process each frame
4. Print messages like:
   ✓ [IN]  Person ID 0 entered | Total IN: 1
   ✓ [OUT] Person ID 3 exited  | Total OUT: 1
5. Show progress every 30 frames
6. Save output video as "output_people_counter.mp4"

Processing time depends on:
- Video length (1 minute video ≈ 2-3 minutes processing)
- Your computer speed
- Video resolution

---

## PART 9: VIEW RESULTS
## =====================

After processing completes, you'll see:

======================================================================
FINAL STATISTICS
======================================================================
✓ People Entered (IN):        15
✓ People Exited (OUT):        12
✓ Net Count (IN - OUT):       3
✓ Total Frames Processed:     900
✓ Processing Time:            45.23 seconds
✓ Average FPS:                19.89
✓ Output Video Saved:         output_people_counter.mp4
======================================================================

The output video will have:
- Green bounding boxes around people
- Unique IDs for each person
- Yellow counting line
- IN/OUT counters
- Tracking trails

Open "output_people_counter.mp4" in any video player to see the results!

---

## TROUBLESHOOTING
## ================

### Problem: "python is not recognized"
Solution: 
- Python not installed or not in PATH
- Try "python3" instead of "python"
- Reinstall Python with "Add to PATH" checked

### Problem: "No module named 'cv2'"
Solution:
- Libraries not installed
- Run: pip install opencv-python

### Problem: "No module named 'ultralytics'"
Solution:
- Run: pip install ultralytics

### Problem: "Video file not found"
Solution:
- Check video filename spelling
- Make sure video is in the same folder
- Use full path: video_path = "C:/Users/YourName/Desktop/video.mp4"

### Problem: "Could not open video file"
Solution:
- Video file might be corrupted
- Try a different video
- Check video format (MP4 works best)

### Problem: Processing is very slow
Solution:
- Normal! Processing takes time
- 1 minute video ≈ 2-3 minutes to process
- Close other programs to free up CPU

### Problem: No detections / counting is wrong
Solution:
- Check video quality (needs clear view of people)
- Adjust confidence threshold in code (try 0.3 or 0.5)
- Make sure video shows people clearly

---

## QUICK START SUMMARY
## ====================

For experienced users, here's the short version:

1. Install Python 3.8+
2. Create folder with 3 files:
   - CentroidTracker.py
   - people_counter.py
   - your_video.mp4
3. Install libraries:
   pip install ultralytics opencv-python numpy scipy
4. Edit video_path in people_counter.py
5. Run:
   python people_counter.py
6. Wait for processing
7. Open output_people_counter.mp4

---

## FILE EXECUTION ORDER
## =====================

DO NOT run CentroidTracker.py directly!

ONLY run: python people_counter.py

The execution flow is:
1. You run: people_counter.py
2. people_counter.py imports: CentroidTracker.py
3. people_counter.py loads: YOLO model
4. people_counter.py processes: your video
5. people_counter.py saves: output video

---

## EXPECTED OUTPUT FILES
## ======================

After running, you will have:
```
people_counter/
    CentroidTracker.py       (your code)
    people_counter.py        (your code)
    requirements.txt         (dependencies)
    mall_entrance.mp4        (input video)
    output_people_counter.mp4  (✓ OUTPUT - watch this!)
    yolov8n.pt               (YOLO model - auto-downloaded)
```

---

## NEXT STEPS
## ===========

After successfully running:
1. Watch the output video
2. Check if counting is accurate
3. Try with different videos
4. Adjust parameters:
   - Change line_y position (line 107 in people_counter.py)
   - Change confidence threshold (line 186)
   - Change max_disappeared (line 104)

---

## SUPPORT
## ========

If you still have issues:
1. Check Python version: python --version
2. Check library versions: pip list
3. Make sure all 3 files are in same folder
4. Try with a simple, short video first (30 seconds)
5. Check video plays normally in VLC or other player

---

## SUMMARY CHECKLIST
## ==================

Before running, make sure:
☐ Python 3.8+ installed
☐ All libraries installed (ultralytics, opencv-python, numpy, scipy)
☐ CentroidTracker.py in folder
☐ people_counter.py in folder
☐ Video file in folder
☐ video_path correctly set in people_counter.py
☐ Command prompt/terminal in correct folder

Then run: python people_counter.py

Good luck! 🎉

---

Author: Computer Vision Tutorial
Date: October 2025
