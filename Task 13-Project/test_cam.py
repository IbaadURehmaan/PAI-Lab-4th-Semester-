import cv2

print("Trying to open camera...")
cap = cv2.VideoCapture(0) # Try changing this to 1 or 2 if it fails

if not cap.isOpened():
    print("ERROR: Could not open camera.")
else:
    print("Camera opened successfully! Press 'q' to close.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("ERROR: Cannot read frame.")
            break
        
        cv2.imshow('Raw Camera Test', frame)
        
        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()