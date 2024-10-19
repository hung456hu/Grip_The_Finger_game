import cv2
import mediapipe as mp
import math
import random
import time

# Timer class to handle the drawing of the timer bar
class Timer:
    @staticmethod
    def draw_timer_bar(image, start_time, time_limit, bar_position=(50, 50), bar_size=(400, 30)):
        elapsed_time = time.time() - start_time
        remaining_time = max(0, time_limit - elapsed_time)
        bar_fill = int((remaining_time / time_limit) * bar_size[0])

        # Draw the background bar
        cv2.rectangle(image, bar_position, (bar_position[0] + bar_size[0], bar_position[1] + bar_size[1]), (200, 200, 200), -1)

        # Draw the filled portion
        cv2.rectangle(image, bar_position, (bar_position[0] + bar_fill, bar_position[1] + bar_size[1]), (0, 255, 0), -1)

        # Display remaining time
        cv2.putText(image, f'Time Left: {int(remaining_time)}s', (bar_position[0] + 10, bar_position[1] + bar_size[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

# FingerTracking class to handle finger tracking, sequence generation, and distance calculation
class FingerTracking:
    @staticmethod
    def calculate_distance(point1, point2, image_width, image_height):
        x1, y1 = int(point1.x * image_width), int(point1.y * image_height)
        x2, y2 = int(point2.x * image_width), int(point2.y * image_height)
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    @staticmethod
    def generate_unique_sequence(length=5):
        finger_names = ["thumb", "index", "middle", "ring", "pinky"]
        return random.sample(finger_names, length)

# HandTrackingGame class that manages the game loop and instructions
class HandTrackingGame:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.cap = cv2.VideoCapture(0)
        self.instructions_shown = False  # Flag to track if instructions have been shown

    def show_instructions(self):
        instructions = """
      ██████╗ ██████╗ ██╗██████╗     ████████╗██╗  ██╗███████╗    ███████╗██╗███╗   ██╗ ██████╗ ███████╗██████╗ 
     ██╔════╝ ██╔══██╗██║██╔══██╗    ╚══██╔══╝██║  ██║██╔════╝    ██╔════╝██║████╗  ██║██╔════╝ ██╔════╝██╔══██╗
     ██║  ███╗██████╔╝██║██████╔╝       ██║   ███████║█████╗      █████╗  ██║██╔██╗ ██║██║  ███╗█████╗  ██████╔╝
     ██║   ██║██╔══██╗██║██╔═══╝        ██║   ██╔══██║██╔══╝      ██╔══╝  ██║██║╚██╗██║██║   ██║██╔══╝  ██╔══██╗
     ╚██████╔╝██║  ██║██║██║            ██║   ██║  ██║███████╗    ██║     ██║██║ ╚████║╚██████╔╝███████╗██║  ██║
      ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝            ╚═╝   ╚═╝  ╚═╝╚══════╝    ╚═╝     ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝       
    
    Welcome to the Grip the Finger Game!
    Follow the sequence of fingers to fold.
    """
        print(instructions)

    def game_loop(self):
       
        with self.mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
            time_limit = 10
            game_over = False
            sequence = FingerTracking.generate_unique_sequence()
            index = 0
            start_time = time.time()
            loop = 0

            while self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret:
                    break

                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                results = hands.process(image)
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                if not game_over:
                    if results.multi_hand_landmarks:
                        for hand_landmarks in results.multi_hand_landmarks:
                            self.mp_drawing.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                            image_width, image_height = image.shape[1], image.shape[0]
                            folded_fingers = []

                            thumb_tip = hand_landmarks.landmark[4]
                            middle_base = hand_landmarks.landmark[9]
                            distance_thumb_to_middle_base = FingerTracking.calculate_distance(thumb_tip, middle_base, image_width, image_height)
                            thumb_status = "Folded" if distance_thumb_to_middle_base < 40 else "Extended"
                            if thumb_status == "Folded":
                                folded_fingers.append("thumb")

                            fingertip_landmarks = [8, 12, 16, 20]
                            joint_landmarks = [6, 10, 14, 18]
                            finger_names = ["index", "middle", "ring", "pinky"]

                            for i, fingertip in enumerate(fingertip_landmarks):
                                y_tip = int(hand_landmarks.landmark[fingertip].y * image_height)
                                y_joint = int(hand_landmarks.landmark[joint_landmarks[i]].y * image_height)

                                status = "Folded" if y_tip > y_joint else "Extended"
                                if status == "Folded":
                                    folded_fingers.append(finger_names[i])

                            folded_fingers_text = ", ".join(folded_fingers) if folded_fingers else "None"

                            if folded_fingers_text in sequence:
                                if folded_fingers_text == sequence[index]:
                                    index += 1
                                    if index >= len(sequence):
                                        loop += 1
                                        sequence = FingerTracking.generate_unique_sequence()
                                        index = 0
                                        start_time = time.time()
                            else:
                                cv2.putText(image, 'Wrong! Try Again.', (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv2.LINE_AA)

                            cv2.putText(image, f'Score: {loop}', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2, cv2.LINE_AA)
                            cv2.putText(image, f'Please hold: {", ".join(sequence[:index+1])}', (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2, cv2.LINE_AA)
                            cv2.putText(image, f'Folded Fingers: {folded_fingers_text}', (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2, cv2.LINE_AA)

                    Timer.draw_timer_bar(image, start_time, time_limit)

                    if (time.time() - start_time) > time_limit:
                        game_over = True

                else:
                    cv2.putText(image, 'Game Over!', (50, 220), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 3, cv2.LINE_AA)
                    cv2.putText(image, 'Press "r" to Restart or "q" to Quit.', (30, 280), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_AA)

                cv2.imshow('Hand Tracking Game', image)

                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    self.cap.release()
                    cv2.destroyAllWindows()
                    break
                elif key == ord('r') and game_over:
                    self.game_loop()
                    break

    def start_game(self):
        self.game_loop()

# Start the game
if __name__ == "__main__":
    game = HandTrackingGame()
    game.show_instructions()
    key = input("Press 'Y' to start the game or 'Q' to quit: ").strip().lower()
    if key == 'y':
        game.start_game()
