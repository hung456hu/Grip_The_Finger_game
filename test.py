import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import mediapipe as mp
import numpy as np
import random
import time

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Menu")

        # Set the window to fullscreen
        self.root.attributes('-fullscreen', True)

        # Title label with proper formatting
        self.title_label = tk.Label(self.root, text=self.get_title_text(), font=("Courier New", 16), justify="center")
        self.title_label.pack(pady=70, anchor="n")

        # Create a frame for the buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(side="bottom", pady=100)

        # Button properties
        button_font = ("Helvetica", 26)
        button_width = 18
        button_height = 2

        # Button text for English and Vietnamese
        self.button_texts = {
            'Play': {'English': 'Play', 'Vietnamese': 'Chơi'},
            'Settings': {'English': 'Settings', 'Vietnamese': 'Cài đặt'},
            'Quit': {'English': 'Quit', 'Vietnamese': 'Thoát'},
            'Select Language': {'English': 'Select Language', 'Vietnamese': 'Chọn ngôn ngữ'},
            'Back': {'English': 'Back', 'Vietnamese': 'Quay lại'},
            'Start Timer': {'English': 'Start Timer', 'Vietnamese': 'Bắt đầu hẹn giờ'},
            'Enter Timer Duration (seconds)': {'English': 'Enter Timer Duration (seconds)', 'Vietnamese': 'Nhập thời gian hẹn giờ (giây)'},
            'Play again' : {'English': 'Play again', 'Vietnamese': 'Chơi lại'},
            'Quit' : {'English': 'Quit', 'Vietnamese': 'Thoát'},
            'Folded Fingers' : {'English': 'Folded Fingers', 'Vietnamese': 'Ngón tay đang gập'},
            'Target Finger' : {'English': 'Target Finger', 'Vietnamese': 'Hãy gập ngón'},
            'Follow the sequence by folding the correct fingers at the bottom.' : {'English': 'Follow the sequence by folding the correct fingers at the bottom.', 'Vietnamese': 'Gập ngón tay ở vị trí dưới cùng để hoàn thành '},
            'Score' : {'English': 'Score', 'Vietnamese': 'Điểm số'},
            'Thumb' : {'English': 'Thumb', 'Vietnamese': 'Ngón cái'},
            'Index' : {'English': 'Index', 'Vietnamese': 'Ngón trỏ'},
            'Middle' : {'English': 'Middle', 'Vietnamese': 'Ngón giữa'},
            'Ring' : {'English': 'Ring', 'Vietnamese': 'Ngón áp út'},
            'Pinky' : {'English': 'Pinky', 'Vietnamese': 'Ngón út'},
        }

        # Initialize default language
        self.selected_language = "English"

        # Create buttons
        self.play_button = tk.Button(button_frame, text=self.button_texts['Play'][self.selected_language],
                                     font=button_font, command=self.open_play_window,
                                     width=button_width, height=button_height)
        self.play_button.pack(fill="x", pady=5)

        self.settings_button = tk.Button(button_frame, text=self.button_texts['Settings'][self.selected_language],
                                          font=button_font, command=self.open_settings,
                                          width=button_width, height=button_height)
        self.settings_button.pack(fill="x", pady=5)

        self.quit_button = tk.Button(button_frame, text=self.button_texts['Quit'][self.selected_language],
                                     font=button_font, command=self.quit_game,
                                     width=button_width, height=button_height)
        self.quit_button.pack(fill="x", pady=5)

    # Initialize MediaPipe hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.mp_draw = mp.solutions.drawing_utils
    # Initialize time-tracking variables
        self.last_finger_fold_time = time.time()
        self.sequence_hold_duration = 0.5  # seconds each finger must remain folded

    def get_title_text(self):
        return f"""\
     ██████╗ ██████╗ ██╗██████╗     ████████╗██╗  ██╗███████╗    ███████╗██╗███╗   ██╗ ██████╗ ███████╗██████╗
     ██╔════╝ ██╔══██╗██║██╔══██╗    ╚══██╔══╝██║  ██║██╔════╝    ██╔════╝██║████╗  ██║██╔════╝ ██╔════╝██╔══██╗
     ██║  ███╗██████╔╝██║██████╔╝       ██║   ███████║█████╗      █████╗  ██║██╔██╗ ██║██║  ███╗█████╗  ██████╔╝
     ██║   ██║██╔══██╗██║██╔═══╝        ██║   ██╔══██║██╔══╝      ██╔══╝  ██║██║╚██╗██║██║   ██║██╔══╝  ██╔══██╗
     ╚██████╔╝██║  ██║██║██║            ██║   ██║  ██║███████╗    ██║     ██║██║ ╚████║╚██████╔╝███████╗██║  ██║
      ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝            ╚═╝   ╚═╝  ╚═╝╚══════╝    ╚═╝     ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
        """        

    def open_play_window(self):
        self.play_window = tk.Toplevel(self.root)
        self.play_window.title("Play")
        self.play_window.attributes('-fullscreen', True)

        # Create a label for the timer input
        timer_label_text = self.button_texts['Enter Timer Duration (seconds)'][self.selected_language]
        timer_label = tk.Label(self.play_window, text=timer_label_text, font=("Helvetica", 24))
        timer_label.pack(pady=20)

        self.timer_entry = tk.Entry(self.play_window, font=("Helvetica", 24), justify="center")
        self.timer_entry.pack(pady=20)

        # Start Timer button
        start_button = tk.Button(self.play_window, text=self.button_texts['Start Timer'][self.selected_language],
                          font=("Helvetica", 24), command=lambda: (self.start_timer(),self.play_window.destroy))
        start_button.pack(pady=20)

        # Back button to return to the main menu
        back_button = tk.Button(self.play_window, text=self.button_texts['Back'][self.selected_language],
                                font=("Helvetica", 24), command=self.play_window.destroy)
        back_button.pack(pady=20)
        
    def start_timer(self):
        try:
            duration = int(self.timer_entry.get())
            self.timer_entry.delete(0, tk.END)

            # Create a new window for countdown and video feed
            self.timer_window = tk.Toplevel(self.root)
            self.timer_window.title("Timer and Video Feed")
            self.timer_window.attributes('-fullscreen', True)

            # Main frame to organize layout
            main_frame = tk.Frame(self.timer_window)
            main_frame.pack(expand=True, fill=tk.BOTH)

            # Timer label at the top center
            self.timer_label = tk.Label(main_frame, text="", font=("Helvetica", 48), fg="red")
            self.timer_label.pack(pady=(50, 20))

            # Frame for video feed on the left
            video_frame = tk.Frame(main_frame)
            video_frame.pack(side=tk.LEFT, padx=20, pady=50)

            # Label for the video feed on the left side
            self.video_frame = tk.Label(video_frame, width=640, height=480)
            self.video_frame.pack()

            # Label for showing score
            self.score_label = tk.Label(main_frame, text="Score: 0", font=("Helvetica", 24))
            self.score_label.pack(pady=(10, 10))

            # Label for showing game instructions above the folded fingers label
            instructions = self.button_texts['Follow the sequence by folding the correct fingers at the bottom.'][self.selected_language]
            self.instruction_label = tk.Label(main_frame, text=instructions, font=("Helvetica", 18), fg="blue")
            self.instruction_label.pack(pady=(10, 10))
            
            # Label for showing folded fingers and sequence
            self.folded_fingers_label = tk.Label(main_frame, text="", font=("Helvetica", 24))
            self.folded_fingers_label.pack(pady=(10, 50))
            
            # Initialize score and sequence
            self.score = 0
            self.target_sequence = self.generate_finger_sequence()
            self.sequence_index = 0
            self.update_score_display()

            # Initialize OpenCV
            self.vid = cv2.VideoCapture(0)

            # Start updating the video feed
            self.update_video_feed()

            # Back button at the bottom center
            back_button = tk.Button(main_frame, text=self.button_texts['Back'][self.selected_language],
                                    font=("Helvetica", 24), command=self.go_back)
            back_button.pack(side=tk.BOTTOM, pady=20)

            # Start countdown
            self.countdown(duration)

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number of seconds.")

    def generate_finger_sequence(self):
        thumb = self.button_texts['Thumb'][self.selected_language]
        index = self.button_texts['Index'][self.selected_language]
        middle = self.button_texts['Middle'][self.selected_language]
        ring = self.button_texts['Ring'][self.selected_language]
        pinky = self.button_texts['Pinky'][self.selected_language]
        fingers = [thumb, index, middle, ring, pinky]
        return random.sample(fingers, k=5)  # Generate a random sequence of 5 fingers

    def update_video_feed(self):
        ret, frame = self.vid.read()
        if ret:
            # Convert frame to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(frame_rgb)

            folded_fingers = ""
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_draw.draw_landmarks(frame_rgb, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    
                    # Detect folded fingers
                    folded_fingers = self.identify_folded_fingers(hand_landmarks)

                    # Check if folded fingers match the target sequence
                    self.check_finger_sequence(folded_fingers)

            # Update folded fingers and target finger display
            target_finger_text = f"{self.button_texts['Target Finger'][self.selected_language]}:\n\n" + "\n".join(self.target_sequence[:self.sequence_index + 1])
            text = f"{self.button_texts['Folded Fingers'][self.selected_language]}: {', '.join(folded_fingers)}\n\n{target_finger_text}"

            self.folded_fingers_label.config(text=text)

            # Convert frame to ImageTk for Tkinter display
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_frame.imgtk = imgtk
            self.video_frame.configure(image=imgtk)

        # Schedule the next frame update
        self.video_frame.after(10, self.update_video_feed)

    def identify_folded_fingers(self, hand_landmarks):
        # Determine if each finger is folded using landmark coordinates
        folded_fingers = []
        thumb_folded = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP].x < hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_MCP].x
        index_folded = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP].y > hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_MCP].y
        middle_folded = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP].y > hand_landmarks.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_MCP].y
        ring_folded = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.RING_FINGER_TIP].y > hand_landmarks.landmark[mp.solutions.hands.HandLandmark.RING_FINGER_MCP].y
        pinky_folded = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.PINKY_TIP].y > hand_landmarks.landmark[mp.solutions.hands.HandLandmark.PINKY_MCP].y

        # Append detected folded fingers
        if thumb_folded: folded_fingers.append(self.button_texts['Thumb'][self.selected_language])
        if index_folded: folded_fingers.append(self.button_texts['Index'][self.selected_language])
        if middle_folded: folded_fingers.append(self.button_texts['Middle'][self.selected_language])
        if ring_folded: folded_fingers.append(self.button_texts['Ring'][self.selected_language])
        if pinky_folded: folded_fingers.append(self.button_texts['Pinky'][self.selected_language])

        return folded_fingers

    def check_finger_sequence(self, folded_fingers):
        current_time = time.time()
        target_finger = self.target_sequence[self.sequence_index]  # Current target finger

        # Check if the correct finger is held
        if (target_finger in folded_fingers and
            current_time - self.last_finger_fold_time >= self.sequence_hold_duration):
            
            # Move to the next finger if matched
            self.sequence_index += 1
            self.last_finger_fold_time = current_time  # Reset hold timer

            # If sequence of 5 fingers is completed
            if self.sequence_index == len(self.target_sequence):
                self.score += 1  # Increment score
                self.sequence_index = 0  # Reset sequence index
                self.target_sequence = self.generate_finger_sequence()  # Generate new sequence
                self.update_score_display()

    def update_score_display(self):
        # Update score display label
        score_text = self.button_texts['Score'][self.selected_language]
        self.score_label.config(text=f"{score_text}: {self.score}")

    def go_back(self):
            if hasattr(self, 'vid'):
                self.vid.release()  # Release the webcam if it's open
            self.timer_window.destroy()  # Close the timer window

    def countdown(self, remaining):
        if remaining >= 0:
            self.timer_label.config(text=str(remaining))
            self.timer_window.after(1000, self.countdown, remaining - 1)
        else:
            # Release the webcam and close the timer window
            self.vid.release()
            self.timer_window.destroy()
            
            # Create the Game Over window
            self.show_game_over()

    def show_game_over(self):
        # Create a new Toplevel window for the Game Over screen
        game_over_window = tk.Toplevel(self.root)
        game_over_window.title("Game Over")
        game_over_window.attributes("-fullscreen", True)

        game_over_frame = tk.Frame(game_over_window)
        game_over_frame.pack(side="bottom", pady=100)

        button_font = ("Helvetica", 26)
        button_width = 18
        button_height = 2

        text_gameover = f"""\
██████╗  █████╗ ███╗   ███╗███████╗     ██████╗ ██╗   ██╗███████╗██████╗ 
██╔════╝ ██╔══██╗████╗ ████║██╔════╝    ██╔═══██╗██║   ██║██╔════╝██╔══██╗
██║  ███╗███████║██╔████╔██║█████╗      ██║   ██║██║   ██║█████╗  ██████╔╝
██║   ██║██╔══██║██║╚██╔╝██║██╔══╝      ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗
╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗    ╚██████╔╝ ╚████╔╝ ███████╗██║  ██║
 ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝     ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝
        """        

        # Display Game Over title
        tk.Label(game_over_window, text=text_gameover, font=("Courier New", 16)).pack(pady=70)
        
        # Play Again button
        play_again_button = tk.Button(
            game_over_frame,
            text=self.button_texts['Play again'][self.selected_language],
            command=lambda: self.restart_game(game_over_window),
            font=("Helvetica", 26),
            width=button_width, height=button_height
        )
        play_again_button.pack(pady=5)
        
        # Quit button
        quit_button = tk.Button(
            game_over_frame,
            text=self.button_texts['Quit'][self.selected_language],
            command=self.root.quit,
            font=("Helvetica", 26),
            width=button_width, height=button_height
        )
        quit_button.pack(pady=5)

    def restart_game(self, game_over_window):
        # Destroy the Game Over window and return to main menu
        game_over_window.destroy()

    def open_settings(self):
        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title("Settings")
        self.settings_window.attributes('-fullscreen', True)

        settings_frame = tk.Frame(self.settings_window)
        settings_frame.pack(side="bottom", pady=220)

        button_font = ("Helvetica", 26)
        button_width = 18
        button_height = 2

        lang_button = tk.Button(settings_frame, text=self.button_texts['Select Language'][self.selected_language],
                                font=button_font, command=self.open_language_selection,
                                width=button_width, height=button_height)
        lang_button.pack(pady=5)

        back_button = tk.Button(settings_frame, text=self.button_texts['Back'][self.selected_language],
                                font=button_font, command=self.settings_window.destroy,
                                width=button_width, height=button_height)
        back_button.pack(pady=5)

    def open_language_selection(self):
        lang_window = tk.Toplevel(self.root)
        lang_window.title("Select Language")
        lang_window.attributes('-fullscreen', True)

        lang_frame = tk.Frame(lang_window)
        lang_frame.pack(side="bottom", pady=100)

        button_font = ("Helvetica", 26)
        button_width = 18
        button_height = 2

        english_button = tk.Button(lang_frame, text="English", font=button_font,
                                   command=lambda: self.select_language("English"),
                                   width=button_width, height=button_height)
        english_button.pack(pady=5)

        vietnamese_button = tk.Button(lang_frame, text="Vietnamese", font=button_font,
                                       command=lambda: self.select_language("Vietnamese"),
                                       width=button_width, height=button_height)
        vietnamese_button.pack(pady=5)

        back_button = tk.Button(lang_frame, text=self.button_texts['Back'][self.selected_language],
                                font=button_font, command=lang_window.destroy,
                                width=button_width, height=button_height)
        back_button.pack(pady=5)

    def select_language(self, lang):
        self.selected_language = lang
        self.play_button.config(text=self.button_texts['Play'][self.selected_language])
        self.settings_button.config(text=self.button_texts['Settings'][self.selected_language])
        self.quit_button.config(text=self.button_texts['Quit'][self.selected_language])

    def quit_game(self):
        self.root.quit()

    def on_closing(self):
        if hasattr(self, 'vid'):
            self.vid.release()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    main_menu = MainMenu(root)
    root.protocol("WM_DELETE_WINDOW", main_menu.on_closing)
    root.mainloop()
