🧍‍♂️ People Counter with YOLOv8
Real-time Detection, Tracking & Counting using Computer Vision

🧭 Overview

People Counter with YOLOv8 is a computer vision system designed to automatically detect, track, and count people entering and exiting a video scene. It leverages YOLOv8 (You Only Look Once) for object detection and Centroid Tracking for consistent object identification across frames.

This project provides a foundational framework for real-world applications such as retail analytics, facility management, and crowd monitoring.

🎯 Objective

To develop a robust and customizable people counting solution capable of accurately monitoring human movement in various video feeds using advanced detection and tracking algorithms.

⚙️ System Architecture

Video Input:
The system reads frames sequentially from a video file or live stream.

Detection (YOLOv8):
Each frame is analyzed to locate and classify people.

Tracking (Centroid Algorithm):
Detected positions are compared with previous frames using Euclidean distance to maintain unique IDs.

Counting Logic:
When a tracked person crosses the predefined line, they are counted as entering (IN) or exiting (OUT).

Output Generation:
Annotated frames are compiled into an output video with total IN/OUT/NET counts.

🧮 Performance Metrics
Metric	Typical Range	Notes
CPU Speed	15–25 FPS	Depends on video resolution
GPU Speed (CUDA)	30–50+ FPS	Enables near real-time operation
Model Size	~6 MB (YOLOv8n)	Small footprint
Accuracy	85–95%	Dependent on lighting and camera angle
Memory Usage	~500 MB	During active processing
🖥️ System Requirements
Minimum

Processor: Intel i5 or equivalent

RAM: 8 GB

Storage: 2 GB free space

Python: 3.8+

Internet: Required for first-time model download

Recommended

Processor: Intel i7 or higher

GPU: NVIDIA GPU with CUDA

RAM: 16 GB+

Storage: 5 GB+

🧩 Applications

Retail customer traffic analysis

Smart building and facility management

Event and stadium crowd control

Public transport monitoring

Safety and occupancy limit enforcement

💡 Advantages

Lightweight and easy to deploy

Customizable parameters (line position, sensitivity, model type)

Works with both recorded videos and live camera feeds

Provides interpretable, visual results through annotated outputs

⚠️ Limitations

Reduced accuracy in poor lighting or crowded conditions

Requires proper camera placement for optimal results

Processing may not be real-time on lower-end CPUs

🚀 Future Enhancements

Integration with DeepSORT or ByteTrack for advanced tracking

Database logging for analytical data storage

Web dashboard for real-time visual analytics

Heatmap generation to visualize high-traffic zones

Edge AI optimization for IoT deployment

🧠 Troubleshooting Summary
Issue	Likely Cause	Suggested Fix
No detections	Low lighting or high confidence threshold	Improve lighting or reduce threshold
False positives	Low confidence threshold	Increase threshold or use larger YOLO model
ID switching	Tracker losing objects	Increase patience or use DeepSORT
Slow processing	High resolution or CPU usage	Lower resolution or enable GPU
Video not loading	Invalid path or codec	Verify video source and format
📘 Terminology Summary Table
Term	Description
YOLO (You Only Look Once)	Real-time object detection algorithm predicting multiple objects in one pass.
Object Detection	Identifying and classifying objects within an image or video frame.
Centroid Tracking	Tracks object positions based on their geometric center (centroid).
Line Crossing Detection	Counts objects that cross a predefined virtual line.
Confidence Threshold	Minimum confidence level for a detection to be valid.
Bounding Box	Rectangular outline marking detected object location.
Frame	A single still image in a video sequence.
FPS (Frames Per Second)	Number of frames processed each second, indicating speed.
Tracker Patience	Number of frames an ID remains active after disappearing.
Model Variant	Different YOLO model versions optimized for speed or accuracy.
Detection Class	Object category identified by the model (e.g., person, car).
Euclidean Distance	Formula to measure distance between two centroid points.
Output Video	Annotated video showing bounding boxes and counts.
Input Source	The video file or live feed analyzed by the system.
🧾 License

This project is provided as-is for both educational and commercial purposes.
Users are free to modify, extend, and distribute it under open terms.

👨‍💻 Author

Developed by: Computer Vision Expert
Date: October 2025
Purpose: Real-world people counting solution using deep learning and vision-based tracking.