import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self, detection_confidence=0.7, tracking_confidence=0.7):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            max_num_hands=1,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.mpDraw = mp.solutions.drawing_utils

    def find_hand(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def get_position(self, img):
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[0]
            h, w, _ = img.shape
            lm = myHand.landmark[8]  # Index finger tip
            cx, cy = int(lm.x * w), int(lm.y * h)
            return cx, cy
        return None
