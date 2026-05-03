import cv2
import threading
import time
from flask import Flask, render_template, Response

app = Flask(__name__)

face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')

# Global variables
blink_count = 0
closed_frames = 0
current_frame = None

# Timer variable to track the exact moment of the last blink
last_blink_time = time.time()

MIN_FRAMES = 2
MAX_FRAMES = 12 
MAX_STARE_SECONDS = 7  # If you don't blink for 7 seconds, trigger the warning!

def process_webcam_in_background():
    global blink_count, closed_frames, current_frame, last_blink_time
    
    camera = cv2.VideoCapture(0)

    while True:
        success, frame = camera.read()
        if not success:
            continue
            
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        eyes_detected = False

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 255), 1)
            
            top_half_y = int(h * 0.55)
            roi_gray = gray[y:y+top_half_y, x:x+w]
            roi_color = frame[y:y+top_half_y, x:x+w]
            
            eyes = eye_detector.detectMultiScale(roi_gray, 1.1, 3)

            if len(eyes) > 0:
                eyes_detected = True
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

        # --- BLINK & TIMER LOGIC ---
        if len(faces) > 0:
            if not eyes_detected:
                closed_frames += 1
            else:
                if closed_frames >= MIN_FRAMES and closed_frames <= MAX_FRAMES:
                    blink_count += 1
                    last_blink_time = time.time()  # Reset the stare timer on a successful blink!
                closed_frames = 0 
        else:
            closed_frames += 1

        # Calculate how long it has been since the last blink
        time_since_blink = time.time() - last_blink_time

        # --- WARNING OVERLAYS ---
        if closed_frames > MAX_FRAMES:
            # Face/Eyes missing logic
            status_text = "NOT DETECTED"
            text_color = (0, 0, 255)
            blink_count = 0 
            last_blink_time = time.time()  # Keep resetting timer so it doesn't trigger stare warning while away
            
            cv2.putText(frame, 'WARNING: FACE/EYES MISSING!', (30, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            cv2.putText(frame, 'BLINK COUNT RESET TO 0', (80, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        elif time_since_blink > MAX_STARE_SECONDS:
            # THE NEW STARE TIMER WARNING
            status_text = "STARING DETECTED"
            text_color = (0, 0, 255)
            
            # Create a flashing red screen effect (flashes twice per second)
            if int(time.time() * 2) % 2 == 0:
                cv2.rectangle(frame, (0, 0), (640, 480), (0, 0, 255), 15)  # Thick red border
                cv2.putText(frame, 'BLINK NOW!', (180, 240), cv2.FONT_HERSHEY_DUPLEX, 1.5, (0, 0, 255), 4)
                
        elif not eyes_detected and closed_frames > 0:
            status_text = "Blinking..."
            text_color = (0, 165, 255)
        else:
            # Show the live countdown timer on screen
            time_left = max(0, MAX_STARE_SECONDS - int(time_since_blink))
            status_text = f"Active (Timer: {time_left}s)"
            text_color = (0, 255, 0)

        # Draw dark box for top left text
        cv2.rectangle(frame, (10, 10), (380, 90), (0, 0, 0), -1)
        cv2.putText(frame, f'Status: {status_text}', (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, text_color, 2)
        cv2.putText(frame, f'Total Blinks: {blink_count}', (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        if ret:
            current_frame = buffer.tobytes()

        time.sleep(0.03)

threading.Thread(target=process_webcam_in_background, daemon=True).start()

def stream_to_browser():
    global current_frame
    while True:
        if current_frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + current_frame + b'\r\n')
        time.sleep(0.03)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(stream_to_browser(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True, threaded=True, use_reloader=False)