import pickle
import cv2
import mediapipe as mp
import numpy as np
import pyttsx3
from collections import deque, Counter
import time


model_dict = pickle.load(open('./model_final.p', 'rb'))
model = model_dict['model']

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.7)

labels_dict = {
    0: 'A',  1: 'B',  2: 'C',  3: 'D',  4: 'E',
    5: 'F',  6: 'G',  7: 'H',  8: 'I',  9: 'J',
    10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O',
    15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T',
    20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y',
    25: 'Z'
}


word = ""
hands_down = False
predictions = deque(maxlen=30)  # Store the last 30 predictions to stabilize output
CONFIDENCE_THRESHOLD = 0.4  # Increase confidence threshold for predictions
MINIMUM_COUNT = 7  # Increase the count required for character stabilization
hands_down_start_time = None  # Track the time when hands go down
HANDS_DOWN_DURATION = 1.5  # Minimum time in seconds that hands must be down to confirm the word
last_character = None  # Track the last added character
character_cooldown_start_time = None  # Track time to debounce character detection
CHARACTER_COOLDOWN = 1.2  # Slightly increase cooldown period to prevent rapid character appending

while True:
    data_aux = []
    x_ = []
    y_ = []

    ret, frame = cap.read()
    if not ret:
        break  

    H, W, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    
    num_hands_detected = len(results.multi_hand_landmarks) if results.multi_hand_landmarks else 0

    if num_hands_detected > 0:
        hands_down = False  
        hands_down_start_time = None  # Reset hands down timer
        
        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y

                x_.append(x)
                y_.append(y)

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))

        if num_hands_detected == 1:
            data_aux.extend([0] * 42)  

        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, 
                hand_landmarks,  
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )

        if len(data_aux) == 84:
            prediction = model.predict([np.asarray(data_aux)])
            prediction_prob = model.predict_proba([np.asarray(data_aux)])
            predicted_character = labels_dict[int(prediction[0])]
            confidence = max(prediction_prob[0])  
            
            if confidence > CONFIDENCE_THRESHOLD:
                predictions.append(predicted_character)

                if len(predictions) == predictions.maxlen:
                    char_counts = Counter(predictions)
                    most_common_char, count = char_counts.most_common(1)[0]
                    
                    if count >= MINIMUM_COUNT and (most_common_char != last_character or (time.time() - character_cooldown_start_time > CHARACTER_COOLDOWN if character_cooldown_start_time else True)):
                        word += most_common_char
                        last_character = most_common_char
                        character_cooldown_start_time = time.time()  

                x1 = int(min(x_) * W) - 10
                y1 = int(min(y_) * H) - 10
                x2 = int(max(x_) * W) + 10
                y2 = int(max(y_) * H) + 10

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
                cv2.putText(frame, predicted_character + f" ({confidence:.2f})", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 255), 3, cv2.LINE_AA)

    else:
        if not hands_down:
            hands_down_start_time = time.time() if hands_down_start_time is None else hands_down_start_time
            
            if time.time() - hands_down_start_time > HANDS_DOWN_DURATION:
                if word:  
                    print("Word formed:", word)
                    speak(word) 
                    word = ""  
                    predictions.clear()  
                hands_down = True  

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()