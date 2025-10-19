from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np


class CentroidTracker:
    def __init__(self, max_disappeared=40):
        # Initialize the next unique object ID
        self.next_object_id = 0
        
        # Dictionary mapping object ID to centroid
        # Example: {0: (150, 200), 1: (300, 400)}
        self.objects = OrderedDict()
        
        # Dictionary tracking how many frames each object has been missing
        # Example: {0: 0, 1: 5}  # Object 1 missing for 5 frames
        self.disappeared = OrderedDict()
        
        # Maximum frames an object can be missing
        self.max_disappeared = max_disappeared
        
        # Store tracking history for line crossing detection
        # Example: {0: [(100,150), (105,155), (110,160)]}
        self.track_history = {}
    
    def register(self, centroid):
    
        # Store the centroid with the next available object ID
        self.objects[self.next_object_id] = centroid
        
        # Initialize disappearance counter to 0 (object is visible)
        self.disappeared[self.next_object_id] = 0
        
        # Start tracking history with initial position
        self.track_history[self.next_object_id] = [centroid]
        
        # Increment ID counter for next new object
        self.next_object_id += 1
    
    def deregister(self, object_id):
        del self.objects[object_id]
        del self.disappeared[object_id]
        del self.track_history[object_id]
    
    def update(self, rects):

        # CASE 1: No detections in current frame
        if len(rects) == 0:
            for object_id in list(self.disappeared.keys()):
                self.disappeared[object_id] += 1
                
                # If object has been missing for too long, deregister it
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)
            
            # Return current state (even with no detections)
            return self.objects
        
        
        # Compute centroids for all input bounding boxes
        
        input_centroids = np.zeros((len(rects), 2), dtype="int")
        
        for (i, (x1, y1, x2, y2)) in enumerate(rects):
            cX = int((x1 + x2) / 2.0)
            cY = int((y1 + y2) / 2.0)
            input_centroids[i] = (cX, cY)
        
        
        # No objects currently being tracked
        if len(self.objects) == 0:
            # Register all detections as new objects
            for i in range(0, len(input_centroids)):
                self.register(input_centroids[i])
        
        
        # Match existing objects to new detections
        else:
            object_ids = list(self.objects.keys())
            object_centroids = list(self.objects.values())
            D = dist.cdist(np.array(object_centroids), input_centroids)
            rows = D.min(axis=1).argsort()
            cols = D.argmin(axis=1)[rows]
            used_rows = set()
            used_cols = set()
            
            
            # Match existing objects to detections
            for (row, col) in zip(rows, cols):
                if row in used_rows or col in used_cols:
                    continue
                object_id = object_ids[row]
                self.objects[object_id] = input_centroids[col]
                
                # Append to tracking history
                self.track_history[object_id].append(tuple(input_centroids[col]))
                
                # Keep only recent history (last 50 positions)
                if len(self.track_history[object_id]) > 50:
                    self.track_history[object_id].pop(0)
                
                # Reset disappeared counter (object was found)
                self.disappeared[object_id] = 0
                
                # Mark this row and column as used
                used_rows.add(row)
                used_cols.add(col)
            
            
            # Handle unmatched existing objects (disappeared)
            unused_rows = set(range(0, D.shape[0])).difference(used_rows)
            
            for row in unused_rows:
                object_id = object_ids[row]
                self.disappeared[object_id] += 1
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)
            
            
            # Register new objects
            unused_cols = set(range(0, D.shape[1])).difference(used_cols)
            
            for col in unused_cols:
                self.register(input_centroids[col])
        return self.objects


# Test the tracker(optional)
if __name__ == "__main__":
    print("CentroidTracker class loaded successfully!")
    print("This file should be imported by people_counter.py")
    print("\nTo use:")
    print("  from CentroidTracker import CentroidTracker")
    print("  tracker = CentroidTracker(max_disappeared=40)")
