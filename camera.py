import cv2
import numpy as np

def detect_mask_color(face_region):
    """Simple mask detection using color analysis"""
    if face_region.size == 0:
        return False, 0
    
    # Convert to HSV
    hsv = cv2.cvtColor(face_region, cv2.COLOR_BGR2HSV)
    
    # Mask color ranges
    # Blue masks
    blue_mask = cv2.inRange(hsv, np.array([100, 50, 50]), np.array([130, 255, 255]))
    # White masks  
    white_mask = cv2.inRange(hsv, np.array([0, 0, 200]), np.array([180, 30, 255]))
    # Black masks
    black_mask = cv2.inRange(hsv, np.array([0, 0, 0]), np.array([180, 255, 50]))
    
    # Combine all masks
    combined = cv2.bitwise_or(blue_mask, white_mask)
    combined = cv2.bitwise_or(combined, black_mask)
    
    # Calculate percentage
    mask_pixels = cv2.countNonZero(combined)
    total_pixels = face_region.shape[0] * face_region.shape[1]
    percentage = (mask_pixels / total_pixels) * 100 if total_pixels > 0 else 0
    
    return percentage > 15, percentage

print("=== Face Mask Detection System ===")
print(f"OpenCV Version: {cv2.__version__}")

# Initialize camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Camera nahi khul raha!")
    print("Solutions:")
    print("1. Camera USB properly connected hai?")
    print("2. Dusre apps camera use kar rahe to band karo")
    print("3. Camera permissions check karo")
    exit()

# Load face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

print("\n✅ System Ready!")
print("📹 Camera started successfully")
print("👥 Face detection activated")
print("😷 Mask detection enabled")
print("\nControls:")
print("- Press 'q' to quit")
print("- Press 's' to take screenshot")

screenshot_count = 0

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Frame capture failed!")
        break
    
    # Detect faces
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
    
    mask_count = 0
    
    # Process each face
    for (x, y, w, h) in faces:
        # Extract face region
        face_region = frame[y:y+h, x:x+w]
        
        # Detect mask
        has_mask, confidence = detect_mask_color(face_region)
        
        if has_mask:
            color = (0, 255, 0)  # Green
            label = f"MASK ({confidence:.1f}%)"
            mask_count += 1
        else:
            color = (0, 0, 255)  # Red
            label = f"NO MASK ({100-confidence:.1f}%)"
        
        # Draw rectangle and label
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 3)
        cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    
    # Display statistics
    cv2.putText(frame, f"Faces: {len(faces)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(frame, f"With Mask: {mask_count}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.putText(frame, f"Without Mask: {len(faces)-mask_count}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    cv2.putText(frame, "Press 'q' to quit, 's' for screenshot", (10, frame.shape[0]-20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
    # Show frame
    cv2.imshow('Face Mask Detection System', frame)
    
    # Handle key presses
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        screenshot_count += 1
        filename = f"screenshot_{screenshot_count}.jpg"
        cv2.imwrite(filename, frame)
        print(f"📸 Screenshot saved: {filename}")

# Cleanup
cap.release()
cv2.destroyAllWindows()
print("\n✅ Program ended successfully!")
print(f"📸 Total screenshots taken: {screenshot_count}")