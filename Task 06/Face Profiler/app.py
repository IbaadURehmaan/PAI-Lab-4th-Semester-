from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import cv2
import os
import time

app = Flask(__name__)

# Absolute path set kiya hai taake image save/load hone mein koi error na aaye
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 16 Personality Types mapping
PERSONALITIES = {
    "INTJ": "The Architect - Strategic and logical thinkers.",
    "INTP": "The Logician - Innovative inventors with an unquenchable thirst for knowledge.",
    "ENTJ": "The Commander - Bold, imaginative and strong-willed leaders.",
    "ENTP": "The Debater - Smart and curious thinkers who cannot resist an intellectual challenge.",
    "INFJ": "The Advocate - Quiet and mystical, yet very inspiring and tireless idealists.",
    "INFP": "The Mediator - Poetic, kind and altruistic people.",
    "ENFJ": "The Protagonist - Charismatic and inspiring leaders.",
    "ENFP": "The Campaigner - Enthusiastic, creative and sociable free spirits.",
    "ISTJ": "The Logistician - Practical and fact-minded individuals.",
    "ISFJ": "The Defender - Very dedicated and warm protectors.",
    "ESTJ": "The Executive - Excellent administrators.",
    "ESFJ": "The Consul - Extraordinarily caring, social and popular people.",
    "ISTP": "The Virtuoso - Bold and practical experimenters.",
    "ISFP": "The Adventurer - Flexible and charming artists.",
    "ESTP": "The Entrepreneur - Smart, energetic and very perceptive people.",
    "ESFP": "The Entertainer - Spontaneous, energetic and enthusiastic people."
}

def analyze_face(image_path):
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    
    if os.path.exists('haarcascade_frontalface_default.xml'):
        cascade_path = 'haarcascade_frontalface_default.xml'
        
    face_cascade = cv2.CascadeClassifier(cascade_path)
    
    img = cv2.imread(image_path)
    if img is None:
        return None, "Invalid image format or file corrupted.", "", 0, 0

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=6, minSize=(30, 30))
    
    if len(faces) == 0:
        return None, "No face detected. Please try another image with a clear, front-facing face.", "", 0, 0

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 255), 3)
        
        # Naya Logic: Face ki position, size aur average color ko mix kar ke random result generate karega
        face_roi = gray[y:y+h, x:x+w]
        mean_color = cv2.mean(face_roi)[0]
        
        # Is algorithm se har alag shakal par completely alag result aayega
        magic_number = int(x + y + (w * h) + mean_color)
        
        keys = list(PERSONALITIES.keys())
        index = magic_number % 16 
        ptype = keys[index]
        desc = PERSONALITIES[ptype]

        # Dynamic Stats (Taake real lage)
        confidence = 75 + (magic_number % 22)  # Generates a number between 75 and 96
        symmetry = 70 + ((magic_number // 5) % 25) # Generates a number between 70 and 94

        # Unique filename taake browser caching ka issue na aaye aur image display ho
        unique_id = str(int(time.time()))
        output_filename = f"processed_{unique_id}.png"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        cv2.imwrite(output_path, img)
        
        return output_filename, ptype, desc, confidence, symmetry

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error="No file uploaded.")
        
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error="No selected file.")
            
        if file:
            filename = secure_filename(file.filename)
            # Har upload ko bhi unique naam de rahe hain
            unique_upload_name = f"raw_{int(time.time())}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_upload_name)
            file.save(filepath)
            
            output_img, ptype, desc, conf, sym = analyze_face(filepath)
            
            if output_img:
                return render_template('index.html', ptype=ptype, desc=desc, image_url=output_img, confidence=conf, symmetry=sym)
            else:
                return render_template('index.html', error=ptype)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)