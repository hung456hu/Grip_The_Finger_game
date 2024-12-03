import cv2
import mediapipe as mp
import numpy as np
import math
import random
import time

class GameStartGUI:
    def __init__(self):
        self.window_name = "Grip The Finger Game - Start"
        self.start_game = False
        self.timer_options = [15, 30, 60]  # Timer options for 15, 30, and 60 seconds
        self.timer = self.timer_options[1]  # Default timer is 30 seconds

    def show_start_screen(self):
        """Display the start screen until 'S' is pressed to proceed to timer selection."""
        while True:
            start_screen = 255 * np.ones((480, 640, 3), dtype=np.uint8)  # white background
            cv2.putText(start_screen, 'Welcome to Grip The Finger Game', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            cv2.putText(start_screen, 'Press S to Start', (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            cv2.putText(start_screen, 'Press I for Instructions', (50, 350), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            cv2.putText(start_screen, 'Press Q to Quit', (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

            cv2.imshow(self.window_name, start_screen)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('s'):
                self.start_game = True
                cv2.destroyWindow(self.window_name)
                break
            elif key == ord('i'):
                self.show_instruction_screen()
            elif key == ord('q'):
                cv2.destroyAllWindows()
                exit()

    def show_instruction_screen(self):
        """Display the instruction screen."""
        while True:
            instruction_screen = 255 * np.ones((480, 640, 3), dtype=np.uint8)  # white background
            cv2.putText(instruction_screen, 'Game Instructions:', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            cv2.putText(instruction_screen, '1. Press S to Start the Game', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)
            cv2.putText(instruction_screen, '2. Choose the game duration', (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)
            cv2.putText(instruction_screen, '3. Fold the correct finger according to the ', (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)
            cv2.putText(instruction_screen, '   last rightmost position in the sequence', (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)
            cv2.putText(instruction_screen, '4. Press Q at any time to Quit', (50, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)
            cv2.putText(instruction_screen, 'Press B to go back', (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)

            cv2.imshow(self.window_name, instruction_screen)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('b'):  # Go back to main menu
                cv2.destroyWindow(self.window_name)
                break
    
    def select_timer(self):
        """Display timer selection screen after 'S' is pressed in start screen."""
        while True:
            timer_screen = 255 * np.ones((480, 640, 3), dtype=np.uint8)
            cv2.putText(timer_screen, 'Select Timer Duration', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            cv2.putText(timer_screen, f'Timer: {self.timer} seconds', (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            cv2.putText(timer_screen, 'Press 1 for 15s, 2 for 30s, 3 for 60s', (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)
            cv2.putText(timer_screen, 'Press Enter to confirm', (50, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)
            cv2.putText(timer_screen, 'Press B to go back to menu', (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)
            cv2.putText(timer_screen, 'Press Q to quit', (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)

            cv2.imshow(self.window_name, timer_screen)
            key = cv2.waitKey(1) & 0xFF  # Continuous check for key press

            if key == ord('q'):
                cv2.destroyAllWindows()
                exit()
            elif key == ord('b'):
                # Return to the main menu
                cv2.destroyWindow(self.window_name)
                self.start_game = False  # Reset start_game to False to go back to menu
                return None
            elif key == 13:  # Enter key
                cv2.destroyWindow(self.window_name)
                return self.timer
            elif key == ord('1'):
                self.timer = self.timer_options[0]  # 15 seconds
            elif key == ord('2'):
                self.timer = self.timer_options[1]  # 30 seconds
            elif key == ord('3'):
                self.timer = self.timer_options[2]  # 60 seconds

            # Clear the screen and update the timer display after selecting the timer
            timer_screen[:] = 255  # Reset the screen for fresh drawing each loop
            cv2.putText(timer_screen, f'Timer: {self.timer} seconds', (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

            cv2.imshow(self.window_name, timer_screen)

    def show_game_over_screen(self, score):
        """Display game over screen with options to replay or quit."""
        while True:
            game_over_screen = 255 * np.ones((480, 640, 3), dtype=np.uint8)
            cv2.putText(game_over_screen, 'Game Over!', (45, 150), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 2)
            cv2.putText(game_over_screen, f'Score: {score}', (215, 220), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)
            cv2.putText(game_over_screen, 'Press R to Replay or Q to Quit', (70, 350), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

            cv2.imshow(self.window_name, game_over_screen)
            key = cv2.waitKey(1) & 0xFF

            if key == ord('r'):  # Replay the game
                cv2.destroyWindow(self.window_name)
                return "replay"
            elif key == ord('q'):  # Quit the game
                cv2.destroyAllWindows()
                exit()

class HandTrackingGame:
    def __init__(self, time_limit, sequence_length=5):
        self.time_limit = time_limit
        self.sequence_length = sequence_length
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.cap = cv2.VideoCapture(0)
        self.reset_game()

    def reset_game(self):
        """Initialize game variables for a new round"""
        self.start_time = time.time()
        self.sequence = self.generate_unique_sequence()
        self.index = 0
        self.loop = 0
        self.game_over = False

    def calculate_distance(self, point1, point2, image_width, image_height):
        """Calculate Euclidean distance between two landmarks"""
        x1, y1 = int(point1.x * image_width), int(point1.y * image_height)
        x2, y2 = int(point2.x * image_width), int(point2.y * image_height)
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def draw_timer_bar(self, image):
        """Draws a timer bar showing remaining time"""
        elapsed_time = time.time() - self.start_time
        remaining_time = max(0, self.time_limit - elapsed_time)
        bar_fill = int((remaining_time / self.time_limit) * 400)
        cv2.rectangle(image, (50, 50), (450, 80), (200, 200, 200), -1)
        cv2.rectangle(image, (50, 50), (50 + bar_fill, 80), (0, 255, 0), -1)
        cv2.putText(image, f'Time Left: {int(remaining_time)}s', (60, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 5)
        cv2.putText(image, f'Time Left: {int(remaining_time)}s', (60, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    def generate_unique_sequence(self):
        """Generate a random sequence of unique finger names to fold"""
        finger_names = ["thumb", "index", "middle", "ring", "pinky"]
        return random.sample(finger_names, self.sequence_length)

    def check_folded_fingers(self, hand_landmarks, image_width, image_height):
        """Identify folded fingers based on hand landmarks"""
        folded_fingers = []
        
        thumb_tip = hand_landmarks.landmark[4]
        middle_base = hand_landmarks.landmark[9]
        distance_thumb_to_middle_base = self.calculate_distance(thumb_tip, middle_base, image_width, image_height)
        if distance_thumb_to_middle_base < 40:
            folded_fingers.append("thumb")

        fingertip_landmarks = [8, 12, 16, 20]  
        joint_landmarks = [6, 10, 14, 18]  
        finger_names = ["index", "middle", "ring", "pinky"]

        for i, fingertip in enumerate(fingertip_landmarks):
            y_tip = int(hand_landmarks.landmark[fingertip].y * image_height)
            y_joint = int(hand_landmarks.landmark[joint_landmarks[i]].y * image_height)
            if y_tip > y_joint:
                folded_fingers.append(finger_names[i])

        return folded_fingers

    def play(self):
        """Main game loop"""
        with self.mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    break

                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                results = hands.process(image)
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        self.mp_drawing.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                        image_width, image_height = image.shape[1], image.shape[0]
                        folded_fingers = self.check_folded_fingers(hand_landmarks, image_width, image_height)
                        folded_fingers_text = ", ".join(folded_fingers) if folded_fingers else "All fingers open"

                        if folded_fingers_text in self.sequence:
                            if folded_fingers_text == self.sequence[self.index]:
                                self.index += 1
                                if self.index >= len(self.sequence):
                                    self.loop += 1
                                    self.sequence = self.generate_unique_sequence()
                                    self.index = 0
                                    self.start_time = time.time()
                            else:
                                #outline
                                cv2.putText(image, 'Wrong! Try Again.', (25, 325), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 5)
                                cv2.putText(image, 'Wrong! Try Again.', (25, 325), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
                        #outline
                        cv2.putText(image, f'Score: {self.loop}', (25, 175), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 5)
                        cv2.putText(image, f'Score: {self.loop}', (25, 175), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
                        #outline 
                        cv2.putText(image, f'Sequence: {", ".join(self.sequence[:self.index+1])}', (25, 225), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 5)
                        cv2.putText(image, f'Sequence: {", ".join(self.sequence[:self.index+1])}', (25, 225), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
                        #outline
                        cv2.putText(image, f'Folded Fingers: {folded_fingers_text}', (25, 275), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 5)
                        cv2.putText(image, f'Folded Fingers: {folded_fingers_text}', (25, 275), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

                self.draw_timer_bar(image)

                if (time.time() - self.start_time) > self.time_limit:
                    self.cap.release()
                    cv2.destroyAllWindows()
                    return "game_over", self.loop 

                cv2.imshow('Hand Tracking Game', image)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    self.cap.release()
                    cv2.destroyAllWindows()
                    return "game_over", self.loop
    
if __name__ == "__main__":
    start_gui = GameStartGUI()

    while True:  # Continuous main loop
        start_gui.show_start_screen()
        
        if start_gui.start_game:
            timer = start_gui.select_timer()
            
            if timer is None:  # User pressed B to go back to menu
                continue  # Return to start screen
            
            # Start the game with selected timer
            game = HandTrackingGame(time_limit=timer)
            result, score = game.play()

            if result == "game_over":
                choice = start_gui.show_game_over_screen(score)
                if choice == "replay":
                    continue  # Go back to timer selection
                else:
                    break  # Exit the game if "quit"
            elif result == "back_to_timer":
                continue  # Return to timer selection if 'B' was pressed