# Bidirectional AI Communicator 🤖✋

A real-time, edge-AI gesture-to-text and speech translator. This project bridges the communication gap by tracking hand gestures through a standard webcam, classifying them using advanced Euclidean geometry, and generating context-aware conversational responses using a Large Language Model (Llama-3.1). The response is spoken aloud via a Text-to-Speech (TTS) engine and physically displayed on an Arduino-controlled LCD screen.

## ✨ Features
*   **Real-Time Computer Vision:** Utilizes Google's MediaPipe for lightweight, 21-point 3D hand tracking.
*   **Geometric Pose Classification:** Identifies 5 core gestures (Peace, Fist, OK, Thumbs Up, Open Hand) using custom Euclidean math without needing a heavy ML classifier.
*   **LLM Integration:** Uses the Groq Cloud API (Llama-3.1-8b) to translate rigid gestures into fluid, natural language responses.
*   **Multimodal Output:** Translates gestures into audio (via `pyttsx3`) and text (via physical LCD).
*   **Hardware Edge Display:** PC-to-Arduino serial communication pushes AI responses to a 16x2 I2C LCD.

## 🛠️ Hardware Requirements & Wiring
*   1x Arduino Uno R3
*   1x 16x2 Character LCD Display
*   1x PCF8574 I2C Backpack (Soldered to the back of the LCD)
*   4x Jumper Wires (Female-to-Male)
*   1x Webcam / PC Camera

### I2C LCD to Arduino Wiring:
| I2C Backpack Pin | Arduino Uno Pin |
| :--- | :--- |
| **GND** | GND |
| **VCC** | 5V |
| **SDA** | A4 (Analog 4) |
| **SCL** | A5 (Analog 5) |

*(Note: If the LCD lights up blue but shows no text, adjust the contrast using the blue potentiometer screw on the back of the I2C module.)*

## 💻 Software Setup

### 1. Arduino Firmware
1. Open `receiver.ino` in the Arduino IDE.
2. Install the `LiquidCrystal_I2C` library (by Frank de Brabander).
3. Connect your Arduino via USB and select the correct COM port.
4. Click **Upload**. 

### 2. Python Environment
Ensure you have Python 3.8+ installed. Install the required dependencies:
```bash
pip install opencv-python pyttsx3 pyserial requests mediapipe groq
```

### 3. API Key Configuration
This project requires a free Groq API key for the LLM processing.
1. Get an API key from [Groq Cloud](https://console.groq.com/).
2. Open `app.py`.
3. Locate line 22 and paste your API key:
   ```python
   client = Groq(api_key="YOUR_GROQ_API_KEY_HERE")
   ```

## 🚀 Usage
1. Ensure your Arduino is plugged in.
2. Check `app.py` (Line 29) to ensure the `COM` port matches your Arduino (e.g., `'COM3'`).
3. Run the Python application:
   ```bash
   python app.py
   ```
4. Wait for the terminal to display `"System Ready. Waiting for hand gestures..."`
5. Hold up a gesture (e.g., Peace Sign, Fist, Thumbs Up) to your webcam.
6. The AI will speak the translation, and it will appear on the Arduino LCD screen!

## 📂 Project Structure
*   `app.py`: The main Python application (Vision + AI + Serial TX).
*   `receiver.ino`: The Arduino firmware (Serial RX + I2C LCD Display).
*   `Microprocessor Report.pdf`: Academic project documentation.

## 🎓 Academic Credit
Developed for the Microprocessor (UCS7103) laboratory assessment. 
**Session:** 2026 - 2027