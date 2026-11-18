import cv2
import pyttsx3
import time
import serial
import os
import requests
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from groq import Groq

# --- 0. AUTO-DOWNLOAD THE AI MODEL ---
model_path = 'hand_landmarker.task'
if not os.path.exists(model_path):
    url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
    response = requests.get(url)
    with open(model_path, 'wb') as f:
        f.write(response.content)

# --- 1. INITIALIZE GROQ AI ---
# Paste your actual Groq API Key here
client = Groq(api_key="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")

# --- 2. INITIALIZE ARDUINO (Smart Detect) ---
arduino = None
try:
    # IMPORTANT: Change 'COM3' to whatever port your Arduino uses when plugged in!
    arduino = serial.Serial('COM3', 9600, timeout=1) 
    print("Hardware Connected Successfully!")
    time.sleep(2)
except Exception as e:
    print("Hardware not detected. Running in Software-Only Mode for now!")

# --- 3. INITIALIZE NEW MEDIAPIPE TASKS API ---
base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=1)
detector = vision.HandLandmarker.create_from_options(options)

cooldown_time = 0 

def ask_groq(prompt_text):
    print(f"\n[Prompting AI]: {prompt_text}")
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt_text}],
            model="openai/gpt-oss-20b", # <-- ACTIVE 2026 MODEL
        )
        return chat_completion.choices[0].message.content.strip().upper()
    except Exception as e:
        return f"API ERROR: {e}"

def output_response(text):
    print(f"[AI Replies]: {text}")
    
    if arduino is not None:
        try:
            arduino.write((text + '\n').encode('utf-8'))
        except Exception as e:
            print("Serial error.")
            
    # Initialize a fresh audio engine every single time so it never freezes
    engine = pyttsx3.init()
    engine.setProperty('rate', 140)
    engine.say(text)
    engine.runAndWait()

# Custom Drawing Function
def draw_landmarks(image, hand_landmarks):
    h, w, c = image.shape
    for landmark in hand_landmarks:
        x, y = int(landmark.x * w), int(landmark.y * h)
        cv2.circle(image, (x, y), 5, (0, 255, 0), -1)

cap = cv2.VideoCapture(0) # Change 0 to DroidCam URL if using phone
print("System Ready. Waiting for hand gestures...")

while True:
    success, img = cap.read()
    if not success:
        break
        
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
    
    detection_result = detector.detect(mp_image)

    if detection_result.hand_landmarks:
        hand_landmarks = detection_result.hand_landmarks[0]
        draw_landmarks(img, hand_landmarks)
        
        fingertips = [8, 12, 16, 20]
        fingers_up = 0
        
        for tip in fingertips:
            if hand_landmarks[tip].y < hand_landmarks[tip - 2].y:
                fingers_up += 1
                
        if time.time() - cooldown_time > 5:
            response = ""
            
            if fingers_up == 0: # CLOSED FIST
                # Meaning: "Stop" or "Emergency"
                response = ask_groq("The user made a closed fist sign. Translate this into a 2-word alert like 'STOP NOW' or 'NEED HELP'. No punctuation.")
                cooldown_time = time.time()
                
            elif fingers_up == 2: # PEACE SIGN
                # Meaning: "Peace" or "Friendship"
                response = ask_groq("The user made a peace sign. Translate this into a short 2-word phrase like 'PEACE OUT' or 'HELLO FRIEND'. No punctuation.")
                cooldown_time = time.time()

            elif fingers_up == 5: # OPEN HAND
                # Meaning: "Hello" or "Stop"
                response = ask_groq("The user waved an open hand. Translate this into a short 2-word greeting like 'HI THERE'. No punctuation.")
                cooldown_time = time.time()

            elif fingers_up == 1: # ONE FINGER (Pointer)
                response = ask_groq("The user held up one finger. Translate this to a 2-word phrase like 'WAIT PLEASE' or 'ATTENTION'. No punctuation.")
                cooldown_time = time.time()
                
            elif fingers_up == 3: # THREE FINGERS
                response = ask_groq("The user held up three fingers. Translate this to a 2-word phrase like 'I PROMISE' or 'EXCELLENT WORK'. No punctuation.")
                cooldown_time = time.time()
                
            elif fingers_up == 4: # FOUR FINGERS
                response = ask_groq("The user held up four fingers. Translate this to a 2-word phrase like 'ALMOST THERE' or 'FOUR ITEMS'. No punctuation.")
                cooldown_time = time.time()

            if response != "":
                output_response(response)

    cv2.imshow("Bidirectional AI Communicator", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()