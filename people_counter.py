import cv2
import numpy as np
from ultralytics import YOLO
from CentroidTracker import CentroidTracker
import time
import os

def count_people_video(video_path, output_path="output_people_counter.mp4"):
    print("\n" + "="*70)
    print("PEOPLE COUNTER - YOLO + CENTROID TRACKER")
    print("="*70 + "\n")
    
    # Initialize YOLO Model
    print("[STEP 1/7] Loading YOLO model...")
    try:
        # Load YOLOv8 nano model (fastest, good for real-time)
        # Model will auto-download on first run (~6MB)
        model = YOLO('yolov8n.pt')
        print("✓ YOLO model loaded successfully!")
    except Exception as e:
        print(f"✗ Error loading YOLO model: {e}")
        print("Tip: Make sure you have internet connection for first-time download")
        return None
    
    
    # Initialize Video Capture
    print(f"\n[STEP 2/7] Opening video file: {video_path}")
    
    if not os.path.exists(video_path):
        print(f"✗ Error: Video file not found at '{video_path}'")
        print(f"Tip: Make sure the video file exists in the same folder")
        return None
    
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"✗ Error: Could not open video file")
        return None
    
    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"✓ Video opened successfully!")
    print(f"  - Resolution: {width}x{height}")
    print(f"  - FPS: {fps}")
    print(f"  - Total frames: {total_frames}")
    print(f"  - Duration: {total_frames/fps:.1f} seconds")
    
    
    # Initialize Video Writer
    print(f"\n[STEP 3/7] Setting up output video: {output_path}")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    if not out.isOpened():
        print(f"✗ Error: Could not create output video file")
        cap.release()
        return None
    print(f"✓ Output video writer ready!")
    
    # Initialize Centroid Tracker
    print(f"\n[STEP 4/7] Initializing Centroid Tracker...")
    ct = CentroidTracker(max_disappeared=40)
    print(f"✓ Tracker initialized (max_disappeared=40)")

    # Set Up Counting Variables
    print(f"\n[STEP 5/7] Setting up counting system...")
    
    # Define counting line (horizontal line in middle of frame)
    line_y = height // 2
    print(f"✓ Counting line set at y={line_y} (middle of frame)")
    
    # Counters
    people_in = 0
    people_out = 0
    
    # Track which IDs have already been counted
    already_counted = set()
    
    print(f"✓ Counters initialized")

    # Process Video Frame by Frame
    print(f"\n[STEP 6/7] Processing video...")
    print(f"This may take a few minutes depending on video length...\n")
    
    frame_count = 0
    start_time = time.time()
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("\n[INFO] End of video reached")
            break
        frame_count += 1
        
        # Run YOLO Detection
        # Detect only "person" class (class 0 in COCO dataset)
        results = model.predict(
            frame,
            classes=[0],        
            conf=0.4,           
            verbose=False       
        )
        
        # Extract Bounding Boxes
        boxes = []
        if results and len(results[0].boxes) > 0:
            # Get bounding box coordinates [x1, y1, x2, y2]
            boxes_data = results[0].boxes.xyxy.cpu().numpy()
            
            for box in boxes_data:
                x1, y1, x2, y2 = box[:4]
                boxes.append((int(x1), int(y1), int(x2), int(y2)))
        
        
        # Update Tracker
        objects = ct.update(boxes)
        
        # Draw Counting Line
        cv2.line(frame, (0, line_y), (width, line_y), 
                 (0, 255, 255), 3)
        
        # Add line label
        cv2.putText(frame, "COUNTING LINE", (width//2 - 100, line_y - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        
        # Track Each Object and Count Line Crossings
        for object_id, centroid in objects.items():
            # Get tracking history
            track = ct.track_history[object_id]
            
            # Need at least 2 points to detect movement
            if len(track) >= 2:
                prev_y = track[-2][1]
                curr_y = track[-1][1]
                
                # Check if object crossed the line and hasn't been counted yet
                if object_id not in already_counted:
                    
                    # Crossing from top to bottom: enter
                    if prev_y < line_y and curr_y >= line_y:
                        people_in += 1
                        already_counted.add(object_id)
                        print(f"✓ [IN]  Person ID {object_id} entered | Total IN: {people_in}")
                    
                    # Crossing from bottom to top: exit
                    elif prev_y > line_y and curr_y <= line_y:
                        people_out += 1
                        already_counted.add(object_id)
                        print(f"✓ [OUT] Person ID {object_id} exited  | Total OUT: {people_out}")
            
            
            # Draw Annotations
            cv2.circle(frame, centroid, 5, (0, 255, 0), -1)
            
            # Draw ID label above centroid
            text = f"ID {object_id}"
            cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 15),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Draw bounding box
            for (x1, y1, x2, y2) in boxes:
                box_center_x = (x1 + x2) // 2
                box_center_y = (y1 + y2) // 2
                if abs(box_center_x - centroid[0]) < 10 and abs(box_center_y - centroid[1]) < 10:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    break
            
            # Draw tracking trail (last 10 positions)
            if len(track) > 1:
                points = np.array(track[-10:], dtype=np.int32)
                cv2.polylines(frame, [points], False, (0, 200, 255), 2)
        
        
        # Display Counters and Info and creating semi-transparent overlay for counters
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (350, 150), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        
        # Display IN counter: grn
        cv2.putText(frame, f"IN: {people_in}", (10, 45),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
        
        # Display OUT counter: rd
        cv2.putText(frame, f"OUT: {people_out}", (10, 100),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
        
        # Display net count
        net_count = people_in - people_out
        cv2.putText(frame, f"NET: {net_count}", (10, 145),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        # Display frame counter:TR
        cv2.putText(frame, f"Frame: {frame_count}/{total_frames}", 
                   (width - 280, 35),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Calculate and display FPS
        elapsed_time = time.time() - start_time
        current_fps = frame_count / elapsed_time if elapsed_time > 0 else 0
        cv2.putText(frame, f"FPS: {current_fps:.1f}", 
                   (width - 280, 70),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Display active tracks
        cv2.putText(frame, f"Active Tracks: {len(objects)}", 
                   (width - 280, 105),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        out.write(frame)
        
        # Progress indicator
        if frame_count % 30 == 0:
            progress = (frame_count / total_frames) * 100
            print(f"[PROGRESS] {progress:.1f}% | Frame {frame_count}/{total_frames} | "
                  f"IN: {people_in} | OUT: {people_out} | FPS: {current_fps:.1f}")
    
    
    # Clean Up and Save Results
    print(f"\n[STEP 7/7] Finalizing...")
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
    end_time = time.time()
    processing_time = end_time - start_time
    print("\n" + "="*70)
    print("FINAL STATISTICS")
    print("="*70)
    print(f"✓ People Entered (IN):        {people_in}")
    print(f"✓ People Exited (OUT):        {people_out}")
    print(f"✓ Net Count (IN - OUT):       {people_in - people_out}")
    print(f"✓ Total Frames Processed:     {frame_count}")
    print(f"✓ Processing Time:            {processing_time:.2f} seconds")
    print(f"✓ Average FPS:                {frame_count / processing_time:.2f}")
    print(f"✓ Output Video Saved:         {output_path}")
    print("="*70 + "\n")
    
    return {
        'people_in': people_in,
        'people_out': people_out,
        'net_count': people_in - people_out,
        'frames_processed': frame_count,
        'processing_time': processing_time,
        'avg_fps': frame_count / processing_time
    }


if __name__ == "__main__":
    print("\n" + "*"*70)
    print("PEOPLE COUNTER - SETUP")
    print("*"*70)
    
    # Input video path
    video_path = "test_vid_2.mp4"
    
    # Output video path
    output_path = "output_people_counter_2.mp4"
    
    print(f"\nInput video:  {video_path}")
    print(f"Output video: {output_path}")

    if not os.path.exists(video_path):
        print("\n" + "!"*70)
        print("ERROR: Video file not found!")
        print("!"*70)
        print(f"\nThe file '{video_path}' does not exist.")
        print("\nPLEASE DO ONE OF THE FOLLOWING:")
        print("1. Place your video file in the same folder as this script")
        print("2. Rename your video to 'mall_entrance.mp4'")
        print("3. Or change the 'video_path' variable above to match your filename")
        print("\nExample:")
        print("  video_path = 'my_video.mp4'")
        print("  video_path = 'C:/Videos/entrance.mp4'  # Full path")
        print("\n" + "!"*70)
    else:
        stats = count_people_video(video_path, output_path)
        
        if stats:
            print("\n✓ SUCCESS! Processing completed.")
            print(f"\nYou can now open '{output_path}' to see the results!")
        else:
            print("\n✗ FAILED! Check the error messages above.")
