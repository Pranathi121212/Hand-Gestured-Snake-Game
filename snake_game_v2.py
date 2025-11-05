import cv2
import numpy as np
import mediapipe as mp
import pygame
import random
import os
import math

# silence TensorFlow logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# ---------------- Hand Detector ---------------- #
class HandDetector:
    def __init__(self, detection_confidence=0.7, tracking_confidence=0.7):
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.results = None

    def find_hand(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks and draw:
            for handLms in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    img, handLms, mp.solutions.hands.HAND_CONNECTIONS)
        return img

    def get_position(self, img):
        if self.results and self.results.multi_hand_landmarks:
            h, w, _ = img.shape
            hand = self.results.multi_hand_landmarks[0]
            lm = hand.landmark[8]  # index-finger tip
            return int(lm.x * w), int(lm.y * h)
        return None

# ---------------- Snake Game ---------------- #
def main():
    # camera
    cap = cv2.VideoCapture(0)
    detector = HandDetector()

    # pygame setup
    pygame.init()
    width, height = 960, 720
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("🐍 Hand-Controlled Snake – Fun Edition")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Comic Sans MS", 32, bold=True)

    # sounds
    eat_sound = None
    try:
        pygame.mixer.init()
        eat_sound = pygame.mixer.Sound(pygame.mixer.Sound.get_raw.__doc__ or "")
    except Exception:
        pass  # skip if sound fails

    # colors
    BG_COLOR = (10, 10, 30)
    SNAKE_COLORS = [(0, 255, 0), (0, 180, 255), (255, 255, 0), (255, 0, 255)]
    RED = (255, 80, 80)
    WHITE = (255, 255, 255)

    # snake setup
    snake_pos = [[100, 50]]
    snake_length = 10
    score = 0
    food_pos = [random.randint(100, width - 100), random.randint(100, height - 100)]
    food_size = 20
    smooth_x, smooth_y = 0, 0
    trail_color_index = 0

    # difficulty progression
    base_speed = 30
    level = 1

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        success, img = cap.read()
        if not success:
            continue
        img = cv2.flip(img, 1)
        img = detector.find_hand(img)
        pos = detector.get_position(img)

        if pos:
            x, y = pos
            x = np.interp(x, [0, 640], [0, width])
            y = np.interp(y, [0, 480], [0, height])

            smooth_x = 0.75 * smooth_x + 0.25 * x
            smooth_y = 0.75 * smooth_y + 0.25 * y

            snake_pos.append([smooth_x, smooth_y])
            if len(snake_pos) > snake_length:
                del snake_pos[0]

        # collision with food
        if pos and math.dist((smooth_x, smooth_y), food_pos) < 25:
            food_pos = [random.randint(50, width - 50), random.randint(50, height - 50)]
            snake_length += 5
            score += 1
            level = 1 + score // 5
            base_speed = min(60, 30 + score // 2)
            trail_color_index = (trail_color_index + 1) % len(SNAKE_COLORS)
            if eat_sound:
                eat_sound.play()

        # collision with self
        head = snake_pos[-1]
        for block in snake_pos[:-10]:
            if math.dist(head, block) < 10:
                score = 0
                snake_pos = [[100, 50]]
                snake_length = 10

        # draw
        win.fill(BG_COLOR)

        # snake trail color shift
        for i, block in enumerate(snake_pos):
            color = SNAKE_COLORS[(trail_color_index + i // 10) % len(SNAKE_COLORS)]
            pygame.draw.circle(win, color, (int(block[0]), int(block[1])), 10)

        pygame.draw.rect(win, RED, [food_pos[0], food_pos[1], food_size, food_size])

        score_text = font.render(f"Score: {score}", True, WHITE)
        level_text = font.render(f"Level: {level}", True, (200, 200, 255))
        win.blit(score_text, (10, 10))
        win.blit(level_text, (10, 50))

        pygame.display.update()
        clock.tick(base_speed)

        cv2.imshow("Hand Tracking", img)
        if cv2.waitKey(1) & 0xFF == 27:
            running = False

    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()

if __name__ == "__main__":
    main()
